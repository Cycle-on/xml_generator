from pprint import pprint

from google_sheet_parser import _get_service_acc
from constants import *

CARDS_INDEXES_INCIDENT_TYPES = {
    1: INCIDENT_TYPES_FOR_CARD01,
    2: INCIDENT_TYPES_FOR_CARD02,
    3: INCIDENT_TYPES_FOR_CARD03,
    4: INCIDENT_TYPES_FOR_CARD04,
    5: AT_INCIDENT_TYPES,
    6: CS_INCIDENT_TYPES,
}

s = [
    {'name': 'Авария ЖКХ в доме (электрика, вода, канализация, теплосеть)', 'ukio_count': 3, 'type': 'Пожарная Служба',
     'linked_eos': ['ЖКХ']},
    {'name': 'Аварийно - спасательные работы', 'ukio_count': 4, 'type': 'Пожарная Служба'},
    {'name': 'Возгорание на линии', 'ukio_count': 3, 'type': 'Пожарная Служба', 'linked_eos': ['Скорая помощь']},
    {'name': 'Вскрытие автомобиля', 'ukio_count': 5, 'type': 'Полиция'},
    {'name': 'Угроза убийством', 'ukio_count': 3, 'type': 'Полиция', 'linked_eos': ['Антитеррор']},
    {'name': 'Боли в животе', 'ukio_count': 15, 'type': 'Скорая помощь'},
    {'name': 'Боли в пояснице', 'ukio_count': 11, 'type': 'Скорая помощь'},
    {'name': 'Возгорание на линии', 'linked_eos': ['Пожарная Служба'], 'ukio_count': 3, 'type': 'Скорая помощь'},
    {'name': 'Газ. Запах газа в помещении.', 'ukio_count': 4, 'type': 'Газовая служба'},
    {'name': 'Угроза убийством', 'linked_eos': ['Полиция'], 'ukio_count': 3, 'type': 'Антитеррор'},
    {'name': 'Авария ЖКХ в доме (электрика, вода, канализация, теплосеть)', 'linked_eos': ['Пожарная Служба'],
     'ukio_count': 3, 'type': 'ЖКХ'}, {'name': 'ЖКХ', 'ukio_count': 9, 'type': 'ЖКХ'}
]


def __delete_duplicates_from_list():
    for k, lst in CARDS_INDEXES_INCIDENT_TYPES.items():
        doubles = []
        for el in lst:
            if el in doubles:
                continue
            doubles.append(el)
        CARDS_INDEXES_INCIDENT_TYPES[k] = doubles


def fill_incident_type_lists():
    global CARDS_INDEXES_INCIDENT_TYPES

    # resp = _get_service_acc('').spreadsheets().values().get(spreadsheetId=SHEET_ID,
    #                                                         range=f"{INCIDENT_TYPES_LIST_NAME}!A1:I999").execute()
    resp = {'range': 'IncidentTypes!A1:I999', 'majorDimension': 'ROWS',
            'values':
                [
                    ['ukio_type', 'count_ukio', 'Пожарная Служба', 'Полиция', 'Скорая помощь', 'Газовая служба',
                     'Антитеррор', 'ЖКХ'],
                    ['Авария ЖКХ в доме (электрика, вода, канализация, теплосеть)', '3', '1', '', '', '', '', '1'],
                    ['Аварийно - спасательные работы', '4', '1'], ['Боли в животе', '15', '', '', '1'],
                    ['Боли в пояснице', '11', '', '', '1'], ['Возгорание на линии', '3', '1', '', '1'],
                    ['Вскрытие автомобиля', '5', '', '1'], ['Газ. Запах газа в помещении.', '4', '', '', '', '1'],
                    ['Угроза убийством', '3', '', '1', '', '', '1'],
                    ['ЖКХ', '9', '', '', '', '', '', '1'],
                    ['test at type', '1', '', '', '', '', '1']
                ]

            }

    column_names = resp['values'][0]
    for el in resp['values'][1:]:
        incident_type_name = el[0]
        ukio_count = int(el[1])
        F: list[int] = []
        incident_type_names = []
        for i, bool_card_info in enumerate(el[2:], 1):  # eos iteration

            if bool(bool_card_info):

                if F:

                    CARDS_INDEXES_INCIDENT_TYPES[i].append({
                        'name': incident_type_name,
                        'linked_eos': [column_names[F[0] + 1]],
                        'ukio_count': ukio_count,
                        'type': column_names[i + 1]
                    })
                    incident_type_names.append(incident_type_name)
                    if CARDS_INDEXES_INCIDENT_TYPES[F[0]][-1].get('linked_eos'):
                        CARDS_INDEXES_INCIDENT_TYPES[F[0]][-1]['linked_eos'].append(column_names[i + 1])
                    else:
                        CARDS_INDEXES_INCIDENT_TYPES[F[0]][-1]['linked_eos'] = [column_names[i + 1]]
                    for eos_index in F[1:]:
                        CARDS_INDEXES_INCIDENT_TYPES[i][-1]['linked_eos'].append(column_names[eos_index + 1])
                        if CARDS_INDEXES_INCIDENT_TYPES[eos_index][-1].get('linked_eos'):
                            CARDS_INDEXES_INCIDENT_TYPES[eos_index][-1]['linked_eos'].append(
                                column_names[i + 1])
                        else:
                            CARDS_INDEXES_INCIDENT_TYPES[eos_index][-1]['linked_eos'] = [column_names[i + 1]]
                else:
                    if incident_type_name in incident_type_names:
                        continue
                    CARDS_INDEXES_INCIDENT_TYPES[i].append({
                        'name': incident_type_name,
                        'ukio_count': ukio_count,
                        "type": column_names[i + 1]
                    })
                    incident_type_names.append(incident_type_name)

                F.append(i)
    __delete_duplicates_from_list()
    return CARDS_INDEXES_INCIDENT_TYPES


fill_incident_type_lists()


def main():
    s = fill_incident_type_lists()
    pprint(s)


if __name__ == '__main__':
    main()
