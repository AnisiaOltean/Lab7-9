from datetime import date

from domain.dtos import EvenimentParticipanti, EvenimentIDParticipanti
from domain.entities import Entitate_legatura, Eveniment
from repository.eveniment_repository import Memory_rep_event
from repository.exeptions.exeptions import PersonNotFound, EventNotFound, NotEnoughEvents, NotEnoughPers
from repository.legatura_repository import Memory_rep_legatura
from repository.persoana_repository import Memory_rep_pers
from domain.validators import LegaturaValidator


class LegaturaService:
    def __init__(self, repo, val, repo1, repo2):
        self.__repo = repo
        self.__val = val
        self.__repo1 = repo1
        self.__repo2 = repo2

    def get_lista_leg(self):
        return self.__repo.get_lista_legaturi()

    def get_legatura_repo(self):
        return self.__repo

    def delete_all(self):
        self.__repo.delete_all()

    # def exista_id(self, id_citit, lista):
    #     '''
    #     Verifica daca id-ul persoanei citit se afla in lista de persoane
    #     :param lista_persoane: list, lista de persoane
    #     :return: True, daca id-ul se gaseste, False altfel
    #     '''
    #     for element in lista:
    #         if int(id_citit) == int(element.get_id()):
    #             return True
    #     return False

    def adauga_pers_eveniment(self, id_persoana, id_eveniment):
        '''
        Adauga peroana cu id-ul dat la evenimentul cu id-ul dat
        :param persoana: object, persoana din lista de persoane
        :param eveniment: object, eveniment din lista de evenimente
        :return: -
        '''
        # lista_persoane = self.__repo1.get_persoane()
        # lista_evenimente = self.__repo2.get_evenimente()
        # if self.exista_id(id_persoana, lista_persoane) == False:
        # raise ValueError("Persoana cu id-ul dat nu exista in lista! ")
        # f self.exista_id(id_eveniment, lista_evenimente) == False:
        # raise ValueError("Evenimentul cu id-ul dat nu exista in lista! ")

        legatura = Entitate_legatura(id_persoana, id_eveniment)
        self.__val.validate(legatura)
        if self.__repo1.exists_with_id(id_persoana) == False:
            #raise ValueError("Persoana cu id-ul dat nu exista in lista! ")
            raise PersonNotFound()
        if self.__repo2.exista_cu_id(id_eveniment) == False:
            #raise ValueError("Evenimentul cu id-ul dat nu exista in lista! ")
            raise EventNotFound()
        self.__repo.adauga_persoana_la_eveniment(legatura)

    # def ordonare_data_lista(self, id_persoana):
    #     '''
    #     Pentru persoana cu id-ul dat se formeaza lista de evenimente la care participa
    #     :param id_persoana: string, id-ul persoanei citit
    #     :return: lista, lista ce contine evenimentele ordoante crescator dupa data
    #     '''
    # lista_pers = self.__repo1.get_persoane()
    # ok = 0
    # for pers in lista_pers:
    #     if int(pers.get_id()) == int(id_persoana):
    #         ok = 1
    # if ok == 0:
    # if self.__repo1.exists_with_id(id_persoana) == False:
    #     raise ValueError("Persoana cu id-ul citit nu exista in lista! ")
    # lista_legaturi = self.__repo.get_lista_legaturi()
    # lista = self.__repo2.return_lista_evenimente_persoana(id_persoana, lista_legaturi)
    # return lista

    def get_evenimente_persoana(self, id_persoana):
        '''
        Returneaza lista de evenimente la care participa o persoana cu id-ul dat
        :param id_persoana: string, id-ul persoanei citite de la tastatura
        :return: lista_ev, lista ce contine evenimentele corespunzatoare
        '''
        lista_leg = self.__repo.get_lista_legaturi()
        lista_ev = []
        if self.__repo1.exists_with_id(id_persoana) == False:
            #raise ValueError("Nu exista persoana cu id-ul dat! ")
            raise PersonNotFound()
        for leg in lista_leg:
            if int(leg.get_id_persoana()) == int(id_persoana):
                eveniment = self.__repo2.find_ev_id(int(leg.get_id_eveniment()))
                lista_ev.append(eveniment)
        return lista_ev

    def lista_ordonata_data(self, id_persoana):
        '''
        Returneaza lista de evenimente la care participa persoana cu id-ul dat ordonata dupa data
        :param id_persoana: string, id-ul persoanei citit de la tasattura
        :return: ordered_list, lista de evenimete ordonata
        '''
        if self.__repo1.exists_with_id(id_persoana) == False:
            #raise ValueError("Persoana cu id-ul citit nu exista in lista! ")
            raise PersonNotFound()
        lista_ev = self.get_evenimente_persoana(id_persoana)
        for ev in lista_ev:
            data_list = ev.get_data().split("/")
            data = date(int(data_list[2]), int(data_list[1]), int(data_list[0]))
            ev.set_date(data)
        #sorted_list = sorted(lista_ev, key=lambda a: a.get_data())
        sorted_list = self.__repo2.insertion_sorted(lista_ev, key=None, cmp= lambda x,y: self.__repo2.cmp_ev(x,y))
        return sorted_list

    def lista_ordonata_descriere(self, id_persoana):
        '''
        Returneaza lista de evenimente la care participa persoana cu id-ul dat ordonata dupa descriere
        :param id_persoana: string, id-ul persoanei
        :return: ordered_list, lista de evenimente ordonata dupa descriere
        '''
        if self.__repo1.exists_with_id(id_persoana) == False:
            #raise ValueError("Persoana cu id-ul citit nu exista in lista! ")
            raise PersonNotFound()
        #lista_ev = self.get_evenimente_persoana(id_persoana)
        lista_ev = self.get_evenimente_persoana(id_persoana)
        #sorted_list = sorted(lista_ev, key=lambda a: a.get_description())
        for ev in lista_ev:
            data_list = ev.get_data().split("/")
            data = date(int(data_list[2]), int(data_list[1]), int(data_list[0]))
            ev.set_date(data)
        sorted_list= self.__repo2.comb_sorted(lista_ev, key=None, cmp= lambda x,y: self.__repo2.cmp_ev_2(x,y), reverse=False)
        return sorted_list

    def get_nr_evenimente(self, id_persoana):
        '''
        Returneaza nr. de evenimente la care participa o persoana
        :param id_persoana: string, id-ul persoanei citit de la tastatura
        :return: nr_evenimente, int, nr de evenimente la care participa persoana cu id-ul dat
        '''
        lista_leg = self.get_lista_leg()
        nr_ev = 0
        for element in lista_leg:
            if int(element.get_id_persoana()) == int(id_persoana):
                nr_ev += 1
        return nr_ev

    def persoane_nr_maxim_de_evenimente(self):
        '''
        Returneaza lista formata din id-urile persoanelor care participa la un numar maxim de evenimente
        :return: lista_id, list, lista ce contine id-urile persoanelor
        '''
        lista_pers = self.__repo1.get_persoane()
        nr_max = 0
        lista_id = []
        for persoana in lista_pers:
            nr_ev = self.get_nr_evenimente(
                int(persoana.get_id()))  # calculez la cate evenimente participa fiecare persoana
            if nr_ev > nr_max:
                lista_id = []
                lista_id.append(persoana.get_id())
                nr_max = nr_ev
            elif nr_ev == nr_max:
                lista_id.append(persoana.get_id())
        return lista_id

    def return_lista_persoane_nr_maxim_de_evenimente(self):
        '''
        Returneaza lista formata din persoanele ce participa la un numar maxim de evenimente
        :return: lista_pers, lista de persoane ceruta
        '''
        lista_id = self.persoane_nr_maxim_de_evenimente()
        # lista_persoane = self.__repo1.get_persoane()
        lista_noua_pers = []
        # for id in lista_id:
        #     for persoana in lista_persoane:
        #         if int(id) == int(persoana.get_id()):
                    #lista_noua_pers.append(persoana)
        for id in lista_id:
            pers= self.__repo1.find_pers_id(id)
            lista_noua_pers.append(pers)
        return lista_noua_pers

    def get_nr_participanti(self, id_eveniment):
        '''
        Returneaza nr. de persoane ce participa la evenimentul cu id-ul dat
        :param id_eveniment: string, id-ul evenimentului
        :return: nr_participanti, int, numarul de participanti
        '''
        lista_leg = self.get_lista_leg()
        nr_pers = 0
        for element in lista_leg:
            if int(element.get_id_eveniment()) == int(id_eveniment):
                nr_pers += 1
        return nr_pers

    def get_nr_participanti_rec(self, lista_leg, id_eveniment):
        '''
        Returneaza nr. de persoane ce participa la evenimentul cu id-ul dat
        :param lista_leg: list, lista de legaturi
        :param id_eveniment: string, id-yl evenimentului
        :return: int, numarul de persoane care participa la evenimentul dat
        '''
        if lista_leg == []:
            return 0
        elif int(lista_leg[0].get_id_eveniment()) == int(id_eveniment):
            return 1 + self.get_nr_participanti_rec(lista_leg[1:], id_eveniment)
        else:
            return self.get_nr_participanti_rec(lista_leg[1:], id_eveniment)

    def get_descriere_nr_participanti(self):
        '''
        Returneaza lista ce contine descrierea evenimentelor si numarul de participanti
        Se foloseste un data transfer object, EvenimentParticipanti, format din descrierea evenimentului si nr de participanti
        :return: lista_dto, lista ce contine evenimentele cerute
        '''
        lista_leg = self.__repo.get_lista_legaturi()
        lista_ev = self.__repo2.get_evenimente()
        lista_dto = []
        for ev in lista_ev:
            #nr_participanti = self.get_nr_participanti(ev.get_id())
            nr_participanti= self.get_nr_participanti_rec(lista_leg, ev.get_id())
            dto = EvenimentParticipanti(ev.get_description(), nr_participanti)
            lista_dto.append(dto)
        return lista_dto

    def get_id_nr_participanti(self):
        '''
        Returneaza o lista fomata din id-ul evenimentelor si numarul de participanti
        Se foloseste EvenimentIDParticipanti, data transfer object
        :return: lista dto, lista ce contine id-urile si nr de participanti ale evenimentelor
        '''
        lista_leg = self.__repo.get_lista_legaturi()
        lista_ev = self.__repo2.get_evenimente()
        lista_dto = []
        for ev in lista_ev:
            nr_participanti = self.get_nr_participanti(ev.get_id())
            dto = EvenimentIDParticipanti(ev.get_id(), nr_participanti)
            lista_dto.append(dto)
        return lista_dto

    def evenimente_most_participanti(self):
        '''
        Returneaza primele 20% evenimente (prima cincime) cu cei mai multi participanti
        :return: lista_ordonata, lista ce contine descrierea si nr_participanti ordoanata descrescator dupa nr. de participanti
        '''
        lista_dto = self.get_descriere_nr_participanti()  # lista de dto pentru toate evenimentele din lista
        if len(lista_dto) < 5:
            #raise ValueError("Nu s-au inscris persoane la cel putin 5 evenimente! ")
            raise NotEnoughEvents()
        #lista_ordonata = sorted(lista_dto, key=lambda a: a.get_nr_participanti(), reverse=True)
        lista_ordonata = sorted(lista_dto, key=lambda a: a.get_nr_participanti(), reverse=True)
        procent_20 = len(lista_dto) // 5
        lista_ordonata = lista_ordonata[:procent_20]
        return lista_ordonata

    def top_3_evenimente(self):
        '''
        Returneaza primele 3 evenimente cu cei mai multi participanti
        :return: lista_ev, lista de evenimente
        '''
        lista_dto = self.get_id_nr_participanti()
        lista_ev = []
        if len(lista_dto) < 3:
            #raise ValueError("Nu s-au inscris peroane la 3 evenimente! ")
            raise NotEnoughPers()
        #lista_sortata = sorted(lista_dto, key = lambda a: a.get_nr_participanti(), reverse=True) #sorteaza lista de evenimente dupa nr. de participanti
        lista_sortata = sorted(lista_dto, key=lambda a: a.get_nr_participanti(), reverse=True)
        lista_sortata =lista_sortata[:3]
        for el in lista_sortata:
            eveniment = self.__repo2.find_ev_id(el.get_id())
            lista_ev.append(eveniment)
        return lista_ev


