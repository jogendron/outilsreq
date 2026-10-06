"""
Module d'initialisation de la base de données REQ
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg

def initialiser_bd() -> None:
    """Initialise la base de données selon les paramètres en variables d'environnement"""
    load_dotenv()

    with psycopg.connect(
        host=os.getenv("OUTILSREQ_HOTE"),
        port=os.getenv("OUTILSREQ_PORT"),
        dbname=os.getenv("OUTILSREQ_BD_POSTGRES"),
        user=os.getenv("OUTILSREQ_UTILISATEUR_POSTGRES"),
        password=os.getenv("OUTILSREQ_MOT_PASSE_POSTGRES"),
        autocommit=True
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL(
                    "create user req_adm with password {}"
                ).format(psycopg.sql.Literal(os.getenv("OUTILSREQ_MOT_PASSE_REQADM")))
            )

            cur.execute(
                psycopg.sql.SQL(
                    "create user req_usr with password {}"
                ).format(psycopg.sql.Literal(os.getenv("OUTILSREQ_MOT_PASSE_REQUSR")))
            )

            cur.execute("create database req")

    script = Path("sql/creer_bd.sql").read_text(encoding="utf-8")

    with psycopg.connect(
        host=os.getenv("OUTILSREQ_HOTE"),
        port=os.getenv("OUTILSREQ_PORT"),
        dbname="req",
        user=os.getenv("OUTILSREQ_UTILISATEUR_POSTGRES"),
        password=os.getenv("OUTILSREQ_MOT_PASSE_POSTGRES")
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(script)

if __name__ == "__main__":
    initialiser_bd()
