import string

from domain.entities import Persoana
from domain.validators import PersoanaValidator
from repository.exeptions.exeptions import ValidationException, PersonNotFound
from repository.persoana_repository import Memory_rep_pers
import random


class PersoanaService:
    def __init__(self, repo, val):
        self.__repo = repo
        self.__validator = val

    def random_string_generator(self, size, letters):
        return ''.join(random.choice(letters) for x in range(size))

    def adauga_random(self):
        '''
        Genereaza valori random pt. id, nume si adresa
        :return:
        '''
        id = random.randint(3, 100)
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        name = self.random_string_generator(7, lowercase).capitalize() + ' ' + self.random_string_generator(7,lowercase).capitalize()
        adress = self.random_string_generator(6, lowercase).capitalize()+ ', nr. '+self.random_string_generator(2, string.digits)+self.random_string_generator(1, string.ascii_uppercase)
        self.adaug_persoana(id, name, adress)


    def adaug_persoana(self, id_pers, nume, adresa):
        '''
        Adauga persoana in lista de persoane
        :param id_pers: id-ul persoanei, nr. intreg
        :param nume: string, numele persoanei
        :param adresa: string, adresa persoanei
        :return: a, persoana creata
        '''
        a = Persoana(id_pers, nume, adresa)  # creeaza persoana
        self.__validator.validate(a)  # validez persoana
        self.__repo.adauga(a)  # adauga persoana

        return a

    def modifica_persoana(self, id_citit, nume, adresa):
        '''
        Modifica persoana cu id-ul citit de la tastatura cu datele persoanei citite
        :param id_pers: int, id-ul persoanei de modificat
        :param id_citit: id-ul citit de la tastatura
        :param nume: string, numele persoanei de modificat
        :param adresa: string, adresa persoanei de modificat
        :return:-
        '''
        p = Persoana(id_citit, nume, adresa)  # se creeaza noua persoana cu datele citite de la tastatura
        self.__validator.validate(p)  # se valideaza datele introduse de la tastatura
        # self.__validator.valid_id_citit(id_citit)  # valideaza id-ul citit de la tastatura
        self.__repo.modifica_persoana_din_lista(id_citit, p)  # se modifica persoana din lista

    def sterge_persoana(self, id_persoana):
        '''
        Sterge (elimina) din lista de persoane persoana cu id-ul citit de la tastatura
        :param id_persoana: int, id-ul persoanei
        :return: -
        '''
        # self.__validator.valid_id_in_lista(id_persoana,
        # self.__repo.get_persoane())  # valideaza id-ul citit de la tastatura
        self.__repo.sterge_persoana_id_dat(id_persoana)

    def afiseaza_pers_nume_dat(self, nume_citit):
        '''
        Creeaza lista de persoane ce au numele de familie egal cu cel citit de la tastatura
        :param nume_citit: string, numele citit
        :return: lista_pers, list, contine persoanele ce repecta conditia ceruta
        '''
        lista_pers = self.__repo.lista_pers_nume_dat(nume_citit)
        return lista_pers

    def get_persoane(self):
        return self.__repo.get_persoane()


def test_sterge_persoana():
    repo = Memory_rep_pers()
    val = PersoanaValidator()
    test_srv = PersoanaService(repo, val)
    id_citit = 3
    test_srv.sterge_persoana(id_citit)
    assert len(test_srv.get_persoane()) == 2
    # for el in test_srv.get_persoane():
    # print(el.get_id(), el.get_nume())
    id_citit = 4
    try:
        test_srv.sterge_persoana(id_citit)
        assert False
    #except ValueError as ve:
    except PersonNotFound as ve:
        #print(ve)
        assert True


test_sterge_persoana()


def test_adaug_persoana():
    repo = Memory_rep_pers()
    val = PersoanaValidator()
    test_srv = PersoanaService(repo, val)
    pers = test_srv.adaug_persoana(5, 'Mihai Enescu', 'Bastionului, nr. 23')

    assert pers.get_nume() == 'Mihai Enescu'
    assert len(test_srv.get_persoane()) == 4

    try:
        pers2 = test_srv.adaug_persoana('ac', 'Amalia', 'Independentei, nr.45A')
        assert False
    #except ValueError as ve:
    except ValidationException as ve:
        #print(ve)
        assert True


def test_modifica_persoana():
    repo = Memory_rep_pers()
    val = PersoanaValidator()
    test_srv = PersoanaService(repo, val)
    id_citit = 3
    for i, pers in enumerate(test_srv.get_persoane()):
        if pers.get_id() == id_citit:
            index = i
    test_srv.modifica_persoana(id_citit, 'Amalia Popescu', 'Bastionului, nr.5')
    assert test_srv.get_persoane()[index].get_nume() == 'Amalia Popescu'

    try:
        id_citit = 'a'
        test_srv.modifica_persoana(id_citit, 'Popescu Gheorghe', 'Bucuresti, nr.67C')
        assert False
    except ValidationException as ve:
        #print(ve)
        assert True


def test_afiseaza_persoane_nume_dat():
    repo = Memory_rep_pers()
    val = PersoanaValidator()
    test_srv = PersoanaService(repo, val)
    nume_citit = 'Popescu'
    lista_rez = test_srv.afiseaza_pers_nume_dat(nume_citit)
    # for pers in lista_rez:
    # print(pers.get_id(), pers.get_nume())
    assert len(lista_rez) == 2

    nume_citit = 'Traian'
    lista_rez = test_srv.afiseaza_pers_nume_dat(nume_citit)
    assert len(lista_rez) == 0


test_adaug_persoana()
test_modifica_persoana()
test_afiseaza_persoane_nume_dat()
