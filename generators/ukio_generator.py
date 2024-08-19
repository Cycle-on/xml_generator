import datetime
import random
from pprint import pprint
from datetime import timedelta as td

from config import load_config
from generators.eos_probability import generate_card_from_eos_model, generate_random_eos_list, T
from generators.phone_calls import generate_phone_data, generate_call_from_phone_call
from schemas.string_eos import EOSType, consult, psycho
from schemas.ukio_model import Ukio
from schemas.phonecall import PhoneCall, RedirectCall, Calls, Call
from schemas.string_schemas import IncidentType, CardStates, CallSource

config = load_config()


def _check_ukio_cards(
        eos_list: list[EOSType],
        dt_send: datetime.datetime = datetime.datetime.now()
) -> dict[str, T]:
    """
    convert eos_dict to the pydantic model / from eos_for_ukio_models
    :param eos_list: list with eos_dicts from string_eos(can be created in generate_random_eos_list())
    :param dt_send: ukio card date_send
    :return:  dict with eos_models
    """
    eos_dict = {}
    for eos in eos_list:
        card = generate_card_from_eos_model(eos, dt_send)
        eos_dict[card.__class__.__name__.capitalize()] = card

    return eos_dict


def generate_ukio_phone_call_data() -> Ukio:
    """
    creating ukio card with call_source = mobile phone
    :return: Ukio model
    """
    ukio_dict = {}
    card_state = random.choice(list(CardStates))
    incident_type = random.choice(list(IncidentType))
    call_source = CallSource.mobile_phone

    phone_calls: list[PhoneCall] = generate_phone_data()

    ukio_eos_cards = _check_ukio_cards(generate_random_eos_list(), phone_calls[-1].dtSend)
    if ukio_eos_cards:
        ukio_eos_card = ukio_eos_cards[random.choice(list(ukio_eos_cards.keys()))]
        if not isinstance(ukio_eos_card, psycho) and not isinstance(ukio_eos_card, consult):
            phone_calls[-1].RedirectCall = RedirectCall(
                eosClassTypeId=ukio_eos_card.__class__.__name__,
                dtRedirectTime=ukio_eos_card.dtCreate + td(seconds=random.randint(10, 40)),
                dtRedirectConfirm=ukio_eos_card.dtCreate,
                redirectCancel=False,
                bConference=False,
                PhoneCallId=phone_calls[-1].phoneCallId
            )

    ukio_dict |= ukio_eos_cards

    wrong = False
    child_play = False

    ukio_dict['cardState'] = card_state
    ukio_dict['incidentType'] = incident_type
    ukio_dict['dtSend'] = phone_calls[-1].dtSend
    ukio_dict['dtUpdate'] = phone_calls[-1].dtSend
    ukio_dict['dtCreate'] = phone_calls[-1].dtConnect
    ukio_dict['callSource'] = call_source
    ukio_dict['wrong'] = wrong
    ukio_dict['bChildPlay'] = child_play

    ukio_dict['phoneCall'] = phone_calls
    ukio_dict['PhoneCallID'] = [phone_call.phoneCallId for phone_call in phone_calls]

    return Ukio(**ukio_dict), generate_call_from_phone_call(phone_calls[0])


def main():
    for _ in range(1):
        d = generate_ukio_phone_call_data()
        pprint(d)
        # if d.get('Psycho') or d.get('Consult'):
        #     print(d)


if __name__ == '__main__':
    main()
