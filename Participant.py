from functools import total_ordering
from typing import Dict, Tuple

from Configuration import CHOICE, EMAIL, PARTICIPANT_NAME, SELECTED_WORKSHOP, PREFERRED
from WorkshopSlot import WorkshopSlot


@total_ordering
class Participant:

    LIST_HEADER = (PARTICIPANT_NAME, EMAIL, PREFERRED, SELECTED_WORKSHOP, CHOICE)

    __name = ""
    __email = ""
    __choices = {}
    __preferred = False
    __current_choice = 0

    def __init__(self, name: str, email: str, choices: Dict[int, WorkshopSlot], *_, preferred: bool=False):
        self.__name = name
        self.__email = email
        self.__choices = choices
        self.__preferred = preferred
        self.__current_choice = None

        return


    def __str__(self):
        return f"({self.__name}, {self.__email})"

    def __lt__(self, other):
        return self.__current_choice > other.__current_choice

    def __eq__(self, other):
        return self.__current_choice == other.__current_choice


    def get_workshop(self, choice: int=None) -> WorkshopSlot:
        if choice is None:
            choice = self.choice
        if choice in self.__choices:
            return self.__choices[choice]
        return None

    @property
    def workshop(self):
        return self.get_workshop()

    @property
    def choice(self) -> int:
        return self.__current_choice

    @choice.setter
    def choice(self, current_choice: int):
        if current_choice in self.__choices:
            self.__current_choice = current_choice
        else:
            self.__current_choice = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def is_preferred(self) -> bool:
        return self.__preferred

    @property
    def is_pleased(self) -> bool:
        return self.__current_choice is not None

    @property
    def list(self) -> Tuple[str, str, bool, str, int]:
        workshop_name = None if self.workshop is None else self.workshop.name
        return self.name, self.email, self.is_preferred, workshop_name, self.__current_choice

