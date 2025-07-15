---
id: sms
slug: /gestionnaire/sms
sidebar_label: Mode SMS
title: Mode de jeu SMS
---

# Mode de jeu : SMS

Ce mode permet de jouer à Among Us Real via SMS, en utilisant un téléphone Android comme passerelle grâce à l'application **Android SMS Gateway**.

## Prérequis
- Un téléphone Android compatible
- L'application [Android SMS Gateway](https://github.com/capcom6/android-sms-gateway) installée sur le téléphone (voir ci-dessous)
- Le téléphone connecté au même réseau que l'ordinateur
- Le module Python `android_sms_gateway` installé (voir ci-dessous)

## Installation et configuration de Android SMS Gateway

L'application [Android SMS Gateway](https://github.com/capcom6/android-sms-gateway) permet de transformer un téléphone Android en passerelle SMS accessible via une API locale ou cloud.

### Installation de l'application sur le téléphone
1. Rendez-vous sur la page [Releases du projet](https://github.com/capcom6/android-sms-gateway/releases) et téléchargez la dernière version de l'APK.
2. Transférez l'APK sur votre téléphone Android et installez-le (vous devrez peut-être autoriser l'installation d'applications depuis des sources inconnues).
3. Ouvrez l'application et activez le **Local Server**. (Vous pouvez également activer le **Cloud Server** si vous souhaitez y accéder depuis l'extérieur de votre réseau local, mais cela nécessite une configuration supplémentaire et n'est pas recommandé pour les parties locales.)
4. Notez l'adresse IP locale (ou l'URL de l'API), le port, le nom d'utilisateur et le mot de passe affichés dans l'application.

Pour plus de détails, consultez la [documentation officielle](https://docs.sms-gate.app/).


### Configuration
1. Connectez le téléphone au même réseau Wi-Fi que l'ordinateur.
2. Renseignez l'IP, le port, le nom d'utilisateur et le mot de passe dans le fichier `config.json` :
   ```json
   {
     "ip": "192.168.1.XX",
     "port": 8080,
     "sms_username": "admin",
     "sms_password": "votre_mot_de_passe"
   }
   ```
3. Vérifiez que le port n'est pas bloqué par un pare-feu.

## Formalités et précautions
- **Forfait SMS** : Prévoyez un forfait SMS suffisant pour le téléphone utilisé.
- **Vie privée** : Utilisez de préférence un téléphone dédié pour éviter de mélanger messages personnels et messages de jeu.
- **Connexion réseau** : Le téléphone et l'ordinateur doivent rester connectés au même réseau pendant toute la partie.

## Fonctionnement général
- Les joueurs envoient des SMS à un numéro dédié (celui du téléphone Android utilisé).
- Les réponses et notifications sont envoyées par SMS.
- Les commandes sont envoyées par SMS sous la forme : `commande arguments`.
- Les permissions sont gérées par le système.
- La communication se fait exclusivement par SMS.

## Lancement
- Lancer le script avec :
```bash
python sms/sms_game_class.py
```
:::danger
Lancer le logiciel avec une commande comme celle-ci peut ne pas fonctionner correctement.
Veuillez toujours préférer lancer le logiciel avec le main.py 
```bash
python main.py
```
:::

## Conseils
- Vérifiez la connexion entre le téléphone et l'ordinateur
- Prévoyez un forfait SMS suffisant
- Utilisez un téléphone dédié pour éviter les interférences
- Surveillez les éventuels messages d'erreur ou de déconnexion


## Fonctionnement du fichier `sms_game_class.py`

Le fichier `sms_game_class.py` gère toute la logique du mode SMS :

- **Serveur Flask** :
  - Lance un serveur local pour recevoir les messages entrants du téléphone via un webhook.
  - Analyse chaque message reçu pour gérer l'inscription, les commandes ou la validation/activation de tâches.
- **Gestion des inscriptions** :
  - Les joueurs peuvent s'inscrire automatiquement en envoyant un code d'inscription par SMS.
  - Les nouveaux joueurs sont ajoutés à la partie et, si l'option `save_register` est activée, enregistrés dans `players.json`.
- **Gestion des commandes** :
  - Les commandes sont analysées et exécutées (validation de tâche, activation, etc.).
  - Les commandes sont définies dans `sms/commands.py`.
- **Envoi d'informations** :
  - Le bot envoie à chaque joueur son rôle, ses tâches et des messages personnalisés par SMS.
- **Gestion des tâches** :
  - Les joueurs valident ou activent leurs tâches en envoyant des mots-clés par SMS.
  - Le bot gère les différents types de tâches (activation, validation, etc.).
- **Gestion de la partie** :
  - Toutes les actions de jeu (tâches, votes, informations) sont synchronisées entre les SMS et l'interface de gestion.
- **Arrêt de la partie** :
  - Le serveur Flask et le webhook sont arrêtés proprement à la fin de la partie.
