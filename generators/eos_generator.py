import random
from datetime import timedelta as td
from typing import TypeVar

from generators import *
from random_names import get_random_name
from schemas.string_eos import *
from schemas.string_eos import Psycho, Consult
from schemas.eos_for_ukio_models import *
from generators import check_event_probability
from schemas.ukio_model import EosItem

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

genders = {True: "M", False: "F"}


def _check_eos_probability(eos_value_dict: dict) -> bool:
    """
    takes string_eos and check eos probability by p_min and p_max
    :param eos_value_dict: dict from string_eos
    :return:
    """
    if check_event_probability(EOS_SHARE_MIN, EOS_SHARE_MAX):
        return check_event_probability(eos_value_dict['p_min'], eos_value_dict['p_max'])


def generate_patients_list() -> list[Patient]:
    patients = []
    patients_count = int(get_distribution_var_by_work_type())
    for _ in range(patients_count):
        gender = genders[check_event_probability(AMBULANCE_MALE_PROBABILITY)]
        name, middle_name, surname = get_random_name(gender)
        age = int(get_distribution_var_by_work_type(AMBULANCE_AGE_WORK_TYPE, "AMBULANCE_AGE"))
        birth_day = get_random_birth_date_by_year(DATE_ZERO - td(days=365 * age))

        patients.append(
            Patient(
                strLastName=surname,
                strName=name,
                strMiddleName=middle_name,
                dtDateBirth=birth_day,
                iAge=age,
                strGender=gender,
                strOccasion=random.choice(OCCASION_TYPES),
                strAbilityMoveIndependently=random.choice(ABILITY_MOVE_INDEPENDENTLY),
            )
        )
    return patients


def generate_wanted_list() -> list[WantedPerson]:
    wanted_persons = []
    wanted_count = int(get_distribution_var_by_work_type(HOW_MANY_WANTED_WORK_TYPE, "HOW_MANY_WANTED"))
    for _ in range(wanted_count):
        gender = genders[check_event_probability(WANTED_MALE_GENDER_PROBABILITY)]
        name, middle_name, surname = get_random_name(gender)
        age = int(get_distribution_var_by_work_type(WANTED_AGE_WORK_TYPE, "WANTED_AGE"))
        birth_day = get_random_birth_date_by_year(DATE_ZERO - td(days=365 * age))
        wanted_persons.append(
            WantedPerson(
                strGender=gender,
                iAge=age,
                strHeightType=random.choice(HEIGHT_TYPES),
                strBodyType=random.choice(BODY_TYPES),
                strDressed=random.choice(DRESSES),
                strSpecialSigns=random.choice(SPECIAL_SIGNS),
                strLastName=surname,
                strName=name,
                strMiddleName=middle_name,
                dtDateBirth=birth_day,
            )
        )
    return wanted_persons


def generate_suspects_list() -> list[Suspect]:
    suspects = []
    suspects_count = int(get_distribution_var_by_work_type(HOW_MANY_SUSPECTS_WORK_TYPE, 'HOW_MANY_SUSPECTS'))
    for _ in range(suspects_count):
        suspects.append(
            Suspect(
                strGender=genders[check_event_probability(SUSPECT_MALE_GENDER_PROBABILITY)],
                iAge=int(get_distribution_var_by_work_type(SUSPECT_AGE_WORK_TYPE, 'SUSPECT_AGE')),
                strHeightType=random.choice(HEIGHT_TYPES),
                strBodyType=random.choice(BODY_TYPES),
                strDressed=random.choice(DRESSES),
                strSpecialSigns=random.choice(SPECIAL_SIGNS),
            )
        )
    return suspects


