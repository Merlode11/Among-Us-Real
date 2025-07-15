---
id: tache
slug: /joueur/commandes/tache
sidebar_label: task
---

# Commande `task`

Cette commande permet d'obtenir des informations détaillées sur une tâche à réaliser dans le jeu.

- **Alias** : `tâche`, `détail`, `detail`, `task`, `tache`
- **Arguments** : `[numéro]` (obligatoire, numéro de la tâche)
- **Utilisation** :
    - `tâche 1`
- **Exemple d'utilisation** :
    - `tâche 2`
- **Exemple de retour** :
  ```
  Réparer l'électricité
  Lieu : Salle électrique
  Description : Remettre les fusibles en place.
  Activée : Oui
  Tâche terminée !
  ```
- **Exemple de retour pour une errur** :
  ```
    Veuillez entrer un numéro de tâche valide !
    ```

La commande `tâche` permet d'obtenir des informations détaillées sur une tâche à réaliser.

Vous recevez alors la description, le lieu et les étapes de la tâche à accomplir.
