import requests

url = "https://rsc.test.s112.fastec.ru/soap_4_3"

payload = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<SOAP-ENV:Envelope\n\txmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\"\n\txmlns:ns1=\"s112\">\n\t<SOAP-ENV:Body>\n"
    "<Ukios><Ukio><globalId>TEST_ZZZ_2201cd8b-a6e1-4bfb-adc4-7a6667210330</globalId><dtSend>2024-08-31T20:39:47.363025</dtSend><dtCreate>2024-08-31T20:39:31.363025</dtCreate><dtUpdate>2024-08-31T20:39:47.363025</dtUpdate><dtCall>2024-08-31T20:39:13.945236</dtCall><aCallEnded>False</aCallEnded><bHumanThreat>False</bHumanThreat><bChs>False</bChs><bWrong>False</bWrong><bChildPlay>False</bChildPlay><PhoneCall><phoneCallId>8fc25558-33fa-4b18-b153-d8eaabc53d32</phoneCallId><dtSend>2024-08-31T20:47:12.699121</dtSend><bOperatorIniciatied>True</bOperatorIniciatied><dtCall>2024-08-31T20:45:11.234023</dtCall><dtConnect>2024-08-31T20:45:13.334638</dtConnect><dtEndCall>2024-09-23T11:46:09.711434</dtEndCall></PhoneCall><PhoneCall><phoneCallId>aac05d83-79ee-4c26-9a76-79b9d5eeca29</phoneCallId><dtSend>2024-08-31T20:39:47.363025</dtSend><bOperatorIniciatied>False</bOperatorIniciatied><dtCall>2024-08-31T20:38:00</dtCall><dtConnect>2024-08-31T20:38:07.319441</dtConnect><bCallEnded>False</bCallEnded><aCallEnded>True</aCallEnded><dtEndCall>2024-08-31T20:39:08</dtEndCall><OperatorId>e1eab429-d828-496e-a38d-945788a520ae</OperatorId></PhoneCall><PhoneCall><phoneCallId>3708d1d1-7db0-4d7f-8619-0f7e9bad0952</phoneCallId><dtSend>2024-08-31T20:39:47.363025</dtSend><bOperatorIniciatied>True</bOperatorIniciatied><dtCall>2024-08-31T20:39:13.945236</dtCall><dtConnect>2024-08-31T20:39:31.363025</dtConnect><bCallEnded>True</bCallEnded><aCallEnded>False</aCallEnded><dtEndCall>2024-08-31T20:39:43.363025</dtEndCall><OperatorId>e1eab429-d828-496e-a38d-945788a520ae</OperatorId><RedirectCall><redirectCallId>1ac3147c-f9fb-4ae1-8c4e-cec91c18977c</redirectCallId><eosClassTypeId>5</eosClassTypeId><dtRedirectTime>2024-08-31T20:44:47.234023</dtRedirectTime><dtRedirectConfirm>2024-08-31T20:45:11.234023</dtRedirectConfirm><redirectCancel>False</redirectCancel><bConference>False</bConference><PhoneCallId>8fc25558-33fa-4b18-b153-d8eaabc53d32</PhoneCallId></RedirectCall></PhoneCall><CallContent><callContentId>45bac771-106d-4374-b404-e1a37df1002d</callContentId><strLastName>Богданова</strLastName><strName>Арина</strName><strMiddleName>Михайловна</strMiddleName><strCallerContactPhone>+7(968)-361-5631</strCallerContactPhone><strCgPN>+7(996)-688-4768</strCgPN><appResAddress>Хабаровский край, р-н Имени Полины Осипенко, 30 км от п. Бриакан</appResAddress><strLanguage>ru</strLanguage><strIncidentDescription>desc1</strIncidentDescription><appLocAddress>Хабаровский край, р-н Имени Лазо, село Дрофа</appLocAddress></CallContent><Address><addressId>773ed2fb-8dfa-49fe-830f-1583086ffd04</addressId><strAddress>проспект 60-летия Октября, 158А, Хабаровск</strAddress><geoLatitude>48.483592</geoLatitude><geoLongitude>135.109763</geoLongitude><strDistrict>железнодорожный район</strDistrict><strCity>Хабаровск</strCity><strStreet>60-летия Октября</strStreet><strHouse>158А</strHouse><strCityKLADR>2701800000000</strCityKLADR><strCityFIAS>e037f0b4-b7cc-4a06-9a08-70c4bc429452</strCityFIAS></Address><TransferItem><transferItemId>09b73704-2965-4dc5-8bdd-0e1d31a44684</transferItemId><eosClassTypeId>5</eosClassTypeId><dtTransfer>2024-08-31T20:39:47.363025</dtTransfer><bSuccess>True</bSuccess></TransferItem><EosItem><assignId>dec89402-43a8-4d9a-8796-94094c14d3d6</assignId><Operator><operatorId>e1eab429-d828-496e-a38d-945788a520ae</operatorId></Operator><operatorId>e1eab429-d828-496e-a38d-945788a520ae</operatorId><dtDepart>2024-08-31T20:38:42</dtDepart><dtConfirmDepart>2024-08-31T20:41:27</dtConfirmDepart><dtArrival>2024-08-31T20:42:28</dtArrival><dtComplete>2024-08-31T20:43:26</dtComplete><dispatchService><dispatchServiceId>6d99a975-e0be-40a3-b47e-36553d57f2ac</dispatchServiceId><eosClassTypeId>3</eosClassTypeId><strDispatchServiceName>Полиция</strDispatchServiceName></dispatchService><eosResource><eosResourceId>63e1c18f-fe94-4f31-9561-0aff6832227a</eosResourceId><eosClassTypeId>3</eosClassTypeId><strResourceUnitName>Бригада 1</strResourceUnitName><strMembership>mem1</strMembership></eosResource><eosResource><eosResourceId>a45828b3-2067-4a73-b501-31beaba40145</eosResourceId><eosClassTypeId>4</eosClassTypeId><strResourceUnitName>Бригада 3</strResourceUnitName><strMembership>mem3</strMembership></eosResource><eosResource><eosResourceId>bd5db141-63b8-4cf6-abb7-a77c4b2447b6</eosResourceId><eosClassTypeId>5</eosClassTypeId><strResourceUnitName>Бригада 3</strResourceUnitName><strMembership>mem1</strMembership></eosResource></EosItem><EosItem><assignId>0885fcbc-70c8-4f0f-a9d7-8dbf16c129f8</assignId><Operator><operatorId>e1eab429-d828-496e-a38d-945788a520ae</operatorId></Operator><operatorId>e1eab429-d828-496e-a38d-945788a520ae</operatorId><dtDepart>2024-08-31T20:38:27</dtDepart><dtConfirmDepart>2024-08-31T20:39:05</dtConfirmDepart><dtArrival>2024-08-31T20:39:56</dtArrival><dtComplete>2024-08-31T20:40:55</dtComplete><dispatchService><dispatchServiceId>96e73e44-a245-4dd1-a9c2-4f26b8ec596b</dispatchServiceId><eosClassTypeId>4</eosClassTypeId><strDispatchServiceName>Скорая помощь</strDispatchServiceName></dispatchService><eosResource><eosResourceId>ca658722-6d16-467d-a2ed-01e4e4137104</eosResourceId><eosClassTypeId>3</eosClassTypeId><strResourceUnitName>Бригада 1</strResourceUnitName><strMembership>mem3</strMembership></eosResource><eosResource><eosResourceId>d7c001b3-a7fe-47ca-9202-4e0ea44a3811</eosResourceId><eosClassTypeId>4</eosClassTypeId><strResourceUnitName>Бригада 1</strResourceUnitName><strMembership>mem1</strMembership></eosResource><eosResource><eosResourceId>1013f454-4896-4a43-a26b-fdb3c8e62d6c</eosResourceId><eosClassTypeId>5</eosClassTypeId><strResourceUnitName>Бригада 3</strResourceUnitName><strMembership>mem2</strMembership></eosResource></EosItem><EosItem><assignId>81749749-1d52-4fed-832d-c1584e854458</assignId><Operator><operatorId>e1eab429-d828-496e-a38d-945788a520ae</operatorId></Operator><operatorId>e1eab429-d828-496e-a38d-945788a520ae</operatorId><dtDepart>2024-08-31T20:39:35</dtDepart><dtConfirmDepart>2024-08-31T20:40:53</dtConfirmDepart><dtArrival>2024-08-31T20:42:05</dtArrival><dtComplete>2024-08-31T20:42:46</dtComplete><dispatchService><dispatchServiceId>55317994-a4fb-422a-b0b8-1ba9677a8a16</dispatchServiceId><eosClassTypeId>5</eosClassTypeId><strDispatchServiceName>Газовая служба</strDispatchServiceName></dispatchService><eosResource><eosResourceId>3ae83fc3-ddc6-4f72-b836-353013783deb</eosResourceId><eosClassTypeId>3</eosClassTypeId><strResourceUnitName>Бригада 1</strResourceUnitName><strMembership>mem1</strMembership></eosResource><eosResource><eosResourceId>baa2e82b-3caf-41f3-b1a7-7a1c4f30a98a</eosResourceId><eosClassTypeId>4</eosClassTypeId><strResourceUnitName>Бригада 3</strResourceUnitName><strMembership>mem3</strMembership></eosResource><eosResource><eosResourceId>c0313708-1af9-4704-9de6-fddff03923c2</eosResourceId><eosClassTypeId>5</eosClassTypeId><strResourceUnitName>Бригада 3</strResourceUnitName><strMembership>mem2</strMembership></eosResource></EosItem><Card02><card02Id>0370f5ad-7269-4569-8b95-ee53469e7486</card02Id><dtCreate>2024-08-31T20:44:41.220324</dtCreate><strIncidentType>-</strIncidentType><iNumberOffenders>6</iNumberOffenders><iNumberVehicle>5</iNumberVehicle><suspect><suspectId>37f40c1a-45e1-428f-b190-b5c4097f78cc</suspectId><strGender>M</strGender><iAge>29</iAge><strHeightType>Рост 1</strHeightType><strBodyType>тип тела 2</strBodyType><strDressed>одежда2</strDressed><strSpecialSigns>спец знак 2</strSpecialSigns></suspect><suspect><suspectId>0b684757-a1d8-4f67-b30e-48f476546f73</suspectId><strGender>F</strGender><iAge>27</iAge><strHeightType>Рост 2</strHeightType><strBodyType>тип тела 3</strBodyType><strDressed>одежда3</strDressed><strSpecialSigns>спец знак 2</strSpecialSigns></suspect><suspect><suspectId>837a2ed3-3b58-4c0f-a669-4ed8f84143e2</suspectId><strGender>M</strGender><iAge>26</iAge><strHeightType>Рост 1</strHeightType><strBodyType>Тип тела 1</strBodyType><strDressed>одежда1</strDressed><strSpecialSigns>спец знак 2</strSpecialSigns></suspect><suspect><suspectId>333310a4-4262-4d9a-9322-aaec661c4304</suspectId><strGender>F</strGender><iAge>27</iAge><strHeightType>Рост 2</strHeightType><strBodyType>тип тела 2</strBodyType><strDressed>одежда1</strDressed><strSpecialSigns>спец знак 2</strSpecialSigns></suspect><wantedPerson><wantedId>96831323-e7e5-46ea-a238-520bd25ae223</wantedId><strGender>M</strGender><iAge>32</iAge><strHeightType>Рост 2</strHeightType><strBodyType>тип тела 2</strBodyType><strDressed>одежда3</strDressed><strSpecialSigns>спец знак 1</strSpecialSigns><strLastName>Виноградов</strLastName><strName>Давид</strName><strMiddleName>Макарович</strMiddleName><dtDateBirth>1992-03-30T00:00:00</dtDateBirth></wantedPerson><wantedPerson><wantedId>a940995b-1e41-4294-8763-d564b89be74b</wantedId><strGender>F</strGender><iAge>33</iAge><strHeightType>Рост 1</strHeightType><strBodyType>Тип тела 1</strBodyType><strDressed>одежда2</strDressed><strSpecialSigns>спец знак 2</strSpecialSigns><strLastName>Калмыкова</strLastName><strName>София</strName><strMiddleName>Данииловна</strMiddleName><dtDateBirth>1991-03-24T00:00:00</dtDateBirth></wantedPerson><wantedPerson><wantedId>39ae7fc2-033d-4746-850b-dd5e7a2a1f8a</wantedId><strGender>F</strGender><iAge>36</iAge><strHeightType>Рост 1</strHeightType><strBodyType>Тип тела 1</strBodyType><strDressed>одежда1</strDressed><strSpecialSigns>спец знак 2</strSpecialSigns><strLastName>Евдокимова</strLastName><strName>Элина</strName><strMiddleName>Владиславовна</strMiddleName><dtDateBirth>1988-11-08T00:00:00</dtDateBirth></wantedPerson><wantedPerson><wantedId>a72ef798-ce86-4e09-9a36-a7a29f9f6967</wantedId><strGender>F</strGender><iAge>29</iAge><strHeightType>Рост 2</strHeightType><strBodyType>тип тела 3</strBodyType><strDressed>одежда3</strDressed><strSpecialSigns>спец знак 1</strSpecialSigns><strLastName>Иванова</strLastName><strName>Мария</strName><strMiddleName>Ивановна</strMiddleName><dtDateBirth>1995-03-06T00:00:00</dtDateBirth></wantedPerson><vehicle><vehicleId>b21b4978-2093-41f2-bb60-5b5c55cfbc2d</vehicleId><strVehicleType>vehicle type 2</strVehicleType><strColorVehicleType>color1</strColorVehicleType><strRegistrationNumber>number2</strRegistrationNumber><strRegion>region2 </strRegion><bHidden>False</bHidden></vehicle></Card02><Card03><card03Id>8d614b5a-3888-4829-991a-807ca58fca9f</card03Id><dtCreate>2024-08-31T20:44:43.185822</dtCreate><strIncidentType>-</strIncidentType><strWhoCalled>прохожий</strWhoCalled><bConsultation>True</bConsultation><patient><patientId>b8aba267-9781-4a91-a771-75983f0cd866</patientId><strLastName>Иванова</strLastName><strName>Карина</strName><strMiddleName>Евгеньевна</strMiddleName><dtDateBirth>1995-01-18T00:00:00</dtDateBirth><iAge>29</iAge><strGender>F</strGender><strOccasion>повод 1</strOccasion><strAbilityMoveIndependently>ability1</strAbilityMoveIndependently></patient><patient><patientId>67492490-89a2-4e95-abcc-844b27f036e2</patientId><strLastName>Ульянов</strLastName><strName>Степан</strName><strMiddleName>Иванович</strMiddleName><dtDateBirth>1995-10-05T00:00:00</dtDateBirth><iAge>29</iAge><strGender>M</strGender><strOccasion>повод 1</strOccasion><strAbilityMoveIndependently>ability2</strAbilityMoveIndependently></patient><patient><patientId>29bf33d2-c27f-45e5-a100-bf0a82a02a3c</patientId><strLastName>Федоров</strLastName><strName>Тимур</strName><strMiddleName>Романович</strMiddleName><dtDateBirth>1996-06-21T00:00:00</dtDateBirth><iAge>28</iAge><strGender>M</strGender><strOccasion>повод 1</strOccasion><strAbilityMoveIndependently>ability1</strAbilityMoveIndependently></patient><patient><patientId>5e4ece6c-d803-4f08-8ddc-b1cb6a7d52f7</patientId><strLastName>Виноградов</strLastName><strName>Давид</strName><strMiddleName>Макарович</strMiddleName><dtDateBirth>1997-02-19T00:00:00</dtDateBirth><iAge>27</iAge><strGender>M</strGender><strOccasion>повод 1</strOccasion><strAbilityMoveIndependently>ability1</strAbilityMoveIndependently></patient><patient><patientId>f2b219a8-2a48-4e92-ad6d-6f5a3df620bb</patientId><strLastName>Мешков</strLastName><strName>Александр</strName><strMiddleName>Елисеевич</strMiddleName><dtDateBirth>1995-01-30T00:00:00</dtDateBirth><iAge>29</iAge><strGender>M</strGender><strOccasion>повод 1</strOccasion><strAbilityMoveIndependently>ability1</strAbilityMoveIndependently></patient><patient><patientId>1b9543d1-a1c0-4a55-b501-92b6c71156ee</patientId><strLastName>Орлова</strLastName><strName>Аделина</strName><strMiddleName>Александровна</strMiddleName><dtDateBirth>1995-02-19T00:00:00</dtDateBirth><iAge>29</iAge><strGender>F</strGender><strOccasion>повод2</strOccasion><strAbilityMoveIndependently>ability2</strAbilityMoveIndependently></patient></Card03><Card04><card04Id>4e3e08cd-70e1-4ad4-a394-2d427dfce0b1</card04Id><dtCreate>2024-08-31T20:44:47.234023</dtCreate><strIncidentType>-</strIncidentType><strInstructions>instruction2</strInstructions><bConsultation>True</bConsultation></Card04></Ukio></Ukios>"
    "</SOAP-ENV:Body>\n</SOAP-ENV:Envelope>\n")
headers = {
    "Content-Type": "application/xml",
    "Authorization": "Basic cnNjLXJlZ2lvbi0yNzppbW00SjNUa0ZQRGJZbzh5dTRYdXFqZTA4cXlKVnhJVA=="
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)