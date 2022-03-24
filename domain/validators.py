from domain.entities import Persoana, Eveniment, Entitate_legatura
from repository.exeptions.exeptions import ValidationException


def este_intreg(numar):
    '''
    verifica daca numarul dat de la tastatura este intreg
    :return: True daca este numar intreg, False altfel
    '''
    try:
        numar = int(numar)
        return True
    except ValueError:
        return False


def test_este_intreg():
    numar = 14
    assert este_intreg(numar) == True

    numar = '12c'
    assert este_intreg(numar) == False


test_este_intreg()


def valid_data(data):
    lista_date = data.split("/")
    errors = []
    zi = lista_date[0]
    luna = lista_date[1]
    an = lista_date[2]
    if len(lista_date) < 3:
        errors.append("Data nu a fost instrodusa sub formatul corect!")
    if este_intreg(zi) == False:
        errors.append("Ziua trebuie sa fie numar intreg!")
    if este_intreg(zi) == True and (int(zi) < 0 or int(zi) > 31):
        errors.append("Ziua trebuie sa fie intre 1 si 31! ")
    if este_intreg(luna) == False:
        errors.append("Luna trebuie sa fie numar intreg!")
    if este_intreg(luna) == True and (int(luna) < 0 or int(luna) > 12):
        errors.append("Luna trebuie sa fie intre 1 si 12!")
    if este_intreg(an) == False:
        errors.append("Anul trebuie sa fie numar intreg!")
    return errors


def test_valid_data():
    data = '14/02/2018'
    lista_erori = valid_data(data)
    assert len(lista_erori) == 0

    data2 = '32/cc/2013'
    lista_erori = valid_data(data2)
    assert len(lista_erori) == 2


test_valid_data()


def validare_timp(timp):
    '''
    Valideaza un timp citit de la tastatura (se considera ca timpul este un string de forma ora:minut)
    :param timp: string
    :return: errors, list, contine toate erorile gasite
    '''
    errors = []
    timp_list = timp.split(":")
    ora = timp_list[0]
    minut = timp_list[1]
    if este_intreg(ora) == False:
        errors.append('Ora trebuie sa fie intreg!')
    if este_intreg(ora) == True and (int(ora) < 0 or int(ora) > 23):
        errors.append("Ora trebuie sa fie intre 1 si 24! ")
    if este_intreg(minut) == False:
        errors.append('Minutul trebuie sa fie intreg!')
    if este_intreg(minut) == True and (int(minut) < 0 or int(minut) > 59):
        errors.append("Minutul trebuie sa fie intre 1 si 59! ")
    return errors


def test_validare_timp():
    timp = '14:58'
    lista_erori = validare_timp(timp)
    assert len(lista_erori) == 0

    timp1 = 'aa:03'
    lista_erori = validare_timp(timp1)
    assert len(lista_erori) == 1
    # print(lista_erori)

    timp = '24:cd'
    lista_erori = validare_timp(timp)
    assert len(lista_erori) == 2
    # print(lista_erori)


test_validare_timp()


class PersoanaValidator:

    def validate(self, persoana):
        '''
        Valideaza datele unei persoane
        :param persoana: Persoana object, o persoana
        :return:-
        :raises ValueError daca gaseste erori de validare
        '''
        errors = []
        if este_intreg(persoana.get_id()) == False:
            errors.append("Id-ul persoanei trebuie sa fie numar intreg! ")
        if len(persoana.get_nume().split()) < 2:
            errors.append("Numele persoanei trebuie sa aiba 2 cuvinte! ")
        if len(persoana.get_adress().split(",")) < 2:
            errors.append("Adresa persoanei trebuie sa aiba o strada si un numar!")

        if len(errors) > 0:
            #error_string = '\n'.join(errors)
            #raise ValueError(error_string)
            raise ValidationException(errors)

    def valid_id_citit(self, id_citit):
        '''
        Verifica daca id-ul citit de la tastatura este nr. intreg
        :param id_citit: int, id-ul citit
        :return:-
        :raises: ValueError daca id-ul nu este numar intreg
        '''
        if este_intreg(id_citit) == False:
            raise ValueError('Id-ul citit trebuie sa fie numar intreg! ')

    def valid_id_in_lista(self, id_citit, lista_persoane):
        '''
        Verifica daca id-ul citit este intreg si exista in lista de persoane
        :param id_citit: int, id-ul citit de la tastatura
        :param lista_persoane: list, lista de persoane
        :return: -
        :raises: ValueError daca se gasesc erori de validare
        '''
        if este_intreg(id_citit) == False:
            raise ValueError('Id-ul citit trebuie sa fie numar intreg! ')
        ok = 0
        if este_intreg(id_citit) == True:
            for i, el in enumerate(lista_persoane):
                if int(el.get_id()) == int(id_citit):
                    ok = 1
            if ok == 0:
                raise ValueError("Id-ul citit nu exista in lista! ")


