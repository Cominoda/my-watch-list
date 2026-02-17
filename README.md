# to-do-list app
To-Do-List application built with django to Create, Update and Delete tasks.
<br>
<br>
![todolist](https://user-images.githubusercontent.com/65074901/125083144-a5e03900-e0e5-11eb-9092-da716a30a5f3.JPG)

# Gestion des Commits et des Versions

## Conventions de Commits
Spécification [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) pour les messages de commit.

### Format

    [type] [scope (optionnel)]: [description]

### Types utilisés 

- `feat` : nouvelle fonctionnalité
- `fix` : correction de bug
- `docs` : documentation
- `refactor` : amélioration interne
- `test` : ajout/mise à jour de tests
- `chore` : maintenance, dépendances, scripts

### Exemples

    feat(todo): ajouter la création de tâches
    fix(ui): corriger l'affichage mobile
    docs: mettre à jour le README avec les nouvelles instructions

---

## Gestion Sémantique des Versions (SemVer)
Sspécification [Semantic Versioning 2.0.0](https://semver.org/lang/fr/) pour versionnage. 

**Format** : `MAJEUR.MINEUR.CORRECTIF`.

- **MAJEUR** : Incrémenté pour des changements non rétrocompatibles.
- **MINEUR** : Incrémenté pour des ajouts de fonctionnalités rétrocompatibles.
- **CORRECTIF** : Incrémenté pour des corrections de bugs rétrocompatibles.

### Exemples
- `1.0.0` : Première version stable.
- `1.1.0` : Ajout d’une fonctionnalité rétrocompatible.
- `2.0.0` : Changement non rétrocompatible.
