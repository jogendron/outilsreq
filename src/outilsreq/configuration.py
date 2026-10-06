"""
Module de chargement de la configuration 
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class UtilisateurBd:
    """Représente un utilisateur de la base de données"""
    nom: str
    mot_passe: str

@dataclass
class Utilisateurs:
    """Représente la liste des utilisateurs de la base de données"""
    admin_req: UtilisateurBd
    standard_req: UtilisateurBd
    postgres: UtilisateurBd

@dataclass
class ConfigurationBd:
    """Représente les configurations en lien avec la base de données"""
    hote: str
    port: int
    nom_bd_postgres: str
    nom_bd_req: str
    utilisateurs: Utilisateurs

@dataclass
class Configuration:
    """Représente la configuration dans son ensemble"""
    bd: ConfigurationBd

def charger_configuration_depuis_environnement() -> Configuration:
    """Charge la configuration depuis les variables d'environnement"""
    load_dotenv()

    return Configuration(
        bd=ConfigurationBd(
            hote=os.getenv("OUTILSREQ_BD_HOTE"),
            port=int(os.getenv("OUTILSREQ_BD_PORT")),
            nom_bd_postgres=os.getenv("OUTILSREQ_BD_NOMBDPOSTGRES"),
            nom_bd_req=os.getenv("OUTILSREQ_BD_NOMBDREQ"),
            utilisateurs=Utilisateurs(
                admin_req=UtilisateurBd(
                    nom=os.getenv("OUTILSREQ_BD_UTILISATEURS_ADMINREQ_NOM"),
                    mot_passe=os.getenv("OUTILSREQ_BD_UTILISATEURS_ADMINREQ_MOTPASSE")
                ),
                standard_req=UtilisateurBd(
                    nom=os.getenv("OUTILSREQ_BD_UTILISATEURS_STANDARDREQ_NOM"),
                    mot_passe=os.getenv("OUTILSREQ_BD_UTILISATEURS_STANDARDREQ_MOTPASSE")
                ),
                postgres=UtilisateurBd(
                    nom=os.getenv("OUTILSREQ_BD_UTILISATEURS_POSTGRES_NOM"),
                    mot_passe=os.getenv("OUTILSREQ_BD_UTILISATEURS_POSTGRES_MOTPASSE")
                )
            )
        )
    )