def test_valid_id_in_lista():
    val=PersoanaValidator()
    lista=[Persoana(1, 'Amalia Popescu', 'Blv. Transilvaniei, nr.18'),
           Persoana(2, 'Bogdan Bucurenci', 'Bucuriei, nr.34')
          ]

    id_citit=2
    val.valid_id_in_lista(id_citit, lista)

    id_citit=3
    try:
        val.valid_id_in_lista(id_citit, lista)
        assert False
    except ValueError as ve:
        #print(ve)
        assert True

test_valid_id_in_lista()

class EvenimentValidator:

    def validate(self, eveniment):
        errors = []
        errors_date = valid_data(eveniment.get_data())
        errors_time = validare_timp(eveniment.get_time())
        if este_intreg(eveniment.get_id()) == False:
            errors.append("Id-ul evenimentului trebuie sa fie numar intreg! ")
        for er in errors_date:
            errors.append(er)
        for er in errors_time:
            errors.append(er)
        if eveniment.get_description() == '':
            errors.append("Descrierea evenimentului trebuie sa existe! ")

        if len(errors) > 0:
            #error_string = '\n'.join(errors)
            #raise ValueError(errors)
            raise ValidationException(errors)

    def valid_id_citit(self, id_citit):
        '''
        Verifica daca id-ul citit de la tastatura este nr. intreg
        :param id_citit: int, id-ul citit
        :return:-
        :raises: ValueError daca id-ul nu este numar intreg
        '''
        if este_intreg(id_citit) == False:
            raise ValueError('Id-ul citit trebuie sa fie numar intreg! ')

class LegaturaValidator:
    def validate(self, legatura):
        lista_erori= []
        if int(legatura.get_id_persoana())<0:
            lista_erori.append("Id-ul persoanei trebuie sa fie numar pozitiv! ")
        if int(legatura.get_id_eveniment())<0:
            lista_erori.append("Id-ul evenimentului trebuie sa fie numar pozitiv! ")
        if len(lista_erori) > 0:
            error_string = '\n'.join(lista_erori)
            raise ValueError(lista_erori)


def test_validare_legatura():
    legatura=Entitate_legatura(1,3)
    val=LegaturaValidator()
    try:
        legatura=Entitate_legatura(-1,4)
        val.validate(legatura)
        assert False
    except ValueError as ve:
        #print(ve)
        assert True

test_validare_legatura()



def test_validare_eveniment():
    eveniment = Eveniment(1, '14/02/2022', '18:30', 'Nunta')
    val = EvenimentValidator()
    val.validate(eveniment)

    try:
        event2 = Eveniment(2, '13/15/201s', '24:13', 'Aniversare')
        val.validate(event2)
        assert False
    #except ValueError as ve:
    except ValidationException as ve:
        #print(ve)
        assert True

    try:
        event3 = Eveniment('ac', '2cf/10/2018', '3d:15', 'Botez')
        val.validate(event3)
        assert False
    #except ValueError as ve:
    except ValidationException as ve:
        #print(ve)
        assert True


test_validare_eveniment()


def test_validare_persoana():
    a = Persoana(1, 'Maria Popescu', 'Rozelor, nr.14')
    val = PersoanaValidator()
    val.validate(a)

    try:
        b = Persoana('cde', 'Amalia', 'Independentei, nr.3')
        val.validate(b)
        assert False
    #except ValueError:
    except ValidationException as ve:
        #print(ve)
        assert True


def test_valid_id_citit():
    val = PersoanaValidator()
    id_citit = 4
    val.valid_id_citit(id_citit)
    id_citit = 'a'
    try:
        val.valid_id_citit(id_citit)
        assert False
    except ValueError as ve:
        # print(ve)
        assert True


test_validare_persoana()
test_valid_id_citit()
