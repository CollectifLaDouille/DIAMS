from typing import Tuple, List

import pandas as pd

from Configuration import PRIORITY_FILE_PATH, STANDARD_FILE_PATH, WORKSHOP_SHEET_NAME, CHOICES_SHEET_NAME, CHOICE, \
    WORKSHOP_NAME, DESCRIPTION, CAPACITY, PARTICIPANT_NAME, EMAIL, UNSOLVED_SHEET_NAME, \
    SOLVED_SHEET_NAME, OUTPUT_FILE_PATH
from Participant import Participant
from WorkshopSlot import WorkshopSlot, get_workshop_from_name


def read_and_convert_from_workbook() -> Tuple[List[WorkshopSlot], List[Participant], List[Participant], int]:
    """
    Calls to `get_dataframes()`, retrieves dataframes from the two workbooks and
    converts them into `WorkshopSlot` and `Participant` (standard+priority) objects with
    `convert_workshops()` and `convert_participants()`.
    :return: `WorkshopSlot`, `Participant` (priority), `Participant` (standard), number of possible choices
    """
    workshops_df, priority_participants_df, standard_participants_df = get_dataframes()

    max_choices = max(get_max_choices(priority_participants_df), get_max_choices(standard_participants_df))

    # Convert all three dataframes into lists of custom types
    workshops = convert_workshops(workshops_df)
    priority_participants = convert_participants(priority_participants_df, workshops, max_choices, preferred=True)
    standard_participants = convert_participants(standard_participants_df, workshops, max_choices)

    return workshops, priority_participants, standard_participants, max_choices


def convert_workshops(workshops_df: pd.DataFrame) -> List[WorkshopSlot]:
    """
    Convert a dataframe into a `WorkshopSlot` object, using column names from Configuration file.
    :param workshops_df: the workshops dataframe directly read from workbook.
    :return: `WorkshopSlot` object
    """
    workshops = []
    for _, w in workshops_df.iterrows():
        workshopSlot = WorkshopSlot(w[WORKSHOP_NAME], w[DESCRIPTION], w[CAPACITY])
        workshops.append(workshopSlot)
    return workshops


def convert_participants(participants_df: pd.DataFrame, workshops: List[WorkshopSlot], max_choices: int, **kwargs) -> List[Participant]:
    """
    Convert a dataframe into a List of `Participant` object, using column names from Configuration file.
    :param participants_df: the participants dataframe directly read from workbook.
    :param workshops: the corresponding `WorkshopSlot` object.
    :param max_choices: number of possible choices.
    :param kwargs: used to pass additional arguments to the `Participant` object (like `preferred=True`).
    :return: `Participant` object
    """
    participants = []
    for _, p in participants_df.iterrows():
        choices = {}
        for choice in range(1, max_choices + 1):
            w_name = p.get(f'{CHOICE} {choice}', None)
            choices[choice] = get_workshop_from_name(workshops, w_name)
        participant = Participant(p[PARTICIPANT_NAME], p[EMAIL], choices, **kwargs)
        participants.append(participant)
    return participants


def get_max_choices(participants_df: pd.DataFrame) -> int:
    """
    Detect the max possible number of choices made.
    :param participants_df: the participants dataframe directly read from workbook.
    :return: number of possible choices
    """
    max_choices = sum(CHOICE in k for k in participants_df.keys())

    return max_choices


def get_dataframes() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Reads workbooks from the files specified in Configuration file. Convert them in DataFrame.
    :return: three Dataframes: `workshops`, `priority_participants`, and `standard_participants`
    """
    # Read workbook from files
    priority_workbook = pd.ExcelFile(PRIORITY_FILE_PATH)
    standard_workbook = pd.ExcelFile(STANDARD_FILE_PATH)

    # Select specific sheets, store them in dataframes
    workshops_df = pd.read_excel(priority_workbook, sheet_name=WORKSHOP_SHEET_NAME)
    priority_participants_df = pd.read_excel(priority_workbook, sheet_name=CHOICES_SHEET_NAME)
    standard_participants_df = pd.read_excel(standard_workbook, sheet_name=CHOICES_SHEET_NAME)

    return workshops_df, priority_participants_df, standard_participants_df


def write_to_workbook(workshops_df: pd.DataFrame, pleased_df: pd.DataFrame, sad_df: pd.DataFrame):
    """
    Write DataFrame to workbook file, at specified sheet names in Configuration file.
    :param workshops_df: the workshops dataframe directly read from workbook.
    :param pleased_df: the participants that have a workshop
    :param sad_df: the participants that does not have a workshop.
    """
    with pd.ExcelWriter(OUTPUT_FILE_PATH, engine='odf', mode='w') as writer:

        workshops_df.to_excel(writer, sheet_name=WORKSHOP_SHEET_NAME, index=False)
        pleased_df.to_excel(writer, sheet_name=SOLVED_SHEET_NAME, index=False)
        sad_df.to_excel(writer, sheet_name=UNSOLVED_SHEET_NAME, index=False)


def read_from_workbook() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Read back from output workbook file, and store the data in DataFrames (specified in Configuration file).
    :return: three Dataframes: `workshops`, `pleased_participants`, and `sad_participants`
    """
    # Read workbook from file
    output_workbook = pd.ExcelFile(OUTPUT_FILE_PATH)

    # Select specific sheets, store them in dataframes
    workshops_df = pd.read_excel(output_workbook, sheet_name=WORKSHOP_SHEET_NAME)
    pleased_participants_df = pd.read_excel(output_workbook, sheet_name=SOLVED_SHEET_NAME)
    sad_participants_df = pd.read_excel(output_workbook, sheet_name=UNSOLVED_SHEET_NAME)

    return workshops_df, pleased_participants_df, sad_participants_df

