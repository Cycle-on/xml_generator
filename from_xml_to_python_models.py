from bs4 import BeautifulSoup

with open('wsdl_4_3.wsdl') as f:
    s = BeautifulSoup(f.read(), 'xml')
normal_type = {
    'string': 'str',
    'integer': 'int',
    'dateTime': 'datetime.datetime',
    'boolean': 'bool',
    'tns:Operator': 'Operator'
}
for el in s.find_all('complexType'):
    print(f"class {el.get('name')}:")

    for le in el.find_next('sequence'):
        if le is not None and le not in ('', ' ', '\n'):
            # print('pn')
            # print(le)
            # print('pn')
            print(f"  {le.get('name')}: {normal_type.get(le.get('type'), le.get('type'))} = None")
