import numpy as np

def grad2rad(grad: float) -> float:
    return (grad / 180) * np.pi

def rad2grad(rad: float) -> float:
    return (rad / np.pi) * 180