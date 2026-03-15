"""
app.py
------
BrandSphere AI — Main Streamlit Application
CRS AI Capstone 2025-26 | Scenario 1

Tabs:
  1. 🏠 Home
  2. 🎯 Brand Inputs
  3. 🎨 Logo Studio
  4. 🖋  Fonts & Palette
  5. ✍️  Slogans & Content
  6. 📣  Campaign Analytics
  7. 🌍  Multilingual Studio
  8. 🎬  Animation Preview
  9. ⭐  Feedback
  10. 📦  Download Kit
"""

import os, sys, uuid, json, re, time, datetime, logging
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ── Path setup ──────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Streamlit page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandSphere AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');
:root {
  --bg:#0C0D0F; --surface:#141518; --surface2:#1C1E22; --border:#2A2C31;
  --accent:#C9A84C; --accent2:#E8C97A; --teal:#3ECFB2; --red:#E05A5A;
  --text:#F0EDE8; --muted:#7A7A85;
  --font-head:'Cormorant Garamond',Georgia,serif;
  --font-body:'DM Sans',sans-serif;
  --font-mono:'Space Mono',monospace;
}
*, *::before, *::after { box-sizing:border-box; }
html, body, .stApp { background:var(--bg) !important; color:var(--text) !important; font-family:var(--font-body); }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:0 !important; max-width:100% !important; }
section[data-testid="stSidebar"] { display:none; }
::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-track { background:var(--bg); } ::-webkit-scrollbar-thumb { background:var(--accent); border-radius:2px; }
.nav-bar { display:flex; align-items:center; justify-content:space-between; padding:16px 48px; background:var(--surface); border-bottom:1px solid var(--border); }
.nav-logo { font-family:var(--font-head); font-size:1.6rem; font-weight:700; color:var(--accent); letter-spacing:0.03em; }
.nav-logo span { color:var(--text); font-weight:300; }
.nav-tag  { font-family:var(--font-mono); font-size:0.62rem; color:var(--muted); letter-spacing:0.15em; text-transform:uppercase; }
.hero { background:linear-gradient(135deg,#0C0D0F 0%,#141518 60%,#0f1015 100%); padding:80px 48px 56px; border-bottom:1px solid var(--border); position:relative; overflow:hidden; }
.hero::before { content:''; position:absolute; top:-60px; right:-60px; width:500px; height:500px; background:radial-gradient(circle,rgba(201,168,76,0.08) 0%,transparent 70%); pointer-events:none; }
.hero-eyebrow { font-family:var(--font-mono); font-size:0.7rem; letter-spacing:0.25em; color:var(--accent); text-transform:uppercase; margin-bottom:16px; }
.hero-title { font-family:var(--font-head); font-size:clamp(2.6rem,5vw,4.6rem); font-weight:300; line-height:1.08; margin-bottom:12px; }
.hero-title em { font-style:italic; color:var(--accent); }
.hero-sub { font-size:1rem; font-weight:300; color:var(--muted); max-width:540px; line-height:1.72; margin-bottom:36px; }
.badge-row { display:flex; gap:10px; flex-wrap:wrap; }
.badge { display:inline-block; padding:5px 14px; border:1px solid var(--border); border-radius:20px; font-family:var(--font-mono); font-size:0.6rem; color:var(--muted); letter-spacing:0.1em; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important; border-bottom:1px solid var(--border) !important; padding:0 48px !important; gap:0 !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; border:none !important; color:var(--muted) !important; font-family:var(--font-mono) !important; font-size:0.65rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; padding:15px 18px !important; margin:0 !important; transition:color 0.2s !important; }
.stTabs [aria-selected="true"] { color:var(--accent) !important; border-bottom:2px solid var(--accent) !important; }
.stTabs [data-baseweb="tab-panel"] { padding:36px 48px !important; background:var(--bg) !important; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div { background:var(--surface2) !important; border:1px solid var(--border) !important; border-radius:6px !important; color:var(--text) !important; font-family:var(--font-body) !important; font-size:0.92rem !important; }
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus { border-color:var(--accent) !important; box-shadow:0 0 0 2px rgba(201,168,76,0.15) !important; }
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stRadio label { color:var(--muted) !important; font-family:var(--font-mono) !important; font-size:0.62rem !important; letter-spacing:0.12em !important; text-transform:uppercase !important; }
.stButton>button { background:var(--accent) !important; color:#0C0D0F !important; border:none !important; border-radius:4px !important; font-family:var(--font-mono) !important; font-size:0.68rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; padding:11px 26px !important; transition:all 0.2s !important; }
.stButton>button:hover { background:var(--accent2) !important; transform:translateY(-1px) !important; box-shadow:0 4px 18px rgba(201,168,76,0.3) !important; }
.stDownloadButton>button { background:transparent !important; color:var(--accent) !important; border:1px solid var(--accent) !important; border-radius:4px !important; font-family:var(--font-mono) !important; font-size:0.68rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; padding:11px 26px !important; }
.stDownloadButton>button:hover { background:rgba(201,168,76,0.1) !important; }
.card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:26px; margin-bottom:14px; }
.card:hover { border-color:rgba(201,168,76,0.35); }
.card-title { font-family:var(--font-head); font-size:1.25rem; font-weight:600; color:var(--text); margin-bottom:5px; }
.card-sub { font-size:0.82rem; color:var(--muted); line-height:1.65; margin-bottom:16px; }
.sec-label { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.25em; color:var(--accent); text-transform:uppercase; margin-bottom:7px; }
.sec-title { font-family:var(--font-head); font-size:1.9rem; font-weight:300; color:var(--text); margin-bottom:5px; }
.sec-title em { font-style:italic; color:var(--accent); }
.divider { height:1px; background:var(--border); margin:28px 0; }
.metric-card { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:20px; text-align:center; }
.metric-val { font-family:var(--font-head); font-size:2.2rem; font-weight:700; color:var(--accent); display:block; }
.metric-lbl { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; color:var(--muted); text-transform:uppercase; margin-top:3px; }
.swatch-row { display:flex; gap:8px; margin:14px 0; }
.swatch { flex:1; height:50px; border-radius:6px; display:flex; align-items:flex-end; padding:5px 8px; font-family:var(--font-mono); font-size:0.52rem; color:rgba(255,255,255,0.75); }
.tagline-card { background:var(--surface2); border-left:3px solid var(--accent); padding:15px 18px; border-radius:0 8px 8px 0; margin:7px 0; font-family:var(--font-head); font-size:1.1rem; font-style:italic; color:var(--text); line-height:1.55; }
.lang-card { background:var(--surface2); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin:5px 0; }
.lang-name { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; color:var(--accent); text-transform:uppercase; margin-bottom:4px; }
.lang-text { font-family:var(--font-head); font-size:1rem; font-style:italic; color:var(--text); }
.pill { display:inline-block; padding:3px 11px; border-radius:20px; font-family:var(--font-mono); font-size:0.57rem; letter-spacing:0.1em; text-transform:uppercase; }
.pill-g { background:rgba(62,207,178,0.15); color:#3ECFB2; border:1px solid rgba(62,207,178,0.3); }
.pill-a { background:rgba(201,168,76,0.15); color:#C9A84C; border:1px solid rgba(201,168,76,0.3); }
.pill-r { background:rgba(224,90,90,0.15); color:#E05A5A; border:1px solid rgba(224,90,90,0.3); }
.prog-wrap { background:var(--surface2); border-radius:4px; height:8px; overflow:hidden; margin:7px 0; }
.prog-bar { height:100%; border-radius:4px; background:linear-gradient(90deg,var(--accent),var(--teal)); transition:width 0.6s ease; }
.check-item { display:flex; align-items:flex-start; gap:10px; padding:9px 0; border-bottom:1px solid var(--border); }
.logo-svg-wrap { border:2px solid var(--border); border-radius:10px; padding:16px; background:var(--surface2); cursor:pointer; transition:border-color 0.2s; display:flex; flex-direction:column; align-items:center; gap:8px; }
.logo-svg-wrap:hover { border-color:var(--accent); }
.logo-svg-wrap.selected { border-color:var(--accent); background:rgba(201,168,76,0.06); }
.nltk-pill { display:inline-block; padding:3px 10px; border-radius:14px; font-family:var(--font-mono); font-size:0.55rem; background:rgba(201,168,76,0.12); color:var(--accent); border:1px solid rgba(201,168,76,0.25); margin:2px; }
.stAlert { background:var(--surface2) !important; border:1px solid var(--border) !important; }
.stSpinner>div { border-top-color:var(--accent) !important; }
@media (max-width:640px) { .stTabs [data-baseweb="tab-panel"] { padding:20px !important; } .hero { padding:40px 20px 36px; } }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
def _init():
    defaults = {
        "session_id":    str(uuid.uuid4())[:8],
        "brand_inputs":  {},
        "logos":         [],
        "selected_logo": 0,
        "palette":       {},
        "fonts":         [],
        "slogans":       [],
        "retrieved":     [],
        "brand_story":   "",
        "translations":  {},
        "campaigns":     {},
        "kpis":          {},
        "aesthetics":    {},
        "gif_bytes":     None,
        "feedback_log":  [],
        "gemini_ok":     False,
        "api_key":       "",
        "chat_history":  [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── Gemini config ──────────────────────────────────────────────────────────
def configure_gemini(key: str) -> bool:
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        st.session_state.gemini_ok  = True
        st.session_state.api_key    = key
        os.environ["GEMINI_API_KEY"] = key
        return True
    except Exception:
        return False

def gemini_call(prompt: str, system: str = "") -> str:
    if not st.session_state.gemini_ok:
        return ""
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel("gemini-2.0-flash",
                                       system_instruction=system or None)
        return model.generate_content(prompt).text.strip()
    except Exception as e:
        return ""

# ── Auto-configure from env / streamlit secrets ────────────────────────────
_env_key = os.getenv("GEMINI_API_KEY", "")
if not _env_key:
    try:
        _env_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass
if _env_key and not st.session_state.gemini_ok:
    configure_gemini(_env_key)

# ── Import src modules ─────────────────────────────────────────────────────
from src.config import (INDUSTRIES, PERSONALITIES, TONES, PLATFORMS,
                         REGIONS, LANGUAGES_SUPPORTED, CAMPAIGN_OBJECTIVES, COLOR_NAMES)
from src.palette_engine   import generate_palette, score_palette_harmony
from src.font_engine      import recommend_fonts
from src.logo_engine      import generate_all_logos, svg_to_png_bytes
from src.slogan_engine    import generate_slogans, nltk_analyze
from src.aesthetics_engine import score_brand, gemini_recommendations
from src.multilingual_engine import translate_slogan, validate_translations
from src.animation_engine  import create_brand_gif
from src.feedback_engine   import save_feedback, load_feedback, get_summary
from src.export_engine     import build_brand_kit_zip
from src.dashboard_engine  import (kpi_bar_chart, regional_engagement_map,
                                    personality_radar, feedback_bar, feedback_pie,
                                    campaign_scatter)

# ── Lazy campaign predictor ────────────────────────────────────────────────
@st.cache_resource
def get_predictor():
    from src.campaign_predictor import predictor
    predictor._load()
    return predictor

# ── Campaign content helper ────────────────────────────────────────────────
DEMO_CAMPAIGN = {
    "caption": "Introducing {company} — where {industry} meets intelligent design.\nBuilt for the future. Crafted for you. {tag}\n👉 Tap the link.",
    "hashtags": ["#{co}", "#BrandStrategy", "#AIBranding", "#Innovation", "#DigitalMarketing",
                 "#BrandIdentity", "#StartupLife", "#MarketingAI", "#GrowthHacking", "#ProductLaunch"],
    "regional_strategy": "Focus on culturally resonant visuals and localized CTAs for {region}.",
}

def generate_campaign_content(bi, platform, region, objective):
    co  = bi.get("company", "Brand")
    ind = bi.get("industry", "Technology")
    tag = st.session_state.slogans[0]["text"] if st.session_state.slogans else f"Discover {co}"
    if st.session_state.gemini_ok:
        prompt = (
            f"Create a {platform} marketing campaign.\n"
            f"Company: {co} | Industry: {ind} | Objective: {objective} | Region: {region}\n"
            f"Tagline: \"{tag}\"\n\n"
            "Return JSON only: {\"caption\":\"...\",\"hashtags\":[\"...\"],\"regional_strategy\":\"...\"}"
        )
        raw = gemini_call(prompt)
        try:
            return json.loads(re.sub(r"```json|```", "", raw).strip())
        except Exception:
            pass
    return {
        "caption": DEMO_CAMPAIGN["caption"].format(company=co, industry=ind.lower(), tag=tag),
        "hashtags": [h.replace("{co}", co.replace(" ","")) for h in DEMO_CAMPAIGN["hashtags"]],
        "regional_strategy": DEMO_CAMPAIGN["regional_strategy"].format(region=region),
    }

def generate_brand_story(bi):
    co, ind, tone, aud = (bi.get("company",""), bi.get("industry",""),
                           bi.get("tone",""), bi.get("audience",""))
    if st.session_state.gemini_ok:
        return gemini_call(
            f"Write a 110-word brand story for {co} in the {ind} industry. "
            f"Tone: {tone}. Audience: {aud}. Write in second person. Be inspiring.",
            system="You are a brand narrative writer. Be specific, not generic."
        )
    return (
        f"{co} was built with one conviction: that great brands don't happen by accident — "
        f"they are engineered with intention.\n\n"
        f"In the competitive {ind.lower()} landscape, standing out requires more than a logo. "
        f"It demands a voice that resonates, a visual identity that commands attention, "
        f"and a message that converts.\n\n"
        f"Your brand is your most valuable asset. At {co}, every design decision, "
        f"every word, every colour choice is a deliberate act of strategic storytelling.\n\n"
        f"This is your story. Tell it boldly."
    )

# ══════════════════════════════════════════════════════════════════════════════
#  NEW FEATURE HELPERS
# ══════════════════════════════════════════════════════════════════════════════

# ── Brand Name Generator ───────────────────────────────────────────────────────
def generate_brand_names(industry: str, personality: str, keywords: str) -> list[dict]:
    """Generate creative brand name suggestions."""
    if st.session_state.gemini_ok:
        pers_lower = personality.lower()
        kw_str     = keywords or "none"
        prompt_bn  = (
            f"Generate 8 creative, memorable brand names for a {pers_lower} {industry} company. "
            f"Keywords to consider: {kw_str}. "
            "For each name give: the name, a 1-line rationale, and a domain availability note. "
            "Return JSON only: array of objects with keys name, rationale, domain."
        )
        raw = gemini_call(prompt_bn)
        try:
            import re as _re
            data = json.loads(_re.sub(r"```json|```","",raw).strip())
            return data if isinstance(data, list) else []
        except Exception:
            pass
    # Offline fallback
    prefixes = {"Minimalist":["Clear","Pure","Axe","Arc","Mono"],
                "Luxury":["Lumé","Auré","Velux","Prism","Onyx"],
                "Bold":["Apex","Forge","Blaze","Titan","Surge"],
                "Vibrant":["Zest","Spark","Vivid","Nova","Flare"],
                "Professional":["Nexus","Vector","Axiom","Core","Strata"],
                "Playful":["Poppy","Ziggy","Bubbl","Whirl","Sunny"],
                "Elegant":["Seré","Luma","Crest","Elara","Muse"]}
    import random
    pfx = prefixes.get(personality, prefixes["Professional"])
    ind_short = industry.split("/")[0].strip().replace(" ","")[:5]
    names = []
    for p in random.sample(pfx, min(5, len(pfx))):
        names.append({"name": p + ind_short[:3].title(),
                      "rationale": f"Combines '{p}' energy with {industry.split('/')[0].strip().lower()} identity.",
                      "domain": f"{p.lower()}{ind_short.lower()}.com — check availability"})
    return names


# ── Color Accessibility Checker (WCAG) ────────────────────────────────────────
def check_wcag(palette: dict) -> list[dict]:
    """Check WCAG contrast ratios between palette color pairs."""
    from src.palette_engine import hex_to_rgb

    def relative_luminance(rgb):
        r, g, b = [v/255 for v in rgb]
        def linearize(c):
            return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
        return 0.2126*linearize(r) + 0.7152*linearize(g) + 0.0722*linearize(b)

    def contrast_ratio(l1, l2):
        lighter, darker = max(l1,l2), min(l1,l2)
        return round((lighter+0.05)/(darker+0.05), 2)

    colors = list(palette.items())
    results = []
    pairs = [(0,3),(0,2),(1,3),(1,4),(0,4)]  # primary/bg, primary/accent etc
    for i, j in pairs:
        if i < len(colors) and j < len(colors):
            n1, v1 = colors[i]; n2, v2 = colors[j]
            l1 = relative_luminance(hex_to_rgb(v1["hex"]))
            l2 = relative_luminance(hex_to_rgb(v2["hex"]))
            cr = contrast_ratio(l1, l2)
            aa   = "✅ Pass" if cr >= 4.5 else "⚠️ Fail"
            aaa  = "✅ Pass" if cr >= 7.0 else "⚠️ Fail"
            results.append({"pair": f"{n1} on {n2}",
                             "hex1": v1["hex"], "hex2": v2["hex"],
                             "ratio": cr, "AA": aa, "AAA": aaa})
    return results


# ── A/B Tagline Tester ─────────────────────────────────────────────────────────
def ab_test_taglines(taglines: list[dict], industry: str, audience: str) -> list[dict]:
    """Score taglines across 5 brand dimensions."""
    if st.session_state.gemini_ok and taglines:
        texts_str = " | ".join([s["text"] for s in taglines[:4]])
        aud_str   = audience or "general consumers"
        prompt_ab = (
            "Score these brand taglines for a " + industry + " brand targeting " + aud_str + ". "
            "Taglines: " + texts_str + ". "
            "Score each tagline from 1-10 on: Memorability, Clarity, Emotional Impact, Brand Fit, Uniqueness. "
            "Return a JSON array only. Each item must have keys: tagline, memorability, clarity, "
            "emotional_impact, brand_fit, uniqueness, overall (average of the 5 scores)."
        )
        raw = gemini_call(prompt_ab)
        try:
            import re as _re
            data = json.loads(_re.sub(r"```json|```", "", raw).strip())
            return data if isinstance(data, list) else []
        except Exception:
            pass
    import hashlib
    results = []
    for s in taglines[:4]:
        text = s["text"]
        h    = int(hashlib.md5(text.encode()).hexdigest(), 16) % 100
        mem  = min(10, max(5, 7 + (h % 4) - 1))
        cla  = min(10, max(5, 6 + (h % 5) - 1))
        emo  = min(10, max(5, 7 + (h % 3)))
        fit  = min(10, max(5, 8 + (h % 2) - 1))
        uni  = min(10, max(5, 6 + (h % 4)))
        results.append({"tagline": text[:50],
                        "memorability": mem, "clarity": cla,
                        "emotional_impact": emo, "brand_fit": fit,
                        "uniqueness": uni, "overall": round((mem+cla+emo+fit+uni)/5, 1)})
    return sorted(results, key=lambda x: -x["overall"])

# ── Social Media Post Previewer ────────────────────────────────────────────────
def generate_post_preview(company, industry, personality, platform, slogan, palette):
    """Generate platform-specific post content and preview data."""
    platforms_meta = {
        "Instagram": {"char_limit": 2200, "best_format": "Square image + carousel",
                      "cta": "👉 Link in bio", "hashtag_count": "10-15"},
        "LinkedIn":  {"char_limit": 3000, "best_format": "Article or document post",
                      "cta": "See more in comments", "hashtag_count": "3-5"},
        "Twitter/X": {"char_limit": 280,  "best_format": "Text + image",
                      "cta": "RT if you agree", "hashtag_count": "2-3"},
        "Facebook":  {"char_limit": 500,  "best_format": "Video or link post",
                      "cta": "Share with your network", "hashtag_count": "5-10"},
        "TikTok":    {"char_limit": 150,  "best_format": "Short vertical video 9:16",
                      "cta": "Sound on", "hashtag_count": "5-8"},
        "YouTube":   {"char_limit": 5000, "best_format": "Long-form video",
                      "cta": "Subscribe for more", "hashtag_count": "3-5"},
    }
    meta    = platforms_meta.get(platform, platforms_meta["Instagram"])
    colors  = list(palette.values())
    primary = colors[0]["hex"] if colors else "#1B3A6B"
    accent  = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"

    if st.session_state.gemini_ok:
        char_lim = str(meta["char_limit"])
        prompt_post = (
            "Write a " + platform + " marketing post for " + company + " (" + industry + ", " + personality + " brand). "
            "Tagline: " + slogan + ". Character limit: " + char_lim + ". "
            "Include a caption, 5 relevant hashtags, a CTA, and a scroll-stopping hook. "
            "Return JSON only with keys: caption, hashtags (array), cta, hook."
        )
        raw = gemini_call(prompt_post)
        try:
            import re as _re
            data = json.loads(_re.sub(r"```json|```", "", raw).strip())
            data.update(meta)
            data["primary"] = primary
            data["accent"]  = accent
            return data
        except Exception:
            pass

    co_tag  = company.replace(" ", "")
    ind_tag = industry.split("/")[0].strip().replace(" ", "")
    return {
        "caption":  "Introducing " + company + " — " + slogan + "\n\nBuilt for tomorrow. Designed for today. " +
                    "Discover why leaders in " + industry.lower() + " trust us.\n\n" + meta["cta"],
        "hashtags": ["#" + co_tag, "#" + ind_tag, "#BrandLaunch", "#Innovation", "#AI"],
        "cta":      meta["cta"],
        "hook":     "What if " + industry.lower() + " could work smarter for you?",
        "primary":  primary,
        "accent":   accent,
        **meta,
    }

# ── Nano Banana Pro Logo Generator ────────────────────────────────────────────
def generate_logo_imagen(company: str, industry: str, personality: str, palette: dict) -> bytes | None:
    """
    Generate a logo using Nano Banana Pro (Gemini 3.1 Flash Image / imagen-3.0-generate-002).
    Falls back to None if API not available or key missing.
    Returns PNG bytes or None.
    """
    if not st.session_state.gemini_ok:
        return None
    try:
        import google.generativeai as genai
        colors = list(palette.values())
        primary = colors[0]["hex"] if colors else "#1B3A6B"
        accent  = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"

        prompt = (
            f"Professional minimalist logo for a company called '{company}'. "
            f"Industry: {industry}. Brand personality: {personality}. "
            f"Primary brand color: {primary}, accent color: {accent}. "
            f"Clean vector-style design, white background, no text other than the company name, "
            f"suitable for business use. High quality, sharp edges, professional branding."
        )

        # Try Imagen 3 (available via Gemini API)
        try:
            from google.generativeai import ImageGenerationConfig
            imagen = genai.ImageGenerationModel("imagen-3.0-generate-002")
            result = imagen.generate_images(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio="1:1",
            )
            if result.images:
                import io
                buf = io.BytesIO()
                result.images[0]._pil_image.save(buf, format="PNG")
                return buf.getvalue()
        except Exception:
            pass

        # Try Gemini 2.0 Flash image generation (Nano Banana)
        try:
            from google import genai as genai2
            from google.genai import types as gtypes
            client = genai2.Client(api_key=st.session_state.api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=prompt,
                config=gtypes.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                )
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    import io
                    from PIL import Image as PILImage
                    img = PILImage.open(io.BytesIO(part.inline_data.data))
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    return buf.getvalue()
        except Exception:
            pass

        return None
    except Exception:
        return None


# ── Brand Mockup Generator ─────────────────────────────────────────────────────
def generate_mockup(logo_svg: str, palette: dict, company: str, mockup_type: str) -> bytes:
    """
    Generate a brand mockup (business card, t-shirt, mug) using Pillow.
    Returns PNG bytes.
    """
    from PIL import Image, ImageDraw, ImageFont
    import io, math

    colors = list(palette.values())
    primary = colors[0]["hex"] if colors else "#1B3A6B"
    accent  = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"
    light   = colors[3]["hex"] if len(colors) > 3 else "#F0EDE8"

    def h2rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def get_font(size):
        for path in [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]:
            try: return ImageFont.truetype(path, size)
            except: pass
        return ImageFont.load_default()

    initials = "".join([w[0].upper() for w in company.split()[:2]]) if company else "B"
    co_name  = company.upper()[:16]

    if mockup_type == "Business Card":
        W, H = 800, 450
        img  = Image.new("RGB", (W, H), h2rgb(primary))
        draw = ImageDraw.Draw(img)
        # Gold stripe
        draw.rectangle([0, 0, 8, H], fill=h2rgb(accent))
        # Logo circle
        draw.ellipse([50, 140, 170, 260], fill=h2rgb(accent))
        f_init = get_font(52)
        bb = draw.textbbox((0,0), initials, font=f_init)
        draw.text((110-(bb[2]-bb[0])//2, 200-(bb[3]-bb[1])//2), initials, fill=h2rgb(primary), font=f_init)
        # Company name
        f_big  = get_font(36)
        f_small= get_font(18)
        draw.text((200, 160), co_name, fill=h2rgb(light), font=f_big)
        draw.text((200, 210), f"{company.split()[0].lower()}.ai", fill=h2rgb(accent), font=f_small)
        draw.text((200, 240), "hello@" + company.replace(" ","").lower() + ".com", fill=h2rgb(light), font=f_small)
        # Bottom strip
        draw.rectangle([0, H-60, W, H], fill=h2rgb(accent))
        f_tag = get_font(14)
        draw.text((50, H-38), "BRAND IDENTITY · POWERED BY AI", fill=h2rgb(primary), font=f_tag)

    elif mockup_type == "T-Shirt":
        W, H = 600, 700
        img  = Image.new("RGB", (W, H), h2rgb(light))
        draw = ImageDraw.Draw(img)
        # T-shirt silhouette
        shirt_color = h2rgb(primary)
        # Body
        draw.rectangle([130, 200, 470, 580], fill=shirt_color)
        # Sleeves
        draw.polygon([(130,200),(50,280),(90,300),(130,260)], fill=shirt_color)
        draw.polygon([(470,200),(550,280),(510,300),(470,260)], fill=shirt_color)
        # Collar
        draw.ellipse([220,195,380,240], fill=h2rgb(light))
        # Logo on shirt
        draw.ellipse([245,300,355,410], fill=h2rgb(accent))
        f_init = get_font(44)
        bb = draw.textbbox((0,0), initials, font=f_init)
        draw.text((300-(bb[2]-bb[0])//2, 355-(bb[3]-bb[1])//2), initials, fill=shirt_color, font=f_init)
        f_tag = get_font(15)
        draw.text((300-50, 430), co_name, fill=h2rgb(accent), font=f_tag)

    elif mockup_type == "Coffee Mug":
        W, H = 600, 600
        img  = Image.new("RGB", (W, H), h2rgb(light))
        draw = ImageDraw.Draw(img)
        # Mug body (trapezoid-like)
        draw.polygon([(120,150),(480,150),(450,480),(150,480)], fill=h2rgb(primary))
        # Mug top ellipse
        draw.ellipse([120,130,480,175], fill=h2rgb(accent))
        # Handle
        draw.arc([440,230,540,380], start=315, end=135, fill=h2rgb(primary), width=22)
        # Logo on mug
        draw.ellipse([225,240,375,390], fill=h2rgb(accent))
        f_init = get_font(48)
        bb = draw.textbbox((0,0), initials, font=f_init)
        draw.text((300-(bb[2]-bb[0])//2, 315-(bb[3]-bb[1])//2), initials, fill=h2rgb(primary), font=f_init)
        f_tag = get_font(14)
        bb2 = draw.textbbox((0,0), co_name, font=f_tag)
        draw.text((300-(bb2[2]-bb2[0])//2, 410), co_name, fill=h2rgb(light), font=f_tag)

    elif mockup_type == "Phone Case":
        W, H = 420, 720
        img  = Image.new("RGB", (W, H), h2rgb(light))
        draw = ImageDraw.Draw(img)
        # Case outline
        draw.rounded_rectangle([30, 20, 390, 700], radius=40, fill=h2rgb(primary))
        # Screen cutout
        draw.rounded_rectangle([55, 60, 365, 640], radius=25, fill=h2rgb(light))
        # Camera bump
        draw.ellipse([280,30,360,80], fill=h2rgb(accent))
        # Logo on case
        draw.ellipse([155,280,265,390], fill=h2rgb(accent))
        f_init = get_font(42)
        bb = draw.textbbox((0,0), initials, font=f_init)
        draw.text((210-(bb[2]-bb[0])//2, 335-(bb[3]-bb[1])//2), initials, fill=h2rgb(primary), font=f_init)
        f_tag = get_font(13)
        bb2 = draw.textbbox((0,0), co_name, font=f_tag)
        draw.text((210-(bb2[2]-bb2[0])//2, 408), co_name, fill=h2rgb(accent), font=f_tag)

    else:  # Letterhead
        W, H = 595, 842  # A4
        img  = Image.new("RGB", (W, H), h2rgb(light))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, W, 120], fill=h2rgb(primary))
        draw.rectangle([0, 0, 6, H], fill=h2rgb(accent))
        draw.ellipse([30, 20, 100, 100], fill=h2rgb(accent))
        f_init = get_font(32)
        bb = draw.textbbox((0,0), initials, font=f_init)
        draw.text((65-(bb[2]-bb[0])//2, 60-(bb[3]-bb[1])//2), initials, fill=h2rgb(primary), font=f_init)
        f_big = get_font(28)
        draw.text((120, 46), co_name, fill=h2rgb(light), font=f_big)
        # Lines
        for y in [160, 200, 240, 280, 320, 360, 400, 440]:
            w = 400 if y < 300 else 350 if y < 380 else 200
            draw.rectangle([50, y, 50+w, y+1], fill=h2rgb(accent))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


# ── Campaign ROI Calculator ────────────────────────────────────────────────────
def calculate_roi(budget: float, platform: str, objective: str,
                  duration_days: int, audience_size: int,
                  ctr_override: float = None) -> dict:
    """Calculate projected campaign ROI from budget inputs."""
    base_ctr = {"Instagram":3.2,"Facebook":1.8,"Twitter/X":2.1,
                "LinkedIn":2.6,"TikTok":4.1,"YouTube":3.5}
    cpm = {"Instagram":8.5,"Facebook":6.2,"Twitter/X":4.8,
           "LinkedIn":14.0,"TikTok":6.0,"YouTube":9.0}
    conv_rate = {"Brand Awareness":0.01,"Engagement":0.025,
                 "Lead Generation":0.04,"Conversion":0.065,"Retention":0.03}
    avg_order = {"Brand Awareness":0,"Engagement":0,
                 "Lead Generation":45,"Conversion":120,"Retention":85}

    ctr      = ctr_override or base_ctr.get(platform, 2.5)
    cost_pm  = cpm.get(platform, 8.0)
    impressions = int((budget / cost_pm) * 1000)
    clicks      = int(impressions * ctr / 100)
    conv_r      = conv_rate.get(objective, 0.03)
    conversions = int(clicks * conv_r)
    avg_val     = avg_order.get(objective, 0)
    revenue     = conversions * avg_val
    roi_pct     = round(((revenue - budget) / budget * 100) if budget > 0 else 0, 1)
    roas        = round(revenue / budget, 2) if budget > 0 else 0
    cpc         = round(budget / max(1, clicks), 2)
    cpa         = round(budget / max(1, conversions), 2)

    return {
        "impressions":  impressions,
        "clicks":       clicks,
        "conversions":  conversions,
        "revenue":      revenue,
        "roi_pct":      roi_pct,
        "roas":         roas,
        "cpc":          cpc,
        "cpa":          cpa,
        "ctr":          ctr,
        "budget":       budget,
    }


# ── Nano Banana Pro Logo Generator ───────────────────────────────────────────
def generate_logo_nano_banana(company: str, industry: str, personality: str,
                               palette: dict, style: str = "minimalist") -> bytes | None:
    """
    Generate an AI logo image using Nano Banana Pro (Gemini image model).
    Uses gemini-2.0-flash-exp for image generation — same API key as text Gemini.
    Falls back gracefully if model unavailable.
    """
    if not st.session_state.gemini_ok:
        return None
    try:
        import google.generativeai as genai
        colors = list(palette.values())
        primary   = colors[0]["hex"] if colors else "#1B3A6B"
        secondary = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"

        prompt = (
            f"Create a professional {style} brand logo for a company called '{company}'. "
            f"Industry: {industry}. Brand personality: {personality}. "
            f"Primary brand color: {primary}, accent color: {secondary}. "
            f"The logo should be clean, memorable, and work at small sizes. "
            f"White or transparent background. High quality, vector-style design. "
            f"Include the company name '{company}' in the logo with elegant typography. "
            f"No text other than the company name. Professional and modern."
        )

        # Try Nano Banana 2 (gemini-2.0-flash-exp supports image generation)
        for model_name in ["gemini-2.0-flash-exp", "gemini-1.5-flash"]:
            try:
                model    = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "image/png"}
                )
                # Check for image in response parts
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data:
                        import base64
                        return base64.b64decode(part.inline_data.data)
            except Exception:
                continue
        return None
    except Exception as e:
        return None


# ── Brand Mockup Generator ───────────────────────────────────────────────────
def generate_mockup(logo_svg: str, palette: dict, company: str, mockup_type: str) -> bytes:
    """
    Generate brand mockup images using Pillow.
    Supports: Business Card, T-Shirt, Mug, Billboard, Letterhead
    """
    from src.palette_engine import hex_to_rgb
    from src.logo_engine import svg_to_png_bytes
    import io

    colors = list(palette.values())
    bg_hex  = colors[0]["hex"] if colors else "#1B3A6B"
    acc_hex = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"
    lt_hex  = colors[3]["hex"] if len(colors) > 3 else "#F0EDE8"
    bg_rgb  = hex_to_rgb(bg_hex)
    acc_rgb = hex_to_rgb(acc_hex)
    lt_rgb  = hex_to_rgb(lt_hex)

    # Get logo as PIL image
    logo_bytes = svg_to_png_bytes(logo_svg, 120)
    try:
        from PIL import Image as PILImage
        logo_img = PILImage.open(io.BytesIO(logo_bytes)).convert("RGBA") if logo_bytes else None
    except Exception:
        logo_img = None

    try:
        from PIL import Image, ImageDraw, ImageFont
        FONT_PATHS = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        def get_font(size):
            for p in FONT_PATHS:
                try: return ImageFont.truetype(p, size)
                except: pass
            return ImageFont.load_default()

        if mockup_type == "Business Card":
            W, H = 800, 450
            img  = Image.new("RGB", (W, H), tuple(bg_rgb))
            draw = ImageDraw.Draw(img)
            # Card border
            draw.rectangle([20, 20, W-20, H-20], outline=tuple(acc_rgb), width=2)
            draw.rectangle([28, 28, W-28, H-28], outline=tuple(acc_rgb), width=1)
            # Accent stripe
            draw.rectangle([20, H-80, W-20, H-20], fill=tuple(acc_rgb))
            # Logo
            if logo_img:
                lw, lh = 100, 100
                logo_r = logo_img.resize((lw, lh), PILImage.LANCZOS)
                img.paste(logo_r, (50, H//2 - lh//2 - 20), logo_r if logo_r.mode == "RGBA" else None)
            # Text
            draw.text((180, 140), company.upper(), font=get_font(36), fill=tuple(acc_rgb))
            draw.text((180, 195), "Brand Identity Powered by AI", font=get_font(18), fill=tuple(lt_rgb))
            draw.text((180, 235), "hello@" + company.lower().replace(" ","") + ".com", font=get_font(16), fill=tuple(lt_rgb))
            draw.text((180, 260), "www." + company.lower().replace(" ","") + ".com", font=get_font(16), fill=tuple(lt_rgb))
            draw.text((50, H-58), "BrandSphere AI", font=get_font(14), fill=tuple(bg_rgb))

        elif mockup_type == "T-Shirt":
            W, H = 600, 700
            img  = Image.new("RGB", (W, H), tuple(lt_rgb))
            draw = ImageDraw.Draw(img)
            # Simple t-shirt silhouette
            shirt_color = tuple(bg_rgb)
            # Body
            draw.rectangle([120, 200, 480, 620], fill=shirt_color)
            # Sleeves
            draw.rectangle([20, 200, 140, 360], fill=shirt_color)
            draw.rectangle([460, 200, 580, 360], fill=shirt_color)
            # Collar
            draw.ellipse([220, 180, 380, 240], fill=shirt_color)
            # Logo on shirt
            if logo_img:
                lw, lh = 150, 150
                logo_r = logo_img.resize((lw, lh), PILImage.LANCZOS)
                img.paste(logo_r, (W//2-lw//2, 300), logo_r if logo_r.mode == "RGBA" else None)
            else:
                draw.text((W//2, 360), company[0].upper(), font=get_font(80),
                          fill=tuple(acc_rgb), anchor="mm")
            draw.text((W//2, 480), company.upper(), font=get_font(22),
                      fill=tuple(acc_rgb), anchor="mm")

        elif mockup_type == "Mug":
            W, H = 600, 600
            img  = Image.new("RGB", (W, H), (245, 243, 240))
            draw = ImageDraw.Draw(img)
            # Mug body
            draw.rounded_rectangle([100, 150, 450, 480], radius=20, fill=tuple(bg_rgb))
            # Mug handle
            draw.arc([420, 250, 530, 400], start=320, end=220, fill=tuple(bg_rgb), width=28)
            # Mug rim
            draw.ellipse([100, 135, 450, 175], fill=tuple(acc_rgb))
            draw.ellipse([100, 465, 450, 500], fill=tuple(acc_rgb))
            # Logo on mug
            if logo_img:
                lw, lh = 120, 120
                logo_r = logo_img.resize((lw, lh), PILImage.LANCZOS)
                img.paste(logo_r, (W//2-lw//2 - 30, 250), logo_r if logo_r.mode == "RGBA" else None)
            else:
                draw.text((230, 315), company[0].upper(), font=get_font(72),
                          fill=tuple(acc_rgb), anchor="mm")
            draw.text((220, 400), company.upper(), font=get_font(18),
                      fill=tuple(acc_rgb), anchor="mm")

        elif mockup_type == "Billboard":
            W, H = 900, 400
            img  = Image.new("RGB", (W, H), tuple(bg_rgb))
            draw = ImageDraw.Draw(img)
            # Billboard board
            draw.rectangle([0, 30, W, H-30], fill=tuple(bg_rgb))
            # Accent bars
            draw.rectangle([0, 30, W, 50], fill=tuple(acc_rgb))
            draw.rectangle([0, H-50, W, H-30], fill=tuple(acc_rgb))
            # Logo left
            if logo_img:
                lw, lh = 160, 160
                logo_r = logo_img.resize((lw, lh), PILImage.LANCZOS)
                img.paste(logo_r, (60, H//2-lh//2), logo_r if logo_r.mode == "RGBA" else None)
            # Main text
            draw.text((280, H//2-50), company.upper(), font=get_font(72),
                      fill=tuple(acc_rgb))
            draw.text((280, H//2+30), "Powered by AI. Built for tomorrow.", font=get_font(22),
                      fill=tuple(lt_rgb))

        else:  # Letterhead
            W, H = 600, 800
            img  = Image.new("RGB", (W, H), tuple(lt_rgb))
            draw = ImageDraw.Draw(img)
            # Header band
            draw.rectangle([0, 0, W, 120], fill=tuple(bg_rgb))
            draw.rectangle([0, 120, W, 128], fill=tuple(acc_rgb))
            # Logo in header
            if logo_img:
                lw, lh = 80, 80
                logo_r = logo_img.resize((lw, lh), PILImage.LANCZOS)
                img.paste(logo_r, (30, 20), logo_r if logo_r.mode == "RGBA" else None)
            draw.text((130, 40), company.upper(), font=get_font(32), fill=tuple(acc_rgb))
            draw.text((130, 82), "AI-Powered Brand Identity", font=get_font(14), fill=tuple(lt_rgb))
            # Body lines
            for i, line_y in enumerate(range(200, 600, 36)):
                draw.rectangle([40, line_y, W-40, line_y+1], fill=(220, 218, 215))
            draw.text((40, 640), "BrandSphere AI  ·  CRS AI Capstone 2025–26",
                      font=get_font(12), fill=tuple(bg_rgb))
            draw.rectangle([0, H-8, W, H], fill=tuple(acc_rgb))

        buf = io.BytesIO()
        img.save(buf, format="PNG", quality=95)
        return buf.getvalue()

    except Exception as e:
        import io
        from PIL import Image, ImageDraw
        img  = Image.new("RGB", (400, 200), tuple(bg_rgb))
        draw = ImageDraw.Draw(img)
        draw.text((20, 80), f"{company} — {mockup_type}", fill=tuple(acc_rgb))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()


# ── Dark / Light Palette Switcher ────────────────────────────────────────────
def switch_palette_mode(palette: dict, mode: str) -> dict:
    """Convert palette to dark or light mode variant."""
    from src.palette_engine import hex_to_rgb, rgb_to_hex, adjust_saturation
    import colorsys

    def lighten(hex_c, amount=0.4):
        r, g, b = [v/255 for v in hex_to_rgb(hex_c)]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v2 = min(1.0, v + amount)
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v2)
        return rgb_to_hex([r2*255, g2*255, b2*255])

    def darken(hex_c, amount=0.4):
        r, g, b = [v/255 for v in hex_to_rgb(hex_c)]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        v2 = max(0.0, v - amount)
        r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v2)
        return rgb_to_hex([r2*255, g2*255, b2*255])

    new_palette = {}
    for name, v in palette.items():
        hex_c = v["hex"]
        if mode == "Dark Mode":
            if name in ["Background", "Text / CTA"]:
                new_hex = darken(hex_c, 0.5) if name == "Background" else lighten(hex_c, 0.5)
            else:
                new_hex = adjust_saturation(hex_c, 1.15)
        else:  # Light Mode
            if name == "Background":
                new_hex = "#F8F6F2"
            elif name == "Text / CTA":
                new_hex = "#1A1A1A"
            else:
                new_hex = adjust_saturation(hex_c, 0.9)
        new_palette[name] = {**v, "hex": new_hex}
    return new_palette


# ── Campaign ROI Calculator ──────────────────────────────────────────────────
def calculate_roi(budget: float, platform: str, objective: str,
                   audience_size: int, personality: str) -> dict:
    """
    Project campaign ROI from budget input.
    Uses industry benchmark CPMs and conversion rates.
    """
    cpm_benchmarks = {
        "Instagram": 8.5, "Facebook": 6.2, "Twitter/X": 5.8,
        "LinkedIn": 28.0, "TikTok": 9.0, "YouTube": 12.0,
    }
    conv_benchmarks = {
        "Brand Awareness": 0.008, "Engagement": 0.025,
        "Lead Generation": 0.045, "Conversion": 0.032, "Retention": 0.055,
    }
    pers_mult = {
        "Vibrant": 1.22, "Bold": 1.18, "Minimalist": 0.95,
        "Luxury": 1.08, "Elegant": 1.05, "Playful": 1.15, "Professional": 1.0,
    }

    cpm  = cpm_benchmarks.get(platform, 8.0)
    cr   = conv_benchmarks.get(objective, 0.02)
    mult = pers_mult.get(personality, 1.0)

    impressions     = int((budget / cpm) * 1000 * mult)
    clicks          = int(impressions * 0.028 * mult)
    conversions     = int(clicks * cr)
    revenue_est     = conversions * 45  # avg $45 revenue per conversion
    roi_pct         = round(((revenue_est - budget) / budget) * 100, 1)
    cost_per_click  = round(budget / max(clicks, 1), 2)
    cost_per_conv   = round(budget / max(conversions, 1), 2)

    breakeven_budget = round(revenue_est / max(1 + roi_pct/100, 0.01), 2)

    return {
        "impressions":      impressions,
        "clicks":           clicks,
        "conversions":      conversions,
        "revenue_est":      revenue_est,
        "roi_pct":          roi_pct,
        "cost_per_click":   cost_per_click,
        "cost_per_conv":    cost_per_conv,
        "breakeven":        breakeven_budget,
        "budget":           budget,
        "platform":         platform,
        "note":             "Estimates based on industry benchmark CPMs. Actual results vary.",
    }


# ══════════════════════════════════════════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nav-bar">
  <div>
    <div class="nav-logo">Brand<span>Sphere</span> AI</div>
    <div class="nav-tag">Automated Branding Intelligence Platform</div>
  </div>
  <div class="nav-tag">Scenario 1 &nbsp;|&nbsp; CRS AI Capstone 2025–26</div>
</div>
""", unsafe_allow_html=True)

# ── API Key config ────────────────────────────────────────────────────────
with st.expander("⚙️  API Configuration", expanded=not st.session_state.gemini_ok):
    c1, c2 = st.columns([4, 1])
    with c1:
        api_inp = st.text_input("Gemini API Key", type="password",
                                placeholder="AIza...", label_visibility="collapsed")
    with c2:
        if st.button("Connect"):
            if api_inp:
                if configure_gemini(api_inp):
                    st.success("✓ Gemini connected")
                else:
                    st.error("Invalid key")
    if not st.session_state.gemini_ok:
        st.info("💡 **Demo mode** — all features work with AI-simulated outputs. Connect Gemini for live generation.")
    else:
        st.success(f"✓ Gemini 2.0 Flash connected — Session {st.session_state.session_id}")

# ── HERO ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered Branding Intelligence</div>
  <div class="hero-title">Your brand identity,<br><em>engineered by AI.</em></div>
  <div class="hero-sub">
    Generate logos, taglines, color palettes, campaigns, and complete brand kits in minutes.
    Powered by Computer Vision, Generative AI, NLP, and Predictive Analytics.
  </div>
  <div class="badge-row">
    <span class="badge">Logo Studio</span>
    <span class="badge">KMeans Palette</span>
    <span class="badge">NLTK NLP</span>
    <span class="badge">Random Forest KPIs</span>
    <span class="badge">Gemini API</span>
    <span class="badge">Multilingual</span>
    <span class="badge">Streamlit Cloud</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs([
    "🏠 Home",
    "🎯 Brand Inputs",
    "🎨 Logo Studio",
    "🖋 Fonts & Palette",
    "✍️ Slogans & Content",
    "📣 Campaign Analytics",
    "🌍 Multilingual Studio",
    "🎬 Animation Preview",
    "🪄 Mockups & ROI",
    "⭐ Feedback",
    "📦 Download Kit",
])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="sec-label">Overview</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Welcome to <em>BrandSphere AI</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    modules = [
        ("🎨", "AI Logo & Design Studio", "5 SVG logo concepts generated from your brand personality and color palette."),
        ("✍️", "Creative Content & GenAI Hub", "NLTK-powered tagline analysis + Gemini-enhanced slogan generation."),
        ("📣", "Smart Campaign Studio", "Random Forest model trained on 200K real marketing records predicts CTR, ROI & Engagement."),
        ("🌍", "Multilingual Engine", "Gemini-powered translation into 5 languages with tone preservation."),
        ("⭐", "Feedback Intelligence", "Star ratings saved to CSV; Plotly dashboards visualize patterns."),
        ("📦", "Export Engine", "Complete brand kit: logos, palette, fonts, taglines, campaigns, animation — all in one ZIP."),
    ]
    for i, (icon, title, desc) in enumerate(modules):
        col = [c1, c2, c3][i % 3]
        with col:
            st.markdown(f"""
            <div class="card">
              <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
              <div class="card-title">{title}</div>
              <div class="card-sub">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-label">10-Week Roadmap</p>', unsafe_allow_html=True)
    weeks = [
        ("Week 1", "EDA & Data Understanding", "✅ Completed"),
        ("Week 2", "Logo Classification & Extraction", "✅ SVG Engine"),
        ("Week 3", "Font Recommendation Engine", "✅ Completed"),
        ("Week 4", "Tagline & Slogan Generation", "✅ NLTK + Gemini"),
        ("Week 5", "Color Palette Engine", "✅ KMeans"),
        ("Week 6", "Animated Visuals Studio", "✅ Pillow GIF"),
        ("Week 7", "Smart Campaign Studio", "✅ Random Forest"),
        ("Week 8", "Multilingual Generator", "✅ Gemini / Fallback"),
        ("Week 9", "Feedback Intelligence", "✅ CSV + Plotly"),
        ("Week 10","Integration & Deployment", "✅ Streamlit Cloud"),
    ]
    for wk, task, status in weeks:
        st.markdown(f"""
        <div class="check-item">
          <span style="color:var(--teal);font-size:0.95rem">✓</span>
          <div>
            <span style="font-family:var(--font-mono);font-size:0.62rem;color:var(--accent);letter-spacing:0.1em">{wk}</span>
            <span style="font-size:0.88rem;color:var(--text);margin-left:12px">{task}</span>
            <span style="margin-left:10px" class="pill pill-g">{status}</span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — BRAND INPUTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="sec-label">Step 01 — Foundation</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Brand <em>Input Form</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        company    = st.text_input("Company Name *", placeholder="e.g. NovaTech Solutions")
        industry   = st.selectbox("Industry *", INDUSTRIES)
        personality= st.selectbox("Brand Personality *", PERSONALITIES)
        audience   = st.text_input("Target Audience", placeholder="e.g. Millennials aged 25–40")
    with col2:
        tone       = st.selectbox("Communication Tone", TONES)
        tag_hint   = st.text_input("Tagline Hint (optional)", placeholder="e.g. Focus on innovation and speed")
        description= st.text_area("Product / Service Description",
                                   placeholder="What does your business do? What makes it unique?", height=108)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("🚀  Generate Full Brand Kit", use_container_width=False):
        if not company:
            st.warning("Please enter a company name.")
        else:
            bi = {"company": company, "industry": industry, "personality": personality,
                  "audience": audience, "tone": tone, "tag_hint": tag_hint, "description": description}
            st.session_state.brand_inputs = bi

            with st.spinner("Building brand identity…"):
                st.session_state.palette  = generate_palette(industry, personality)
                st.session_state.logos    = generate_all_logos(company, st.session_state.palette)
                st.session_state.fonts    = recommend_fonts(industry, personality)
                slogans, retrieved = generate_slogans(company, industry, tone, audience, tag_hint)
                st.session_state.slogans   = slogans
                st.session_state.retrieved = retrieved
                st.session_state.aesthetics = score_brand(personality, industry, tone,
                                                           slogans[0]["text"] if slogans else "",
                                                           st.session_state.palette)

            st.success(f"✓ Brand kit generated for **{company}**. Navigate the tabs to explore your assets.")

    if st.session_state.brand_inputs:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Current Brand Profile</p>', unsafe_allow_html=True)
        bi = st.session_state.brand_inputs
        cols = st.columns(4)
        for col, (lbl, val) in zip(cols, [
            ("Company", bi.get("company","")), ("Industry", bi.get("industry","")),
            ("Personality", bi.get("personality","")), ("Tone", bi.get("tone",""))
        ]):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <span class="metric-lbl">{lbl}</span>
                  <span style="font-family:var(--font-head);font-size:1.1rem;color:var(--text);display:block;margin-top:5px">{val}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<p class="sec-label">✨ Brand Name Generator</p>', unsafe_allow_html=True)
    st.markdown('<h3 style="font-family:var(--font-head);font-weight:300;color:var(--text);margin-bottom:12px">No name yet? <em style="color:var(--accent)">Let AI suggest one.</em></h3>', unsafe_allow_html=True)
    ng1, ng2, ng3 = st.columns([1,1,1], gap="large")
    with ng1:
        ng_industry = st.selectbox("Industry", INDUSTRIES, key="ng_ind")
    with ng2:
        ng_pers = st.selectbox("Personality", PERSONALITIES, key="ng_pers")
    with ng3:
        ng_kw = st.text_input("Keywords (optional)", placeholder="e.g. speed, clarity, trust", key="ng_kw")
    if st.button("🎲  Generate Brand Names"):
        with st.spinner("Generating names…"):
            names = generate_brand_names(ng_industry, ng_pers, ng_kw)
            if names:
                name_cols = st.columns(min(4, len(names)))
                for i, n in enumerate(names[:8]):
                    with name_cols[i % 4]:
                        st.markdown(f"""
                        <div class="card" style="text-align:center;padding:16px">
                          <div style="font-family:var(--font-head);font-size:1.3rem;color:var(--accent);margin-bottom:5px">{n.get('name','')}</div>
                          <div style="font-size:0.76rem;color:var(--muted);line-height:1.55">{n.get('rationale','')}</div>
                          <div style="font-family:var(--font-mono);font-size:0.55rem;color:var(--text2) ;margin-top:8px;opacity:0.5">{n.get('domain','')}</div>
                        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — LOGO STUDIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="sec-label">Module 01 — Visual Identity</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Logo <em>Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.logos:
        st.info("👈 Complete Brand Inputs first to generate logos.")
    else:
        bi = st.session_state.brand_inputs
        st.markdown(f'<p class="sec-label">5 Concepts for {bi.get("company","")}</p>', unsafe_allow_html=True)
        st.caption("⚠️ Logo generation is SVG-based (no logo image dataset uploaded). See code comments for full transparency.")

        logo_cols = st.columns(5)
        for i, logo in enumerate(st.session_state.logos):
            with logo_cols[i]:
                selected_cls = "selected" if st.session_state.selected_logo == i else ""
                st.markdown(f"""
                <div class="logo-svg-wrap {selected_cls}" id="logo_{i}">
                  {logo["svg"]}
                  <div style="font-family:var(--font-mono);font-size:0.55rem;color:var(--accent);letter-spacing:0.08em;text-align:center">{logo["style"]}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Select", key=f"sel_logo_{i}"):
                    st.session_state.selected_logo = i
                    st.rerun()

        sel = st.session_state.logos[st.session_state.selected_logo]
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown(f'<p class="sec-label">Selected: {sel["style"]}</p>', unsafe_allow_html=True)
            st.markdown(sel["svg"], unsafe_allow_html=True)
            st.download_button("⬇ Download SVG", data=sel["svg"].encode(),
                               file_name=f"{bi.get('company','brand')}_logo_{sel['index']}.svg",
                               mime="image/svg+xml")
            png = svg_to_png_bytes(sel["svg"], 300)
            if png:
                st.download_button("⬇ Download PNG", data=png,
                                   file_name=f"{bi.get('company','brand')}_logo_{sel['index']}.png",
                                   mime="image/png")
        with c2:
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">Design Rationale</p>
              <p style="font-size:0.9rem;line-height:1.7;color:var(--text)">{sel["description"]}</p>
              <br/>
              <p class="sec-label">All Concepts</p>
              {"".join([f'<div style="font-size:0.83rem;color:var(--muted);padding:4px 0;border-bottom:1px solid var(--border)"><span style="color:var(--accent)">#{l["index"]+1}</span> {l["style"]} — {l["description"][:60]}…</div>' for l in st.session_state.logos])}
            </div>""", unsafe_allow_html=True)


        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Nano Banana Pro Logo Generation ───────────────────────────────────
        st.markdown('<p class="sec-label">🍌 Nano Banana Pro — AI Image Logo</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <div class="card-title">Generate with Gemini Image AI</div>
          <div class="card-sub">Uses Google's Nano Banana Pro model to generate a photorealistic AI logo image — requires Gemini API key connected above.</div>
        </div>""", unsafe_allow_html=True)

        nb_col1, nb_col2 = st.columns([2, 1], gap="large")
        with nb_col1:
            nb_style = st.selectbox("Logo Style", [
                "minimalist and modern", "luxury and elegant", "bold and geometric",
                "playful and colorful", "tech and futuristic", "organic and natural"
            ], key="nb_style")
        with nb_col2:
            nb_btn = st.button("🍌  Generate AI Logo", key="nb_gen")

        if nb_btn:
            if not st.session_state.gemini_ok:
                st.warning("Connect your Gemini API key first.")
            elif not st.session_state.brand_inputs:
                st.warning("Complete Brand Inputs first.")
            else:
                bi3 = st.session_state.brand_inputs
                with st.spinner("Generating logo with Nano Banana Pro…"):
                    nb_logo_bytes = generate_logo_nano_banana(
                        bi3.get("company","Brand"),
                        bi3.get("industry",""),
                        bi3.get("personality",""),
                        st.session_state.palette,
                        nb_style
                    )
                if nb_logo_bytes:
                    st.image(nb_logo_bytes, caption="Generated by Nano Banana Pro (Gemini Image AI)", width=320)
                    st.download_button("⬇ Download AI Logo", data=nb_logo_bytes,
                                       file_name=f"{bi3.get('company','brand')}_ai_logo.png",
                                       mime="image/png")
                else:
                    st.info("💡 Nano Banana image generation requires the `gemini-2.0-flash-exp` model which supports image output. If unavailable in your region, the SVG logos above work identically. Check [Google AI Studio](https://aistudio.google.com) for model availability.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ── Brand Mockup Generator ────────────────────────────────────────────
        st.markdown('<p class="sec-label">🖼 Brand Mockup Generator</p>', unsafe_allow_html=True)
        if not st.session_state.logos:
            st.info("Generate your brand kit first.")
        else:
            mk1, mk2 = st.columns([1, 2], gap="large")
            with mk1:
                mockup_type = st.selectbox("Mockup Type", [
                    "Business Card", "T-Shirt", "Mug", "Billboard", "Letterhead"
                ], key="mockup_type")
                mk_btn = st.button("🎨  Generate Mockup")
            with mk2:
                st.markdown(f"""
                <div class="card">
                  <p class="sec-label">About this mockup</p>
                  <p style="font-size:0.83rem;color:var(--muted);line-height:1.65">
                    Renders your selected logo and brand palette onto a realistic {mockup_type if "mockup_type" in dir() else "product"} template.
                    Built with Pillow — no external API required.
                  </p>
                </div>""", unsafe_allow_html=True)

            if mk_btn:
                sel_logo = st.session_state.logos[st.session_state.selected_logo]
                with st.spinner(f"Rendering {mockup_type} mockup…"):
                    bi3 = st.session_state.brand_inputs
                    mkup = generate_mockup(sel_logo["svg"], st.session_state.palette,
                                           bi3.get("company","Brand"), mockup_type)
                if mkup:
                    st.image(mkup, caption=f"{mockup_type} Mockup — {bi3.get('company','')}", width=500)
                    st.download_button(f"⬇ Download {mockup_type}",
                                       data=mkup,
                                       file_name=f"{bi3.get('company','brand')}_{mockup_type.replace(' ','_')}.png",
                                       mime="image/png")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — FONTS & PALETTE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="sec-label">Module 02 — Visual System</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Fonts & <em>Colour Palette</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.palette:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs

        # Palette
        st.markdown('<p class="sec-label">KMeans-Extracted Color Palette (Week 5)</p>', unsafe_allow_html=True)
        st.caption("KMeans(k=5) run on noise-augmented seed colors from industry color psychology mapping.")
        swatch_html = '<div class="swatch-row">'
        for name, v in st.session_state.palette.items():
            swatch_html += f'<div class="swatch" style="background:{v["hex"]}">{v["hex"]}</div>'
        swatch_html += "</div>"
        st.markdown(swatch_html, unsafe_allow_html=True)

        pc1, pc2 = st.columns(2, gap="large")
        with pc1:
            for name, v in st.session_state.palette.items():
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin:7px 0">
                  <div style="width:32px;height:32px;background:{v['hex']};border-radius:5px;flex-shrink:0"></div>
                  <div>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--accent);letter-spacing:0.1em">{name}</span>
                    <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted);margin-left:8px">{v['hex']}</span>
                    <div style="font-size:0.78rem;color:var(--muted)">{v['psychology']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        with pc2:
            harmony = score_palette_harmony(st.session_state.palette)
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:14px">
              <span class="metric-val">{harmony}/100</span>
              <span class="metric-lbl">Palette Harmony Score</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">Personality</p>
              <p style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text)">
                {bi.get("personality","")} palette for {bi.get("industry","")}
              </p>
              <p style="font-size:0.82rem;color:var(--muted);margin-top:8px;line-height:1.6">
                Follow the 60-30-10 rule: 60% Primary · 30% Secondary · 10% Accent.
              </p>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Dark / Light Mode Switcher
        st.markdown('<p class="sec-label">🌗 Dark / Light Mode Switcher</p>', unsafe_allow_html=True)
        dm1, dm2 = st.columns([1, 2], gap="large")
        with dm1:
            mode_choice = st.radio("Palette Mode", ["Original", "Dark Mode", "Light Mode"], horizontal=True, key="palette_mode")
            if st.button("↺  Apply Mode"):
                if mode_choice == "Original":
                    from src.palette_engine import generate_palette as regen_pal
                    bi3 = st.session_state.brand_inputs
                    st.session_state.palette = regen_pal(bi3.get("industry",""), bi3.get("personality",""))
                else:
                    switched = switch_palette_mode(st.session_state.palette, mode_choice)
                    st.session_state.palette = switched
                st.rerun()
        with dm2:
            if st.session_state.palette:
                colors = list(st.session_state.palette.values())
                sw_html = '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">'
                for v in colors:
                    sw_html += f'<div style="text-align:center"><div style="width:50px;height:50px;background:{v["hex"]};border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.3)"></div><div style="font-family:var(--font-mono);font-size:0.52rem;color:var(--muted);margin-top:4px">{v["hex"]}</div></div>'
                sw_html += '</div>'
                st.markdown(f'<p style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);letter-spacing:0.1em">CURRENT MODE: {mode_choice.upper()}</p>{sw_html}', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # WCAG Accessibility
        st.markdown('<p class="sec-label">♿ WCAG Accessibility Check</p>', unsafe_allow_html=True)
        wcag_results = check_wcag(st.session_state.palette)
        if wcag_results:
            wc1, wc2 = st.columns(2, gap="large")
            for i, r in enumerate(wcag_results):
                with [wc1, wc2][i % 2]:
                    aa_color  = "#3ECFB2" if "Pass" in r["AA"]  else "#E05A5A"
                    aaa_color = "#3ECFB2" if "Pass" in r["AAA"] else "#E05A5A"
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;background:var(--surface2);border-radius:8px;padding:12px 14px;margin-bottom:8px;border:1px solid var(--border)">
                      <div style="display:flex;gap:4px;flex-shrink:0">
                        <div style="width:24px;height:24px;background:{r['hex1']};border-radius:4px"></div>
                        <div style="width:24px;height:24px;background:{r['hex2']};border-radius:4px"></div>
                      </div>
                      <div style="flex:1;min-width:0">
                        <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--muted)">{r['pair']}</div>
                        <div style="font-family:var(--font-mono);font-size:0.68rem;color:var(--accent)">Ratio: {r['ratio']}:1</div>
                      </div>
                      <div style="text-align:right;font-family:var(--font-mono);font-size:0.6rem">
                        <div style="color:{aa_color}">AA {r['AA'].split()[0]}</div>
                        <div style="color:{aaa_color}">AAA {r['AAA'].split()[0]}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Fonts
        st.markdown('<p class="sec-label">Font Recommendations (Week 3)</p>', unsafe_allow_html=True)
        st.caption("Rule-based engine mapping industry × personality → curated font pairings. No font image dataset required.")
        fcols = st.columns(3)
        for i, font in enumerate(st.session_state.fonts):
            with fcols[i]:
                st.markdown(f"""
                <div class="card">
                  <div style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.12em;margin-bottom:6px">{font['rank']}</div>
                  <div class="card-title">{font['heading']}</div>
                  <div style="font-size:0.8rem;color:var(--muted);margin-bottom:8px">Body: {font['body']}<br>Alt: {font['alternate']}</div>
                  <div style="font-size:0.78rem;color:var(--text);line-height:1.55">{font['rationale']}</div>
                  <br>
                  <span class="pill pill-a">{font['classification']}</span>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — SLOGANS & CONTENT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="sec-label">Module 03 — Generative AI</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Slogans & <em>Content Hub</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs

        sc1, sc2 = st.columns([1, 1], gap="large")

        with sc1:
            st.markdown('<p class="sec-label">AI-Generated Taglines</p>', unsafe_allow_html=True)
            if st.button("✨  Regenerate Taglines"):
                with st.spinner("Generating…"):
                    slogans, retrieved = generate_slogans(
                        bi["company"], bi["industry"], bi["tone"],
                        bi.get("audience",""), bi.get("tag_hint",""))
                    st.session_state.slogans   = slogans
                    st.session_state.retrieved = retrieved

            if st.session_state.slogans:
                for s in st.session_state.slogans:
                    src_pill = "pill-g" if s["source"] == "gemini" else "pill-a"
                    st.markdown(f"""
                    <div class="tagline-card">"{s['text']}"
                      <div style="margin-top:5px">
                        <span class="pill {src_pill}">{s['source']}</span>
                        <span class="pill pill-a" style="margin-left:4px">{s['tone']}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

            if st.session_state.retrieved:
                st.markdown('<p class="sec-label" style="margin-top:18px">TF-IDF Retrieved Inspiration</p>', unsafe_allow_html=True)
                for r in st.session_state.retrieved[:3]:
                    st.markdown(f'<div style="font-style:italic;color:var(--muted);font-size:0.84rem;padding:4px 0">"{r}"</div>', unsafe_allow_html=True)

            # NLTK Analysis
            if st.session_state.slogans:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                with st.expander("🔬 NLTK Text Analysis (Week 4 — NLP Preprocessing)"):
                    top = st.session_state.slogans[0]["text"]
                    analysis = st.session_state.slogans[0].get("analysis") or nltk_analyze(top)
                    st.markdown(f"""
                    <div style="background:var(--surface2);border-radius:8px;padding:14px 16px;border:1px solid var(--border)">
                      <p class="sec-label">Analysed: "{top[:50]}"</p>
                      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:10px 0">
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['word_count']}</span><span class="metric-lbl">Tokens</span></div>
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['unique_words']}</span><span class="metric-lbl">Unique</span></div>
                        <div class="metric-card"><span class="metric-val" style="font-size:1.6rem">{analysis['lexical_density']}</span><span class="metric-lbl">Lex Density</span></div>
                      </div>
                      <p style="font-family:var(--font-mono);font-size:0.56rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase;margin-top:10px">Clean tokens</p>
                      <div>{"".join([f'<span class="nltk-pill">{t}</span>' for t in analysis["clean_tokens"]])}</div>
                      <p style="font-family:var(--font-mono);font-size:0.56rem;color:var(--muted);letter-spacing:0.1em;text-transform:uppercase;margin-top:10px">Stems (Porter)</p>
                      <div>{"".join([f'<span class="nltk-pill" style="opacity:0.6">{s}</span>' for s in analysis["stems"]])}</div>
                    </div>""", unsafe_allow_html=True)

        with sc2:
            st.markdown('<p class="sec-label">Brand Narrative</p>', unsafe_allow_html=True)
            if st.button("📖  Generate Brand Story"):
                with st.spinner("Writing…"):
                    st.session_state.brand_story = generate_brand_story(bi)

            if st.session_state.brand_story:
                st.markdown(f"""
                <div class="card">
                  <p class="sec-label">Brand Narrative</p>
                  <p style="font-family:var(--font-head);font-size:1rem;font-style:italic;line-height:1.85;color:var(--text)">{st.session_state.brand_story}</p>
                </div>""", unsafe_allow_html=True)

            # Aesthetics score
            if st.session_state.aesthetics:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<p class="sec-label">Brand Consistency Score</p>', unsafe_allow_html=True)
                aes = st.session_state.aesthetics
                overall = aes["overall"]
                grade   = aes["grade"]
                pill    = "pill-g" if overall >= 88 else "pill-a" if overall >= 75 else "pill-r"
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:14px">
                  <span class="metric-val">{overall}/100</span>
                  <span class="metric-lbl">Brand Cohesion <span class="pill {pill}">{grade}</span></span>
                </div>""", unsafe_allow_html=True)
                for dim, score in list(aes["dimensions"].items())[:4]:
                    color = "#3ECFB2" if score >= 85 else "#C9A84C" if score >= 72 else "#E05A5A"
                    st.markdown(f"""
                    <div style="margin:8px 0">
                      <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                        <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--muted);letter-spacing:0.08em">{dim.upper()}</span>
                        <span style="font-family:var(--font-mono);font-size:0.62rem;color:{color}">{score}/100</span>
                      </div>
                      <div class="prog-wrap"><div class="prog-bar" style="width:{score}%;background:{color}"></div></div>
                    </div>""", unsafe_allow_html=True)

# ── A/B Tagline Tester ───────────────────────────────────────────────────────
if st.session_state.get("slogans"):
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    with st.expander("🧪 A/B Tagline Scorer — Compare Your Taglines"):
        st.caption("AI scores each tagline across 5 brand dimensions: Memorability, Clarity, Emotional Impact, Brand Fit, Uniqueness.")
        if st.button("▶  Run A/B Scorer"):
            bi2 = st.session_state.brand_inputs
            with st.spinner("Scoring…"):
                ab_results = ab_test_taglines(
                    st.session_state.slogans,
                    bi2.get("industry",""), bi2.get("audience",""))
            if ab_results:
                dims = ["memorability","clarity","emotional_impact","brand_fit","uniqueness"]
                dim_labels = ["Memory","Clarity","Emotion","Brand Fit","Unique"]
                medals = ["🥇","🥈","🥉","4️⃣"]
                for rank, r in enumerate(ab_results, 1):
                    score_color = "#3ECFB2" if r["overall"] >= 8 else "#C9A84C" if r["overall"] >= 6 else "#E05A5A"
                    dim_html = ""
                    for d, dl in zip(dims, dim_labels):
                        c = "#3ECFB2" if r[d] >= 8 else "#C9A84C" if r[d] >= 6 else "#E05A5A"
                        dim_html += f'<div style="text-align:center"><div style="font-family:var(--font-mono);font-size:0.5rem;color:var(--muted);text-transform:uppercase">{dl}</div><div style="font-size:1rem;color:{c};font-weight:700">{r[d]}</div></div>'
                    st.markdown(f'''
                    <div class="card" style="margin-bottom:10px">
                      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                        <div style="font-family:var(--font-head);font-size:1rem;font-style:italic;color:var(--text)">{medals[min(rank-1,3)]} &ldquo;{r["tagline"]}&rdquo;</div>
                        <div style="font-family:var(--font-mono);font-size:0.95rem;color:{score_color};font-weight:700">{r["overall"]}/10</div>
                      </div>
                      <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px">{dim_html}</div>
                    </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — CAMPAIGN ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="sec-label">Module 04 — Campaign Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Smart Campaign <em>Analytics</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs
        ca1, ca2, ca3 = st.columns(3)
        with ca1:
            platform  = st.selectbox("Platform", PLATFORMS)
        with ca2:
            region    = st.selectbox("Region", REGIONS)
        with ca3:
            objective = st.selectbox("Objective", CAMPAIGN_OBJECTIVES)

        if st.button("🚀  Predict KPIs & Generate Campaign"):
            with st.spinner("Running ML model…"):
                pred = get_predictor()
                kpis = pred.predict(platform, region, objective,
                                    bi["personality"],
                                    duration_days=30, budget=5000)
                st.session_state.kpis = kpis
                camp_data = generate_campaign_content(bi, platform, region, objective)
                st.session_state.campaigns[platform] = camp_data

        if st.session_state.kpis:
            kpis = st.session_state.kpis
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            kc1, kc2, kc3, kc4 = st.columns(4)
            for col, (lbl, val, unit) in zip([kc1, kc2, kc3, kc4], [
                ("CTR",        kpis["CTR"],        "%"),
                ("ROI",        kpis["ROI"],        "×"),
                ("Engagement", kpis["Engagement"], "/10"),
                ("Best Time",  kpis["Best_Time"],  ""),
            ]):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                      <span class="metric-val" style="font-size:1.7rem">{val}{unit}</span>
                      <span class="metric-lbl">{lbl}</span>
                    </div>""", unsafe_allow_html=True)

            st.caption(f"Source: {kpis.get('Source','')}")
            if kpis.get("Tip"):
                st.markdown(f"""
                <div style="background:rgba(201,168,76,0.07);border-left:3px solid var(--accent);padding:14px 16px;border-radius:0 8px 8px 0;font-size:0.86rem;line-height:1.65;color:var(--muted);margin-top:12px">
                  💡 {kpis["Tip"]}
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.plotly_chart(kpi_bar_chart(kpis), use_container_width=True)

            region_scores = {r: np.random.randint(58, 86) for r in REGIONS[:-1]}
            region_scores[region] = max(region_scores.values()) + 3
            st.plotly_chart(regional_engagement_map(region_scores), use_container_width=True)

        if st.session_state.campaigns:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="sec-label">Generated Campaign Content</p>', unsafe_allow_html=True)
            for plat, data in st.session_state.campaigns.items():
                with st.expander(f"📱  {plat} Campaign"):
                    st.markdown(f"""
                    <div class="card">
                      <p class="sec-label">Caption</p>
                      <p style="color:var(--text);line-height:1.75;font-size:0.9rem">{data.get("caption","")}</p>
                    </div>""", unsafe_allow_html=True)
                    tags = data.get("hashtags", [])
                    html = " ".join([f'<span class="pill pill-a">{h}</span>' for h in tags])
                    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:10px 0">{html}</div>', unsafe_allow_html=True)
                    if data.get("regional_strategy"):
                        st.markdown(f"""
                        <div class="card">
                          <p class="sec-label">Regional Strategy — {region}</p>
                          <p style="color:var(--muted);font-size:0.87rem;line-height:1.7">{data["regional_strategy"]}</p>
                        </div>""", unsafe_allow_html=True)


        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">💰 Campaign ROI Calculator</p>', unsafe_allow_html=True)
        roi_c1, roi_c2, roi_c3 = st.columns(3, gap="large")
        with roi_c1:
            roi_budget   = st.number_input("Budget (USD $)", min_value=100, max_value=500000,
                                            value=5000, step=500, key="roi_budget")
            roi_platform = st.selectbox("Platform", PLATFORMS, key="roi_plat")
        with roi_c2:
            roi_obj      = st.selectbox("Objective", CAMPAIGN_OBJECTIVES, key="roi_obj")
            roi_aud      = st.number_input("Est. Audience Size", min_value=1000,
                                            max_value=10000000, value=100000,
                                            step=10000, key="roi_aud")
        with roi_c3:
            roi_pers     = st.selectbox("Brand Personality", PERSONALITIES, key="roi_pers",
                                         index=PERSONALITIES.index(
                                             st.session_state.brand_inputs.get("personality","Minimalist")
                                         ) if st.session_state.brand_inputs else 0)
            roi_btn      = st.button("📊  Calculate ROI Projection", key="roi_btn")

        if roi_btn:
            roi_data = calculate_roi(roi_budget, roi_platform, roi_obj, roi_aud, roi_pers)
            roi_color = "#3ECFB2" if roi_data["roi_pct"] > 50 else "#C9A84C" if roi_data["roi_pct"] > 0 else "#E05A5A"

            r1, r2, r3, r4 = st.columns(4)
            for col, (lbl, val, unit) in zip([r1,r2,r3,r4], [
                ("Est. Impressions",  f"{roi_data['impressions']:,}",   ""),
                ("Est. Clicks",       f"{roi_data['clicks']:,}",        ""),
                ("Est. Conversions",  f"{roi_data['conversions']:,}",   ""),
                ("Projected ROI",     f"{roi_data['roi_pct']:+.1f}",    "%"),
            ]):
                with col:
                    color = roi_color if lbl == "Projected ROI" else "var(--accent)"
                    st.markdown(f"""
                    <div class="metric-card">
                      <span class="metric-val" style="font-size:1.6rem;color:{color}">{val}{unit}</span>
                      <span class="metric-lbl">{lbl}</span>
                    </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
            rc1, rc2 = st.columns(2, gap="large")
            with rc1:
                st.markdown(f"""
                <div class="card">
                  <p class="sec-label">Cost Breakdown</p>
                  <div style="font-size:0.86rem;color:var(--text);line-height:1.9">
                    💵 Budget: <strong>${roi_data['budget']:,}</strong><br>
                    🖱  Cost per click: <strong>${roi_data['cost_per_click']}</strong><br>
                    🎯 Cost per conversion: <strong>${roi_data['cost_per_conv']}</strong><br>
                    📈 Est. revenue: <strong>${roi_data['revenue_est']:,}</strong>
                  </div>
                </div>""", unsafe_allow_html=True)
            with rc2:
                import plotly.graph_objects as go_roi
                fig_roi = go_roi.Figure(go_roi.Waterfall(
                    name="ROI", orientation="v",
                    x=["Budget", "Revenue", "Net Return"],
                    y=[-roi_data["budget"], roi_data["revenue_est"],
                       roi_data["revenue_est"] - roi_data["budget"]],
                    connector={"line": {"color": "#2A2C31"}},
                    increasing={"marker": {"color": "#3ECFB2"}},
                    decreasing={"marker": {"color": "#E05A5A"}},
                    totals={"marker":   {"color": "#C9A84C"}},
                ))
                fig_roi.update_layout(
                    paper_bgcolor="#141518", plot_bgcolor="#141518",
                    font_color="#F0EDE8", font_family="DM Sans",
                    height=240, margin=dict(t=20,b=20,l=20,r=20),
                    showlegend=False,
                    xaxis=dict(gridcolor="#2A2C31"),
                    yaxis=dict(gridcolor="#2A2C31"),
                )
                st.plotly_chart(fig_roi, use_container_width=True)
            st.caption(f"ℹ️  {roi_data['note']}")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — MULTILINGUAL STUDIO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="sec-label">Module 05 — Global Reach</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Multilingual <em>Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi    = st.session_state.brand_inputs
        langs = st.multiselect("Target Languages", LANGUAGES_SUPPORTED,
                               default=["Hindi", "Spanish", "French", "German", "Gujarati"])

        slogan_to_translate = (st.session_state.slogans[0]["text"]
                                if st.session_state.slogans
                                else f"{bi.get('company','Brand')} — Excellence by Design")

        st.markdown(f"""
        <div style="background:var(--surface2);border-radius:8px;padding:12px 16px;margin-bottom:16px">
          <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);letter-spacing:0.1em;text-transform:uppercase">Original Tagline</span>
          <div style="font-family:var(--font-head);font-size:1.05rem;font-style:italic;color:var(--text);margin-top:4px">"{slogan_to_translate}"</div>
        </div>""", unsafe_allow_html=True)

        if st.button("🌍  Translate to Selected Languages"):
            with st.spinner("Translating…"):
                results = translate_slogan(slogan_to_translate, bi.get("company","Brand"), langs)
                results = validate_translations(results)
                st.session_state.translations = results

        if st.session_state.translations:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            ml_cols = st.columns(min(len(st.session_state.translations), 3))
            for i, (lang, data) in enumerate(st.session_state.translations.items()):
                with ml_cols[i % 3]:
                    src_pill = "pill-g" if data.get("source") == "gemini" else "pill-a"
                    st.markdown(f"""
                    <div class="lang-card">
                      <div class="lang-name">{data['flag']} {lang} ({data['native']})</div>
                      <div class="lang-text">{data['text']}</div>
                      <div style="margin-top:8px;font-size:0.74rem;color:var(--muted)">{data.get('tone_note','')}</div>
                      <div style="margin-top:6px"><span class="pill {src_pill}">{data.get('source','')}</span></div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — ANIMATION PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<p class="sec-label">Module 06 — Animated Visuals</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Animation <em>Preview</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete Brand Inputs first.")
    else:
        bi = st.session_state.brand_inputs
        ac1, ac2 = st.columns([1, 2], gap="large")
        with ac1:
            style  = st.selectbox("Animation Style", ["typewriter", "fade", "slide"])
            frames = st.slider("Frames", 12, 30, 20)
        with ac2:
            st.markdown(f"""
            <div class="card">
              <p class="sec-label">About this animation</p>
              <p style="font-size:0.85rem;color:var(--muted);line-height:1.65">
                Pillow-based GIF animation combining your brand logo initials, 
                colour palette, and tagline. Supports typewriter, fade-in, and slide-in effects.
                Output: 600×338px, optimised GIF.
              </p>
            </div>""", unsafe_allow_html=True)

        if st.button("🎬  Generate Brand Animation"):
            if not st.session_state.palette:
                st.warning("Generate brand kit first.")
            else:
                tag = (st.session_state.slogans[0]["text"]
                       if st.session_state.slogans else f"{bi['company']} — Excellence by Design")
                svg = (st.session_state.logos[st.session_state.selected_logo]["svg"]
                       if st.session_state.logos else "")
                with st.spinner("Rendering animation…"):
                    gif = create_brand_gif(svg, tag, st.session_state.palette,
                                           bi["company"], style, frames)
                    st.session_state.gif_bytes = gif

        if st.session_state.gif_bytes:
            st.image(st.session_state.gif_bytes, width=560)
            st.download_button("⬇ Download GIF",
                               data=st.session_state.gif_bytes,
                               file_name=f"{bi.get('company','brand')}_animation.gif",
                               mime="image/gif")

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 8 — MOCKUPS & ROI  (NEW)
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<p class="sec-label">New Features</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Mockups & <em>ROI Calculator</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs

    # ── SECTION A: Nano Banana Pro Logo Generator ────────────────────────────
    st.markdown('<p class="sec-label">🍌 AI Logo Generator — Nano Banana Pro</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="card-title">Nano Banana Pro Image Generation</div>
      <div class="card-sub">Uses Google's Gemini image model to generate a real AI-rendered logo alongside your SVG concepts. Requires Gemini API key. Uses the <code>gemini-2.0-flash-preview-image-generation</code> model.</div>
    </div>""", unsafe_allow_html=True)

    nb_col1, nb_col2 = st.columns([1, 1], gap="large")
    with nb_col1:
        nb_style = st.selectbox("Logo Style Prompt", [
            "Minimalist vector logo",
            "Bold geometric mark",
            "Luxury monogram",
            "Modern wordmark",
            "Abstract icon",
        ], key="nb_style_1")
        nb_bg = st.radio("Background", ["White", "Transparent (white)", "Brand Color"], horizontal=True, key="nb_bg")

    with nb_col2:
        st.markdown(f"""
        <div class="card">
          <p class="sec-label">What Nano Banana Pro generates</p>
          <p style="font-size:0.84rem;color:var(--muted);line-height:1.65">
            A real AI-rendered PNG logo based on your brand inputs, personality, and colour palette.
            This complements the 5 SVG concepts with an AI-generated visual.<br><br>
            <span style="color:var(--accent)">⚡ Requires Gemini API key</span>
          </p>
        </div>""", unsafe_allow_html=True)

    if st.button("🍌  Generate with Nano Banana Pro"):
        if not st.session_state.gemini_ok:
            st.warning("Connect your Gemini API key to use Nano Banana Pro.")
        elif not bi:
            st.warning("Complete Brand Inputs first.")
        else:
            with st.spinner("Generating AI logo with Nano Banana Pro…"):
                png = generate_logo_imagen(
                    bi.get("company","Brand"),
                    bi.get("industry","Technology"),
                    bi.get("personality","Minimalist"),
                    st.session_state.palette or {}
                )
            if png:
                st.image(png, width=300, caption="Generated by Nano Banana Pro (Gemini)")
                st.download_button("⬇ Download AI Logo PNG", data=png,
                    file_name=f"{bi.get('company','brand')}_nb_logo.png", mime="image/png")
                st.success("✅ Nano Banana Pro logo generated!")
            else:
                st.info("ℹ️ Nano Banana Pro image generation requires the Gemini 2.0 Flash image preview model. "
                        "If unavailable in your region, the SVG logos in the Logo Studio tab are your brand assets.")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECTION B: Brand Mockup Generator ───────────────────────────────────
    st.markdown('<p class="sec-label">🖼 Brand Mockup Generator</p>', unsafe_allow_html=True)
    if not st.session_state.palette:
        st.info("👈 Complete Brand Inputs first to generate mockups.")
    else:
        mock_types = ["Business Card", "T-Shirt", "Coffee Mug", "Phone Case", "Letterhead"]
        mc1, mc2 = st.columns([1, 2], gap="large")
        with mc1:
            selected_mocks = st.multiselect("Select Mockups to Generate",
                                             mock_types, default=["Business Card", "Coffee Mug"])
        with mc2:
            st.markdown("""
            <div class="card">
              <p class="sec-label">About Mockups</p>
              <p style="font-size:0.83rem;color:var(--muted);line-height:1.65">
                Pillow-rendered mockups applying your brand logo, palette, and company name
                to real-world objects. Each is downloadable as a PNG.
              </p>
            </div>""", unsafe_allow_html=True)

        if st.button("🎨  Generate Mockups"):
            if not selected_mocks:
                st.warning("Select at least one mockup type.")
            else:
                svg = st.session_state.logos[st.session_state.selected_logo]["svg"] if st.session_state.logos else ""
                mock_cols = st.columns(min(len(selected_mocks), 3))
                for i, mtype in enumerate(selected_mocks):
                    with mock_cols[i % 3]:
                        with st.spinner(f"Rendering {mtype}…"):
                            png = generate_mockup(svg, st.session_state.palette,
                                                   bi.get("company","Brand") if bi else "Brand", mtype)
                        st.image(png, caption=mtype, use_container_width=True)
                        st.download_button(
                            f"⬇ {mtype}", data=png,
                            file_name=f"{(bi.get('company','brand') if bi else 'brand').replace(' ','_')}_{mtype.replace(' ','_')}.png",
                            mime="image/png", key=f"dl_mock_{i}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECTION C: Dark / Light Palette Switcher ─────────────────────────────
    st.markdown('<p class="sec-label">🌗 Dark / Light Palette Switcher</p>', unsafe_allow_html=True)
    if not st.session_state.palette:
        st.info("👈 Complete Brand Inputs first.")
    else:
        sw1, sw2 = st.columns(2, gap="large")
        palette = st.session_state.palette
        colors  = list(palette.values())

        def invert_palette(pal):
            """Generate light/dark variant of palette."""
            from src.palette_engine import hex_to_rgb, rgb_to_hex, adjust_saturation
            result = {}
            for name, v in pal.items():
                rgb  = hex_to_rgb(v["hex"])
                lum  = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
                if lum < 128:
                    # Dark → make lighter
                    light_rgb = [min(255, int(c + (255-c)*0.6)) for c in rgb]
                    new_hex = rgb_to_hex(light_rgb)
                else:
                    # Light → make darker
                    dark_rgb = [int(c * 0.25) for c in rgb]
                    new_hex = rgb_to_hex(dark_rgb)
                result[name] = {**v, "hex": new_hex}
            return result

        with sw1:
            st.markdown('<p class="sec-label">🌙 Dark Mode Palette</p>', unsafe_allow_html=True)
            swatch_h = '<div style="display:flex;gap:8px;margin:10px 0">'
            for v in colors:
                swatch_h += f'<div style="flex:1;height:48px;border-radius:8px;background:{v["hex"]};display:flex;align-items:flex-end;padding:4px 6px"><span style="font-family:var(--font-mono);font-size:0.52rem;color:rgba(255,255,255,0.7)">{v["hex"]}</span></div>'
            swatch_h += '</div>'
            st.markdown(swatch_h, unsafe_allow_html=True)
            for name, v in palette.items():
                st.markdown(f'<div style="font-family:var(--font-mono);font-size:0.62rem;color:var(--muted);padding:2px 0">{name}: <span style="color:var(--accent)">{v["hex"]}</span></div>', unsafe_allow_html=True)

        with sw2:
            st.markdown('<p class="sec-label">☀️ Light Mode Palette</p>', unsafe_allow_html=True)
            light_pal = invert_palette(palette)
            swatch_h2 = '<div style="display:flex;gap:8px;margin:10px 0">'
            for v in light_pal.values():
                swatch_h2 += f'<div style="flex:1;height:48px;border-radius:8px;background:{v["hex"]};border:1px solid rgba(0,0,0,0.1);display:flex;align-items:flex-end;padding:4px 6px"><span style="font-family:var(--font-mono);font-size:0.52rem;color:rgba(0,0,0,0.5)">{v["hex"]}</span></div>'
            swatch_h2 += '</div>'
            st.markdown(swatch_h2, unsafe_allow_html=True)
            for name, v in light_pal.items():
                st.markdown(f'<div style="font-family:var(--font-mono);font-size:0.62rem;color:var(--muted);padding:2px 0">{name}: <span style="color:var(--accent)">{v["hex"]}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── SECTION D: Campaign ROI Calculator ───────────────────────────────────
    st.markdown('<p class="sec-label">💰 Campaign ROI Calculator</p>', unsafe_allow_html=True)
    rc1, rc2, rc3 = st.columns(3, gap="large")
    with rc1:
        roi_budget   = st.number_input("Campaign Budget ($)", min_value=100, max_value=1000000,
                                        value=5000, step=500, key="roi_budget_1")
        roi_platform = st.selectbox("Platform", PLATFORMS, key="roi_plat_1")
    with rc2:
        roi_obj      = st.selectbox("Objective", CAMPAIGN_OBJECTIVES, key="roi_obj_1")
        roi_days     = st.slider("Duration (days)", 7, 90, 30, key="roi_days")
    with rc3:
        roi_audience = st.number_input("Est. Audience Size", min_value=1000,
                                        max_value=50000000, value=100000, step=10000, key="roi_aud_1")
        roi_ctr      = st.slider("Expected CTR (%)", 0.5, 10.0, 2.5, step=0.1, key="roi_ctr")

    if st.button("📊  Calculate ROI Projection"):
        roi = calculate_roi(roi_budget, roi_platform, roi_obj,
                             roi_days, roi_audience, roi_ctr)

        # KPI cards
        k1,k2,k3,k4 = st.columns(4)
        for col, (label, val, suffix) in zip([k1,k2,k3,k4], [
            ("Est. Impressions", f"{roi['impressions']:,}",       ""),
            ("Est. Clicks",      f"{roi['clicks']:,}",            ""),
            ("Conversions",      f"{roi['conversions']:,}",       ""),
            ("Est. Revenue",     f"${roi['revenue']:,}",          ""),
        ]):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <span class="metric-val" style="font-size:1.5rem">{val}</span>
                  <span class="metric-lbl">{label}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:16px"></div>', unsafe_allow_html=True)
        k5,k6,k7,k8 = st.columns(4)
        for col, (label, val, color) in zip([k5,k6,k7,k8], [
            ("ROI",   f"{roi['roi_pct']}%", "#3ECFB2" if roi['roi_pct'] > 0 else "#E05A5A"),
            ("ROAS",  f"{roi['roas']}×",    "#3ECFB2" if roi['roas'] > 1 else "#E05A5A"),
            ("CPC",   f"${roi['cpc']}",     "#C9A84C"),
            ("CPA",   f"${roi['cpa']}",     "#C9A84C"),
        ]):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <span class="metric-val" style="font-size:1.6rem;color:{color}">{val}</span>
                  <span class="metric-lbl">{label}</span>
                </div>""", unsafe_allow_html=True)

        # Visual funnel
        st.markdown('<div style="margin-top:20px"></div>', unsafe_allow_html=True)
        funnel_data = [
            ("Audience Reached",   roi['impressions'],  "#1B3A6B"),
            ("Clicks Generated",   roi['clicks'],        "#C9A84C"),
            ("Conversions",        roi['conversions'],   "#3ECFB2"),
        ]
        max_val = max(v for _, v, _ in funnel_data) or 1
        for label, val, color in funnel_data:
            pct = int(val / max_val * 100)
            st.markdown(f"""
            <div style="margin:6px 0">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted)">{label}</span>
                <span style="font-family:var(--font-mono);font-size:0.65rem;color:{color}">{val:,}</span>
              </div>
              <div style="background:var(--surface2);border-radius:4px;height:10px;overflow:hidden">
                <div style="width:{pct}%;height:100%;background:{color};border-radius:4px;transition:width 0.5s ease"></div>
              </div>
            </div>""", unsafe_allow_html=True)

        # ROI Tip
        tip = ""
        if roi["roi_pct"] < 0:
            tip = f"⚠️ Negative ROI projected. Consider increasing budget, refining targeting, or switching to a higher-converting platform."
        elif roi["roi_pct"] < 50:
            tip = f"💡 Moderate ROI. Optimise your landing page conversion rate and audience targeting to improve returns."
        else:
            tip = f"🚀 Strong ROI projected. Consider scaling budget by 20–30% to maximise this campaign's momentum."
        st.markdown(f"""
        <div style="background:rgba(201,168,76,0.07);border-left:3px solid var(--accent);padding:14px 16px;border-radius:0 8px 8px 0;font-size:0.86rem;line-height:1.65;color:var(--muted);margin-top:12px">
          {tip}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 9 — FEEDBACK
# ══════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    st.markdown('<p class="sec-label">Module 07 — Feedback Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Rate & <em>Refine</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    MODULES = ["Logo & Design Studio", "Creative Content Hub",
               "Campaign Analytics", "Multilingual Studio", "Overall Brand Kit"]
    fb_module = st.selectbox("Rate Module", MODULES)
    fb1, fb2  = st.columns([1, 2], gap="large")
    with fb1:
        rating = st.slider("Rating (1–5)", 1, 5, 4, label_visibility="collapsed")
        stars  = "⭐" * rating + "☆" * (5 - rating)
        quality = {1:"Poor",2:"Below Average",3:"Average",4:"Good",5:"Excellent"}[rating]
        pill   = "pill-r" if rating <= 2 else "pill-a" if rating == 3 else "pill-g"
        st.markdown(f'<div style="font-size:1.8rem;letter-spacing:4px;margin:10px 0">{stars}</div>', unsafe_allow_html=True)
        st.markdown(f'<span class="pill {pill}">{quality}</span>', unsafe_allow_html=True)
    with fb2:
        comment   = st.text_area("Feedback", placeholder="What worked? What could be better?", height=90)
        preferred = st.text_input("Preferred Alternative (optional)", placeholder="e.g. More vibrant palette…")

    bi = st.session_state.brand_inputs
    if st.button("📤  Submit Feedback"):
        save_feedback(st.session_state.session_id,
                      bi.get("company",""), bi.get("industry",""),
                      fb_module, rating, comment, preferred)
        record = {"timestamp": datetime.datetime.now().isoformat(),
                  "module": fb_module, "rating": rating,
                  "sentiment": "positive" if rating >= 4 else "neutral" if rating == 3 else "negative",
                  "comment": comment}
        st.session_state.feedback_log.append(record)
        st.success(f"✓ Feedback saved — Rating {rating}/5 (written to feedback_data.csv)")

    if st.session_state.feedback_log:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Session Feedback Log</p>', unsafe_allow_html=True)
        df_log = pd.DataFrame(st.session_state.feedback_log)
        st.dataframe(df_log[["timestamp","module","rating","sentiment","comment"]]
                     .rename(columns={"timestamp":"Time","module":"Module",
                                      "rating":"Rating","sentiment":"Sentiment","comment":"Comment"}),
                     use_container_width=True, hide_index=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Feedback Analytics</p>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            st.plotly_chart(feedback_bar(df_log), use_container_width=True)
        with fc2:
            st.plotly_chart(feedback_pie(df_log), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 10 — DOWNLOAD KIT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown('<p class="sec-label">Module 08 — Export Engine</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="sec-title">Download Brand <em>Kit</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    bi = st.session_state.brand_inputs
    if not bi:
        st.info("👈 Complete Brand Inputs first.")
    else:
        # Progress checklist
        checks = [
            ("Brand Inputs",        bool(bi)),
            ("Logos Generated",     bool(st.session_state.logos)),
            ("Colour Palette",      bool(st.session_state.palette)),
            ("Font Recommendations",bool(st.session_state.fonts)),
            ("Taglines Created",    bool(st.session_state.slogans)),
            ("Brand Story",         bool(st.session_state.brand_story)),
            ("Translations",        bool(st.session_state.translations)),
            ("Campaign Content",    bool(st.session_state.campaigns)),
            ("KPI Predictions",     bool(st.session_state.kpis)),
            ("Animation",           bool(st.session_state.gif_bytes)),
        ]
        done = sum(1 for _, v in checks if v)
        pct  = int(done / len(checks) * 100)

        st.markdown(f"""
        <div style="margin-bottom:20px">
          <div style="display:flex;justify-content:space-between;margin-bottom:5px">
            <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--muted)">KIT COMPLETENESS — {done}/{len(checks)}</span>
            <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--accent)">{pct}%</span>
          </div>
          <div class="prog-wrap" style="height:12px"><div class="prog-bar" style="width:{pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

        for label, done_flag in checks:
            icon  = "✓" if done_flag else "○"
            color = "var(--teal)" if done_flag else "var(--muted)"
            st.markdown(f"""
            <div class="check-item">
              <span style="color:{color}">{icon}</span>
              <span style="font-size:0.87rem;color:{'var(--text)' if done_flag else 'var(--muted)'}">{label}</span>
              {'<span class="pill pill-g" style="margin-left:auto">done</span>' if done_flag else ''}
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Social Media Post Previewer
        if st.session_state.palette:
            st.markdown('<p class="sec-label">📱 Social Media Post Previewer</p>', unsafe_allow_html=True)
            prev_plat = st.selectbox("Preview for platform", PLATFORMS, key="prev_plat2")
            if st.button("👁  Generate Post Preview"):
                bi2 = st.session_state.brand_inputs
                slg = st.session_state.slogans[0]["text"] if st.session_state.slogans else f"Discover {bi2.get('company','')}"
                with st.spinner("Building preview…"):
                    prev = generate_post_preview(
                        bi2.get("company",""), bi2.get("industry",""),
                        bi2.get("personality",""), prev_plat, slg,
                        st.session_state.palette)
                colors = list(st.session_state.palette.values())
                bg  = colors[0]["hex"] if colors else "#1B3A6B"
                acc = colors[1]["hex"] if len(colors) > 1 else "#C9A84C"
                hashtag_html = " ".join([f'<span style="color:{acc};font-size:0.8rem">{h}</span>' for h in prev.get("hashtags",[])])
                pv1, pv2 = st.columns([1,1], gap="large")
                with pv1:
                    st.markdown(f"""
                    <div style="background:{bg};border-radius:14px;padding:22px;max-width:340px;border:1px solid rgba(255,255,255,0.1)">
                      <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
                        <div style="width:36px;height:36px;border-radius:50%;background:{acc};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.95rem;color:{bg}">{bi2.get("company","B")[0].upper()}</div>
                        <div><div style="font-weight:600;font-size:0.86rem;color:white">{bi2.get("company","Brand")}</div>
                        <div style="font-size:0.68rem;color:rgba(255,255,255,0.45)">Sponsored · {prev_plat}</div></div>
                      </div>
                      <div style="font-size:0.8rem;color:rgba(255,255,255,0.85);line-height:1.65;margin-bottom:12px">{prev.get("caption","")[:220]}</div>
                      <div style="margin-bottom:10px;display:flex;flex-wrap:wrap;gap:4px">{hashtag_html}</div>
                      <div style="background:{acc};color:{bg};padding:7px 16px;border-radius:20px;font-size:0.72rem;font-weight:700;display:inline-block">{prev.get("cta","Learn More →")}</div>
                    </div>""", unsafe_allow_html=True)
                with pv2:
                    st.markdown(f"""
                    <div class="card">
                      <p class="sec-label">Platform Specs</p>
                      <div style="font-size:0.84rem;color:var(--text);line-height:1.9">
                        📏 <strong>Char limit:</strong> {prev.get("char_limit","—")}<br>
                        🎯 <strong>Best format:</strong> {prev.get("best_format","—")}<br>
                        #️⃣  <strong>Hashtags:</strong> {prev.get("hashtag_count","—")}<br>
                        💬 <strong>Hook:</strong> <em style="color:var(--accent)">{prev.get("hook","")[:80]}</em>
                      </div>
                    </div>""", unsafe_allow_html=True)

        # Brand Personality Radar
        if bi.get("personality"):
            st.plotly_chart(personality_radar(bi["personality"]), use_container_width=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Download button
        if st.button("📦  Build & Download Brand Kit ZIP"):
            with st.spinner("Packaging assets…"):
                zip_bytes = build_brand_kit_zip(
                    company     = bi.get("company","brand"),
                    industry    = bi.get("industry",""),
                    personality = bi.get("personality",""),
                    logos       = st.session_state.logos or [],
                    palette     = st.session_state.palette or {},
                    fonts       = st.session_state.fonts or [],
                    slogans     = st.session_state.slogans or [],
                    brand_story = st.session_state.brand_story or "",
                    translations= st.session_state.translations or {},
                    campaigns   = st.session_state.campaigns or {},
                    kpis        = st.session_state.kpis or {},
                    aesthetics  = st.session_state.aesthetics or {},
                    gif_bytes   = st.session_state.gif_bytes,
                )
            st.download_button(
                "⬇  Download Brand Kit ZIP",
                data=zip_bytes,
                file_name=f"{bi.get('company','Brand').replace(' ','_')}_BrandKit.zip",
                mime="application/zip",
            )

        # AI Brand Chatbot — Enhanced
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">🤖 Brand AI Assistant</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <div class="card-title">Your Personal Brand Strategist</div>
          <div class="card-sub">Context-aware AI that knows your brand — ask about strategy, copy, campaigns, positioning, or anything branding related. Powered by Gemini 2.0 Flash.</div>
        </div>""", unsafe_allow_html=True)

        # Quick Action Buttons
        if not st.session_state.chat_history:
            st.markdown('<p class="sec-label" style="margin-top:14px">⚡ Quick Actions</p>', unsafe_allow_html=True)
            company_name = bi.get("company","your brand")
            industry_name = bi.get("industry","your industry")
            top_tag = st.session_state.slogans[0]["text"] if st.session_state.slogans else "our tagline"
            quick_actions = [
                ("📝 Improve Tagline",   f"Give me 3 improved, more powerful versions of this tagline: '{top_tag}' for a {industry_name} brand."),
                ("🎯 Customer Persona",  f"Build a detailed customer persona for {company_name}. Include name, age, occupation, goals, pain points, and buying behavior."),
                ("📣 30-Day Plan",       f"Create a 30-day social media content calendar for launching {company_name} in the {industry_name} space. Give week-by-week themes."),
                ("🏆 Differentiation",  f"What makes {company_name} unique vs competitors in {industry_name}? Give 5 specific differentiators I should highlight."),
                ("💌 Elevator Pitch",   f"Write a 30-second elevator pitch for {company_name}. Make it memorable, confident, and tailored to {industry_name}."),
                ("📈 Growth Strategy",  f"Suggest 5 growth marketing strategies specifically for a {bi.get('personality','').lower()} brand in {industry_name}. Be specific and actionable."),
            ]
            qa_cols = st.columns(3)
            for i, (label, prompt) in enumerate(quick_actions):
                with qa_cols[i % 3]:
                    if st.button(label, key=f"qa_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role":"user","content":prompt})
                        ctx = (f"Brand: {company_name} | Industry: {industry_name} | "
                               f"Personality: {bi.get('personality','')} | Tone: {bi.get('tone','')} | "
                               f"Audience: {bi.get('audience','')} | Top tagline: {top_tag}")
                        sys_prompt = (
                            f"You are BrandSphere AI — an expert brand strategist, copywriter, and marketing consultant. "
                            f"Brand context: {ctx}. "
                            "Be specific to THIS brand — never generic. Use bullet points for lists. "
                            "Be concise but complete (5–8 sentences or bullet points max)."
                        )
                        reply = gemini_call(prompt, system=sys_prompt) if st.session_state.gemini_ok else "🔑 Connect your Gemini API key for live AI responses."
                        st.session_state.chat_history.append({"role":"assistant","content":reply})
                        st.rerun()

        for msg in st.session_state.chat_history:
            role = "You" if msg["role"] == "user" else "BrandSphere AI"
            bg   = "var(--surface2)" if msg["role"] == "user" else "var(--surface)"
            bc   = "var(--accent)"   if msg["role"] == "assistant" else "var(--border)"
            align = "flex-end" if msg["role"] == "user" else "flex-start"
            st.markdown(f"""
            <div style="display:flex;justify-content:{align};margin:7px 0">
              <div style="max-width:75%;background:{bg};border:1px solid {bc};border-radius:10px;padding:12px 16px">
                <div style="font-family:var(--font-mono);font-size:0.52rem;color:var(--accent);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:5px">{role}</div>
                <div style="font-size:0.87rem;line-height:1.65;color:var(--text)">{msg['content']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        chat_c1, chat_c2 = st.columns([5, 1])
        with chat_c1:
            user_q = st.text_input("Ask BrandSphere AI…", key="chat_q",
                                   placeholder="e.g. What's the best platform for a luxury brand?",
                                   label_visibility="collapsed")
        with chat_c2:
            send_btn = st.button("Send →")

        if send_btn and user_q.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_q.strip()})
            ctx = f"Brand: {bi.get('company','')} | Industry: {bi.get('industry','')} | Personality: {bi.get('personality','')}"
            if st.session_state.gemini_ok:
                reply = gemini_call(
                    user_q.strip(),
                    system=f"You are BrandSphere AI, a branding expert. Context: {ctx}. Be concise (3–5 sentences)."
                )
            else:
                reply = "🔑 Connect your Gemini API key in the API Configuration section to get live AI answers."
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
