from datetime import date

from domain.entities import Entitate_legatura, Persoana, Eveniment


# from repository.eveniment_repository import Memory_rep_event
# from repository.persoana_repository import Memory_rep_pers
from repository.exeptions.exeptions import Legatura_creeata, CorruptedFileException


class Memory_rep_legatura:
    def __init__(self):
        self.__lista_legaturi = []
        # self.__repo1 = repo1
        # self.__repo2 = repo2

    def get_lista_legaturi(self):
        return self.__lista_legaturi

    # def ordonare_dupa_data(self, lista_evenimente):
    #     '''
    #     Ordoneaza o lista de evenimente dupa data evenimentelor
    #     :param lista_evenimente:
    #     :return:
    #     '''
    #     for eveniment in lista_evenimente:
    #         data_eveniment = eveniment.get_data()
    #         lista_date = data_eveniment.split("/")
    #         data_creata = date(int(lista_date[2]), int(lista_date[1]), int(lista_date[0]))
    #         eveniment.set_date(data_creata)
    #     for i in range(len(lista_evenimente) - 1):
    #         for j in range(i + 1, len(lista_evenimente)):
    #             if lista_evenimente[i].get_data() > lista_evenimente[j].get_data():
    #                 aux = lista_evenimente[i]
    #                 lista_evenimente[i] = lista_evenimente[j]
    #                 lista_evenimente[j] = aux

    # def exista_id(self, id_citit, lista):
    #     '''
    #     #Verifica daca id-ul persoanei citit se afla in lista de persoane
    #     #:param lista_persoane: list, lista de persoane
    #     #:return: True, daca id-ul se gaseste, False altfel
    #     '''
    #     for element in lista:
    #         if int(id_citit) == int(element.get_id()):
    #             return True
    #     return False

    def __exista_in_lista(self, id_persoana, id_eveniment):
        '''
        Verifica daca exista in lista de legaturi legatura cu acelasi id_persoana si id_eveniment
        :param id_persoana: string, id-ul persoanei
        :param id_eveniment: string, id-ul evenimentului
        :return: True, daca se gaseste o legatura duplicata, False altfel
        '''
        for leg in self.get_lista_legaturi():
            if (int(leg.get_id_persoana()) == int(id_persoana)) and (int(leg.get_id_eveniment()) == int(id_eveniment)):
                return True
        return False

    def adauga_persoana_la_eveniment(self, legatura):
        '''
        Face legatura dintre persoana si eveniment
        :param id_persoana:
        :param id_eveniment:
        :return:-
        :raises: ValueError daca se gasesc erori de validare
        '''
        # lista_persoane = self.__repo1.get_persoane()
        # lista_evenimente = self.__repo2.get_evenimente()
        # if self.exista_id(id_persoana, lista_persoane) == False:
        # raise ValueError("Persoana cu id-ul dat nu exista in lista! ")
        # if self.exista_id(id_eveniment, lista_evenimente) == False:
        # raise ValueError("Evenimentul cu id-ul dat nu exista in lista! ")

        id_persoana=legatura.get_id_persoana()
        id_eveniment=legatura.get_id_eveniment()
        if self.__exista_in_lista(id_persoana, id_eveniment)==True:
            #raise ValueError("Legatura data a fost deja creeata! ")
            raise Legatura_creeata()
        #legatura = Entitate_legatura(id_persoana, id_eveniment)
        self.get_lista_legaturi().append(legatura)

    # def lista_evenimente_persoana(self, id_persoana):
    #     '''
    #     #Returneaza lista cu id-ul evenimentelor la care participa o persoana
    #     #:param id_persoana: string, id-ul persoanei citite de la tastatura
    #     #:return: lista_evenimente, list, lista de evenimente
    #     '''
    #     lista_evenimente = []
    #     for el in self.__lista_legaturi:
    #         if int(el.get_id_persoana()) == int(id_persoana):
    #             lista_evenimente.append(el.get_id_eveniment())
    #     return lista_evenimente


# def test_ordonare_dupa_data():
#     repo = Memory_rep_legatura()
#     lista_evenimente = [Eveniment(1, '13/09/2021', '14:30', 'Botez'),
#                         Eveniment(4, '14/09/2020', '14:30', 'Nunta'),
#                         Eveniment(3, '12/11/2020', '14:30', 'Concert')
#                         ]
#     repo.ordonare_dupa_data(lista_evenimente)
# for eveniment in lista_evenimente:
# print(eveniment.get_id(), eveniment.get_data())


# test_ordonare_dupa_data()


