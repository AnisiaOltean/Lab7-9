import random

from domain.entities import Persoana
from repository.exeptions.exeptions import DuplicateIDException, PersonNotFound, CorruptedFileException


class Memory_rep_pers:
    def __init__(self):
        # vom stoca aici toate persoanele intr-o lista de persoane
        # se adauga niste persoane predefinite in lista
        self.__persoane = [Persoana(1, 'Maria Popescu', 'Independentei, nr.16'),
                           Persoana(2, 'Mihai Popescu', 'Blv. Transilvaniei, nr.16'),
                           Persoana(3, 'Elena Georgescu', 'Bucium, nr.23C')]

    def exists_with_id(self, id_citit):
        '''
        Verifica daca in lista curenta de persoane exista o persoana cu id-ul egal cu cel citit de la tastatura
        :param: id_citit- string, id-ul citit de la tastatura
        :return: True daca se gaseste o astfel de persoana, False altfel
        '''
        for pers in self.get_persoane():
            if int(pers.get_id()) == int(id_citit):
                return True
        return False

    def adauga(self, persoana):
        '''
        Adauga persoana in lista de persoane
        :param persoana: object, obiect al clasei Persoana
        :return:-
        '''
        if self.exists_with_id(persoana.get_id()):  # verifcare daca exista o persoana cu id-ul citit in lista
            # raise ValueError("Exista persoana cu id-ul citit! ")
            raise DuplicateIDException()
        self.__persoane.append(persoana)

    def get_persoane(self):
        '''
        Returneaza lista de persoane
        :return: self.__persoane, lista de persoane
        '''
        return self.__persoane

    def get_lungime_lista_persoane(self):
        return len(self.__persoane)

    def find_pers_with_id(self, id_citit):
        '''
        Cauta persoana cu id-ul citit de la tastatura
        Daca se gaseste returneaza index-ul din lista, altfel returneaza -1
        :param id_citit: string, id-ul citit de la tastatura
        :return: index, int, indexul persoanei cu id-ul egal cuc el citit de la tastatura
        '''

        index = -1
        for i, persoana in enumerate(self.get_persoane()):
            if int(persoana.get_id()) == int(id_citit):
                index = i
        return index

    def modifica_persoana_din_lista(self, id_pers, persoana):
        '''
        Modifica persoana cu id-ul citit de la tastatura cu persoana noua citita de la tastatura
        :param persoana: object, obiect al clasei persoana
        :return: -
        '''
        index = self.find_pers_with_id(id_pers)
        if index == -1:
            # raise ValueError("Nu exista persoana cu id-ul dat!")
            raise PersonNotFound()
            # for i, el in enumerate(self.__persoane):
            # if int(el.get_id()) == int(id_pers):
        self.__persoane[index] = persoana

    def sterge_persoana_id_dat(self, id_dat):
        '''
        Sterge persoana cu id-ul dat din lista
        :param: id_dat- int, id-ul persoanei ce trebuie eliminata din lista
        :return: -
        '''

        index = self.find_pers_with_id(id_dat)  # index-ul persoanei cu id-ul citit
        if index == -1:
            # raise ValueError("Nu exista persoana cu id-ul dat! ")
            raise PersonNotFound()
        self.__persoane.pop(index)

    def lista_pers_nume_dat(self, name):
        '''
        Returneaza o lista noua de persoane formata doar din persoanele care au numele de familie egal
        cu cel citit de la tastatura
        :param name: string, numele citit de la tastatura
        :return: new_list, list, lista de persoane ce respecta conditia data
        '''
        nume_familie = name
        new_list = []
        for persoana in self.get_persoane():
            nume_pers = persoana.get_nume()
            name_list = nume_pers.split()
            if nume_familie == name_list[1]:
                new_list.append(persoana)
        return new_list

    def find_pers_id(self, id_pers):
        '''
        Returneaza persoana din lista ce are id-ul egal cu cel citit de la tastatura
        :param id_eveniment: string, id-ul evenimentului
        :return: eveniment, obiect al clasei eveniment
        '''
        lista_pers = self.get_persoane()
        if self.exists_with_id(id_pers) == False:
            # raise ValueError("Persoana cu id-ul dat nu exista in lista! ")
            raise PersonNotFound()
        for pers in lista_pers:
            if int(pers.get_id()) == int(id_pers):
                return pers

    def delete_all(self):
        self.__persoane=[]

    def find_pers_with_id_rec(self, lista, lungime, id_citit):
        '''
        Cauta persoana cu id-ul citit de la tastatura
        Daca se gaseste returneaza index-ul din lista, altfel returneaza -1
        :param id_citit: string, id-ul citit de la tastatura
                lista: list, lista de persoane
                lungime: int, lungimea listei de persoane
        :return: index, int, indexul persoanei cu id-ul egal cu cel citit de la tastatura
        '''
        if lista == []:
            return  -(lungime+1)   # base case
        elif int(lista[0].get_id()) == int(id_citit):
                return 0
        else:
            return 1 + self.find_pers_with_id_rec(lista[1:], lungime, id_citit)



