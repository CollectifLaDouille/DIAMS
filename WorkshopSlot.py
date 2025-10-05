from typing import List, Union, Dict

from typing_extensions import Self

from Configuration import WORKSHOP_NAME, SEATS_TAKEN, CAPACITY, FREE_SEATS, DESCRIPTION


class WorkshopSlot:

    __name = ""
    __description = ""
    __capacity = 0
    __capacity_percentage = .0
    __seats_taken = 0

    def __init__(self, name:str, description:str, capacity:int, capacity_percentage:float = .0):
        self.__name = name
        self.__description = description
        self.__capacity = capacity
        self.__capacity_percentage = capacity_percentage
        self.__seats_taken = 0

        return


    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


    def set_capacity_percentage(self, capacity_percentage:float):
        if capacity_percentage < self.__capacity_percentage:
            raise Exception(f"New value ({capacity_percentage}) can't be lower than current one ({self.__capacity_percentage})")
        else:
            self.__capacity_percentage = capacity_percentage


    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def real_capacity(self) -> int:
        return self.__capacity

    @property
    def capacity(self) -> int:
        return int(self.real_capacity * self.__capacity_percentage)

    @property
    def seats_taken(self) -> int:
        return self.__seats_taken

    @seats_taken.setter
    def seats_taken(self, seats:int):
        if seats < 0:
            raise Exception(f"Seats ({seats}) can't be negative")
        if seats > self.capacity:
            raise Exception(f"Seats ({seats}) can't be greater than capacity ({self.capacity})")
        self.__seats_taken = seats

    @property
    def is_full(self) -> bool:
        return self.__seats_taken >= self.capacity

    @property
    def list(self) -> Dict[str, Union[str, str, int, int, int]]:
        return {WORKSHOP_NAME: self.name, DESCRIPTION: self.description, CAPACITY: self.real_capacity,
                SEATS_TAKEN: self.seats_taken, FREE_SEATS: self.real_capacity - self.seats_taken}


    @staticmethod
    def get_workshop_from_name(workshops:List[Self], name:str):
        #TODO: go to 3.11 and change whileloop+typing+iterator (:=)
        for workshop in workshops:
            if workshop.name == name:
                return workshop
        return None

