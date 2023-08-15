from unidecode import unidecode
from num2words import num2words
from .homoclave import Homoclave
from .verification_digit import VerificationDigit
import re

class RFC_PM:
    _REGEX_DATE_FORMAT = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    _ROMAN_NUMBER_REGEX = "^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    _ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    _JURISTIC_PERSON_TYPE_REGEX = "(^S+\.+N+\.+C+\.)||(^S+\.+C+\.+L+\.)||(^S+\.+C+\.+S+\.)||(^A+\.+C+\.)||(^N+\.+C+\.)||(^S+\.+A+\.)||(^S+\.+C+\.)||(^R+\.+L+\.)||(^C+\.+V+\.)||(^S+\.)||(^R+\.)||(^C+\.)||(^V+\.)||(^L+\.)||(^A+\.)||(^N+\.)||(^P+\.)"

    _FORBIDDEN_WORDS = [
        "EL",
        "LA",
        "DE",
        "LOS",
        "LAS",
        "Y",
        "DEL",
        "MI",
        "POR",
        "CON",
        "AL",
        "SUS",
        "E",
        "PARA",
        "EN",
        "MC",
        "VON",
        "MAC",
        "VAN",
        "COMPANIA",
        "CIA",
        "CIA.",
        "SOCIEDAD",
        "SOC",
        "SOC.",
        "COMPANY",
        "CO",
        "COOPERATIVA",
        "COOP",
        "SC",
        "SCL",
        "SCS",
        "SNC",
        "SRL",
        "CV",
        "SA",
        "THE",
        "OF",
        "AND",
        "A",
    ]

    def __init__(self, nombre_empresa:str, fecha_constitucion:str) -> None:

        if len(nombre_empresa) <= 1:
            raise Exception("Error, company name should have at least 2 characters.")

        if not self._validate_date_format(fecha_constitucion):
            raise Exception("Incorrect foundation date format, should be YYYY-MM-DD")

        self.company_name = nombre_empresa.replace(",", " ").upper()
        self.day = fecha_constitucion.split("-")[2]
        self.month = fecha_constitucion.split("-")[1]
        self.year = fecha_constitucion.split("-")[0]
        self.homoclave = Homoclave()
        self.verification_digit = VerificationDigit()

    def _validate_date_format(self,date_text) -> bool:
        if self._REGEX_DATE_FORMAT.match(date_text):
            return True
        return False

    def generate(self) -> str:
        words = self.company_name.replace(",", "").split(" ")
        words = list(map(self._normalize, words))
        words = list(map(self._ignoreJuristicPersonTypeAbbreviations, words))
        words = self._remove_empty_words(words)
        words = list(map(self._ignoreForbiddenWords, words))
        words = self._remove_empty_words(words)
        words = list(map(self._markOneLetterAbbreviations, words))
        words = self._remove_empty_words(words)
        words = list(map(self._expandSpecialCharactersInSingletonWord, words))
        words = self._remove_empty_words(words)
        words = self._splitOneLetterAbbreviations(words)
        words = self._remove_empty_words(words)
        words = list(map(self._ignoreSpecialCharactersInWords, words))
        words = self._remove_empty_words(words)
        words = self._expandArabicNumerals(words)
        words = self._remove_empty_words(words)
        words = list(map(self._expandRomanNumerals, words))
        words = self._remove_empty_words(words)

        three_digit_code = self._threeDigitsCode(words)
        foundation_code = self._foundationCode()
        homoclave = self.homoclave.calculate(" ".join(words))
        verification_digit = self.verification_digit.calculate(
            three_digit_code + foundation_code + homoclave
        )

        return three_digit_code + foundation_code + homoclave + verification_digit

    def _normalize(self, word) -> str:
        return unidecode(word).upper().strip() if len(word) > 0 else word

    def _ignoreJuristicPersonTypeAbbreviations(self, word) -> str:
        return re.sub(self._JURISTIC_PERSON_TYPE_REGEX, "", word).strip()

    def _remove_empty_words(self, words) -> list:
        return [word for word in words if len(word) > 0]

    def _ignoreForbiddenWords(self, word) -> str:
        if word in self._FORBIDDEN_WORDS:
            return ""
        return word

    def _markOneLetterAbbreviations(self, word) -> str:
        return re.sub("^([^.])\\.", r"\1.AABBRREEVVIIAATTIIOONN", word)

    def _expandSpecialCharactersInSingletonWord(self, word) -> str:
        if len(word) == 1:
            return (
                word.replace("@", "ARROBA")
                .replace("´", "APOSTROFE")
                .replace("%", "PORCIENTO")
                .replace("#", "NUMERO")
                .replace("!", "ADMIRACION")
                .replace(".", "PUNTO")
                .replace("$", "PESOS")
                .replace('"', "COMILLAS")
                .replace("-", "GUION")
                .replace("/", "DIAGONAL")
                .replace("+", "SUMA")
                .replace("(", "ABRE PARENTESIS")
                .replace(")", "CIERRA PARENTESIS")
            )
        return word

    def _ignoreSpecialCharactersInWords(self, word) -> str:
        return re.sub('(.+?)[@´%#!.$"-/+\\(\\)](.+?)', r"\1\2", word)

    def _splitOneLetterAbbreviations(self, words) -> list:
        temp_words = "**********SPLIT**********".join(words)
        temp_words = temp_words.split("AABBRREEVVIIAATTIIOONN")
        final_words = list()
        for word in temp_words:
            final_words += word.split("**********SPLIT**********")
        return final_words

    def _expandArabicNumerals(self, words) -> str:
        final_words = list()
        for word in words:
            if re.match("[0-9]+", word):
                number = self._normalize(num2words(word, lang="es"))
                final_words += number.split(" ")
            else:
                final_words.append(word)
        return final_words

    def _expandRomanNumerals(self, word) -> str:
        if re.match(self._ROMAN_NUMBER_REGEX, word):
            return self._romanToInt(word)
        return word

    def _romanToInt(self, word) -> int:
        int_val = 0
        for i in range(len(word)):
            if i > 0 and self._ROMAN_VALUES[word[i]] > self._ROMAN_VALUES[word[i - 1]]:
                int_val += (
                    self._ROMAN_VALUES[word[i]] - 2 * self._ROMAN_VALUES[word[i - 1]]
                )
            else:
                int_val += self._ROMAN_VALUES[word[i]]
        return int_val

    def _threeDigitsCode(self, words) -> str:
        if len(words) >= 3:
            return words[0][0] + words[1][0] + words[2][0]
        elif len(words) == 2:
            return words[0][0] + words[1][0:2]
        return self._firstThreeCharactersWithRightPad(words[0])

    def _firstThreeCharactersWithRightPad(self, word) -> str:
        if len(word) >= 3:
            return word[0:3]
        return word.ljust(3, "X")

    def _foundationCode(self) -> str:
        return (
            self._lastTwoDigitsOf(self.year)
            + self._formattedInTwoDigits(self.month)
            + self._formattedInTwoDigits(self.day)
        )

    def _lastTwoDigitsOf(self, number) -> str:
        return number[-2:]

    def _formattedInTwoDigits(self, number) -> str:
        return number.rjust(2, "0")
