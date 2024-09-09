import random
from pprint import pprint

from generators import *
from generators.eos_models_generator import *
from google_sheet_parser.parse_incident_types import CARDS_INDEXES_INCIDENT_TYPES
from schemas.string_eos import *
from schemas.string_eos import Psycho, Consult
from schemas.eos_for_ukio_models import *
from generators import check_event_probability
from schemas.string_schemas import EosResourceUnitNames
from schemas.ukio_model import EosItem, DispatchService, EosResource

T = TypeVar(
    "T",
    Psycho,
    Consult,
    Card03,
    Card02,
    Card01,
    Card04,
    CardAT,
    CardCommServ
)


def _check_eos_probability(eos_value_dict: dict) -> bool:
    """
    takes string_eos and check eos probability by p_min and p_max
    :param eos_value_dict: dict from string_eos
    :return:
    """
    if check_event_probability(EOS_SHARE_MIN, EOS_SHARE_MAX):
        return check_event_probability(eos_value_dict['p_min'], eos_value_dict['p_max'])


def generate_card_from_eos_model(eos_value_dict: dict, date_from: datetime.datetime, operator: Operator) -> T:
    """
    take eos_class from string_eos and converts it to the model in eos_for_ukio_models
    :param operator:
    :param eos_value_dict: dict with eos models from string_eos
    :param date_from
    :return:
    """
    if eos_value_dict.get('class'):
        eos_class = eos_value_dict['class']
        dt_create = date_from + td(
            seconds=get_distribution_var_by_work_type(
                work_type=EOS_CARD_CREATE_WORK_TYPE,
                var_name="EOS_CARD_CREATE"
            )
        )

        match eos_class:
            case 'consult':
                start_consult = date_from
                consult_normal_time = get_distribution_var_by_work_type(CONSULT_WORK_TYPE, 'CONSULT')
                return Consult(
                    operator=operator,
                    operatorId=operator.operatorId,
                    dtConsultStart=start_consult,
                    dtConsultEnd=start_consult + td(seconds=consult_normal_time)
                )

            case 'psycho':
                start_psycho = date_from
                psycho_time = get_distribution_var_by_work_type(PSYCHO_WORK_TYPE, 'PSYCHO')
                return Psycho(
                    operator=operator,
                    operatorId=operator.operatorId,
                    bPsychoInHouse=check_event_probability(PSYCHO_IN_HOUSE_PROBABILITY),
                    dtPsychoStart=start_psycho,
                    dtPsychoEnd=start_psycho + td(minutes=int(psycho_time), seconds=psycho_time * 60 % 60)
                )
            case "card01":
                return Card01(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list([eos_value_dict]),
                    strObject=random.choice(OBJECT_FOR_CARD01),
                    strStoreys=random.choice(INCIDENT_TYPES_FOR_CARD01)['name'],
                    bObjectGasified=check_event_probability(OBJECT_GASIFIED_PROBABILITY),
                    strEstimation=str(int(np.random.normal(ESTIMATION, ESTIMATION_SCALE))),
                    strObservedConsequencesFire=random.choice(OBSERVED_CONSEQUENCES_FIRE),
                    strCharacteristicsAccessRoads=random.choice(ROADS_CHARACTERS),
                    strCharacteristicsWorkingConditions=random.choice(WORKING_CONDITIONS_CHARACTERS),
                    bNeedRescueWork=check_event_probability(NEED_RESCUE_WORK_PROBABILITY),
                    strEvacuationPossibilitiesAssessment=random.choice(EVACUATIONS_POSSIBILITIES),
                    strObjectOwnerInfo=random.choice(OWNERS_INFO),
                )

            case "card02":
                return Card02(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list([eos_value_dict]),
                    iNumberOffenders=int(
                        get_distribution_var_by_work_type(OFFENDERS_NUMBER_WORK_TYPE, "OFFENDERS_NUMBER")),
                    iNumberVehicle=int(get_distribution_var_by_work_type(VEHICLE_NUMBER_WORK_TYPE, "VEHICLE_NUMBER")),
                    suspect=generate_suspects_list(),
                    wantedPerson=generate_wanted_list(),
                    vehicle=generate_vehicles_list(),
                )
            case "card03":
                return Card03(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list([eos_value_dict]),
                    strWhoCalled=random.choice(WHO_CALLED),
                    bConsultation=check_event_probability(AMBULANCE_CONSULT_PROBABILITY),
                    patient=generate_patients_list(),
                )
            case "card04":
                return Card04(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list([eos_value_dict]),
                    strInstructions=random.choice(GAS_INSTRUCTIONS),
                    bConsultation=check_event_probability(GAS_CONSULT_PROBABILITY),
                )
            case "cardcommserv":
                return CardCommServ(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list([eos_value_dict]),
                    strCommServ=random.choice(C_S),
                    strInstructions=random.choice(CS_INSTRUCTIONS),
                    bConsultation=check_event_probability(CS_CONSULT_PROBABILITY),
                    strServiced=[random.choice(CS_SERVICES) for _ in range(
                        int(get_distribution_var_by_work_type(SERVICES_COUNT_WORK_TYPE, "SERVICES_COUNT")))],
                    strAppeal=random.choice(CS_APPEALS),
                )
            case "cardat":
                return CardAT(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list([eos_value_dict]),
                    iPerishedPeople=int(
                        get_distribution_var_by_work_type(PERISHED_PEOPLE_WORK_TYPE, 'PERISHED_PEOPLE')),
                    iAffectedPeople=int(
                        get_distribution_var_by_work_type(AFFECTED_PEOPLE_WORK_TYPE, 'AFFECTED_PEOPLE')),
                    iSuspectPeople=int(get_distribution_var_by_work_type(SUSPECT_PEOPLE_WORK_TYPE, 'SUSPECT_PEOPLE')),
                    strSuspectDescription=random.choice(SUSPECT_DESCRIPTION),
                    strArmament=[random.choice(ARMAMENTS)],
                    strVehicles=[random.choice(ARMAMENTS) for _ in range(
                        int(get_distribution_var_by_work_type(ARMAMENTS_WORK_TYPE, "ARMAMENTS")))],
                    strDirection=random.choice(DIRECTION_TYPES),
                    strInjurySuspect=random.choice(AT_INJURIES)
                )


