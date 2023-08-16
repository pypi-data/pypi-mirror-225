from .models import config
from .test import CamTest

import logging
import csv
import time

from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process, Queue

import yaml
import pandas as pd

READY_MEM_NAME="framebench_all_ready"
READY_MEM_SIZE=1

def _run_test(device: str, queue: Queue, test_time: int = 30, resolution="640x480", framerate=30, format="MJPG"):
    test = CamTest(device, resolution, framerate, format, test_time)
    queue.put('ready')
    
    # Wait for all processes to be ready
    mem = SharedMemory(name=READY_MEM_NAME, create=False, size=READY_MEM_SIZE)
    while mem.buf[0] != 1:
        time.sleep(0.066)
    mem.close()
    test.run()
    queue.put(test.get_result())
    queue.close()
    

def run(device: str, test_time: int = 30, resolution="640x480", framerate=30, format="MJPG", output="timings.csv"):
    """Run benchmark with the provided device

    :param device: The video device which will be used.
    :param test_time: The time (in seconds) to run the benchmark for.
    :param resolution: The desired resolution of the camera
    :param framerate: The desired framerate of the camera
    :param format: The format to be used (must be 4 characters, use `list` to validate what is supported on a camera)
    """
    test = CamTest(device, resolution, framerate, format, test_time)
    test.run()

    df = pd.DataFrame(test.get_result())
    df = df.transpose()
    df.to_csv(output, index=False, header=False)

def run_multiple(config_path: str, output: str = "timings.csv"):
    """Run benchmark with multiple devices.

    :param config_path: Path to a YAML file containing the device configurations
        (if non-required options are not provided, their defaults are the same as in test)
    :param output: The file to be used to save the timing results
    """
    cols = []
    process_list = []

    with open(config_path, 'r') as config_file:
        config_obj: config.Config = config.Config.parse_obj(yaml.safe_load(config_file))
 
    ready_mem = SharedMemory(name=READY_MEM_NAME, create=True, size=READY_MEM_SIZE)
    ready_mem.buf[0] = 0
    results_queue = Queue()

    for cam in config_obj.cams:
        cam_process = Process(
            target=_run_test,
            args=(
                cam.path,
                results_queue,
                config_obj.test_time,
                cam.resolution,
                cam.framerate,
                cam.stream_format,
            )
        )

        cam_process.start()
        process_list.append(
            cam_process
        )
    
    # Wait for all processes to be ready
    for process in process_list:
        results_queue.get()
    ready_mem.buf[0] = 1

    for process in process_list: # Grab the results when they come in
        cols.append(results_queue.get())
    
    df = pd.DataFrame(cols)
    df.to_csv(output, index=False, header=False)
    ready_mem.unlink()
    results_queue.close()
