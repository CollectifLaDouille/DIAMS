import pandas as pd

from Configuration import STANDARD_CAPACITY_REDUCER, PRIORITY_CAPACITY_REDUCER
from Participant import Participant
from WorkbookWorm import read_and_convert_from_workbook, write_to_workbook
from WorkshopSlot import WorkshopSlot
from stableMatchingSolver import stable_matching_solver

if __name__ == "__main__":
    workshops, priority_participants, standard_participants, max_choices = read_and_convert_from_workbook()

    # Change workshops capacity (if needed)
    for w in workshops:
        w.set_capacity_percentage(PRIORITY_CAPACITY_REDUCER)

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


    # Print & write to file
    print(workshops_df)
    print(pleased_df)
    print(sad_df)
    write_to_workbook(workshops_df, pleased_df, sad_df)

