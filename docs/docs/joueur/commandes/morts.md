---
id: morts
slug: /joueur/commandes/morts
sidebar_label: deads
---

# Commande `deads`

Cette commande permet de visualiser l'état des joueurs dans la partie, indiquant s'ils sont vivants ou éliminés.

- **Alias** : `morts`, `mort`, `view`, `states`, `états`
- **Permissions** : Rôle [**scientifique**](/docs/joueur/roles#scientifique) uniquement
- **Utilisation** :
  - `morts`
- **Exemple d'utilisation** :
  - `morts`
- **Exemple de retour** :
  - Quand il reste des demandes :
    ```
    Voici les états de chaque joueur:
    - Alice (mort)
    - Bob (vivant)
    - Charlie (mort)
    Il vous reste 2/3 demandes.
    ```
  - Quand il n'y a plus de demandes :
    ```
    Vous avez utilisé toutes vos demandes !
    ```

Cette commande va permettre de surveiller l'évolution de la partie et d'anticiper les stratégies.
