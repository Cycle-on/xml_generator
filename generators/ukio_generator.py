import datetime
import random
from datetime import timedelta as td

from config import load_config, missed_info, ukios_info
from constants import ALL_PROJ_CONSTANTS
from csv_parser.parse_addresses import ADDRESSES
from csv_parser.parse_incident_types import CARDS_INDEXES_INCIDENT_TYPES
from generators import check_event_probability, genders
from generators.eos_generator import (
    T,
    generate_card_from_eos_model,
    generate_eos_item_from_eos_list,
    generate_random_eos_list,
)
from generators.operators_and_arms import get_operator
from generators.phonecall_generator import (
    generate_missed_call,
    generate_phone_data,
    generate_phone_date,
)
from generators.random_generators import (
    get_address_by_code,
    get_random_name,
    get_random_telephone_number,
)
from schemas.phonecall import MissedCall, PhoneCall, redirectCall
from schemas.string_eos import (
    Consult,
    Operator,
    Psycho,
    StringEosType,
    get_string_eos_type,
)
from schemas.string_schemas import CardStates
from schemas.ukio_model import CallContent, TransferItem, Ukio

config = load_config()


def generate_phonecall_from_redirect(dt_call: datetime.datetime) -> PhoneCall:
    """
    a function creates a phoneCall model which is used to create redirect call
    :param dt_call:
    :return:
    """
    dt_call, dt_connect, dt_end_call, date_send = generate_phone_date(dt_call=dt_call)
    return PhoneCall(
        dtSend=date_send,
        bOperatorIniciatied=True,
        dtCall=dt_call,
        dtConnect=dt_connect,
    )


def __generate_call_content() -> CallContent:
    """
    function returning call content for ukio card
    :return:
    """
    applicant_number = get_random_telephone_number()
    (
        applicant_surname,
        applicant_name,
        applicant_middle_name,
    ) = get_random_name(
        genders[
            check_event_probability(
                ALL_PROJ_CONSTANTS["CALL_CONTENT_APPLICANT_MALE_PROBABILITY"]
            )
        ]
    )

    return CallContent(
        strLastName=applicant_surname,
        strMiddleName=applicant_middle_name,
        strName=applicant_name,
        strCallerContactPhone=applicant_number,
        strCgPN=applicant_number
        if check_event_probability(
            ALL_PROJ_CONSTANTS["CALL_NUMBER_APPLICANT_NUMBER_EQUALITY_PROBABILITY"]
        )
        else get_random_telephone_number(),
        appResAddress=get_address_by_code()[0],
        strLanguage="ru",
        strIncidentDescription=random.choice(
            ALL_PROJ_CONSTANTS["INCIDENT_DESCRIPTIONS"]
        ),
        appLocAddress=get_address_by_code()[0],
    )


def __decapitalize(s: str):
    """
    make the first letter lower
    :param s:
    :return:
    """
    return s[0].lower() + s[1:]


