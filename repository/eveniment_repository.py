from datetime import date

from domain.entities import Eveniment, Entitate_legatura
from repository.exeptions.exeptions import EventNotFound, DuplicateIDException, CorruptedFileException
from repository.legatura_repository import Memory_rep_legatura


class Memory_rep_event:
    def __init__(self):
        # se stocheaza evenimentele sub forma unei liste
        # adaugam niste evenimente predefinite
        self.__evenimente = [Eveniment(1, '10/03/2017', '13:30', 'Nunta'),
                             Eveniment(2, '24/02/2018', '17:45', 'Nunta'),
                             Eveniment(3, '13/09/2020', '20:00', 'Botez')]

    def exista_cu_id(self, id_citit):
        '''
        Verifica daca exista in lista de evenimente un eveniment cu id-ul egal cu cel citit de la tastatura
        :param id_citit: string ,id-ul citit de la tastatura
        :return: True daca se gaseste evenimentul, False altfrl
        :rtype: bool
        '''
        for eveniment in self.get_evenimente():
            if int(eveniment.get_id()) == int(id_citit):
                return True
        return False

    def __find_given_id(self, id_citit):
        '''
        Returneaza pozitia(indexul) evenimentului din lista care are id-ul egal cu cel citit de la tastatura
        :param id_citit: string, id-ul citit de la tastatura
        :return: index, int
        '''
        index = -1
        for i, ev in enumerate(self.get_evenimente()):
            if int(ev.get_id()) == int(id_citit):
                index = i
        return index

    def find_ev_id(self, id_eveniment):
        '''
        Returneaza evenimentul din lista ce are id-ul egal cu cel citit de la tastatura
        :param id_eveniment: string, id-ul evenimentului
        :return: eveniment, obiect al clasei eveniment
        '''
        lista_evenimente= self.get_evenimente()
        if self.exista_cu_id(id_eveniment)==False:
            #raise ValueError("Evenimentul cu id-ul dat nu exista in lista! ")
            raise EventNotFound()
        for ev in lista_evenimente:
            if int(ev.get_id())==int(id_eveniment):
                return ev



    def adauga_eveniment(self, eveniment):
        '''
        Adauag un eveniment in lista de evenimente
        :param eveniment: object, obiect al clasei eveniment
        :return: -
        '''
        if self.exista_cu_id(eveniment.get_id()):  # verifica daca exista evenimentul cu id-ul dat in lista
            #raise ValueError("Exista evenimentul cu id-ul dat in lista! ")
            raise DuplicateIDException()
        #data_list = eveniment.get_data().split("/")
        #eveniment.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
        self.__evenimente.append(eveniment)

    def get_evenimente(self):
        return self.__evenimente

    def modifica_eveniment(self, id_event, eveniment):
        '''
        Modifica evenimentul cu id-ul citit (id_event) cu eveniemntul citit (event)
        :param id_event: int, id-ul evenimentului de modificat
        :param eveniment: noul eveniment ce il va inlocui pe cel corespunzator
        :return: -
        '''
        index = self.__find_given_id(id_event)
        if index == -1:
            #raise ValueError("Nu exista eveniment cu id-ul dat! ")
            raise EventNotFound()
        #data_list = eveniment.get_data().split("/")
        #eveniment.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
        self.__evenimente[index] = eveniment

    def get_lungime_lista_evenimente(self):
        return len(self.__evenimente)

    def sterge_eveniment(self, id_citit):
        '''
        Sterge evenimentul din lista care are id-ul egal cu cel citit de la tasattura
        :param id_citit: string, id-ul evenimentului citit de la tastatura
        :return: -
        '''
        index = self.__find_given_id(id_citit)
        if index == -1:
            #raise ValueError("Nu exista eveniment cu id-ul dat! ")
            raise EventNotFound()
        self.__evenimente.pop(index)

    def filter_by_function(self, filter_criteria):
        '''
        Returneaza o noua lista de evenimente ce contine toate evenimentele ce respecta criteriile
        functiei filter_criteria
        :param filter_criteria: function, criteriul de cautare
        :return: filtered_list, lista de evenimente ce respecta cerinta
        '''
        filtered_list = []
        for event in self.get_evenimente():
            if filter_criteria(event) == True:
                filtered_list.append(event)
        return filtered_list

    def cmp_ev(self, ev1, ev2):
        '''
        Comparator pentru 2 evenimente
        :param ev1: primul eveniment
        :param ev2: al doilea eveniment
        :return:
        '''
        if ev1.get_data() == ev2.get_data():
            return ev1.get_description() < ev2.get_description()
        elif ev1.get_data() < ev2.get_data():
            return True
        else:
            return False
    def cmp_ev_2(self, ev1, ev2):
        '''
        Comparator pentru 2 evenimente
        :param ev1: primul eveniment
        :param ev2: al doilea eveniment
        :return:
        '''
        if ev1.get_description()==ev2.get_description():
            return ev1.get_data()< ev2.get_data()
        if ev1.get_description()< ev2.get_description():
            return True
        else: return False

    def insertion_sorted(self, lista, key=None, cmp=None, reverse=False):
        '''
        Sorteaza o lista dupa cheia key si in funcitie de parametrul reverse
        :param lista: list, lista de elemente
        :param key: lambda function, cheia dupa care se sorteaza
        :param reverse: False daca se doreste crescator(implicit), True daca se doreste crescator
        :return: sorted_list, lista sortata
        '''
        for i in range(1, len(lista)):
            x = lista[i]  # elementul de pe pozitia curenta
            j = i - 1  # elementul de pe pozitia precedenta
            if reverse == False:
                #while j >= 0 and key(lista[j]) > key(x):  # muta toate elementele precedente mai mari decat x
                while j >= 0 and cmp(lista[j],x) == False:
                    lista[j + 1] = lista[j]
                    j -= 1
                lista[j + 1] = x  # il muta pe x pe pozitia specifica
            else:
                #while j >= 0 and key(lista[j]) < key(x):
                while j >= 0 and cmp(lista[j], x)==True:
                    lista[j + 1] = lista[j]
                    j -= 1
                lista[j + 1] = x
        return lista

    def comb_sorted(self, lista, key=None, cmp=None, reverse=False):
        '''
        Sorteaza o lista utilizand comb sort
        :param lista: list, lista de evenimente
        :param key: lambda function, cheia dupa care se face comparatia
        :param reverse: parametru tip bool, False daca dorim sortare crescatoare dupa cheie, False pentru descrescatoare
        :return: sorted_list, lista sortata
        '''
        ok = False  # verificam daca lista este sortata
        dif = len(
            lista)  # verificam entitati din lista adiacente situate la distanta dif (se compara lista[i] cu lista [i+dif] la fiecare pas)
        n = len(lista)  # lungimea listei
        while ok == False or dif != 1:
            ok = True  # presupunem ca lista e sortata
            dif = (dif * 10) // 13
            #print(dif)
            if dif < 1: dif = 1  # micsorarea diferentei poate fi cel putin 1, nu 0! (nu ar avea sens)
            for i in range(0, n - dif):
                if reverse == False:
                    #if key(lista[i]) > key(lista[i + dif]):
                    if cmp(lista[i],lista[i + dif])==False:
                        lista[i], lista[i + dif] = lista[i + dif], lista[i]  # interschimba folosind tuple packing
                        ok = False
                else:
                    #if key(lista[i]) < key(lista[i + dif]):
                    if cmp(lista[i],lista[i + dif])==True:
                        lista[i], lista[i + dif] = lista[i + dif], lista[i]  # interschimba folosind tuple packing
                        ok = False
        return lista

    def delete_all(self):
        self.__evenimente=[]



