---
id: mort
slug: /joueur/commandes/mort
sidebar_label: mort
---

# Commande `mort`

Cette commande permet de signaler la découverte d'un joueur éliminé et de déclencher une [réunion](/docs/joueur/partie#phase-reunion).

- **Alias** : `death`, `cadavre`, `corps`
- **Arguments** : `[identifiant]` (obligatoire, identifiant du joueur trouvé)
- **Utilisation** :
    - `mort PERSONNE`
- **Exemple d'utilisation** :
    - `mort 568`
- **Exemple de retour** :
    - La personne est bien morte, une réunion est déclenchée.
      ```
      Un cadavre a été signalé par Bob.
      ```
    - Si le joueur n'existe pas :
      ```
      Veuillez entrer un joueur valide !
      ```
    - Si la demande a été refusée :
      ```
      Votre demande a été refusée par l'organisateur.ice
      ```
    - Si le joueur n'est pas mort :
      ```
      Ce joueur ne peut pas être déclaré comme cadavre car il n'est pas mort
      ```

Cette commande est essentielle pour signaler un joueur éliminé et initier une [réunion](/docs/joueur/partie#phase-reunion), permettant ainsi aux autres joueurs de discuter et de [voter](/docs/joueur/commandes/vote) sur l'identité du coupable.
À utiliser dès qu'un corps est découvert pour alerter tous les joueurs.
