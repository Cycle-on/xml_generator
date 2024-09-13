import random
from copy import deepcopy
from decimal import Decimal
from pprint import pprint
from datetime import timedelta as td

from config import load_config, ukios_info, missed_info
from config.config_data import *
from generators.eos_generator import generate_card_from_eos_model, generate_random_eos_list, T, \
    generate_eos_item_from_eos_list
from generators.phonecall_generator import generate_phone_data, generate_phone_date, generate_missed_call
from generators import check_event_probability, genders
from generators.random_generators import get_address_by_code, get_random_name, get_random_telephone_number
from google_sheet_parser.parse_addresses import get_random_address, ADDRESSES
from schemas.string_eos import StringEosType, Consult, Psycho, Operator
from schemas.ukio_model import Ukio, TransferItem, Address, CallContent
from schemas.phonecall import PhoneCall, redirectCall, Call, MissedCall
from schemas.string_schemas import IncidentTypes, CardStates, CallSource

config = load_config()


def generate_phonecall_from_redirect(dt_call: datetime.datetime) -> PhoneCall:
    dt_call, dt_connect, dt_end_call, date_send = generate_phone_date(
        dt_call=dt_call
    )
    return PhoneCall(
        dtSend=date_send,
        bOperatorIniciatied=True,
        dtCall=dt_call,
        dtConnect=dt_connect,

    )


def generate_call_from_phone_call(phone_call: PhoneCall | datetime.datetime, rtype='') -> Call:
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
        phoneCall=phone_call_without_end_params,
        PhoneCallID=phone_call_without_end_params.phoneCallId,
        dtCall=phone_call.dtCall,
        dtSend=phone_call.dtCall + td(seconds=random.randint(3, 10))
    )


def __generate_call_content() -> CallContent:
    applicant_number = get_random_telephone_number()
    applicant_surname, applicant_name, applicant_middle_name, = get_random_name(
        genders[check_event_probability(CALL_CONTENT_APPLICANT_MALE_PROBABILITY)])

    return CallContent(
        strLastName=applicant_surname,
        strMiddleName=applicant_middle_name,
        strName=applicant_name,
        strCallerContactPhone=applicant_number,
        strCgPN=applicant_number if check_event_probability(
            CALL_NUMBER_APPLICANT_NUMBER_EQUALITY_PROBABILITY) else get_random_telephone_number(),
        appResAddress=get_address_by_code()[0],
        strLanguage="ru",
        strIncidentDescription=random.choice(INCIDENT_DESCRIPTIONS),
        appLocAddress=get_address_by_code()[0],
    )


def __decapitalize(s: str):
    return s[0].lower() + s[1:]


def _check_ukio_cards(
        eos_list: list[StringEosType],
        dt_send: datetime.datetime,
        operator: Operator
) -> dict[str, T]:
    """
    convert eos_dict to the pydantic model / from eos_for_ukio_models
    :param eos_list: list with eos_dicts from string_eos(can be created in generate_random_eos_list())
    :param dt_send: ukio card date_send
    :return:  dict with eos_models
    """
    eos_dict = {}

    for eos in eos_list:
        card = generate_card_from_eos_model(eos, dt_send, operator)
        eos_dict[__decapitalize(card.__class__.__name__)] = card

    return eos_dict


def generate_transfer_items_by_ukio_cards(eos_id: str,
                                          transfer_date: datetime.datetime) -> TransferItem:
    return TransferItem(
        eosClassTypeId=eos_id,
        dtTransfer=transfer_date,
        bSuccess=True
    )


def generate_ukio_phone_call_data(call_date: datetime.datetime) -> Ukio | MissedCall:
    """
    creating ukio card with call_source = mobile phone
    :return: Ukio model
    """
    ukio_dict = {}
    card_state = random.choice(list(CardStates))
    incident_type = random.choice(list(IncidentTypes))
    call_source = CallSource.mobile_phone
    operator = Operator()
    phone_calls: list[PhoneCall] = generate_phone_data(call_date, operator)
    eos_type_list: list[StringEosType] = generate_random_eos_list()
    ukio_eos_cards = _check_ukio_cards(eos_type_list, phone_calls[-1].dtSend, operator)

    if check_event_probability(MISSED_CALL_PROBABILITY):

        missed_info.append({'filename': '', 'dt_send': phone_calls[0].dtSend})
        return generate_missed_call(phone_calls[0])

    elif check_event_probability(CHILD_PLAY_UKIO_PROBABILITY):
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
        ukio_dict['eosItem'] = generate_eos_item_from_eos_list(eos_type_list, operator, call_date)
        ukio_dict['address'] = random.choice(ADDRESSES)
        ukio_dict['callContent'] = __generate_call_content()

    if ukio_eos_cards and not ukio_dict['bWrong']:
        ukio_eos_card = ukio_eos_cards[random.choice(list(ukio_eos_cards.keys()))]
        if not isinstance(ukio_eos_card, Psycho) and not isinstance(ukio_eos_card, Consult):
            eos_id = ''
            for eos_card in StringEosType:
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
            ukio_dict['transferItem'] = [generate_transfer_items_by_ukio_cards(eos_id, phone_calls[-1].dtSend)]

    ukio_dict['callSource'] = call_source
    ukio_dict['dtSend'] = phone_calls[-1].dtSend
    ukio_dict['dtUpdate'] = phone_calls[-1].dtSend
    ukio_dict['dtCreate'] = phone_calls[-1].dtConnect

    ukios_info.append({'filename': '', 'dt_send': phone_calls[-1].dtSend})
    ukio_dict['phoneCall'] = phone_calls

    ukio_dict['dtCall'] = phone_calls[-1].dtCall
    ukio_dict['dtCallEnded'] = phone_calls[-1].dtEndCall
    ukio_dict['aCallEnded'] = phone_calls[-1].aCallEnded
    # make delay between calls
    return Ukio(**ukio_dict)
