# Déroulement d'une partie par SMS

## Initialisation 
Pour commencer, avant de démarrer une partie, il faut enregistrer les joueurs qui vont participer au jeu.

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
Une fois la partie lancée, chaque joueur reçoit un SMS lui indiquant son rôle, et dans le cas où il est imposteur, ses coéquipiers, les tâches qu'il doit réaliser, son code joueur. Il y a une petite indication par rapport à la commande `aide` qui lui servira à avoir des informations sur les commandes.


### Faire des tâches
La liste des tâches est envoyée en premier lieu dans le message de début de partie. Mais les tâches restantes sont accessibles à tout moment avec la commande `tâches`. Il y a différents types de tâches, qui possèdent leurs propres règles de validation.

#### La basique
La tâche basique est très simple: on se rend sur le lieu de la tâche, on la réalise, et pour la valider, il faut faire la commande `fait TÂCHE` pour enregistrer la tâche comme faite pour l'ordinateur.

#### La validation
Cette tâche avec validation demande de faire la tâche, et pour la valider, il faut mettre le mot donné en fin de tâche dans un SMS et l'envoyer. Si jamais ce mot est correct, la tâche sera validée.

#### L'activation
Une tâche avec activation demande d'envoyer un mot par SMS. Si ce mot est correct, alors on reçoit les informations enregistrées dans la tâche. C'est seulement après que l'on peut faire la tâche et la valider avec la commande `fait TÂCHE` par SMS.

#### La combinée
Ce type de tâche est une combinaison des deux types précédents. La tâche demande d'être activée en envoyant un mot par SMS. Une fois les consignes reçues en retour, il faut envoyer un autre mot par SMS pour valider celle-ci.


### Tuer une personne
Pour tuer une personne, les imposteurs doivent en premier lieu demander à la personne tuée son identifiant (*donné en début de partie et accessible à tout moment avec la commande `info`*). Une fois cette information demandée, l'imposteur peut faire la commande `tuer IDENTIFIANT` pour signaler au jeu que ce joueur a été tué.

### Les réunions
Les réunions sont des moments où tous les joueurs se retrouvent pour discuter et voter pour un joueur à éliminer. Pour lancer une réunion, il faut soit déclarer un joueur mort comme trouvé avec la commande `mort IDENTIFIANT`, soit cliquer sur le bouton **Réunion** sur le logiciel. Une fois la réunion lancée, les joueurs doivent se rassembler autour de l'ordinateur avec le logiciel. Ils doivent indiquer leur présence en entrant un code sur la fenêtre prévue à cet effet. Une fois tout le monde arrivé, la phase de discussion se lance. Une fois le timer terminé, c'est la phase de vote qui arrive. Pour voter, il faut faire la commande `vote IDENTIFIANT` par SMS pour voter pour le joueur dont l'identifiant est donné. Il y a la possibilité de passer le vote en indiquant `vote passer`. Une fois le temps écoulé, le joueur ayant le plus de votes est éliminé. En cas d'égalité ou qu'un grand nombre de personnes vote pour passer, personne n'est éliminé. 

### La victoire
La victoire est déclarée lorsque tous les imposteurs sont éliminés, ou lorsque tous les joueurs sont éliminés. Dans le premier cas, les imposteurs gagnent, dans le second cas, les joueurs gagnent. Les joueurs peuvent également gagner en faisant toutes les tâches.