def setup_evenimente():
    ev1 = Eveniment('4', '13/09/2021', '14:30', 'Concert')
    ev2 = Eveniment('5', '14/09/2021', '14:30', 'Concert')
    ev3 = Eveniment('6', '13/09/2021', '14:30', 'Botez')
    ev4 = Eveniment('7', '13/09/2021', '14:30', 'Nunta')
    ev5 = Eveniment('8', '13/09/2021', '14:30', 'Botez')
    ev6 = Eveniment('9', '13/09/2021', '14:30', 'Botez')
    ev7 = Eveniment('10', '13/09/2021', '14:30', 'Aniversare')
    ev8 = Eveniment('11', '13/09/2021', '14:30', 'Revelion')
    ev9 = Eveniment('12', '13/09/2021', '14:30', 'Revelion')
    ev10 = Eveniment('13', '13/09/2021', '14:30', 'Petrecere')
    ev11 = Eveniment('14', '13/09/2021', '14:30', 'Petrecere')
    ev12 = Eveniment('15', '13/09/2021', '14:30', 'Botez')
    ev13 = Eveniment('16', '13/09/2021', '14:30', 'Botez')
    ev14 = Eveniment('17', '13/09/2021', '14:30', 'Inmormantare')
    ev15 = Eveniment('18', '13/09/2021', '14:30', 'Botez')
    ev16 = Eveniment('19', '13/09/2021', '14:30', 'Nunta')
    ev17 = Eveniment('20', '13/09/2021', '14:30', 'Botez')
    # ev3 = Eveniment('6', '13/09/2021', '14:30', 'Inmormantare')
    # ev3 = Eveniment('6', '13/09/2021', '14:30', 'Botez')
    # ev3 = Eveniment('6', '13/09/2021', '14:30', 'Botez')

    test_repo = Memory_rep_event()
    test_repo.adauga_eveniment(ev1)
    test_repo.adauga_eveniment(ev2)
    test_repo.adauga_eveniment(ev3)
    test_repo.adauga_eveniment(ev4)
    test_repo.adauga_eveniment(ev5)
    test_repo.adauga_eveniment(ev6)
    test_repo.adauga_eveniment(ev7)
    test_repo.adauga_eveniment(ev8)
    test_repo.adauga_eveniment(ev9)
    test_repo.adauga_eveniment(ev10)
    test_repo.adauga_eveniment(ev11)
    test_repo.adauga_eveniment(ev12)
    test_repo.adauga_eveniment(ev13)
    test_repo.adauga_eveniment(ev14)
    test_repo.adauga_eveniment(ev15)
    test_repo.adauga_eveniment(ev16)
    test_repo.adauga_eveniment(ev17)

    return test_repo


