# Les commandes par message

Ce logiciel propose des commandes utilisant les SMS afin de rendre le jeu plus simple à jouer.

## Côté joueur

### Utiliser une commande

Pour utiliser une commande, il suffit d'envoyer un message au maître du jeu avec la commande qui debute le message: `info`.

Si jamais la commande demande un argument, il faut mettre celui-ci juste après: `tâche 1`

Vous recevrez quelques secondes plus tard un message de retour avec les informations demandés par la commande

### La commande d'aide

Une commande regroupant toutes les autres commandes existe. Il s'agit de la commande `aide`. Une fois envoyée, elle vous donnera toutes les commandes qui sont disponibles dans le jeu

## Côté développeur

Les commandes peuvent être trouvées dans le fichier `commands.py`.

Pour créer une commande, il faut créer une nouvelle classe du type `NomCommand` en héritage à la class command. 
En l'instanciant la commande, il faut mettre ses paramètres suivant:

- `name`: le nom de la commande
- `description`: la description de ce que la commande fait
- `aliasas`: une liste d'autres noms possibles pour la commande
- `usage`: montre comment la commande s'utilise
- `exemple`: montre un exemple de l'utilisation de la commande

Vous pouvez ainsi ajouter la méthode `execute` avec ce que fait la commande.

Une fois tout cela fait, vous pourrez ajouter à la liste `commands` la classe instanciée (`commands.append(NomCommand())`)


## Les commandes disponibles de base

#### Aide (COMMANDE)
`aide (COMMANDE)` (*ex: `aide`, `aide tâche`*)


La commande aide affiche toutes les commandes disponibles au joueur. On peut obtenir de l'aide pour une commande spécifique en spécifiant la commande après: `aide COMMANDE`


#### Tâche NUMERO
`tâche NUMERO` (*ex: `tâche 1`*)


Apporte plus d'informations sur une tâche que le joueur doit effectuer. Cette commande fourni le **titre**, le **lieu** où réaliser la tâche, la **description** de la tâche, dans le cas où on doit activer au préalable la tâche: si jamais elle a été **activée** ou non, et si jamais la tâche a été effectuée ou non.


#### Info
`info` (*ex: `info`*)


Indique les tâches restantes au joueur. Cette commande donne également l'identifiant du joueur, utilisé pour tout ce qui est assassinat et signalement de corps.


#### Morts
`morts` (*ex: `morts`*)

Cette commande est uniquement disponible pour le rôle **Scientifique** !

Elle donne la liste des joueurs et leur état, donc soit mort, ou vivant. Ceci est semblable a la tablette des scientifiques



#### Mort IDENTIFIANT
`mort IDENTITIANT` (*ex: `MORT 123`*)

Indique au jeu que l'on a découvert un joueur assassiné par un imposteur. Ceci va déclencher une réunion qui va convoquer tous les joueurs au point de rendez-vous


#### Fait TÂCHE
`fait tâche` (*ex: `fait 1`*)

Valide une tâche pour le jeu. Une fois que toutes les tâches ont été réalisées, l'équipage aura gagné


#### Sos (LOCALISATION MESSAGE)
`sos (LOCALISATION MESSAGE)` (*ex: `sos maison problème de jambe`*)

Envoie un message de demande d'assistance à tous les joueurs en cas d'urgence. Lorsque cette commande est déclenchée, la partie est mise en pause, tous les joueurs sont prévenus et viendront aider la personne


#### Tuer IDENTIFIANT
`tuer IDENTIFIANT` (*ex: `tuer 123`*)

Cette commande est uniquement disponible pour le rôle **Imposteurs** !

Permet de montrer que l'on a tué une personne au jeu. Il faut indiquer l'identifiant du joueur que l'on a tué: c'est le joueur qui le donne son identifiant au moment où l'imposteur le tue.


#### Vote CODE
`vote CODE` (*ex: `vote 1`, `vote skip`*)

Enregistre le vote du joueur pour la fin des délibérations. Une fois que tous les joueurs ont voté, l'option la plus choisie sera montrée. On peut choisir soit le numéro d'un joueur qui sera affiché, et que l'on pourra voter, ou alors, choisir de passer ce vote.
