from dio import *

d = Diagram("D - Emergency Access")
d.title(20, 10, 1400, "MedX — Accès d'urgence (« bris de glace ») (Annexe D)",
        "Un urgentiste obtient les informations vitales d'un patient en moins d'une seconde — chaque accès est tracé, limité dans le temps et contrôlé")

lanes = ["Urgentiste", "Application MedX", "API Gateway<br>+ Keycloak", "Dossiers patients<br>(module Urgence)",
         "Redis<br>Résumé d'urgence", "Journal des accès<br>(S3, verrouillé)", "Notifications"]
X = [110 + 205 * k for k in range(len(lanes))]
TOP, BOT = 85, 690
for k, (x, name) in enumerate(zip(X, lanes)):
    red = k in (0, 3, 5)
    d.box(x - 88, TOP, 176, 56, f"<b>{name}</b>", fill=RED_L if red else "#FFFFFF", stroke=RED if red else NAVY, fs=12, sw=1.6)
    d.line(x, TOP + 56, x, BOT, col=GREY)

steps = [(185, 0, 1, "1 · recherche le patient (carte Vitale / INS, ou nom + date de naissance)", False, NAVY),
         (235, 1, 2, "2 · « Accès d'urgence » + motif", False, NAVY),
         (340, 2, 3, "4 · transmet la demande", False, NAVY),
         (455, 3, 5, "6 · écrit l'entrée : qui, patient, motif, heure", False, RED),
         (505, 3, 4, "7 · lit le résumé", False, RED),
         (550, 4, 3, "8 · groupe sanguin · allergies · traitements · pathologies", True, RED),
         (600, 3, 1, "9 · résumé + « valable 60 min · accès tracé »", True, RED),
         (645, 3, 6, "10 · prévient le patient (via le bus, après coup)", False, KAFKA)]
for y, a, b, lbl, dash, col in steps:
    d.arrow(X[a], y, X[b], y, lbl, col=col, dashed=dash, fs=11, sw=1.8, lw=560)

d.box(X[2] - 95, 260, 190, 54, "<b>3 ·</b> connexion valide ?<br>redemande la MFA", fill="#FFFFFF", stroke=NAVY, fs=11)
d.box(X[3] - 95, 365, 190, 64, "<b>5 ·</b> est-ce un médecin<br>avec un RPPS actif ?<br>motif renseigné ?", fill="#FFFFFF", stroke=RED, fs=11, sw=1.6)
d.box(X[5] - 30, 385, 260, 52, "<b>Tracer d'abord, afficher ensuite :</b><br>pas d'entrée au journal → pas de données", fill=RED_L, stroke=RED, fs=11, sw=1.6)

d.line(40, 235, 40, 600, col=RED, dashed=False, sw=2.5)
d.vertex(8, 360, 28, 140, "< 1 seconde", "text;html=1;fontSize=12;fontStyle=1;fontColor=#C0392B;rotation=-90;align=center;verticalAlign=middle;")

g = [("Limité", "Résumé uniquement (pas le dossier complet), lecture seule, expire au bout de 60 minutes."),
     ("Traçable", "Chaque accès est inscrit dans un journal que personne ne peut modifier ni supprimer."),
     ("Transparent", "Le patient est informé de qui a consulté ses données, et quand."),
     ("Contrôlé", "Un responsable conformité vérifie chaque accès d'urgence sous 72 heures.")]
for k, (a, b) in enumerate(g):
    d.box(20 + k * 350, 715, 335, 80, f"<b style='font-size:13px;color:#C0392B'>{a}</b><br>{b}",
          fill=RED_L, stroke=RED, fs=11, sw=1.6, align="left")

d.box(20, 810, 1385, 75,
      "<b>En cas de panne :</b>  Redis indisponible → le résumé est lu dans la base  ·  région Paris indisponible → la réplique de Francfort sert les résumés "
      "et le journal est écrit dans la copie S3 de Francfort  ·  MedX totalement indisponible → une astreinte 24h/24 lit le résumé à un soignant vérifié.",
      fill="#FFFFFF", stroke=NAVY, fs=11.5, align="left", dashed=True)

d.save("/home/claude/medx3/diagrams/sources/annexe_d_emergency_access.drawio")
