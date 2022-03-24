import random
#from datetime import date
from random import randint

from domain.entities import Eveniment, Entitate_legatura
from domain.validators import EvenimentValidator
from repository.eveniment_repository import Memory_rep_event
#from repository.legatura_repository import Memory_rep_legatura
from repository.exeptions.exeptions import ValidationException, EventNotFound, DuplicateIDException


class EvenimentService:
    def __init__(self, repo, val):
        self.__repo = repo
        self.__val = val

    def random_string_generator(self, size, letters):
        return ''.join(random.choice(letters) for x in range(size))

    def adauga_eveniment_random(self):
        '''
        Genereaza un eveniment random
        :return:
        '''
        id_event = randint(4,25)
        data= self.random_string_generator(1, '012')+self.random_string_generator(1, '123')+'/'+self.random_string_generator(1,'123456789')+'/'+self.random_string_generator(1, '12')+self.random_string_generator(3, '0123456')
        timp= self.random_string_generator(1, '01')+self.random_string_generator(1,'1234566789')+':'+self.random_string_generator(1, '01234')+self.random_string_generator(1, '012345')
        descriere=self.random_string_generator(7, 'abcdefghijklmnopqrtuvwxyz').capitalize()
        self.adauga_eveniment(id_event, data, timp, descriere)


    def adauga_eveniment(self, id_event, data, timp, descriere):
        '''
        Adauga evenimentul cu id-ul, data, timpul si descrierea citite de la tastatura
        Se valideaza datele introduse de utilizator
        :param id_event: int, id-ul evenimentului
        :param data: string, data evenimentului
        :param timp: string, timpul evenimentului
        :param descriere: string, descrierea eveniemntului
        :return: e, evenimentul creat
        :raises: ValueError daca sunt gasite date invalide introduse
        '''
        e = Eveniment(id_event, data, timp, descriere)  # creeaza obiectul de tip eveniment
        self.__val.validate(e)  # valideaza evenimentul
        self.__repo.adauga_eveniment(e)  # adauga evenimentul in lista de evenimente
        return e

    def modifica_eveniment(self, id_citit, data, timp, descriere):
        '''
        Modifica evenimentul cu id-ul citit de la tastatura cu cel format din datele noului eveniment citie,
        id_eveniment, data, timp, descriere
        :param id_citit: int, id-ul evenimentului de modificat
        :param id_eveniment: int, id-ul noului eveniment
        :param data: string, data noului eveniment
        :param timp: string, timpul noului eveniment
        :param descriere: string, descrierea noului eveniment
        :return: -
        :raises: ValueError daca sunt gasite date de intrare invalide
        '''
        e = Eveniment(id_citit, data, timp, descriere)  # se creeaza noul eveniment
        self.__val.validate(e)  # se valideaza noul eveniment
        # self.__val.valid_id_citit(id_citit)  # se valideaza id-ul citit
        self.__repo.modifica_eveniment(id_citit, e)  # se modifica evenimentul

    def sterge_eveniment_din_lista(self, id_citit):
        '''
        Sterge evenimentul din lista ce are id-ul egal cu cel citit de la tastaturas
        :param id_citit: string, id-ul citit
        :return: -
        '''
        self.__val.valid_id_citit(id_citit)  # valideaza id-ul citit de la tastatura
        self.__repo.sterge_eveniment(id_citit)

    def cauta_dupa_descriere(self, descriere):
        '''
        Returneaza o noua lista de evenimente ce contine doar evenimentele cu descrierea data
        :param descriere: string, descrierea unui eveniment
        :return: new_list, lista de evenimente ce respecta cerinta
        '''
        lista_evenimente = self.get_lista_evenimente()
        filter_criteria = lambda x: x.get_description() == descriere
        new_list = self.__repo.filter_by_function(filter_criteria)
        return new_list

    def get_lista_evenimente(self):
        return self.__repo.get_evenimente()


    # def lista_evenimente_ordonata_persoana(self, id_persoana, lista_legaturi):
    #     '''
    #     Returneaza lista de evenimente la care participa persoana cu id-ul dat ordonata dupa data
    #     :param id_persoana: string, id-ul persoanei
    #     :return: lista_evenimente, list, lista ce respecta conditia data
    #     '''
    #     lista_persoane=self.__repo.return_lista_evenimente_persoana(id_persoana, lista_legaturi)
    #     return lista_persoane

    # def lista_evenimente_ord_descr(self, id_persoana, lista_legaturi):
    #     '''
    #     Returneaza lista de evenimente la care participa o persoana cu id-ul dat ordonata dupa descriere
    #     :param id_persoana: string, id-ul persoanei citit de la tastatura
    #     :param lista_legaturi: list, lista ce contine lista de legaturi (id-urile)
    #     :return: lista_evenimente
    #     '''
    #     lista_evenimente = self.__repo.return_lista_ord_descr(id_persoana, lista_legaturi)
    #     return lista_evenimente


