'''
P5. Organizare evenimente
    Scrieți o aplicație pentru organizarea de evenimente
    Aplicația stochează:
        - persoane: <personID>, <nume>, <adresă>
        - evenimente: <ID>, <dată>, <timp>, <descriere>
Creați o aplicație care permite:
    - gestiunea listei de persoane și evenimente.
    - adaugă, șterge, modifică, lista de persoane, lista de evenimente
    - căutare persoane, căutare evenimente
    - Înscriere persoană la eveniment.
    - Rapoarte:
        - Lista de evenimente la care participă o persoană ordonat alfabetic după descriere, după dată
        - Persoane participante la cele mai multe evenimente
        - Primele 20% evenimente cu cei mai mulți participanți (descriere, număr participanți)

'''
from domain.validators import PersoanaValidator, EvenimentValidator, LegaturaValidator
from repository.eveniment_repository import Memory_rep_event, Event_file_repo
from repository.legatura_repository import Memory_rep_legatura, LegaturaFileRepo
from repository.persoana_repository import Memory_rep_pers, Persoana_file_repo
from service.eveniment_service import EvenimentService
from service.legatura_service import LegaturaService
from service.persoana_service import PersoanaService
from ui.console import Console

val1 = PersoanaValidator()
#repo1 = Memory_rep_pers()
repo1file= Persoana_file_repo('persoane.txt')
val2 = EvenimentValidator()
#repo2 = Memory_rep_event()
repo2file=Event_file_repo('evenimente.txt')
#srv1 = PersoanaService(repo1, val1)
srv1file=PersoanaService(repo1file, val1)
#srv2 = EvenimentService(repo2, val2)
srv2file=EvenimentService(repo2file, val2)
#repo3 = Memory_rep_legatura()
repo3file=LegaturaFileRepo('legaturi.txt')
val3 = LegaturaValidator()
#srv3 = LegaturaService(repo3, val3, repo1, repo2)
srv3file= LegaturaService(repo3file, val3, repo1file, repo2file)
ui = Console(srv1file, srv2file, srv3file)
ui.show_ui()
