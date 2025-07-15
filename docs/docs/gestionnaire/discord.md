---
id: discord
slug: /gestionnaire/discord
sidebar_label: Mode Discord
title: Mode de jeu Discord
---

# Mode de jeu : Discord

Ce mode permet de jouer à Among Us Real via un serveur Discord.

## Prérequis
- Un serveur Discord pour que les joueurs puissent interagir avec le bot
- Un bot Discord configuré et ajouté au serveur
- Les droits d'administrateur sur le serveur pour ajouter le bot

## Créer un bot Discord

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/Y8RcqgmYVU8?si=_syW8pbgUNRDWiJV" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

1. Rendez-vous sur le [Portail des développeurs Discord](https://discord.com/developers/applications).
2. Cliquez sur "New Application" et donnez un nom à votre bot.
3. Allez dans l'onglet "Bot" puis cliquez sur "Add Bot".
4. Copiez le **token** du bot (à placer dans le champ `discord_token` de votre `config.json`).
5. Dans l'onglet "OAuth2 > URL Generator", sélectionnez les scopes `bot` et `applications.commands`, puis les permissions nécessaires (envoyer des messages, gérer les messages, lire l'historique, etc.).
6. Copiez l'URL générée et ouvrez-la dans votre navigateur pour inviter le bot sur votre serveur Discord.

## Configuration
- Adaptez le fichier `config.json` pour activer le mode Discord.
- Renseignez le token du bot dans la configuration (champ `discord_token`).

## Fonctionnement général
- Les joueurs interagissent avec le bot via des commandes slash Discord
- Les notifications et actions de jeu sont envoyées dans les salons Discord
- Les rôles sont attribués automatiquement

## Utilisation des commandes
- Toutes les commandes sont accessibles via `/` ou via le préfixe défini
- Les permissions sont gérées automatiquement selon le rôle du joueur

## Lancement
- Lancer le logiciel avec :
```bash
python discord_us/discord_game_class.py
```
:::danger
Lancer le logiciel avec une commande comme celle-ci peut ne pas fonctionner correctement.
Veuillez toujours préférer lancer le logiciel avec le main.py
```bash
python main.py
```
:::

## Conseils
- Vérifiez que le bot a les permissions nécessaires
- Utilisez un salon dédié pour les logs du bot

## Fonctionnalités du fichier `discord_game_class.py`

Le fichier `discord_game_class.py` gère toute la logique du mode Discord :

- **Connexion et initialisation du bot** :
  - Utilise la classe `DiscordClient` pour gérer la connexion, l'enregistrement des commandes slash et la présence du bot.
- **Gestion des commandes slash** :
  - Les commandes sont définies dans `discord_us/commands.py` et enregistrées automatiquement à chaque démarrage.
- **Inscription des joueurs** :
  - Les joueurs peuvent s'inscrire automatiquement en envoyant un code au bot en message privé (voir la fenêtre d'importation lors du lancement d'une partie).
  - Les inscriptions sont sauvegardées dans `players.json` si l'option `save_register` est activée.
- **Gestion des messages privés** :
  - Les joueurs peuvent valider ou activer leurs tâches en envoyant des mots-clés au bot.
  - Le bot répond automatiquement selon le type de tâche (activation, validation, etc.).
- **Importation des joueurs** :
  - Deux modes : par liste (`players.json`) ou par inscription directe via Discord.
  - Une interface graphique permet de visualiser les joueurs inscrits et de démarrer la partie.
- **Envoi d'informations** :
  - Le bot envoie à chaque joueur son rôle, ses tâches et des messages personnalisés.
- **Gestion de la partie** :
  - Toutes les actions de jeu (tâches, votes, informations) sont synchronisées entre Discord et l'interface de gestion.
- **Arrêt de la partie** :
  - Le bot peut être arrêté proprement, fermant la fenêtre de gestion et déconnectant le bot Discord.

:::note
Pour toute personnalisation avancée, consultez le code source du fichier `discord_game_class.py` et la documentation des commandes dans `discord_us/commands.py`.
:::

