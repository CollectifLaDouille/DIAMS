from pathlib import Path

PRIORITY_FILE_PATH = Path('FichierTypePrio.ods')
STANDARD_FILE_PATH = Path('FichierTypeStandard.ods')
OUTPUT_FILE_PATH = Path('Sortie.ods')

PRIORITY_CAPACITY_REDUCER = .5
STANDARD_CAPACITY_REDUCER = 1.
WORKSHOP_SHEET_NAME = "Ateliers"
CHOICES_SHEET_NAME = "Inscriptions"
SOLVED_SHEET_NAME = "Attributions"
UNSOLVED_SHEET_NAME = "Sans ateliers"
WORKSHOP_NAME = "Créneaux"
DESCRIPTION = "Description"
CAPACITY = "Places"
UID = "UID"
PARTICIPANT_NAME = "Prénom"
EMAIL = "Email"
CHOICE = "Voeu"
PREFERRED = "Prioritaire"
SELECTED_WORKSHOP = "Atelier attribué"
SEATS_TAKEN = "Places prises"
FREE_SEATS = "Places libres"

RANDOM_SEED = "douille"

class Ids:
    SMTP_SERVER = ""
    SMTP_PORT = 587
    SENDER_EMAIL = ""
    SENDER_EMAIL_PASSWORD = ""

