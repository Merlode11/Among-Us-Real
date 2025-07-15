---
id: parametres
slug: /gestionnaire/configuration/parametres
sidebar_label: Paramètres avancés
---

# Paramètres avancés

Les paramètres permettent de personnaliser en profondeur le déroulement d'une partie. Ils influencent les règles, la difficulté, l'équilibre et l'expérience de jeu.

## Principaux paramètres modifiables

- **Nombre d'imposteurs** (`impostors`) : nombre de joueurs ayant le rôle d'imposteur.
- **Nombre d'ingénieurs** (`engineers`) : nombre de joueurs pouvant réparer instantanément.
- **Nombre de scientifiques** (`scientists`) : nombre de joueurs pouvant vérifier l'état des autres.
- **Nombre de tâches par joueur** (`tasks`) : nombre de tâches attribuées à chaque joueur.
- **Nombre maximum de distributions d'une tâche** (`max_task_given`) : limite de répartition d'une même tâche.
- **Noms personnalisés des rôles** (`names`) : personnalisez les noms affichés pour chaque rôle.
- **Nombre de consultations pour le scientifique** (`max_dead_check`) : nombre de vérifications autorisées.
- **Présence d'un maître du jeu** (`game_master`) : active ou non la supervision par un organisateur.
- **Affichage des rôles après la mort** (`show_dead_roles`) : indique si le rôle d'un joueur est révélé à sa mort.
- **Temps de discussion** (`discussion_time`) : durée des phases de discussion (en secondes).
- **Temps de vote** (`vote_time`) : durée des phases de vote (en secondes).
- **Temps entre deux assassinats** (`kill_cooldown`) : délai minimum entre deux éliminations (en secondes).
- **Liste de tâches utilisée** (`task_list`) : nom du fichier de tâches à utiliser (dans le dossier `taskList`).
- **Gestion des avertissements d'inactivité** (`min_before_inactiv_warn`, `max_warns`) : délai avant avertissement et nombre maximal d'avertissements.
- **Type de gestion des joueurs** (`manager_type`) : mode de gestion (sms, web, whatsapp, instagram, discord, telegram).
- **Type d'inscription des joueurs** (`register_type`) : inscription par liste ou directe.
- **Enregistrement automatique des inscriptions** (`save_register`) : conserve ou non les inscriptions pour les prochaines parties.
- **Paramètres spécifiques aux modes** :
    - **IP et port** pour SMS-gateway
    - **Identifiants et tokens** pour Discord, Telegram, Instagram, WhatsApp

Pour plus de détails, consultez le fichier `config.json` ou l'interface de configuration.

## Deux modes de modification des paramètres

### 1. Par l'interface graphique

Lancez le fichier `config_settings.py` pour ouvrir une fenêtre conviviale permettant de modifier tous les paramètres sans risque d'erreur de format. L'interface propose :
- Des champs pour chaque paramètre
- Des menus déroulants pour les choix
- Des boutons pour enregistrer ou réinitialiser
- Des contrôles de validité (ex : vérification d'adresse IP, de tokens, etc.)

[//]: # (> ![Illustration interface paramètres]&#40;/img/parametres-interface.png&#41;)

### 2. Par le fichier `config.json`

Vous pouvez éditer directement le fichier `config.json` à la racine du projet avec un éditeur de texte. Chaque paramètre correspond à une clé du fichier. Attention à respecter la structure JSON !

:::tip
Utilisez l'interface graphique pour éviter les erreurs de syntaxe ou de type. Modifiez le fichier JSON uniquement si vous êtes à l'aise avec ce format.
:::
