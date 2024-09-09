import random
from datetime import timedelta as td

from config import DATE_ZERO
from constants import *
from generators import get_distribution_var_by_work_type, check_event_probability, genders, \
    get_random_birth_date_by_year
from generators.random_generators import get_random_name
from schemas.eos_for_ukio_models import Patient, WantedPerson, Suspect, Vehicle


def generate_patients_list() -> list[Patient]:
    patients = []
    patients_count = int(get_distribution_var_by_work_type(PATIENTS_COUNT_WORK_TYPE, 'PATIENTS_COUNT'))
    for _ in range(patients_count):
        gender = genders[check_event_probability(AMBULANCE_MALE_PROBABILITY)]
        surname, name, middle_name = get_random_name(gender)
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
        surname, name, middle_name = get_random_name(gender)
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
