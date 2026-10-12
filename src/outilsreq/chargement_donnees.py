"""
    Module de chargement des données ouvertes du REQ
"""
import os
import pandas as pd
import psycopg as pg
from .configuration import charger_configuration_depuis_environnement

def vider_base_donnees(connexion: pg.Connection) -> None:
    """Vide la base de données"""
    print("Effacement des données existantes...")
    with connexion.cursor() as cur:
        cur.execute("TRUNCATE TABLE donnees_ouvertes.entreprise CASCADE")
        cur.execute("TRUNCATE TABLE donnees_ouvertes.domaine_valeur CASCADE")

def charger_entreprises(fichier: str, connexion: pg.Connection) -> None:
    """Charge les entreprises dans la base de données"""
    print(f"Chargement du fichier {fichier}...")
    donnees = pd.read_csv(fichier, sep=",", encoding="utf-8", dtype=str)

    print('Nettoyage des données...')
    donnees["IND_FAIL"] = donnees["IND_FAIL"].map({"O": True, "N": False})
    donnees["IND_CONVEN_UNMN_ACTNR"] = donnees["IND_CONVEN_UNMN_ACTNR"].map({"O": True, "N": False})
    donnees["IND_RET_TOUT_POUVR"] = donnees["IND_RET_TOUT_POUVR"].map({"O": True, "N": False})
    donnees["IND_LIMIT_RESP"] = donnees["IND_LIMIT_RESP"].map({"O": True, "N": False})
    donnees["ADR_DOMCL_ADR_DISP"] = donnees["ADR_DOMCL_ADR_DISP"].map({"O": True, "N": False})
    donnees = donnees.drop_duplicates(subset=["NEQ"], keep="first")
    donnees = donnees.astype(object).where(pd.notna(donnees), None)

    try:
        print('Insertion des données dans la base de données...')
        with connexion.cursor() as cur:
            with cur.copy(
                """
                COPY donnees_ouvertes.entreprise (
                    neq,
                    ind_fail,
                    dat_immat,
                    cod_regim_juri,
                    cod_intval_emplo_que,
                    dat_cess_prevu,
                    cod_stat_immat,
                    cod_forme_juri,
                    dat_stat_immat,
                    cod_regim_juri_consti,
                    dat_depo_declr,
                    an_decl,
                    an_prod,
                    dat_limit_prod,
                    an_prod_pre,
                    dat_limit_prod_pre,
                    dat_maj_index_nom,
                    cod_act_econ_cae,
                    no_act_econ_assuj,
                    desc_act_econ_assuj,
                    cod_act_econ_cae2,
                    no_act_econ_assuj2,
                    desc_act_econ_assuj2,
                    nom_loclt_consti,
                    dat_consti,
                    ind_conven_unmn_actnr,
                    ind_ret_tout_pouvr,
                    ind_limit_resp,
                    dat_deb_resp,
                    dat_fin_resp,
                    objet_soc,
                    no_mtr_volont,
                    adr_domcl_adr_disp,
                    adr_domcl_lign1_adr,
                    adr_domcl_lign2_adr,
                    adr_domcl_lign3_adr,
                    adr_domcl_lign4_adr
                )
                FROM STDIN 
                """
            ) as copy:
                for ligne in donnees.itertuples(index=False, name=None):
                    copy.write_row(ligne)
        connexion.commit()
    except:
        connexion.rollback()
        raise