def generate_random_eos_list() -> list[StringEosType]:
    """
    creates a list with random eos dicts from string_eos

    :return:
    """
    eos_list = []
    for eos_obj in StringEosType:
        if eos_obj.value.get('p_min') is not None and eos_obj.value.get('class'):
            if _check_eos_probability(eos_obj):
                eos_list.append(eos_obj)
    return eos_list


def check_list_equality(l1: list, l2: list) -> bool:
    return set(l1) == set(l2)


def delete_linked_eos_from_list_by_needed_count(incident_type_list: list, eos_count: int = 1,
                                                ignored_types=None):
    if ignored_types is None:
        ignored_types = []
    ans = []
    for el in incident_type_list:
        # if I have linked eoses, I need to check eoses which are ignored
        if len(el.get('linked_eos', [])) < eos_count:
            ans.append(el)
    return ans


def get_names_from_eos_type_list(eos_type_list: list[StringEosType]) -> list[str]:
    ans = []
    for el in eos_type_list:
        ans.append(el['name'])
    return ans


def __make_section_from_list(s: list[dict]):
    counter = 0
    for el in s:
        el['section_min'] = counter + 1
        el['section_max'] = counter + el['ukio_count']
        counter += el['ukio_count']
    return s, counter


def generate_card_incident_types_from_list(eos_type_list: list[StringEosType]) -> str:
    return '-'
    if len(eos_type_list) == 1:
        string_eos_incident_types_list = delete_linked_eos_from_list_by_needed_count(
            CARDS_INDEXES_INCIDENT_TYPES[int(eos_type_list[0]['code'])]
        )
    else:
        string_eos_incident_types_list = delete_linked_eos_from_list_by_needed_count(
            CARDS_INDEXES_INCIDENT_TYPES[int(eos_type_list[0]['code'])]
        )
    # else:
    #
    #     string_eos_incident_types_list = []
    #     added_names = []
    #     for i in range(len(eos_type_list)):
    #         incident_types_list_by_eos: list = CARDS_INDEXES_INCIDENT_TYPES[int(eos_type_list[i]['code'])]
    #
    #         for var in incident_types_list_by_eos:
    #             if var['name'] in added_names:
    #                 continue
    #
    #             # at first, check double eoses
    #             if var.get('linked_eos'):
    #                 if len(var['linked_eos']) <= len(eos_type_list) - 1:  # if I have one linked eos
    #                     linked_eos_name = var['linked_eos'][0]
    #                     if linked_eos_name in get_names_from_eos_type_list(eos_type_list):
    #                         string_eos_incident_types_list.append(var)
    #             # at second, add without linked
    #             else:
    #                 string_eos_incident_types_list.append(var)
    #             added_names.append(var['name'])
    if len(eos_type_list) == 1:
        string_eos_incident_types_list, last_number = __make_section_from_list(string_eos_incident_types_list)
        one_incident = get_solo_incident_type(string_eos_incident_types_list, last_number)
    else:
        # many eoses algorithm
        pass
    return one_incident['name']


