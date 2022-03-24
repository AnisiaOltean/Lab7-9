
import unittest

from domain.entities import Persoana
from domain.validators import PersoanaValidator
from repository.exeptions.exeptions import ValidationException


class TestCasePersDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.__validator = PersoanaValidator()

    def test_creare_persoana(self):
        p= Persoana('1', 'Mihai Edenescu', 'Bucium, nr.34')
        self.assertTrue(p.get_id() == '1')
        self.assertTrue(p.get_nume()=='Mihai Edenescu')
        self.assertTrue(p.get_adress()=='Bucium, nr.34')

        p.set_nume('Adriana Enescu')
        self.assertTrue(p.get_nume()=='Adriana Enescu')

    def test_validare_persoana(self):
        p=Persoana('1', 'Mihai Edenescu', 'Bucium, nr.34')
        self.__validator.validate(p)

        p=Persoana('2', 'Elena', 'Terezin, nr.12')
        self.assertRaises(ValidationException, self.__validator.validate, p)

        p = Persoana('2c', 'Elena', 'Terezin')
        self.assertRaises(ValidationException, self.__validator.validate, p)
