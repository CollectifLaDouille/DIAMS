from pathlib import Path

PRIORITY_FILE_PATH = Path('FichierTypePrio.ods')
STANDARD_FILE_PATH = Path('FichierTypeStandard.ods')
OUTPUT_FILE_PATH = Path('Sortie.ods')

PRIORITY_CAPACITY_REDUCER = .5  # Preferred participants only have access to 50% of the slots capacity.
STANDARD_CAPACITY_REDUCER = 1.  # Normal participants have access to 100% of the slots capacity.
RANDOM_SEED = "douille"  # Random seed for the initial shuffling

# Sheets names
WORKSHOP_SHEET_NAME = "Ateliers"        # I/O
CHOICES_SHEET_NAME = "Inscriptions"     # I
SOLVED_SHEET_NAME = "Attributions"      # O
UNSOLVED_SHEET_NAME = "Sans ateliers"   # O
# Columns names
WORKSHOP_NAME = "Créneaux"              # I/O
DESCRIPTION = "Description"             # I/O
CAPACITY = "Places"                     # I/O
UID = "UID"                             # O
PARTICIPANT_NAME = "Prénom"             # I/O
EMAIL = "Email"                         # I/O
CHOICE = "Voeu"                         # I/O
PREFERRED = "Prioritaire"               # O
SELECTED_WORKSHOP = "Atelier attribué"  # O
SEATS_TAKEN = "Places prises"           # O
FREE_SEATS = "Places libres"            # O

# Connection details for the mail server
class Ids:
    SMTP_SERVER = ""
    SMTP_PORT = 587
    SENDER_EMAIL = ""
    SENDER_EMAIL_PASSWORD = ""

