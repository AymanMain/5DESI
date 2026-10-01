"""Tiny draw.io (mxGraph) XML generator used for all MedX diagrams.
All coordinates are absolute (every cell is parented to the root layer)."""
from xml.sax.saxutils import escape

# ---- MedX visual language -------------------------------------------------
NAVY = "#0B2545"
TEAL = "#0F766E"
TEAL_L = "#E6F4F2"
GREY = "#5B6770"
GREY_L = "#F4F6F8"
RED = "#C0392B"       # High priority / emergency
RED_L = "#FDEDEC"
AMB = "#B9770E"       # Medium priority
AMB_L = "#FEF5E7"
SLATE = "#5D6D7E"     # Low priority
SLATE_L = "#EEF1F4"
KAFKA = "#6C3483"
KAFKA_L = "#F4ECF7"

PRIO = {"H": (RED, RED_L, "HAUTE"), "M": (AMB, AMB_L, "MOYENNE"), "L": (SLATE, SLATE_L, "BASSE")}

AWS_COL = {
    "eks": "#ED7100", "lambda": "#ED7100",
    "s3": "#7AA116", "glacier": "#7AA116", "backup": "#7AA116",
    "aurora": "#C925D1", "dynamodb": "#C925D1", "elasticache": "#C925D1", "rds": "#C925D1",
    "route_53": "#8C4FFF", "cloudfront": "#8C4FFF", "elastic_load_balancing": "#8C4FFF",
    "managed_streaming_for_kafka": "#8C4FFF", "nat_gateway": "#8C4FFF", "privatelink": "#8C4FFF",
    "transit_gateway": "#8C4FFF",
    "api_gateway": "#E7157B", "cloudwatch": "#E7157B", "cloudtrail": "#E7157B", "sns": "#E7157B",
    "sqs": "#E7157B", "eventbridge": "#E7157B", "config": "#E7157B",
    "waf": "#DD344C", "shield": "#DD344C", "key_management_service": "#DD344C",
    "secrets_manager": "#DD344C", "cognito": "#DD344C", "guardduty": "#DD344C",
    "certificate_manager": "#DD344C", "cloudhsm": "#DD344C", "simple_email_service": "#DD344C",
    "chime": "#DD344C", "macie": "#DD344C", "security_hub": "#DD344C", "inspector": "#DD344C",
    "identity_and_access_management": "#DD344C", "end_user_messaging": "#DD344C",
    "healthlake": "#01A88D",
}


