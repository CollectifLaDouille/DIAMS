from functools import total_ordering
from typing import Dict, Union

from Configuration import CHOICE, EMAIL, PARTICIPANT_NAME, SELECTED_WORKSHOP, PREFERRED, UID
from WorkshopSlot import WorkshopSlot


@total_ordering
class Participant:

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

    def __hash__(self):
        return hash(str(self))


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
    def list(self) -> Dict[str, Union[int, str, str, bool, str, int]]:
        return {UID: hash(self), PARTICIPANT_NAME: self.name, EMAIL: self.email, PREFERRED: self.is_preferred,
                SELECTED_WORKSHOP: str(self.workshop), CHOICE: self.__current_choice}

