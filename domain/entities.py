from datetime import date


class Persoana:
    def __init__(self, id_pers, nume, adresa):
        '''
        Creeaza o persoana cu id-ul, numele si adresa data
        :param id_pers: int, id-ul persoanei
        :param nume: string, numele persoanei
        :param adresa: string, adresa persoanei
        '''
        self.__id = id_pers
        self.__name = nume
        self.__adress = adresa

    def get_id(self):
        return self.__id

    def get_nume(self):
        return self.__name

    def get_adress(self):
        return self.__adress

    def set_id(self, new_id):
        self.__id = new_id

    def set_nume(self, new_name):
        self.__name = new_name

    def set_adress(self, new_adress):
        self.__adress = new_adress


class Eveniment:
    def __init__(self, id_eveniment, data, timp, descriere):
        '''
        Creeaza un eveniment cu id-ul, data, timpul si descrierea date
        :param id_eveniment: int, id-ul evenimentului
        :param data: string, data evenimentului
        :param timp: string, timpul evenimentului
        :param descriere: string, descrierea evenimentului
        '''
        self.__id = id_eveniment
        self.__date = data
        self.__time = timp
        self.__desc = descriere

    def get_id(self):
        return self.__id

    def get_data(self):
        return self.__date

    def get_time(self):
        return self.__time

    def get_description(self):
        return self.__desc

    def set_id(self, new_id):
        self.__id = new_id

    def set_date(self, new_date):
        self.__date = new_date

    def set_time(self, new_time):
        self.__time = new_time

    def set_description(self, new_description):
        self.__desc = new_description


class Entitate_legatura:
    def __init__(self, id_persoana, id_event):
        self.__id_persoana = id_persoana
        self.__id_eveniment = id_event

    def get_id_persoana(self):
        return self.__id_persoana

    def get_id_eveniment(self):
        return self.__id_eveniment


def test_creare_legatura():
    entity = Entitate_legatura(1, 5)
    assert entity.get_id_persoana() == 1
    assert entity.get_id_eveniment() == 5


def test_creare_persoana():
    p = Persoana(1, 'Popescu Ion', 'Rozelor, nr.14')
    assert p.get_id() == 1
    assert p.get_nume() == 'Popescu Ion'
    assert p.get_adress() == 'Rozelor, nr.14'

    p.set_id(2)
    p.set_nume('Georgescu Maria')
    p.set_adress('Blv. Eroilor, nr.16')

    assert p.get_id() == 2
    assert p.get_nume() == 'Georgescu Maria'
    assert p.get_adress() == 'Blv. Eroilor, nr.16'


def test_creare_eveniment():
    event = Eveniment(1, '13/02/2020', '18:00', 'Nunta')

    assert event.get_id() == 1
    assert event.get_data() =='13/02/2020'
    assert event.get_time() == '18:00'
    assert event.get_description() == 'Nunta'

    event.set_id(3)
    event.set_date('14/09/2021')
    event.set_time('17:30')
    event.set_description('Aniversare')

    assert event.get_id() == 3
    assert event.get_data() == '14/09/2021'
    assert event.get_time() == '17:30'
    assert event.get_description() == 'Aniversare'


test_creare_persoana()
test_creare_eveniment()
test_creare_legatura()
