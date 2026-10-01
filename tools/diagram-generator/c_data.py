from dio import *

d = Diagram("C - Data")
d.title(20, 10, 1180, "MedX — Modèle de données et stockage (Annexe C)",
        "Entités principales et leurs liens · [C] = champ chiffré par l'application, en plus du chiffrement de la base")
d.legend_priority(1310, 12)

d.zone(20, 80, 900, 700, "Entités principales", fill="#FFFFFF", stroke=NAVY, fs=13)
EW = 255
E = "<b style='color:#C0392B'>[C]</b>"


def ent(x, y, name, fields, pr="H"):
    s, f, _ = PRIO[pr]
    body = (f"<div style='background:{s};color:#fff;padding:5px;font-weight:bold;font-size:13px'>{name}</div>"
            f"<div style='text-align:left;padding:5px 8px;font-size:11px;line-height:1.45'>{fields}</div>")
    h = 30 + 16 * (fields.count("<br>") + 1) + 14
    st = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontColor={NAVY};"
          f"verticalAlign=top;spacing=0;strokeWidth=1.6;overflow=fill;")
    return d.vertex(x, y, EW, h, body, st)


doc = ent(45, 120, "Médecin", f"id · n° RPPS<br>spécialité<br>nom, coordonnées {E}", "H")
pat = ent(340, 120, "Patient", f"id · identifiant INS {E}<br>nom, date de naissance {E}<br>coordonnées, adresse {E}", "H")
pha = ent(635, 120, "Pharmacie", "id · n° FINESS<br>adresse · horaires", "L")
app = ent(45, 300, "Rendez-vous", "id · patient · médecin<br>début / fin · statut<br>urgent ? · rang en liste d'attente", "M")
ems = ent(340, 300, "Résumé d'urgence", f"id patient<br>groupe sanguin · allergies {E}<br>traitements · pathologies {E}<br>contacts d'urgence {E}", "H")
log = ent(635, 300, "Journal des accès", "qui · quel patient · quand<br>motif (ex. urgence)<br>ajout seulement", "H")
con = ent(45, 500, "Consultation", f"id · rendez-vous<br>début / fin<br>notes du médecin {E} (versionnées)", "M")
rec = ent(340, 500, "Entrée du dossier médical", f"id · patient · consultation<br>type : diagnostic, allergie, examen…<br>contenu {E} · version", "H")
rx = ent(635, 500, "Prescription", "id · patient · médecin · pharmacie<br>médicament · posologie<br>statut · signature · version", "M")
d.text(45, 680, 860, 90,
       "Aussi : <b>Document</b> (fichier S3 + empreinte, lié à un patient), <b>Facture</b> (consultation, montant, statut), "
       "<b>Notification</b> (canal, reçue, lue). Les entités cliniques reprennent les noms du standard HL7 <b>FHIR</b> "
       "(Patient, Encounter, MedicationRequest…), ce qui facilite les échanges futurs avec les hôpitaux.", fs=11)

d.edge(doc, app, "1 → n", fs=10)
d.edge(pat, app, "1 → n", fs=10, ex=0.15, ey=1, nx=1, ny=0.3, points=[(378, 270), (320, 270), (320, 330)])
d.edge(pat, ems, "1 → 1", fs=10, col=RED)
d.edge(app, con, "1 → 1", fs=10)
d.edge(con, rec, "1 → n", fs=10)
d.edge(con, rx, "1 → n", fs=10, ex=1, ey=0.85, nx=0.5, ny=1, points=[(320, 600), (320, 670), (762, 670)])
d.edge(pha, rx, "", fs=10, ex=1, ey=0.5, nx=1, ny=0.5, points=[(912, 160), (912, 545)])
d.edge(rec, ems, "tient à jour", fs=10, col=RED, dashed=True)

d.zone(940, 80, 600, 225, "Où sont les données", fill=GREY_L, stroke=GREY, fs=13)
rows = [("PostgreSQL (RDS)", "Toutes les données structurées. Un schéma par service ; un service ne lit jamais les tables d'un autre.", "Relations, transactions, contraintes (pas de double réservation)"),
        ("S3", "Documents, factures, journal des accès", "Économique, très durable ; Object Lock = impossible à supprimer ou modifier"),
        ("Redis", "Cache + copie des résumés d'urgence", "Lecture en quelques millisecondes"),
        ("Francfort", "Réplique en lecture + copies des sauvegardes", "Survit à la perte de la région Paris")]
html = ("<table style='border-collapse:collapse;width:570px;font-size:11px;text-align:left'>"
        "<tr style='background:#0B2545;color:#fff'><th style='padding:5px'>Stockage</th><th style='padding:5px'>Contenu</th><th style='padding:5px'>Pourquoi</th></tr>")
for k, (a, b, c) in enumerate(rows):
    bg = "#FFFFFF" if k % 2 == 0 else "#EEF1F4"
    html += (f"<tr style='background:{bg}'><td style='padding:5px'><b>{a}</b></td><td style='padding:5px'>{b}</td>"
             f"<td style='padding:5px'>{c}</td></tr>")
html += "</table>"
d.box(955, 108, 575, 192, html, fill="none", stroke="none", valign="top")

d.zone(940, 320, 600, 225, "Des données sûres et exactes", fill=RED_L, stroke=RED, fs=13)
d.text(960, 352, 565, 185,
       "• <b>Jamais d'écrasement</b> : modifier une entrée crée une nouvelle version (qui, quand, pourquoi)<br><br>"
       "• <b>Empreintes</b> sur chaque fichier, vérifiées au téléchargement<br><br>"
       "• <b>Sauvegardes</b> quotidiennes + restauration à 35 jours, copiées à Francfort, verrouillées contre la suppression<br><br>"
       "• <b>Environnements de test</b> : faux patients générés (Synthea), jamais de vraies données",
       fs=11.5, valign="top")
d.zone(940, 560, 600, 220, "Chiffrement", fill=TEAL_L, stroke=TEAL, fs=13)
d.text(960, 592, 565, 180,
       "• <b>En transit</b> : HTTPS (TLS 1.3) pour les utilisateurs, TLS entre services et vers les bases<br><br>"
       "• <b>Au repos</b> : base, fichiers et sauvegardes chiffrés avec des clés AWS KMS<br><br>"
       "• <b>Champs [C]</b> : chiffrés par le service lui-même — une sauvegarde volée ou un administrateur de base ne voit que des données illisibles<br><br>"
       "• Une clé par fichier : supprimer la clé efface le fichier définitivement",
       fs=11.5, valign="top")

d.save("/home/claude/medx3/diagrams/sources/annexe_c_data.drawio")