def test_insertion_sort():
    repo = Memory_rep_event()
    ev1 = Eveniment('7', '14/09/2020', '16:40', 'Party')
    ev2 = Eveniment('9', '15/08/2020', '16:40', 'Majorat')
    ev3 = Eveniment('5', '17/01/2019', '16:40', 'Botez')
    ev4 = Eveniment('6', '14/09/2018', '16:40', 'Party')

    repo.adauga_eveniment(ev1)
    repo.adauga_eveniment(ev2)
    repo.adauga_eveniment(ev3)
    repo.adauga_eveniment(ev4)

    lista_ev= repo.get_evenimente()
    for ev in lista_ev:
        data_list= ev.get_data().split("/")
        zi= int(data_list[0])
        luna= int(data_list[1])
        an=int(data_list[2])
        ev.set_date(date(an,luna,zi))
    lista_ev=repo.insertion_sorted(lista_ev, key= None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=False)
    assert lista_ev[0].get_data()==date(2017, 3,10)
    assert lista_ev[1].get_data()==date(2018, 2, 24)
    assert lista_ev[2].get_data()==date(2018, 9, 14)
    assert lista_ev[6].get_data()==date(2020,9,14)

    lista_ev = repo.insertion_sorted(lista_ev, key=None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=True)
    #for e in lista_ev:
        #print(e.get_id(), e.get_data(), e.get_description())
    assert lista_ev[6].get_data() == date(2017, 3, 10)
    assert lista_ev[2].get_data() == date(2020, 8, 15)
    assert lista_ev[1].get_data() == date(2020, 9, 13)
    assert lista_ev[0].get_data() == date(2020, 9, 14)

    #for e in lista_ev:
        #print(e.get_id(), e.get_data(), e.get_time(), e.get_description())

