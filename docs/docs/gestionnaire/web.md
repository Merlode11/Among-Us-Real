---
id: web
slug: /gestionnaire/web
sidebar_label: Mode Web
title: Mode de jeu Web
---

# Mode de jeu : Web

Ce mode permet de jouer à Among Us Real via une interface web accessible depuis un navigateur.

## Prérequis
- Un navigateur web moderne
- Accès au serveur hébergeant le jeu
- **Tous les joueurs doivent être connectés sur le même réseau local** (LAN) que le serveur pour accéder à l'interface web (sauf si le serveur est accessible publiquement via internet, **non supporté**)

## Configuration
- Adapter le fichier `config.json` pour activer le mode Web
- Vérifier le port utilisé (par défaut : 80) et l'adresse IP du serveur

## Fonctionnement général
- Les joueurs se connectent à l'interface web via l'adresse IP du serveur (ex : `http://192.168.1.10/`)
- Les notifications et actions de jeu sont affichées en temps réel
- Les commandes sont saisies via l'interface web
- Les permissions sont gérées automatiquement
- La communication se fait uniquement via l'interface web

## Lancement
- Lancer le serveur web avec :
```bash
python web/web_game_class.py
```
:::danger
Lancer le logiciel avec une commande comme celle-ci peut ne pas fonctionner correctement.
Veuillez toujours préférer lancer le logiciel avec le main.py 
```bash
python main.py
```
:::

## Conseils
- Vérifiez que le port utilisé n'est pas bloqué par un pare-feu
- Utilisez un navigateur à jour
- Assurez-vous que tous les joueurs sont bien sur le même réseau local

---

## Fonctionnement du fichier `web_game_class.py`

Le fichier `web_game_class.py` gère toute la logique du mode Web :

- **Serveur Flask** : Lance un serveur web local qui gère toutes les routes nécessaires au jeu (accueil, page joueur, réunion, pause, fin, API pour les actions de jeu, etc.)
- **Gestion des joueurs** :
  - Les joueurs s'inscrivent via l'interface web (choix du pseudo et de la couleur)
  - Un QR code et une URL sont générés pour faciliter la connexion des joueurs
  - Les joueurs sont ajoutés à la partie et peuvent être visualisés dans l'interface de gestion
- **Gestion des actions de jeu** :
  - Validation et activation des tâches via l'interface
  - Système de vote, réunion, signalement de mort, SOS, etc.
  - Toutes les actions sont synchronisées en temps réel entre les joueurs et l'organisateur
- **Gestion des états de partie** :
  - Pause automatique si un joueur est inactif ou en cas de SOS
  - Fin de partie gérée via l'interface
- **Sécurité et sessions** :
  - Utilisation de sessions Flask pour identifier chaque joueur
  - Gestion des erreurs et redirections selon l'état du joueur
- **Interface graphique d'importation** :
  - L'organisateur peut visualiser les joueurs connectés et démarrer la partie via une fenêtre dédiée
- **Envoi d'informations** :
  - Chaque joueur reçoit ses informations (rôle, tâches, messages) via des popups dans l'interface

Pour plus de détails techniques, consultez le code source du fichier `web/web_game_class.py`.