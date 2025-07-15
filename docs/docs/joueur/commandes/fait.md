---
id: fait
slug: /joueur/commandes/fait
sidebar_label: done
---

# Commande `done`

Cette commande permet de valider une tâche que vous venez de réaliser.

- **Alias** : `done`, `réalisé`
- **Arguments** : `[NOMBRE]` (obligatoire)
- **Permissions** : Tout le monde sauf les [**imposteurs**](/docs/joueur/roles#imposteur)
- **Utilisation** :
    - `fait NOMBRE`
- **Exemple d'utilisation** :
    - `fait 1`
- **Exemples de retour** :
    - Validation réussie :
        ```
        Votre tâche scanner a été confirmée comme faite !
        ```
    - Si la tâche n'existe pas :
        ```
        Veuillez entrer un numéro de tâche valide !
        ```
    - Si la tâche est déjà faite :
        ```
        Vous avez déjà déclaré avoir fait la tâche 1
        ```
    - Si vous êtes imposteur :
        ```
        Vous ne pouvez pas valider des tâches, vous êtes imposteur.
        ```

La commande `fait` permet de valider une tâche que vous venez de réaliser.

Indispensable pour faire progresser la partie et prouver votre implication !

:::warning
N'abusez pas de cette commande et ne validez que les tâches réellement effectuées.
:::