class Diagram:
    def __init__(self, name):
        self.name = name
        self.cells = []
        self.n = 0

    def _id(self):
        self.n += 1
        return f"c{self.n}"

    def _add(self, xml):
        self.cells.append(xml)

    def vertex(self, x, y, w, h, value, style):
        i = self._id()
        self._add(f'<mxCell id="{i}" value="{escape(value, {chr(34): "&quot;"})}" style="{style}" '
                  f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return i

    # -- primitives ---------------------------------------------------------
    def box(self, x, y, w, h, text, fill="#FFFFFF", stroke=NAVY, fc=NAVY, fs=11, bold=False,
            rounded=True, dashed=False, align="center", valign="middle", sw=1.2, extra=""):
        st = (f"rounded={1 if rounded else 0};absoluteArcSize=1;arcSize=14;whiteSpace=wrap;html=1;fillColor={fill};"
              f"strokeColor={stroke};fontColor={fc};fontSize={fs};fontStyle={1 if bold else 0};"
              f"align={align};verticalAlign={valign};strokeWidth={sw};spacing=6;"
              f"{'dashed=1;dashPattern=6 4;' if dashed else ''}fontFamily=Helvetica;{extra}")
        return self.vertex(x, y, w, h, text, st)

    def zone(self, x, y, w, h, title, fill=GREY_L, stroke=GREY, fc=None, fs=13, dashed=False):
        """Background container with title in the top-left."""
        fc = fc or stroke
        st = (f"rounded=1;absoluteArcSize=1;arcSize=14;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
              f"fontColor={fc};fontSize={fs};fontStyle=1;align=left;verticalAlign=top;spacingLeft=10;"
              f"spacingTop=4;strokeWidth=1.5;{'dashed=1;dashPattern=8 4;' if dashed else ''}"
              f"fontFamily=Helvetica;container=0;")
        return self.vertex(x, y, w, h, title, st)

    def text(self, x, y, w, h, text, fs=11, fc=NAVY, bold=False, align="left", italic=False, valign="middle"):
        style = (1 if bold else 0) + (2 if italic else 0)
        st = (f"text;html=1;whiteSpace=wrap;fontSize={fs};fontColor={fc};fontStyle={style};"
              f"align={align};verticalAlign={valign};fontFamily=Helvetica;strokeColor=none;fillColor=none;")
        return self.vertex(x, y, w, h, text, st)

    def aws(self, x, y, icon, label="", size=44, fs=10, lw=130):
        col = AWS_COL[icon]
        st = (f"outlineConnect=0;fontColor=#232F3E;fillColor={col};strokeColor=#ffffff;"
              f"html=1;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};")
        i = self.vertex(x, y, size, size, "", st)
        if label:
            st2 = (f"text;html=1;whiteSpace=wrap;fontSize={fs};fontColor=#232F3E;align=center;"
                   f"verticalAlign=top;strokeColor=none;fillColor=none;fontFamily=Helvetica;spacing=0;")
            self.vertex(x + size / 2 - lw / 2, y + size + 3, lw, 14 * (label.count("<br>") + 1) + 4, label, st2)
        return i

    def actor(self, x, y, label, col=NAVY, lw=150):
        st = (f"shape=umlActor;html=1;outlineConnect=0;fillColor=#FFFFFF;strokeColor={col};strokeWidth=1.5;")
        i = self.vertex(x, y, 26, 48, "", st)
        if label:
            st2 = (f"text;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;fontColor={col};align=center;"
                   f"verticalAlign=top;strokeColor=none;fillColor=none;spacing=0;")
            self.vertex(x + 13 - lw / 2, y + 52, lw, 16 * (label.count("<br>") + 1), label, st2)
        return i

    def cyl(self, x, y, w, h, text, fill="#FFFFFF", stroke=NAVY, fs=10):
        st = (f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=8;"
              f"fillColor={fill};strokeColor={stroke};fontColor={NAVY};fontSize={fs};strokeWidth=1.2;")
        return self.vertex(x, y, w, h, text, st)

    def pill(self, x, y, w, h, text, fill, fc="#FFFFFF", fs=9):
        st = (f"rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=none;"
              f"fontColor={fc};fontSize={fs};fontStyle=1;")
        return self.vertex(x, y, w, h, text, st)

    def circle(self, x, y, d, text, fill=RED, fc="#FFFFFF", fs=10):
        st = (f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=none;fontColor={fc};"
              f"fontSize={fs};fontStyle=1;")
        return self.vertex(x, y, d, d, text, st)

    def line(self, x1, y1, x2, y2, col=GREY, dashed=True, sw=1):
        i = self._id()
        st = (f"endArrow=none;html=1;strokeColor={col};strokeWidth={sw};"
              f"{'dashed=1;dashPattern=4 4;' if dashed else ''}")
        self._add(f'<mxCell id="{i}" style="{st}" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
                  f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/><mxPoint x="{x2}" y="{y2}" as="targetPoint"/>'
                  f'</mxGeometry></mxCell>')
        return i

    def arrow(self, x1, y1, x2, y2, label="", col=NAVY, dashed=False, sw=1.4, fs=10, lbl_bg="#FFFFFF",
              end="block", start="none", bold=False, above=True, lw=440):
        """Free-floating arrow between two points (sequence diagrams). Label sits above the line."""
        i = self._id()
        st = (f"endArrow={end};startArrow={start};endFill=1;html=1;strokeColor={col};strokeWidth={sw};"
              f"{'dashed=1;dashPattern=6 4;' if dashed else ''}")
        self._add(f'<mxCell id="{i}" value="" style="{st}" edge="1" parent="1">'
                  f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
                  f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/></mxGeometry></mxCell>')
        if label:
            lx = min(x1, x2) + 8
            st2 = (f"text;html=1;fontSize={fs};fontColor={col};fontStyle={1 if bold else 0};align=left;"
                   f"verticalAlign=bottom;spacing=0;labelBackgroundColor={lbl_bg};whiteSpace=nowrap;")
            self.vertex(lx, y1 - 20, lw, 18, label, st2)
        return i

    def edge(self, s, t, label="", col=NAVY, dashed=False, sw=1.4, fs=9, points=None, ortho=True,
             ex=None, ey=None, nx=None, ny=None, end="block", start="none", curved=False):
        i = self._id()
        st = (f"endArrow={end};startArrow={start};endFill=1;startFill=1;html=1;strokeColor={col};"
              f"strokeWidth={sw};fontColor={col};fontSize={fs};labelBackgroundColor=#FFFFFF;"
              f"{'edgeStyle=orthogonalEdgeStyle;rounded=1;' if ortho else ''}"
              f"{'curved=1;' if curved else ''}"
              f"{'dashed=1;dashPattern=6 4;' if dashed else ''}")
        if ex is not None: st += f"exitX={ex};exitY={ey};exitDx=0;exitDy=0;"
        if nx is not None: st += f"entryX={nx};entryY={ny};entryDx=0;entryDy=0;"
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + "</Array>"
        self._add(f'<mxCell id="{i}" value="{escape(label, {chr(34): '&quot;'})}" style="{st}" edge="1" parent="1" source="{s}" '
                  f'target="{t}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>')
        return i

    # -- composite ------------------------------------------------------------
    def service(self, x, y, w, h, name, sub, prio, tech=""):
        """Microservice card coloured by MedX priority."""
        stroke, fill, _ = PRIO[prio]
        body = f"<b style='font-size:12px'>{name}</b><br><span style='font-size:9.5px'>{sub}</span>"
        if tech:
            body += f"<br><i style='font-size:9px;color:{GREY}'>{tech}</i>"
        return self.box(x, y, w, h, body, fill=fill, stroke=stroke, fc=NAVY, sw=1.8)

    def legend_priority(self, x, y):
        self.text(x, y, 200, 18, "Priorité (annexe 2 du sujet)", fs=10, bold=True)
        for k, (i, lbl) in enumerate([("H", "Haute"), ("M", "Moyenne"), ("L", "Basse")]):
            s, f, _ = PRIO[i]
            self.box(x + k * 78, y + 22, 70, 20, lbl, fill=f, stroke=s, fs=9, bold=True, sw=1.8)

    def title(self, x, y, w, t, sub=""):
        self.text(x, y, w, 30, t, fs=20, bold=True, fc=NAVY)
        if sub:
            self.text(x, y + 28, w, 20, sub, fs=11, fc=GREY, italic=True)

    def save(self, path):
        xml = ('<mxfile host="MedX-generator" agent="python" version="24.0.0">'
               f'<diagram id="{self.name}" name="{self.name}"><mxGraphModel dx="1600" dy="900" grid="1" '
               'gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" '
               'pageScale="1" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
               + "".join(self.cells) + "</root></mxGraphModel></diagram></mxfile>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
