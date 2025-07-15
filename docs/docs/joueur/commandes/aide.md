---
id: aide
slug: /joueur/commandes/aide
sidebar_label: help
---

# Commande `help`

Cette commande permet d'obtenir de l'aide sur les commandes disponibles dans le jeu, ainsi que des informations détaillées sur une commande spécifique.

- **Alias** : `aide`, `commandes`, `commande`, `command`, `commands`
- **Arguments** : `[commande]` (optionnel, nom d'une commande)
- **Utilisation** :
  - `aide` : affiche toutes les commandes disponibles
  - `aide tache` : affiche l'aide détaillée pour la commande `tache`
- **Exemple d'utilisation** :
  - `aide`
  - `aide vote`
- **Exemple de retour** :
  - Pour `aide` :
    ```
    Voici toutes les commandes disponibles:
    task NOMBRE: Permet de voir la description d'une tâche
    info Permet de voir les tâches restantes
    deads Voir les états de chaque joueur
    mort PERSONNE: Annonce à l'organisateur la découverte d'un corps
    done NOMBRE: Valide une tâche comme faite
    help (COMMANDE): Obtenir toutes les commandes et de l'aide pour chacune
    sos (LOCALISATION - MESSAGE): Commande d'URGENCE pour signaler que vous avez un problème
    kill PERSONNE: Tuer une personne, si elle est à côté de vous
    vote PERSONNE: Voter pour une personne durant les phases de meeting
    ```
  - Pour `aide tache` :
    ```
    Voici la page d'aide pour la commande [task](/docs/joueur/commandes/tache):
    Permet de voir la description d'une tâche
    Alias: tâche, détail, detail, task, tache
    Utilisation: task NOMBRE (exemple: task 1)
    ```

La commande `aide` permet d'obtenir la liste des commandes ou des informations détaillées sur une commande spécifique.