def charger_etablissements(fichier: str, fichier_entreprise: str, connexion: pg.Connection) -> None:
    """Charge les établissements dans la base de données"""
    print(f"Chargement du fichier {fichier}...")
    donnees = pd.read_csv(fichier, sep=",", encoding="utf-8", dtype=str)

    print('Nettoyage des données...')
    neqs = pd.read_csv(fichier_entreprise, usecols=["NEQ"], dtype=str)["NEQ"]
    donnees = donnees[donnees["NEQ"].isin(neqs)]
    donnees["IND_ETAB_PRINC"] = donnees["IND_ETAB_PRINC"].map({"O": True, "N": False})
    donnees["IND_SALON_BRONZ"] = donnees["IND_SALON_BRONZ"].map({"O": True, "N": False})
    donnees["IND_VENTE_TABAC_DETL"] = donnees["IND_VENTE_TABAC_DETL"].map({"O": True, "N": False})
    donnees["IND_DISP"] = donnees["IND_DISP"].map({"O": True, "N": False})
    donnees = donnees.drop_duplicates(subset=["NEQ", "NO_SUF_ETAB"], keep="first")
    donnees = donnees.astype(object).where(pd.notna(donnees), None)

    try:
        print('Insertion des données dans la base de données...')
        with connexion.cursor() as cur:
            with cur.copy(
                """
                COPY donnees_ouvertes.etablissement (
                    neq,
                    no_suf_etab,
                    ind_etab_princ,
                    ind_salon_bronz,
                    ind_vente_tabac_detl,
                    ind_disp,
                    lign1_adr,
                    lign2_adr,
                    lign3_adr,
                    lign4_adr,
                    cod_act_econ,
                    desc_act_econ_etab,
                    no_act_econ_etab,
                    cod_act_econ2,
                    desc_act_econ_etab2,
                    no_act_econ_etab2,
                    nom_etab
                )
                FROM STDIN 
                """
            ) as copy:
                for ligne in donnees.itertuples(index=False, name=None):
                    copy.write_row(ligne)

        connexion.commit()
    except:
        connexion.rollback()
        raise

def charger_noms(fichier: str, fichier_entreprise: str, connexion: pg.Connection) -> None:
    """Charge les noms dans la base de données"""
    print(f"Chargement du fichier {fichier}...")
    donnees = pd.read_csv(fichier, sep=",", encoding="utf-8", dtype=str)

    print('Nettoyage des données...')
    neqs = pd.read_csv(fichier_entreprise, usecols=["NEQ"], dtype=str)["NEQ"]
    donnees = donnees[donnees["NEQ"].isin(neqs)]
    donnees = donnees.dropna(subset=["NOM_ASSUJ"])
    donnees = donnees.drop_duplicates(
        subset=["NEQ", "NOM_ASSUJ", "STAT_NOM", "TYP_NOM_ASSUJ"],
        keep="first"
    )
    donnees = donnees.astype(object).where(pd.notna(donnees), None)

    try:
        print('Insertion des données dans la base de données...')
        with connexion.cursor() as cur:
            with cur.copy(
                """
                COPY donnees_ouvertes.nom (
                    neq,
                    nom_assuj,
                    nom_assuj_lang_etrng,
                    stat_nom,
                    typ_nom_assuj,
                    dat_init_nom_assuj,
                    dat_fin_nom_assuj
                )
                FROM STDIN 
                """
            ) as copy:
                for ligne in donnees.itertuples(index=False, name=None):
                    copy.write_row(ligne)

        connexion.commit()
    except:
        connexion.rollback()
        raise

def charger_fusions_scissions(
        fichier: str,
        fichier_entreprise: str,
        connexion: pg.Connection
) -> None:
    """Charge les fusions et scissions dans la base de données"""
    print(f"Chargement du fichier {fichier}...")
    donnees = pd.read_csv(fichier, sep=",", encoding="utf-8", dtype=str)

    print('Nettoyage des données...')
    neqs = pd.read_csv(fichier_entreprise, usecols=["NEQ"], dtype=str)["NEQ"]
    donnees = donnees[donnees["NEQ"].isin(neqs)]
    donnees = donnees[donnees["NEQ_ASSUJ_REL"].isin(neqs)]
    donnees["IND_DISP"] = donnees["IND_DISP"].map({"O": True, "N": False})
    donnees = donnees.dropna(subset=["NEQ_ASSUJ_REL"])
    donnees = donnees.drop_duplicates(
        subset=["NEQ", "NEQ_ASSUJ_REL", "COD_RELA_ASSUJ", "DAT_EFCTVT"],
        keep="first"
    )
    donnees = donnees.astype(object).where(pd.notna(donnees), None)

    try:
        print('Insertion des données dans la base de données...')
        with connexion.cursor() as cur:
            with cur.copy(
                """
                COPY donnees_ouvertes.fusion_scission (
                    neq,
                    neq_assuj_rel,
                    denomn_soc,
                    cod_rela_assuj,
                    dat_efctvt,
                    ind_disp,
                    lign1_adr,
                    lign2_adr,
                    lign3_adr,
                    lign4_adr
                )
                FROM STDIN 
                """
            ) as copy:
                for ligne in donnees.itertuples(index=False, name=None):
                    copy.write_row(ligne)

        connexion.commit()
    except:
        connexion.rollback()
        raise

