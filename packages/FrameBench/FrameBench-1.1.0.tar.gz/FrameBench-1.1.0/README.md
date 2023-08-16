# Framebench
Framebench is a simple benchmark to capture frame times from video devices on Linux.

## Installation

To install Framebench, do the following steps:
1. Clone this repository
    - `git clone https://github.com/kdvalin/framebench.git`
2. Enter into the repository's directory
    - `cd framebench`
3. Install using `pip3`
    - `pip3 install .`
4. (Optional) Install package that contain v4l2-ctl, this is used to list capabilities of video devices
    - Fedora: `dnf install v4l-utils`

## Commands
### `list`
`framebench list` is used to list all video devices on a host and provide minimal information about
them.  An example can be seen below:

```
/dev/video5: UVC Camera (046d:0825)
/dev/video3: Integrated Camera: Integrated I
/dev/video1: Integrated Camera: Integrated C
/dev/video4: UVC Camera (046d:0825)
/dev/video2: Integrated Camera: Integrated I
/dev/video0: Integrated Camera: Integrated C
```

### `list -d <device>`
`framebench list -d <device>` is used to list the capabilities of a single video device (mainly what resolutions are supported at what framerate).

This command requires the binary `v4l2-ctl` to be installed and accessible on the system.

An example of the output of this command can be seen below

```
$ framebench list -d /dev/video0
ioctl: VIDIOC_ENUM_FMT
        Type: Video Capture

        [0]: 'MJPG' (Motion-JPEG, compressed)
                Size: Discrete 1280x720
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x180
                        Interval: Discrete 0.033s (30.000 fps)
...
        [1]: 'YUYV' (YUYV 4:2:2)
                Size: Discrete 640x480
                        Interval: Discrete 0.033s (30.000 fps)
                Size: Discrete 320x180
                        Interval: Discrete 0.033s (30.000 fps)
...
```

### `run <device>`
`framebench run <device>` is used to run a frame timing test on a specific camera.

Options:
```
-t, --test_time=<int>
    How long (in seconds) to run the test for (Default is 30)
-r, --resolution=<str>
    The desired resolution of the camera during the test, must be in WxH format. (Default is 640x480)
--framerate=<int>
    The desired framerate of the camera during the test.  (Default is 30)
--format=<str>
    The format to be used by the camera.  Must be 4 characters.
    Use the "list -d" command to validate what is supported by the camera.
    (Default is MJPG)
-o, --output=<str>
    File path to save the timings to (csv format)
    (Default is "timings.csv")
```

### `run_multiple <config>`
`framebench run_multiple <config>` is used to run a frame timing test on multiple cameras specified in a config file.

See [config.yaml] as an example of this configuration

Options:
```
-o, --output=<str>
    File path to save the timings to (csv format)
    (Default is "timings.csv")
```