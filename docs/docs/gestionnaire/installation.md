---
id: installation
title: Installation du projet
slug: /gestionnaire/installation
---
# Installation du projet Among Us Real

Bienvenue dans la documentation d'installation du projet Among Us Real !

## Prérequis

- **Python 3.9+** (recommandé : 3.11)
- **pip** (gestionnaire de paquets Python)
- **Git** (pour cloner le dépôt)
- **Node.js** (pour la partie WhatsApp)
- Accès à Internet

## Étapes d'installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Merlode11/Among-Us-Real.git
cd Among-Us-Real
```

Vous pouvez aussi télécharger le projet en tant qu'archive ZIP depuis GitHub et l'extraire.

### 2. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 3. Installer les dépendances pour la documentation (optionnel)

```bash
cd docs
npm install
```

### 4. Configuration du projet

- Copiez le fichier `config-exemple.json` en `config.json` et adaptez-le à votre configuration.
- Modifiez les fichiers de tâches et de joueurs si besoin.

### 5. Lancer le jeu

- Pour lancer le logiciel en mode général (toutes plateformes), utilisez la commande suivante :

```bash
python main.py
```

- *Pour lancer un mode spécifique (Discord, SMS, Instagram, WhatsApp, Web), voir la documentation dédiée à chaque mode dans la section Gestionnaire.*

:::danger
Le mode spécifique peut ne pas fonctionner selon l'endroit où vous lancez la commande. Préférez toujours lancer le mode général.
:::

### 6. Tester la documentation localement (optionnel)

```bash
cd docs
npm run start
```

## Conseils supplémentaires

- Vérifiez que tous les ports nécessaires sont ouverts si vous utilisez des API externes (SMS, WhatsApp, etc.).
- Consultez la documentation de chaque mode de jeu pour les configurations spécifiques.
- En cas de problème, consultez le README ou ouvrez une issue sur GitHub.

## Ressources utiles

- [Documentation officielle de Python](https://docs.python.org/fr/3/)
- [Documentation pip](https://pip.pypa.io/en/stable/)
- [Node.js](https://nodejs.org/)
- [Docusaurus](https://docusaurus.io/)

Bon jeu !