def generate_vehicles_list() -> list[Vehicle]:
    vehicles = []
    vehicles_count = int(get_distribution_var_by_work_type(VEHICLES_COUNT_WORK_TYPE, "VEHICLES_COUNT"))
    for _ in range(vehicles_count):
        vehicles.append(
            Vehicle(
                strVehicleType=random.choice(VEHICLE_TYPES),
                strColorVehicleType=random.choice(VEHICLE_COLORS),
                strRegistrationNumber=random.choice(VEHICLE_NUMBERS),
                strRegion=random.choice(VEHICLE_REGIONS),
                bHidden=check_event_probability(VEHICLE_HIDDEN_PROBABILITY)
            )
        )
    return vehicles


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
                    strIncidentType=random.choice(INCIDENT_TYPES_FOR_CARD01),
                    strObject=random.choice(OBJECT_FOR_CARD01),
                    strStoreys=random.choice(INCIDENT_TYPES_FOR_CARD01),
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
                    strIncidentType=random.choice(INCIDENT_TYPES_FOR_CARD02),
                    iNumberOffenders=get_distribution_var_by_work_type(OFFENDERS_NUMBER_WORK_TYPE, "OFFENDERS_NUMBER"),
                    iNumberVehicle=get_distribution_var_by_work_type(VEHICLE_NUMBER_WORK_TYPE, "VEHICLE_NUMBER"),
                    suspect=generate_suspects_list(),
                    wantedPerson=generate_wanted_list(),
                    vehicle=generate_vehicles_list(),
                )
            case "card03":
                return Card03(
                    dtCreate=dt_create,
                    strIncidentType=random.choice(AMBULANCE_INCIDENT_TYPES),
                    strWhoCalled=random.choice(WHO_CALLED),
                    bConsultation=check_event_probability(AMBULANCE_CONSULT_PROBABILITY),
                    patient=generate_patients_list(),
                )
            case "card04":
                return Card04(
                    dtCreate=dt_create,
                    strIncidentType=random.choice(GAS_INCIDENT_TYPES),
                    strInstructions=random.choice(GAS_INSTRUCTIONS),
                    bConsultation=check_event_probability(GAS_CONSULT_PROBABILITY),
                )
            case "cardcommserv":
                return CardCommServ(
                    dtCreate=dt_create,
                    strIncidentType=random.choice(CS_INCIDENT_TYPES),
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
                    strIncidentType=random.choice(AT_INCIDENT_TYPE),
                    iPerishedPeople=int(
                        get_distribution_var_by_work_type(PERISHED_PEOPLE_WORK_TYPE, 'PERISHED_PEOPLE')),
                    iAffectedPeople=int(
                        get_distribution_var_by_work_type(AFFECTED_PEOPLE_WORK_TYPE, 'AFFECTED_PEOPLE')),
                    iSuspectPeople=int(get_distribution_var_by_work_type(SUSPECT_PEOPLE_WORK_TYPE, 'SUSPECT_PEOPLE')),
                    strSuspectDescription=random.choice(SUSPECT_DESCRIPTION),
                    strArmament=random.choice(ARMAMENTS),
                    strVehicles=[random.choice(ARMAMENTS) for _ in range(
                        int(get_distribution_var_by_work_type(ARMAMENTS_WORK_TYPE, "ARMAMENTS")))],
                    strDirection=random.choice(DIRECTION_TYPES),
                    strInjurySuspect=random.choice(AT_INJURIES)
                )


def generate_random_eos_list() -> list[EOSType]:
    """
    creates a list with random eos dicts from string_eos

    :return:
    """
    eos_list = []
    for eos_obj in EOSType:
        if eos_obj.value.get('p_min') is not None and eos_obj.value.get('class'):
            if _check_eos_probability(eos_obj):
                eos_list.append(eos_obj)
    return eos_list


def generate_eos_item_from_eos_list(eos_type_list: list[EOSType], operator: Operator) -> list[EosItem]:
    eos_items = []

    return eos_items


def main():
    for _ in range(1):
        d = generate_random_eos_list()
        for el in d:
            generate_card_from_eos_model(el, datetime.datetime.now(), Operator())


if __name__ == '__main__':
    main()
