from inspqcommun.fa.validateurs.validateur_usager import ValidateurUsager
from inspqcommun.fa.validateurs.validateur_acte_vaccinal import ValidateurActeVaccinal
from inspqcommun.fa.convertisseurs.convertisseur_usager import ConvertisseurUsager
from inspqcommun.fa.convertisseurs.convertisseur_acte_vaccinal import ConvertisseurActeVaccinal
from inspqcommun.fa.chargeur_fichiers import ChargeurFichiers
from inspqcommun.fhir.clients.patient_client import PatientClient
from inspqcommun.fhir.clients.immunization_client import ImmunizationClient

class ChargementService:

    def __init__(self, chargeur_fichiers : ChargeurFichiers, validateur_usager: ValidateurUsager, validateur_acte_vaccinal: ValidateurActeVaccinal,
                 convertisseur_usager : ConvertisseurUsager, convertisseur_acte_vaccinal : ConvertisseurActeVaccinal, patient_client: PatientClient,
                 immunization_client: ImmunizationClient):
        self.__chargeur_fichiers : ChargeurFichiers = chargeur_fichiers
        self.__validateur_usager : ValidateurUsager = validateur_usager
        self.__validateur_acte_vaccinal : ValidateurActeVaccinal = validateur_acte_vaccinal
        self.__convertisseur_usager : ConvertisseurUsager = convertisseur_usager
        self.__convertisseur_acte_vaccinal : ConvertisseurActeVaccinal = convertisseur_acte_vaccinal
        self.__patient_client : PatientClient = patient_client
        self.__immunization_client : ImmunizationClient = immunization_client

    def charger(self):
        for fichier in self.__chargeur_fichiers.obtenir_fichiers():
            ressources = self.__chargeur_fichiers.charger_fichier(fichier)

            for ressource in ressources:
                match ressource.ressource:
                    case "Usager":
                        if self.__validateur_usager.valider(ressource):
                            patient = self.__convertisseur_usager.toFhir(ressource)
                            response = self.__patient_client.match(patient)
                            if response.status_code == 204:
                                self.__patient_client.create(patient)
                            # TODO supporter la modification de l'usager
                    case "ActeVaccinal":
                        if self.__validateur_acte_vaccinal.valider(ressource):
                            immunization = self.__convertisseur_acte_vaccinal.toFhir(ressource)
                            self.__immunization_client.create(immunization)
                            # TODO supporter la modification de l'acte vaccinal s'il existe (faire un appariement)