from dio import *

d = Diagram("B - Services")
d.title(20, 10, 1180, "MedX — Services, communication et cycle de vie des prescriptions (Annexe B)",
        "Flèches pleines = appels directs (4 seulement, toujours vers un service plus critique) · tout le reste passe par le bus d'événements")
d.legend_priority(1310, 12)

CW, CH = 330, 128
X = [170, 520, 870]
for pr, y, lbl in [("H", 95, "HAUTE"), ("M", 250, "MOYENNE"), ("L", 405, "BASSE")]:
    s, f, _ = PRIO[pr]
    d.box(20, y, 135, CH, f"<b>{lbl}</b>", fill=f, stroke=s, fc=s, fs=13, sw=1.8)


def card(x, y, w, pr, name, owns, pubs):
    s, f, _ = PRIO[pr]
    return d.box(x, y, w, CH,
                 f"<b style='font-size:14px'>{name}</b><br><br><span style='font-size:11px'><b>Possède :</b> {owns}<br>"
                 f"<b>Publie :</b> <span style='color:#6C3483'>{pubs}</span></span>",
                 fill=f, stroke=s, fs=11, sw=1.8, align="left", valign="top")


um = card(X[0], 95, CW, "H", "Gestion des utilisateurs", "utilisateurs, rôles, préférences", "utilisateur.inscrit")
rec = card(X[1], 95, 680, "H", "Dossiers patients  <span style='color:#C0392B'>+ module Accès d'urgence</span>",
           "antécédents, notes, documents, résumé d'urgence, journal des accès",
           "dossier.modifie · urgence.acces.accorde")
sc = card(X[0], 250, CW, "M", "Planification", "rendez-vous, disponibilités, liste d'attente", "rdv.reserve / deplace / annule")
co = card(X[1], 250, CW, "M", "Consultation", "salles vidéo, messages de chat", "consultation.terminee")
rx = card(X[2], 250, CW, "M", "Prescriptions", "prescriptions + historique des statuts", "prescription.creee / modifiee / revoquee")
no = card(X[0], 405, CW, "L", "Notifications", "statut d'envoi et de lecture", "—")
bi = card(X[1], 405, CW, "L", "Facturation & paiement", "factures, paiements, remboursements", "paiement.effectue")
ph = card(X[2], 405, CW, "L", "Interface pharmacie", "pharmacies, statut de délivrance", "prescription.statut.modifie")

d.edge(sc, um, "profil du médecin", fs=10)
d.edge(co, rec, "enregistre notes & fichiers", fs=10, ex=0.5, ey=0, nx=0.25, ny=1)
d.edge(rx, rec, "allergies & traitements en cours", fs=10, ex=0.5, ey=0, nx=0.76, ny=1)
d.edge(ph, rx, "lit la prescription", fs=10)

d.zone(1225, 95, 315, 438, "Bus d'événements — qui écoute", fill=KAFKA_L, stroke=KAFKA, fs=13)
subs = [("rdv.reserve", "Notifications · Consultation · Facturation"),
        ("consultation.terminee", "Dossiers patients · Facturation"),
        ("dossier.modifie", "module Urgence (met à jour le résumé)"),
        ("prescription.creee / revoquee", "Pharmacie · Notifications · Dossiers"),
        ("prescription.statut.modifie", "Prescriptions · Notifications"),
        ("urgence.acces.accorde", "Notifications (prévenir le patient)"),
        ("paiement.effectue", "Notifications")]
for k, (t, c) in enumerate(subs):
    d.box(1240, 130 + k * 56, 285, 50, f"<b>{t}</b><br><span style='font-size:10.5px;color:#0B2545'>→ {c}</span>",
          fill="#FFFFFF", stroke=KAFKA, fc=KAFKA, fs=11, sw=1, align="left")

d.zone(20, 560, 1520, 225, "Cycle de vie d'une prescription (service Prescriptions · chaque étape publie un événement)", fill=AMB_L, stroke=AMB, fs=13)
st = [("BROUILLON", "le médecin rédige", AMB), ("SIGNÉE", "signature (MFA)", AMB), ("ENVOYÉE", "visible patient + pharmacie", AMB),
      ("REÇUE", "la pharmacie confirme", SLATE), ("PRÊTE / EXPÉDIÉE", "retrait ou livraison", SLATE), ("DÉLIVRÉE", "terminé", TEAL)]
prev = None
ids = []
for k, (a, b, c) in enumerate(st):
    i = d.box(45 + k * 248, 600, 205, 66, f"<b style='font-size:13px'>{a}</b><br><span style='font-size:10.5px'>{b}</span>",
              fill="#FFFFFF", stroke=c, fs=11, sw=2)
    if prev:
        d.edge(prev, i, "")
    prev = i
    ids.append(i)
rv = d.box(570, 712, 260, 56, "<b style='font-size:13px'>RÉVOQUÉE</b><br><span style='font-size:10.5px'>le médecin annule — pharmacie alertée aussitôt</span>",
           fill=RED_L, stroke=RED, fs=11, sw=2)
for i, xx in [(ids[1], 395), (ids[2], 643), (ids[3], 891)]:
    d.edge(i, rv, "", col=RED, ex=0.5, ey=1, nx=0.5, ny=0, points=[(xx, 692), (700, 692)])
d.text(940, 712, 590, 56,
       "<b>Règles :</b> une prescription signée n'est jamais modifiée — un changement crée une nouvelle version. "
       "Le pharmacien voit le médicament et la posologie, pas le diagnostic.", fs=11)

d.save("/home/claude/medx3/diagrams/sources/annexe_b_services.drawio")
