# Les commandes par message

Ce logiciel propose des commandes pour les SMS afin de rensre le jeu plus simple à jouer.

## Côté joueur

### Utiliser une commande

Pour utiliser une commande, il suffit d'envoyer un message au maître du jeu avec la commande qui debute le message: `info`.

Si jamais la commande demande un argument, il faut mettre celui-ci juste après: `tâche 1`

Vous recevrez quelques secondes plus tard un message de retour avec les informations demandés par la commande

### La commande d'aide

Une commande regroupant toutes les autres commandes existe. Il s'agit de la commande `aide`. Une fis envoyée, elle vous donnera toutes les commandes qui sont disponibles dans le jeu

## Côté développeur

Les commandes peuvent être trouvées dans le fichier `commands.py`.

Pour créer une commande, il faut en premier lieu créer une fonction de ce que fera la commande avec comme argument `(command, player, message, game)`.
Une fois cela fait, vous pouvez créer une variable pour mettre un Objet de type `Command` à l'intérieur. Il faut évidemment donner toutes les informations nécessaires:

- `name`: le nom de la commande
- `description`: la description de ce que la commande fait
- `aliasas`: une liste d'autres noms possibles pour la commande
- `usage`: montre comment la commande s'utilise
- `exemple`: montre un exemple de l'utilisation de la commande

Vous pourrez ensuite renseigner la fonction que vous avez créé juste avant en la mettant dans a fonction `execute`:
```py
cmd.execute = cmd_func
```

Une fois tout cela fait, vous pourrez ajouter à la liste `commands` votre nouvelle commande