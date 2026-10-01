# 🩺 MedX — Plateforme de santé : architecture technique

> Conception technique d'une plateforme de santé : téléconsultations, dossiers patients, accès d'urgence et prescriptions.
> AWS (Paris + Francfort) · 8 services · conforme RGPD et HDS.
> *Auteurs : Ayman EL KARROUSSI · Abdoulaye FOFANA · Hamid AIT MIMOUN — mini-projet académique*

---

## Présentation

MedX veut proposer des téléconsultations, gérer les dossiers patients et permettre aux pharmacies de suivre les prescriptions. Le sujet classe ses exigences par priorité, et deux passent avant tout : **protéger les données de santé** (en transit et au repos) et **donner aux professionnels de santé un accès immédiat en cas d'urgence**.

La conception suit un principe : **l'effort suit la priorité**. Les fonctions de priorité haute bénéficient de la meilleure protection et de la plus forte redondance ; celles de priorité basse restent simples et peuvent attendre en cas de charge. Tous les schémas utilisent le même code couleur : 🔴 Haute · 🟠 Moyenne · ⚪ Basse.

---

## L'architecture en bref

```
Utilisateurs (patients · médecins · urgentistes · pharmaciens)
  → CloudFront + AWS WAF                 (HTTPS, filtrage des attaques)
  → API Gateway + Keycloak               (point d'entrée unique · connexion · MFA pour les professionnels)
  → 8 services sur Amazon EKS
       HAUTE    Gestion des utilisateurs · Dossiers patients (+ module Accès d'urgence)
       MOYENNE  Planification · Consultation (vidéo Chime SDK) · Prescriptions
       BASSE    Interface pharmacie · Notifications · Facturation (Stripe)
       ↕ Bus d'événements : Amazon SNS + SQS  (identifiants uniquement, jamais de contenu médical)
  → Données (chiffrées avec AWS KMS)
       PostgreSQL (RDS Multi-AZ, un schéma par service) · S3 avec Object Lock · Redis
  → Région de secours : Francfort (réplique en lecture + copies des sauvegardes)
```

---

## Décisions clés

**Accès d'urgence en moins d'une seconde.** Chaque patient a un *résumé d'urgence* préparé à l'avance (groupe sanguin, allergies, traitements, pathologies, contacts), rafraîchi à chaque modification du dossier et mis en cache dans Redis. L'urgentiste confirme son identité par MFA, indique un motif, et une entrée est écrite au journal **avant** tout affichage. L'accès est en lecture seule, dure 60 minutes, le patient est informé et chaque accès est contrôlé. En cas de panne : lecture en base → Francfort → astreinte téléphonique 24h/24.

**Des données protégées en couches.** HTTPS/TLS en transit, chiffrement KMS au repos, chiffrement supplémentaire des champs les plus sensibles par le service lui-même, et masquage pour que chaque rôle ne voie que le nécessaire.

**Des dossiers jamais écrasés.** Chaque modification est une nouvelle version (qui, quand, pourquoi) ; les fichiers sont verrouillés et dotés d'une empreinte ; les sauvegardes sont quotidiennes, copiées à Francfort et testées chaque mois.

**Qui peut voir un dossier ?** Le patient, un médecin ayant un rendez-vous (récent), un médecin autorisé par le patient, ou un urgentiste via l'accès d'urgence. Tout le reste est refusé, et chaque accès est tracé.

**Montée en charge.** La vidéo passe par un service géré (Chime SDK), les services s'adaptent automatiquement sur Kubernetes, et le travail de priorité basse attend en file quand le système est chargé.

---

## Schémas

Réalisés avec **draw.io** et la bibliothèque d'icônes AWS. Sources dans `diagrams/sources/`, exports PNG dans `diagrams/exports/`.

| Schéma | Contenu |
| --- | --- |
| [Annexe A — Architecture](diagrams/exports/annexe_a_architecture.png) | Utilisateurs → périphérie → passerelle & identité → 8 services → données ; sécurité, services externes, région de secours |
| [Annexe B — Services](diagrams/exports/annexe_b_services.png) | Ce que possède et publie chaque service, les 4 appels directs, les abonnements aux événements, le cycle de vie des prescriptions |
| [Annexe C — Données](diagrams/exports/annexe_c_data.png) | Entités principales, emplacement des données, intégrité et chiffrement |
| [Annexe D — Accès d'urgence](diagrams/exports/annexe_d_emergency_access.png) | Déroulement « bris de glace » pas à pas, garde-fous, solutions de repli |
| [Annexe E — Sécurité](diagrams/exports/annexe_e_security.png) | Zones réseau, connexion par rôle, règle d'accès, tableau de masquage, conformité |

---

## Organisation du dépôt

```
medx-architecture/
├── README.md
├── report/MedX_Architecture.pdf          (≈ 11 pages + 5 annexes)
├── presentation/MedX_Presentation.pptx   (10 diapositives, notes de présentation)
├── diagrams/
│   ├── sources/   *.drawio
│   └── exports/   *.png
└── tools/diagram-generator/              (scripts ayant généré les fichiers .drawio)
```

## Contenu du rapport

1. Introduction et décisions clés · 2. Hypothèses et objectifs · 3. Couverture des exigences · 4. Architecture générale · 5. Conception des composants (8 services) · 6. Modèle de données et stockage · 7. Sécurité et conformité · 8. Montée en charge et performance · 9. Compromis · 10. Conclusion · Annexes A–E

## Technologies

| Couche | Technologie |
| --- | --- |
| Périphérie | CloudFront · AWS WAF · Route 53 |
| Point d'entrée & connexion | API Gateway · Keycloak (MFA, Pro Santé Connect) |
| Services | Conteneurs sur Amazon EKS |
| Bus d'événements | Amazon SNS + SQS |
| Données | PostgreSQL (Amazon RDS) · Amazon S3 · Redis (ElastiCache) |
| Sécurité | AWS KMS · Secrets Manager · CloudTrail · GuardDuty · AWS Backup |
| Vidéo | Amazon Chime SDK |
| Messages | Amazon SES · SMS |
| Paiements | Stripe |