# def test_lista_evenimente_ord_descr():
#     repo = Memory_rep_event()
#     val = EvenimentValidator()
#     test_srv = EvenimentService(repo, val)
#     repo_legatura = Memory_rep_legatura()
#     legatura = Entitate_legatura(1, 3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura = Entitate_legatura(1,1)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     id_persoana = 1
#     lista_legaturi = repo_legatura.get_lista_legaturi()
#     lista_event = test_srv.lista_evenimente_ord_descr(id_persoana, lista_legaturi)
#     assert lista_event[0].get_id()==3
#     assert lista_event[0].get_description()=='Botez'
#     assert lista_event[1].get_description()=='Nunta'
    #for el in lista_event:
        #print(el.get_id(), el.get_data(), el.get_description())


#test_lista_evenimente_ord_descr()
# def test_lista_evenimente_ordoanta_persoana():
#     repo=Memory_rep_event()
#     val=EvenimentValidator()
#     test_srv=EvenimentService(repo, val)
#     repo_legatura=Memory_rep_legatura()
#     legatura = Entitate_legatura(1, 3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura = Entitate_legatura(1, 1)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     id_persoana=1
#     lista_legaturi= repo_legatura.get_lista_legaturi()
#     lista_event= test_srv.lista_evenimente_ordonata_persoana(id_persoana, lista_legaturi)
#     assert len(lista_event)==2
#     assert lista_event[0].get_id()==1
#     assert lista_event[0].get_data()== date(2017,3,10)
#     assert lista_event[0].get_description()=='Nunta'
#
#     id_persoana=5
#     try:
#         lista_event=test_srv.lista_evenimente_ordonata_persoana(id_persoana, repo_legatura)
#         assert False
#     except ValueError as ve:
        #print(ve)
        #assert True
    #for el in lista_event:
        #print(el.get_id(), el.get_data(), el.get_description())

#test_lista_evenimente_ordoanta_persoana()


def test_adauga_ev_random():
    repo = Memory_rep_event()
    val = EvenimentValidator()
    test_srv = EvenimentService(repo, val)
    for i in range(5):
        test_srv.adauga_eveniment_random()
    #for ev in test_srv.get_lista_evenimente():
        #print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())

#test_adauga_ev_random()

def test_adauga_eveniment():
    repo = Memory_rep_event()
    val = EvenimentValidator()
    test_srv = EvenimentService(repo, val)

    added_ev = test_srv.adauga_eveniment(4, '13/08/2020', '14:50', 'Nunta')
    assert len(test_srv.get_lista_evenimente()) == 4

    try:
        added_ev2 = test_srv.adauga_eveniment(4, '15/09/20c2', '18:60', 'Botez')
        assert False
    #except ValueError as ve:
    except DuplicateIDException as ve:
        #print(ve)
        assert True
    except ValidationException as ve:
        #print(ve)
        assert True

    assert len(test_srv.get_lista_evenimente()) == 4


def test_modifica_eveniment():
    repo = Memory_rep_event()
    val = EvenimentValidator()
    test_srv = EvenimentService(repo, val)
    id_citit = 2
    for i, el in enumerate(test_srv.get_lista_evenimente()):
        if el.get_id() == id_citit:
            index = i
    test_srv.modifica_eveniment(id_citit, '12/5/2018', '14:20', 'Inmormantare')
    assert test_srv.get_lista_evenimente()[index].get_description() == 'Inmormantare'

    id_citit = 'b'
    try:
        test_srv.modifica_eveniment(id_citit, '13/3/2019', '16:40', 'Petrecere')
        assert False
    #except ValueError as ve:
    except ValidationException as ve:
        #print(ve)
        assert True

    id_citit = 4
    try:
        test_srv.modifica_eveniment(id_citit, '13/09/2020', '14:45', 'Concert')
        assert False
    #except ValueError as ve:
    except ValidationException as ve:
        #print(ve)
        assert True
    except EventNotFound as ve:
       #print(ve)
        assert True


def test_sterge_eveniment():
    repo = Memory_rep_event()
    val = EvenimentValidator()
    test_srv = EvenimentService(repo, val)
    id_citit = 3
    test_srv.sterge_eveniment_din_lista(id_citit)
    assert len(test_srv.get_lista_evenimente()) == 2

    id_citit = 3
    try:
        test_srv.sterge_eveniment_din_lista(id_citit)
        assert False
    #except ValueError as ve:
    except EventNotFound as ve:
        #print(ve)
        assert True


def test_cauta_dupa_descriere():
    repo = Memory_rep_event()
    val = EvenimentValidator()
    test_srv = EvenimentService(repo, val)
    test_srv.adauga_eveniment(4, '13/6/2021', '12:30', 'Botez')
    descriere = 'Botez'
    lista_noua = test_srv.cauta_dupa_descriere(descriere)
    assert len(lista_noua) == 2

test_adauga_eveniment()
test_modifica_eveniment()
test_sterge_eveniment()
test_cauta_dupa_descriere()
