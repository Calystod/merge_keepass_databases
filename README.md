# Merge KeePass Databases

## Présentation

Ce projet a pour but de merger plusieurs bases KeePass ayant le même mot de passe, par exemple, si vous utilisez le même fichier d'origine sur différents supports et que ces copies ne sont pas synchronisées.

Pour une même entrée, la version la plus récemment modifiée sera celle qui sera gardé.

Si aucune date d'expiration n'a été programmé sur une entrée, celle-ci sera ajouté et calculé sur 1 an après la date de dernière modification de l'entrée.

## Installation

1. Installer les dépendances avec `pipenv install`
2. Ajoutez les répertoires `new_bases` et `old_bases` à la racine de ce dossier
3. Ajoutez les bases de données keepass (version 2) que vous souhaitez merger dans le répertoire `old_bases`. Celles-ci doivent toutes avoir le même mot de passe
4. Lancez la commande `pipenv run python merge_keepass.py`
5. Entrez le mot de passe utilisé pour vos bases de données. Ce sera le même mot de passe pour la nouvelle base de données
6. Attendez la fin de l'exécution
