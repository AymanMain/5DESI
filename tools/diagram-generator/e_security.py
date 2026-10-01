from dio import *

d = Diagram("E - Security")
d.title(20, 10, 1300, "MedX — Sécurité : réseau, contrôle d'accès et masquage (Annexe E)",
        "Défense en profondeur : zones réseau isolées · authentification forte · règles « qui peut voir quoi » · données masquées selon le rôle")

d.zone(20, 80, 470, 470, "Zones réseau (dans chacun des 3 datacenters)", fill="#FFFFFF", stroke=TEAL, fs=13)
pub = d.box(45, 120, 420, 95, "", fill=TEAL_L, stroke=TEAL, sw=1.6)
d.aws(65, 145, "elastic_load_balancing", "", size=44)
d.text(125, 120, 330, 95, "<b style='font-size:13px'>Zone publique</b><br>Répartiteur de charge + API Gateway<br><i>seule partie accessible depuis Internet</i>", fs=11.5)
app = d.box(45, 250, 420, 95, "", fill="#FDF0E6", stroke="#ED7100", sw=1.6)
d.aws(65, 275, "eks", "", size=44)
d.text(125, 250, 330, 95, "<b style='font-size:13px'>Zone applicative privée</b><br>Les 8 services · pas d'accès Internet direct<br>appels sortants vers partenaires autorisés", fs=11.5)
dat = d.box(45, 380, 420, 95, "", fill="#FCF3FD", stroke="#C925D1", sw=1.6)
d.aws(65, 405, "rds", "", size=44)
d.text(125, 380, 330, 95, "<b style='font-size:13px'>Zone de données privée</b><br>PostgreSQL · Redis<br>accessible uniquement depuis la zone applicative", fs=11.5)
d.edge(pub, app, "HTTPS", fs=10)
d.edge(app, dat, "TLS", fs=10)
d.text(45, 485, 420, 60, "Des règles de pare-feu (security groups) n'autorisent chaque zone à parler qu'à la suivante. "
       "S3 et KMS sont joints par des points d'accès privés AWS, jamais par Internet.", fs=11, valign="top")

d.zone(510, 80, 470, 470, "Connexion et règles d'accès", fill=RED_L, stroke=RED, fs=13)
rows = [("Patient", "mot de passe + MFA facultative (obligatoire pour consulter le dossier)"),
        ("Médecin", "MFA obligatoire · RPPS vérifié · ou Pro Santé Connect"),
        ("Pharmacien", "MFA obligatoire · rattaché à une pharmacie"),
        ("Admin", "MFA + clé de sécurité · accès temporaire et approuvé")]
html = ("<table style='border-collapse:collapse;width:440px;font-size:11.5px;text-align:left'>"
        "<tr style='background:#C0392B;color:#fff'><th style='padding:5px'>Rôle</th><th style='padding:5px'>Connexion (Keycloak)</th></tr>")
for k, (a, b) in enumerate(rows):
    html += f"<tr style='background:{'#FFFFFF' if k % 2 == 0 else '#FBEAE8'}'><td style='padding:6px 5px'><b>{a}</b></td><td style='padding:6px 5px'>{b}</td></tr>"
html += "</table>"
d.box(525, 112, 445, 200, html, fill="none", stroke="none", valign="top")
d.box(525, 290, 440, 245,
      "<b style='font-size:13px'>Qui peut voir le dossier d'un patient ?</b><br><br>"
      "Le <b>rôle</b> dit quel type de données, la <b>relation</b> dit de qui :<br><br>"
      "• le patient lui-même<br>"
      "• un médecin qui a (ou a eu récemment) un rendez-vous avec lui<br>"
      "• un médecin que le patient a explicitement autorisé<br>"
      "• un urgentiste via l'<b>accès d'urgence</b> (Annexe D)<br><br>"
      "Toute autre demande est refusée — et chaque accès est tracé.",
      fill="#FFFFFF", stroke=RED, fs=11.5, align="left", valign="top", sw=1.4)

d.zone(1000, 80, 540, 470, "Masquage : ce que voit chaque rôle", fill=AMB_L, stroke=AMB, fs=13)
cols = ["Patient", "Médecin<br>traitant", "Urgentiste", "Pharma-<br>cien", "Support"]
F_, M_, P_, N_ = "#D5F5E3", "#FCF3CF", "#FAE5D3", "#F2F3F4"
data = [("Nom, date de naissance", [("Complet", F_), ("Complet", F_), ("Complet", F_), ("Nom + année", P_), ("Masqué", M_)]),
        ("Identifiant INS", [("Complet", F_), ("Complet", F_), ("Complet", F_), ("—", N_), ("•••• 1234", M_)]),
        ("Diagnostics, notes", [("Complet", F_), ("Complet", F_), ("Résumé", P_), ("—", N_), ("—", N_)]),
        ("Allergies, traitements", [("Complet", F_), ("Complet", F_), ("Complet", F_), ("Ordonnance", P_), ("—", N_)]),
        ("Prescriptions", [("Complet", F_), ("Complet", F_), ("Résumé", P_), ("Sa pharmacie", P_), ("Statut", M_)]),
        ("Paiements", [("Complet", F_), ("—", N_), ("—", N_), ("—", N_), ("4 derniers chiffres", M_)])]
html = ("<table style='border-collapse:collapse;width:510px;font-size:11px;text-align:center'>"
        "<tr style='background:#B9770E;color:#fff'><th style='padding:5px;text-align:left'>Donnée</th>"
        + "".join(f"<th style='padding:5px'>{c}</th>" for c in cols) + "</tr>")
for name, cells in data:
    html += f"<tr><td style='padding:6px 5px;text-align:left;background:#fff'><b>{name}</b></td>"
    html += "".join(f"<td style='padding:6px 3px;background:{bg};border:1px solid #fff'>{v}</td>" for v, bg in cells) + "</tr>"
html += "</table>"
d.box(1015, 112, 515, 300, html, fill="none", stroke="none", valign="top")
d.text(1015, 345, 510, 150,
       "Le masquage est appliqué par le service avant que les données ne sortent : aucune application ne peut le contourner.<br><br>"
       "Un médecin peut différer l'affichage d'une note au patient jusqu'à l'annonce en personne d'un diagnostic difficile.",
       fs=11.5, valign="top")

d.box(20, 570, 1520, 80,
      "<b style='font-size:13px'>Conformité</b><br>"
      "<b>RGPD</b> : données de santé = catégorie particulière — minimisation, chiffrement, accès et export par le patient, analyse d'impact (AIPD) avant lancement  ·  "
      "<b>HDS</b> : hébergement uniquement sur infrastructure certifiée (AWS Paris / Francfort)  ·  "
      "<b>Conservation</b> : dossiers médicaux conservés 20 ans  ·  <b>Paiements</b> : données de carte gérées uniquement par Stripe",
      fill=GREY_L, stroke=GREY, fs=11.5, align="left")

d.save("/home/claude/medx3/diagrams/sources/annexe_e_security.drawio")
