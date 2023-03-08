# Déroulement d'une partie par SMS

## Initialisation 
Pour commencer, avant de démarrer une partie, il faut enregistrer les joueurs qui vont participer au jeux.

### Les joueurs
Les joueurs peuvent donc être enregistrés depuis la page d'accueil du jeu, en cliquant sur le bouton **Modifier**.
Une fois sur cette fenêtre, on peut ajouter à souhait les joueurs qui vont participer, avec leur nom, leur prénom et leur **numéro de téléphone**.

### Les tâches 
Vous devez configurer quelques tâches pour pouvoir correctement jouer au jeu. Vous avez une page dédiée à la configuration des tâches:

[Configurer les tâches](config-task.md "Accéder à l'information sur la configuration des tâches")

### Le maître du jeu
Vous pouvez définir si jamais vous souhaitez un maître du jeu dans la partie ou pas. Ce maître du jeu devra rester sur place, à gérer toute l'équipe de joueurs et les différents aléas.


## La partie

### Le lancement
Une fois la partie lancée, chanque joueur reçoit un SMS lui indiquant son rôle, et dans le cas où il est imposteur, ses coéquipiers, les tâches qu'il doit réaliser, son code joueur. Il y a une petite indication par rapport à la commande `aide` qui lui servira à avoir des informations sur les commandes.


### Faire des tâche
La liste des tâches est envoyée en premier lieu dans le message de début de partie. Mais les tâches restantes sont accessibles à tout moment avec la commande `tâches`. Il y a différents types de tâches, qui possèdent leur propres règles de validation.

#### La basique
La tâches basique est très simple: on se rend sur le lieu de la tâche, on la réalise, et pour la valider, il faut faire la commande `fait TÂCHE` pour enregistrer la tâche comme faite pour l'ordinateur.

#### La validation
Cette tâche avec validation demande de faire la tâche, et pour la valider, il faut mettre le mot donné en fin de tâche dans un SMS et l'envoyer. Si jamais ce mot est correct, la tâche sera validée.

#### L'activation
Un tâche avec activation demande d'envoyer un mot par SMS. Si ce mot est correct, alors on reçoit les informations enregistrés dans la tâche. C'est seulement après que l'on peut faire la tâche et la valider avec la commande `fait TÂCHE` par SMS.

#### La combinée
Ce type de tâche est une combinaison des deux types précédents. La tache demande d'être activée en envoyant un mot par SMS. Une fois les consignes reçues en retour, il faut envoyer un autre mot par SMS pour valider celle-ci.


### Tuer une personne
Pour tuer une personne, les imposteurs doivent en premier lieu demander à la personne tuée son identifiant (*donné en début de partie et accessible à tout moment avec la commande `info`*). Une fois cette information demandée, l'imposteur peut faire la commande `tuer IDENTIFIANT` pour signaler au jeu que ce joueur a été tué.