test_insertion_sort()


def test_comb_sort():
    repo = Memory_rep_event()
    ev1 = Eveniment('7', '14/09/2020', '16:40', 'Party')
    ev2 = Eveniment('9', '15/08/2020', '16:40', 'Majorat')
    ev3 = Eveniment('5', '17/01/2019', '16:40', 'Botez')
    ev4 = Eveniment('6', '14/09/2018', '16:40', 'Party')

    repo.adauga_eveniment(ev1)
    repo.adauga_eveniment(ev2)
    repo.adauga_eveniment(ev3)
    repo.adauga_eveniment(ev4)

    lista_ev= repo.get_evenimente()
    for ev in lista_ev:
        data_list= ev.get_data().split("/")
        zi= int(data_list[0])
        luna= int(data_list[1])
        an=int(data_list[2])
        ev.set_date(date(an,luna,zi))
    lista_ev=repo.comb_sorted(lista_ev, key= None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=False)
    assert lista_ev[0].get_data()==date(2017, 3,10)
    assert lista_ev[1].get_data()==date(2018, 2, 24)
    assert lista_ev[2].get_data()==date(2018, 9, 14)
    assert lista_ev[6].get_data()==date(2020,9,14)

    lista_ev = repo.comb_sorted(lista_ev, key=None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=True)
    assert lista_ev[6].get_data() == date(2017, 3, 10)
    assert lista_ev[2].get_data() == date(2020, 8, 15)
    assert lista_ev[1].get_data() == date(2020, 9, 13)
    assert lista_ev[0].get_data() == date(2020, 9, 14)
test_comb_sort()


    # def lista_id_evenimente_persoana(self, id_persoana, lista_legaturi):
    #     '''
    #     Returneaza lista cu id-ul evenimentelor la care participa o persoana
    #     :param id_persoana: string, id-ul persoanei citite de la tastatura
    #     :return: lista_evenimente, list, lista de evenimente
    #     '''
    #     lista_evenimente = []
    #     # repo_legatura = Memory_rep_legatura()
    #     for el in lista_legaturi:
    #         if int(el.get_id_persoana()) == int(id_persoana):
    #             lista_evenimente.append(el.get_id_eveniment())
    #     return lista_evenimente
    #
    # def transforma_in_lista_evenimente(self, id_persoana, lista_legaturi):
    #     '''
    #     Transforma lista de id-uri de evenimente in lista de evenimente
    #     :param lista_id_evenimente: list, lista de id-uri
    #     :return: lista_evenimente, lista de evenimente
    #     '''
    #     lista_initiala = self.get_evenimente()
    #     lista_id = self.lista_id_evenimente_persoana(id_persoana, lista_legaturi)
    #     lista_evenimente = []
    #     for ev in lista_id:
    #         for i, ev2 in enumerate(lista_initiala):
    #             if int(ev2.get_id()) == int(ev):
    #                 lista_evenimente.append(lista_initiala[i])
    #     return lista_evenimente

    # def ordonare_dupa_data(self, lista_evenimente):
    #     '''
    #     Ordoneaza o lista de evenimente dupa data evenimentelor
    #     :param lista_evenimente:
    #     :return:
    #     '''
        # for eveniment in lista_evenimente:
        # data_eveniment = eveniment.get_data()
        # lista_date = data_eveniment.split("/")
        # data_creata = date(int(lista_date[2]), int(lista_date[1]), int(lista_date[0]))
        # eveniment.set_date(data_creata)
        # for i in range(len(lista_evenimente) - 1):
        #     for j in range(i + 1, len(lista_evenimente)):
        #         data1 = lista_evenimente[i].get_data()
        #         data2 = lista_evenimente[j].get_data()
        #         if data1 > data2:
        #             aux = lista_evenimente[i]
        #             lista_evenimente[i] = lista_evenimente[j]
        #             lista_evenimente[j] = aux

    # def ordonare_dupa_descriere(self, lista_evenimente):
    #     '''
    #     Ordoneaza o lista de evenimente in ordine alfabetica a descrierii
    #     :param lista_evenimente: list, lista de evenimente
    #     :return: -
    #     '''
    #     for i in range(len(lista_evenimente) - 1):
    #         for j in range(i + 1, len(lista_evenimente)):
    #             desc1 = lista_evenimente[i].get_description()
    #             desc2 = lista_evenimente[j].get_description()
    #             if desc1 > desc2:
    #                 aux = lista_evenimente[i]
    #                 lista_evenimente[i] = lista_evenimente[j]
    #                 lista_evenimente[j] = aux

    # def return_lista_evenimente_persoana(self, id_persoana, lista_legaturi):
    #     '''
    #     Returneaza lista de evenimente la care participa persoana cu id-ul dat ordonata crescator dupa data
    #     :param id_persoana: string, id-ul persoanei citit de al tastatura
    #     :return: lista_evenimente, list, lista ce contine evenimentele corespunzatoare
    #     '''
    #     # repo_legatura = Memory_rep_legatura()
    #     if self.exista_cu_id(id_persoana) == False:
    #         raise ValueError("Nu exista persoana cu id-ul dat!")
    #     lista_evenimente = self.transforma_in_lista_evenimente(id_persoana, lista_legaturi)
        # for eveniment in lista_evenimente:
        # if type(eveniment.get_data()) == 'str':
        # data_list = eveniment.get_data().split("/")
        # eveniment.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
        # self.ordonare_dupa_data(lista_evenimente)
        # return lista_evenimente

    # def return_lista_ord_descr(self, id_persoana, lista_legaturi):
    #     if self.exista_cu_id(id_persoana) == False:
    #         raise ValueError("Nu exista persoana cu id-ul dat!")
    #     lista_evenimente = self.transforma_in_lista_evenimente(id_persoana, lista_legaturi)
    #     self.ordonare_dupa_descriere(lista_evenimente)
    #     return lista_evenimente




