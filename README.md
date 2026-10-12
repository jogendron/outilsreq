# Outils REQ
Ce projet regroupe des outils ayant pour but d'interagir avec les données du Registraire des entreprises du Québec.

Pour le moment, la seule fonctionnalité consiste à charger les données ouvertes dans une base de données SQL.

## Prérequis
* docker (ou votre propre installation de PostgreSQL)
* uv

## Configuration des variables d'environnement
Le projet lit ses paramètres à partir d'un fichier `.env` (exclu de Git). Créez à la racine du projet un fichier `.env` contenant les variables suivantes :

```env
OUTILSREQ_BD_HOTE=localhost
OUTILSREQ_BD_PORT=5432
OUTILSREQ_BD_NOMBDPOSTGRES=postgres
OUTILSREQ_BD_NOMBDREQ=req

OUTILSREQ_BD_UTILISATEURS_POSTGRES_NOM=postgres
OUTILSREQ_BD_UTILISATEURS_POSTGRES_MOTPASSE=postgres

OUTILSREQ_BD_UTILISATEURS_ADMINREQ_NOM=req_adm
OUTILSREQ_BD_UTILISATEURS_ADMINREQ_MOTPASSE=req_adm

OUTILSREQ_BD_UTILISATEURS_STANDARDREQ_NOM=req_usr
OUTILSREQ_BD_UTILISATEURS_STANDARDREQ_MOTPASSE=req_usr
```

Ces valeurs sont fournies à titre d'exemple pour un environnement de développement local. Modifiez-les selon votre configuration et choisissez des mots de passe robustes, notamment pour les comptes `postgres`, `req_usr` et `req_adm`.

## Installation des dépendances Python
À la racine du projet, lancez la commande suivante :
```bash
uv sync
```

## Mise en place de la base de données
### 1.a) Configuration avec Docker (pour développement local)
À la racine du projet, lancez la commande suivante :

```bash
docker compose -f docker/outilsreq/compose.yaml up -d
```

Le mot de passe défini pour le compte `postgres` dans `docker/outilsreq/compose.yaml` doit correspondre à la valeur de `OUTILSREQ_BD_UTILISATEURS_POSTGRES_MOTPASSE` dans le fichier `.env`.

### 1.b) Configuration manuelle
La procédure détaillée ne sera pas couverte ici, mais vous pouvez installer PostgreSQL à l'emplacement de votre choix. Assurez-vous que les variables d'environnement reflètent votre configuration.

### 2) Création du schéma et des tables
Vérifiez que vos variables d'environnement sont correctes, puis lancez la commande suivante à la racine du projet :

```bash
uv run outilsreq initialiser_bd
```

## Utilisation
Téléchargez une archive des données ouvertes du REQ et extrayez-la. Le répertoire d'extraction doit contenir les fichiers CSV suivants :

* `Entreprise.csv`
* `Etablissements.csv`
* `Nom.csv`
* `FusionScissions.csv`
* `ContinuationsTransformations.csv`
* `DomaineValeur.csv`

À la racine du projet, lancez la commande suivante pour charger ces fichiers dans les tables de la base de données :

```bash
uv run outilsreq charger_donnees "/chemin/vers/votre_extraction"
```
