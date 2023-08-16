from typing import List
import pydantic

class CamConfig(pydantic.BaseModel):
    path: str
    framerate: int = 30
    resolution: str = "640x480"
    stream_format: str = "MJPG"

class Config(pydantic.BaseModel):
    test_time: int = 30
    cams: List[CamConfig]
