from random import Random
from typing import List, Tuple

from Configuration import RANDOM_SEED
from Participant import Participant


def stable_matching_solver(participants:List[Participant], max_choices:int) -> Tuple[List[Participant], List[Participant]]:

    # Shuffles participants
    Random(RANDOM_SEED).shuffle(participants)

    # Go through each participants, in descending priority (as if it was sorted by priority)
    for priority in range(1, max_choices + 1):
        for participant in participants:
            # If the participant doesn't have any workshop yet
            if not participant.is_pleased:
                # And if the next higher priority workshop is not full
                wanted_workshop = participant.get_workshop(priority)
                if wanted_workshop is not None:  # Can be None if no good match found, poor participant :(
                    if not wanted_workshop.is_full:
                        # Then set that workshop to the participant choice, and take a seat !
                        participant.choice = priority
                        participant.workshop.seats_taken += 1
                    else:
                        # If it's full, lets have a battle !
                        # First, select all rivals (already in the desired workshop)
                        rivals = [rival for rival in participants if rival.workshop==wanted_workshop]
                        participant.choice = priority  # Only now set them to the desired workshop
                        rivals.append(participant)  # Add our fellow competitor at the end
                        rivals.sort(reverse=True)  # Fight ! (put the lowest priority at the end of the list)
                        rivals[-1].choice = None  # Bye bye, try again next loop turn ;)

    # Sort participants in two lists, depending whether or not they have a workshop
    pleased_participants = []
    sad_participants = []
    for participant in participants:
        if participant.is_pleased:
            pleased_participants.append(participant)
        else:
            sad_participants.append(participant)

    return pleased_participants, sad_participants