def _check_ukio_cards(
    eos_list: list[StringEosType], dt_send: datetime.datetime, operator: Operator
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


def generate_transfer_items_by_ukio_cards(
    eos_id: str, transfer_date: datetime.datetime
) -> TransferItem:
    """
    a function creates transfer item for ukio card
    :param eos_id:
    :param transfer_date:
    :return:
    """
    return TransferItem(eosClassTypeId=eos_id, dtTransfer=transfer_date, bSuccess=True)


def generate_ukio_phone_call_data(call_date: datetime.datetime) -> Ukio | MissedCall:
    """
    creating ukio card with call_source = mobile phone
    at first function create card state, random incident type from list, one operator for one card
    then creating phonecalls and eos cards by probabilities
    :return: Ukio model or missed call model
    """
    ukio_dict = {}
    # create non-logic fields
    card_state = random.choice(list(CardStates))
    # incident_type = random.choice(list(IncidentTypes))
    call_source = "Номер 112"
    # create fields with some logica

    operator_info = get_operator(call_date)
    if operator_info is None:
        print("no free ops")
        return
    operator = operator_info["operator"]

    phone_calls: list[PhoneCall] = generate_phone_data(call_date, operator)
    eos_type_list: list[StringEosType] = generate_random_eos_list()
    ukio_eos_cards: dict[str, T] = _check_ukio_cards(
        eos_type_list, phone_calls[-1].dtSend, operator
    )
    # start checks random events
    # missed call without ukio
    if check_event_probability(ALL_PROJ_CONSTANTS["MISSED_CALL_PROBABILITY"]):
        missed_info.append({"filename": "", "dt_send": phone_calls[0].dtSend})
        return generate_missed_call(phone_calls[0])
    # child play ukio card
    elif check_event_probability(ALL_PROJ_CONSTANTS["CHILD_PLAY_UKIO_PROBABILITY"]):
        ukio_dict["cardState"] = "child play"
        ukio_dict["bWrong"] = True
        ukio_dict["bChildPlay"] = True
    # wrong ukio card
    elif check_event_probability(ALL_PROJ_CONSTANTS["WRONG_CALLS_PROBABILITY"]):
        ukio_dict["cardState"] = "wrong"
        ukio_dict["bWrong"] = True
        ukio_dict["bChildPlay"] = False
    # ukio card with some event
    else:
        # non-logic
        ukio_dict["strCardState"] = card_state
        try:
            incident_type_id = random.choice(eos_type_list).get("id")
            incident_type = random.choice(
                CARDS_INDEXES_INCIDENT_TYPES[incident_type_id]
            ).get("name")
            ukio_dict["strIncidentType"] = incident_type

        except IndexError:
            pass
        except KeyError:
            pass
        ukio_dict["bWrong"] = False
        ukio_dict["bChildPlay"] = False
        ukio_dict["bChs"] = check_event_probability(
            ALL_PROJ_CONSTANTS["CHS_PROBABILITY"]
        )
        ukio_dict["bHumanThreat"] = check_event_probability(
            ALL_PROJ_CONSTANTS["HUMAN_TREAT_PROBABILITY"]
        )

        # logic fields
        ukio_dict["address"] = random.choice(ADDRESSES)
        ukio_dict |= ukio_eos_cards
        ukio_dict["eosItem"] = generate_eos_item_from_eos_list(
            eos_type_list, operator, call_date
        )
        ukio_dict["callContent"] = __generate_call_content()

    if ukio_eos_cards and not ukio_dict["bWrong"]:  # if card has eos card
        """
        conditional creates redirect call to random eos
        """
        # take random eos from eoses generated for ukio
        eos_string_class_name = random.choice(list(ukio_eos_cards.keys()))
        ukio_eos_card = ukio_eos_cards[eos_string_class_name]
        # if card need redirect
        if not isinstance(ukio_eos_card, Psycho) and not isinstance(
            ukio_eos_card, Consult
        ):
            # creating redirect call
            eos_id = ""
            for eos_card in get_string_eos_type().model_dump()["values"]:
                # linear search for stringEosType to find eos class type index
                if eos_card.get("class_").lower() == eos_string_class_name.lower():
                    eos_id = str(eos_card["id"])
                    break

            # create redirect call params from phoneCall model
            redirect_time_confirm = ukio_eos_card.dtCreate + td(
                seconds=random.randint(10, 40)
            )
            redirect_phone_call = generate_phonecall_from_redirect(
                redirect_time_confirm
            )
            # fill redirect call
            phone_calls[-1].RedirectCall = redirectCall(
                eosClassTypeId=eos_id,
                dtRedirectTime=ukio_eos_card.dtCreate,
                dtRedirectConfirm=redirect_time_confirm,
                redirectCancel=False,
                bConference=False,
                PhoneCallId=redirect_phone_call.phoneCallId,
            )

            # add new phonecall
            if len(phone_calls) > 1:
                # add phone call with redirect info
                phone_calls.insert(-2, redirect_phone_call)
            else:
                phone_calls.insert(0, redirect_phone_call)
            # add new phoneCallId to redirect
            phone_calls[-1].RedirectCall.PhoneCallId = redirect_phone_call.phoneCallId

            # creating transfer item
            ukio_dict["transferItem"] = [
                generate_transfer_items_by_ukio_cards(eos_id, phone_calls[-1].dtSend)
            ]
    # fill call info to ukio root
    ukio_dict["strCallSource"] = call_source

    # fill date fields with last phone call information
    ukio_dict["dtSend"] = phone_calls[-1].dtSend
    ukio_dict["dtUpdate"] = phone_calls[-1].dtSend
    ukio_dict["dtCreate"] = phone_calls[-1].dtConnect
    ukio_dict["dtCall"] = phone_calls[-1].dtCall
    ukio_dict["dtCallEnd"] = phone_calls[-1].dtEndCall
    ukio_dict["aCallEnded"] = phone_calls[-1].aCallEnded
    # add phonecalls to ukio
    ukio_dict["phoneCall"] = phone_calls
    # appending to queue for sending module
    ukios_info.append({"filename": "", "dt_send": phone_calls[-1].dtSend})
    # update operator info
    operator_info["end_time"] = phone_calls[-1].dtEndCall
    return Ukio(**ukio_dict)
