import random
from pprint import pprint

from generators.eos_probability import generate_card_from_eos_model, generate_random_eos_list
from generators.phone_calls import generate_phone_data
from schemas.string_eos import EOSType
from schemas.models import Ukio
from schemas.phonecall import PhoneCall
from schemas.string_schemas import IncidentType, CardStates, CallSource


def _check_ukio_cards(eos_list: list[EOSType]):
    eos_dict = {}
    for eos in eos_list:
        card = generate_card_from_eos_model(eos)
        eos_dict[card.__class__.__name__.capitalize()] = card

    return eos_dict


def generate_ukio_phone_call_data():
    ukio_dict = {}
    card_state = list(CardStates)[random.randint(0, len(list(CardStates)) - 1)]
    incident_type = list(IncidentType)[random.randint(0, len(list(IncidentType)) - 1)]

    call_source = CallSource.mobile_phone
    phone_call: PhoneCall = generate_phone_data()

    ukio_dict |= _check_ukio_cards(generate_random_eos_list())

    # casualties = None  # get from config
    wrong = False
    child_play = False

    ukio_dict['cardState'] = card_state
    ukio_dict['incidentType'] = incident_type
    ukio_dict['dtSend'] = phone_call.dtSend
    ukio_dict['dtCreate'] = phone_call.dtEndCall
    ukio_dict['callSource'] = call_source
    ukio_dict['wrong'] = wrong
    ukio_dict['bChildPlay'] = child_play
    ukio_dict['phoneCalls'] = [phone_call]

    return Ukio(**ukio_dict)


def generate_card():
    pass


def main():
    for _ in range(1_000_000):
        d = generate_ukio_phone_call_data().dict()
        # if d.get('Psycho') or d.get('Consult'):
        #     print(d)


if __name__ == '__main__':
    main()
