class VerificationDigit:
    _MAPPING = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
        "H": 17,
        "I": 18,
        "J": 19,
        "K": 20,
        "L": 21,
        "M": 22,
        "N": 23,
        "&": 24,
        "O": 25,
        "P": 26,
        "Q": 27,
        "R": 28,
        "S": 29,
        "T": 30,
        "U": 31,
        "V": 32,
        "W": 33,
        "X": 34,
        "Y": 35,
        "Z": 36,
        " ": 37,
        "Ñ": 38,
    }

    def calculate(self, rfc) -> str:
        sum = 0 if len(rfc) == 12 else 481
        range_value = 13 if len(rfc) == 12 else 12
        for i in range(range_value - 1):
            sum += self._mapDigit(rfc[i]) * (range_value - i)
        reminder = int(sum % 11)
        if reminder == 0:
            return "0"
        else:
            temp_reminder = 11 - reminder
            return f"{temp_reminder:x}".upper()

    def _mapDigit(self, char) -> str:
        key = str(char)
        if key not in self._MAPPING:
            return 0
        else:
            return self._MAPPING[key]
