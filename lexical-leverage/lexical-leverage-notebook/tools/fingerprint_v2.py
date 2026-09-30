
import re, colorsys
from collections import Counter

GENERIC_SANS = {"-apple-system","blinkmacsystemfont","system-ui","segoe ui","roboto","helvetica","helvetica neue","arial","sans-serif","ui-sans-serif"}
SERIFS = {"georgia","times","times new roman","garamond","playfair display","merriweather","lora","cormorant","cormorant garamond","dm serif display","libre baskerville","crimson text","eb garamond","fraunces","source serif pro","serif","ui-serif"}
MONOS = {"jetbrains mono","fira code","ibm plex mono","space mono","courier","courier new","monospace","ui-monospace","sf mono","menlo","consolas"}

def css_of(html):
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))

def css_vars(css):
    return {k.strip(): v.strip() for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", css)}

def resolve(val, V, depth=0):
    if val is None or depth > 5: return val
    def sub(m):
        name, fb = m.group(1).strip(), m.group(2)
        return V.get(name, fb.strip() if fb else "")
    out = re.sub(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^)]+))?\)", sub, val)
    return resolve(out, V, depth + 1) if "var(" in out else out

def rules(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [(s.strip(), b) for s, b in re.findall(r"([^{}@]+)\{([^{}]*)\}", css)]

def prop(body, name):
    m = re.findall(rf"(?<![\w-]){name}\s*:\s*([^;]+)", body, re.I)
    return m[-1].strip() if m else None

def first_family(val):
    if not val: return None
    return val.split(",")[0].strip(" '\"").lower()

def family_class(f):
    if f is None: return None
    if f in SERIFS: return "serif"
    if f in MONOS: return "mono"
    if f in GENERIC_SANS: return "system-sans"
    return "named-sans"

def to_hex(c):
    if not c: return None
    m = re.search(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", c)
    if m:
        h = m.group(1); return "#" + ("".join(x*2 for x in h) if len(h) == 3 else h).lower()
    m = re.search(r"rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)", c)
    if m: return "#%02x%02x%02x" % tuple(int(x) for x in m.groups())
    named = {"white": "#ffffff", "black": "#000000"}
    for k, v in named.items():
        if re.search(rf"\b{k}\b", c, re.I): return v
    return None

def hls(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5)); return colorsys.rgb_to_hls(r, g, b)

def hue_family(h):
    H, L, S = hls(h)
    if S < 0.15 or L < 0.08 or L > 0.95: return "neutral"
    d = H * 360
    for lo, hi, name in [(0,15,"red"),(15,45,"orange"),(45,70,"yellow"),(70,165,"green"),(165,200,"cyan"),(200,255,"blue"),(255,290,"purple"),(290,335,"pink"),(335,361,"red")]:
        if lo <= d < hi: return name

def fingerprint_html(html):
    css = css_of(html); V = css_vars(css); R = rules(css)
    def find(selpat, name):
        val = None
        for s, b in R:
            if re.search(selpat, s, re.I):
                v = prop(b, name)
                if v: val = v
        return resolve(val, V)
    body_font = first_family(find(r"(^|,|\s)(body|html|\*)(\s*$|,)", "font-family"))
    head_font = first_family(find(r"(^|,|\s)(h1)(\s*$|,|\b)", "font-family")) or body_font
    bg = to_hex(find(r"(^|,|\s)(body|html)(\s*$|,)", "background-color") or find(r"(^|,|\s)(body|html)(\s*$|,)", "background"))
    fg = to_hex(find(r"(^|,|\s)(body|html)(\s*$|,)", "color"))
    allc = [to_hex(x) for x in re.findall(r"#[0-9a-fA-F]{3,6}\b|rgba?\([^)]*\)", resolve(css, V))]
    allc = [c for c in allc if c]
    sat = [c for c in allc if hue_family(c) not in ("neutral", None)]
    accent = Counter(sat).most_common(1)[0][0] if sat else None
    radii = [float(x) for x in re.findall(r"border-radius\s*:\s*([\d.]+)px", resolve(css, V))]
    maxw = [int(x) for x in re.findall(r"max-width\s*:\s*(\d+)px", resolve(css, V))]
    grads = re.findall(r"(?:linear|radial|conic)-gradient\(", css)
    return dict(
        body_font=body_font, body_font_class=family_class(body_font),
        heading_font=head_font, heading_font_class=family_class(head_font),
        bg=bg, bg_lightness=round(hls(bg)[1], 2) if bg else None,
        dark_theme=(hls(bg)[1] < 0.5) if bg else None,
        accent=accent, accent_hue=hue_family(accent) if accent else None,
        n_distinct_colors=len(set(allc)), n_gradients=len(grads),
        max_radius_px=max(radii) if radii else 0, container_px=max(maxw) if maxw else None,
        n_keyframes=len(re.findall(r"@keyframes", css)), uses_backdrop_blur="backdrop-filter" in css,
        n_sections=len(re.findall(r"<section\b", html, re.I)), html_chars=len(html),
    )