def test_find_ev_given_id():
    repo=Memory_rep_event()
    id_eveniment=2
    eveniment= repo.find_ev_id(id_eveniment)
    assert eveniment.get_description()=='Nunta'

    try:
        eveniment=repo.find_ev_id('4')
        assert False
    #except ValueError as ve:
    except EventNotFound as ve:
        #print(ve)
        assert True


test_find_ev_given_id()





# def test_return_evenimnete_ord_descr():
#     repo = Memory_rep_event()
#     id_persoana = 1
#     repo_legatura = Memory_rep_legatura()
#     legatura= Entitate_legatura(1,3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura=Entitate_legatura(1,1)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     lista_legaturi = repo_legatura.get_lista_legaturi()
#     lista = repo.return_lista_ord_descr(id_persoana, lista_legaturi)
#     assert lista[0].get_id()==3
#     assert lista[0].get_description()=='Botez'
    #for el in lista:
        #print(el.get_id(), el.get_data(), el.get_description())

#test_return_evenimnete_ord_descr()


# def test_return_lista_evenimente_persoana():
#     repo = Memory_rep_event()
#     id_persoana = 1
#     repo_legatura = Memory_rep_legatura()
#     legatura= Entitate_legatura(1,3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura= Entitate_legatura(1,1)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     lista_legaturi = repo_legatura.get_lista_legaturi()
#     lista = repo.return_lista_evenimente_persoana(id_persoana, lista_legaturi)
#     # for el in lista:
#     # print(el.get_id(), el.get_data(), el.get_description())
#     assert len(lista) == 2
#     assert lista[0].get_id() == 1
#     assert lista[0].get_data() == date(2017, 3, 10)
#     # print(type(lista[0].get_data()))
#
#     id_persoana = 5
#     try:
#         lista = repo.return_lista_evenimente_persoana(id_persoana, lista_legaturi)
#         assert False
#     except ValueError as ve:
#         # print(ve)
#         assert True
    # for el in lista:
    # print(el.get_id(), el.get_data(), el.get_description())


#test_return_lista_evenimente_persoana()


def test_adauga_eveniment():
    repo = Memory_rep_event()
    event = Eveniment(4, '2/01/2021', '17:00', 'Aniversare')
    repo.adauga_eveniment(event)
    assert len(repo.get_evenimente()) == 4
    event = Eveniment(4, '2/01/2021', '17:00', 'Aniversare')
    try:
        repo.adauga_eveniment(event)
        assert False
    #except ValueError as ve:
    except DuplicateIDException as ve:
        #print(ve)
        assert True


