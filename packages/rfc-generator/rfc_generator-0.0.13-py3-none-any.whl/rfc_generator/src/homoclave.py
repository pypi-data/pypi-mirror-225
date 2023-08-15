from unidecode import unidecode


class Homoclave:
    _FULL_NAME_MAPPING = {
        " ": "00",
        "0": "00",
        "1": "01",
        "2": "02",
        "3": "03",
        "4": "04",
        "5": "05",
        "6": "06",
        "7": "07",
        "8": "08",
        "9": "09",
        "&": "10",
        "A": "11",
        "B": "12",
        "C": "13",
        "D": "14",
        "E": "15",
        "F": "16",
        "G": "17",
        "H": "18",
        "I": "19",
        "J": "21",
        "K": "22",
        "L": "23",
        "M": "24",
        "N": "25",
        "O": "26",
        "P": "27",
        "Q": "28",
        "R": "29",
        "S": "32",
        "T": "33",
        "U": "34",
        "V": "35",
        "W": "36",
        "X": "37",
        "Y": "38",
        "Z": "39",
        "Ñ": "40",
    }

    _HOMOCLAVE_DIGITS = "123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"

    def calculate(self, fullname) -> str:
        full_name = self._normalizeFullName(fullname)
        mapped_full_name = self._mapFullNameToDigitsCode(full_name)
        pairs_of_digits_sum = self._sumPairsOfDigits(mapped_full_name)
        homoclave = self._buildHomoclave(pairs_of_digits_sum)
        return homoclave

    def _normalizeFullName(self, fullname) -> str:
        full_name = fullname.upper()
        full_name = self._normalize(full_name)
        full_name = (
            full_name.replace(",", "")
            .replace(".", "")
            .replace("'", "")
            .replace("-", "")
        )
        full_name = self._addMissingCharToFullName(full_name, "Ñ")
        return full_name

    def _normalize(self, string) -> str:
        return unidecode(string)

    def _addMissingCharToFullName(self, full_name, missing_char) -> str:
        index = full_name.find(missing_char)
        if index == -1:
            return full_name

        while index >= 0:
            full_name[index] = missing_char
            index = full_name.find(missing_char)

        return str(full_name)

    def _mapFullNameToDigitsCode(self, full_name) -> str:
        mapped_full_name = "0"
        for i in range(len(full_name)):
            mapped_full_name += self._mapCharacterToTwoDigitCode(full_name[i])
        return mapped_full_name

    def _mapCharacterToTwoDigitCode(self, c) -> str:
        if c not in self._FULL_NAME_MAPPING:
            raise BaseException("No two-digit-code mapping for char: " + c)
        else:
            return self._FULL_NAME_MAPPING[c]

    def _sumPairsOfDigits(self, mapped_full_name) -> int:
        pairs_of_digits_sum = 0
        for i in range(len(mapped_full_name) - 1):
            int_num1 = int(mapped_full_name[i : i + 2])
            int_num2 = int(mapped_full_name[i + 1 : i + 2])
            pairs_of_digits_sum += int_num1 * int_num2
        return pairs_of_digits_sum

    def _buildHomoclave(self, pairs_of_digits_sum) -> str:
        last_three_digits = pairs_of_digits_sum % 1000
        quo = int(last_three_digits / 34)
        reminder = int(last_three_digits % 34)
        homoclave = str(self._HOMOCLAVE_DIGITS[quo]) + str(
            self._HOMOCLAVE_DIGITS[reminder]
        )
        return homoclave
