from distutils.core import setup

setup(
    name="FrameBench",
    description="A Benchmark for measuring frame timings from multiple cameras simultaneously",
    version="1.1.0",
    author="Keith Valin",
    author_email="kvalin@redhat.com",
    license="GPL-3.0",
    url="https://github.com/kdvalin/framebench",
    download_url="https://github.com/kdvalin/framebench/archive/refs/tags/v1.0.1.tar.gz",
    keywords=["camera", "webcam", "framebench", "test", "benchmark", "frame timings"],
    packages=["framebench", "framebench.models"],
    install_requires = [
        "opencv-python",
        "fire",
        "pillow",
        "pyyaml",
        "pydantic",
        "pandas"
    ],
    entry_points = {
        "console_scripts": [
            "framebench = framebench.main:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Benchmark",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8"
    ]
)
