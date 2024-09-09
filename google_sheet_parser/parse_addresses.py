import random

from google_sheet_parser import _get_service_acc
from constants import *
from schemas.ukio_model import Address

ADDRESSES = []


def fill_with_address_headers(headers: list[str], address: list[str]):
    address_dict = {}
    for i in range(len(address)):
        if address[i] == '':
            continue
        if address[i][0] == 'n':
            address[i] = int(address[i])
        elif address[i][0] == 'b':
            address[i] = bool(address[i])
        address_dict[headers[i]] = address[i]
    return address_dict


def fill_addresses():
    """
    send request to google sheets and saving addresses in the list
    :return:
    """
    global ADDRESSES

    # resp = _get_service_acc().spreadsheets().values().get(spreadsheetId=SHEET_ID,
    #                                                         range=f"{ADDRESSES_LIST_NAME}!A1:AE999").execute()
    resp = {'range': 'Addresses!A1:AE999', 'majorDimension': 'ROWS', 'values': [
        ['strAddress', 'geoLatitude', 'geoLongitude', 'strCity', 'strDistrict', 'strStreet', 'strHouse', 'strHouseSlah',
         'strCorps', 'strBuilding', 'strHolding', 'strEntrance', 'nFloor', 'strRoom', 'strEntranceCode', 'strRoad',
         'nKm', 'nM', 'strAddressSection', 'bNear', 'strPlace', 'OKATO', 'OKTMO', 'strDistrictKLADR', 'strCityKLADR',
         'strStreetKLADR', 'strDistrictFIAS', 'strCityFIAS', 'strStreetFIAS', 'strHouseFIAS', 'orgOKPO'],
        ['переулок Дежнёва, 17, Хабаровск', '48.500378', '135.104486', 'Хабаровск', 'железнодорожный район', '', '17',
         '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2701800000000', '', '',
         'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['Промышленная улица, 19к1, Хабаровск', '48.494561', '135.104112', 'Хабаровск', 'железнодорожный район',
         'Промышленная', '19', '', '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2701800000000', '',
         '', 'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['Хабаровская улица, 8, Хабаровск', '48.488679', '135.107283', 'Хабаровск', 'железнодорожный район',
         'Хабаровская', '8', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2701800000000', '',
         '', 'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['проспект 60-летия Октября, 158А, Хабаровск', '48.483592', '135.109763', 'Хабаровск', 'железнодорожный район',
         '60-летия Октября', '158А', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
         '2701800000000', '', '', 'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['улица Гагарина, 11, микрорайон имени Горького, Хабаровск', '48.458491', '135.184637', 'Хабаровск',
         'железнодорожный район', 'Гагарина', '11', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
         '2701800000000', '', '', 'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['Новая улица, 7, Железнодорожный район, Хабаровск', '48.434436', '135.153116', 'Хабаровск',
         'железнодорожный район', 'Новая', '7', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
         '2701800000000', '', '', 'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['Целинная улица, 31, Хабаровск', '48.428040', '135.155487', 'Хабаровск', 'железнодорожный район', 'Целинная',
         '31', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2701800000000', '', '',
         'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['Овражная улица, 2/8, Хабаровск', '48.515418', '135.075798', 'Хабаровск', 'железнодорожный район', 'Овражная',
         '2/8', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2701800000000', '', '',
         'e037f0b4-b7cc-4a06-9a08-70c4bc429452'],
        ['улица Героев Пассаров, 45/7, Хабаровск', '48.533242', '135.086658', 'Хабаровск', 'железнодорожный район',
         'Героев Пассаров', '45/7', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '2701800000000',
         '', '', 'e037f0b4-b7cc-4a06-9a08-70c4bc429452']]}

    headers = resp['values'][0]
    for el in resp['values'][1:]:
        address_dict_with_headers = fill_with_address_headers(headers, el)
        ADDRESSES.append(Address(**address_dict_with_headers))


def get_random_address() -> tuple[str, str, str, str, str, str, str]:
    """
    :return: string_address, lat, long, city, district, kladr, fias
    """
    global ADDRESSES

    return random.choice(ADDRESSES)


if __name__ == '__main__':
    fill_addresses()
    print(get_random_address())
