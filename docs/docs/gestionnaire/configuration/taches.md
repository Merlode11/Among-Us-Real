---
id: taches
slug: /gestionnaire/configuration/taches
sidebar_label: Gestion des tâches
---

# Gestion des tâches

Une **tâche** est une action ou un mini-jeu à réaliser par les joueurs pendant la partie. Les tâches sont au cœur du gameplay et permettent de rythmer la partie, d'équilibrer les rôles et de donner des objectifs variés aux participants.

## Qu'est-ce qu'une tâche ? {#what-is-a-task}

Chaque tâche possède plusieurs caractéristiques :

- **Nom** : le titre de la tâche, visible par les joueurs.
- **Description** : explication de ce que doit faire le joueur.
- **Emplacement** : lieu physique ou virtuel où la tâche doit être réalisée (peut être un lien, une salle, etc.).
- **[Type](#task-types)** : détermine le mode de validation ou d'activation de la tâche (voir ci-dessous).
- **Étapes** : nombre d'étapes nécessaires pour valider la tâche.
- **Mots-clés** : (optionnel) mots à fournir pour valider la tâche.
- **Mots-clés d'activation** : (optionnel) mots à fournir pour activer la tâche.
- **Message d'activation** : (optionnel) message envoyé lors de l'activation de la tâche

> _Exemple de structure JSON d'une tâche :_
> ```json
> {
>   "name": "Histoire de la France",
>   "location": "Dans la ruelle principale",
>   "description": "Répondez à la question sur la Révolution Française.",
>   "type": "activ_valid",
>   "steps": 1,
>   "activ_keywords": ["histoire"],
>   "keywords": ["qcm2"],
>   "message": "Quelle est la date de la fête de la fédération ?"
> }
> ```

### Les différents types de tâches {#task-types}

- **Basique** : tâche simple, validée par l'organisateur.
- **Avec validation** : le joueur doit fournir un mot-clé pour valider.
- **Avec activation** : la tâche s'active avec un mot-clé, puis se valide.
- **Avec activation et validation** : nécessite un mot-clé d'activation puis un mot-clé de validation

## Les listes de tâches

Les tâches sont organisées en **listes** (fichiers `.json` dans le dossier `taskList`). Chaque partie peut utiliser une liste différente, adaptée au contexte (scolaire, entreprise, etc.).

- Pour changer de liste, utilisez l'interface de gestion ou modifiez la configuration.
- Vous pouvez créer, renommer ou supprimer des listes selon vos besoins.

## Ajouter ou modifier des tâches

### 1. Modification directe du fichier JSON

Vous pouvez éditer les fichiers `.json` dans le dossier `taskList` avec un éditeur de texte. Ajoutez, modifiez ou supprimez des objets représentant les tâches.

### 2. Utilisation de l'interface graphique

Lancez le fichier `task_config.py` pour ouvrir l'interface de gestion des tâches. Vous pourrez :
- Créer une nouvelle tâche.
- Modifier ou supprimer une tâche existante.
- Gérer les listes de tâches.

L'interface guide l'utilisateur et évite les erreurs de format.

[//]: # (![Illustration interface graphique]&#40;./img/taches-interface.png&#41;)

:::tip
- Privilégiez l'interface graphique pour éviter les erreurs de syntaxe.
- Testez vos listes avant de lancer une partie réelle.
- Adaptez les tâches à votre public pour plus de fun et d'équilibre
:::