# def test_get_lista_evenimente():
#     repo1 = Memory_rep_pers()
#     repo2 = Memory_rep_event()
#     repo = Memory_rep_legatura(repo1, repo2)
#     id_persoana = 1
#     repo.adauga_persoana_la_eveniment(1, 1)
#     repo.adauga_persoana_la_eveniment(1, 3)
#     repo.adauga_persoana_la_eveniment(2, 3)
#     lista_id = repo.lista_evenimente_persoana(id_persoana)
#     lista_evenimente = repo.get_lista_evenimente(lista_id)
#     assert len(lista_evenimente) == 2
#
#
# test_get_lista_evenimente()
#
#
# def test_lista_evenimente_persoana():
#     repo1 = Memory_rep_pers()
#     repo2 = Memory_rep_event()
#     repo = Memory_rep_legatura(repo1, repo2)
#     repo.adauga_persoana_la_eveniment(1, 1)
#     repo.adauga_persoana_la_eveniment(1, 3)
#     repo.adauga_persoana_la_eveniment(2, 3)
#     id_persoana = 1
#     lista = repo.lista_evenimente_persoana(id_persoana)
#     assert len(lista) == 2
#
#
# test_lista_evenimente_persoana()
#
#
# def test_exista_id():
#     repo1 = Memory_rep_pers()
#     repo2 = Memory_rep_event()
#     repo = Memory_rep_legatura(repo1, repo2)
#     id_citit = 3
#     lista_persoane = repo1.get_persoane()
#     assert repo.exista_id(id_citit, lista_persoane) == True
#
#     id_citit = 4
#     assert repo.exista_id(id_citit, lista_persoane) == False
#
#     lista_evenimente = repo2.get_evenimente()
#     id_citit = 5
#     assert repo.exista_id(id_citit, lista_evenimente) == False
#
#
# test_exista_id()
#
#
#


def test_adauga_pers_la_eveniment():
    repo = Memory_rep_legatura()
    legatura=Entitate_legatura(1,3)
    repo.adauga_persoana_la_eveniment(legatura)
    try:
        repo.adauga_persoana_la_eveniment(legatura)
        assert False
    #except ValueError as ve:
    except Legatura_creeata as ve:
        #print(ve)
        assert True
    assert len(repo.get_lista_legaturi()) == 1

    legatura=Entitate_legatura(1,2)
    repo.adauga_persoana_la_eveniment(legatura)
    assert len(repo.get_lista_legaturi())==2

test_adauga_pers_la_eveniment()



class LegaturaFileRepo:
    def __init__(self, filename):
        self.__filename=filename

    def __load_from_file(self):
        try:
            f=open(self.__filename, 'r')
        except IOError:
            raise CorruptedFileException()

        lista_leg=[]
        lines=f.readlines()
        for line in lines:
            data_list=line.split(";")
            id_pers=data_list[0].strip()
            id_ev= data_list[1].strip()
            legatura=Entitate_legatura(id_pers, id_ev)
            lista_leg.append(legatura)
        f.close()
        return lista_leg

    def __save_to_file(self, lista_leg):
        with open(self.__filename, 'w') as f:
            for leg in lista_leg:
                leg_str = str(leg.get_id_persoana())+';'+str(leg.get_id_eveniment())+'\n'
                f.write(leg_str)

    def get_lista_legaturi(self):
        return self.__load_from_file()

    def __exista_in_lista(self, id_persoana, id_eveniment):
        '''
        Verifica daca exista in lista de legaturi legatura cu acelasi id_persoana si id_eveniment
        :param id_persoana: string, id-ul persoanei
        :param id_eveniment: string, id-ul evenimentului
        :return: True, daca se gaseste o legatura duplicata, False altfel
        '''
        for leg in self.get_lista_legaturi():
            if (int(leg.get_id_persoana()) == int(id_persoana)) and (int(leg.get_id_eveniment()) == int(id_eveniment)):
                return True
        return False

    def adauga_persoana_la_eveniment(self, legatura):
        '''
        Face legatura dintre persoana si eveniment
        :param id_persoana:
        :param id_eveniment:
        :return:-
        :raises: ValueError daca se gasesc erori de validare
        '''
        # lista_persoane = self.__repo1.get_persoane()
        # lista_evenimente = self.__repo2.get_evenimente()
        # if self.exista_id(id_persoana, lista_persoane) == False:
        # raise ValueError("Persoana cu id-ul dat nu exista in lista! ")
        # if self.exista_id(id_eveniment, lista_evenimente) == False:
        # raise ValueError("Evenimentul cu id-ul dat nu exista in lista! ")

        id_persoana=legatura.get_id_persoana()
        id_eveniment=legatura.get_id_eveniment()
        if self.__exista_in_lista(id_persoana, id_eveniment)==True:
            #raise ValueError("Legatura data a fost deja creeata! ")
            raise Legatura_creeata()
        #legatura = Entitate_legatura(id_persoana, id_eveniment)
        lista_leg= self.get_lista_legaturi()
        #self.get_lista_legaturi().append(legatura)
        lista_leg.append(legatura)
        self.__save_to_file(lista_leg)

    def delete_all(self):
        lista_leg=[]
        self.__save_to_file(lista_leg)





def test_load_file():
    repo=LegaturaFileRepo('legatura_test.txt')
    lista_leg= repo.load_from_file()
    for leg in lista_leg:
        print(leg.get_id_persoana(), leg.get_id_eveniment())

def test_save_to_file():
    lista=[Entitate_legatura('1', '3'),
           Entitate_legatura('2', '4'),
           Entitate_legatura('1','2')]
    repo=LegaturaFileRepo('legatura_test.txt')
    repo.save_to_file(lista)
    lista_leg=repo.load_from_file()
    for leg in lista_leg:
        print(leg.get_id_persoana(), leg.get_id_eveniment())

def test_adauga_legatura():
    leg=Entitate_legatura('4', '3')
    repo=LegaturaFileRepo('legatura_test.txt')
    #repo.adauga_persoana_la_eveniment(leg)
    leg=Entitate_legatura('1','2')
    try:
        repo.adauga_persoana_la_eveniment(leg)
        assert False
    except Legatura_creeata as ve:
        #print(ve)
        assert True


#test_load_file()
#test_save_to_file()
#test_adauga_legatura()
