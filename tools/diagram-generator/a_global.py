from dio import *

d = Diagram("A - Architecture")
d.title(20, 10, 1150, "MedX — Architecture générale (Annexe A)",
        "Utilisateurs → Périphérie → Passerelle & identité → 8 services → Données · les services communiquent via un bus d'événements")
d.legend_priority(1310, 12)

d.zone(370, 75, 1180, 715, "Région AWS eu-west-3 (Paris) · certifiée HDS · 3 zones de disponibilité",
       fill="#FFFFFF", stroke=TEAL, dashed=True, fs=13)

uz = d.zone(20, 95, 160, 500, "Utilisateurs", fill=GREY_L, stroke=GREY)
for k, (lbl, col) in enumerate([("Patient", NAVY), ("Médecin", NAVY), ("Urgentiste", RED), ("Pharmacien", NAVY)]):
    d.actor(87, 135 + k * 112, lbl, col)

d.zone(195, 95, 160, 500, "Périphérie", fill=GREY_L, stroke=GREY)
cf = d.aws(253, 150, "cloudfront", "CloudFront<br>HTTPS · TLS 1.3", fs=11)
d.aws(253, 290, "waf", "AWS WAF<br>filtrage des attaques", fs=11)
d.aws(253, 430, "route_53", "Route 53<br>DNS + bascule", fs=11)
d.edge(uz, cf, "HTTPS", ex=1, ey=0.2, nx=0, ny=0.5, fs=10)

d.zone(385, 110, 175, 465, "Passerelle & identité", fill=TEAL_L, stroke=TEAL)
gw = d.box(400, 160, 145, 80, "<b>API Gateway</b><br><span style='font-size:10px'>vérifie le jeton · limite le débit</span>",
           stroke=TEAL, fs=12)
kc = d.box(400, 300, 145, 110, "<b>Keycloak</b><br><span style='font-size:10px'>connexion · MFA pour les professionnels · rôles</span>",
           fill=RED_L, stroke=RED, fs=12, sw=1.8)
d.edge(cf, gw, "", nx=0, ny=0.5, ex=1, ey=0.5, points=[(370, 172), (370, 200)])
d.edge(gw, kc, "valide le jeton", fs=10)

sz = d.zone(575, 110, 640, 465, "8 services · conteneurs sur Amazon EKS · TLS entre services", fill="#FFFFFF", stroke="#ED7100")
d.service(590, 150, 300, 92, "Gestion des utilisateurs", "comptes · connexion · rôles · préférences", "H")
d.service(900, 150, 300, 92, "Dossiers patients", "antécédents · documents<br><b style='color:#C0392B'>+ module Accès d'urgence</b>", "H")
for k, (n, sub) in enumerate([("Planification", "réserver · déplacer · agendas"), ("Consultation", "vidéo · chat · fichiers"),
                              ("Prescriptions", "créer · modifier · révoquer")]):
    d.service(590 + k * 205, 262, 195, 84, n, sub, "M")
for k, (n, sub) in enumerate([("Interface pharmacie", "réception · statut · stock"), ("Notifications", "SMS · e-mail · push"),
                              ("Facturation", "honoraires · factures · remboursements")]):
    d.service(590 + k * 205, 366, 195, 84, n, sub, "L")
d.box(590, 475, 610, 85,
      "<b style='font-size:13px'>Bus d'événements — sujets Amazon SNS → files Amazon SQS</b><br>"
      "rdv.reserve · consultation.terminee · dossier.modifie · prescription.creee / revoquee · paiement.effectue<br>"
      "<i>les événements ne contiennent que des identifiants, jamais de contenu médical</i>",
      fill=KAFKA_L, stroke=KAFKA, fc=KAFKA, fs=11, sw=1.6)
d.edge(gw, sz, "", ex=1, ey=0.5, nx=0, ny=0.12, fs=10)

dz = d.zone(1230, 110, 305, 465, "Données · chiffrées au repos (AWS KMS)", fill="#FCF3FD", stroke="#C925D1")
d.aws(1360, 145, "rds", "PostgreSQL (RDS Multi-AZ) · un schéma par service", fs=11, lw=285)
d.aws(1360, 250, "s3", "S3 · versionné + Object Lock · documents, journal", fs=11, lw=285)
d.aws(1360, 355, "elasticache", "Redis · cache + copies des résumés d'urgence", fs=11, lw=285)
d.text(1245, 460, 285, 110,
       "• Les données médicales ne sont jamais écrasées : chaque modification crée une nouvelle version<br>"
       "• Sauvegardes quotidiennes, restauration à 35 jours<br>• Copies répliquées à Francfort", fs=11)
d.edge(sz, dz, "", ex=1, ey=0.3, nx=0, ny=0.3)

d.zone(385, 595, 1150, 180, "Sécurité & exploitation", fill=RED_L, stroke=RED, fs=13)
for k, (ic, lb) in enumerate([("key_management_service", "KMS<br>clés de chiffrement"), ("secrets_manager", "Secrets Manager<br>mots de passe & clés API"),
                              ("cloudtrail", "CloudTrail<br>journal des actions admin"), ("guardduty", "GuardDuty<br>détection des menaces"),
                              ("cloudwatch", "CloudWatch<br>supervision & alertes"), ("backup", "AWS Backup<br>sauvegardes verrouillées")]):
    d.aws(440 + k * 182, 640, ic, lb, fs=11, lw=160)

d.zone(370, 810, 1180, 120, "Services externes", fill=GREY_L, stroke=GREY)
d.aws(420, 845, "chime", "Chime SDK (vidéo)", fs=11)
d.aws(620, 845, "simple_email_service", "SES / SMS", fs=11)
d.box(760, 848, 170, 50, "<b>Stripe</b><br><span style='font-size:10px'>paiements</span>", stroke=GREY, fs=12)
d.box(950, 848, 190, 50, "<b>Google / Outlook</b><br><span style='font-size:10px'>agendas des médecins</span>", stroke=GREY, fs=12)
d.box(1160, 848, 170, 50, "<b>Logiciels pharmacie</b><br><span style='font-size:10px'>niveaux de stock</span>", stroke=GREY, fs=12)
d.box(1350, 848, 180, 50, "<b>Pro Santé Connect</b><br><span style='font-size:10px'>identité des médecins</span>", stroke=GREY, fs=12)

d.box(20, 615, 335, 315,
      "<b style='font-size:13px'>Région de secours — Francfort</b><br><br>"
      "• Réplique en lecture de la base (quelques secondes de retard)<br>• Copies des documents et des sauvegardes<br>"
      "• Peut servir les <b>résumés d'urgence</b> en lecture seule pendant une panne<br><br>"
      "<b style='font-size:13px;color:#C0392B'>Dernier recours</b><br>Si MedX est totalement indisponible, les urgences appellent une astreinte MedX 24h/24 qui lit le résumé à un soignant vérifié.",
      fill=TEAL_L, stroke=TEAL, fs=11, align="left", valign="top", dashed=True)

d.save("/home/claude/medx3/diagrams/sources/annexe_a_architecture.drawio")
