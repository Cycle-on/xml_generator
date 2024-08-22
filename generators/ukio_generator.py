import datetime
import random
from copy import deepcopy
from pprint import pprint
from datetime import timedelta as td

import numpy as np

from config import load_config
from config.config_data import *
from generators.eos_probability import generate_card_from_eos_model, generate_random_eos_list, T
from generators.phonecall_generator import generate_phone_data, generate_phone_date
from generators import check_event_probability
from schemas.string_eos import EOSType, consult, psycho
from schemas.ukio_model import Ukio, transferItem
from schemas.phonecall import phoneCall, redirectCall, Call
from schemas.string_schemas import IncidentType, CardStates, CallSource

config = load_config()


def generate_phonecall_from_redirect(dt_call: datetime.datetime) -> phoneCall:
    dt_call, dt_connect, dt_end_call, date_send = generate_phone_date(
        dt_call=dt_call
    )
    return phoneCall(
        dtSend=date_send,
        bOperatorIniciatied=True,
        dtCall=dt_call,
        dtConnect=dt_connect,

    )


def generate_call_from_phone_call(phone_call: phoneCall | datetime.datetime, rtype='') -> Call:
    if rtype == 'wrong':
        return Call(
            strCallStatus='status1',
            dtCall=phone_call,
        )

    phone_call_without_end_params = deepcopy(phone_call)

    phone_call_without_end_params.aCallEnded = None
    phone_call_without_end_params.bCallEnded = None
    phone_call_without_end_params.RedirectCall = None
    phone_call_without_end_params.dtEndCall = None
    phone_call_without_end_params.bOperatorIniciatied = None

    return Call(
        strCallStatus=random.choice(list(CardStates)),
        PhoneCall=phone_call_without_end_params,
        dtCall=phone_call.dtCall,
        dtSend=phone_call.dtCall + td(seconds=random.randint(3, 10))
    )


def _check_ukio_cards(
        eos_list: list[EOSType],
        dt_send: datetime.datetime
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


def generate_transfer_items_by_ukio_cards(eos_id: str,
                                          transfer_date: datetime.datetime) -> transferItem:
    return transferItem(
        eosClassTypeId=eos_id,
        dtTransfer=transfer_date,
        bSuccess=True
    )


def generate_ukio_phone_call_data(call_date: datetime.datetime) -> Ukio:
    """
    creating ukio card with call_source = mobile phone
    :return: Ukio model
    """
    ukio_dict = {}
    card_state = random.choice(list(CardStates))
    incident_type = random.choice(list(IncidentType))
    call_source = CallSource.mobile_phone

    phone_calls: list[phoneCall] = generate_phone_data(call_date)
    eos_type_list = generate_random_eos_list()
    ukio_eos_cards = _check_ukio_cards(eos_type_list, phone_calls[-1].dtSend)

    if check_event_probability(CHILD_PLAY_UKIO_PROBABILITY):
        ukio_dict['cardState'] = "child play"
        ukio_dict['bWrong'] = True
        ukio_dict['bChildPlay'] = True

    elif check_event_probability(WRONG_CALLS_PROBABILITY):
        ukio_dict['cardState'] = "wrong"
        ukio_dict['bWrong'] = True
        ukio_dict['bChildPlay'] = False
    elif check_event_probability(CALLS_WITHOUT_ANSWER_PROBABILITY):
        return None, generate_call_from_phone_call(call_date, 'wrong')

    else:
        ukio_dict['cardState'] = card_state
        ukio_dict['incidentType'] = incident_type
        ukio_dict['bWrong'] = False
        ukio_dict['bChildPlay'] = False
        ukio_dict |= ukio_eos_cards

    if ukio_eos_cards and not ukio_dict['bWrong']:
        ukio_eos_card = ukio_eos_cards[random.choice(list(ukio_eos_cards.keys()))]
        if not isinstance(ukio_eos_card, psycho) and not isinstance(ukio_eos_card, consult):
            eos_id = ''
            for eos_card in EOSType:
                if eos_card.get('class') == type(ukio_eos_card):
                    eos_id = str(eos_card['id'])
                    break
            redirect_time_confirm = ukio_eos_card.dtCreate + td(seconds=random.randint(10, 40))
            redirect_phone_call = generate_phonecall_from_redirect(redirect_time_confirm)

            phone_calls[-1].RedirectCall = redirectCall(
                eosClassTypeId=eos_id,
                dtRedirectTime=ukio_eos_card.dtCreate,
                dtRedirectConfirm=redirect_time_confirm,
                redirectCancel=False,
                bConference=False,
                PhoneCallId=redirect_phone_call.phoneCallId
            )

            # add new phonecall
            if len(phone_calls) > 1:
                phone_calls.insert(-2, redirect_phone_call)
            else:
                phone_calls.insert(0, redirect_phone_call)
            # add new phoneCallId to redirect
            phone_calls[-1].RedirectCall.PhoneCallId = redirect_phone_call.phoneCallId

            # creating transfer item
            ukio_dict['TransferItem'] = [generate_transfer_items_by_ukio_cards(eos_id, phone_calls[-1].dtSend)]

    ukio_dict['callSource'] = call_source
    ukio_dict['dtSend'] = phone_calls[-1].dtSend
    ukio_dict['dtUpdate'] = phone_calls[-1].dtSend
    ukio_dict['dtCreate'] = phone_calls[-1].dtConnect

    ukio_dict['PhoneCall'] = phone_calls
    call = generate_call_from_phone_call(phone_calls[0])
    # make delay between calls
    return Ukio(**ukio_dict), call


def main():
    for _ in range(1):
        d = generate_ukio_phone_call_data()
        pprint(d)
        # if d.get('Psycho') or d.get('Consult'):
        #     print(d)


if __name__ == '__main__':
    main()
