
import unittest

from domain.validators import PersoanaValidator
from repository.exeptions.exeptions import DuplicateIDException, PersonNotFound, ValidationException
from repository.persoana_repository import Persoana_file_repo, Memory_rep_pers
from service.persoana_service import PersoanaService


class TestCasePersMemory(unittest.TestCase):
    def setUp(self) -> None:
        repo=Memory_rep_pers()
        val= PersoanaValidator()
        self.__srv= PersoanaService(repo, val)

    def test_adauga_persoana(self):
        self.__srv.adaug_persoana('4', 'Georgeta Vian', 'Terezin, nr.14A')

        self.assertTrue(len(self.__srv.get_persoane())==4)

        self.assertRaises(DuplicateIDException, self.__srv.adaug_persoana, '4', 'Ileana Man', 'EVEREN, NR.45')

        self.assertRaises(ValidationException, self.__srv.adaug_persoana, '1c', 'Ana Pop', 'EBE, nr.5')
        self.assertRaises(ValidationException, self.__srv.adaug_persoana, '5', 'Ani', 'Nei, nr.67')
        self.assertRaises(ValidationException, self.__srv.adaug_persoana, '5', 'Ani Olt', 'Neivii')

    def test_modifica_persoana(self):
        id_pers=1
        self.__srv.modifica_persoana(id_pers, 'Amalia Mianu', 'Bastionului, nr.5')
        for i, pers in enumerate(self.__srv.get_persoane()):
            if pers.get_id() == id_pers:
                index = i
        self.assertTrue(self.__srv.get_persoane()[index].get_nume()=='Amalia Mianu')

        id_pers=5
        self.assertRaises(PersonNotFound, self.__srv.modifica_persoana, id_pers, 'Piri Pop', 'Haha, nr.3')

        self.assertRaises(ValidationException, self.__srv.modifica_persoana, 'c', 'Ami', 'Privighetorii')

    def test_sterge_pers_id_dat(self):
        id_dat=2
        self.__srv.sterge_persoana(id_dat)
        self.assertTrue(len(self.__srv.get_persoane())==2)

        self.assertRaises(PersonNotFound, self.__srv.sterge_persoana, id_dat)

    def test_afisare_pers_nume_dat(self):
        nume='Popescu'
        lista=self.__srv.afiseaza_pers_nume_dat(nume)
        self.assertTrue(len(lista)==2)



