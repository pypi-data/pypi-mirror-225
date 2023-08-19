from __future__ import annotations
import numpy as np
from typing import Callable

class BoundFunction:   
    def __init__(self, parent_fn: Callable, x_min: float, x_max: float) -> None:
        
        self.parent_fn = parent_fn
        self.x_min = x_min
        self.x_max = x_max
        
    def __call__(self, x: np.ndarray):
        x = np.clip(x, self.x_min, self.x_max)
        return self.parent_fn(x)
    
    
        
        