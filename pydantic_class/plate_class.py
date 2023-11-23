from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any


class Box(BaseModel):
    xmax: int
    xmin: int
    ymax: int
    ymin: int

class PlateInfo(BaseModel):
    plate: str
    box: Box
    score: float

