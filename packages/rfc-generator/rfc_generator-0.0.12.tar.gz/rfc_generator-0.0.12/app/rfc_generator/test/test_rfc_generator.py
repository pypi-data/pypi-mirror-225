import unittest
import string
from ..src.rfc_pf import RFC_PF
from ..src.rfc_pm import RFC_PM


class GeneratorTest(unittest.TestCase):
    def test_generate_rfc_pf(self) -> None:
        rfc_pf = RFC_PF(
            nombres='Dimitrj',
            apellido_paterno='Bonansea',
            fecha_nacimiento='1989-06-10'
        )
        rfc = rfc_pf.generate()
        print(rfc[:4])
        print(rfc[4:10])
        print(rfc[-3:])
        self.assertTrue(
            (rfc[:4] == "BODI") and (rfc[4:10] == "890610") and (rfc[-3:] == "MM6")
        )

    def test_generate_rfc_pm(self) -> None:
        rfc_pm = RFC_PM(
            nombre_empresa="Sonora Industrial Azucarera, S. de R. L.",
            fecha_constitucion="1982-11-29"
        )
        rfc = rfc_pm.generate()
        print(rfc[:3])
        print(rfc[3:9])
        print(rfc[-3:])
        self.assertTrue(
            (rfc[:3] == "SIA") and (rfc[3:9] == "821129") and (rfc[-3:] == "4L3")
        )