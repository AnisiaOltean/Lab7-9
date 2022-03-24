
import unittest

from domain.entities import Eveniment
from repository.eveniment_repository import Memory_rep_event, Event_file_repo
from repository.exeptions.exeptions import DuplicateIDException, EventNotFound


class TestCaseEvenimentRepoMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.repo= Memory_rep_event()
        #in repo exista 3 evenimente adaugate!!

    def test_adauga_eveniment(self):
        e=Eveniment('4', '13/05/2019', '19:00', 'Party')
        self.repo.adauga_eveniment(e)
        self.assertTrue(self.repo.get_lungime_lista_evenimente()==4)
        e = Eveniment('1', '13/05/2019', '19:00', 'Party')
        self.assertRaises(DuplicateIDException, self.repo.adauga_eveniment, e)

    def test_modifica_eveniment(self):
        id_dat=2
        e=Eveniment(id_dat, '13/01/2022', '12:00', 'Revelion')
        self.repo.modifica_eveniment(id_dat, e)

        self.assertTrue(self.repo.find_ev_id(id_dat).get_data()=='13/01/2022')
        self.assertTrue(self.repo.find_ev_id(id_dat).get_description()=='Revelion')

        id_dat=4
        self.assertRaises(EventNotFound, self.repo.modifica_eveniment, id_dat, e)

    def test_sterge_ev_id_dat(self):
        id=2
        self.repo.sterge_eveniment(id)
        self.assertTrue(self.repo.get_lungime_lista_evenimente()==2)

        self.assertRaises(EventNotFound, self.repo.sterge_eveniment, id)

    def test_evenimente_decriere_data(self):
        e=Eveniment('4', '11/09/2020', '13:45', 'Nunta')
        self.repo.adauga_eveniment(e)
        e=Eveniment('5', '14/04/2020', '15:00', 'Nunta')
        self.repo.adauga_eveniment(e)
        filter_by_description = lambda x: x.get_description() == 'Nunta'
        filtered_by_description = self.repo.filter_by_function(filter_by_description)
        self.assertTrue(len(filtered_by_description)==4)

class TestCaseEvenimentFileRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.repo= Event_file_repo('eveniment_test.txt')
        self.repo.delete_all()

    def test_adauga_eveniment(self):
        e=Eveniment('1', '12/02/2020', '17:59', 'Concert')
        self.repo.adauga_eveniment(e)
        self.assertTrue(len(self.repo.get_evenimente())==1)

        self.assertRaises(DuplicateIDException, self.repo.adauga_eveniment, e)

    def test_modifica_eveniment(self):
        e = Eveniment('1', '12/02/2020', '17:59', 'Concert')
        self.repo.adauga_eveniment(e)
        e1 = Eveniment('2', '2/01/2021', '17:59', 'Party')
        e2 = Eveniment('4', '13/11/2020', '16:00', 'Botez')
        self.repo.adauga_eveniment(e1)
        self.repo.adauga_eveniment(e2)

        id_modif=2
        ev= Eveniment(id_modif, '1/1/2021', '17:45', 'Nunta')
        self.repo.modifica_eveniment(id_modif, ev)
        self.assertTrue(self.repo.find_ev_id(id_modif).get_data()=='1/1/2021')
        self.assertTrue(self.repo.find_ev_id(id_modif).get_description()=='Nunta')

        id_modif=3
        self.assertRaises(EventNotFound, self.repo.modifica_eveniment, id_modif, ev)

    def test_sterge_ev_id_dat(self):
        e = Eveniment('1', '12/02/2020', '17:59', 'Concert')
        self.repo.adauga_eveniment(e)
        e1 = Eveniment('2', '2/01/2021', '17:59', 'Party')
        e2 = Eveniment('4', '13/11/2020', '16:00', 'Botez')
        self.repo.adauga_eveniment(e1)
        self.repo.adauga_eveniment(e2)

        self.repo.sterge_eveniment(2)
        self.assertTrue(len(self.repo.get_evenimente())==2)

        self.assertRaises(EventNotFound, self.repo.sterge_eveniment, '2')

    def test_evenimente_decriere_data(self):
        e=Eveniment('4', '11/09/2020', '13:45', 'Nunta')
        self.repo.adauga_eveniment(e)
        e=Eveniment('5', '14/04/2020', '15:00', 'Nunta')
        self.repo.adauga_eveniment(e)
        filter_by_description = lambda x: x.get_description() == 'Nunta'
        filtered_by_description = self.repo.filter_by_function(filter_by_description)
        self.assertTrue(len(filtered_by_description)==2)