def get_random_eos_incident_type(eos_type_list: list, incident_types_list, max_number):
    eos_count = len(eos_type_list)
    random_value = random.randint(1, max_number)  # 13
    filtered_incident_types_list = []
    for el in incident_types_list:
        if el['section_min'] <= random_value <= el['section_max']:
            if eos_count == 1:
                filtered_incident_types_list.append(el)
                break
            if el.get('linked_eos'):
                if len(el['linked_eos']) == eos_count - 1:
                    filtered_incident_types_list.append(el)
                    break
                else:
                    filtered_incident_types_list.append(el)
                    return get_random_eos_incident_type(
                        eos_type_list,
                        delete_linked_eos_from_list_by_needed_count(
                            incident_types_list,
                            eos_count - len(el['linked_eos']),
                            ignored_types=el['linked_eos']
                        ),
                        max_number
                    )
            else:
                filtered_incident_types_list.append(el)
                return  # something

    return filtered_incident_types_list


def get_solo_incident_type(section_incident_type_list: list, last_number: int):
    random_value = random.randint(1, last_number)
    for el in section_incident_type_list:
        if el['section_min'] <= random_value <= el['section_max']:
            return el


def __generate_eos_resources(eos_type_list: list[StringEosType]) -> list[EosResource]:
    eos_resources = []
    for el in eos_type_list:
        eos_resources.append(
            EosResource(
                eosClassTypeId=el['id'],
                strResourceUnitName=random.choice(list(EosResourceUnitNames)),
                strMembership=random.choice(MEMBERSHIP)
            )
        )
    return eos_resources


def generate_eos_item_from_eos_list(eos_type_list: list[StringEosType],
                                    operator: Operator,
                                    date_from: datetime.datetime) -> list[EosItem]:
    eos_items = []
    for el in eos_type_list:
        dt_depart = date_from + td(seconds=int(
            get_distribution_var_by_work_type(
                DT_DEPART_WORK_TYPE, "DT_DEPART"
            )))

        if check_event_probability(EOS_ITEM_CANCEL_PROBABILITY):
            dt_confirm_depart = None
            dt_arrival = None
            dt_complete = None
            dt_cancel = dt_depart + td(seconds=int(
                get_distribution_var_by_work_type(DT_CANCEL_WORK_TYPE, "DT_CANCEL")
            ))
        else:
            dt_confirm_depart = dt_depart + td(seconds=int(
                get_distribution_var_by_work_type(
                    DT_DEPART_CONFIRM_WORK_TYPE, 'DT_DEPART'
                )))
            dt_arrival = dt_confirm_depart + td(seconds=int(
                get_distribution_var_by_work_type(DT_ARRIVAL_WORK_TYPE, 'DT_ARRIVAL')
            ))
            dt_complete = dt_arrival + td(seconds=int(
                get_distribution_var_by_work_type(DT_COMPLETE_WORK_TYPE, "DT_COMPLETE")
            ))
            dt_cancel = None

        eos_items.append(
            EosItem(
                operator=operator,
                operatorId=operator.operatorId,
                dtDepart=dt_depart,
                dtConfirmDepart=dt_confirm_depart,
                dtArrival=dt_arrival,
                dtComplete=dt_complete,
                dtCancel=dt_cancel,
                dispatchService=DispatchService(
                    eosClassTypeId=el['id'],
                    strDispatchServiceName=el['name']
                ),
                eosResource=__generate_eos_resources(eos_type_list) if dt_cancel is None else None

            )
        )
    return eos_items


random.seed(1696)


def __find_seed():
    for i in range(100000):
        random.seed(i)
        s = generate_random_eos_list()
        if len(s) == 2:
            if StringEosType.houseDepartment in s and StringEosType.fireDepartment in s:
                print(i)
                break


def main():
    pprint(generate_card_incident_types_from_list(
        generate_random_eos_list()
    ))


if __name__ == '__main__':
    main()
