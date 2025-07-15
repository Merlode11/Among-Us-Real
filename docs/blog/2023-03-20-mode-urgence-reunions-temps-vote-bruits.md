---
slug: mode-urgence-reunions-temps-vote-bruits
title: Nouveautés ! Mode d’Urgence, Réunions Améliorées et Signalétique Sonore
authors: merlode
tags: [fonctionnalité, sos, réunion, vote, son, gameplay, configuration, expérience]
date: 2023-03-20
---

## 📝 Introduction

Pour rendre vos parties Among Us IRL toujours plus immersives, **Among Us Real** introduit deux grandes nouveautés :  
- Un **mode d’urgence** accessible à tout moment pour signaler un problème ou une inactivité anormale.  
- Une **nouvelle gestion des réunions** : temps de discussion, temps de vote, commandes simplifiées… et toute une ambiance sonore pour rythmer votre enquête !

Découvrez en détail ces évolutions majeures qui enrichissent l’expérience de jeu et la rendent encore plus fidèle à l’original.
<!-- truncate -->
---

## 1️⃣ Mode d’urgence : SOS & détection d’inactivité

### ❓ Pourquoi ce mode ?

En partie IRL, tout ne se passe pas toujours comme prévu :  
- Un joueur s’est perdu ou rencontre un souci ?
- Le jeu semble bloqué parce qu’un participant ne répond plus ?
- Un problème de communication ou technique ?

Le **mode d’urgence** permet désormais de réagir rapidement, d’alerter l’organisateur et tous les autres joueurs et d’assurer la sécurité et le bon déroulement de la session.

### ⚙️ Fonctionnalités

- **Commande SOS** : Chaque joueur peut, à tout moment, envoyer la commande `sos` (ou appuyer sur le bouton “SOS” dans l’interface Web) pour signaler un problème.
- **Détection automatique d’inactivité** :  
  Détection automatique d’inactivité : 
  le logiciel surveille l’activité des joueurs : :  
  - Si un joueur ne valide aucune action pendant une période prédéfinie, une alerte est automatiquement envoyée à l’organisateur.
  - Possibilité de paramétrer la durée d’inactivité avant déclenchement automatique.
- **Journal des SOS** :  
  Toutes les alertes sont enregistrées, pour assurer un suivi et éviter les abus.

### 🛠️ Exemple de configuration

```json
{
  "min_before_inactiv_warn": 5,
  "max_warns": 3
}
```

---

## 2️⃣ Nouvelle gestion des réunions : discussion, vote, ambiance sonore

### 🗣️ Réunions : un vrai temps fort du jeu

Les réunions sont centrales dans l’expérience Among Us. Cette mise à jour les structure en plusieurs phases :

- **Phase de discussion** :  
  Un temps limité où chacun peut débattre et défendre son innocence.  
  Un compte à rebours est affiché et un son signale le début et la fin de la discussion.
- **Phase de vote** :  
  Une nouvelle commande `vote NOMBRE` permet à chaque joueur de désigner le suspect de son choix dans un temps imparti.  
  Un signal sonore marque le début et la fin de la phase de vote.
- **Résultats** :  
  L’annonce des résultats est accompagnée d’un son dédié pour dramatiser le moment.

### 🕹️ Commandes associées et exemples d’utilisation

- **Démarrer une réunion** :  
  `mort PERSONNE` ou bouton “Réunion”.
- **Voter (joueur)** :  
  `vote NOMBRE`.

### 🔔 Signalétique sonore

- Début de réunion : son spécifique (ex : gong).
- Début de discussion : bip long.
- Fin de discussion : double bip.
- Début du vote : alerte sonore courte.
- Fin du vote : son dramatique.
- Affichage des résultats : jingle.

### ⚙️ Personnalisation

- Durée discussion/vote paramétrable dans la configuration (ex : 60s discussion, 30s vote).
- Possibilité de désactiver/activer les sons selon le contexte de jeu.

```json
{
  "discussion_time": 120,
  "vote_time": 30
}
```

---

## 3️⃣ Bénéfices & expérience utilisateur

- **Réactivité et sécurité** : mode SOS rassurant pour tous les joueurs.
- **Immersion** : les réunions sont rythmées et plus proches de la version numérique du jeu.
- **Simplicité** : commandes claires, interface épurée.
- **Adaptabilité** : tout est paramétrable pour coller à votre style de jeu et à vos contraintes.

---

## 4️⃣ Conseils d’utilisation

- Expliquez aux joueurs l’existence de la commande SOS avant chaque partie.
- Prévoyez un appareil (téléphone, tablette, ordi) avec le son activé pour profiter pleinement de l’ambiance.
- Adaptez les temps de réunion selon le nombre de participants pour garder un bon rythme.

---

## ✅ Conclusion

Cette mise à jour assure des parties plus sûres, plus immersives et mieux organisées.  
Essayez dès maintenant le mode d’urgence et les nouvelles réunions : la tension monte, l’ambiance sonore vous plonge au cœur du jeu… et personne ne sera laissé de côté en cas de soucis !

N’hésitez pas à faire vos retours ou à demander de nouvelles fonctionnalités via le [GitHub du projet](https://github.com/Merlode11/Among-Us-Real).