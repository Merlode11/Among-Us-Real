# Among-US-Real
Jouez avec vos amis à un Among Us dans la vie réelle avec ce logiciel fait pour !

## Installation

Ce projet utilise [Python 3.9.13](https://www.python.org/downloads/release/python-3913/) principalement avec plusieurs modules tel que [PyAirmore](https://pyairmore.readthedocs.io/en/master/), [Flask](https://flask.palletsprojects.com/en/2.2.x/), et [playsound](https://pypi.org/project/playsound/).

Pour installer les modules, vous pouvez utiliser la commande suivante :

```bash
pip install -r requirements.txt
```

## Utilisation

Vous avez deux options de jeux avec ce logiciel : le mode "web" et le mode "sms".

### Mode "web"

*En construction*

### Mode "sms"

#### Logiciels requis
Pour utiliser le mode "sms", vous devez avoir un téléphone Android avec le service Airmore activé. Vous pouvez télécharger l'application [Airmore](https://airmore.com/fr/download) directement depuis leur site internet. Attention, pour les utilisateurs android, vous devrez télécharger le fichier APK car le logiciel n'est plus présent sur le PlayStore.

#### Configuration
**⚠️ Votre téléphone doit être connecté au même réseau que votre ordinateur ⚠️**

Vous devez ainsi définir l'adresse IP du téléphone Airmore dans la configuration. Vous avez deux options pour cela :

- Soit, vous définissez l'adresse IP donnée par Airmore dans le fichier `config.json` sous le nom `ip`.
- Sinon, vous pouvez lancer le logiciel et dans la fenêtre des paramètres, vous pouvez définir l'adresse IP donnée par AirMore via le texte ou via le bouton de recherche de l'adresse IP.

### Configuration de la partie
Vous avez de multiples options pour personnaliser au maximum votre partie.

#### Les nombres 
Vous pouvez définir le nombre de joueurs qui seront imposteurs, ingénieurs ou scientifique

Vous pouvez ensuite définir le nombre de tâches qui seront distribués par personnes.

Pour continuer avec les tâches, on a aussi le nombre de fois qu'une tâche peut-être distribuée.

Pour le scientifique, on peut définir le nombre de fois que celui-ci peut consulter l'état de chaque joueur

#### Les noms
Vous pouvez configurer le nom de chaque rôle, pour avoir une partie avec un thème personnalisé


## Système d'urgence
Nous avons mis en place un système d'urgence en cas de problème avec un joueur. Ce mode stoppe la partie temporairement et informe les joueurs qu’une personne peut-être blessé et qu'il faut aller l'aider. 
Ce mode peut-être déclenché manuellement par un joueur, en indiquant son problème ou alors de manière automatique, lorsque le joueur ne donne plus signe de vie.
