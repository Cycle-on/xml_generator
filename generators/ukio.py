import random

from generators.phone_calls import generate_phone_data
from schemas import EOSType
from schemas.phone import Phone
from schemas.string_schemas import IncidentType, CardStates, CallSource


def _check_ukio_cards(eos_list: list[EOSType]):
    for eos in eos_list:
        match eos:
            case EOSType.fireDepartment:
                pass
            case EOSType.police:
                pass
            case EOSType.ambulance:
                pass
            case EOSType.gasDepartment:
                pass
            case EOSType.houseDepartment:
                pass
            case EOSType.antiTerror:
                pass
            case EOSType.s112:
                pass
            case EOSType.psycho:
                pass


def generate_other_ukio_phone_call_data():
    call_source = CallSource.mobile_phone

    card_state = list(CardStates)[random.randint(0, len(list(CardStates)) - 1)]
    incident_type = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]
    casualties = None  # get from config
    wrong = False
    child_play = False
    phone_call: Phone = generate_phone_data()
    _check_ukio_cards(phone_call.operator.eosClassTypeId)


def generate_card():
    pass


def main():
    generate_other_ukio_phone_call_data()


if __name__ == '__main__':
    main()
