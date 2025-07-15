---
id: vote
slug: /joueur/commandes/vote
sidebar_label: vote
---

# Commande `vote`

Cette commande permet d'enregistrer votre vote lors des délibérations.

- **Alias** : `vote`, `voter`, `voté`, `votée`, `votés`
- **Arguments** : `[PERSONNE]` (obligatoire, code ou identifiant du joueur à éliminer)
- **Utilisation** :
  - `vote PERSONNE`
- **Exemple d'utilisation** :
  - `vote 1`
- **Exemple de retour** :
  ```
  Vous avez voté contre Bob !
  ```

:::note
Cette commande est uniquement disponible pendant les réunions. Vous ne pouvez pas voter en dehors de ces moments.
:::