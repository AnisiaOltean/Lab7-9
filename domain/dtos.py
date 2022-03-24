class EvenimentParticipanti:
    def __init__(self, descriere_eveniment, nr_participanti):
        self.__descriere=descriere_eveniment
        self.__nr_participanti= nr_participanti

    def get_descriere(self):
        return self.__descriere
    def get_nr_participanti(self):
        return self.__nr_participanti

class EvenimentIDParticipanti:
    def __init__(self, id_eveniment, nr_participanti):
        self.__id=id_eveniment
        self.__nr_participanti= nr_participanti
    def get_id(self):
        return self.__id
    def get_nr_participanti(self):
        return self.__nr_participanti