def test_modifica_eveniment():
    repo = Memory_rep_event()
    eveniment = Eveniment(2, '13/8/2019', '19:00', 'Banchet')
    id_event_de_modificat = 2
    for i, el in enumerate(repo.get_evenimente()):
        if el.get_id() == id_event_de_modificat:
            index = i
    repo.modifica_eveniment(id_event_de_modificat, eveniment)
    # for el in repo.get_evenimente():
    # print(el.get_id(), el.get_description())
    assert repo.get_evenimente()[index].get_description() == 'Banchet'

    id_nou = 4
    try:
        repo.modifica_eveniment(id_nou, eveniment)
        assert False
    #except ValueError as ve:
    except EventNotFound as ve:
        #print(ve)
        assert True


def test_sterge_eveniment():
    repo = Memory_rep_event()
    id_citit = 2
    repo.sterge_eveniment(id_citit)
    assert len(repo.get_evenimente()) == 2

    id_citit = 2
    try:
        repo.sterge_eveniment(id_citit)
        assert False
    #except ValueError as ve:
    except EventNotFound as ve:
        #print(ve)
        assert True


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


def setup_repo():
    ev1 = Eveniment('4', '13/09/2021', '14:30', 'Concert')
    ev2 = Eveniment('5', '14/09/2021', '14:30', 'Concert')
    ev3 = Eveniment('6', '13/09/2021', '14:30', 'Botez')

    test_repo = Memory_rep_event()
    test_repo.adauga_eveniment(ev1)
    test_repo.adauga_eveniment(ev2)
    test_repo.adauga_eveniment(ev3)

    return test_repo


def test_filter_by_criteria():
    test_repo = setup_repo()
    filter_by_description = lambda x: x.get_description() == 'Concert'
    filtered_by_description = test_repo.filter_by_function(filter_by_description)
    assert len(filtered_by_description) == 2

    filter_by_date = lambda x: x.get_data() == '13/09/2021'
    filtered_by_date = test_repo.filter_by_function(filter_by_date)
    assert len(filtered_by_date) == 2


# def test_lista_id_evenimente_persoana():
#     repo = Memory_rep_event()
#     repo_legatura = Memory_rep_legatura()
#     legatura = Entitate_legatura(1, 3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura = Entitate_legatura(1, 1)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura = Entitate_legatura(2, 3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     id_persoana = 1
#     lista_legaturi = repo_legatura.get_lista_legaturi()
#     lista = repo.lista_id_evenimente_persoana(id_persoana, lista_legaturi)
#     assert len(lista) == 2


# def test_transforma_in_eveniment():
#     repo = Memory_rep_event()
#     repo_legatura = Memory_rep_legatura()
#     legatura= Entitate_legatura(1,3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura = Entitate_legatura(1, 1)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     legatura = Entitate_legatura(2, 3)
#     repo_legatura.adauga_persoana_la_eveniment(legatura)
#     lista_legaturi = repo_legatura.get_lista_legaturi()
#     id_persoana = 1
#     # lista = repo.lista_id_evenimente_persoana(id_persoana, repo_legatura)
#     lista_noua = repo.transforma_in_lista_evenimente(id_persoana, lista_legaturi)
#     assert len(lista_noua) == 2
#     assert lista_noua[0].get_id() == 3
#     assert lista_noua[0].get_description() == 'Botez'
#     assert lista_noua[1].get_description() == 'Nunta'
    # for el in lista_noua:
    # print(el.get_id(), el.get_description())


# def test_ordonare_dupa_data():
#     repo = Memory_rep_event()
#     lista_evenimente = [Eveniment(1, '13/09/2021', '14:30', 'Botez'),
#                         Eveniment(4, '14/09/2020', '14:30', 'Nunta'),
#                         Eveniment(3, '12/11/2020', '14:30', 'Concert')
#                         ]
#     for eveniment in lista_evenimente:
#         data_list = eveniment.get_data().split("/")
#         eveniment.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
#     repo.ordonare_dupa_data(lista_evenimente)
    # for el in lista_evenimente:
    # print(el.get_id(), el.get_description(), el.get_data())
    #assert lista_evenimente[0].get_id() == 4
    # for el in lista_evenimente:
    # print(el.get_id(), el.get_data())


def test_ordonare_dupa_descr():
    repo = Memory_rep_event()
    lista_evenimente = [Eveniment(1, '13/09/2021', '14:30', 'Botez'),
                        Eveniment(4, '14/09/2020', '14:30', 'Nunta'),
                        Eveniment(3, '12/11/2020', '14:30', 'Concert')
                        ]
    repo.ordonare_dupa_descriere(lista_evenimente)
    assert lista_evenimente[0].get_id() == 1
    assert lista_evenimente[0].get_description() == 'Botez'
    assert lista_evenimente[2].get_description() == 'Nunta'
    # for el in lista_evenimente:
    # print(el.get_id(), el.get_description(), el.get_data())


