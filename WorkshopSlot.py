from typing import List, Union, Dict

from Configuration import WORKSHOP_NAME, SEATS_TAKEN, CAPACITY, FREE_SEATS, DESCRIPTION


class WorkshopSlot:

    __name = ""
    __description = ""
    __capacity = 0
    __capacity_percentage = .0
    __seats_taken = 0

    def __init__(self, name:str, description:str, capacity:int, capacity_percentage:float = .0):
        """
        `WorkshopSlot` objects are used to store all infos on one workshop slot (one workshop can have multiple slots).
        It allows to quickly set and retrieve seats taken, with data validation.
        :param name: name of the workshop (must be unique).
        :param description: description of the workshop.
        :param capacity: number of free seats.
        :param capacity_percentage: used to virtually limit the number of free seats (see `set_capacity_percentage()`).
        """
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

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(str(self))


    def set_capacity_percentage(self, capacity_percentage:float):
        """
        Virtually change the capacity of the workshop slot. This helps to limit the available seats for the first pass,
        for example for the priority participants.
        :param capacity_percentage: Float between 0. and 1., must be greater than the previously set percentage.
        """
        if capacity_percentage < self.__capacity_percentage:
            raise Exception(f"New value ({capacity_percentage}) can't be lower than current one ({self.__capacity_percentage})")
        else:
            self.__capacity_percentage = capacity_percentage


    @property
    def name(self) -> str:
        """
        Get the name of the workshop slot.
        :return: str representing the name of the workshop slot
        """
        return self.__name

    @property
    def description(self) -> str:
        """
        Get the description of the workshop slot.
        :return: str representing the description of the workshop slot
        """
        return self.__description

    @property
    def real_capacity(self) -> int:
        """
        Get the real capacity (not affected by the limiting percentage) of the workshop slot.
        :return: int, the number of seats
        """
        return self.__capacity

    @property
    def capacity(self) -> int:
        """
        Get the capacity (affected by the limiting percentage) of the workshop slot.
        :return: int, the number of seats
        """
        return int(self.real_capacity * self.__capacity_percentage)

    @property
    def seats_taken(self) -> int:
        """
        Get the number of seats taken for this workshop slot.
        :return: int, number of seats taken
        """
        return self.__seats_taken

    @seats_taken.setter
    def seats_taken(self, seats:int):
        """
        Set the number of seats taken for this workshop slot.
        Seats can't be less than 0 and greater than the capacity.
        :param seats: int, number of seats taken.
        """
        if seats < 0:
            raise Exception(f"Seats ({seats}) can't be negative")
        if seats > self.capacity:
            raise Exception(f"Seats ({seats}) can't be greater than capacity ({self.capacity})")
        self.__seats_taken = seats

    @property
    def is_full(self) -> bool:
        """
        Whether the workshop slot is full or not.
        :return: bool, True if full, False if not.
        """
        return self.__seats_taken >= self.capacity

    @property
    def list(self) -> Dict[str, Union[str, str, int, int, int]]:
        """
        Create a dictionary with all useful information for this workshop slot.
        :return: Dict{name, description, capacity, real capacity, seats taken, free seats}
        """
        return {WORKSHOP_NAME: self.name, DESCRIPTION: self.description, CAPACITY: self.real_capacity,
                SEATS_TAKEN: self.seats_taken, FREE_SEATS: self.real_capacity - self.seats_taken}


def get_workshop_from_name(workshops:List[WorkshopSlot], name:str) -> WorkshopSlot | None:
    """
    Helper function used to search a specific `WorkshopSlot` by name, in a list of `WorkshopSlot`.
    :param workshops: the list of `WorkshopSlot` objects.
    :param name: the searched name.
    :return: the found `WorkshopSlot` object, or None if not found.
    """
    itr = iter(workshops)
    while (workshop := next(itr, None)) is not None:
        if workshop.name == name:
            return workshop
    return None

