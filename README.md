# RappelVocal

Service de rappel de rendez-vous par appel téléphonique, en français.

## À quoi ça sert

RappelVocal appelle automatiquement vos clients pour leur rappeler leur rendez-vous
à venir (médical, salon de coiffure, garage, etc.). Le client décroche, une voix
naturelle lui rappelle la date, l'heure et le lieu de son rendez-vous, et peut
confirmer, reporter ou annuler via le clavier du téléphone.

## Fonctionnement

- Vous planifiez les rendez-vous (import CSV ou API REST)
- Le service appelle le client quelques heures avant le rendez-vous
- Le client confirme (touche 1), reporte (touche 2) ou demande un rappel humain (touche 3)
- Vous recevez un rapport simple des confirmations

## Stack

- Python 3.12, FastAPI
- Téléphonie : Twilio Voice
- Synthèse vocale française
- Docker Compose pour le déploiement

## Démarrage

```bash
cp .env.example .env   # renseigner les clés Twilio
docker compose up -d
```

## Statut

Projet en développement (phase de test). Les appels de test sont passés vers des
numéros vérifiés (mon numéro personnel) avant la mise en production.
