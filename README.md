# Merge KeePass Databases

## Présentation

Ce projet a pour but de merger plusieurs bases KeePass ayant le même mot de passe, par exemple, si vous utilisez le même fichier d'origine sur différents supports et que ces copies ne sont pas synchronisées.

Pour une même entrée, la version la plus récemment modifiée sera celle qui sera gardé.

Si aucune date d'expiration n'a été programmé sur une entrée, celle-ci sera ajouté et calculé sur 1 an après la date de dernière modification de l'entrée.