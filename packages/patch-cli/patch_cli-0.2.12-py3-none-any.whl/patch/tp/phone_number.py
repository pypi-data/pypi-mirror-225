class PhoneNumber:

    def __init__(self, number, country_code):
        self._number = number
        self._country_code = country_code

    @property
    def canonical(self):
        return f"+{self._country_code}{self._number}"
