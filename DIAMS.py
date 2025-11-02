import pandas as pd

from Configuration import STANDARD_CAPACITY_REDUCER, PRIORITY_CAPACITY_REDUCER, Ids
from MailingMachine import MailingMachine
from WorkbookWorm import read_and_convert_from_workbook, write_to_workbook, read_from_workbook
from stableMatchingSolver import stable_matching_solver

RUN_DIAMS = True
SEND_EMAILS = False

if __name__ == "__main__":
    workshops, priority_participants, standard_participants, max_choices = read_and_convert_from_workbook()
    pleased_df = None
    sad_df = None

    if RUN_DIAMS:
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
        workshops_df = pd.DataFrame([w.list for w in workshops])
        pleased_df = pd.DataFrame([p.list for p in pleased])
        sad_df = pd.DataFrame([p.list for p in sad])


        # Print & write to file
        print(workshops_df)
        print(pleased_df)
        print(sad_df)
        write_to_workbook(workshops_df, pleased_df, sad_df)


    if SEND_EMAILS:
        if pleased_df is None or sad_df is None:
            workshops_df, pleased_df, sad_df = read_from_workbook()

        errors = 0
        mm = MailingMachine(Ids, workshops)
        errors += mm.send_dataframe(pleased_df)
        errors += mm.send_dataframe(sad_df)
        print(f"Finished with {errors} errors !")

