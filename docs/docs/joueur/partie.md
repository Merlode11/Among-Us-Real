---
id: partie
slug: /joueur/partie
sidebar_label: Déroulement d'une partie
---

# Déroulement d'une partie

Dans Among Us Real, une partie se déroule en plusieurs phases distinctes, chacune avec ses propres règles et enjeux. Voici le détail de chaque phase, les conditions de victoire et de défaite, et les conseils pour bien jouer !

## Phases du jeu {#phases-jeu}

### 1. Préparation {#phase-preparation}
- Les joueurs s'inscrivent et rejoignent la partie. 
- Le [maître du jeu](/docs/joueur/roles#maitre-du-jeu) configure les paramètres (nombre d'[imposteurs](/docs/joueur/roles#imposteur), rôles spéciaux, etc).
- Une fois que tous les joueurs sont prêts, la partie commence. Les rôles ([Innocents](/docs/joueur/roles#innocent), [Imposteurs](/docs/joueur/roles#imposteur), [Scientifique](/docs/joueur/roles#scientifique), etc.) et différentes les tâches sont attribués aléatoirement.

### 2. Phase de jeu libre {#phase-libre}
- Les joueurs accomplissent leurs tâches ou, pour les [imposteurs](/docs/joueur/roles#imposteur), tentent de saboter et d'éliminer discrètement les autres.
- Les discussions sont interdites sauf si une réunion est déclenchée.

### 3. Découverte d'un corps ou demande {#phase-decouverte}
- Lorsqu'un joueur découvre un corps ou vient faire sa demande de réunion, une réunion est déclenchée.

### 4. Les réunions : déroulement et interactions {#phase-reunion}

Les réunions sont des moments clés dans Among Us Real, déclenchées lorsqu'un joueur découvre un corps ou fait une demande de réunion. Elles permettent aux joueurs d'échanger, de débattre et de [voter](/docs/joueur/commandes/vote) pour éliminer un suspect. Voici le détail des phases et des interactions possibles lors d'une réunion :

#### Déclenchement d'une réunion {#reunion-declenchement}
- Un joueur signale un corps ([mort](/docs/joueur/commandes/mort)) ou viennent au lieu de réunion pour demander une réunion.
- Tous les joueurs sont informés et la partie est mise en pause.

#### Phase de discussion {#reunion-discussion}
- Tous les joueurs peuvent discuter librement, en présentiel.
- Chacun peut donner son avis, accuser, se défendre ou partager des informations.
- Les [imposteurs](/docs/joueur/roles#imposteur) peuvent mentir ou manipuler les débats.

#### Phase de vote {#reunion-vote}
- Chaque joueur [vote](/docs/joueur/commandes/vote) pour éliminer un suspect (`vote [identifiant]`).
- Il est possible de [voter](/docs/joueur/commandes/vote) pour "personne" si l'on ne souhaite éliminer personne. On dit alors qu'on "passe" ou qu'on "skip".
- Les votes sont secrets jusqu'à la révélation des résultats.

#### Résultat du vote {#reunion-resultat}
- Le joueur ayant le plus de votes est éliminé (en cas d'égalité, personne n'est éliminé).
- Le rôle du joueur éliminé peut être révélé ou non selon les paramètres de la partie.

#### Retour au jeu {#reunion-retour}
- La partie reprend normalement, avec un joueur en moins si quelqu'un a été éliminé.

:::note[Interactions et stratégies possibles]
- **Défense** : Un joueur accusé peut se défendre et expliquer ses actions.
- **Accusation** : Les joueurs peuvent accuser d'autres participants en se basant sur des indices ou des comportements suspects.
- **Alibi** : Présenter un alibi crédible peut sauver un joueur [innocent](/docs/joueur/roles#innocent).
- **Manipulation** : Les [imposteurs](/docs/joueur/roles#imposteur) peuvent semer le doute ou accuser à tort.
- Tous les joueurs peuvent discuter, accuser, se défendre.
- Un vote est organisé pour éliminer un suspect.
- Le joueur ayant le plus de votes est éliminé (en cas d'égalité, personne n'est éliminé).
:::

### 5. Retour au jeu libre {#phase-retour}
- Le jeu reprend jusqu'à la prochaine réunion ou la fin de partie.

## Fin de partie {#fin-partie}

### Victoire des innocents {#victoire-innocents}
- Toutes les tâches sont accomplies.
- Tous les [imposteurs](/docs/joueur/roles#imposteur) sont éliminés.

### Victoire des imposteurs {#victoire-imposteurs}
- Les [imposteurs](/docs/joueur/roles#imposteur) sont en nombre égal ou supérieur aux [innocents](/docs/joueur/roles#innocent).
- Les [imposteurs](/docs/joueur/roles#imposteur) sabotent de façon décisive (selon les règles du mode).

:::tip
- Communiquez efficacement lors des réunions.
- Soyez attentif aux comportements suspects.
- Les imposteurs doivent être discrets et stratégiques.
:::

Pour plus de détails sur les [commandes](/docs/joueur/commandes) et les [rôles](/docs/joueur/roles), consultez les sections dédiées.

## Gestion de crise : Commande SOS {#gestion-crise-sos}

En cas de situation d'urgence ou de crise dans la partie, un joueur peut utiliser la commande [`sos`](/docs/joueur/commandes/sos) pour alerter tous les participants. Cette commande permet de signaler un événement inhabituel ou critique nécessitant une attention immédiate (par exemple, un problème physique, une personne en danger).

**Déroulement d'une gestion de crise :**
- Lorsqu'un SOS est déclenché, tous les joueurs sont informés de la gestion de crise en cours.
- La partie va être temporairement suspendue.
- L'[organisateur](/docs/joueur/roles#maitre-du-jeu) ou le [maître du jeu](/docs/joueur/roles#maitre-du-jeu) prend en charge la résolution du problème.
- Une fois la crise résolue, la partie reprend normalement.

:::warning
Utilisez la commande [`sos`](/docs/joueur/commandes/sos) de façon responsable, uniquement en cas de réelle nécessité.
:::