import datetime
import random
from copy import deepcopy
from pprint import pprint
from datetime import timedelta as td

from config import load_config
from config.config_data import *
from generators.eos_probability import generate_card_from_eos_model, generate_random_eos_list, T
from generators.phonecall_generator import generate_phone_data, generate_call_from_phone_call
from generators import check_event_probability
from schemas.string_eos import EOSType, consult, psycho
from schemas.ukio_model import Ukio, transferItem
from schemas.phonecall import phoneCall, redirectCall
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


def generate_transfer_items_by_ukio_cards(ukio_eos_cards: list[EOSType],
                                          transfer_date: datetime.datetime) -> list[transferItem]:
    transfers: list[transferItem] = []
    for eos in ukio_eos_cards:
        transfers.append(
            transferItem(
                eosClassTypeId=eos,
                dtTransfer=transfer_date,
                bSuccess=True
            )
        )
    return transfers


def generate_ukio_phone_call_data() -> Ukio:
    """
    creating ukio card with call_source = mobile phone
    :return: Ukio model
    """
    ukio_dict = {}
    card_state = random.choice(list(CardStates))
    incident_type = random.choice(list(IncidentType))
    call_source = CallSource.mobile_phone

    phone_calls: list[phoneCall] = generate_phone_data()
    eos_type_list = generate_random_eos_list()
    ukio_eos_cards = _check_ukio_cards(eos_type_list, phone_calls[-1].dtSend)
    if ukio_eos_cards:
        ukio_eos_card = ukio_eos_cards[random.choice(list(ukio_eos_cards.keys()))]
        if not isinstance(ukio_eos_card, psycho) and not isinstance(ukio_eos_card, consult):
            phone_calls[-1].RedirectCall = redirectCall(
                eosClassTypeId=ukio_eos_card.__class__.__name__,
                dtRedirectTime=ukio_eos_card.dtCreate + td(seconds=random.randint(10, 40)),
                dtRedirectConfirm=ukio_eos_card.dtCreate,
                redirectCancel=False,
                bConference=False,
                PhoneCallId=phone_calls[-1].phoneCallId
            )

    if check_event_probability(CHILD_PLAY_UKIO_PROBABILITY):
        ukio_dict['cardState'] = "child play"
        ukio_dict['bWrong'] = True
        ukio_dict['bChildPlay'] = True

    elif check_event_probability(WRONG_CALLS_PROBABILITY):
        ukio_dict['cardState'] = "wrong"
        ukio_dict['bWrong'] = True
        ukio_dict['bChildPlay'] = False

    else:
        ukio_dict['cardState'] = card_state
        ukio_dict['incidentType'] = incident_type
        ukio_dict['bWrong'] = False
        ukio_dict['bChildPlay'] = False
        ukio_dict |= ukio_eos_cards

    ukio_dict['callSource'] = call_source
    ukio_dict['dtSend'] = phone_calls[-1].dtSend
    ukio_dict['dtUpdate'] = phone_calls[-1].dtSend
    ukio_dict['dtCreate'] = phone_calls[-1].dtConnect

    ukio_dict['PhoneCall'] = []
    if phone_calls[-1].RedirectCall and not ukio_dict['bWrong']:
        # creating transfer item
        ukio_dict['TransferItem'] = generate_transfer_items_by_ukio_cards(eos_type_list, phone_calls[-1].dtSend)

        # we need to put the card with redirect to ukio
        ukio_dict['PhoneCall'] = [phone_calls[-1]]

        # card without redirect put to call
        phone_call_without_redirect = deepcopy(phone_calls[-1])
        phone_call_without_redirect.RedirectCall = None

        call = generate_call_from_phone_call(phone_call_without_redirect, rtype='structure')
    else:
        if check_event_probability(
                PHONE_CALL_STRUCTURE_PROBABILITY_IN_UKIO,
                PHONE_CALL_STRUCTURE_PROBABILITY_IN_UKIO):
            ukio_dict['PhoneCall'] = [phone_calls[0]]
            call = generate_call_from_phone_call(phone_calls[0], rtype='id')
        else:
            ukio_dict['PhoneCallID'] = [phone_calls[0].phoneCallId]
            call = generate_call_from_phone_call(phone_calls[0], rtype='structure')

        if len(phone_calls) > 1:
            middle_recalls = phone_calls[1:-1]
            ukio_dict['PhoneCall'].extend(middle_recalls)

    return Ukio(**ukio_dict), call


def main():
    for _ in range(1):
        d = generate_ukio_phone_call_data()
        pprint(d)
        # if d.get('Psycho') or d.get('Consult'):
        #     print(d)


if __name__ == '__main__':
    main()
