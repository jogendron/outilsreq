"""
Module d'initialisation de la base de données REQ
"""
from pathlib import Path
import psycopg
from .configuration import Configuration
from .configuration import charger_configuration_depuis_environnement

def creer_bd_avec_utilisateurs(configuration : Configuration) -> None:
    """Crée la base de données REQ et les utilisateurs"""
    with psycopg.connect(
        host=configuration.bd.hote,
        port=configuration.bd.port,
        dbname=configuration.bd.nom_bd_postgres,
        user=configuration.bd.utilisateurs.postgres.nom,
        password=configuration.bd.utilisateurs.postgres.mot_passe,
        autocommit=True
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL(
                    "create database {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.nom_bd_req)
                )
            )

def creer_schema_donnees_ouvertes(configuration : Configuration) -> None:
    """Crée le schéma donnees_ouvertes dans la base de données REQ"""
    script = Path("sql/creer_bd.sql").read_text(encoding="utf-8")
    
    with psycopg.connect(
        host=configuration.bd.hote,
        port=configuration.bd.port,
        dbname=configuration.bd.nom_bd_req,
        user=configuration.bd.utilisateurs.postgres.nom,
        password=configuration.bd.utilisateurs.postgres.mot_passe
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(script)

def creer_utilisateurs(configuration : Configuration) -> None:
    """Donne les droits d'accès aux utilisateurs sur la base de données REQ"""
    with psycopg.connect(
        host=configuration.bd.hote,
        port=configuration.bd.port,
        dbname=configuration.bd.nom_bd_req,
        user=configuration.bd.utilisateurs.postgres.nom,
        password=configuration.bd.utilisateurs.postgres.mot_passe,
        autocommit=True
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL(
                    "create user {} with password {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.admin_req.nom),
                    psycopg.sql.Literal(configuration.bd.utilisateurs.admin_req.mot_passe)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "create user {} with password {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.standard_req.nom),
                    psycopg.sql.Literal(configuration.bd.utilisateurs.standard_req.mot_passe)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "GRANT CONNECT ON DATABASE req TO {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.admin_req.nom)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "GRANT CONNECT ON DATABASE req TO {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.standard_req.nom)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "GRANT USAGE ON SCHEMA donnees_ouvertes TO {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.standard_req.nom)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "GRANT USAGE ON SCHEMA donnees_ouvertes TO {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.admin_req.nom)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA donnees_ouvertes TO {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.standard_req.nom)
                )
            )

            cur.execute(
                psycopg.sql.SQL(
                    "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA donnees_ouvertes TO {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.utilisateurs.admin_req.nom)
                )
            )

def initialiser_bd() -> None:
    """Initialise la base de données selon les paramètres en variables d'environnement"""
    configuration = charger_configuration_depuis_environnement()

    try:
        creer_bd_avec_utilisateurs(configuration)
        creer_schema_donnees_ouvertes(configuration)
        creer_utilisateurs(configuration)
    except (psycopg.errors.DuplicateDatabase, psycopg.errors.DuplicateObject):
        print("La base de donnees est deja initialisee.")

if __name__ == "__main__":
    initialiser_bd()
