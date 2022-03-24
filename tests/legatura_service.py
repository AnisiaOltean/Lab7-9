
import unittest

from domain.validators import LegaturaValidator
from repository.eveniment_repository import Event_file_repo
from repository.exeptions.exeptions import Legatura_creeata, PersonNotFound, EventNotFound
from repository.legatura_repository import LegaturaFileRepo
from repository.persoana_repository import Persoana_file_repo
from service.legatura_service import LegaturaService


class TestCaseLegSrvFile(unittest.TestCase):
    def setUp(self) -> None:
        repo = LegaturaFileRepo('leg_file_test.txt')
        val = LegaturaValidator()
        repo_pers = Persoana_file_repo('pers1.txt')
        repo_ev = Event_file_repo('evenimente1.txt')
        self.__leg_srv = LegaturaService(repo, val, repo_pers, repo_ev)


    def test_adauga_legatura(self):
        self.__leg_srv.adauga_pers_eveniment('1', '5')
        self.assertTrue(len(self.__leg_srv.get_lista_leg())==1)

        self.assertRaises(Legatura_creeata, self.__leg_srv.adauga_pers_eveniment,'1', '5')

        self.assertRaises(PersonNotFound, self.__leg_srv.adauga_pers_eveniment, '7', '2')
        self.assertRaises(EventNotFound, self.__leg_srv.adauga_pers_eveniment, '1', '4')

    def test_lista_ordoanta_data(self):
        self.__leg_srv.adauga_pers_eveniment('1', '3')
        self.__leg_srv.adauga_pers_eveniment('1', '5')
        self.__leg_srv.adauga_pers_eveniment('1', '6')

        lista_ev= self.__leg_srv.lista_ordonata_data('1')
        self.assertEqual(len(lista_ev), 3)

        self.assertEqual(lista_ev[0].get_id(), '3')
        self.assertEqual(lista_ev[1].get_id(), '6')
        self.assertEqual(lista_ev[2].get_id(), '5')

        self.assertRaises(PersonNotFound, self.__leg_srv.lista_ordonata_data, '7')

    def test_lista_ordonata_descriere(self):
        self.__leg_srv.adauga_pers_eveniment('1', '3')
        self.__leg_srv.adauga_pers_eveniment('1', '5')
        self.__leg_srv.adauga_pers_eveniment('1', '6')

        lista_ev = self.__leg_srv.lista_ordonata_descriere('1')
        self.assertEqual(len(lista_ev), 3)

        self.assertEqual(lista_ev[0].get_id(), '3')
        self.assertEqual(lista_ev[1].get_id(), '5')
        self.assertEqual(lista_ev[2].get_id(), '6')

        self.assertRaises(PersonNotFound, self.__leg_srv.lista_ordonata_descriere, '7')

    def test_persoane_nr_maxim_evenimente(self):
        self.__leg_srv.adauga_pers_eveniment('1', '3')
        self.__leg_srv.adauga_pers_eveniment('1', '5')
        self.__leg_srv.adauga_pers_eveniment('1', '6')
        self.__leg_srv.adauga_pers_eveniment('5', '7')
        self.__leg_srv.adauga_pers_eveniment('5', '13')
        self.__leg_srv.adauga_pers_eveniment('5', '16')

        lista=self.__leg_srv.return_lista_persoane_nr_maxim_de_evenimente()
        self.assertEqual(len(lista), 2)

        self.assertEqual(lista[0].get_nume(), 'Amalia Popescu')
        self.assertEqual(lista[1].get_nume(), 'Gigel Frone')

    def test_evenimente_most_participanti(self):
        self.__leg_srv.adauga_pers_eveniment('1', '3')
        self.__leg_srv.adauga_pers_eveniment('2', '5')
        self.__leg_srv.adauga_pers_eveniment('5', '6')
        self.__leg_srv.adauga_pers_eveniment('4', '3')
        self.__leg_srv.adauga_pers_eveniment('6', '3')
        self.__leg_srv.adauga_pers_eveniment('2', '6')

        lista=self.__leg_srv.evenimente_most_participanti()
        self.assertEqual(len(lista), 2)
        self.assertEqual(lista[0].get_nr_participanti(),3)
        self.assertEqual(lista[1].get_nr_participanti(), 2)

    def test_top_3evenimente(self):
        self.__leg_srv.adauga_pers_eveniment('1', '3')
        self.__leg_srv.adauga_pers_eveniment('2', '5')
        self.__leg_srv.adauga_pers_eveniment('5', '6')
        self.__leg_srv.adauga_pers_eveniment('4', '3')
        self.__leg_srv.adauga_pers_eveniment('6', '3')
        self.__leg_srv.adauga_pers_eveniment('2', '6')
        self.__leg_srv.adauga_pers_eveniment('3', '6')
        self.__leg_srv.adauga_pers_eveniment('1', '6')


        lista_ev=self.__leg_srv.top_3_evenimente()
        self.assertEqual(lista_ev[0].get_id(), '6')
        self.assertEqual(lista_ev[1].get_id(), '3')
        self.assertEqual(lista_ev[2].get_id(), '5')

    def tearDown(self) -> None:
        self.__leg_srv.delete_all()