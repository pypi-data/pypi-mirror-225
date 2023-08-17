from inspqcommun.fa.chargement_service import ChargementService
from inspqcommun.fa.validateurs.validateur_usager import ValidateurUsager, ValidateurUsagerPourAppariement
from inspqcommun.fa.validateurs.validateur_acte_vaccinal import ValidateurActeVaccinal
from inspqcommun.fa.convertisseurs.convertisseur_usager import ConvertisseurUsager
from inspqcommun.fa.convertisseurs.convertisseur_acte_vaccinal import ConvertisseurActeVaccinal
from inspqcommun.fa.chargeur_fichiers import ChargeurFichiers
from inspqcommun.fhir.clients.patient_client import PatientClient
from inspqcommun.fhir.clients.immunization_client import ImmunizationClient

url_base_fonctions_allegees = 'http://location:8080'
uri_serveur_fhir = '/fa-services'
headers = {"Authorization": "bearer eysdfsdf"}

validateur_usager = ValidateurUsager()
validateur_usager_pour_appariement = ValidateurUsagerPourAppariement()
validateur_acte_vaccinal = ValidateurActeVaccinal(validateur_usager_pour_appariement)

convertisseur_usager = ConvertisseurUsager()
convertisseur_acte_vaccinal = ConvertisseurActeVaccinal(convertisseur_usager=convertisseur_usager)

chargeur = ChargeurFichiers()

patient_client = PatientClient(base_url=url_base_fonctions_allegees, base_uri=uri_serveur_fhir, token_header=headers,validate_certs=False)
immunization_client = ImmunizationClient(base_url=url_base_fonctions_allegees, base_uri=uri_serveur_fhir, token_header=headers,validate_certs=False)

service = ChargementService(chargeur_fichiers=chargeur, 
                            validateur_usager=validateur_usager, 
                            validateur_acte_vaccinal=validateur_acte_vaccinal,
                            convertisseur_usager=convertisseur_usager,
                            convertisseur_acte_vaccinal=convertisseur_acte_vaccinal,
                            patient_client=patient_client,
                            immunization_client=immunization_client)

service.charger()

print ('Chargé!')