def test_find_id_rec():
    repo = Memory_rep_pers()
    p = Persoana(4, 'Amalia Dinescu', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    lista= repo.get_persoane()
    lungime= len(lista)
    index= repo.find_pers_with_id_rec(lista, lungime, 4)
    assert index == 3

    index= repo.find_pers_with_id_rec(lista, lungime, 6)
    assert index == -1

    index = repo.find_pers_with_id_rec(lista, lungime, '1')
    assert index == 0


test_find_id_rec()



def test_find_pers_id():
    repo = Memory_rep_pers()
    p = Persoana(4, 'Amalia Dinescu', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    pers = repo.find_pers_id('4')
    assert pers.get_nume() == 'Amalia Dinescu'
    try:
        pers = repo.find_pers_id(5)
        assert False
    # except ValueError as ve:
    except PersonNotFound as ve:
        # print(ve)
        assert True


test_find_pers_id()


def test_sterge_persoana_id_dat():
    repo = Memory_rep_pers()
    p = Persoana(4, 'Amalia Dinescu', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    id_citit = 4
    repo.sterge_persoana_id_dat(id_citit)
    assert len(repo.get_persoane()) == 3

    id_citit = 5
    try:
        repo.sterge_persoana_id_dat(id_citit)
        assert False
    # except ValueError as ve:
    except PersonNotFound as ve:
        # print(ve)
        assert True


test_sterge_persoana_id_dat()


def test_adauga_persoana():
    repo = Memory_rep_pers()
    pers = Persoana(4, 'Ion Gheorghe', 'Pacii, nr.32C')
    repo.adauga(pers)
    assert len(repo.get_persoane()) == 4
    pers = Persoana(4, 'Ion Gheorghe', 'Pacii, nr.32C')
    try:
        repo.adauga(pers)
        assert False
    # except ValueError as ve:
    except DuplicateIDException:
        # print(ve)
        assert True


def test_modifica_persoana_din_lista():
    repo = Memory_rep_pers()
    id_pers = 3
    for i, el in enumerate(repo.get_persoane()):
        if el.get_id() == id_pers:
            index = i
    persoana = Persoana(id_pers, 'Amalia Dutu', 'Bucuriei, nr.34')
    try:
        repo.modifica_persoana_din_lista(id_pers, persoana)
        assert True
    # except ValueError as ve:
    except PersonNotFound as ve:
        # print(ve)
        assert False
    assert repo.get_persoane()[index].get_nume() == 'Amalia Dutu'

    id_citit = 5
    persoana = Persoana(id_citit, 'Popescu Aurelia', 'Barzan, nr.56V')
    try:
        repo.modifica_persoana_din_lista(id_citit, persoana)
        assert False
    # except ValueError as ve:
    except PersonNotFound as ve:
        # print(ve)
        assert True

    # assert repo.get_persoane()[index].get_nume() == 'Amalia Dutu'


def test_afisare_persoane():
    repo = Memory_rep_pers()
    nume_dat = 'Popescu'
    lista_noua = repo.lista_pers_nume_dat(nume_dat)
    assert len(lista_noua) == 2
    # for pers in lista_noua:
    # print(pers.get_id(), pers.get_nume())


test_afisare_persoane()
test_modifica_persoana_din_lista()
test_adauga_persoana()


class Persoana_file_repo:
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

        lista_persoane = []
        lines = f.readlines()
        for line in lines:
            pers_id, pers_name, prs_adress = [token.strip() for token in line.split(';')]
            a = Persoana(pers_id, pers_name, prs_adress)
            lista_persoane.append(a)
        f.close()
        return lista_persoane

    def __save_to_file(self, lista_persoane):
        '''
        Salveaza pesoanele din lista in fisier
        :param lista_persoane: list, lista de persoane
        :return: -
        '''
        with open(self.__filename, 'w') as f:
            for persoana in lista_persoane:
                pers_string = str(persoana.get_id()) + ';' + str(persoana.get_nume()) + ';' + str(
                    persoana.get_adress()) + '\n'
                f.write(pers_string)

    def get_persoane(self):
        '''
        Returneaza lista de persoane
        :return: self.__persoane, lista de persoane
        '''
        return self.__load_from_file()

    def exists_with_id(self, id_citit):
        '''
        Verifica daca in lista curenta de persoane exista o persoana cu id-ul egal cu cel citit de la tastatura
        :param: id_citit- string, id-ul citit de la tastatura
        :return: True daca se gaseste o astfel de persoana, False altfel
        '''
        for pers in self.get_persoane():
            if int(pers.get_id()) == int(id_citit):
                return True
        return False

    def adauga(self, persoana):
        '''
        Adauga persoana in lista de persoane
        :param persoana: object, obiect al clasei Persoana
        :return:-
        '''

        lista_persoane=self.__load_from_file()
        if self.exists_with_id(persoana.get_id()):  # verifcare daca exista o persoana cu id-ul citit in lista
            # raise ValueError("Exista persoana cu id-ul citit! ")
            raise DuplicateIDException()
        lista_persoane.append(persoana)
        self.__save_to_file(lista_persoane)

    def find_pers_with_id(self, id_citit):
        '''
        Cauta persoana cu id-ul citit de la tastatura
        Daca se gaseste returneaza index-ul din lista, altfel returneaza -1
        :param id_citit: string, id-ul citit de la tastatura
        :return: index, int, indexul persoanei cu id-ul egal cuc el citit de la tastatura
        '''

        index = -1
        for i, persoana in enumerate(self.get_persoane()):
            if int(persoana.get_id()) == int(id_citit):
                index = i
        return index

    def modifica_persoana_din_lista(self, id_pers, persoana):
        '''
        Modifica persoana cu id-ul citit de la tastatura cu persoana noua citita de la tastatura
        :param persoana: object, obiect al clasei persoana
        :return: -
        '''
        #index = self.find_pers_with_id(id_pers)
        index = self.find_pers_with_id_rec(self.get_persoane(), len(self.get_persoane()), id_pers)
        if index == -1:
            # raise ValueError("Nu exista persoana cu id-ul dat!")
            raise PersonNotFound()
            # for i, el in enumerate(self.__persoane):
            # if int(el.get_id()) == int(id_pers):
        lista_persoane= self.get_persoane()
        lista_persoane[index] = persoana
        self.__save_to_file(lista_persoane)

    def sterge_persoana_id_dat(self, id_dat):
        '''
        Sterge persoana cu id-ul dat din lista
        :param: id_dat- int, id-ul persoanei ce trebuie eliminata din lista
        :return: -
        '''

        #index = self.find_pers_with_id(id_dat)  # index-ul persoanei cu id-ul citit
        index = self.find_pers_with_id_rec(self.get_persoane(), len(self.get_persoane()), id_dat)
        if index == -1:
            # raise ValueError("Nu exista persoana cu id-ul dat! ")
            raise PersonNotFound()
        lista_pers= self.get_persoane()
        lista_pers.pop(index)
        self.__save_to_file(lista_pers)

    def lista_pers_nume_dat(self, name):
        '''
        Returneaza o lista noua de persoane formata doar din persoanele care au numele de familie egal
        cu cel citit de la tastatura
        :param name: string, numele citit de la tastatura
        :return: new_list, list, lista de persoane ce respecta conditia data
        '''
        nume_familie = name
        new_list = []
        for persoana in self.get_persoane():
            nume_pers = persoana.get_nume()
            name_list = nume_pers.split()
            if nume_familie == name_list[1]:
                new_list.append(persoana)
        return new_list

    def find_pers_id(self, id_pers):
        '''
        Returneaza persoana din lista ce are id-ul egal cu cel citit de la tastatura
        :param id_eveniment: string, id-ul evenimentului
        :return: eveniment, obiect al clasei eveniment
        '''
        lista_pers = self.get_persoane()
        if self.exists_with_id(id_pers) == False:
            # raise ValueError("Persoana cu id-ul dat nu exista in lista! ")
            raise PersonNotFound()
        for pers in lista_pers:
            if int(pers.get_id()) == int(id_pers):
                return pers

    def find_pers_with_id_rec(self, lista, lungime, id_citit):
        '''
        Cauta persoana cu id-ul citit de la tastatura
        Daca se gaseste returneaza index-ul din lista, altfel returneaza -1
        :param id_citit: string, id-ul citit de la tastatura
                lista: list, lista de persoane
                lungime: int, lungimea listei de persoane
        :return: index, int, indexul persoanei cu id-ul egal cuc el citit de la tastatura
        '''
        if lista == []:
            return  -(lungime+1)   # base case
        elif int(lista[0].get_id()) == int(id_citit):
                return 0
        else:
            return 1 + self.find_pers_with_id_rec(lista[1:], lungime, id_citit)

    def delete_all(self):
        lista_pers = []
        self.__save_to_file(lista_pers)





def test_id_rec():
    repo = Persoana_file_repo('pers_test.txt')
    repo.delete_all()
    p = Persoana(4, 'Amalia Dinescu', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    p = Persoana(2, 'Amalia Popescu', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    p = Persoana(1, 'Ion Gheorghe', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    p = Persoana(3, 'Ghita Ene', 'Transilvaniei, nr.6C')
    repo.adauga(p)
    lista= repo.get_persoane()
    lungime= len(lista)
    index= repo.find_pers_with_id_rec(lista, lungime, 4)
    assert index == 0

    index = repo.find_pers_with_id_rec(lista, lungime, 6)
    assert index == -1

    index = repo.find_pers_with_id_rec(lista, lungime, '1')
    assert index == 2

test_id_rec()

def test_load_from_file():
    repo= Persoana_file_repo('pers_test.txt')
    lista=repo.get_persoane()
    for pers in lista:
        print(pers.get_id(), pers.get_nume(), pers.get_adress())


def test_modifica_persoana_file():
    repo=Persoana_file_repo('pers_test.txt')
    id_pers=4
    #p=Persoana(id_pers, 'Maricica Lucica', 'Unirii, nr.26C')
    repo.modifica_persoana_din_lista(id_pers, p)
    lista=repo.get_persoane()
    #for pers in lista:
        #print(pers.get_id(), pers.get_nume(), pers.get_adress())

def test_sterge_file():
    repo=Persoana_file_repo('pers_test.txt')
    id_pers=2
    repo.sterge_persoana_id_dat(2)
    lista=repo.get_persoane()
    # try:
    #     repo.sterge_persoana_id_dat(2)
    #     assert False
    # except PersonNotFound as ve:
    #     print(ve)
    #     assert True
    #for pers in lista:
        #print(pers.get_id(), pers.get_nume(), pers.get_adress())


def test_nume_file():
    repo=Persoana_file_repo('pers_test.txt')
    nume='Popescu'
    lista_nume= repo.lista_pers_nume_dat(nume)
    for persona in lista_nume:
        print(persona.get_id(), persona.get_nume(), persona.get_adress())

def test_find_id_file():
    repo=Persoana_file_repo('pers_test.txt')
    id=2
    persoana=repo.find_pers_id(id)
    print(persoana.get_id(), persoana.get_nume(), persoana.get_adress())
    id=7
    try:
        persoana=repo.find_pers_id(id)
        assert False
    except PersonNotFound as ve:
        print(ve)
        assert True

#test_load_from_file()
#test_modifica_persoana_file()
#test_sterge_file()
#test_nume_file()
#test_find_id_file()

