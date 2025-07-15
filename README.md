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
LE MONDE SMS N'EST PLUS MAINTENU, VEUILLEZ UTILISER UN AUTRE MODE
#### ~~Logiciels requis~~
~~Pour utiliser le mode "sms", vous devez avoir un téléphone Android avec le service Airmore activé. Vous pouvez télécharger l'application [Airmore](https://airmore.com/fr/download) directement depuis leur site internet. Attention, pour les utilisateurs android, vous devrez télécharger le fichier APK car le logiciel n'est plus présent sur le PlayStore.~~

#### ~~Configuration~~
~~**⚠️ Votre téléphone doit être connecté au même réseau que votre ordinateur ⚠️**~~

~~Vous devez ainsi définir l'adresse IP du téléphone Airmore dans la configuration. Vous avez deux options pour cela :~~

- ~~Soit, vous définissez l'adresse IP donnée par Airmore dans le fichier `config.json` sous le nom `ip`.~~
- ~~Sinon, vous pouvez lancer le logiciel et dans la fenêtre des paramètres, vous pouvez définir l'adresse IP donnée par AirMore via le texte ou via le bouton de recherche de l'adresse IP.~~

### Mode "whatsapp"
Lorsque vous lancez le jeu, vous aurez besoin de scanner un QR code pour vous connecter à votre compte WhatsApp. Vous pourrez le faire via la page web qui s'ouvrira automatiquement.

### Mode "discord"
Ce mode vous permet de jouer à Among Us avec vos amis sur Discord. Le bot vous enverra des messages privés pour vous informer de votre rôle et des actions que vous pouvez effectuer.

#### Configuration
Pour utiliser le mode "discord", vous devez avoir un bot discord. Vous pouvez suivre [ce tutoriel](https://discordpy.readthedocs.io/en/stable/discord.html) pour créer votre bot.
[![Miniature de la création du bot](http://img.youtube.com/vi/Y8RcqgmYVU8/0.jpg)](http://www.youtube.com/watch?v=Y8RcqgmYVU8 "Miniature de la création du bot")

Une fois votre bot créé, vous devez définir le token de votre bot dans le fichier `config.json` sous le nom `discord_token`.
Vous pouvez ensuite inviter votre bot sur votre serveur discord en utilisant le lien suivant : `https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=8` en remplaçant `YOUR_CLIENT_ID` par l'ID de votre bot.

⚠️ **Veillez à ce que les joueurs soient sur le même serveur discord que le bot et qu'ils ont ouvert leur DM pour recevoir les messages du bot** ⚠️

### Mode "instagram"
Ce mode vous permet de jouer à Among Us avec vos amis sur Instagram. Le bot vous enverra des messages privés pour vous informer de votre rôle et des actions que vous pouvez effectuer.

#### Configuration
Pour utiliser le mode "instagram", vous devez avoir un compte Instagram. Vous devez définir votre nom d'utilisateur et votre mot de passe dans le fichier `config.json` sous les noms `instagram_username` et `instagram_password`.

⚠️ **Veillez à ce que les joueurs aient demandé à suivre le compte du bot pour recevoir les messages** ⚠️

Il faut faire attention à ne pas se faire bannir par Instagram en utilisant ce mode. En effet, Instagram peut considérer que l'utilisation de ce bot est une violation de leur politique d'utilisation.
Nous vous conseillons de ne pas utiliser votre compte principal pour jouer.

### Configuration de la partie
Vous avez de multiples options pour personnaliser au maximum votre partie.

#### Les nombres 
Vous pouvez définir le nombre de joueurs qui seront imposteurs, ingénieurs ou scientifique

Vous pouvez ensuite définir le nombre de tâches qui seront distribués par personnes.

Pour continuer avec les tâches, on a aussi le nombre de fois qu'une tâche peut être distribuée.

Pour le scientifique, on peut définir le nombre de fois que celui-ci peut consulter l'état de chaque joueur

#### Les noms
Vous pouvez configurer le nom de chaque rôle, pour avoir une partie avec un thème personnalisé


## Système d'urgence
Nous avons mis en place un système d'urgence en cas de problème avec un joueur. Ce mode stoppe la partie temporairement et informe les joueurs qu’une personne peut être blessé et qu'il faut aller l'aider. 
Ce mode peut être déclenché manuellement par un joueur, en indiquant son problème ou alors de manière automatique, lorsque le joueur ne donne plus signe de vie.

## Crédits
Ce projet a été entièrement créé par [Merlode11](https://github.com/Merlode11/) et a été assisté par [Lantojv](https://github.com/Lantojv) pour la partie Web.
Si vous avez des questions, des suggestions ou des problèmes, n'hésitez pas à nous contacter via les issues.
Vous pouvez aussi nous contacter sur notre compte instagram [`among.us.real`](https://www.instagram.com/among.us.real/)