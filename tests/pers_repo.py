import unittest

from domain.entities import Persoana
from repository.exeptions.exeptions import DuplicateIDException, PersonNotFound
from repository.persoana_repository import Memory_rep_pers, Persoana_file_repo


class TestCasePersMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Memory_rep_pers()
        # in repo exista deja 3 persoane adaugate!!!

    def test_adauga_pers(self):
        p1 = Persoana('4', 'Amalia Popescu', 'Bucium, nr.24')
        p2 = Persoana('5', 'Andrei Gheorghe', 'Terania, nr.24')

        self.repo.adauga(p1)
        self.assertTrue(self.repo.get_lungime_lista_persoane() == 4)

        self.repo.adauga(p2)
        self.assertTrue(self.repo.get_lungime_lista_persoane() == 5)

        self.assertRaises(DuplicateIDException, self.repo.adauga, p2)

    def test_modifica_persoana(self):
        id_pers = 3
        persoana = Persoana(id_pers, 'Mihai Popescu', 'Traian, nr.56V')

        self.repo.modifica_persoana_din_lista(id_pers, persoana)
        self.assertTrue(self.repo.find_pers_id(id_pers).get_nume() == 'Mihai Popescu')

        id_persoana=5
        self.assertRaises(PersonNotFound, self.repo.modifica_persoana_din_lista, id_persoana, persoana)

    def test_sterge_persoana_id_dat(self):
        id_pers='2'
        self.repo.sterge_persoana_id_dat(id_pers)
        self.assertTrue(self.repo.get_lungime_lista_persoane()==2)

        self.assertRaises(PersonNotFound, self.repo.sterge_persoana_id_dat, id_pers)

    def test_persoane_nume_dat(self):
        p1 = Persoana('4', 'Amalia Mihail', 'Bucium, nr.24')
        p2 = Persoana('5', 'Andrei Mihail', 'Terania, nr.24')

        self.repo.adauga(p1)
        self.repo.adauga(p2)

        lista=self.repo.lista_pers_nume_dat('Mihail')
        self.assertTrue(len(lista)==2)

        lista = self.repo.lista_pers_nume_dat('Emanoil')
        self.assertTrue(len(lista) == 0)

    def test_find_pers_id(self):
        p1 = Persoana('4', 'Amalia Mihail', 'Bucium, nr.24')
        self.repo.adauga(p1)

        #pers = self.repo.find_pers_id('4')
        self.assertTrue(self.repo.find_pers_id('4').get_nume()=='Amalia Mihail')


class TestCasePersFile(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Persoana_file_repo('pers_test.txt')
        self.repo.delete_all()

    def test_adauga_pers(self):
        p1 = Persoana('4', 'Amalia Popescu', 'Bucium, nr.24')
        p2 = Persoana('5', 'Andrei Gheorghe', 'Terania, nr.24')

        self.repo.adauga(p1)
        self.repo.adauga(p2)
        self.assertTrue(len(self.repo.get_persoane())==2)

        self.assertRaises(DuplicateIDException, self.repo.adauga, p1)

    def test_modifica_persoana(self):
        p1 = Persoana('4', 'Amalia Popescu', 'Bucium, nr.24')
        p2 = Persoana('5', 'Andrei Gheorghe', 'Terania, nr.24')

        self.repo.adauga(p1)
        self.repo.adauga(p2)

        id_pers=4
        p=Persoana(id_pers, 'Ania Meme', 'Blv. Incoronarii, nr.12B')
        self.repo.modifica_persoana_din_lista(id_pers, p)
        self.assertTrue(self.repo.find_pers_id(id_pers).get_nume()=='Ania Meme')

        id_pers=7
        self.assertRaises(PersonNotFound, self.repo.modifica_persoana_din_lista, id_pers, p)

    def test_sterge_pers_id_dat(self):
        p1 = Persoana('4', 'Amalia Popescu', 'Bucium, nr.24')
        p2 = Persoana('5', 'Andrei Gheorghe', 'Terania, nr.24')
        p3= Persoana('1', 'Diane Limina', 'Evangheliei, nr.24C')

        self.repo.adauga(p1)
        self.repo.adauga(p2)
        self.repo.adauga(p3)

        id_dat=5
        self.repo.sterge_persoana_id_dat(id_dat)
        self.assertTrue(len(self.repo.get_persoane())==2)

        self.assertRaises(PersonNotFound, self.repo.sterge_persoana_id_dat, id_dat)

    def test_persoane_nume_dat(self):
        p1 = Persoana('4', 'Amalia Mihail', 'Bucium, nr.24')
        p2 = Persoana('5', 'Andrei Mihail', 'Terania, nr.24')

        self.repo.adauga(p1)
        self.repo.adauga(p2)

        lista=self.repo.lista_pers_nume_dat('Mihail')
        self.assertTrue(len(lista)==2)

        lista = self.repo.lista_pers_nume_dat('Emanoil')
        self.assertTrue(len(lista) == 0)

    def test_find_pers_id(self):
        p1 = Persoana('4', 'Amalia Mihail', 'Bucium, nr.24')
        self.repo.adauga(p1)

        #pers = self.repo.find_pers_id('4')
        self.assertTrue(self.repo.find_pers_id('4').get_nume()=='Amalia Mihail')

        self.assertRaises(PersonNotFound, self.repo.find_pers_id, '5')



