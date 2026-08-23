class Node:
    def __init__(self, id: int, weight: float, state: bool, radius: int):
        self.id: int = id
        self.weight: float = weight

        self.state: bool = state
        self.color = "white"

        self.center: list[int] = [0, 0]
        self.radius: int = radius

    def getId(self) -> int:
        return self.id

    def setId(self, new_id: int):
        self.id = new_id

    def getWeight(self) -> float:
        return self.weight

    def setWeight(self, new_weight: float):
        self.weight = new_weight

    def get_state(self) -> bool:
        return self.state

    def turn_on(self):
        self.state = 1

    def turn_off(self):
        self.state = 0

    def getCenter(self) -> list[int]:
        return self.center

    def setCenter(self, new_center: list[int]):
        self.center = new_center

    def getRadius(self) -> int:
        return self.radius

    def setRadius(self, new_radius: int):
        self.radius = new_radius
