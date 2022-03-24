from repository.exeptions.exeptions import DuplicateIDException, ValidationException, PersonNotFound, EventNotFound, \
    Legatura_creeata, NotEnoughEvents, NotEnoughPers


class Console:
    def __init__(self, srv1, srv2, srv3):
        self.__srv1 = srv1
        self.__srv2 = srv2
        self.__srv3 = srv3

    def __afisare_persoane(self, lista_persoane):
        # lista_persoane = self.__srv1.get_persoane()
        if len(lista_persoane) == 0:
            print('Nu exista persoane in lista. ')
        if len(lista_persoane) != 0:
            print("Persoanele sunt: ")
            for persoana in lista_persoane:
                print('Id:', persoana.get_id(), 'Nume:', persoana.get_nume(), 'Adresa:', persoana.get_adress())

    def __afisare_evenimente(self, lista_evenimente):
        # lista_evenimente = self.__srv2.get_lista_evenimente()
        if len(lista_evenimente) == 0:
            print('Nu exista evenimente in lista. ')
        if len(lista_evenimente) != 0:
            print("Evenimentele sunt: ")
            for eveniment in lista_evenimente:
                print('Id:', eveniment.get_id(), 'Data:', eveniment.get_data(), 'Timp:', eveniment.get_time(),
                      'Descriere:', eveniment.get_description())

    def __adaugare_persoana(self):
        id_pers = input("Introduceti id-ul persoanei (trebuie sa fie numar intreg): ")
        nume = input("Introduceti numele complet al persoanei: ")
        adresa = input("Introduceti adresa persoanei: ")

        try:
            pers = self.__srv1.adaug_persoana(id_pers, nume, adresa)
            print('Persoana cu id-ul', pers.get_id(), 'numele', pers.get_nume(), 'si adresa', pers.get_adress(),
                  's-a adaugat cu succes. ')
        #except ValueError as ve:
        except DuplicateIDException as ve:
            print(str(ve))
        except ValidationException as ve:
            print(str(ve))

    def __adaugare_eveniment(self):
        id_eveniment = input("Introduceti id-ul evenimentului (ca numar intreg): ")
        data = input("Introduceti data evenimentului (sub forma zz/ll/aaaa): ")
        timp = input("Introduceti timpul (sub forma hh/mm): ")
        descriere = input("Introduceti descrierea evenimentului: ")

        try:
            eveniment = self.__srv2.adauga_eveniment(id_eveniment, data, timp, descriere)
            print('Evenimentul cu id-ul', eveniment.get_id(), 'data', eveniment.get_data(), 'timpul',
                  eveniment.get_time(),
                  'si descrierea', eveniment.get_description(), 's-a adaugat cu succes')
        except DuplicateIDException as ve:
            print(ve)
        except ValidationException as ve:
            print(ve)
        #except ValueError as ve:
            #print(ve)

    def __modificare_persoana_din_lista(self):
        id_citit = input("Introduceti id-ul persoanei de modificat: ")
        # id_persoana = input("Introduceti id-ul noii persoane: ")
        nume = input("Introduceti numele noii persoane: ")
        adresa = input("Introduceti noua adresa a persoanei: ")
        try:
            self.__srv1.modifica_persoana(id_citit, nume, adresa)
            print("Persoana s-a modificat cu succes! ")
        #except ValueError as ve:
        except PersonNotFound as ve:
            print(str(ve))
        except ValidationException as ve:
            print(str(ve))

    def __modificare_eveniment_din_lista(self):
        id_citit = input("Introduceti id-ul evenimentului de modificat: ")
        # id_eveniment = input("Introduceti id-ul noului eveniment: ")
        data = input("Introduceti data noului eveniment: ")
        timp = input("Introduceti timpul noului eveniment: ")
        descriere = input("Introduceti descrierea noului eveniment: ")
        try:
            self.__srv2.modifica_eveniment(id_citit, data, timp, descriere)
            print("Evenimentul s-a modificat cu succes! ")
        except EventNotFound as ve:
            print(ve)
        except ValidationException as ve:
            print(ve)
        #except ValueError as ve:
            #print(ve)

    def __sterge_persoana_din_lista(self):
        id_citit = input("Introduceti id-ul persoanei de sters: ")
        try:
            self.__srv1.sterge_persoana(id_citit)
            print("Persoana s-a sters cu succes! ")
        #except ValueError as ve:
        except PersonNotFound as ve:
            print(str(ve))

    def __sterge_eveniment_din_lista(self):
        id_citit = input("Introduceti id-ul evenimentului: ")
        try:
            self.__srv2.sterge_eveniment_din_lista(id_citit)
            print("Evenimentul s-a sters cu succes! ")
        #except ValueError as ve:
        except EventNotFound as ve:
            print(ve)

    def __afisare_persoane_nume_dat(self):
        nume_citit = input("Introduceti numele de familie: ")
        try:
            lista_pers = self.__srv1.afiseaza_pers_nume_dat(nume_citit)
            self.__afisare_persoane(lista_pers)
        except ValueError as ve:
            print(str(ve))

    def __evenimente_descrierea_data(self):
        descriere = input("Introduceti descrierea evenimentului: ")
        try:
            lista_evenimente = self.__srv2.cauta_dupa_descriere(descriere)
            self.__afisare_evenimente(lista_evenimente)
        except ValueError as ve:
            print(ve)

    def __add_pers_eveniment(self):
        id_persoana = input("Introduceti id-ul persoanei: ")
        id_eveniment = input("Introduceti id-ul evenimentului: ")
        try:
            self.__srv3.adauga_pers_eveniment(id_persoana, id_eveniment)
            print("Legatura s-a creeat cu succes! ")
        #except ValueError as ve:
        except PersonNotFound as ve:
            print(ve)
        except EventNotFound as ve:
            print(ve)
        except Legatura_creeata as ve:
            print(ve)

    def __afisare_evenimente_persoana_data(self):
        id_persoana = input("Introduceti id-ul persoanei: ")
        try:
            # lista_legaturi = self.__srv3.get_lista_leg()
            # repo_legatura= self.__srv3.get_legatura_repo()
            # lista = self.__srv2.lista_evenimente_ordonata_persoana(id_persoana, lista_legaturi)
            lista = self.__srv3.lista_ordonata_data(id_persoana)
            self.__afisare_evenimente(lista)
        #except ValueError as ve:
        except PersonNotFound as ve:
            print(ve)

    def __afisare_evenimente_ord_cresc_descriere(self):
        id_persoana = input("Introduceti id-ul persoanei: ")
        try:
            # lista_legaturi = self.__srv3.get_lista_leg()
            # repo_legatura= self.__srv3.get_legatura_repo()
            lista = self.__srv3.lista_ordonata_descriere(id_persoana)
            self.__afisare_evenimente(lista)
        #except ValueError as ve:
        except PersonNotFound as ve:
            print(ve)

    def __adaug_pers_random(self):
        self.__srv1.adauga_random()
        print("Persoana s-a adugat cu succes! ")

    def __afisare_persoane_nr_maxim_evenimente(self):
        lista_persoane = self.__srv3.return_lista_persoane_nr_maxim_de_evenimente()
        self.__afisare_persoane(lista_persoane)

    def __primele_evenimente(self):
        try:
            lista_ev = self.__srv3.evenimente_most_participanti()
            for ev in lista_ev:
                print(ev.get_descriere(), ev.get_nr_participanti())
        #except ValueError as ve:
        except NotEnoughEvents as ve:
            print(ve)

    def __adauga_ev_random(self):
        try:
            self.__srv2.adauga_eveniment_random()
        #except ValueError as ve:
        except ValidationException as ve:
            print(ve)
        except DuplicateIDException as ve:
            print(ve)

    def __top3_eveniemnte(self):
        try:
            lista_ev = self.__srv3.top_3_evenimente()
            for ev in lista_ev:
                print(ev.get_id(), ev.get_data(), ev.get_time(), ev.get_description())
        #except ValueError as ve:
        except NotEnoughPers as ve:
            print(ve)

    def show_ui(self):
        while True:
            print("1. Adaugare persoana")
            print("2. Adaugare eveniment")
            print("3. Afisare lista persoane")
            print("4. Afisare lista evenimente")
            print("5. Modificare persoana din lista")
            print("6. Modificare eveniment din lista")
            print("7. Sterge persoana din lista")
            print("8. Sterge eveniment din lista")
            print("9. Cautare persoane dupa nume de familie dat")
            print("10. Cautare evenimente dupa descrierea data")
            print("11. Inscriere persoana la eveniment")
            print("12. Afisare lista de evenimente la care participă o persoană ordonat crescator după data ")
            print("13. Afisare lista de evenimente la care participă o persoană ordonat alfabetic după descriere ")
            print("14. Adauga persoana random")
            print("15. Afisare persoane participante la cele mai multe evenimente")
            print("16. Afisare primele 20% evenimente cu cei mai mulți participanți (descriere, număr participanți)")
            print("17. Adauga eveniment random")
            print("18. Afisare top 3 evenimente cu cei mai multi participanti")
            print("19. Iesire din aplicatie")
            cmd = input("Introduceti optiunea dumneavoastra: ")
            if cmd == '1':
                self.__adaugare_persoana()
            elif cmd == '2':
                self.__adaugare_eveniment()
            elif cmd == '3':
                self.__afisare_persoane(self.__srv1.get_persoane())
            elif cmd == '4':
                self.__afisare_evenimente(self.__srv2.get_lista_evenimente())
            elif cmd == '5':
                self.__modificare_persoana_din_lista()
            elif cmd == '6':
                self.__modificare_eveniment_din_lista()
            elif cmd == '7':
                self.__sterge_persoana_din_lista()
            elif cmd == '8':
                self.__sterge_eveniment_din_lista()
            elif cmd == '9':
                self.__afisare_persoane_nume_dat()
            elif cmd == '10':
                self.__evenimente_descrierea_data()
            elif cmd == '11':
                self.__add_pers_eveniment()
            elif cmd == '12':
                self.__afisare_evenimente_persoana_data()
            elif cmd == '13':
                self.__afisare_evenimente_ord_cresc_descriere()
            elif cmd == '14':
                self.__adaug_pers_random()
            elif cmd == '15':
                self.__afisare_persoane_nr_maxim_evenimente()
            elif cmd == '16':
                self.__primele_evenimente()
            elif cmd=='17':
                self.__adauga_ev_random()
            elif cmd=='18':
                self.__top3_eveniemnte()
            elif cmd == '19':
                print("Ati iesit din aplicatie! ")
                return
            else:
                print("Comanda invalida! ")