def charger_continuations_transformations(
    fichier: str,
    fichier_entreprise: str,
    connexion: pg.Connection
) -> None:
    """Charge les continuations et transformations dans la base de données"""
    print(f"Chargement du fichier {fichier}...")
    donnees = pd.read_csv(fichier, sep=",", encoding="utf-8", dtype=str)

    print('Nettoyage des données...')
    neqs = pd.read_csv(fichier_entreprise, usecols=["NEQ"], dtype=str)["NEQ"]
    donnees = donnees[donnees["NEQ"].isin(neqs)]
    donnees = donnees.drop_duplicates(
        subset=["NEQ", "COD_TYP_CHANG", "DAT_EFCTVT"],
        keep="first"
    )
    donnees = donnees.astype(object).where(pd.notna(donnees), None)

    try:
        print('Insertion des données dans la base de données...')
        with connexion.cursor() as cur:
            with cur.copy(
                """
                COPY donnees_ouvertes.continuation_transformation (
                    neq,
                    cod_typ_chang,
                    cod_regim_juri,
                    autr_regim_juri,
                    nom_loclt,
                    dat_efctvt
                )
                FROM STDIN 
                """
            ) as copy:
                for ligne in donnees.itertuples(index=False, name=None):
                    copy.write_row(ligne)

        connexion.commit()
    except:
        connexion.rollback()
        raise

def charger_domaine_valeur(fichier: str, connexion: pg.Connection) -> None:
    """Charge les domaines de valeurs dans la base de données"""
    print(f"Chargement du fichier {fichier}...")
    donnees = pd.read_csv(fichier, sep=",", encoding="utf-8", dtype=str)

    print('Nettoyage des données...')
    donnees = donnees.drop_duplicates(
        subset=["TYP_DOM_VAL", "COD_DOM_VAL"],
        keep="first"
    )
    donnees = donnees.astype(object).where(pd.notna(donnees), None)

    try:
        print('Insertion des données dans la base de données...')
        with connexion.cursor() as cur:
            with cur.copy(
                """
                COPY donnees_ouvertes.domaine_valeur (
                    typ_dom_val,
                    cod_dom_val,
                    val_dom_fran
                )
                FROM STDIN 
                """
            ) as copy:
                for ligne in donnees.itertuples(index=False, name=None):
                    copy.write_row(ligne)

        connexion.commit()
    except:
        connexion.rollback()
        raise

def charger_donnees(repertoire: str) -> None:
    """Charge les données ouvertes du REQ dans une bd postgres"""
    if not os.path.exists(repertoire):
        raise FileNotFoundError(f"Le répertoire {repertoire} n'existe pas.")

    if not os.path.isdir(repertoire):
        raise NotADirectoryError(f"{repertoire} n'est pas un répertoire.")

    fichier_entreprise = os.path.join(repertoire, "Entreprise.csv")
    fichier_etablissement = os.path.join(repertoire, "Etablissements.csv")
    fichier_nom = os.path.join(repertoire, "Nom.csv")
    fichier_fusion_scission = os.path.join(repertoire, "FusionScissions.csv")
    fichier_continuation = os.path.join(repertoire, "ContinuationsTransformations.csv")
    fichier_domaine_valeur = os.path.join(repertoire, "DomaineValeur.csv")

    configuration = charger_configuration_depuis_environnement()
    connexion = pg.connect(
        host=configuration.bd.hote,
        port=configuration.bd.port,
        dbname=configuration.bd.nom_bd_req,
        user=configuration.bd.utilisateurs.admin_req.nom,
        password=configuration.bd.utilisateurs.admin_req.mot_passe
    )

    vider_base_donnees(connexion)

    charger_entreprises(fichier_entreprise, connexion)
    charger_etablissements(fichier_etablissement, fichier_entreprise, connexion)
    charger_noms(fichier_nom, fichier_entreprise, connexion)
    charger_fusions_scissions(fichier_fusion_scission, fichier_entreprise, connexion)
    charger_continuations_transformations(fichier_continuation, fichier_entreprise, connexion)
    charger_domaine_valeur(fichier_domaine_valeur, connexion)
