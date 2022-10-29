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

#### Aide
La commande aide affiche toutes les commandes disponibles au joueur
