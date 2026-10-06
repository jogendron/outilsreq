"""
Module d'initialisation de la base de données REQ
"""
from pathlib import Path
import psycopg

from .configuration import charger_configuration_depuis_environnement

def initialiser_bd() -> None:
    """Initialise la base de données selon les paramètres en variables d'environnement"""
    configuration = charger_configuration_depuis_environnement()

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
                    "create database {}"
                ).format(
                    psycopg.sql.Identifier(configuration.bd.nom_bd_req)
                )
            )

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

if __name__ == "__main__":
    initialiser_bd()
