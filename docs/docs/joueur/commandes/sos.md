---
id: sos
slug: /joueur/commandes/sos
sidebar_label: sos
---

# Commande `sos`

La commande `sos` permet d'envoyer un message d'urgence à tous les joueurs et de mettre la partie en pause. La partie ne reprendra que lorsque l'utilisateur aura entré le code reçu dans le message d'urgence.

- **Alias** : `urgence`, `problème`, `prob`, `problem`
- **Arguments** : `[localisation] [message]` (obligatoire)
- **Utilisation** :
  - `sos [localisation] [message]`
- **Exemple d'utilisation** :
  - `sos maison problème de jambe`
- **Exemples de retour** :
  - Confirmation d'envoi :
    ```
    Votre demande d'aide a bien été transmise aux autres joueurs. Le code pour rétablir la partie normalement est '1234'.
    ```
  - Message reçu par les autres joueurs :
    ```
    Bob a besoin d'aide en URGENCE ! Son message :
      maison problème de jambe
    ```

:::danger
Cette commande est réservée aux situations d'urgence. Utilisez-la uniquement si vous avez un problème réel qui nécessite l'attention de tous les joueurs.
:::
