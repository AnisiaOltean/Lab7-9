
import unittest

from domain.entities import Eveniment
from domain.validators import EvenimentValidator
from repository.exeptions.exeptions import ValidationException


class TestCaseEventDomain(unittest.TestCase):
    def setUp(self) -> None:
        self.__validator=EvenimentValidator()

    def test_creare_eveniment(self):
        ev= Eveniment('1', '14/02/2020', '15:30', 'Concert')

        self.assertTrue(ev.get_id()=='1')
        self.assertTrue(ev.get_data()=='14/02/2020')
        self.assertTrue(ev.get_time()=='15:30')
        self.assertTrue(ev.get_description()=='Concert')

        ev.set_date('15/07/2021')
        ev.set_time('14:00')

        self.assertTrue(ev.get_data()=='15/07/2021')
        self.assertTrue(ev.get_time()=='14:00')

    def test_validare_eveniment(self):
        e=Eveniment('c', '14/02/2020', '14:45', 'Concert')
        self.assertRaises(ValidationException, self.__validator.validate, e)

        e = Eveniment('1', '1z/02/2020', '14:45', 'Concert')
        self.assertRaises(ValidationException, self.__validator.validate, e)

        e = Eveniment('1', '14/19/2020', '14:45', 'Concert')
        self.assertRaises(ValidationException, self.__validator.validate, e)

        e = Eveniment('1', '14/02/202c', '14:45', 'Concert')
        self.assertRaises(ValidationException, self.__validator.validate, e)

        e = Eveniment('1', '14/02/2020', '1c:45', 'Concert')
        self.assertRaises(ValidationException, self.__validator.validate, e)

        e = Eveniment('1', '14/02/2020', '14:62', 'Concert')
        self.assertRaises(ValidationException, self.__validator.validate, e)
