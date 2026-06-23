import numpy as np

def grad2rad(grad: float) -> float:
    return (grad / 180) * np.pi

def rad2grad(rad: float) -> float:
    return (rad / np.pi) * 180

def get_distance(pos1: np.ndarray, pos2: np.ndarray) -> float:
    sum_sqr_dif: float = 0
    for p1, p2 in zip(pos1, pos2):
        sum_sqr_dif += (p1 - p2) * (p1 - p2)
    distance = np.sqrt(sum_sqr_dif)
    return distance