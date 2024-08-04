import datetime

from schemas.Phone import Phone, RedirectCall
from schemas.models import Card, Police

cards = [
    Card(
        globalId='2',
        wrong=False,
        childPlay=False,
        card02=Police(dtCreate=datetime.datetime.now()),
        phoneCalls=[
            Phone(
                phoneCallId='1',
                OperatorIniciatied=False,
                redirectCall=RedirectCall(
                    dtRedirectConfirm_=datetime.datetime.now(),
                    redirectCancel=True,
                    newPhoneCallId='1',
                    conference=False
                )
            ),
            Phone(
                phoneCallId='2',
                OperatorIniciatied=False,
                redirectCall=RedirectCall(
                    dtRedirectConfirm_=datetime.datetime.now(),
                    redirectCancel=True,
                    newPhoneCallId='1',
                    conference=False
                )
            )
        ]
    ),
    Card(
        globalId='3',
        wrong=False,
        childPlay=False,
        card02=Police(dtCreate=datetime.datetime.now()),
        phoneCalls=[
            Phone(
                phoneCallId='1',
                OperatorIniciatied=False,
                redirectCall=RedirectCall(
                    dtRedirectConfirm_=datetime.datetime.now(),
                    redirectCancel=True,
                    newPhoneCallId='1',
                    conference=False
                )
            ),
            Phone(
                phoneCallId='2',
                OperatorIniciatied=False,
                redirectCall=RedirectCall(
                    dtRedirectConfirm_=datetime.datetime.now(),
                    redirectCancel=True,
                    newPhoneCallId='1',
                    conference=False
                )
            )
        ]
    ),

]