#test_ordonare_dupa_descr()
#test_ordonare_dupa_data()
#test_transforma_in_eveniment()
#test_lista_id_evenimente_persoana()

test_adauga_eveniment()
test_modifica_eveniment()
test_sterge_eveniment()
test_filter_by_criteria()



class Event_file_repo:
    def __init__(self, filename):
        self.__filename = filename

    def __load_from_file(self):
        '''
        Incarca datele din fisier
        :return: person_list,list, lista de persoane
        '''
        try:
            f=open(self.__filename, 'r')
        except IOError:
            raise CorruptedFileException()

        lista_evenimente = []
        lines = f.readlines()
        for line in lines:
            ev_id, data, timp, descriere = [token.strip() for token in line.split(';')]
            #data_list = data.split("/")
            p = Eveniment(ev_id, data, timp, descriere)
            #p.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
            lista_evenimente.append(p)
        f.close()
        return lista_evenimente

    def __save_to_file(self, lista_evenimente):
        '''
        Salveaza pesoanele din lista in fisier
        :param lista_persoane: list, lista de persoane
        :return: -
        '''
        with open(self.__filename, 'w') as f:
            for eveniment in lista_evenimente:
                ev_string = str(eveniment.get_id()) + ';' + str(eveniment.get_data()) + ';' + str(
                    eveniment.get_time()) + ';' + str(eveniment.get_description())+'\n'
                f.write(ev_string)

    def get_evenimente(self):
        return self.__load_from_file()

    def exista_cu_id(self, id_citit):
        '''
        Verifica daca exista in lista de evenimente un eveniment cu id-ul egal cu cel citit de la tastatura
        :param id_citit: string ,id-ul citit de la tastatura
        :return: True daca se gaseste evenimentul, False altfrl
        :rtype: bool
        '''
        for eveniment in self.get_evenimente():
            if int(eveniment.get_id()) == int(id_citit):
                return True
        return False

    def __find_given_id(self, id_citit):
        '''
        Returneaza pozitia(indexul) evenimentului din lista care are id-ul egal cu cel citit de la tastatura
        :param id_citit: string, id-ul citit de la tastatura
        :return: index, int
        '''
        index = -1
        for i, ev in enumerate(self.get_evenimente()):
            if int(ev.get_id()) == int(id_citit):
                index = i
        return index

    def find_ev_id(self, id_eveniment):
        '''
        Returneaza evenimentul din lista ce are id-ul egal cu cel citit de la tastatura
        :param id_eveniment: string, id-ul evenimentului
        :return: eveniment, obiect al clasei eveniment
        '''
        lista_evenimente= self.get_evenimente()
        if self.exista_cu_id(id_eveniment)==False:
            #raise ValueError("Evenimentul cu id-ul dat nu exista in lista! ")
            raise EventNotFound()
        for ev in lista_evenimente:
            if int(ev.get_id())==int(id_eveniment):
                return ev

    def adauga_eveniment(self, eveniment):
        '''
        Adauag un eveniment in lista de evenimente
        :param eveniment: object, obiect al clasei eveniment
        :return: -
        '''
        if self.exista_cu_id(eveniment.get_id()):  # verifica daca exista evenimentul cu id-ul dat in lista
            #raise ValueError("Exista evenimentul cu id-ul dat in lista! ")
            raise DuplicateIDException()
        #data_list = eveniment.get_data().split("/")
        #eveniment.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
        lista_ev= self.get_evenimente()
        lista_ev.append(eveniment)
        self.__save_to_file(lista_ev)

    def modifica_eveniment(self, id_event, eveniment):
        '''
        Modifica evenimentul cu id-ul citit (id_event) cu eveniemntul citit (event)
        :param id_event: int, id-ul evenimentului de modificat
        :param eveniment: noul eveniment ce il va inlocui pe cel corespunzator
        :return: -
        '''
        index = self.__find_given_id(id_event)
        if index == -1:
            #raise ValueError("Nu exista eveniment cu id-ul dat! ")
            raise EventNotFound()
        #data_list = eveniment.get_data().split("/")
        #eveniment.set_date(date(int(data_list[2]), int(data_list[1]), int(data_list[0])))
        lista_ev= self.get_evenimente()
        lista_ev[index] = eveniment
        self.__save_to_file(lista_ev)

    def sterge_eveniment(self, id_citit):
        '''
        Sterge evenimentul din lista care are id-ul egal cu cel citit de la tasattura
        :param id_citit: string, id-ul evenimentului citit de la tastatura
        :return: -
        '''
        index = self.__find_given_id(id_citit)
        if index == -1:
            #raise ValueError("Nu exista eveniment cu id-ul dat! ")
            raise EventNotFound()
        lista_ev= self.get_evenimente()
        lista_ev.pop(index)
        self.__save_to_file(lista_ev)

    def filter_by_function(self, filter_criteria):
        '''
        Returneaza o noua lista de evenimente ce contine toate evenimentele ce respecta criteriile
        functiei filter_criteria
        :param filter_criteria: function, criteriul de cautare
        :return: filtered_list, lista de evenimente ce respecta cerinta
        '''
        filtered_list = []
        for event in self.get_evenimente():
            if filter_criteria(event) == True:
                filtered_list.append(event)
        return filtered_list

    def delete_all(self):
        lista_ev= []
        self.__save_to_file(lista_ev)

    def cmp_ev(self, ev1, ev2):
        '''
        Comparator pentru 2 evenimente
        :param ev1: primul eveniment
        :param ev2: al doilea eveniment
        :return:
        '''
        if ev1.get_data() == ev2.get_data():
            return ev1.get_description() < ev2.get_description()
        elif ev1.get_data() < ev2.get_data():
            return True
        else:
            return False

    def cmp_ev_2(self, ev1, ev2):
        '''
        Comparator pentru 2 evenimente
        :param ev1: primul eveniment
        :param ev2: al doilea eveniment
        :return:
        '''
        if ev1.get_description()== ev2.get_description():
            return ev1.get_data() < ev2.get_data()
        if ev1.get_description() < ev2.get_description():
            return True
        else: return False

    def insertion_sorted(self, lista, key=None, cmp=None, reverse=False):
        '''
        Sorteaza o lista dupa cheia key si in funcitie de parametrul reverse
        :param lista: list, lista de elemente
        :param key: lambda function, cheia dupa care se sorteaza
        :param reverse: False daca se doreste crescator(implicit), True daca se doreste crescator
        :return: sorted_list, lista sortata
        '''
        for i in range(1, len(lista)):
            x = lista[i]  # elementul de pe pozitia curenta
            j = i - 1  # elementul de pe pozitia precedenta
            if reverse == False:
                #while j >= 0 and key(lista[j]) > key(x):  # muta toate elementele precedente mai mari decat x
                while j >= 0 and cmp(lista[j], x) == False:
                    lista[j + 1] = lista[j]
                    j -= 1
                lista[j + 1] = x  # il muta pe x pe pozitia specifica
            else:
                #while j >= 0 and key(lista[j]) < key(x):
                while j >= 0 and cmp(lista[j],x) == True:
                    lista[j + 1] = lista[j]
                    j -= 1
                lista[j + 1] = x
        return lista

    def comb_sorted(self, lista, key=None, cmp=None, reverse=False):
        '''
        Sorteaza o lista utilizand comb sort
        :param lista: list, lista de evenimente
        :param key: lambda function, cheia dupa care se face comparatia
        :param reverse: parametru tip bool, False daca dorim sortare crescatoare dupa cheie, False pentru descrescatoare
        :return: sorted_list, lista sortata
        '''
        ok=False # verificam daca lista este sortata
        dif= len(lista)   #verificam entitati din lista adiacente situate la distanta dif (se compara lista[i] cu lista [i+dif] la fiecare pas)
        n=len(lista)      #lungimea listei
        while ok==False or dif != 1:
            ok=True   #presupunem ca lista e sortata
            dif= (dif*10)//13
            #print(dif)
            if dif<1: dif=1  #micsorarea diferentei poate fi cel putin 1, nu 0! (nu ar avea sens)
            for i in range(0, n-dif):
                if reverse==False:
                    #if key(lista[i]) > key(lista[i+dif]):
                    if cmp(lista[i],lista[i + dif])==False:
                        lista[i], lista[i+dif] = lista[i+dif], lista[i]  #interschimba folosind tuple packing
                        ok=False
                else:
                    #if key(lista[i]) < key(lista[i+dif]):
                    if cmp(lista[i],lista[i + dif])==True:
                        lista[i], lista[i+dif] = lista[i+dif], lista[i]  #interschimba folosind tuple packing
                        ok=False
        return lista




