import subprocess
import glob

def list_device_caps(device: str):
    subprocess.run(["v4l2-ctl", "-d", device, "--list-formats-ext"])

def list_cams(
        #List the capabilities of a single device (FPS/Resolution)
        device: str = ""
    ):
    """List devices or a device's capabilities

    Lists all known cameras on the system, or lists capabilities of a single camera
    :param device: Lists the capabilities of a single video device
    """
    if device != "":
        return list_device_caps(device)

    for cam_name in glob.glob("/sys/class/video4linux/video?/name"):
        video_num = cam_name.split('/')[-2]
        with open(cam_name, "r") as cam_info:
            info = ''.join(cam_info.readlines()).strip()
            print(f'/dev/{video_num}: {info}')
