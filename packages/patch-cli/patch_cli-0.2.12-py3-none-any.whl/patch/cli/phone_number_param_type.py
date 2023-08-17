import typing as t

import click
import phonenumbers

from patch.tp.phone_number import PhoneNumber


class PhoneNumberParamType(click.ParamType):
    #  pylint: disable=no-init

    name = 'Phone Number'

    def convert(self, value: t.AnyStr, _param, _ctx) -> t.Optional[PhoneNumber]:
        if value is None:
            return None
        ph = phonenumbers.parse(value, "US")
        return PhoneNumber(ph.national_number, ph.country_code)