def test_insertion_sorted():
    repo=Event_file_repo('eveniment_test.txt')
    repo.delete_all()
    ev1 = Eveniment('7', '14/09/2020', '16:40', 'Party')
    ev2 = Eveniment('9', '15/08/2020', '16:40', 'Majorat')
    ev3 = Eveniment('5', '17/01/2019', '16:40', 'Botez')
    ev4 = Eveniment('6', '14/09/2018', '16:40', 'Party')
    repo.adauga_eveniment(ev1)
    repo.adauga_eveniment(ev2)
    repo.adauga_eveniment(ev3)
    repo.adauga_eveniment(ev4)

    lista_ev = repo.get_evenimente()
    for ev in lista_ev:
        data_list = ev.get_data().split("/")
        zi = int(data_list[0])
        luna = int(data_list[1])
        an = int(data_list[2])
        ev.set_date(date(an, luna, zi))
    lista_ev = repo.insertion_sorted(lista_ev, key=None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=False)
    assert lista_ev[0].get_data() == date(2018, 9, 14)
    assert lista_ev[1].get_data() == date(2019, 1, 17)
    assert lista_ev[2].get_data() == date(2020, 8, 15)
    assert lista_ev[3].get_data() == date(2020, 9, 14)

    lista_ev = repo.insertion_sorted(lista_ev, key=None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=True)
    assert lista_ev[3].get_data() == date(2018, 9, 14)
    assert lista_ev[2].get_data() == date(2019, 1, 17)
    assert lista_ev[1].get_data() == date(2020, 8, 15)
    assert lista_ev[0].get_data() == date(2020, 9, 14)


