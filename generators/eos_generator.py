import random
from datetime import timedelta as td
from pprint import pprint
from typing import TypeVar

import numpy as np

from generators import check_event_probability, get_distribution_var_by_work_type
from generators.eos_models_generator import (
    generate_patients_list,
    generate_suspects_list,
    generate_vehicles_list,
    generate_wanted_list,
)
from schemas.eos_for_ukio_models import (
    Card01,
    Card02,
    Card03,
    Card04,
    CardAT,
    CardCommServ,
)
from schemas.string_eos import *
from schemas.string_eos import Consult, Psycho
from schemas.string_schemas import EosResourceUnitNames
from schemas.ukio_model import DispatchService, EosItem, EosResource

from .incident_type_generator.incident_type_generator import (
    generate_card_incident_types_from_list,
)

T = TypeVar("T", Psycho, Consult, Card03, Card02, Card01, Card04, CardAT, CardCommServ)


def generate_card_from_eos_model(
    eos_value_dict: dict, date_from: datetime.datetime, operator: Operator
) -> T:
    """
    take eos_class from string_eos and converts it to the model in eos_for_ukio_models
    :param operator:
    :param eos_value_dict: dict with eos models from string_eos
    :param date_from
    :return:
    """
    if eos_value_dict.get("class_"):
        eos_class = eos_value_dict["class_"]
        dt_create = date_from + td(
            seconds=get_distribution_var_by_work_type(
                work_type=ALL_PROJ_CONSTANTS["EOS_CARD_CREATE_WORK_TYPE"],
                var_name="EOS_CARD_CREATE",
            )
        )

        match eos_class:
            case "consult":
                start_consult = date_from
                consult_normal_time = get_distribution_var_by_work_type(
                    ALL_PROJ_CONSTANTS["CONSULT_WORK_TYPE"], "CONSULT"
                )
                return Consult(
                    operator=operator,
                    operatorId=operator.operatorId,
                    dtConsultStart=start_consult,
                    dtConsultEnd=start_consult + td(seconds=consult_normal_time),
                )

            case "psycho":
                start_psycho = date_from
                psycho_time = get_distribution_var_by_work_type(
                    ALL_PROJ_CONSTANTS["PSYCHO_WORK_TYPE"], "PSYCHO"
                )
                return Psycho(
                    operator=operator,
                    operatorId=operator.operatorId,
                    bPsychoInHouse=check_event_probability(
                        ALL_PROJ_CONSTANTS["PSYCHO_IN_HOUSE_PROBABILITY"]
                    ),
                    dtPsychoStart=start_psycho,
                    dtPsychoEnd=start_psycho
                    + td(minutes=int(psycho_time), seconds=psycho_time * 60 % 60),
                )
            case "card01":
                return Card01(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list(
                        [eos_value_dict]
                    ),
                    strObject=random.choice(ALL_PROJ_CONSTANTS["OBJECT_FOR_CARD01"]),
                    strStoreys=ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD01"].index(
                        random.choice(ALL_PROJ_CONSTANTS["INCIDENT_TYPES_FOR_CARD01"])
                    ),
                    bObjectGasified=check_event_probability(
                        ALL_PROJ_CONSTANTS["OBJECT_GASIFIED_PROBABILITY"]
                    ),
                    strEstimation=str(
                        int(
                            np.random.normal(
                                ALL_PROJ_CONSTANTS["ESTIMATION"],
                                ALL_PROJ_CONSTANTS["ESTIMATION_SCALE"],
                            )
                        )
                    ),
                    strObservedConsequencesFire=random.choice(
                        ALL_PROJ_CONSTANTS["OBSERVED_CONSEQUENCES_FIRE"]
                    ),
                    strCharacteristicsAccessRoads=random.choice(
                        ALL_PROJ_CONSTANTS["ROADS_CHARACTERS"]
                    ),
                    strCharacteristicsWorkingConditions=random.choice(
                        ALL_PROJ_CONSTANTS["WORKING_CONDITIONS_CHARACTERS"]
                    ),
                    bNeedRescueWork=check_event_probability(
                        ALL_PROJ_CONSTANTS["NEED_RESCUE_WORK_PROBABILITY"]
                    ),
                    strEvacuationPossibilitiesAssessment=random.choice(
                        ALL_PROJ_CONSTANTS["EVACUATIONS_POSSIBILITIES"]
                    ),
                    strObjectOwnerInfo=random.choice(ALL_PROJ_CONSTANTS["OWNERS_INFO"]),
                )

            case "card02":
                return Card02(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list(
                        [eos_value_dict]
                    ),
                    iNumberOffenders=int(
                        get_distribution_var_by_work_type(
                            ALL_PROJ_CONSTANTS["OFFENDERS_NUMBER_WORK_TYPE"],
                            "OFFENDERS_NUMBER",
                        )
                    ),
                    iNumberVehicle=int(
                        get_distribution_var_by_work_type(
                            ALL_PROJ_CONSTANTS["VEHICLE_NUMBER_WORK_TYPE"],
                            "VEHICLE_NUMBER",
                        )
                    ),
                    suspect=generate_suspects_list(),
                    wantedPerson=generate_wanted_list(),
                    vehicle=generate_vehicles_list(),
                )
            case "card03":
                return Card03(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list(
                        [eos_value_dict]
                    ),
                    strWhoCalled=random.choice(ALL_PROJ_CONSTANTS["WHO_CALLED"]),
                    bConsultation=check_event_probability(
                        ALL_PROJ_CONSTANTS["AMBULANCE_CONSULT_PROBABILITY"]
                    ),
                    patient=generate_patients_list(),
                )
            case "card04":
                return Card04(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list(
                        [eos_value_dict]
                    ),
                    strInstructions=random.choice(
                        ALL_PROJ_CONSTANTS["GAS_INSTRUCTIONS"]
                    ),
                    bConsultation=check_event_probability(
                        ALL_PROJ_CONSTANTS["GAS_CONSULT_PROBABILITY"]
                    ),
                )
            case "cardcommserv":
                return CardCommServ(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list(
                        [eos_value_dict]
                    ),
                    strCommServ=random.choice(ALL_PROJ_CONSTANTS["C_S"]),
                    strInstructions=random.choice(
                        ALL_PROJ_CONSTANTS["CS_INSTRUCTIONS"]
                    ),
                    bConsultation=check_event_probability(
                        ALL_PROJ_CONSTANTS["CS_CONSULT_PROBABILITY"]
                    ),
                    strServiced=[
                        random.choice(ALL_PROJ_CONSTANTS["CS_SERVICES"])
                        for _ in range(
                            int(
                                get_distribution_var_by_work_type(
                                    ALL_PROJ_CONSTANTS["SERVICES_COUNT_WORK_TYPE"],
                                    "SERVICES_COUNT",
                                )
                            )
                        )
                    ],
                    strAppeal=random.choice(ALL_PROJ_CONSTANTS["CS_APPEALS"]),
                )
            case "cardat":
                print(
                    type(ALL_PROJ_CONSTANTS["AT_INJURIES"]),
                    ALL_PROJ_CONSTANTS["AT_INJURIES"],
                )
                return CardAT(
                    dtCreate=dt_create,
                    strIncidentType=generate_card_incident_types_from_list(
                        [eos_value_dict]
                    ),
                    iPerishedPeople=int(
                        get_distribution_var_by_work_type(
                            ALL_PROJ_CONSTANTS["PERISHED_PEOPLE_WORK_TYPE"],
                            "PERISHED_PEOPLE",
                        )
                    ),
                    iAffectedPeople=int(
                        get_distribution_var_by_work_type(
                            ALL_PROJ_CONSTANTS["AFFECTED_PEOPLE_WORK_TYPE"],
                            "AFFECTED_PEOPLE",
                        )
                    ),
                    iSuspectPeople=int(
                        get_distribution_var_by_work_type(
                            ALL_PROJ_CONSTANTS["SUSPECT_PEOPLE_WORK_TYPE"],
                            "SUSPECT_PEOPLE",
                        )
                    ),
                    strSuspectDescription=random.choice(
                        ALL_PROJ_CONSTANTS["SUSPECT_DESCRIPTION"]
                    ),
                    strArmament=[random.choice(ALL_PROJ_CONSTANTS["ARMAMENTS"])],
                    strVehicles=[
                        random.choice(ALL_PROJ_CONSTANTS["ARMAMENTS"])
                        for _ in range(
                            int(
                                get_distribution_var_by_work_type(
                                    ALL_PROJ_CONSTANTS["ARMAMENTS_WORK_TYPE"],
                                    "ARMAMENTS",
                                )
                            )
                        )
                    ],
                    strDirection=random.choice(ALL_PROJ_CONSTANTS["DIRECTION_TYPES"]),
                    strInjurySuspect=random.choice(ALL_PROJ_CONSTANTS["AT_INJURIES"]),
                )


