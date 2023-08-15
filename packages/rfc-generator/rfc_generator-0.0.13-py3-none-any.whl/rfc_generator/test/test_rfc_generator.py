import unittest
import string
from ..src.rfc_pf import RFC_PF
from ..src.rfc_pm import RFC_PM
import pytest


class GeneratorTest(unittest.TestCase):
    def test_generate_rfc_pf(self) -> None:
        rfc_pf = RFC_PF(
            nombres='Dimitrj',
            apellido_paterno='Bonansea',
            fecha_nacimiento='1989-06-10'
        )
        rfc = rfc_pf.generate()
        self.assertTrue(
            (rfc[:4] == "BODI") and (rfc[4:10] == "890610") and (rfc[-3:] == "MM6")
        )

    def test_invalid_brithdate_format_generate_rfc_pf(self) -> None:
        with pytest.raises(Exception) as exc:
            _ = RFC_PF(
                nombres='Dimitrj',
                apellido_paterno='Bonansea',
                fecha_nacimiento='1989-06-'
            )

        assert "Incorrect birthdate format, should be YYYY-MM-DD" in str(exc.value)
        assert exc.type == Exception

    def test_generate_rfc_pm(self) -> None:
        rfc_pm = RFC_PM(
            nombre_empresa="Sonora Industrial Azucarera, S. de R. L.",
            fecha_constitucion="1982-11-29"
        )
        rfc = rfc_pm.generate()
        self.assertTrue(
            (rfc[:3] == "SIA") and (rfc[3:9] == "821129") and (rfc[-3:] == "4L3")
        )
    
    def test_invalid_brithdate_format_generate_rfc_pm(self) -> None:
        with pytest.raises(Exception) as exc:
            _ = RFC_PM(
                nombre_empresa="Sonora Industrial Azucarera, S. de R. L.",
            fecha_constitucion="1982-11-2"
            )

        assert "Incorrect foundation date format, should be YYYY-MM-DD" in str(exc.value)
        assert exc.type == Exception