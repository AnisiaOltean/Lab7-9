class GalaException(Exception):
    pass


class ValidationException(GalaException):
    def __init__(self, msgs):
        """
        :param msgs: lista de mesaje de eroare
        :type msgs: msgs
        """
        self.__err_msgs = msgs

    def getMessages(self):
        return self.__err_msgs

    def __str__(self):
        return 'Validation Exception: ' + str(self.__err_msgs)


class RepositoryException(GalaException):
    def __init__(self, msg):
        self.__msg = msg

    def getMessage(self):
        return self.__msg

    def __str__(self):
        return 'Repository Exception: ' + str(self.__msg)


class DuplicateIDException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "ID duplicat.")

class PersonNotFound(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Persoana cu id-ul dat nu exista in lista! ")

class EventNotFound(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Evenimentul cu id-ul dat nu exista in lista! ")

class Legatura_creeata(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Legatura a fost deja creeata! ")

class NotEnoughEvents(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Nu exista destule evenimente! ")

class NotEnoughPers(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Nu s-au inscris persoane la 3 evenimente! ")

class CorruptedFileException(RepositoryException):
    def __init__(self):
        RepositoryException.__init__(self, "Fisier corupt")