def test_top_3_evenimente():
    repo1 = Memory_rep_pers()
    repo2 = setup_evenimente()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 5)
    #test_srv.adauga_pers_eveniment(1, 6)
    test_srv.adauga_pers_eveniment(2, 3)
    test_srv.adauga_pers_eveniment(2, 4)
    test_srv.adauga_pers_eveniment(3, 3)
    test_srv.adauga_pers_eveniment(1, 4)
    lista_ev= test_srv.top_3_evenimente()
    #for ev in lista_ev:
        #print(ev.get_id(), ev.get_data())
    assert lista_ev[0].get_id()==3
    assert lista_ev[1].get_id()=='4'
    assert lista_ev[2].get_id()=='5'
    #for ev in lista_ev:
       # print(ev.get_id(), ev.get_data(), ev.get_description())

test_top_3_evenimente()



def test_evenimente_most_participanti():
    repo1 = Memory_rep_pers()
    repo2 = setup_evenimente()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 5)
    test_srv.adauga_pers_eveniment(1, 6)
    test_srv.adauga_pers_eveniment(2, 3)
    test_srv.adauga_pers_eveniment(2, 4)
    test_srv.adauga_pers_eveniment(3, 17)
    test_srv.adauga_pers_eveniment(2, 1)
    test_srv.adauga_pers_eveniment(2, 8)
    test_srv.adauga_pers_eveniment(2, 13)
    test_srv.adauga_pers_eveniment(1, 1)
    lista_dto = test_srv.evenimente_most_participanti()
    assert len(lista_dto) == 4
    #for el in lista_dto:
        #print(el.get_descriere(), el.get_nr_participanti())


