import pandas as pd

from Configuration import PRIORITY_FILE_PATH, CHOICES_SHEET_NAME, WORKSHOP_SHEET_NAME, STANDARD_FILE_PATH, CHOICE, \
    WORKSHOP_NAME, DESCRIPTION, CAPACITY, PRIORITY_CAPACITY_REDUCER, PARTICIPANT_NAME, EMAIL, STANDARD_CAPACITY_REDUCER
from Participant import Participant
from WorkshopSlot import WorkshopSlot
from stableMatchingSolver import stable_matching_solver

if __name__ == "__main__":
    # Read workbook from files
    priority_workbook = pd.ExcelFile(PRIORITY_FILE_PATH)
    standard_workbook = pd.ExcelFile(STANDARD_FILE_PATH)

    # Select specific sheets, store them in dataframes
    workshops_df = pd.read_excel(priority_workbook, sheet_name=WORKSHOP_SHEET_NAME)
    priority_participants_df = pd.read_excel(priority_workbook, sheet_name=CHOICES_SHEET_NAME)
    standard_participants_df = pd.read_excel(standard_workbook, sheet_name=CHOICES_SHEET_NAME)

    # Detect the max possible number of choices made
    max_choices = max(sum(CHOICE in k for k in priority_participants_df.keys()),
                      sum(CHOICE in k for k in standard_participants_df.keys()))

    # Convert all three dataframe into lists of custom types
    workshops = []
    for _, w in workshops_df.iterrows():
        workshopSlot = WorkshopSlot(w[WORKSHOP_NAME], w[DESCRIPTION], w[CAPACITY], PRIORITY_CAPACITY_REDUCER)
        workshops.append(workshopSlot)

    priority_participants = []
    for  _, p in priority_participants_df.iterrows():
        choices = {}
        for choice in range(1, max_choices + 1):
            w_name = p.get(f'{CHOICE} {choice}', None)
            choices[choice] = WorkshopSlot.get_workshop_from_name(workshops, w_name)
        participant = Participant(p[PARTICIPANT_NAME], p[EMAIL], choices, preferred=True)
        priority_participants.append(participant)

    standard_participants = []
    for  _, p in standard_participants_df.iterrows():
        choices = {}
        for choice in range(1, max_choices + 1):
            w_name = p.get(f'{CHOICE} {choice}', None)
            choices[choice] = WorkshopSlot.get_workshop_from_name(workshops, w_name)
        participant = Participant(p[PARTICIPANT_NAME], p[EMAIL], choices)
        standard_participants.append(participant)

    # Run matching algorithm on priority participants
    p_pleased, p_sad = stable_matching_solver(priority_participants, max_choices)

    # Change workshops capacity (if needed)
    for w in workshops:
        w.set_capacity_percentage(STANDARD_CAPACITY_REDUCER)

    # Rerun matching algorithm on standard participants
    s_pleased, s_sad = stable_matching_solver(standard_participants, max_choices)

    # Merge participants
    pleased = p_pleased + s_pleased
    sad = p_sad + s_sad

    # Convert it back to dataframe
    workshops_df = pd.DataFrame([w.list for w in workshops], columns=WorkshopSlot.LIST_HEADER)
    pleased_df = pd.DataFrame([p.list for p in pleased], columns=Participant.LIST_HEADER)
    sad_df = pd.DataFrame([p.list for p in sad], columns=Participant.LIST_HEADER)


    print(workshops_df)
    print(pleased_df)
    print(sad_df)

