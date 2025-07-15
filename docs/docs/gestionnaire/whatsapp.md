---
id: whatsapp
slug: /gestionnaire/whatsapp
sidebar_label: Mode WhatsApp
title: Mode de jeu WhatsApp
---

# Mode de jeu : WhatsApp

Ce mode permet de jouer à Among Us Real via WhatsApp.

## Prérequis
- Un compte WhatsApp dédié au bot (évitez d'utiliser votre compte personnel)
- WhatsApp Web accessible
- Node.js installé (pour la gestion de l'API WhatsApp)

## Utilisation d'un compte WhatsApp pour un bot

- **Compte dédié recommandé** : Utilisez un numéro dédié pour le bot afin d'éviter tout blocage ou suspension de votre compte personnel.
- **Authentification** : Lors du premier lancement, un QR code s'affiche dans la console ou l'interface. Scannez-le avec l'application WhatsApp du téléphone associé au compte du bot.
- **Risques et limitations** :
  - WhatsApp n'autorise pas officiellement l'automatisation via des bots. L'utilisation d'API non officielles peut entraîner le bannissement du numéro utilisé.
  - N'utilisez jamais un compte principal ou important.
  - Les fonctionnalités peuvent cesser de fonctionner si WhatsApp modifie ses règles ou son API.
- **Conseil** : Prévoyez un numéro jetable ou secondaire pour le bot.

## Configuration
- Adaptez le fichier `config.json` pour activer le mode WhatsApp
- Renseignez les identifiants nécessaires dans la configuration (numéro, port, etc.)

## Fonctionnement général
- Les joueurs interagissent avec le bot via WhatsApp (messages texte)
- Les notifications et actions de jeu sont envoyées dans les discussions WhatsApp
- Les commandes sont envoyées par message texte
- Les permissions sont gérées automatiquement

## Lancement
- Lancez le script avec :
```bash
python whatsapp/whatsapp_game_class.py
```
:::danger
Lancer le logiciel avec une commande comme celle-ci peut ne pas fonctionner correctement.
Préférez toujours lancer le logiciel avec le main.py
```bash
python main.py
```
:::

## Conseils
- Utilisez un compte WhatsApp dédié pour éviter les interférences et les risques de bannissement.
- Vérifiez la connexion à WhatsApp Web et la stabilité du réseau.
- Surveillez les éventuels messages d'erreur ou de déconnexion.

## Fonctionnement du fichier `whatsapp_game_class.py`

Le fichier `whatsapp_game_class.py` gère toute la logique du mode WhatsApp :

- **Connexion et initialisation** :
  - Lance un serveur Flask pour recevoir les événements de WhatsApp (connexion, messages, QR code, etc.)
  - Démarre un processus Node.js (dans `whatsapp/api/`) pour gérer la connexion à WhatsApp Web
  - Affiche un QR code à scanner pour authentifier le bot
- **Gestion des inscriptions** :
  - Deux modes :
    - Par liste (`players.json`) : les joueurs sont pré-enregistrés
    - Par inscription directe : les joueurs s'inscrivent en envoyant un code au bot
  - L'interface graphique permet de visualiser les joueurs inscrits et de démarrer la partie
- **Réception et traitement des messages** :
  - Les messages reçus sont analysés pour détecter les commandes ou la validation/activation de tâches
  - Les réponses sont envoyées automatiquement selon le contexte (inscription, validation de tâche, etc.)
- **Gestion des tâches** :
  - Les joueurs valident ou activent leurs tâches en envoyant des mots-clés au bot
  - Le bot gère les différents types de tâches (activation, validation, etc.)
- **Gestion des déconnexions** :
  - Si WhatsApp se déconnecte, la partie est mise en pause et un message d'erreur s'affiche
- **Envoi d'informations** :
  - Le bot envoie à chaque joueur son rôle, ses tâches et des messages personnalisés
- **Synchronisation** :
  - Toutes les actions de jeu sont synchronisées entre WhatsApp et l'interface de gestion
