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
        """
        `Participant` objects are used to store all infos on one participant.
        It allows to quickly store and retrieve selected workshop, with data validation.
        :param name: Name of the participant.
        :param email: Email of the participant.
        :param choices: List of workshop choices (with `WorkshopSlot` objects).
        :param preferred: Is it a priority participant.
        """
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


    def get_workshop(self, choice: int=None) -> WorkshopSlot | None:
        """
        Get the `choice`th workshop for this participant.
        If choice is None, return the current selected choice.
        If no workshop choice were made, return None.
        :param choice: int from 0 to `max_choices` or None.
        :return: `WorkshopSlot` or None if not found
        """
        if choice is None:
            choice = self.choice
        if choice in self.__choices:
            return self.__choices[choice]
        return None

    @property
    def workshop(self) -> WorkshopSlot | None:
        """
        Get the current selected workshop for this participant.
        :return: `WorkshopSlot` or None if none was selected
        """
        return self.get_workshop()

    @property
    def choice(self) -> int:
        """
        Get the current choice number for this participant.
        :return: int
        """
        return self.__current_choice

    @choice.setter
    def choice(self, current_choice: int):
        """
        Set the current choice number for this participant.
        :param current_choice: int, must be in participant's list, or will be stored as None.
        """
        if current_choice in self.__choices:
            self.__current_choice = current_choice
        else:
            self.__current_choice = None

    @property
    def name(self) -> str:
        """
        Get the name of the participant.
        :return: str representing the name of the participant
        """
        return self.__name

    @property
    def email(self) -> str:
        """
        Get the email of the participant.
        :return: str representing the email of the participant
        """
        return self.__email

    @property
    def is_preferred(self) -> bool:
        """
        Whether the participant is preferred or not (on priority list).
        :return: bool, True if on priority list
        """
        return self.__preferred

    @property
    def is_pleased(self) -> bool:
        """
        Whether this participant has a workshop.
        :return: bool, True if this participant has a workshop
        """
        return self.__current_choice is not None

    @property
    def list(self) -> Dict[str, Union[int, str, str, bool, str, int]]:
        """
        Create a dictionary with all useful information for this participant.
        :return: Dict{UID, name, email, workshop, preferred, workshop, choice number}
        """
        return {UID: hash(self), PARTICIPANT_NAME: self.name, EMAIL: self.email, PREFERRED: self.is_preferred,
                SELECTED_WORKSHOP: str(self.workshop), CHOICE: self.__current_choice}