test_evenimente_most_participanti()


def test_get_descriere_nr_participanti():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(2, 3)
    lista = test_srv.get_descriere_nr_participanti()
    assert lista[2].get_descriere() == 'Botez'
    assert lista[2].get_nr_participanti() == 2
    # for element in lista:
    # print(element.get_descriere(), element.get_nr_participanti())


test_get_descriere_nr_participanti()


def test_get_nr_participanti():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(2, 3)
    nr_1 = test_srv.get_nr_participanti('3')
    assert nr_1 == 2


def test_get_nr_participanti_rec():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(2, 3)
    lista_leg= test_srv.get_lista_leg()
    nr_1 = test_srv.get_nr_participanti_rec(lista_leg, '3')
    assert nr_1 == 2

    nr_2 = test_srv.get_nr_participanti_rec(lista_leg, '2')
    assert nr_2 == 0


def test_lista_ordoanata():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 2)
    lista_ordonata = test_srv.lista_ordonata_data(1)
    assert len(lista_ordonata) == 2
    assert lista_ordonata[0].get_id() == 2
    assert lista_ordonata[0].get_data() == date(2018, 2, 24)
    assert lista_ordonata[1].get_data() == date(2020, 9, 13)
    # for el in lista_ordonata:
    #     print(el.get_id(), el.get_data(), el.get_description())


