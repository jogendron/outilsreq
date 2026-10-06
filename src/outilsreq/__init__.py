"""
Outils de chargement des données ouvertes du REQ
"""
import argparse
from .initialiser_bd import initialiser_bd
from .charger_donnees import charger_donnees

def main() -> None:
    """Outils de chargement des données ouvertes du REQ."""
    parser = argparse.ArgumentParser(
        prog="outils REQ",
        description="Outils de chargement des données ouvertes du REQ",
    )

    sous_commandes = parser.add_subparsers(
        dest="commande",
        required=True,
    )

    sous_commandes.add_parser(
        "initialiser_bd",
        help="Initialise la base de données",
    )

    charger = sous_commandes.add_parser(
        "charger_donnees",
        help="Charge les données du REQ",
    )
    charger.add_argument(
        "chemin",
        help="Chemin vers les données à charger",
    )

    arguments = parser.parse_args()

    match arguments.commande:
        case "initialiser_bd":
            initialiser_bd()
        case "charger_donnees":
            charger_donnees(arguments.chemin)

if __name__ == "__main__":
    main()
