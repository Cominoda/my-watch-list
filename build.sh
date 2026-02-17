
#-e (errexit) : quitte le script si une commande échoue
#-u (nounset) : quitte le script si une variable non définie est utilisée
#-o pipefail : Par déf, dans un pipeline (ex: cmd1 | cmd2), le code de retour 
    #est celui de la dernière commande (cmd2), même si cmd1 échoue. 
    #Avec pipefail, le pipeline échoue si une seule des commandes du pipeline échoue.
#-x (xtrace) : affiche chaque commande avant de l'exécuter (utile pour le débogage)
set -euo pipefail
#set -euox pipefail

# Vérifier si un argument est fourni
# -z : controle si la chaîne est vide (vraie si la longueur est nulle)
# >&2 : redirige la sortie vers stderr (flux d'erreur standard)
if [ -z "$1" ]; then
    echo "Erreur : Aucun argument fourni. Utilisation : $0 version=<numVersion>" >&2
    exit 1
fi

# Vérifier s'il n'y a qu'un seul argument
# $# : nombre d'arguments passés au script
# -ne : n'est pas égal
if [ $# -ne 1 ]; then
    echo "Erreur : Trop d'arguments. Un seul argument est attendu : version=<numVersion>" >&2
    exit 1
fi

# =~ : Bash's regex-matching operator
# double crochets [[ ]] : test avancé de Bash (ex : =~), pas disponible partout
# https://stackoverflow.com/questions/669452/are-double-square-brackets-preferable-over-single-square-brackets-in-b
# https://mywiki.wooledge.org/BashFAQ/031
if [[ "$1" =~ ^version=[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Format valide : $1"
    # Extraire la valeur de la version
    NUM_VERSION=${1#version=}
    echo "Numéro de version : $NUM_VERSION"
else
    echo "Erreur : Format invalide. Utilisez le format version=<numVersion> (ex: version=1.0 ou version=2.3.4)"
    exit 1
fi

SETTINGS_PATH="todo/settings.py"

#-f : vérifie si le fichier existe et est un fichier régulier
if [ ! -f "$SETTINGS_PATH" ]; then
  echo "Fichier introuvable: $SETTINGS_PATH" >&2
  exit 1
fi

pipenv run ruff check .

#-q (quiet) : supprime la sortie standard, ne renvoie que le code de retour
# . : motif spécial en expressions régulières qui correspond à n'importe quel caractère
if git tag --list "$NUM_VERSION" | grep -q . ; then
  echo "Le tag '$NUM_VERSION' existe déjà" >&2
  exit 1
fi

# - : Indique que le script Python sera lu depuis l'entrée standard (stdin) plutôt que depuis un fichier.
# << : Début d'un "here document" (ou "here string" si c'est <<<). 
      #Cela signifie que tout ce qui suit sera envoyé comme entrée à la commande précédente
# SCRIPT_PY : délimiteur personalisé qui marque le debut et la fin du here document
python3 - << SCRIPT_PY
from pathlib import Path
import re, sys

version = "$NUM_VERSION"
path = Path("$SETTINGS_PATH")
text = path.read_text()
new_text, count = re.subn(r"VERSION\s*=\s*['\"]([^'\"]*)['\"]", f"VERSION = '{version}'", text, count=1)
if count == 0:
    sys.exit("Aucune assignation VERSION trouvée")
path.write_text(new_text)
SCRIPT_PY

#git add .
##git commit -m "Bump version to $NUM_VERSION"
git tag "$NUM_VERSION"

#archivage
ARCHIVE_NAME="todolist-$NUM_VERSION.zip"
git archive --format=zip --output "$ARCHIVE_NAME" HEAD

echo "Mise à jour de la version dans $NUM_VERSION..."