test_lista_ordoanata()


def test_lista_ordonata_descriere():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 2)
    lista_ordonata = test_srv.lista_ordonata_descriere(1)
    assert lista_ordonata[0].get_description() == 'Botez'
    assert lista_ordonata[1].get_description() == 'Nunta'
    # for ev in lista_ordonata:
    # print(ev.get_id(), ev.get_data(), ev.get_description())


test_lista_ordonata_descriere()


def test_get_evenimente_persoana():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 2)
    lista_ev = test_srv.get_evenimente_persoana(1)
    assert len(lista_ev) == 2
    lista_ev = test_srv.get_evenimente_persoana(2)
    assert len(lista_ev) == 0


test_get_evenimente_persoana()


def test_return_lista_persoane_nr_maxim_de_evenimente():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 2)
    test_srv.adauga_pers_eveniment(2, 2)
    test_srv.adauga_pers_eveniment(2, 1)
    lista_persoane = test_srv.return_lista_persoane_nr_maxim_de_evenimente()
    assert len(lista_persoane) == 2


test_return_lista_persoane_nr_maxim_de_evenimente()


def test_persoane_nr_maxim_de_evenimente():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 2)
    test_srv.adauga_pers_eveniment(2, 2)
    test_srv.adauga_pers_eveniment(2, 1)
    lista_id = test_srv.persoane_nr_maxim_de_evenimente()
    assert len(lista_id) == 2
    test_srv.adauga_pers_eveniment(2, 3)
    lista_id = test_srv.persoane_nr_maxim_de_evenimente()
    assert len(lista_id) == 1
    # for id in lista_id:
    # print(id, test_srv.get_nr_evenimente(id))


test_persoane_nr_maxim_de_evenimente()


def test_get_nr_evenimente_pers():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)
    test_srv.adauga_pers_eveniment(1, 2)
    test_srv.adauga_pers_eveniment(2, 2)
    nr_ev1 = test_srv.get_nr_evenimente(1)
    assert nr_ev1 == 2
    nr_ev2 = test_srv.get_nr_evenimente(2)
    assert nr_ev2 == 1


test_get_nr_evenimente_pers()


# def test_ordonare_data_lista():
#     repo1 = Memory_rep_pers()
#     repo2 = Memory_rep_event()
#     repo = Memory_rep_legatura()
#     val = LegaturaValidator()
#     test_srv = LegaturaService(repo, val, repo1, repo2)
#     test_srv.adauga_pers_eveniment(1, 3)
#     test_srv.adauga_pers_eveniment(1, 2)
#     id_persoana = 1
#     lista_return = test_srv.ordonare_data_lista(id_persoana)
#     # for el in lista_return:
#     # print(el.get_id(), el.get_data(), el.get_description())
#
#     id_persoana = 5
#     try:
#         lista_return = test_srv.ordonare_data_lista(id_persoana)
#         assert False
#     except ValueError as ve:
#         print(ve)
#         assert True


# test_ordonare_data_lista()

# def test_exista_id():
#     repo1 = Memory_rep_pers()
#     repo2 = Memory_rep_event()
#     repo = Memory_rep_legatura()
#     test_srv = LegaturaService(repo, repo1, repo2)
#     id_citit = 3
#     lista_persoane = repo1.get_persoane()
#     assert test_srv.exista_id(id_citit, lista_persoane) == True
#
#     id_citit = 4
#     assert test_srv.exista_id(id_citit, lista_persoane) == False
#
#     lista_evenimente = repo2.get_evenimente()
#     id_citit = 5
#     assert test_srv.exista_id(id_citit, lista_evenimente) == False


def test_adaug_pers_eveniment():
    repo1 = Memory_rep_pers()
    repo2 = Memory_rep_event()
    repo = Memory_rep_legatura()
    val = LegaturaValidator()
    test_srv = LegaturaService(repo, val, repo1, repo2)
    test_srv.adauga_pers_eveniment(1, 3)

    try:
        test_srv.adauga_pers_eveniment(1, 4)
        # test_srv.adauga_pers_eveniment(1, 4)
        assert False
    #except ValueError as ve:
    except EventNotFound as ve:
        #print(ve)
        assert True


test_adaug_pers_eveniment()
# test_exista_id()
