---
id: tuer
slug: /joueur/commandes/tuer
sidebar_label: kill
---

# Commande `kill`

Cette commande permet de déclarer l'assassinat d'un joueur.

- **Alias** : `tuer`, `murder`, `stab`
- **Arguments** : `[identifiant]` (obligatoire, identifiant du joueur à éliminer)
- **Permissions** : Rôle **[imposteur](/docs/joueur/roles#imposteur)** uniquement
- **Utilisation** :
  - `tuer PERSONNE`
- **Exemple d'utilisation** :
  - `tuer 124`
- **Exemple de retour** :
  - Quand c'est bon: 
    ```
    Le joueur Alice a bien été tué de votre part !
    ```
  - Quand le joueur n'existe pas:
    ```
    Ce joueur n\'a pas été trouvé ?! Merci de vérifier que la personne a bien donné son matricule.
    ```
  - Quand on est sous cooldown :
    ```
    Vous ne pouvez pas tuer tout de suite
    ```
      

:::note
Cette commande est réservée aux imposteurs. Utilisez-la pour éliminer discrètement vos cibles et semer la confusion parmi les membres d'équipage.
Notez bien qu'elle possède un cooldown, donc utilisez-la avec stratégie !
:::