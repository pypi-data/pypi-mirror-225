import os
import json
from types import SimpleNamespace
from typing import List
from inspqcommun.fa.ressources.ressource import Ressource

class ChargeurFichiers:

    def __init__(self, chemin: str = None) -> None:
        self.chemin : str = chemin

    def obtenir_fichiers(self) -> List[str]:
        return [f for f in os.listdir(self.chemin) if os.path.isfile(f) and f.endswith('.json')]
    
    def charger_fichier(self, fichier) -> List[Ressource]:
        f = open(fichier, encoding='utf-8')
        objet = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
        f.close()
        return objet