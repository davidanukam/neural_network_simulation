class Node:
    def __init__(self, id: int, weight: float, radius: int):
        self.id = id
        self.weight = weight
        self.center: tuple = (0, 0)
        self.radius: int = radius

    def getId(self) -> int:
        return self.id

    def setId(self, new_id: int) -> int:
        self.id = new_id

    def getWeight(self) -> float:
        return self.weight

    def setWeight(self, new_weight: float) -> float:
        self.weight = new_weight

    def getCenter(self) -> tuple:
        return self.center

    def setCenter(self, new_center: tuple):
        self.center = new_center

    def getRadius(self) -> int:
        return self.radius

    def setRadius(self, new_radius: int):
        self.radius = new_radius
