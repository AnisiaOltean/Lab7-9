
import unittest

from domain.entities import Eveniment
from domain.validators import EvenimentValidator
from repository.eveniment_repository import Memory_rep_event
from repository.exeptions.exeptions import DuplicateIDException, ValidationException, EventNotFound
from service.eveniment_service import EvenimentService


class TestCaseEventRepoMemory(unittest.TestCase):
    def setUp(self) -> None:
        repo= Memory_rep_event()
        val= EvenimentValidator()
        self.__srv= EvenimentService(repo, val)

    def test_adaug_eveniment(self):
        self.__srv.adauga_eveniment('4', '13/02/2021', '16:14', 'Concert')
        self.assertTrue(len(self.__srv.get_lista_evenimente())==4)

        self.assertRaises(DuplicateIDException, self.__srv.adauga_eveniment, 4, '14/03/2029', '12:00', 'Inmormantare')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5c', '14/02/2020', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '1c/02/2020', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '32/02/2020', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/0v/2020', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/13/2020', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/02/202m', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/02/2020', '1c:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/02/2020', '25:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/02/2020', '13:0x', 'Concert')
        self.assertRaises(ValidationException, self.__srv.adauga_eveniment, '5', '14/02/2020', '13:61', 'Concert')

    def test_modific_eveniment(self):
        self.__srv.adauga_eveniment('4', '13/02/2021', '16:14', 'Concert')
        self.__srv.modifica_eveniment('4', '5/03/2020', '17:00', 'Botez')
        for i, el in enumerate(self.__srv.get_lista_evenimente()):
            if el.get_id() == '4':
                index = i
        self.assertTrue(self.__srv.get_lista_evenimente()[index].get_data()=='5/03/2020')
        self.assertTrue(self.__srv.get_lista_evenimente()[index].get_description()=='Botez')

        self.assertRaises(EventNotFound, self.__srv.modifica_eveniment, '5', '13/02/2020', '12:30', 'Inmormantare')
        self.assertRaises(ValidationException, self.__srv.modifica_eveniment, 'c', '14/02/2020', '13:00', 'Concert')
        self.assertRaises(ValidationException, self.__srv.modifica_eveniment, '2', '15/16/21c4', '8:00', 'Botez')

    def test_sterge_eveniment(self):
        self.__srv.sterge_eveniment_din_lista('3')
        self.assertTrue(len(self.__srv.get_lista_evenimente())==2)

        self.assertRaises(EventNotFound, self.__srv.sterge_eveniment_din_lista, 3)

    def test_cauta_dupa_descriere(self):
        self.__srv.adauga_eveniment('4', '29/03/2021', '17:00', 'Majorat')
        descriere='Majorat'
        lista=self.__srv.cauta_dupa_descriere(descriere)
        self.assertTrue(len(lista)==1)

        descriere='Nunta'
        self.__srv.adauga_eveniment('5', '15/04/2020', '13:30', 'Nunta')
        lista=self.__srv.cauta_dupa_descriere(descriere)
        self.assertTrue(len(lista)==3)