test_insertion_sorted()



def test_comb_sorted():
    repo = Event_file_repo('eveniment_test.txt')
    repo.delete_all()
    ev1 = Eveniment('7', '14/09/2020', '16:40', 'Party')
    ev2 = Eveniment('9', '15/08/2020', '16:40', 'Majorat')
    ev3 = Eveniment('5', '17/01/2019', '16:40', 'Botez')
    ev4 = Eveniment('6', '14/09/2018', '16:40', 'Party')
    repo.adauga_eveniment(ev1)
    repo.adauga_eveniment(ev2)
    repo.adauga_eveniment(ev3)
    repo.adauga_eveniment(ev4)

    lista_ev = repo.get_evenimente()
    for ev in lista_ev:
        data_list = ev.get_data().split("/")
        zi = int(data_list[0])
        luna = int(data_list[1])
        an = int(data_list[2])
        ev.set_date(date(an, luna, zi))
    lista_ev = repo.comb_sorted(lista_ev, key=None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=False)
    assert lista_ev[0].get_data() == date(2018, 9, 14)
    assert lista_ev[1].get_data() == date(2019, 1, 17)
    assert lista_ev[2].get_data() == date(2020, 8, 15)
    assert lista_ev[3].get_data() == date(2020, 9, 14)

    lista_ev = repo.comb_sorted(lista_ev, key=None, cmp= lambda x,y: repo.cmp_ev(x,y), reverse=True)
    assert lista_ev[3].get_data() == date(2018, 9, 14)
    assert lista_ev[2].get_data() == date(2019, 1, 17)
    assert lista_ev[1].get_data() == date(2020, 8, 15)
    assert lista_ev[0].get_data() == date(2020, 9, 14)

test_comb_sorted()


def test_load_from_file():
    repo=Event_file_repo('eveniment_test.txt')
    lista_ev= repo.get_evenimente()
    for ev in lista_ev:
        print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())


def test_adauga_file():
    repo=Event_file_repo('eveniment_test.txt')
    e=Eveniment(8, '15/03/2021', '20:30', 'Botez')
    repo.adauga_eveniment(e)
    lista= repo.get_evenimente()
    for ev in lista:
        print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())

def test_modific_file():
    repo=Event_file_repo('eveniment_test.txt')
    id=8
    ev= Eveniment(id, '23/05/2021', '14:00', 'Inmormantare')
    repo.modifica_eveniment(id, ev)
    lista_ev= repo.get_evenimente()

    try:
        ev=Eveniment(9, '13/09/2021', '15:45', 'Concert')
        repo.modifica_eveniment(9, ev)
        assert False
    except EventNotFound as ve:
        #print(ve)
        assert True
    for ev  in lista_ev:
        print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())

def test_sterge_file():
    repo=Event_file_repo('eveniment_test.txt')
    id='7'
    repo.sterge_eveniment(id)
    lista= repo.get_evenimente()

    for ev in lista:
        print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())


def test_filter_file():
    repo=Event_file_repo('eveniment_test.txt')
    filter_criteria= lambda x:x.get_description()=='Botez'
    lista= repo.filter_by_function(filter_criteria)
    for ev in lista:
        print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())

#test_load_from_file()
#test_adauga_file()
#test_modific_file()
#test_sterge_file()
#test_filter_file()
