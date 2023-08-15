from unidecode import unidecode
from .homoclave import Homoclave
from .verification_digit import VerificationDigit
import re
import datetime


class RFC_PF:
    _SPECIAL_PARTICLES = {
        "DE",
        "LA",
        "LAS",
        "MC",
        "VON",
        "DEL",
        "LOS",
        "Y",
        "MAC",
        "VAN",
        "MI",
    }
    _FORBIDDEN_WORDS = {
        "BUEI",
        "BUEY",
        "CACA",
        "CACO",
        "CAGA",
        "CAGO",
        "CAKA",
        "CAKO",
        "COGE",
        "COJA",
        "COJE",
        "COJI",
        "COJO",
        "CULO",
        "FETO",
        "GUEY",
        "JOTO",
        "KACA",
        "KACO",
        "KAGA",
        "KAGO",
        "KOGE",
        "KOJO",
        "KAKA",
        "KULO",
        "MAME",
        "MAMO",
        "MEAR",
        "MEAS",
        "MEON",
        "MION",
        "MOCO",
        "MULA",
        "PEDA",
        "PEDO",
        "PENE",
        "PUTA",
        "PUTO",
        "QULO",
        "RATA",
        "RUIN",
    }

    _REGEX_FILTER_NAME = "^(MA|MA.|MARIA|JOSE)\\s+"

    def __init__(self, nombres:str, apellido_paterno:str, fecha_nacimiento:str, apellido_materno:str = None):
        if nombres and len(nombres) <= 1:
            raise Exception("Error, firstname should have at least 2 characters.")
        
        if apellido_paterno and len(apellido_paterno) <= 1:
            raise Exception("Error, paternal lastname should have at least 2 characters.")
        
        if apellido_materno and len(apellido_materno) <= 1:
            raise Exception("Error, maternal lastname should have at least 2 characters.")
        
        if fecha_nacimiento and not self._validate_date_format(fecha_nacimiento):
            raise Exception("Incorrect birthdate format, should be YYYY-MM-DD")

        
        self.first_name = nombres.upper()
        self.first_last_name = apellido_paterno.upper()
        self.second_last_name = apellido_materno.upper() if apellido_materno else ""
        
        self.day = fecha_nacimiento.split("-")[2]
        self.month = fecha_nacimiento.split("-")[1]
        self.year = fecha_nacimiento.split("-")[0]
        self.homoclave = Homoclave()
        self.verification_digit = VerificationDigit()

    def _validate_date_format(date_text) -> bool:
        try:
            datetime.date.fromisoformat(date_text)
            return True
        except ValueError:
            return False

    def generate(self) -> str:
        name_code = self._obfuscateForbiddenWords(self._nameCode())
        birthday_code = self._birthdayCode()
        homoclave = self.homoclave.calculate(
            self.first_name + " " + self.first_last_name + " " + self.second_last_name,
        )
        verification_digit = self.verification_digit.calculate(
            name_code + birthday_code + homoclave
        )
        return name_code + birthday_code + homoclave + verification_digit

    def _obfuscateForbiddenWords(self, namecode) -> str:
        for forbidden in self._FORBIDDEN_WORDS:
            if forbidden == namecode:
                return namecode[0:3] + "X"

        return namecode

    def _nameCode(self) -> str:
        if self._isFirstLastNameEmpty():
            return self._firstLastNameEmptyForm()
        elif self._isSecondLastNameEmpty():
            return self._secondLastNameEmptyForm()
        elif self._isFirstLastNameIsTooShort():
            return self._firstLastNameTooShortForm()
        else:
            return self._normalForm()

    def _normalize(self, string) -> str:
        return unidecode(string)

    def _isFirstLastNameEmpty(self) -> bool:
        temp_string = self._normalize(self.first_last_name)
        if not temp_string or not temp_string.strip():
            return True
        return False

    def _isSecondLastNameEmpty(self) -> bool:
        temp_string = self._normalize(self.second_last_name)
        if not temp_string or not temp_string.strip():
            return True
        return False

    def _isFirstLastNameIsTooShort(self) -> bool:
        return len(self._normalize(self.first_last_name)) <= 2

    def _firstLastNameEmptyForm(self) -> str:
        return self._firstTwoLettersOf(self.second_last_name) + self._firstTwoLettersOf(
            self._filterName(self.first_name)
        )

    def _firstTwoLettersOf(self, word) -> str:
        return self._normalize(word)[:2]

    def _filterName(self, name) -> str:
        temp_name = self._normalize(name).strip()
        return re.sub(self._REGEX_FILTER_NAME, "", temp_name, 1)

    def _normalForm(self) -> str:
        return (
            self._firstLetterOf(self.first_last_name)
            + self._firstVowelExcludingFirstCharacterOf(self.first_last_name)
            + self._firstLetterOf(self.second_last_name)
            + self._firstLetterOf(self._filterName(self.first_name))
        )

    def _firstLastNameTooShortForm(self) -> str:
        return (
            self._firstLetterOf(self.first_last_name)
            + self._firstLetterOf(self.second_last_name)
            + self._firstTwoLettersOf(self._filterName(self.first_name))
        )

    def _secondLastNameEmptyForm(self) -> str:
        return self._firstTwoLettersOf(self.first_last_name) + self._firstTwoLettersOf(
            self._filterName(self.first_name)
        )

    def _firstLetterOf(self, word) -> str:
        return self._normalize(word)[0]

    def _firstVowelExcludingFirstCharacterOf(self, word) -> str:
        temp_word = self._normalize(word)[1:]
        for _, char in enumerate(temp_word):
            if char in "AEIOU":
                return char
        return "X"

    def _birthdayCode(self) -> str:
        return (
            self._lastTwoDigitsOf(self.year)
            + self._formattedInTwoDigits(self.month)
            + self._formattedInTwoDigits(self.day)
        )

    def _lastTwoDigitsOf(self, number) -> str:
        return self._formattedInTwoDigits(int(number) % 100)

    def _formattedInTwoDigits(self, number) -> str:
        return str(number).zfill(2)
