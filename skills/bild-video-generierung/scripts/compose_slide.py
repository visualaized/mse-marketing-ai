#!/usr/bin/env python3
"""
compose_slide.py — MSE Filterpressen GmbH

Komponiert EIN markenkonformes, flaches Bild (Hintergrund + Eyebrow + Headline + optional
Body-Text + optional CTA-Pille + Logo/Bildzeichen-Ecke) für Social-Media-Carousel-/Mehrbild-Posts,
E-Mail-Signatur-Banner o. ä. — nach demselben Prinzip wie das Signatur-Banner der Marketing-Zentrale:
echte Nudica-Schriftdatei statt System-Font, echtes Logo-Asset statt Klartext.

Lesbarkeit — zwei Mittel, beide dezent (KEIN harter, versetzter Umriss und KEIN flächiges Overlay
über dem gesamten Bild):
1. Ein nach oben ausblendender Verlaufs-Scrim NUR im Textbereich (unterer Bildbereich).
2. Bei hellem Text auf Foto-Hintergrund zusätzlich ein LEICHTER, WEICHER Schatten direkt hinter
   den Buchstaben (Gaussian-Blur, minimaler Versatz) — Kundenvorgabe: landet helle Schrift auf
   hellen Bildbereichen (z. B. Edelstahlflächen), muss sie sich per Soft-Schatten abheben.

Zwei Hintergrund-Modi:
  --background <Datei>     Fotografischer Hintergrund (Standardfall, object-fit:cover-Zuschnitt).
  --bg-color <#RRGGBB>     Flächiger Marken-Farbhintergrund für Diagramm-/Infografik-Slides (z. B.
                            ein Prozessschritt-Schaubild) — nur Marken-Farben verwenden (siehe
                            brand/color-palette.json): Fast White #FFFFFF, Light Grey #F5F5F5,
                            Anthracite Black #1B1B1B. Bei hellem --bg-color automatisch dunkle
                            Schrift verwenden (--dark-text), bei dunklem Hintergrund weiße Schrift
                            (Standard).
Genau eines der beiden Argumente ist Pflicht.

Nur Python-Standardbibliothek + Pillow (bereits in dieser Umgebung verfügbar) — kein Build-Schritt.

Beispiel (Foto-Hintergrund):
  python3 compose_slide.py \\
    --background "Outputs/2026-07-01-celltron-launch/celltron-hero-vollansicht.png" \\
    --font-dir "brand/fonts/Nudica/Nudica Complete Desktop" \\
    --logo "brand/logo/MSE Favicon.png" \\
    --eyebrow "PRODUKTNEUHEIT — CELLTRON SERIE" \\
    --headline "CellTRON Xtreme." \\
    --body "Vollständig eingehaust. Gasdicht. Für die anspruchsvollsten Medien." \\
    --index "1/4" \\
    --width 1080 --height 1350 \\
    --out "Outputs/2026-07-01-celltron-launch/carousel/slide-1.png"

Beispiel (Diagramm-Slide mit Marken-Farbfläche statt Foto):
  python3 compose_slide.py \\
    --bg-color "#F5F5F5" --dark-text \\
    --font-dir "brand/fonts/Nudica/Nudica Complete Desktop" \\
    --logo "brand/logo/MSE Favicon.png" \\
    --eyebrow "SO FUNKTIONIERT ES" \\
    --headline "3 Schritte zur passgenauen Filtrationsloesung." \\
    --width 1080 --height 1350 \\
    --out "Outputs/.../carousel/slide-diagramm.png"

Aufruf-Parameter im Detail: --help.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def parse_args():
    p = argparse.ArgumentParser(description="Komponiert eine markenkonforme Social-/Signatur-Slide.")
    bg_group = p.add_mutually_exclusive_group(required=True)
    bg_group.add_argument("--background", help="Pfad zum fotografischen Hintergrundbild.")
    bg_group.add_argument("--bg-color", help="Flächiger Marken-Farbhintergrund als Hex, z. B. '#1B1B1B' (fuer Diagramm-/Infografik-Slides ohne Foto).")
    p.add_argument("--dark-text", action="store_true", help="Dunkle (anthrazitfarbene) statt weisse Schrift verwenden — bei hellem --bg-color noetig.")
    p.add_argument("--font-dir", required=True, help="Ordner mit Nudica-Regular.otf und Nudica-Bold.otf.")
    p.add_argument("--logo", default=None, help="Pfad zum Logo/Bildzeichen (z. B. MSE Favicon.png). Optional, aber empfohlen — immer verwenden, wenn vorhanden.")
    p.add_argument("--eyebrow", default="", help="Kurzes, getracktes Label ueber der Headline (z. B. Kampagnen-/Serienname).")
    p.add_argument("--headline", required=True, help="Haupttext der Slide (kurz, 1-2 Zeilen).")
    p.add_argument("--body", default="", help="Optionaler kurzer Fliesstext unter der Headline (max. ~2-3 Zeilen).")
    p.add_argument("--cta", default="", help="Optionaler CTA-Pill-Text (nur auf der letzten Slide eines Carousels sinnvoll).")
    p.add_argument("--index", default="", help="Optionale Fortschrittsanzeige, z. B. '2/5' (klein, Ecke oben rechts).")
    p.add_argument("--width", type=int, default=1080, help="Ausgabebreite in px (Standard 1080 fuer Instagram).")
    p.add_argument("--height", type=int, default=1350, help="Ausgabehoehe in px (Standard 1350 = 4:5-Hochformat).")
    p.add_argument("--crop-bias", type=float, default=0.25, help="Vertikale Crop-Verschiebung 0..1 (0=oben, 1=unten); Standard 0.25 laesst Kopfraum fuer Text.")
    p.add_argument("--no-scrim", action="store_true", help="Textbereich-Scrim deaktivieren (nur sinnvoll, wenn der Bildausschnitt am Textplatz ohnehin schon dunkel/hell genug ist).")
    p.add_argument("--out", required=True, help="Ausgabepfad (PNG).")
    return p.parse_args()


# MSE-Markenfarben (siehe brand/color-palette.json) — hier hart hinterlegt, damit das Skript
# ohne JSON-Parsing lauffaehig ist; bei Aenderung der Farbpalette hier UND in color-palette.json pflegen.
ANTHRACITE = (27, 27, 27)
WHITE = (255, 255, 255)
MEDIUM_GREY = (112, 112, 112)
LIGHT_GREY_TEXT = (226, 226, 226)


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cover_crop(img, target_w, target_h, vertical_bias=0.25):
    """Skaliert/croppt ein Bild im 'object-fit: cover'-Stil auf exakt target_w x target_h."""
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        x0 = (src_w - new_w) // 2
        img = img.crop((x0, 0, x0 + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        y0 = int((src_h - new_h) * vertical_bias)
        img = img.crop((0, y0, src_w, y0 + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def apply_text_scrim(canvas, zone_top, width, height, dark_text):
    """Dezenter Verlaufs-Scrim NUR im Textbereich (kein Schatten auf Buchstaben, kein Overlay
    über das gesamte Bild) — blendet von transparent (zone_top) auf ein gedecktes Anthrazit
    (bzw. bei hellem Untergrund ein gedecktes Weiss) am unteren Bildrand aus, damit Text darüber
    ohne Schlagschatten lesbar bleibt."""
    zone_height = height - zone_top
    if zone_height <= 0:
        return canvas
    gradient = Image.new("L", (1, zone_height), color=0)
    max_alpha = 190
    for y in range(zone_height):
        alpha = int(max_alpha * (y / zone_height) ** 1.4)
        gradient.putpixel((0, y), alpha)
    gradient = gradient.resize((width, zone_height))
    scrim_color = WHITE if dark_text else ANTHRACITE
    scrim = Image.new("RGBA", (width, zone_height), scrim_color + (0,))
    scrim.putalpha(gradient)
    canvas.alpha_composite(scrim, (0, zone_top))
    return canvas


def draw_tracked_text(draw, pos, text, font, fill, tracking=2):
    """Zeichnet Text mit manuellem Letter-Spacing (Pillow kennt kein natives Tracking) — ohne
    Schlagschatten/Umriss, reine, saubere Typografie."""
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def wrap_text(draw, text, font, max_width):
    """Einfacher Wortumbruch anhand der tatsaechlichen Textbreite."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    args = parse_args()
    font_dir = Path(args.font_dir)

    bold = ImageFont.truetype(str(font_dir / "Nudica-Bold.otf"), max(28, args.width // 22))
    regular = ImageFont.truetype(str(font_dir / "Nudica-Regular.otf"), max(20, args.width // 34))
    eyebrow_font = ImageFont.truetype(str(font_dir / "Nudica-Bold.otf"), max(16, args.width // 55))
    cta_font = ImageFont.truetype(str(font_dir / "Nudica-Bold.otf"), max(16, args.width // 55))
    index_font = ImageFont.truetype(str(font_dir / "Nudica-Regular.otf"), max(14, args.width // 65))

    if args.background:
        bg = Image.open(args.background).convert("RGB")
        bg = cover_crop(bg, args.width, args.height, args.crop_bias)
        canvas = bg.convert("RGBA")
    else:
        canvas = Image.new("RGBA", (args.width, args.height), hex_to_rgb(args.bg_color) + (255,))

    draw = ImageDraw.Draw(canvas)

    text_color = ANTHRACITE if args.dark_text else WHITE
    secondary_text_color = MEDIUM_GREY if args.dark_text else LIGHT_GREY_TEXT
    index_color = ANTHRACITE if args.dark_text else WHITE
    eyebrow_color = MEDIUM_GREY if args.dark_text else LIGHT_GREY_TEXT

    margin = int(args.width * 0.08)
    max_text_width = args.width - 2 * margin

    # Logo/Bildzeichen oben links — IMMER einsetzen, wenn --logo angegeben ist (Markenpflicht).
    if args.logo:
        logo_img = Image.open(args.logo).convert("RGBA")
        logo_w = int(args.width * 0.07)
        ratio = logo_w / logo_img.width
        logo_img = logo_img.resize((logo_w, int(logo_img.height * ratio)), Image.LANCZOS)
        canvas.alpha_composite(logo_img, (margin, margin))

    # Fortschrittsanzeige oben rechts (z. B. "2/5")
    if args.index:
        idx_w = draw.textlength(args.index, font=index_font)
        draw.text((args.width - margin - idx_w, margin), args.index, font=index_font, fill=index_color)

    # Gesamthoehe des Textblocks VORAB messen, damit der Block bei flachen Formaten (z. B.
    # Signatur-Banner 1184x420) nach oben verschoben werden kann statt unten aus dem Bild zu
    # laufen — der CTA-Button darf NIE abgeschnitten werden.
    block_height = 0
    if args.eyebrow:
        block_height += int(eyebrow_font.size * 1.8)
    block_height += len(wrap_text(draw, args.headline, bold, max_text_width)) * int(bold.size * 1.18)
    if args.body:
        block_height += int(bold.size * 0.25)
        block_height += len(wrap_text(draw, args.body, regular, max_text_width)) * int(regular.size * 1.35)
    if args.cta:
        circle_d_probe = int(args.width * 0.045)
        pad_y_probe = int(args.width * 0.022)
        block_height += int(args.height * 0.03) + int(circle_d_probe + pad_y_probe)

    # Text-Startposition: Standard bei 62 % Bildhoehe, aber nach oben begrenzt, sodass der
    # gesamte Block (inkl. CTA) mit einem unteren Sicherheitsabstand vollstaendig ins Bild passt.
    bottom_margin = max(int(args.height * 0.07), int(args.width * 0.04))
    y_start = min(int(args.height * 0.62), args.height - bottom_margin - block_height)
    y_start = max(y_start, margin)  # nie mit dem Logo oben kollidieren lassen

    # Scrim-Zone (nur bei Foto-Hintergrund noetig; bei einer flaechigen Marken-Farbe ist der
    # Kontrast ohnehin garantiert, kein Scrim noetig).
    if args.background and not args.no_scrim:
        apply_text_scrim(canvas, zone_top=y_start - int(args.height * 0.05), width=args.width, height=args.height, dark_text=args.dark_text)
        draw = ImageDraw.Draw(canvas)  # neu binden, da alpha_composite ein neues Bildobjekt-Backing nutzt

    # Der gesamte Textblock wird auf eine SEPARATE, transparente Ebene gezeichnet. Bei hellem
    # Text auf Foto-Hintergrund wird darunter eine weich geblurte, dunkle Kopie der Ebene gelegt
    # (dezenter Soft-Schatten) — Kundenvorgabe: landet helle Schrift auf hellen Bildbereichen,
    # braucht sie einen leichten Schatten zum Abheben. Das ist bewusst KEIN harter, versetzter
    # Umriss (der frühere Per-Buchstaben-Offset-Schatten sah nach Effekt-Spielerei aus), sondern
    # ein weicher Blur direkt hinter den Buchstaben.
    text_layer = Image.new("RGBA", (args.width, args.height), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_layer)

    y = y_start

    if args.eyebrow:
        draw_tracked_text(tdraw, (margin, y), args.eyebrow.upper(), eyebrow_font, eyebrow_color, tracking=3)
        y += int(eyebrow_font.size * 1.8)

    for line in wrap_text(tdraw, args.headline, bold, max_text_width):
        tdraw.text((margin, y), line, font=bold, fill=text_color)
        y += int(bold.size * 1.18)

    if args.body:
        y += int(bold.size * 0.25)
        for line in wrap_text(tdraw, args.body, regular, max_text_width):
            tdraw.text((margin, y), line, font=regular, fill=secondary_text_color)
            y += int(regular.size * 1.35)

    if args.cta:
        y += int(args.height * 0.03)
        pad_x, pad_y = int(args.width * 0.035), int(args.width * 0.022)
        circle_d = int(args.width * 0.045)
        label_w = tdraw.textlength(args.cta.upper(), font=cta_font) + len(args.cta) * 1.5
        pill_w = int(pad_x * 2 + label_w + 14 + circle_d)
        pill_h = int(circle_d + pad_y)
        pill_bg = WHITE if not args.dark_text else ANTHRACITE
        pill_fg = ANTHRACITE if not args.dark_text else WHITE
        tdraw.rounded_rectangle([margin, y, margin + pill_w, y + pill_h], radius=pill_h // 2, fill=pill_bg)
        draw_tracked_text(tdraw, (margin + pad_x, y + pill_h // 2 - cta_font.size // 2), args.cta.upper(), cta_font, pill_fg, tracking=1.5)
        cx0 = margin + pill_w - pad_x - circle_d
        cy0 = y + (pill_h - circle_d) // 2
        tdraw.ellipse([cx0, cy0, cx0 + circle_d, cy0 + circle_d], outline=pill_fg, width=2)
        acx, acy = cx0 + circle_d // 2, cy0 + circle_d // 2
        r = circle_d * 0.22
        tdraw.line([acx - r, acy + r, acx + r, acy - r], fill=pill_fg, width=2)
        tdraw.line([acx + r, acy - r, acx, acy - r], fill=pill_fg, width=2)
        tdraw.line([acx + r, acy - r, acx + r, acy], fill=pill_fg, width=2)

    # Soft-Schatten: nur bei hellem Text auf Foto-Hintergrund (dort kann die Schrift auf helle
    # Bildbereiche treffen — z. B. Edelstahlflächen); auf flächigen Marken-Farben ist der
    # Kontrast ohnehin garantiert.
    if args.background and not args.dark_text:
        shadow_alpha = text_layer.split()[3].point(lambda a: int(a * 0.55))
        shadow = Image.new("RGBA", text_layer.size, (0, 0, 0, 0))
        shadow.paste((13, 14, 17, 255), mask=shadow_alpha)
        shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(3, args.width // 300)))
        offset = max(1, args.width // 550)
        canvas.alpha_composite(shadow, (0, offset))

    canvas.alpha_composite(text_layer)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out_path, "PNG")
    print(f"Slide gespeichert: {out_path}")


if __name__ == "__main__":
    sys.exit(main())
