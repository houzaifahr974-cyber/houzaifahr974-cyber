#!/usr/bin/env python3
"""Génère Masterclass-Cross-Trade.pptx à partir de B-presentation-diapositives.md.

Usage : python3 outils/generer_pptx.py   (depuis le dossier masterclass-cross-trade)
Dépendance : python-pptx
"""
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Pt

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "B-presentation-diapositives.md"
OUTPUT = ROOT / "Masterclass-Cross-Trade.pptx"

NAVY = RGBColor(0x0B, 0x25, 0x45)
OCEAN = RGBColor(0x13, 0x67, 0x8A)
ORANGE = RGBColor(0xF2, 0x8C, 0x28)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xEE, 0xF4, 0xF8)
GREY = RGBColor(0x55, 0x60, 0x6E)

FIELDS = {
    "Message essentiel": "message",
    "Contenu visible": "contenu",
    "Visuel recommandé": "visuel",
    "Notes du professeur": "notes",
    "Explication orale": "oral",
    "Exemple concret": "exemple",
    "Transition": "transition",
}


def parse(md: str):
    slides = []
    for block in re.split(r"^## Diapo ", md, flags=re.M)[1:]:
        header, _, body = block.partition("\n")
        num, _, title = header.partition(" — ")
        slide = {"num": num.strip(), "title": title.strip(), "contenu": []}
        current = None
        for line in body.splitlines():
            m = re.match(r"\*\*(.+?) :\*\*\s*(.*)", line)
            if m and m.group(1) in FIELDS:
                current = FIELDS[m.group(1)]
                if current != "contenu":
                    slide[current] = m.group(2).strip()
                continue
            if current == "contenu" and line.startswith("- "):
                # espaces insécables avant % et : pour éviter les retours à la ligne orphelins
                slide["contenu"].append(line[2:].strip().replace(" %", "\u00a0%").replace(" :", "\u00a0:"))
        slides.append(slide)
    return slides


def add_text(slide, left, top, width, height, text, size, color, bold=False, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = "Montserrat"
    return tf


def rect(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def build(slides):
    prs = Presentation()
    prs.slide_width = Emu(12192000)  # 16:9
    prs.slide_height = Emu(6858000)
    W, H = prs.slide_width, prs.slide_height
    blank = prs.slide_layouts[6]
    margin = Emu(457200)

    for i, s in enumerate(slides):
        sl = prs.slides.add_slide(blank)
        first_or_last = i in (0, len(slides) - 1)

        if first_or_last:
            rect(sl, 0, 0, W, H, NAVY)
            rect(sl, margin, Emu(2700000), Emu(1200000), Emu(60000), ORANGE)
            add_text(sl, margin, Emu(1300000), W - 2 * margin, Emu(1300000), s["title"], 40, WHITE, bold=True)
            add_text(sl, margin, Emu(2900000), W - 2 * margin, Emu(700000), s.get("message", ""), 20, ORANGE)
            tf = add_text(sl, margin, Emu(3800000), W - 2 * margin, Emu(2400000), "", 18, WHITE)
            for j, item in enumerate(s["contenu"]):
                p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                p.text = item
                p.font.size = Pt(18)
                p.font.color.rgb = WHITE
                p.font.name = "Montserrat"
        else:
            rect(sl, 0, 0, W, Emu(1150000), NAVY)
            add_text(sl, margin, Emu(160000), Emu(900000), Emu(500000), s["num"].zfill(2), 14, ORANGE, bold=True)
            add_text(sl, margin, Emu(420000), W - 2 * margin, Emu(700000), s["title"], 28, WHITE, bold=True)
            # message essentiel
            rect(sl, margin, Emu(1350000), Emu(70000), Emu(520000), ORANGE)
            add_text(sl, margin + Emu(150000), Emu(1330000), W - 2 * margin, Emu(600000), s.get("message", ""), 18, OCEAN, bold=True)
            # contenu visible (colonne gauche)
            col_w = Emu(5900000)
            tf = add_text(sl, margin, Emu(2100000), col_w, Emu(4200000), "", 18, NAVY)
            for j, item in enumerate(s["contenu"][:6]):
                p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                p.text = "▸  " + item
                p.font.size = Pt(18)
                p.font.color.rgb = NAVY
                p.font.name = "Montserrat"
                p.space_after = Pt(10)
            # emplacement visuel (colonne droite)
            vx = margin + col_w + Emu(300000)
            vw = W - vx - margin
            box = rect(sl, vx, Emu(2100000), vw, Emu(4100000), LIGHT)
            box.line.color.rgb = OCEAN
            box.line.dash_style = 4
            vt = box.text_frame
            vt.word_wrap = True
            vt.paragraphs[0].text = "VISUEL RECOMMANDÉ"
            vt.paragraphs[0].font.size = Pt(12)
            vt.paragraphs[0].font.bold = True
            vt.paragraphs[0].font.color.rgb = ORANGE
            p = vt.add_paragraph()
            p.text = s.get("visuel", "")
            p.font.size = Pt(13)
            p.font.color.rgb = GREY
            # pied de page
            add_text(sl, margin, H - Emu(420000), W - 2 * margin, Emu(300000),
                     "Masterclass Cross-Trade International · Données fictives et pédagogiques", 10, GREY)

        notes = sl.notes_slide.notes_text_frame
        notes.text = (
            f"MESSAGE ESSENTIEL : {s.get('message', '')}\n\n"
            f"NOTES DU PROFESSEUR : {s.get('notes', '')}\n\n"
            f"EXPLICATION ORALE : {s.get('oral', '')}\n\n"
            f"EXEMPLE CONCRET : {s.get('exemple', '')}\n\n"
            f"TRANSITION : {s.get('transition', '')}\n\n"
            f"VISUEL : {s.get('visuel', '')}"
        )
    prs.save(OUTPUT)
    return len(slides)


if __name__ == "__main__":
    data = parse(SOURCE.read_text(encoding="utf-8"))
    missing = [s["num"] for s in data if not all(k in s for k in FIELDS.values() if k != "contenu")]
    if missing:
        sys.exit(f"Champs manquants dans les diapositives : {missing}")
    n = build(data)
    print(f"{n} diapositives générées → {OUTPUT}")