def generate_random_eos_list() -> list[StringEosType]:
    """
    creates a list with random eos dicts from string_eos

    :return:
    """
    eos_list = []
    for eos_obj in get_string_eos_type().model_dump()["values"]:
        if eos_obj["p_min"] is not None and eos_obj["class_"]:
            # takes string_eos and check eos probability by p_min and p_max
            if check_event_probability(
                ALL_PROJ_CONSTANTS["EOS_SHARE_MIN"], ALL_PROJ_CONSTANTS["EOS_SHARE_MAX"]
            ):
                if check_event_probability(eos_obj["p_min"], eos_obj["p_max"]):
                    eos_list.append(eos_obj)
    return eos_list


def __generate_eos_resources(eos_type_list: list[StringEosType]) -> list[EosResource]:
    eos_resources = []
    for el in eos_type_list:
        eos_resources.append(
            EosResource(
                eosClassTypeId=el["id"],
                strResourceUnitName=random.choice(list(EosResourceUnitNames)),
                strMembership=random.choice(ALL_PROJ_CONSTANTS["MEMBERSHIP"]),
            )
        )
    return eos_resources


def generate_eos_item_from_eos_list(
    eos_type_list: list[StringEosType], operator: Operator, date_from: datetime.datetime
) -> list[EosItem]:
    eos_items = []
    for el in eos_type_list:
        dt_depart = date_from + td(
            seconds=int(
                get_distribution_var_by_work_type(
                    ALL_PROJ_CONSTANTS["DT_DEPART_WORK_TYPE"], "DT_DEPART"
                )
            )
        )

        if check_event_probability(ALL_PROJ_CONSTANTS["EOS_ITEM_CANCEL_PROBABILITY"]):
            dt_confirm_depart = None
            dt_arrival = None
            dt_complete = None
            dt_cancel = dt_depart + td(
                seconds=int(
                    get_distribution_var_by_work_type(
                        ALL_PROJ_CONSTANTS["DT_CANCEL_WORK_TYPE"], "DT_CANCEL"
                    )
                )
            )
        else:
            dt_confirm_depart = dt_depart + td(
                seconds=int(
                    get_distribution_var_by_work_type(
                        ALL_PROJ_CONSTANTS["DT_DEPART_CONFIRM_WORK_TYPE"], "DT_DEPART"
                    )
                )
            )
            dt_arrival = dt_confirm_depart + td(
                seconds=int(
                    get_distribution_var_by_work_type(
                        ALL_PROJ_CONSTANTS["DT_ARRIVAL_WORK_TYPE"], "DT_ARRIVAL"
                    )
                )
            )
            dt_complete = dt_arrival + td(
                seconds=int(
                    get_distribution_var_by_work_type(
                        ALL_PROJ_CONSTANTS["DT_COMPLETE_WORK_TYPE"], "DT_COMPLETE"
                    )
                )
            )
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
                    eosClassTypeId=el["id"], strDispatchServiceName=el["name"]
                ),
                eosResource=__generate_eos_resources(eos_type_list)
                if dt_cancel is None
                else None,
            )
        )

    return eos_items


# random.seed(1696)


def __find_seed():
    for i in range(100000):
        random.seed(i)
        s = generate_random_eos_list()
        if len(s) == 2:
            if StringEosType.houseDepartment in s and StringEosType.fireDepartment in s:
                print(i)
                break


def main():
    pprint(generate_card_incident_types_from_list(generate_random_eos_list()))


if __name__ == "__main__":
    main()
