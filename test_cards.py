import datetime

from schemas.Phone import Phone, RedirectCall
from schemas.models import Card, Police

cards = [
    Card(
        wrong=False,
        childPlay=False,
        card02=Police(dtCreate=datetime.datetime.now()),
        phoneCalls=[
            Phone(
                OperatorIniciatied=False,
                redirectCall=RedirectCall(
                    dtRedirectConfirm_=datetime.datetime.now(),
                    redirectCancel=True,
                    newPhoneCallId='1',
                    conference=False
                )
            ),
            Phone(
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
        wrong=False,
        childPlay=False,
        card02=Police(dtCreate=datetime.datetime.now()),
        phoneCalls=[
            Phone(
                OperatorIniciatied=False,
                redirectCall=RedirectCall(
                    dtRedirectConfirm_=datetime.datetime.now(),
                    redirectCancel=True,
                    newPhoneCallId='1',
                    conference=False
                )
            ),
            Phone(
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
