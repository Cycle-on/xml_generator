import random
from pprint import pprint

from generators.eos_probability import generate_card_from_eos_model
from generators.phone_calls import generate_phone_data
from schemas.string_eos import EOSType
from schemas.models import Card
from schemas.phone import Phone
from schemas.string_schemas import IncidentType, CardStates, CallSource


def _check_ukio_cards(eos_list: list[EOSType]):
    eos_dict = {}

    for eos in eos_list:
        match eos:
            case EOSType.fireDepartment:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.police:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.ambulance:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.gasDepartment:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.houseDepartment:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.antiTerror:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.s112:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card
            case EOSType.psycho:
                card = generate_card_from_eos_model(eos)
                eos_dict[card.__class__.__name__.lower()] = card

    return eos_dict


def generate_ukio_phone_call_data():
    ukio_dict = {}
    card_state = list(CardStates)[random.randint(0, len(list(CardStates)) - 1)]
    incident_type = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]

    call_source = CallSource.mobile_phone
    phone_call: Phone = generate_phone_data()
    ukio_dict |= _check_ukio_cards(phone_call.operator.eosClassTypeId)

    # casualties = None  # get from config
    wrong = False
    child_play = False

    ukio_dict['cardState'] = card_state
    ukio_dict['incidentType'] = incident_type
    ukio_dict['dtSend_'] = phone_call.dtSend_
    ukio_dict['dtCreate'] = phone_call.dtEndCall_
    ukio_dict['callSource'] = call_source
    # ukio_dict['casualties'] = casualties
    ukio_dict['wrong'] = wrong
    ukio_dict['bChildPlay'] = child_play
    ukio_dict['phoneCalls'] = [phone_call]

    return Card(**ukio_dict)


def generate_card():
    pass


def main():
    generate_ukio_phone_call_data()


if __name__ == '__main__':
    main()
