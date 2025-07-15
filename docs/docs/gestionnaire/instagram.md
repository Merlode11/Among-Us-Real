---
id: instagram
slug: /gestionnaire/instagram
sidebar_label: Mode Instagram
title: Mode de jeu Instagram
---

# Mode de jeu : Instagram

Ce mode permet de jouer à Among Us Real via Instagram (messages privés).

## Prérequis
- Un compte Instagram dédié au bot (évitez d'utiliser votre compte personnel)
- Accès à l'API Instagram (ou un wrapper compatible)

## Utilisation d'un compte Instagram pour un bot

- **Compte dédié recommandé** : Utilisez un compte Instagram distinct pour le bot afin d'éviter tout blocage ou suspension de votre compte principal.
- **Authentification** : Lors de la première utilisation, il peut être nécessaire de valider l'accès au compte (code de sécurité, vérification par mail ou téléphone, etc.).

:::danger[**Risques et limitations** :]
  - Instagram n'autorise pas officiellement l'automatisation via des bots. L'utilisation d'API non officielles ou de wrappers peut entraîner la désactivation temporaire ou définitive du compte.
  - Il est fréquent que le compte soit temporairement bloqué ou nécessite une vérification manuelle (parfois plusieurs jours). **Testez toujours le compte bien en avance** pour éviter les mauvaises surprises le jour de l'événement.
  - Ne jamais utiliser un compte principal ou important.
  - Les fonctionnalités peuvent cesser de fonctionner si Instagram modifie ses règles ou son API.
:::
:::tip
Prévoyez un compte jetable ou secondaire pour le bot, et effectuez des tests plusieurs jours avant l'événement.
:::

## Configuration
- Adapter le fichier `config.json` pour activer le mode Instagram
- Renseigner les identifiants nécessaires dans la configuration

## Fonctionnement général
- Les joueurs interagissent avec le bot via messages privés Instagram
- Les notifications et actions de jeu sont envoyées par DM
- Les commandes sont envoyées par message texte
- Les permissions sont gérées automatiquement

## Fonctionnement du fichier `instagram_game_class.py`

Le fichier `instagram_game_class.py` gère toute la logique du mode Instagram :

- **Connexion et initialisation** :
  - Utilise des fonctions pour envoyer et recevoir des messages via l'API ou le wrapper Instagram
  - Démarre un thread pour vérifier périodiquement les nouveaux messages reçus
- **Gestion des inscriptions** :
  - Deux modes :
    - Par liste (`players.json`) : les joueurs sont pré-enregistrés
    - Par inscription directe : les joueurs s'inscrivent en envoyant un code au bot (affiché dans la fenêtre d'importation)
  - L'interface graphique permet de visualiser les joueurs inscrits et de démarrer la partie
- **Réception et traitement des messages** :
  - Les messages reçus sont analysés pour détecter les commandes ou la validation/activation de tâches
  - Les réponses sont envoyées automatiquement selon le contexte (inscription, validation de tâche, etc.)
- **Gestion des tâches** :
  - Les joueurs valident ou activent leurs tâches en envoyant des mots-clés au bot
  - Le bot gère les différents types de tâches (activation, validation, etc.)
- **Gestion des déconnexions** :
  - Si Instagram se déconnecte ou bloque le compte, la partie est mise en pause et un message d'erreur s'affiche
- **Envoi d'informations** :
  - Le bot envoie à chaque joueur son rôle, ses tâches et des messages personnalisés
- **Synchronisation** :
  - Toutes les actions de jeu sont synchronisées entre Instagram et l'interface de gestion

## Lancement
- Lancer le script avec :
```bash
python instagram/instagram_game_class.py
```
:::danger
Lancer le logiciel avec une commande comme celle-ci peut ne pas fonctionner correctement.
Veuillez toujours préférer lancer le logiciel avec le main.py 
```bash
python main.py
```
:::

## Conseils
- Utilisez un compte Instagram dédié pour éviter les interférences et les risques de blocage
- Testez le compte plusieurs jours avant l'événement pour anticiper d'éventuels blocages ou vérifications
- Vérifiez la connexion à l'API Instagram et la stabilité du réseau
- Surveillez les éventuels messages d'erreur ou de déconnexion
