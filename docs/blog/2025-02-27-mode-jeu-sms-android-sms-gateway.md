---
slug: mode-jeu-sms-android-sms-gateway
title: Passage du mode de jeu SMS à android-sms-gateway
authors: merlode
tags: [sms, android, gateway, fonctionnalité, intégration, mode-jeu, nouveauté]
date: 2025-02-27
---

## 📝 Introduction

Dans cette mise à jour, le mode de jeu par SMS a été complètement revu pour utiliser **android-sms-gateway** à la place de la solution précédente. Cette évolution améliore la fiabilité de l’envoi et la réception des messages, tout en simplifiant la configuration côté utilisateur.

<!-- truncate -->

## ❓ Pourquoi changer pour android-sms-gateway ?

- La solution précédente reposait sur AirMore, qui présentait des limitations en termes de fiabilité et de gestion des messages.
- Plus de robustesse dans la gestion des SMS envoyés et reçus.
- Intégration facilitée avec les appareils Android.
- Utilisation d'internet non nécessaire pour l'envoi de SMS, ce qui réduit les risques de déconnexion ou de latence.

## 🛠️ Détails des modifications (commits concernés)

Les commits suivants composent cette évolution :

- `d25b9e2` : Ajout de l’intégration initiale de android-sms-gateway et adaptation du code pour l’envoi/réception via l’API REST.
- `0237d70` : Refactoring des anciennes méthodes d’envoi SMS pour utiliser la nouvelle passerelle, mise à jour de la documentation interne et gestion des erreurs.
- `c0f86d6` : Tests, corrections de bugs et amélioration de l’interface de configuration pour lier l’application Android avec le serveur Among Us Real.

## ⚙️ Comment ça marche maintenant ?

1. **Installer android-sms-gateway** sur un appareil Android dédié.
2. Configurer l’application pour pointer vers l’URL de votre serveur (voir la documentation android-sms-gateway).
3. Renseigner la clé d’API générée dans la configuration du serveur Among Us Real (`config.json`).
4. Le serveur utilise désormais les endpoints REST de android-sms-gateway pour envoyer et recevoir les SMS de jeu.

## 🗂️ Exemple de configuration

```json
{
  "manager_type": "sms",
  "ip": "192.168.1.50",
  "port": 8080,
  "sms_username": "admin",
  "sms_password": "votre_mot_de_passe"
}
```

## ⚠️ Points d’attention

- L’appareil Android doit rester connecté au même réseau local que le serveur, ou doit être accessible depuis ce dernier.
- android-sms-gateway doit disposer des droits nécessaires pour lire et envoyer des SMS.

## ✅ Conclusion

Ce changement rend le mode de jeu SMS plus fiable et plus simple à déployer. N’hésitez pas à consulter les commits cités plus haut pour voir en détail les modifications de code.
