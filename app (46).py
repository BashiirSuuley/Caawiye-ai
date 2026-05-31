"""
Caawiye AI v5 — Academic AI Platform
Inspired by NotebookLM's 3-panel design
PDF → Slides · MCQ · Exam · Summary · Flashcards · Quiz · AI Tutor
EN / AR Bilingual · Zero extra packages
"""
import streamlit as st
import requests, json, re, base64, io, zipfile, random

st.set_page_config(
    page_title="Caawiye AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Google+Sans+Display:wght@400;700&family=Amiri:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Syne:wght@400;500;600;700;800&family=Amiri:wght@400;700&display=swap');

/* ══ RESET ══════════════════════════════════════════════════ */
*{box-sizing:border-box;margin:0;padding:0;}
html,body,[class*="css"]{
  font-family:'DM Sans',sans-serif!important;
  background:#0f0f13!important;
  color:#e8eaf0!important;
}
.stApp{background:#0f0f13!important;}
#MainMenu,footer,header{visibility:hidden!important;}

/* ══ HIDE DEFAULT SIDEBAR ═══════════════════════════════════ */
section[data-testid="stSidebar"]{display:none!important;}
.stDeployButton{display:none!important;}

/* ══ INPUTS — always visible ════════════════════════════════ */
input, textarea,
.stTextInput input,
.stTextArea textarea,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea{
  background:#1e1f2e!important;
  border:1.5px solid rgba(124,58,237,.3)!important;
  border-radius:10px!important;
  color:#f0f2ff!important;
  font-family:'DM Sans',sans-serif!important;
  font-size:.88rem!important;
  caret-color:#a78bfa!important;
}
input:focus, textarea:focus,
.stTextInput input:focus,
.stTextArea textarea:focus{
  border-color:#7c3aed!important;
  box-shadow:0 0 0 3px rgba(124,58,237,.18)!important;
  outline:none!important;
}
input::placeholder, textarea::placeholder,
.stTextInput input::placeholder,
.stTextArea textarea::placeholder{
  color:#4b5280!important;opacity:1!important;
}

/* ══ SELECT / NUMBER ════════════════════════════════════════ */
.stSelectbox>div>div,
div[data-testid="stSelectbox"]>div>div{
  background:#1e1f2e!important;
  border:1.5px solid rgba(124,58,237,.25)!important;
  border-radius:10px!important;color:#f0f2ff!important;
}
.stNumberInput input{
  background:#1e1f2e!important;
  border:1.5px solid rgba(124,58,237,.25)!important;
  color:#f0f2ff!important;border-radius:8px!important;
}

/* ══ BUTTONS ════════════════════════════════════════════════ */
.stButton>button{
  font-family:'DM Sans',sans-serif!important;
  font-weight:600!important;border-radius:10px!important;
  transition:all .2s!important;font-size:.84rem!important;
  color:#c4b5fd!important;
  background:rgba(124,58,237,.1)!important;
  border:1px solid rgba(124,58,237,.25)!important;
}
.stButton>button:hover{
  background:rgba(124,58,237,.2)!important;
  border-color:rgba(124,58,237,.5)!important;
  transform:translateY(-1px)!important;
  box-shadow:0 4px 16px rgba(124,58,237,.2)!important;
}
button[kind="primary"],.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#6d28d9,#7c3aed,#8b5cf6)!important;
  border:none!important;color:#fff!important;
  box-shadow:0 4px 20px rgba(124,58,237,.35)!important;
  font-weight:700!important;
}
button[kind="primary"]:hover{
  box-shadow:0 8px 28px rgba(124,58,237,.5)!important;
  transform:translateY(-2px)!important;
}
button[kind="secondary"]{
  background:rgba(255,255,255,.03)!important;
  border:1px solid rgba(255,255,255,.1)!important;
  color:#6b7280!important;
}

/* ══ TOP NAV BAR ════════════════════════════════════════════ */
.top-nav{
  display:flex;align-items:center;
  background:rgba(15,15,19,.95);
  border-bottom:1px solid rgba(124,58,237,.15);
  padding:.65rem 1.5rem;
  position:sticky;top:0;z-index:999;
  backdrop-filter:blur(20px);
  gap:1.2rem;
}
.nav-logo{
  display:flex;align-items:center;gap:.6rem;flex-shrink:0;
}
.nav-logo-icon{
  width:32px;height:32px;border-radius:8px;
  background:linear-gradient(135deg,#6d28d9,#8b5cf6);
  display:flex;align-items:center;justify-content:center;
  font-size:1rem;box-shadow:0 2px 10px rgba(124,58,237,.4);
}
.nav-logo-text{
  font-family:'Syne',sans-serif;font-weight:800;font-size:1.1rem;
  background:linear-gradient(135deg,#fff,#c4b5fd);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.nav-logo-sub{font-size:.65rem;color:#6b7280;margin-top:-2px;}
.nav-pdf-slot{
  flex:1;max-width:380px;
  background:rgba(124,58,237,.07);
  border:1px dashed rgba(124,58,237,.3);
  border-radius:10px;padding:.4rem .9rem;
  font-size:.78rem;color:#6b7280;
  display:flex;align-items:center;gap:.5rem;cursor:pointer;
  transition:all .2s;
}
.nav-pdf-slot:hover{border-color:rgba(124,58,237,.55);color:#c4b5fd;}
.nav-pdf-slot.has-file{
  border-style:solid;border-color:rgba(124,58,237,.4);
  background:rgba(124,58,237,.12);color:#c4b5fd;
}
.nav-pills{display:flex;gap:.35rem;align-items:center;}
.nav-pill{
  padding:.32rem .75rem;border-radius:20px;font-size:.75rem;
  font-weight:600;cursor:pointer;transition:all .18s;
  color:#6b7280;background:transparent;
  border:1px solid transparent;white-space:nowrap;
}
.nav-pill:hover{color:#c4b5fd;background:rgba(124,58,237,.1);}
.nav-pill.active{
  color:#fff;background:rgba(124,58,237,.2);
  border-color:rgba(124,58,237,.4);
}
.nav-right{margin-left:auto;display:flex;align-items:center;gap:.7rem;}
.nav-badge{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.2);
  border-radius:20px;padding:.28rem .75rem;font-size:.7rem;
  color:#a78bfa;font-weight:600;
}
.nav-badge .dot{width:6px;height:6px;border-radius:50%;background:#10b981;
  display:inline-block;animation:pulse3 2s infinite;}
@keyframes pulse3{0%,100%{opacity:1}50%{opacity:.3}}
.lang-toggle{
  display:flex;background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);border-radius:8px;
  overflow:hidden;
}
.lang-opt{
  padding:.3rem .65rem;font-size:.72rem;font-weight:600;
  cursor:pointer;transition:all .15s;color:#6b7280;
}
.lang-opt.active{background:rgba(124,58,237,.25);color:#c4b5fd;}

/* ══ 3-PANEL LAYOUT ════════════════════════════════════════ */
.three-panel{
  display:grid;
  grid-template-columns:280px 1fr 340px;
  height:calc(100vh - 58px);
  overflow:hidden;
}

/* ── LEFT PANEL — Sources ── */
.panel-left{
  background:#13131a;
  border-right:1px solid rgba(255,255,255,.06);
  overflow-y:auto;padding:1.2rem 1rem;
  display:flex;flex-direction:column;gap:.8rem;
}
.panel-section-title{
  font-size:.65rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.14em;color:#4b5280;margin-bottom:.3rem;
}
.source-card{
  background:rgba(124,58,237,.07);
  border:1px solid rgba(124,58,237,.18);
  border-radius:12px;padding:.85rem;
  transition:all .18s;cursor:pointer;
}
.source-card:hover{
  background:rgba(124,58,237,.13);
  border-color:rgba(124,58,237,.35);
  transform:translateX(2px);
}
.source-card.active{
  background:rgba(124,58,237,.18);
  border-color:rgba(124,58,237,.5);
}
.source-name{font-size:.82rem;font-weight:600;color:#e2e8f0;margin-bottom:.2rem;}
.source-meta{font-size:.7rem;color:#4b5280;}
.source-actions{display:flex;gap:.35rem;margin-top:.5rem;}
.src-btn{
  font-size:.68rem;padding:.22rem .6rem;border-radius:6px;
  background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.2);
  color:#a78bfa;cursor:pointer;transition:all .15s;
  font-family:'DM Sans',sans-serif;font-weight:600;
}
.src-btn:hover{background:rgba(124,58,237,.22);}
.upload-zone{
  border:2px dashed rgba(124,58,237,.3);
  border-radius:14px;padding:1.5rem;text-align:center;
  transition:all .2s;cursor:pointer;
}
.upload-zone:hover{
  border-color:rgba(124,58,237,.55);
  background:rgba(124,58,237,.06);
}
.upload-icon{font-size:2rem;margin-bottom:.5rem;}
.upload-text{font-size:.78rem;color:#6b7280;line-height:1.5;}
.upload-text b{color:#c4b5fd;}

/* ── CENTER PANEL — Tools / Chat ── */
.panel-center{
  overflow-y:auto;background:#0f0f13;
  display:flex;flex-direction:column;
}
.center-inner{padding:1.4rem 1.6rem;flex:1;}

/* Tool tabs */
.tool-tabs{
  display:flex;gap:.3rem;padding:.5rem;
  background:#13131a;border-bottom:1px solid rgba(255,255,255,.05);
  flex-wrap:wrap;position:sticky;top:0;z-index:10;
}
.tool-tab{
  padding:.38rem .85rem;border-radius:8px;font-size:.78rem;
  font-weight:600;cursor:pointer;transition:all .18s;
  color:#6b7280;background:transparent;border:1px solid transparent;
  font-family:'DM Sans',sans-serif;white-space:nowrap;
}
.tool-tab:hover{color:#c4b5fd;background:rgba(124,58,237,.1);}
.tool-tab.active{
  color:#fff;background:rgba(124,58,237,.2);
  border-color:rgba(124,58,237,.4);
}

/* Section headings */
.tool-heading{
  font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
  color:#fff;margin-bottom:.3rem;
}
.tool-subheading{font-size:.8rem;color:#4b5280;margin-bottom:1.1rem;line-height:1.5;}

/* Custom prompt box */
.prompt-box{
  background:rgba(124,58,237,.06);
  border:1px solid rgba(124,58,237,.2);
  border-radius:12px;padding:1rem 1.1rem;
  margin-bottom:1rem;
}
.prompt-label{
  font-size:.68rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.1em;color:#7c3aed;margin-bottom:.5rem;
  display:flex;align-items:center;gap:5px;
}

/* ── RIGHT PANEL — Studio / Output ── */
.panel-right{
  background:#13131a;
  border-left:1px solid rgba(255,255,255,.06);
  overflow-y:auto;padding:1.1rem 1rem;
}
.studio-title{
  font-family:'Syne',sans-serif;font-size:.95rem;font-weight:700;
  color:#e2e8f0;margin-bottom:.2rem;display:flex;align-items:center;gap:.5rem;
}
.studio-sub{font-size:.72rem;color:#4b5280;margin-bottom:1rem;}
.output-card{
  background:rgba(124,58,237,.07);
  border:1px solid rgba(124,58,237,.15);
  border-radius:12px;padding:.9rem;margin-bottom:.7rem;
  transition:all .18s;
}
.output-card:hover{
  border-color:rgba(124,58,237,.35);
  background:rgba(124,58,237,.12);
}
.output-card-icon{font-size:1.5rem;margin-bottom:.4rem;}
.output-card-title{font-size:.85rem;font-weight:700;color:#e2e8f0;margin-bottom:.2rem;}
.output-card-desc{font-size:.72rem;color:#4b5280;line-height:1.5;}
.output-card-btn{
  display:inline-flex;align-items:center;gap:5px;
  background:linear-gradient(135deg,#6d28d9,#7c3aed);
  color:#fff;border:none;border-radius:8px;
  padding:.35rem .8rem;font-size:.74rem;font-weight:700;
  cursor:pointer;margin-top:.6rem;transition:all .2s;
  font-family:'DM Sans',sans-serif;
  box-shadow:0 2px 10px rgba(124,58,237,.3);
}
.output-card-btn:hover{transform:translateY(-1px);box-shadow:0 4px 16px rgba(124,58,237,.45);}
.output-card-btn:disabled{opacity:.4;cursor:not-allowed;transform:none;}

/* ══ CONTENT CARDS ══════════════════════════════════════════ */
.content-card{
  background:#1a1b27;border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:1.1rem 1.2rem;margin-bottom:.8rem;
}
.card-title{
  font-size:.68rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.11em;color:#7c3aed;margin-bottom:.6rem;
  display:flex;align-items:center;gap:5px;
}
.card-title::before{
  content:'';width:3px;height:12px;
  background:linear-gradient(180deg,#7c3aed,#a78bfa);
  border-radius:2px;display:inline-block;
}

/* ══ MCQ ════════════════════════════════════════════════════ */
.mcq-wrap{
  background:#1a1b27;border:1px solid rgba(255,255,255,.05);
  border-radius:12px;padding:1rem 1.1rem;margin-bottom:.75rem;
  transition:border-color .2s;
}
.mcq-wrap:hover{border-color:rgba(124,58,237,.3);}
.mcq-q{font-weight:600;font-size:.91rem;color:#e8eaf0;margin-bottom:.5rem;line-height:1.55;}
.mcq-ar{font-family:'Amiri',serif;font-size:.94rem;color:#8b5cf6;direction:rtl;text-align:right;margin-bottom:.4rem;}
.mcq-opt{
  display:flex;align-items:flex-start;gap:9px;padding:.3rem .45rem;
  border-radius:7px;font-size:.83rem;color:#64748b;
  margin-bottom:2px;border:1px solid transparent;transition:all .15s;
}
.mcq-opt.ok{background:rgba(16,185,129,.07);border-color:rgba(16,185,129,.25);color:#34d399;}
.mcq-ltr{font-family:'Syne',sans-serif;font-weight:700;color:#8b5cf6;min-width:17px;}
.mcq-exp{
  background:rgba(124,58,237,.08);border-left:3px solid #7c3aed;
  border-radius:0 7px 7px 0;padding:.45rem .8rem;
  font-size:.77rem;color:#a78bfa;margin-top:.45rem;
}

/* ══ FLASHCARD ══════════════════════════════════════════════ */
.fc{
  background:linear-gradient(135deg,rgba(109,40,217,.1),rgba(139,92,246,.06));
  border:1px solid rgba(124,58,237,.25);
  border-radius:18px;padding:2rem;text-align:center;min-height:185px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin-bottom:.9rem;cursor:pointer;transition:all .25s;position:relative;overflow:hidden;
}
.fc::before{
  content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,#6d28d9,#8b5cf6,#6366f1,#38bdf8);
}
.fc:hover{border-color:rgba(124,58,237,.55);transform:translateY(-3px);
  box-shadow:0 14px 35px rgba(124,58,237,.18);}
.fc-lbl{font-size:.63rem;color:#8b5cf6;text-transform:uppercase;
  letter-spacing:.15em;margin-bottom:.65rem;font-weight:700;}
.fc-txt{font-size:1.05rem;font-weight:600;color:#e8eaf0;line-height:1.6;}
.fc-ar{font-family:'Amiri',serif;font-size:1rem;color:#a78bfa;direction:rtl;margin-top:.55rem;}

/* ══ SUMMARY ════════════════════════════════════════════════ */
.sum-s{
  background:#1a1b27;border:1px solid rgba(124,58,237,.1);
  border-left:3px solid #7c3aed;border-radius:12px;
  padding:1rem 1.1rem;margin-bottom:.65rem;
}
.sum-h{font-family:'Syne',sans-serif;font-size:.9rem;font-weight:700;color:#a78bfa;margin-bottom:.35rem;}
.sum-ar{font-family:'Amiri',serif;font-size:.93rem;color:#7c3aed;direction:rtl;text-align:right;margin-bottom:.3rem;}
.sum-txt{font-size:.83rem;color:#64748b;line-height:1.75;}
.kterm{
  display:inline-block;background:rgba(124,58,237,.12);
  border:1px solid rgba(124,58,237,.25);border-radius:6px;
  padding:3px 10px;font-size:.75rem;color:#a78bfa;margin:2px 3px;font-weight:500;
}

/* ══ AUDIO BUTTON ═══════════════════════════════════════════ */
.audio-btn{
  display:inline-flex;align-items:center;gap:7px;
  background:linear-gradient(135deg,#6d28d9,#8b5cf6);
  border:none;border-radius:25px;padding:.42rem 1.1rem;
  font-size:.77rem;font-weight:700;color:#fff;cursor:pointer;
  transition:all .22s;box-shadow:0 3px 14px rgba(124,58,237,.35);
  font-family:'DM Sans',sans-serif;
}
.audio-btn:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(124,58,237,.45);}

/* ══ EXAM ═══════════════════════════════════════════════════ */
.exam-sec{
  background:linear-gradient(90deg,rgba(124,58,237,.13),rgba(124,58,237,.04));
  border:1px solid rgba(124,58,237,.2);border-left:3px solid #8b5cf6;
  border-radius:8px;padding:.5rem .9rem;
  font-family:'Syne',sans-serif;font-size:.86rem;font-weight:700;
  color:#c4b5fd;margin:.75rem 0 .45rem;
}
.exam-q{padding:.42rem 0;border-bottom:1px solid rgba(255,255,255,.04);
  font-size:.86rem;color:#c8d0e0;line-height:1.56;}
.exam-qn{color:#8b5cf6;font-weight:700;margin-right:5px;}
.mktag{float:right;background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.2);
  border-radius:20px;padding:1px 7px;font-size:.69rem;color:#a78bfa;}
.ans-ln{border-bottom:1px dashed rgba(124,58,237,.2);height:23px;margin:.26rem 0;}

/* ══ QUIZ ═══════════════════════════════════════════════════ */
.quiz-q{background:#1a1b27;border:1px solid rgba(255,255,255,.05);
  border-radius:12px;padding:1rem 1.1rem;margin-bottom:.75rem;}
.score-card{
  background:linear-gradient(135deg,rgba(109,40,217,.17),rgba(99,102,241,.1));
  border:1px solid rgba(124,58,237,.3);border-radius:18px;
  padding:2rem;text-align:center;margin:1rem 0;
}
.score-num{
  font-family:'Syne',sans-serif;font-size:3.8rem;font-weight:800;
  background:linear-gradient(135deg,#8b5cf6,#38bdf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.score-label{font-size:.83rem;color:#64748b;margin-top:.3rem;}

/* ══ CHAT ═══════════════════════════════════════════════════ */
.qmsg{padding:.72rem .95rem;border-radius:10px;margin-bottom:.5rem;font-size:.86rem;line-height:1.63;}
.quser{background:rgba(109,40,217,.1);border:1px solid rgba(109,40,217,.2);color:#c4b5fd;text-align:right;}
.qai{background:#1a1b27;border:1px solid rgba(255,255,255,.05);color:#94a3b8;}
.qlbl{font-size:.63rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#8b5cf6;margin-bottom:.22rem;}

/* ══ PROGRESS ═══════════════════════════════════════════════ */
.pb{background:rgba(255,255,255,.05);border-radius:6px;height:3px;overflow:hidden;margin:.32rem 0;}
.pf{height:100%;border-radius:6px;
  background:linear-gradient(90deg,#6d28d9,#8b5cf6,#6366f1,#38bdf8);
  transition:width .3s ease;}

/* ══ MISC ═══════════════════════════════════════════════════ */
.sbox{background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.15);
  border-radius:10px;padding:.85rem 1rem;font-size:.78rem;color:#4b5280;line-height:1.68;}
.sbox b{color:#c4b5fd;}
div[data-testid="stExpander"]{
  background:#1a1b27!important;border:1px solid rgba(124,58,237,.12)!important;
  border-radius:11px!important;}
div[data-testid="stExpander"]:hover{border-color:rgba(124,58,237,.28)!important;}
.stSlider>div>div>div>div{background:#8b5cf6!important;}
.stRadio label,.stCheckbox label{font-size:.83rem!important;color:#94a3b8!important;}
::-webkit-scrollbar{width:4px;height:4px;}
::-webkit-scrollbar-track{background:#0f0f13;}
::-webkit-scrollbar-thumb{background:#6d28d9;border-radius:2px;}
</style>
""", unsafe_allow_html=True)


# THEMES defined below after PPTX builder

# Two static dicts — picked at runtime based on ar_only
SECTION_TYPES_EN = {
    "mcq":          "MCQ (Multiple Choice)",
    "true_false":   "True / False",
    "short_answer": "Short Answer",
    "long_answer":  "Long Answer / Essay",
    "calculation":  "Calculation",
    "fill_blank":   "Fill in the Blank",
    "matching":     "Matching",
    "case_study":   "Case Study",
}
SECTION_TYPES_AR = {
    "mcq":          "اختيار من متعدد",
    "true_false":   "صح أو خطأ",
    "short_answer": "إجابة قصيرة",
    "long_answer":  "إجابة مطولة",
    "calculation":  "حساب ومسائل",
    "fill_blank":   "أكمل الفراغ",
    "matching":     "مطابقة",
    "case_study":   "دراسة حالة",
}

# ── GEMINI — fast, single best model first ────────────────────
def call_gemini(api_key, prompt, pdf_b64=None, tokens=3500, json_mode=True):
    """Tries 5 models in order. Auto-retries on 404 and 429 rate limits."""
    MODELS = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite",
    ]
    parts = []
    if pdf_b64:
        parts.append({"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}})
    parts.append({"text": prompt})
    cfg = {"temperature": 0.1, "maxOutputTokens": tokens}
    if json_mode:
        cfg["responseMimeType"] = "application/json"
    last_err = ""
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            r = requests.post(
                url,
                json={"contents": [{"parts": parts}], "generationConfig": cfg},
                timeout=60
            )
        except requests.exceptions.Timeout:
            raise ValueError("⏱️ Request timed out. Try a shorter PDF or fewer questions.")
        except requests.exceptions.ConnectionError:
            raise ValueError("🌐 No internet connection.")
        if r.status_code == 200:
            try:
                return r.json()["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                raise ValueError("Unexpected API response format.")
        elif r.status_code == 404:
            last_err = f"Model {model} not found"
            continue
        elif r.status_code == 429:
            # Auto-retry on next model instead of crashing
            last_err = f"Rate limit on {model}"
            continue
        elif r.status_code == 403:
            raise ValueError("🔑 Invalid API key. Get your free key at aistudio.google.com/app/apikey")
        elif r.status_code == 400:
            raise ValueError("📄 PDF may be too large. Try a document under 5MB.")
        else:
            last_err = f"Error {r.status_code}"
            continue
    raise ValueError(
        f"All Gemini models are busy or unavailable. Last: {last_err}\n\n"
        f"✅ Try this:\n"
        f"• Wait 60 seconds and click Generate again\n"
        f"• Reduce number of slides/questions in sidebar\n"
        f"• The free tier allows 15 requests per minute"
    )

# ── JSON REPAIR ────────────────────────────────────────────────
def safe_parse(raw: str) -> dict:
    t = raw.strip()
    t = re.sub(r"^```(?:json)?", "", t).strip()
    t = re.sub(r"```$", "", t).strip()
    s = t.find("{"); e = t.rfind("}") + 1
    if s == -1: raise ValueError("No JSON found in AI response. Click Generate again.")
    c = t[s:e]
    # fix literal newlines in strings
    r2 = []; in_s = False; esc = False
    for ch in c:
        if esc: r2.append(ch); esc = False; continue
        if ch == "\\" and in_s: esc = True; r2.append(ch); continue
        if ch == '"': in_s = not in_s; r2.append(ch); continue
        if in_s and ch in "\n\r": r2.append(" "); continue
        r2.append(ch)
    c = "".join(r2)
    c = re.sub(r",\s*([\}\]])", r"\1", c)
    c = re.sub(r'(?<!\\)\\([^"\\/bfnrtu])', r' ', c)
    try: return json.loads(c)
    except:
        # close unclosed structures
        stk = []; in_s = False; esc = False
        for ch in c:
            if esc: esc = False; continue
            if ch == "\\" and in_s: esc = True; continue
            if ch == '"': in_s = not in_s; continue
            if not in_s:
                if ch in "{[": stk.append("}" if ch == "{" else "]")
                elif ch in "}]" and stk and stk[-1] == ch: stk.pop()
        c = c + "".join(reversed(stk))
        c = re.sub(r",\s*([\}\]])", r"\1", c)
        try: return json.loads(c)
        except: raise ValueError("Could not parse AI response. Click Generate again.")

# ==============================================================
# WORD DOCX BUILDER — zero external packages
# ==============================================================
def we(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_docx(body_xml: str) -> bytes:
    CT = "application/vnd.openxmlformats-officedocument"
    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="{CT}.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml"   ContentType="{CT}.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="{CT}.wordprocessingml.settings+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles"   Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""
    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr>
    <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Amiri"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/>
  </w:rPr></w:rPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="H1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="1D3461"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="H2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="200" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:color w:val="1E4D8C"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="AR">
    <w:name w:val="Arabic"/>
    <w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:after="80"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Amiri" w:hAnsi="Amiri" w:cs="Amiri"/>
    <w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="1E3A5F"/></w:rPr>
  </w:style>
</w:styles>"""
    settings = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:defaultTabStop w:val="720"/>
</w:settings>"""
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>{body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080"/>
    </w:sectPr>
  </w:body>
</w:document>"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/settings.xml", settings)
    buf.seek(0)
    return buf.read()

def wp(text, bold=False, italic=False, sz=24, color=None, align="left", after=120, indent=0, rtl=False, font=None):
    b = "<w:b/>" if bold else ""
    i = "<w:i/>" if italic else ""
    co = f'<w:color w:val="{color}"/>' if color else ""
    fn_tag = f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>' if font else ""
    rt = "<w:rtl/>" if rtl else ""
    bidi = "<w:bidi/>" if rtl else ""
    alg = {"left":"left","center":"center","right":"right","justify":"both"}.get(align,"left")
    ind_tag = f'<w:ind w:left="{indent}"/>' if indent else ""
    return (f'<w:p><w:pPr><w:jc w:val="{alg}"/><w:spacing w:after="{after}"/>{ind_tag}{bidi}</w:pPr>'
            f'<w:r><w:rPr>{b}{i}{co}{fn_tag}{rt}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
            f'<w:t xml:space="preserve">{we(text)}</w:t></w:r></w:p>')

def wp_ar(text, sz=24, color="1E3A5F", after=100):
    return (f'<w:p><w:pPr><w:bidi/><w:jc w:val="right"/><w:spacing w:after="{after}"/></w:pPr>'
            f'<w:r><w:rPr><w:rFonts w:ascii="Amiri" w:hAnsi="Amiri" w:cs="Amiri"/>'
            f'<w:rtl/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/><w:color w:val="{color}"/></w:rPr>'
            f'<w:t xml:space="preserve">{we(text)}</w:t></w:r></w:p>')

def wp_runs(runs, align="left", after=120, indent=0):
    alg = {"left":"left","center":"center","right":"right"}.get(align,"left")
    ind_tag = f'<w:ind w:left="{indent}"/>' if indent else ""
    xml = ""
    for r in runs:
        b = "<w:b/>" if r.get("b") else ""
        i = "<w:i/>" if r.get("i") else ""
        sz = r.get("sz", 22)
        rc2 = r.get("co","")
        co = f'<w:color w:val="{rc2}"/>' if rc2 else ""
        fn = r.get("fn","")
        fn_tag = f'<w:rFonts w:ascii="{fn}" w:hAnsi="{fn}" w:cs="{fn}"/>' if fn else ""
        rt = "<w:rtl/>" if r.get("rtl") else ""
        xml += (f'<w:r><w:rPr>{b}{i}{co}{fn_tag}{rt}'
                f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                f'<w:t xml:space="preserve">{we(r.get("t",""))}</w:t></w:r>')
    return f'<w:p><w:pPr><w:jc w:val="{alg}"/><w:spacing w:after="{after}"/>{ind_tag}</w:pPr>{xml}</w:p>'

def wempty(n=1):
    return '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>' * n

def whr(col="2563EB"):
    return (f'<w:p><w:pPr><w:pBdr>'
            f'<w:bottom w:val="single" w:sz="6" w:space="1" w:color="{col}"/>'
            f'</w:pBdr><w:spacing w:after="80"/></w:pPr></w:p>')

def wans(n=4):
    lines = ""
    for _ in range(n):
        lines += ('<w:p><w:pPr><w:spacing w:after="0"/>'
                  '<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="BBBBBB"/></w:pBdr>'
                  '</w:pPr></w:p>')
    return lines + wempty()

def wtable(h_en, h_ar, rows, cws=None):
    """Real Word table with blue header, alternating rows."""
    n = len(h_en)
    tw = 9360
    if not cws:
        cws = [tw // n] * n

    def cell_hdr(en, ar, cw):
        return (f'<w:tc><w:tcPr><w:tcW w:w="{cw}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="1D3461"/></w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
                f'<w:t>{we(en)}</w:t></w:r>'
                f'{"<w:r><w:rPr><w:rFonts w:ascii=\"Amiri\" w:hAnsi=\"Amiri\" w:cs=\"Amiri\"/><w:rtl/><w:color w:val=\"BAD0FF\"/><w:sz w:val=\"18\"/><w:szCs w:val=\"18\"/></w:rPr><w:t> | "+we(ar)+"</w:t></w:r>" if ar else ""}'
                f'</w:p></w:tc>')

    def cell_data(val, cw, fill):
        return (f'<w:tc><w:tcPr><w:tcW w:w="{cw}" w:type="dxa"/>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>'
                f'<w:r><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="1E293B"/></w:rPr>'
                f'<w:t xml:space="preserve">{we(str(val))}</w:t></w:r></w:p></w:tc>')

    hdr_cells = "".join(cell_hdr(h_en[i], h_ar[i] if i < len(h_ar) else "", cws[i] if i < len(cws) else cws[-1]) for i in range(n))
    body = ""
    for ri, row in enumerate(rows):
        fill = "EEF3FB" if ri % 2 == 0 else "F8FAFF"
        cells = "".join(cell_data(row[ci] if ci < len(row) else "", cws[ci] if ci < len(cws) else cws[-1], fill) for ci in range(n))
        body += f"<w:tr>{cells}</w:tr>"

    return (f'<w:tbl><w:tblPr>'
            f'<w:tblW w:w="{tw}" w:type="dxa"/>'
            f'<w:tblBorders>'
            f'<w:top    w:val="single" w:sz="6" w:color="2563EB"/>'
            f'<w:left   w:val="single" w:sz="6" w:color="2563EB"/>'
            f'<w:bottom w:val="single" w:sz="6" w:color="2563EB"/>'
            f'<w:right  w:val="single" w:sz="6" w:color="2563EB"/>'
            f'<w:insideH w:val="single" w:sz="4" w:color="BFDBFE"/>'
            f'<w:insideV w:val="single" w:sz="4" w:color="BFDBFE"/>'
            f'</w:tblBorders>'
            f'<w:tblCellMar><w:top w:w="80" w:type="dxa"/><w:left w:w="120" w:type="dxa"/>'
            f'<w:bottom w:w="80" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
            f'</w:tblPr>'
            f'<w:tr>{hdr_cells}</w:tr>{body}</w:tbl>{wempty()}')

def wcover(title_en, title_ar, meta):
    p = []
    p.append(f'<w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="12" w:space="1" w:color="1D3461"/></w:pBdr><w:spacing w:after="80"/></w:pPr></w:p>')
    p.append(wp(title_en, bold=True, sz=36, color="1D3461", align="center", after=60))
    if title_ar:
        p.append(wp_ar(title_ar, sz=30, color="1E4D8C", after=80))
    for en, ar in meta:
        p.append(wp_runs([{"t": en, "sz": 20, "b": True, "co": "1D3461"},
                          {"t": "  |  " + ar if ar else "", "sz": 20, "co": "374151", "fn": "Amiri", "rtl": bool(ar)}],
                         after=60))
    p.append(f'<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="12" w:space="1" w:color="1D3461"/></w:pBdr><w:spacing w:after="160"/></w:pPr></w:p>')
    return "".join(p)

# ── MCQ DOCX ──────────────────────────────────────────────────
def make_mcq_docx(data, show_ans, show_ar):
    p = []
    p.append(wcover("MCQ — " + data.get("subject",""), "أسئلة متعددة — " + data.get("subject_ar",""), []))
    for q in data.get("questions", []):
        p.append(wp_runs([
            {"t": f"Q{q.get('num','')}. ", "b": True, "sz": 24, "co": "1D3461"},
            {"t": q.get("question",""), "sz": 22},
            {"t": f"  [{q.get('difficulty','')}]", "sz": 18, "co": "888888", "i": True},
        ], after=60))
        if show_ar and q.get("question_ar"):
            p.append(wp_ar(q["question_ar"], sz=22, after=60))
        opts = q.get("options", {})
        if opts:
            rows = [[k, opts[k]] for k in sorted(opts.keys())]
            p.append(wtable(["Option", "Text"], ["الخيار", "النص"], rows, cws=[900, 8460]))
        if show_ans:
            corr = q.get("correct","")
            if corr:
                p.append(wp_runs([{"t":"✓ Answer: ","b":True,"sz":20,"co":"16A34A"},
                                   {"t":f"{corr} — {opts.get(corr,'')}","sz":20,"co":"16A34A"}], indent=360, after=40))
            if q.get("explanation"):
                p.append(wp(q["explanation"], italic=True, sz=20, color="374151", indent=360, after=60))
                if show_ar and q.get("explanation_ar"):
                    p.append(wp_ar(q["explanation_ar"], sz=20, after=60))
        p.append(wempty())
    return build_docx("".join(p))

# ── EXAM DOCX ─────────────────────────────────────────────────
def make_exam_docx(data, incl_ms, show_ar):
    p = []
    p.append(wcover(
        data.get("title","EXAMINATION"),
        data.get("title_ar","اختبار"),
        [
            (f"Institution: {data.get('institution','')}", data.get("institution_ar","")),
            (f"Course: {data.get('course','')}  |  Duration: {data.get('duration','')}  |  Total: {data.get('total_marks','')} marks",
             f"المادة: {data.get('course_ar','')}  |  المدة: {data.get('duration','')}  |  المجموع: {data.get('total_marks','')}"),
            (f"Lecturer: {data.get('lecturer','')}", data.get("lecturer_ar","")),
            (f"Date: {data.get('date','_______________')}", f"التاريخ: {data.get('date','_______________')}"),
            ("Student Name: ___________________________", "اسم الطالب: ___________________________"),
        ]
    ))
    p.append(wp("Instructions | التعليمات", bold=True, sz=26, color="1D3461", after=80))
    for inst in data.get("instructions", []):
        en = inst.get("en","") if isinstance(inst,dict) else str(inst)
        ar = inst.get("ar","") if isinstance(inst,dict) else ""
        p.append(wp_runs([{"t":"• ","b":True,"co":"2563EB","sz":22},
                           {"t":en,"sz":22},
                           {"t":"  |  "+ar if ar and show_ar else "","sz":20,"co":"374151","fn":"Amiri","rtl":bool(ar)}], after=50))
    p.append(wempty())

    for sec in data.get("sections", []):
        p.append(whr())
        name = sec.get("name",""); name_ar = sec.get("name_ar","")
        desc = sec.get("description",""); mks = sec.get("marks","")
        p.append(wp_runs([
            {"t": f"{name}  —  {desc}  ({mks} marks)", "b": True, "sz": 26, "co": "1D3461"},
        ], after=60))
        if show_ar and name_ar:
            p.append(wp_ar(f"{name_ar}  —  {sec.get('description_ar','')}  ({mks} درجة)", sz=22, after=80))
        ins = sec.get("instructions",""); ins_ar = sec.get("instructions_ar","")
        if ins:
            p.append(wp(ins + ("  |  " + ins_ar if ins_ar and show_ar else ""), italic=True, sz=20, color="555555", after=100))

        stype = sec.get("type","short_answer")

        # Matching — render as real table
        if stype == "matching" and sec.get("col_a") and sec.get("col_b"):
            rows = list(zip(
                [f"{i+1}. {v}" for i,v in enumerate(sec["col_a"])],
                [f"{chr(65+i)}. {v}" for i,v in enumerate(sec["col_b"])]
            ))
            p.append(wtable(["Column A | العمود أ","Column B | العمود ب"],["",""],rows,cws=[4680,4680]))

        for q in sec.get("questions", []):
            qn = q.get("num",""); qt = q.get("text",""); qar = q.get("text_ar",""); qmk = q.get("marks","")
            p.append(wp_runs([
                {"t": f"Q{qn}.  ", "b": True, "sz": 24, "co": "1D3461"},
                {"t": qt, "sz": 22},
                {"t": f"  [{qmk} marks]", "b": True, "sz": 20, "co": "2563EB", "i": True},
            ], after=60))
            if show_ar and qar:
                p.append(wp_ar(qar, sz=20, after=60))

            if stype == "mcq" and q.get("options"):
                rows = [[k, q["options"][k]] for k in sorted(q["options"].keys())]
                p.append(wtable(["","Option | الخيار"],["",""],rows,cws=[720,8640]))
            elif q.get("parts"):
                for pt in q["parts"]:
                    p.append(wp_runs([
                        {"t": f"  ({pt.get('part','')})  ", "b": True, "sz": 22, "co": "2563EB"},
                        {"t": pt.get("text",""), "sz": 22},
                        {"t": f"  [{pt.get('marks','')} marks]", "sz": 18, "co": "888888", "i": True},
                    ], indent=360, after=50))
                    if show_ar and pt.get("text_ar"):
                        p.append(wp_ar(pt["text_ar"], sz=20, after=50))
                    p.append(wans(pt.get("answer_lines", 3)))
            elif stype not in ("mcq", "matching"):
                p.append(wans(q.get("answer_lines", 4)))

        p.append(wempty())

    if incl_ms:
        p.append(wp("─"*80, sz=8, color="CCCCCC"))
        p.append(wempty())
        p.append(wcover("MARK SCHEME", "مخطط التصحيح", [(data.get("title",""),"")]))
        for sec in data.get("sections",[]):
            p.append(wp(sec.get("name",""), bold=True, sz=24, color="1D3461", after=80))
            for q in sec.get("questions",[]):
                p.append(wp_runs([
                    {"t":f"Q{q.get('num','')}  [{q.get('marks','')} marks]:  ","b":True,"sz":22,"co":"1D3461"},
                    {"t":q.get("model_answer",""),"sz":22},
                ], after=60))
                if show_ar and q.get("model_answer_ar"):
                    p.append(wp_ar(q["model_answer_ar"], sz=20, after=60))
                if q.get("correct"):
                    corr = q["correct"]; opts = q.get("options",{})
                    p.append(wp_runs([{"t":f"   ✓ {corr}: {opts.get(corr,'')}","b":True,"sz":20,"co":"16A34A"}], indent=360, after=40))
                if q.get("parts"):
                    for pt in q["parts"]:
                        p.append(wp_runs([
                            {"t":f"   ({pt.get('part','')}) ","b":True,"sz":20,"co":"2563EB"},
                            {"t":pt.get("model_answer",""),"sz":20},
                        ], indent=360, after=40))
                p.append(wempty())
    return build_docx("".join(p))

# ── SUMMARY DOCX ──────────────────────────────────────────────
def make_summary_docx(data, show_ar):
    p = []
    p.append(wcover(data.get("title","Summary"), data.get("title_ar","ملخص"),
                    [(data.get("subject",""), data.get("subject_ar",""))]))
    p.append(wp("Overview | نظرة عامة", bold=True, sz=26, color="1D3461", after=80))
    p.append(wp(data.get("overview",""), sz=22, after=80))
    if show_ar and data.get("overview_ar"):
        p.append(wp_ar(data["overview_ar"], sz=22, after=120))

    for sec in data.get("sections",[]):
        p.append(wp(sec.get("heading",""), bold=True, sz=26, color="1E4D8C", after=70))
        if show_ar and sec.get("heading_ar"):
            p.append(wp_ar(sec["heading_ar"], sz=24, color="2563EB", after=60))
        p.append(wp(sec.get("summary",""), sz=22, after=70))
        if show_ar and sec.get("summary_ar"):
            p.append(wp_ar(sec["summary_ar"], sz=20, after=80))
        kps = sec.get("key_points",[]); kps_ar = (sec.get("key_points_ar",[]) or []) + [""]*20
        for kp, kp_ar in zip(kps, kps_ar):
            line = f"▸  {kp}" + (f"  |  {kp_ar}" if kp_ar and show_ar else "")
            p.append(wp(line, sz=22, color="2563EB", after=40))
        p.append(wempty())

    if data.get("key_terms"):
        p.append(wp("Key Terms & Definitions | المصطلحات والتعريفات", bold=True, sz=26, color="1D3461", after=80))
        rows = [[kt.get("term",""), kt.get("term_ar",""), kt.get("definition",""), kt.get("definition_ar","")] for kt in data["key_terms"]]
        p.append(wtable(["Term","المصطلح","Definition","التعريف"],["","","",""],rows,cws=[1560,1560,3120,3120]))

    if data.get("formulas"):
        p.append(wempty())
        p.append(wp("Key Formulas | الصيغ الأساسية", bold=True, sz=26, color="1D3461", after=80))
        rows = [[f.get("name",""), f.get("name_ar",""), f.get("formula",""), f.get("meaning",""), f.get("meaning_ar","")] for f in data["formulas"]]
        p.append(wtable(["Name","الاسم","Formula / الصيغة","Meaning","المعنى"],["","","","",""],rows,cws=[1560,1560,2200,2200,1840]))

    if data.get("key_conclusions"):
        p.append(wempty())
        p.append(wp("Key Conclusions | الاستنتاجات", bold=True, sz=26, color="1D3461", after=80))
        concs_ar = (data.get("key_conclusions_ar",[]) or []) + [""]*20
        for c, c_ar in zip(data["key_conclusions"], concs_ar):
            line = f"✓  {c}" + (f"  |  {c_ar}" if c_ar and show_ar else "")
            p.append(wp(line, bold=True, sz=22, color="16A34A", after=50))
    return build_docx("".join(p))

# ==============================================================
# PPTX BUILDER — advanced professional design
# ==============================================================

# ==============================================================
# PPTX BUILDER — Premium design matching reference slides
# ==============================================================
def emu(i): return int(i * 914400)
def pt_(p): return int(p * 12700)
SW = emu(13.33); SH = emu(7.5)

def xe(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'","&apos;")

def is_ar(text):
    return any('\u0600' <= c <= '\u06FF' for c in str(text))

def smart_font(text, default="Calibri"):
    return "Amiri" if is_ar(text) else default

def smart_align(text, default="l"):
    return "r" if is_ar(text) else default

# ── Low-level XML primitives ──────────────────────────────────
def rect(n, x, y, w, h, fill, ln=None, lw=0):
    line = (f'<a:ln w="{pt_(lw)}"><a:solidFill><a:srgbClr val="{ln}"/></a:solidFill></a:ln>'
            if ln and lw > 0 else '<a:ln><a:noFill/></a:ln>')
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="1" name="{n}"/>'
            f'<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
            f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>{line}</p:spPr></p:sp>')

def para(text, sz, bold=False, italic=False, col="FFFFFF",
         alg=None, font=None, bul="", spc=0, rtl=None):
    text = str(text)
    a   = alg  if alg  is not None else smart_align(text)
    fn  = font if font is not None else smart_font(text)
    rt  = rtl  if rtl  is not None else is_ar(text)
    a2  = {"l":"l","c":"ctr","r":"r"}.get(a,"l")
    b   = ' b="1"' if bold   else ""
    i   = ' i="1"' if italic else ""
    bx  = f'<a:buChar char="{xe(bul)}"/>' if bul else "<a:buNone/>"
    sa  = f'<a:spcAft><a:spcPts val="{spc*100}"/></a:spcAft>' if spc else ""
    ra  = ' rtl="1"' if rt else ""
    lng = "ar-SA" if rt else "en-US"
    return (f'<a:p><a:pPr algn="{a2}" indent="0" marL="114300"{ra}>{bx}{sa}</a:pPr>'
            f'<a:r><a:rPr lang="{lng}" sz="{int(sz*100)}" dirty="0"{b}{i}>'
            f'<a:solidFill><a:srgbClr val="{col}"/></a:solidFill>'
            f'<a:latin typeface="{fn}"/></a:rPr>'
            f'<a:t>{xe(text)}</a:t></a:r></a:p>')

def txbox(n, x, y, w, h, paras, wrap="square"):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="{n}"/>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
            f'<a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="{wrap}" lIns="45720" rIns="45720" tIns="45720" bIns="45720"/>'
            f'<a:lstStyle/>{"".join(paras)}</p:txBody></p:sp>')

def slide_xml(shapes, bg="1A2744"):
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            f' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            f' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<p:cSld><p:bg><p:bgPr>'
            f'<a:solidFill><a:srgbClr val="{bg}"/></a:solidFill>'
            f'<a:effectLst/></p:bgPr></p:bg><p:spTree>'
            f'<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{SW}" cy="{SH}"/>'
            f'<a:chOff x="0" y="0"/><a:chExt cx="{SW}" cy="{SH}"/></a:xfrm></p:grpSpPr>'
            f'{"".join(shapes)}</p:spTree></p:cSld></p:sld>')

def footer_bar(T, slide_title="", lecturer="", institution=""):
    """Bottom footer bar like the reference slides."""
    footer_text = ""
    parts = [p for p in [slide_title, lecturer, institution] if p]
    if parts:
        footer_text = "  |  ".join(parts)
    return [
        rect("ftbg", 0, 7.18, 13.33, 0.32, T["footer_bg"]),
        txbox("ft", 0.3, 7.19, 12.73, 0.3,
              [para(footer_text, 9, col=T["footer_txt"], alg="c", italic=True)])
    ]

def slide_num(n, T):
    return txbox("pg", 12.6, 0.08, 0.55, 0.32,
                 [para(str(n), 11, col=T["gold"], alg="r", bold=True)])

# ── Themes matching the reference style ──────────────────────
THEMES = {
    "Academic Dark": {
        "bg":"1A2744","hdr_bg":"1A2744","hdr_line":"C8960C",
        "card_bg":"FFFFFF","card_border":"E8EDF5","card_left":"1A2744",
        "title_col":"FFFFFF","sub_col":"C8960C","body_col":"2D3748",
        "bullet_col":"E8EDF5","accent":"C8960C","gold":"C8960C",
        "formula_bg":"1A2744","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"1A2744","stat_lbl":"4A5568",
        "footer_bg":"0F1A2E","footer_txt":"8899BB",
        "tbl_hdr":"1A2744","tbl_even":"EEF2FF","tbl_odd":"F8FAFF",
    },
    "Forest Scholar": {
        "bg":"F5F5F0","hdr_bg":"1B3A2D","hdr_line":"C8960C",
        "card_bg":"FFFFFF","card_border":"D4E6D9","card_left":"1B3A2D",
        "title_col":"FFFFFF","sub_col":"C8960C","body_col":"2D3748",
        "bullet_col":"F0F5F0","accent":"C8960C","gold":"C8960C",
        "formula_bg":"1B3A2D","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"1B3A2D","stat_lbl":"4A5568",
        "footer_bg":"0F2218","footer_txt":"8AA89A",
        "tbl_hdr":"1B3A2D","tbl_even":"EEF5F0","tbl_odd":"F8FBF9",
    },
    "Royal Blue": {
        "bg":"EEF2FF","hdr_bg":"1E3A8A","hdr_line":"F59E0B",
        "card_bg":"FFFFFF","card_border":"BFDBFE","card_left":"1E3A8A",
        "title_col":"FFFFFF","sub_col":"FCD34D","body_col":"1E293B",
        "bullet_col":"DBEAFE","accent":"1E3A8A","gold":"F59E0B",
        "formula_bg":"1E3A8A","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"1E3A8A","stat_lbl":"4A5568",
        "footer_bg":"1E3A8A","footer_txt":"BFDBFE",
        "tbl_hdr":"1E3A8A","tbl_even":"EEF2FF","tbl_odd":"F8FAFF",
    },
    "Executive White": {
        "bg":"F7F8FA","hdr_bg":"1F2937","hdr_line":"6366F1",
        "card_bg":"FFFFFF","card_border":"E5E7EB","card_left":"1F2937",
        "title_col":"FFFFFF","sub_col":"A5B4FC","body_col":"1F2937",
        "bullet_col":"1F2937","accent":"6366F1","gold":"6366F1",
        "formula_bg":"1F2937","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"1F2937","stat_lbl":"6B7280",
        "footer_bg":"1F2937","footer_txt":"9CA3AF",
        "tbl_hdr":"1F2937","tbl_even":"F3F4F6","tbl_odd":"FFFFFF",
    },
    "Crimson Power": {
        "bg":"FFF5F5","hdr_bg":"7F1D1D","hdr_line":"F59E0B",
        "card_bg":"FFFFFF","card_border":"FECACA","card_left":"7F1D1D",
        "title_col":"FFFFFF","sub_col":"FCD34D","body_col":"1F2937",
        "bullet_col":"FEF2F2","accent":"7F1D1D","gold":"F59E0B",
        "formula_bg":"7F1D1D","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"7F1D1D","stat_lbl":"4A5568",
        "footer_bg":"7F1D1D","footer_txt":"FECACA",
        "tbl_hdr":"7F1D1D","tbl_even":"FFF5F5","tbl_odd":"FFFFFF",
    },
    "Purple Scholar": {
        "bg":"FAF5FF","hdr_bg":"4C1D95","hdr_line":"F59E0B",
        "card_bg":"FFFFFF","card_border":"E9D5FF","card_left":"4C1D95",
        "title_col":"FFFFFF","sub_col":"FCD34D","body_col":"1F2937",
        "bullet_col":"EDE9FE","accent":"4C1D95","gold":"F59E0B",
        "formula_bg":"4C1D95","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"4C1D95","stat_lbl":"4A5568",
        "footer_bg":"3B0764","footer_txt":"E9D5FF",
        "tbl_hdr":"4C1D95","tbl_even":"FAF5FF","tbl_odd":"FFFFFF",
    },
    "Teal Modern": {
        "bg":"F0FDFA","hdr_bg":"134E4A","hdr_line":"F59E0B",
        "card_bg":"FFFFFF","card_border":"99F6E4","card_left":"134E4A",
        "title_col":"FFFFFF","sub_col":"FCD34D","body_col":"1F2937",
        "bullet_col":"CCFBF1","accent":"0D9488","gold":"F59E0B",
        "formula_bg":"134E4A","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"134E4A","stat_lbl":"4A5568",
        "footer_bg":"0F3D3A","footer_txt":"99F6E4",
        "tbl_hdr":"134E4A","tbl_even":"F0FDFA","tbl_odd":"FFFFFF",
    },
    "Gold Prestige": {
        "bg":"FFFDF0","hdr_bg":"78350F","hdr_line":"C8960C",
        "card_bg":"FFFFFF","card_border":"FDE68A","card_left":"78350F",
        "title_col":"FFFFFF","sub_col":"FCD34D","body_col":"1F2937",
        "bullet_col":"FEF9C3","accent":"92400E","gold":"C8960C",
        "formula_bg":"78350F","formula_col":"FFFFFF",
        "stat_bg":"FFFFFF","stat_val":"78350F","stat_lbl":"4A5568",
        "footer_bg":"78350F","footer_txt":"FDE68A",
        "tbl_hdr":"78350F","tbl_even":"FFFDF0","tbl_odd":"FFFFFF",
    },
}

# ── Math cleaner ──────────────────────────────────────────────
def clean_math(text):
    """Convert LaTeX to clean Unicode for PowerPoint."""
    import re as _re
    t = str(text).replace('$','')
    subs = [
        (_re.compile(r'\\bar\{x\}'), 'x̄'), (_re.compile(r'\\bar\{X\}'), 'X̄'),
        (_re.compile(r'\\bar\{([^}]+)\}'), r'\1̄'),
        (_re.compile(r'\\frac\{([^}]+)\}\{([^}]+)\}'), r'(\1)/(\2)'),
        (_re.compile(r'\\sqrt\{([^}]+)\}'), r'√(\1)'),
        (_re.compile(r'\\sum'), 'Σ'), (_re.compile(r'\\Sigma'), 'Σ'),
        (_re.compile(r'\\alpha'), 'α'), (_re.compile(r'\\beta'), 'β'),
        (_re.compile(r'\\gamma'), 'γ'), (_re.compile(r'\\delta'), 'δ'),
        (_re.compile(r'\\mu'), 'μ'), (_re.compile(r'\\sigma'), 'σ'),
        (_re.compile(r'\\pi'), 'π'), (_re.compile(r'\\theta'), 'θ'),
        (_re.compile(r'\\times'), '×'), (_re.compile(r'\\div'), '÷'),
        (_re.compile(r'\\pm'), '±'), (_re.compile(r'\\neq'), '≠'),
        (_re.compile(r'\\leq'), '≤'), (_re.compile(r'\\geq'), '≥'),
        (_re.compile(r'\\approx'), '≈'), (_re.compile(r'\\infty'), '∞'),
        (_re.compile(r'\\cdot'), '·'), (_re.compile(r'\\rightarrow'), '→'),
        (_re.compile(r'\^\{([^}]+)\}'), r'^\1'),
        (_re.compile(r'_\{([^}]+)\}'),  r'_\1'),
        (_re.compile(r'x_i'), 'xᵢ'), (_re.compile(r'f_i'), 'fᵢ'),
        (_re.compile(r'd_i'), 'dᵢ'), (_re.compile(r'm_i'), 'mᵢ'),
        (_re.compile(r'\{([^}]*)\}'), r'\1'),
        (_re.compile(r'\\([a-zA-Z]+)'), r'\1'),
    ]
    for pat, rep in subs:
        try: t = pat.sub(rep, t)
        except: pass
    return t.replace('  ',' ').strip()

def clean_all(s_dict):
    r = dict(s_dict)
    for f in ('formula','where','theory','example','calculation','body','title','subtitle'):
        if r.get(f): r[f] = clean_math(r[f])
    if r.get('bullets'):     r['bullets']     = [clean_math(b) for b in r['bullets']]
    if r.get('left_points'): r['left_points']  = [clean_math(p) for p in r['left_points']]
    if r.get('right_points'):r['right_points'] = [clean_math(p) for p in r['right_points']]
    if r.get('headers'):     r['headers']      = [clean_math(h) for h in r['headers']]
    if r.get('rows'):
        r['rows'] = [[clean_math(c) for c in row] for row in r['rows']]
    if r.get('stats'):
        r['stats'] = [{k: clean_math(v) if isinstance(v,str) else v
                       for k,v in st2.items()} for st2 in r['stats']]
    return r

# ── Header component (matches reference design) ───────────────
def premium_header(title, T, subtitle="", slide_n=0, lecturer="", institution=""):
    """Dark full-width header with gold underline, like the reference."""
    ar = is_ar(title)
    ta = "r" if ar else "l"
    fn = smart_font(title, "Georgia") if not ar else "Amiri"
    title_sz = 28 if len(title) > 50 else (32 if len(title) > 35 else 36)
    shapes = [
        # Full dark header background
        rect("hbg", 0, 0, 13.33, 1.35 if subtitle else 1.1, T["hdr_bg"]),
        # Gold accent line below header
        rect("hln", 0, 1.35 if subtitle else 1.1, 13.33, 0.06, T["hdr_line"]),
        # Title text
        txbox("ht", 0.32, 0.06, 12.7, 1.0 if not subtitle else 0.75,
              [para(title, title_sz, bold=True, col=T["title_col"],
                    alg=ta, font=fn)]),
    ]
    if subtitle:
        shapes.append(txbox("hs", 0.32, 0.78, 12.7, 0.5,
                            [para(subtitle, 16, italic=True,
                                  col=T["sub_col"], alg=ta)]))
    if slide_n:
        shapes.append(slide_num(slide_n, T))
    shapes += footer_bar(T, lecturer=lecturer, institution=institution)
    return shapes

def white_card(n, x, y, w, h, T, left_accent=True):
    """White card with optional dark left accent stripe, like reference."""
    shapes = [rect(f"{n}bg", x, y, w, h, T["card_bg"],
                   T["card_border"], 0.5)]
    if left_accent:
        shapes.append(rect(f"{n}la", x, y, 0.07, h, T["card_left"]))
    return shapes

def native_table(headers, rows, T, x=0.25, y=1.48, w=12.83):
    """Native PPTX table with premium styling."""
    n   = len(headers)
    cw  = int(emu(w) / n)
    rh  = emu(0.44)

    def tc_h(h):
        ar = is_ar(h)
        return (f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>'
                f'<a:p><a:pPr algn="{"r" if ar else "ctr"}"/>'
                f'<a:r><a:rPr lang="{"ar-SA" if ar else "en-US"}" b="1" sz="1300" dirty="0">'
                f'<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
                f'<a:latin typeface="{"Amiri" if ar else "Calibri"}"/></a:rPr>'
                f'<a:t>{xe(str(h))}</a:t></a:r></a:p></a:txBody>'
                f'<a:tcPr><a:solidFill><a:srgbClr val="{T["tbl_hdr"]}"/></a:solidFill></a:tcPr></a:tc>')

    def tc_d(v, bg):
        ar = is_ar(v)
        return (f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>'
                f'<a:p><a:pPr algn="{"r" if ar else "ctr"}"/>'
                f'<a:r><a:rPr lang="{"ar-SA" if ar else "en-US"}" sz="1150" dirty="0">'
                f'<a:solidFill><a:srgbClr val="{T["body_col"]}"/></a:solidFill>'
                f'<a:latin typeface="{"Amiri" if ar else "Calibri"}"/></a:rPr>'
                f'<a:t>{xe(str(v))}</a:t></a:r></a:p></a:txBody>'
                f'<a:tcPr><a:solidFill><a:srgbClr val="{bg}"/></a:solidFill></a:tcPr></a:tc>')

    hrow  = "".join(tc_h(h) for h in headers)
    brows = ""
    for ri, row in enumerate(rows[:18]):
        bg    = T["tbl_even"] if ri%2==0 else T["tbl_odd"]
        cells = "".join(tc_d(row[ci] if ci<len(row) else "", bg) for ci in range(n))
        brows += f'<a:tr h="{rh}">{cells}</a:tr>'

    th = rh * (len(rows[:18]) + 1)
    tbl = (f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/>'
           f'<a:tblGrid>{"".join(f"<a:gridCol w=\"{cw}\"/>" for _ in range(n))}</a:tblGrid>'
           f'<a:tr h="{rh}">{hrow}</a:tr>{brows}</a:tbl>')
    return (f'<p:graphicFrame>'
            f'<p:nvGraphicFramePr><p:cNvPr id="10" name="tbl"/>'
            f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr>'
            f'<p:nvPr/></p:nvGraphicFramePr>'
            f'<p:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/>'
            f'<a:ext cx="{emu(w)}" cy="{th}"/></p:xfrm>'
            f'<a:graphic><a:graphicData '
            f'uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
            f'{tbl}</a:graphicData></a:graphic></p:graphicFrame>')

# ── Slide builders — premium design ──────────────────────────

def _meta(s):
    return {
        'lecturer':    s.get('_lecturer',''),
        'institution': s.get('_institution',''),
        'snum':        s.get('slide_num',''),
    }

def s_title(s, T):
    title    = str(s.get("title",""))
    subtitle = str(s.get("subtitle",""))
    body     = str(s.get("body",""))
    ar       = is_ar(title)
    ta       = "r" if ar else "l"
    m        = _meta(s)
    tsz      = 52 if len(title) < 25 else (40 if len(title) < 40 else 32)

    shapes = [
        # Left panel — dark
        rect("lp",  0,    0,    6.0,  7.5, T["hdr_bg"]),
        # Right panel — slightly lighter
        rect("rp",  6.0,  0,    7.33, 7.5, T["card_bg"]),
        # Gold accent horizontal line in left panel
        rect("gl",  0.32, 4.8,  3.5,  0.06, T["hdr_line"]),
        # Bottom gold bar
        rect("gb",  0,    7.18, 13.33,0.32, T["hdr_line"]),
        # Institution badge top-left
        txbox("ib", 0.32, 0.22, 4.5, 0.4,
              [para(m['institution'] or "Caawiye AI", 11,
                    col=T["sub_col"], bold=True)]),
        # Main title
        txbox("ti", 0.32, 1.1, 5.5, 3.4,
              [para(title, tsz, bold=True, col=T["title_col"],
                    alg=ta, font=smart_font(title,"Georgia"))]),
        # Subtitle
        txbox("su", 0.32, 4.95, 5.5, 0.8,
              [para(subtitle, 18, col=T["sub_col"], alg=ta,
                    font=smart_font(subtitle))]),
        # Lecturer / author bottom-left
        txbox("au", 0.32, 5.85, 5.5, 0.8,
              [para(m['lecturer'] or body, 14, bold=True,
                    col="FFFFFF", alg=ta)]),
        # Date / details
        txbox("dt", 0.32, 6.55, 5.5, 0.5,
              [para(body if m['lecturer'] else "", 12,
                    col=T["sub_col"], alg=ta, italic=True)]),
        # Right panel — big decorative icon
        txbox("ic", 6.5, 1.5, 6.2, 4.0,
              [para("📖", 140, alg="c")]),
        # Right panel footer text
        txbox("rf", 6.2, 6.6, 6.8, 0.5,
              [para("Caawiye AI", 11,
                    col=T["card_left"], alg="c", italic=True)]),
    ]
    return slide_xml(shapes, T["hdr_bg"])

def s_section(s, T):
    """Section divider slide — like 'PART ONE' in reference."""
    title    = str(s.get("title",""))
    subtitle = str(s.get("subtitle",""))
    body     = str(s.get("body",""))
    ar       = is_ar(title)
    m        = _meta(s)
    shapes = [
        rect("bg",  0,    0, 13.33, 7.5,  T["hdr_bg"]),
        rect("gl",  0.32, 5.1, 2.5,  0.06, T["hdr_line"]),
        rect("gb",  0,    7.18,13.33,0.32, T["hdr_line"]),
        txbox("lb", 0.32, 0.5, 12.0, 0.55,
              [para(body or "PART", 14, col=T["sub_col"], bold=True,
                    alg="r" if ar else "l")]),
        txbox("ti", 0.32, 1.1, 12.0, 3.8,
              [para(title, 54, bold=True, col=T["title_col"],
                    alg="r" if ar else "l",
                    font=smart_font(title,"Georgia"))]),
        txbox("su", 0.32, 5.2, 12.0, 1.6,
              [para(subtitle, 20, col=T["sub_col"],
                    italic=True, alg="r" if ar else "l")]),
    ]
    shapes += footer_bar(T, lecturer=m['lecturer'], institution=m['institution'])
    return slide_xml(shapes, T["hdr_bg"])

def s_bullets(s, T):
    title   = str(s.get("title",""))
    bullets = s.get("bullets") or []
    m       = _meta(s)
    ar      = is_ar(title)
    shapes  = premium_header(title, T, slide_n=m['snum'],
                             lecturer=m['lecturer'],
                             institution=m['institution'])
    y_start = 1.5
    n_b     = min(len(bullets), 5)
    gap     = min(1.05, (5.65 / max(n_b, 1)))
    for i, b in enumerate(bullets[:5]):
        b    = str(b)
        b_ar = is_ar(b)
        # Alternate subtle tint on cards for visual rhythm
        fill = T["card_bg"] if i % 2 == 0 else T.get("tbl_odd", T["card_bg"])
        shapes.append(rect(f"bc{i}", 0.25, y_start + i*gap, 12.83, gap-0.08,
                           fill, T["hdr_line"], 0.4))
        # Left accent stripe gets thicker gold line
        shapes.append(rect(f"bl{i}", 0.25, y_start + i*gap, 0.1, gap-0.08, T["hdr_line"]))
        # Text — use body_col for readability on white/light card
        txt_col = T["body_col"]
        shapes.append(txbox(f"bt{i}", 0.52, y_start + i*gap + 0.06,
                            12.1, gap-0.16,
                            [para(b, 17, col=txt_col,
                                  bold=False, font=smart_font(b))]))
    return slide_xml(shapes, T["bg"])

def s_lecture(s, T):
    title    = str(s.get("title",""))
    theory   = str(s.get("theory",""))
    formula  = str(s.get("formula",""))
    where    = str(s.get("where",""))
    example  = str(s.get("example",""))
    calc     = str(s.get("calculation",""))
    m        = _meta(s)
    ar       = is_ar(title or theory)

    shapes   = premium_header(title, T, slide_n=m['snum'],
                              lecturer=m['lecturer'],
                              institution=m['institution'])

    # Left column — theory + formula
    lx, ly, lw = 0.25, 1.5, 6.2
    shapes += white_card("lc", lx, ly, lw, 5.55, T, left_accent=True)

    ps = []
    if theory:
        lbl = "النظرية" if ar else "Theory"
        ps.append(para(lbl, 12, bold=True, col=T["card_left"],
                       alg="r" if ar else "l"))
        ps.append(para(theory, 14, col=T["body_col"],
                       font=smart_font(theory), spc=4))
        ps.append(para("", 6, col="FFFFFF"))
    if formula:
        lbl = "الصيغة" if ar else "Formula"
        ps.append(para(lbl, 12, bold=True, col=T["card_left"],
                       alg="r" if ar else "l"))
        ps.append(para(formula, 17, bold=True, col=T["hdr_bg"],
                       font="Courier New", alg="c", spc=2))
        if where:
            for part in where.replace(";",",").split(","):
                pt = part.strip()
                if len(pt) > 2:
                    ps.append(para(pt, 13, col=T["stat_lbl"],
                                   bul="•", font=smart_font(pt)))
        ps.append(para("", 6, col="FFFFFF"))
    shapes.append(txbox("lct", lx+0.15, ly+0.1, lw-0.25, 5.3, ps))

    # Right column — example + calculation
    rx, ry, rw = 6.6, 1.5, 6.48
    shapes += white_card("rc", rx, ry, rw, 5.55, T, left_accent=True)

    ps2 = []
    if example:
        lbl = "مثال رقمي" if ar else "Worked Example"
        ps2.append(para(lbl, 12, bold=True, col=T["card_left"],
                        alg="r" if ar else "l"))
        ps2.append(para(example, 14, col=T["body_col"],
                        font=smart_font(example), spc=4))
        ps2.append(para("", 6, col="FFFFFF"))
    if calc:
        lbl = "خطوات الحل" if ar else "Solution"
        ps2.append(para(lbl, 12, bold=True, col=T["card_left"],
                        alg="r" if ar else "l"))
        for step in calc.replace("\\n","\n").split("\n"):
            step = step.strip()
            if step:
                ps2.append(para(step, 15, col=T["hdr_bg"],
                                font="Courier New", bul="→", spc=3))
    shapes.append(txbox("rct", rx+0.15, ry+0.1, rw-0.25, 5.3, ps2))
    return slide_xml(shapes, T["bg"])

def s_formula(s, T):
    title   = str(s.get("title",""))
    formula = str(s.get("formula",""))
    where   = str(s.get("where",""))
    example = str(s.get("example",""))
    calc    = str(s.get("calculation",""))
    m       = _meta(s)
    ar      = is_ar(title or formula)

    shapes  = premium_header(title, T, slide_n=m['snum'],
                             lecturer=m['lecturer'],
                             institution=m['institution'])

    # Big formula box — full width, dark background
    shapes.append(rect("fb", 0.25, 1.5, 12.83, 1.6, T["formula_bg"],
                        T["hdr_line"], 1.5))
    fsz = 34 if len(formula) < 30 else (26 if len(formula) < 50 else 20)
    shapes.append(txbox("fml", 0.4, 1.55, 12.5, 1.5,
                        [para(formula, fsz, bold=True,
                              col=T["formula_col"],
                              font="Courier New", alg="c")]))

    # Where + Example left | Calculation right
    lx, ry2 = 0.25, 3.25
    shapes += white_card("wc", lx, ry2, 6.2, 3.8, T, True)
    ps = []
    if where:
        lbl = "تعريف المتغيرات" if ar else "Where:"
        ps.append(para(lbl, 13, bold=True, col=T["card_left"],
                       alg="r" if ar else "l"))
        for part in where.replace(";",",").split(","):
            pt = part.strip()
            if len(pt) > 2:
                ps.append(para(pt, 14, col=T["body_col"],
                               bul="▪", font=smart_font(pt), spc=3))
        ps.append(para("", 6, col="FFFFFF"))
    if example:
        lbl = "مثال" if ar else "Example:"
        ps.append(para(lbl, 13, bold=True, col=T["card_left"],
                       alg="r" if ar else "l"))
        ps.append(para(example, 14, col=T["body_col"],
                       font=smart_font(example)))
    shapes.append(txbox("wct", lx+0.15, ry2+0.1, 5.9, 3.6, ps))

    rx2 = 6.6
    shapes += white_card("sc", rx2, ry2, 6.48, 3.8, T, True)
    ps2 = []
    if calc:
        lbl = "خطوات الحل" if ar else "Step-by-Step Solution:"
        ps2.append(para(lbl, 13, bold=True, col=T["card_left"],
                        alg="r" if ar else "l"))
        for i, step in enumerate(calc.replace("\\n","\n").split("\n")):
            step = step.strip()
            if step:
                ps2.append(para(step, 16, bold=(i==len(calc.split("\\n"))-1),
                                col=T["hdr_bg"], font="Courier New",
                                bul="→", spc=4))
    shapes.append(txbox("sct", rx2+0.15, ry2+0.1, 6.18, 3.6, ps2))
    return slide_xml(shapes, T["bg"])

def s_two_col(s, T):
    title   = str(s.get("title",""))
    ltitle  = str(s.get("left_title",""))
    rtitle  = str(s.get("right_title",""))
    lpts    = s.get("left_points") or []
    rpts    = s.get("right_points") or []
    m       = _meta(s)
    ar      = is_ar(title)

    shapes  = premium_header(title, T, slide_n=m['snum'],
                             lecturer=m['lecturer'],
                             institution=m['institution'])

    for side, (sx, st_, pts) in enumerate([(0.25, ltitle, lpts),
                                            (6.88, rtitle, rpts)]):
        w = 6.2
        shapes.append(rect(f"ch{side}", sx, 1.5, w, 0.52, T["hdr_bg"]))
        shapes.append(rect(f"cl{side}", sx, 1.5, 0.07, 0.52, T["hdr_line"]))
        sar = is_ar(st_)
        shapes.append(txbox(f"ct{side}", sx+0.12, 1.52, w-0.18, 0.46,
                            [para(st_, 15, bold=True, col="FFFFFF",
                                  alg="r" if sar else "c",
                                  font=smart_font(st_))]))
        shapes += white_card(f"cc{side}", sx, 2.1, w, 4.95, T, True)
        ps = []
        for pt in pts[:6]:
            pt = str(pt)
            bul = "◆" if is_ar(pt) else "▶"
            ps.append(para(pt, 15, col=T["bullet_col"],
                           bul=bul, font=smart_font(pt), spc=5))
        shapes.append(txbox(f"cb{side}", sx+0.2, 2.2, w-0.3, 4.75, ps))
    return slide_xml(shapes, T["bg"])

def s_stat(s, T):
    title = str(s.get("title",""))
    stats = s.get("stats") or []
    body  = str(s.get("body",""))
    m     = _meta(s)

    shapes = premium_header(title, T, slide_n=m['snum'],
                            lecturer=m['lecturer'],
                            institution=m['institution'])

    xs = [0.25, 4.55, 8.86]
    ww = 4.05
    for i, si in enumerate(stats[:3]):
        xp  = xs[i]
        val = str(si.get("value",""))
        lbl = str(si.get("label",""))
        src = str(si.get("note",""))
        ar  = is_ar(lbl)
        # White card
        shapes += white_card(f"sc{i}", xp, 1.5, ww, 5.1, T, False)
        # Top colored accent
        shapes.append(rect(f"sa{i}", xp, 1.5, ww, 0.1, T["hdr_line"]))
        # Big value
        vsz = 64 if len(val) < 6 else (48 if len(val) < 10 else 36)
        shapes.append(txbox(f"sv{i}", xp+0.1, 1.75, ww-0.2, 2.2,
                            [para(val, vsz, bold=True,
                                  col=T["stat_val"], alg="c",
                                  font="Georgia")]))
        # Label
        shapes.append(txbox(f"sl{i}", xp+0.1, 3.95, ww-0.2, 1.3,
                            [para(lbl, 15, col=T["stat_lbl"],
                                  alg="r" if ar else "c",
                                  font=smart_font(lbl))]))
        # Source note
        if src:
            shapes.append(txbox(f"sn{i}", xp+0.1, 5.2, ww-0.2, 0.3,
                                [para(src, 10, italic=True,
                                      col=T["footer_txt"], alg="c")]))
    if body:
        shapes.append(txbox("bd", 0.32, 6.55, 12.7, 0.55,
                            [para(body, 12, italic=True,
                                  col=T["footer_txt"], alg="c")]))
    return slide_xml(shapes, T["bg"])

def s_table(s, T):
    title   = str(s.get("title",""))
    headers = s.get("headers") or []
    rows    = s.get("rows") or []
    m       = _meta(s)

    shapes  = premium_header(title, T, slide_n=m['snum'],
                             lecturer=m['lecturer'],
                             institution=m['institution'])
    if headers and rows:
        shapes.append(native_table(headers, rows, T,
                                   x=0.25, y=1.5, w=12.83))
    else:
        shapes.append(txbox("nb", 0.32, 2.2, 12.7, 1.0,
                            [para("No table data.", 16,
                                  col=T["body_col"])]))
    return slide_xml(shapes, T["bg"])

def s_quote(s, T):
    title = str(s.get("title",""))
    body  = str(s.get("body",""))
    src   = str(s.get("source",""))
    m     = _meta(s)
    ar    = is_ar(body)

    shapes = premium_header(title, T, slide_n=m['snum'],
                            lecturer=m['lecturer'],
                            institution=m['institution'])
    # Quote mark
    shapes.append(txbox("qm", 0.32, 1.5, 1.5, 2.0,
                        [para('"', 120, bold=True,
                              col=T["hdr_line"], alg="l",
                              font="Georgia")]))
    # Quote text card
    shapes += white_card("qc", 0.25, 1.5, 12.83, 4.5, T, True)
    qsz = 22 if len(body) < 150 else (18 if len(body) < 250 else 15)
    shapes.append(txbox("qt", 1.6, 1.7, 11.3, 3.8,
                        [para(body, qsz, italic=True,
                              col=T["body_col"],
                              font=smart_font(body,"Georgia"),
                              alg="r" if ar else "l")]))
    if src:
        shapes.append(txbox("qs", 0.32, 6.15, 12.7, 0.85,
                            [para("— " + src, 13,
                                  col=T["stat_lbl"],
                                  alg="r" if ar else "l",
                                  italic=True)]))
    return slide_xml(shapes, T["bg"])

def s_conclusion(s, T):
    title   = str(s.get("title","Key Takeaways"))
    bullets = s.get("bullets") or []
    m       = _meta(s)
    ar      = is_ar(title)

    shapes  = [
        rect("bg",  0, 0, 13.33, 7.5,  T["hdr_bg"]),
        rect("hln", 0, 1.1, 13.33, 0.06, T["hdr_line"]),
        txbox("ti", 0.32, 0.1, 12.7, 0.92,
              [para(title, 34, bold=True, col=T["title_col"],
                    alg="r" if ar else "l",
                    font=smart_font(title,"Georgia"))]),
        rect("gb",  0, 7.18, 13.33, 0.32, T["hdr_line"]),
    ]
    if m['snum']:
        shapes.append(slide_num(m['snum'], T))
    shapes += footer_bar(T, lecturer=m['lecturer'],
                         institution=m['institution'])

    # Two columns of bullets as white cards
    mid   = max(1, len(bullets)//2)
    left  = bullets[:mid]
    right = bullets[mid:]
    for si, pts in enumerate([left, right]):
        sx = 0.25 if si==0 else 6.88
        shapes += white_card(f"ck{si}", sx, 1.22, 6.2, 5.75, T, True)
        ps = []
        for b in pts:
            b  = str(b)
            ps.append(para(b, 16, col=T["bullet_col"],
                           bul="✓", font=smart_font(b), spc=8))
        shapes.append(txbox(f"cb{si}", sx+0.2, 1.32, 5.9, 5.55, ps))
    return slide_xml(shapes, T["hdr_bg"])

def build_slide(s, T):
    s = clean_all(s)
    if "ac2" not in T: T = dict(T)
    t = s.get("type","bullets")
    if   t == "title":        return s_title(s, T)
    elif t == "section":      return s_section(s, T)
    elif t == "lecture":      return s_lecture(s, T)
    elif t == "formula":      return s_formula(s, T)
    elif t == "two_col":      return s_two_col(s, T)
    elif t == "stat_callout": return s_stat(s, T)
    elif t == "table":        return s_table(s, T)
    elif t == "quote":        return s_quote(s, T)
    elif t == "conclusion":   return s_conclusion(s, T)
    else:                     return s_bullets(s, T)

def assemble_pptx(xmls):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        n    = len(xmls)
        ct_s = "".join(
            f'<Override PartName="/ppt/slides/slide{i+1}.xml" '
            f'ContentType="application/vnd.openxmlformats-officedocument.'
            f'presentationml.slide+xml"/>' for i in range(n))
        z.writestr("[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
            '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
            '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
            f'{ct_s}</Types>')
        z.writestr("_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
            '</Relationships>')
        z.writestr("docProps/app.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
            '<Application>Caawiye AI</Application></Properties>')
        z.writestr("ppt/theme/theme1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Kaabe">'
            '<a:themeElements><a:clrScheme name="Kaabe">'
            '<a:dk1><a:sysClr lastClr="000000" val="windowText"/></a:dk1>'
            '<a:lt1><a:sysClr lastClr="FFFFFF" val="window"/></a:lt1>'
            '<a:dk2><a:srgbClr val="1A2744"/></a:dk2>'
            '<a:lt2><a:srgbClr val="F5F7FA"/></a:lt2>'
            '<a:accent1><a:srgbClr val="C8960C"/></a:accent1>'
            '<a:accent2><a:srgbClr val="1B3A2D"/></a:accent2>'
            '<a:accent3><a:srgbClr val="1E3A8A"/></a:accent3>'
            '<a:accent4><a:srgbClr val="7C3AED"/></a:accent4>'
            '<a:accent5><a:srgbClr val="DC2626"/></a:accent5>'
            '<a:accent6><a:srgbClr val="0D9488"/></a:accent6>'
            '<a:hlink><a:srgbClr val="1E3A8A"/></a:hlink>'
            '<a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>'
            '</a:clrScheme>'
            '<a:fontScheme name="Kaabe">'
            '<a:majorFont><a:latin typeface="Georgia"/><a:ea typeface="Amiri"/><a:cs typeface="Amiri"/></a:majorFont>'
            '<a:minorFont><a:latin typeface="Calibri"/><a:ea typeface="Amiri"/><a:cs typeface="Amiri"/></a:minorFont>'
            '</a:fontScheme>'
            '<a:fmtScheme name="Kaabe">'
            '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
            '<a:lnStyleLst>'
            '<a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
            '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
            '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
            '</a:lnStyleLst>'
            '<a:effectStyleLst>'
            '<a:effectStyle><a:effectLst/></a:effectStyle>'
            '<a:effectStyle><a:effectLst/></a:effectStyle>'
            '<a:effectStyle><a:effectLst/></a:effectStyle>'
            '</a:effectStyleLst>'
            '<a:bgFillStyleLst>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '</a:bgFillStyleLst>'
            '</a:fmtScheme></a:themeElements></a:theme>')
        z.writestr("ppt/slideMasters/slideMaster1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg>'
            '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            '</p:spTree></p:cSld>'
            '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1"'
            ' accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5"'
            ' accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
            '<p:txStyles><p:titleStyle><a:lstStyle/></p:titleStyle>'
            '<p:bodyStyle><a:lstStyle/></p:bodyStyle>'
            '<p:otherStyle><a:lstStyle/></p:otherStyle></p:txStyles>'
            '</p:sldMaster>')
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
            '</Relationships>')
        z.writestr("ppt/slideLayouts/slideLayout1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            ' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" type="blank">'
            '<p:cSld name="Blank"><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            '</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
            '</Relationships>')
        ids = "\n".join(f'<p:sldId id="{256+i}" r:id="rId{i+3}"/>' for i in range(n))
        prs_rels = "\n".join(
            f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>'
            for i in range(n))
        for i, xml in enumerate(xmls):
            z.writestr(f"ppt/slides/slide{i+1}.xml", xml)
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
                '</Relationships>')
        z.writestr("ppt/presentation.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
            f' xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
            f' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
            f' saveSubsetFonts="1">'
            f'<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
            f'<p:sldIdLst>{ids}</p:sldIdLst>'
            f'<p:sldSz cx="{SW}" cy="{SH}" type="custom"/>'
            f'<p:notesSz cx="{emu(7.5)}" cy="{emu(10)}"/>'
            f'</p:presentation>')
        z.writestr("ppt/_rels/presentation.xml.rels",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
            f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
            f'{prs_rels}</Relationships>')
    buf.seek(0)
    return buf.read()



# ─────────────────────────────────────────────────────────────
# AUDIO HELPER
# ─────────────────────────────────────────────────────────────
def make_audio_btn(text, ar_only=False, label_en="Listen", label_ar="استمع"):
    label     = label_ar if ar_only else label_en
    stop_lbl  = "إيقاف" if ar_only else "Stop"
    lang_code = "ar-SA" if ar_only else "en-US"
    safe = text[:2200].replace("\\","").replace('"',' ').replace("'"," ").replace("\n"," ").replace("\r","")
    uid = str(random.randint(10000,99999))
    return f'''<button class="audio-btn" id="abtn{uid}" onclick="
    var btn=document.getElementById('abtn{uid}');
    if(window._caw_sp){{window.speechSynthesis.cancel();window._caw_sp=false;btn.innerHTML='🔊 {label}';return;}}
    var u=new SpeechSynthesisUtterance(\\"{safe}\\");
    u.lang='{lang_code}';u.rate=0.88;u.pitch=1.0;
    window._caw_sp=true;
    u.onend=function(){{window._caw_sp=false;btn.innerHTML='🔊 {label}';}};
    u.onerror=function(){{window._caw_sp=false;btn.innerHTML='🔊 {label}';}};
    btn.innerHTML='⏹ {stop_lbl}';
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
    ">🔊 {label}</button>'''

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
for k, v in {
    "tool":"slides","pdf_b64":None,"filename":"","pdf_kb":0,
    "chat":[],"fc_idx":0,"fc_show":False,
    "mcq_data":None,"sum_data":None,"exam_data":None,
    "fc_data":None,"quiz_data":None,
    "quiz_answers":{},"quiz_submitted":False,
    "lang":"en",  # "en" or "ar"
    "exam_sections":[
        {"name":"Section A","name_ar":"القسم أ","type":"mcq",         "marks":20,"num_q":10,"desc":"","desc_ar":"","answer_req":0},
        {"name":"Section B","name_ar":"القسم ب","type":"short_answer","marks":30,"num_q":5, "desc":"","desc_ar":"","answer_req":0},
        {"name":"Section C","name_ar":"القسم ج","type":"long_answer", "marks":30,"num_q":3, "desc":"","desc_ar":"","answer_req":0},
    ]
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

ar_only  = st.session_state.lang == "ar"
show_ar  = ar_only

# ─────────────────────────────────────────────────────────────
# TOP NAVIGATION BAR
# ─────────────────────────────────────────────────────────────
TOOLS_NAV = [
    ("slides",     "📊", "Slides",     "شرائح"),
    ("mcq",        "❓", "MCQ",        "أسئلة"),
    ("exam",       "📝", "Exam",       "اختبار"),
    ("summary",    "📋", "Summary",    "ملخص"),
    ("flashcards", "🃏", "Flashcards", "بطاقات"),
    ("quiz",       "🎯", "Quiz",       "اختبرني"),
    ("qa",         "💬", "AI Tutor",   "معلم"),
]

fn       = st.session_state.filename
pdf_ok   = bool(st.session_state.pdf_b64)
fn_short = (fn[:22]+"…") if len(fn)>24 else fn

# Render nav as HTML + Streamlit buttons side by side
nav_pills_html = "".join(
    f'<span class="nav-pill{" active" if st.session_state.tool==tid else ""}" '
    f'onclick="(function(){{}})()">{ico} {(ar_l if ar_only else en_l)}</span>'
    for tid,ico,en_l,ar_l in TOOLS_NAV
)
pdf_class = "nav-pdf-slot has-file" if pdf_ok else "nav-pdf-slot"
pdf_label = f"📄 {fn_short}" if pdf_ok else ("📎 ارفع ملف PDF" if ar_only else "📎 Drop PDF here")
lang_en_a = "active" if not ar_only else ""
lang_ar_a = "active" if ar_only else ""

st.markdown(f"""
<div class="top-nav">
  <div class="nav-logo">
    <div class="nav-logo-icon">&#129302;</div>
    <div>
      <div class="nav-logo-text">Caawiye AI</div>
      <div class="nav-logo-sub">{"كوييه — منصة الذكاء الاصطناعي" if ar_only else "Academic AI Platform"}</div>
    </div>
  </div>
  <div class="{pdf_class}" onclick="">{pdf_label}</div>
  <div class="nav-right">
    <div class="nav-badge"><span class="dot"></span>{"جاهز" if ar_only else "Live"}</div>
    <div class="lang-toggle">
      <div class="lang-opt {lang_en_a}">EN</div>
      <div class="lang-opt {lang_ar_a}">AR</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Streamlit language toggle (functional)
_lc1, _lc2, _lc3, _lc4, _lc5, _lc6 = st.columns([1,1,6,1,1,1])
with _lc1:
    if st.button("🇬🇧 EN", key="lang_en", type="primary" if not ar_only else "secondary", use_container_width=True):
        st.session_state.lang = "en"; st.rerun()
with _lc2:
    if st.button("🇸🇦 AR", key="lang_ar", type="primary" if ar_only else "secondary", use_container_width=True):
        st.session_state.lang = "ar"; st.rerun()

# Streamlit tool nav
_tcols = st.columns(len(TOOLS_NAV))
for i,(tid,ico,en_l,ar_l) in enumerate(TOOLS_NAV):
    with _tcols[i]:
        lbl = f"{ico} {ar_l if ar_only else en_l}"
        is_active = st.session_state.tool == tid
        if st.button(lbl, key=f"tnav_{tid}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.tool = tid; st.rerun()

st.markdown('<div style="height:.5rem"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# THREE-PANEL LAYOUT
# ─────────────────────────────────────────────────────────────
left_col, center_col, right_col = st.columns([1, 2.8, 1.1])

#                                                               
# LEFT PANEL — Sources & Settings
#                                                               
with left_col:
    st.markdown(f'<div class="panel-section-title">{"المصادر" if ar_only else "Sources"}</div>', unsafe_allow_html=True)

    # Upload
    uploaded = st.file_uploader(
        "PDF" if not ar_only else "ملف PDF",
        type=["pdf"], label_visibility="collapsed")
    if uploaded:
        b64 = base64.standard_b64encode(uploaded.getvalue()).decode()
        st.session_state.pdf_b64  = b64
        st.session_state.filename = uploaded.name
        st.session_state.pdf_kb   = len(uploaded.getvalue()) // 1024

    if st.session_state.pdf_b64:
        kb = st.session_state.pdf_kb
        st.markdown(f"""
<div class="source-card active">
  <div class="source-name">&#128196; {st.session_state.filename}</div>
  <div class="source-meta">{kb} KB &middot; PDF</div>
  <div class="source-actions">
    <span class="src-btn">✓ {"محمل" if ar_only else "Loaded"}</span>
    <span class="src-btn">&#128269; {"جاهز" if ar_only else "Ready"}</span>
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="upload-zone">
  <div class="upload-icon">&#128193;</div>
  <div class="upload-text">
    <b>{"ارفع ملف PDF" if ar_only else "Upload a PDF"}</b><br>
    {"اسحب وأفلت هنا" if ar_only else "Drag & drop or click above"}
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-section-title">{"إعدادات" if ar_only else "Settings"}</div>', unsafe_allow_html=True)

    # API Key
    api_key = st.text_input(
        "🔑 " + ("مفتاح API" if ar_only else "Gemini API Key"),
        type="password",
        placeholder="AIzaSy..." if not ar_only else "الصق المفتاح هنا...",
        help="Free at aistudio.google.com/app/apikey")
    if api_key:
        st.markdown(f'<div style="font-size:.7rem;color:#10b981;margin-top:-4px">✓ {"نشط" if ar_only else "Key active"}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-size:.7rem;margin-top:-4px"><a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#8b5cf6;text-decoration:none">{"← احصل على مفتاح مجاني" if ar_only else "Get free key →"}</a></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:.4rem"></div>', unsafe_allow_html=True)

    sel_theme   = st.selectbox("🎨 " + ("السمة" if ar_only else "Theme"), list(THEMES.keys()))
    num_slides  = st.slider("📊 " + ("الشرائح" if ar_only else "Slides"),    6, 20, 10)
    num_mcq     = st.slider("❓ " + ("عدد MCQ" if ar_only else "MCQ count"), 5, 30, 15)
    num_fc      = st.slider("🃏 " + ("البطاقات" if ar_only else "Cards"),     5, 25, 12)

    st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-section-title">{"تفاصيل المادة" if ar_only else "Course Details"}</div>', unsafe_allow_html=True)
    course_name = st.text_input("📚", placeholder="Course name" if not ar_only else "اسم المادة",     label_visibility="collapsed")
    institution = st.text_input("🏛️", placeholder="Institution" if not ar_only else "المؤسسة",        label_visibility="collapsed")
    lecturer    = st.text_input("👤", placeholder="Lecturer name" if not ar_only else "اسم المحاضر",  label_visibility="collapsed")
    focus_topic = st.text_input("🎯", placeholder="Focus topic" if not ar_only else "موضوع التركيز",  label_visibility="collapsed")

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def check_ready():
    if not api_key:
        st.warning("🔑 " + ("أدخل مفتاح API في الإعدادات." if ar_only else "Enter your Gemini API key in the left panel."))
        return False
    if not st.session_state.pdf_b64:
        st.warning("📄 " + ("ارفع ملف PDF في الإعدادات." if ar_only else "Upload a PDF in the left panel."))
        return False
    return True

def prog(se, pe, msg, pct):
    se.markdown(f'<div style="text-align:center;font-size:.84rem;color:#8b5cf6;margin:.3rem 0">{msg}</div>', unsafe_allow_html=True)
    pe.markdown(f'<div class="pb"><div class="pf" style="width:{pct}%"></div></div>', unsafe_allow_html=True)

def lang_instr():
    return "Provide ALL content in Arabic only." if ar_only else "Provide all content in English only."

tool = st.session_state.tool

#                                                               
# RIGHT PANEL — Studio outputs
#                                                               
with right_col:
    st.markdown(f'<div class="studio-title">⚡ {"الاستوديو" if ar_only else "Studio"}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="studio-sub">{"نتائج الأدوات · انقر للتنزيل" if ar_only else "Generated outputs · Click to download"}</div>', unsafe_allow_html=True)

    # Output cards — shown based on what has been generated
    if st.session_state.pdf_b64:
        # Slides card
        if tool == "slides":
            st.markdown(f'''<div class="output-card">
            <div class="output-card-icon">📊</div>
            <div class="output-card-title">{"شرائح المحاضرة" if ar_only else "Lecture Slides"}</div>
            <div class="output-card-desc">{"احترافية · PPTX محلي" if ar_only else "Premium slides · Local PPTX"}</div>
            </div>''', unsafe_allow_html=True)
        elif tool == "mcq":
            st.markdown(f'''<div class="output-card">
            <div class="output-card-icon">❓</div>
            <div class="output-card-title">{"أسئلة MCQ" if ar_only else "MCQ Questions"}</div>
            <div class="output-card-desc">{"أسئلة + إجابات + شرح" if ar_only else "Questions + answers + explanations"}</div>
            </div>''', unsafe_allow_html=True)
        elif tool == "exam":
            st.markdown(f'''<div class="output-card">
            <div class="output-card-icon">📝</div>
            <div class="output-card-title">{"ورقة الاختبار" if ar_only else "Exam Paper"}</div>
            <div class="output-card-desc">{"Word مع مخطط التصحيح" if ar_only else "Word file with mark scheme"}</div>
            </div>''', unsafe_allow_html=True)
        elif tool == "summary":
            st.markdown(f'''<div class="output-card">
            <div class="output-card-icon">📋</div>
            <div class="output-card-title">{"ملخص ذكي" if ar_only else "Smart Summary"}</div>
            <div class="output-card-desc">{"مصطلحات · صيغ · خريطة ذهنية" if ar_only else "Terms · formulas · mind map"}</div>
            </div>''', unsafe_allow_html=True)
        elif tool == "flashcards":
            st.markdown(f'''<div class="output-card">
            <div class="output-card-icon">🃏</div>
            <div class="output-card-title">{"بطاقات دراسية" if ar_only else "Flashcards"}</div>
            <div class="output-card-desc">{"بطاقات تفاعلية للمذاكرة" if ar_only else "Interactive study cards"}</div>
            </div>''', unsafe_allow_html=True)
        elif tool == "quiz":
            st.markdown(f'''<div class="output-card">
            <div class="output-card-icon">🎯</div>
            <div class="output-card-title">{"اختبر نفسك" if ar_only else "Self Quiz"}</div>
            <div class="output-card-desc">{"أسئلة MCQ مع التصحيح الفوري" if ar_only else "MCQ quiz with instant scoring"}</div>
            </div>''', unsafe_allow_html=True)

    # Tips
    st.markdown(f'<div style="margin-top:.8rem"><div class="panel-section-title">{"نصائح" if ar_only else "Tips"}</div></div>', unsafe_allow_html=True)
    tips_en = [
        "💡 Use custom instructions to focus on specific topics",
        "🎯 Quiz yourself after generating flashcards",
        "🔊 Use audio buttons to listen to summaries",
        "📊 Set slide count in settings panel",
    ]
    tips_ar = [
        "💡 استخدم التعليمات المخصصة لتحديد المواضيع",
        "🎯 اختبر نفسك بعد توليد البطاقات",
        "🔊 استخدم زر الصوت للاستماع للملخص",
        "📊 حدد عدد الشرائح في الإعدادات",
    ]
    for tip in (tips_ar if ar_only else tips_en):
        st.markdown(f'<div style="font-size:.73rem;color:#4b5280;padding:.22rem 0;border-bottom:1px solid rgba(255,255,255,.04)">{tip}</div>', unsafe_allow_html=True)

#                                                               
# CENTER PANEL — Main tools
#                                                               
with center_col:

    # ── 1. SLIDES ────────────────────────────────────────────
    if tool == "slides":
        st.markdown(f'<div class="tool-heading">📊 {"شرائح المحاضرة" if ar_only else "Lecture Slides"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"حوّل ملف PDF إلى عرض تقديمي احترافي مع الصيغ والأمثلة والجداول." if ar_only else "Turn your PDF into a professional presentation with formulas, worked examples, and real tables."}</div>', unsafe_allow_html=True)

        c1, c2 = st.columns([3,2])
        with c1:
            incl_f = st.checkbox("📐 " + ("الصيغ والمعادلات" if ar_only else "Formulas & equations"), value=True)
            incl_e = st.checkbox("✏️ " + ("أمثلة محلولة" if ar_only else "Worked examples"), value=True)
            incl_t = st.checkbox("📊 " + ("الجداول كجداول حقيقية" if ar_only else "Tables as real tables"), value=True)
        with c2:
            st.markdown(f'<div class="sbox" style="font-size:.72rem"><b>{"الأنواع:" if ar_only else "Types:"}</b><br>📖 {"نظرية" if ar_only else "Theory"} · 📐 {"صيغة" if ar_only else "Formula"} · ✏️ {"مثال" if ar_only else "Example"}<br>📊 {"جدول" if ar_only else "Table"} · 🔄 {"عمودان" if ar_only else "Two-col"} · 📈 {"إحصائيات" if ar_only else "Stats"}<br>✓ {"خلاصة" if ar_only else "Conclusion"}</div>', unsafe_allow_html=True)

        # Custom prompt
        st.markdown(f'<div class="prompt-box"><div class="prompt-label">🎯 {"تعليمات مخصصة — اختياري" if ar_only else "Custom Instructions — Optional"}</div>', unsafe_allow_html=True)
        custom_prompt = st.text_area(
            "", height=90, label_visibility="collapsed", key="slides_cp",
            placeholder=("مثال: ركز فقط على المتوسط الحسابي وطريقة الوسط المفترض مع أمثلة رقمية..." if ar_only
                         else "Example: Focus only on arithmetic mean. Include all worked examples with full step-by-step solutions..."))
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("✨ " + ("توليد الشرائح" if ar_only else "Generate Slides"), type="primary", use_container_width=True):
            if not check_ready(): st.stop()
            se = st.empty(); pe = st.empty()
            try:
                lang_ar  = ar_only
                lang_txt = ("Write EVERY word in Arabic only (اللغة العربية فقط). All content must be in Arabic." if lang_ar else "Write everything in English only.")
                ci = f"Course: {course_name}." if course_name else ""
                fi = f"Focus on: {focus_topic}." if focus_topic else ""
                cp_raw   = (custom_prompt or "").strip()
                has_cp   = bool(cp_raw)
                if has_cp:
                    intent_block = f"+   LECTURER INSTRUCTIONS — HIGHEST PRIORITY   +\n{cp_raw}\n+                                              +\nFollow these instructions exactly. They define what to cover and how."
                    focus_for_extract = f"The lecturer wants: {cp_raw}\nExtract ONLY content relevant to these instructions."
                else:
                    intent_block = "Cover all major topics from the document systematically."
                    focus_for_extract = "Extract ALL content from the PDF thoroughly."

                prog(se, pe, ("🧠 قراءة المستند…" if lang_ar else "🧠 Reading PDF…"), 15)

                ext_prompt = f"""You are a document analysis expert.
{focus_for_extract}
{ci} {fi}
{lang_txt}

MATH RULES — critical:
- NEVER write LaTeX like $\\bar{{x}}$ or \\frac{{}}{{}}
- Write clean Unicode: x̄ = Σx / n
- Fractions as: (top)/(bottom)
- Use: x̄ Σ √ ² ³ ≤ ≥ ≠ ± × ÷ → ≈ μ σ

Return ONLY in this exact format:

DOC_TITLE: [title]
DOC_SUBJECT: [subject]
DOC_AUTHOR: [author or blank]

SECTION: [heading]
CONTENT: [full content — all facts, numbers, definitions verbatim]
FORMULAS: [each formula on its own line as clean Unicode]
KEYPOINTS: [key points, one per line]

Repeat for every section."""

                raw_ext = call_gemini(api_key, ext_prompt, st.session_state.pdf_b64, tokens=6000, json_mode=False)

                doc_title=""; doc_subject=""; doc_author=""
                sections=[]; cur_sec=None; last_key=""
                for line in raw_ext.splitlines():
                    line=line.strip()
                    if not line: continue
                    if line.startswith("DOC_TITLE:"):   doc_title=line[10:].strip()
                    elif line.startswith("DOC_SUBJECT:"): doc_subject=line[12:].strip()
                    elif line.startswith("DOC_AUTHOR:"):  doc_author=line[11:].strip()
                    elif line.startswith("SECTION:"):
                        if cur_sec: sections.append(cur_sec)
                        cur_sec={"heading":line[8:].strip(),"content":"","formulas":[],"keypoints":[]}; last_key="heading"
                    elif line.startswith("CONTENT:") and cur_sec:
                        cur_sec["content"]=line[8:].strip(); last_key="content"
                    elif line.startswith("FORMULAS:") and cur_sec:
                        v=line[9:].strip()
                        if v: cur_sec["formulas"].append(v); last_key="formulas"
                    elif line.startswith("KEYPOINTS:") and cur_sec:
                        v=line[10:].strip()
                        if v: cur_sec["keypoints"].append(v); last_key="keypoints"
                    elif cur_sec:
                        if last_key=="content": cur_sec["content"]+=" "+line
                        elif last_key=="formulas": cur_sec["formulas"].append(line)
                        elif last_key=="keypoints": cur_sec["keypoints"].append(line)
                if cur_sec: sections.append(cur_sec)

                doc_summary=f"Document: {doc_title}\nSubject: {doc_subject}\n\n"
                for sec in sections:
                    doc_summary+=f"=== {sec['heading']} ===\n{sec['content']}\n"
                    for f2 in sec.get("formulas",[]): 
                        if f2: doc_summary+=f"FORMULA: {f2}\n"
                    for kp in sec.get("keypoints",[]): 
                        if kp: doc_summary+=f"• {kp}\n"
                    doc_summary+="\n"
                doc_summary=doc_summary[:12000]

                prog(se, pe, ("✅ تم الاستخراج — توليد الشرائح…" if lang_ar else "✅ Extracted — generating slides…"), 38)

                slide_count=num_slides
                slides_prompt=f"""You are a world-class university professor and expert slide designer.
{lang_txt}
{ci}

{intent_block}

DOCUMENT CONTENT — use ONLY this, never invent:
{doc_summary}

CREATE EXACTLY {slide_count} SLIDES.

SLIDE TYPES: title · bullets · lecture · formula · two_col · table · stat_callout · conclusion

RULES:
1. Every bullet: complete sentence with specific real data/numbers from document
2. Theory: minimum 3 sentences — full academic explanation
3. Formula: clean Unicode ONLY — x̄ = Σx/n NOT LaTeX
4. Where: define EVERY variable with units
5. Example: real numbers from document, full problem stated
6. Calc: every step shown — substitution, working, answer with units
7. Tables: ALL rows from document
8. Add emoji to bullets: 📊 📐 🔑 💡 ✅ ⚠️ 🎯 📋

DISTRIBUTE TYPES SMARTLY:
- lecture/formula for technical content with equations
- table for tabular data
- two_col for comparisons
- stat_callout for key numbers

FORMAT — separated by ===:

SLIDE_NUM: 1
TYPE: title
TITLE: exact document title
SUBTITLE: course or subject name
BODY: author and institution
===
SLIDE_NUM: 2
TYPE: bullets
TITLE: topic title
B1: 📋 specific real fact with data
B2: 🔑 specific real fact or definition
B3: 📊 specific fact with numbers
B4: ✅ definition or rule
B5: 💡 example or application
===
SLIDE_NUM: 3
TYPE: lecture
TITLE: concept name
THEORY: Full 3-sentence academic explanation. Define the concept clearly. Explain when and why it is used.
FORMULA: formula in Unicode e.g. x̄ = Σx / n
WHERE: x̄ = arithmetic mean, Σx = sum of all values, n = total number of observations
EXAMPLE: Five students scored 65, 72, 80, 55, 78. Find the arithmetic mean.
CALC1: Step 1 — Σx = 65 + 72 + 80 + 55 + 78 = 350
CALC2: Step 2 — x̄ = 350 / 5
CALC3: Answer — x̄ = 70 marks
===
SLIDE_NUM: 4
TYPE: formula
TITLE: formula name
FORMULA: formula in Unicode
WHERE: var1 = definition with units, var2 = definition
EXAMPLE: full numerical problem from document
CALC1: substitution
CALC2: calculation
CALC3: final answer with units
===
SLIDE_NUM: 5
TYPE: two_col
TITLE: comparison title
LEFT_TITLE: left category
L1: specific left point 1
L2: specific left point 2
L3: specific left point 3
L4: specific left point 4
RIGHT_TITLE: right category
R1: specific right point 1
R2: specific right point 2
R3: specific right point 3
R4: specific right point 4
===
SLIDE_NUM: 6
TYPE: table
TITLE: table title from document
H1: column 1
H2: column 2
H3: column 3
ROW: val | val | val
ROW: val | val | val
ROW: val | val | val
===
SLIDE_NUM: 7
TYPE: stat_callout
TITLE: statistics title
STAT1_VAL: number
STAT1_LBL: what it represents
STAT2_VAL: number
STAT2_LBL: what it represents
STAT3_VAL: number
STAT3_LBL: what it represents
BODY: context sentence
===
SLIDE_NUM: {slide_count}
TYPE: conclusion
TITLE: Key Takeaways
B1: 🎯 most important learning — specific
B2: 📐 key formula and when to use it
B3: 💡 practical application
B4: ✅ common mistake to avoid
B5: 📚 connection to next topic
===

GENERATE ALL {slide_count} SLIDES. Replace every placeholder with real content from the document.
Each slide must be rich enough for a student to study without the original document."""

                prog(se, pe, ("📝 توليد الشرائح…" if lang_ar else "📝 Generating slides…"), 52)
                raw_slides = call_gemini(api_key, slides_prompt, tokens=8000, json_mode=False)

                prog(se, pe, ("🔧 معالجة…" if lang_ar else "🔧 Processing…"), 78)

                def parse_slides_text(raw):
                    slides_out = []
                    for block in raw.split("==="):
                        block = block.strip()
                        if not block: continue
                        s={}; calc_steps=[]; left_pts=[]; right_pts=[]; rows=[]; bullets=[]; hdrs=[]; stats=[]
                        for line in block.splitlines():
                            line=line.strip()
                            if not line or ":" not in line: continue
                            key,_,val=line.partition(":"); key=key.strip().upper(); val=val.strip()
                            if   key=="SLIDE_NUM":  s["slide_num"]=int(val) if val.isdigit() else len(slides_out)+1
                            elif key=="TYPE":       s["type"]=val.lower()
                            elif key=="TITLE":      s["title"]=val
                            elif key=="SUBTITLE":   s["subtitle"]=val
                            elif key=="BODY":       s["body"]=val
                            elif key=="THEORY":     s["theory"]=val
                            elif key=="FORMULA":    s["formula"]=val
                            elif key=="WHERE":      s["where"]=val
                            elif key=="EXAMPLE":    s["example"]=val
                            elif key.startswith("CALC"):  calc_steps.append(val)
                            elif key=="LEFT_TITLE": s["left_title"]=val
                            elif key=="RIGHT_TITLE":s["right_title"]=val
                            elif key.startswith("L") and key[1:].isdigit(): left_pts.append(val)
                            elif key.startswith("R") and key[1:].isdigit(): right_pts.append(val)
                            elif key.startswith("B") and key[1:].isdigit(): bullets.append(val)
                            elif key.startswith("H") and key[1:].isdigit(): hdrs.append(val)
                            elif key=="ROW": rows.append([c.strip() for c in val.split("|")])
                            elif key.startswith("STAT") and key.endswith("_VAL"):
                                idx=int(key[4:-4])-1
                                while len(stats)<=idx: stats.append({})
                                stats[idx]["value"]=val
                            elif key.startswith("STAT") and key.endswith("_LBL"):
                                idx=int(key[4:-4])-1
                                while len(stats)<=idx: stats.append({})
                                stats[idx]["label"]=val
                        if calc_steps: s["calculation"]="\n".join(calc_steps)
                        if left_pts:   s["left_points"]=left_pts
                        if right_pts:  s["right_points"]=right_pts
                        if bullets:    s["bullets"]=bullets
                        if hdrs:       s["headers"]=hdrs
                        if rows:       s["rows"]=rows
                        if stats:      s["stats"]=[x for x in stats if x]
                        if s.get("type") and s.get("title"): slides_out.append(s)
                    return slides_out

                all_slides=parse_slides_text(raw_slides)
                for i,sl in enumerate(all_slides):
                    if "slide_num" not in sl: sl["slide_num"]=i+1
                if len(all_slides)<slide_count:
                    existing={s["slide_num"] for s in all_slides}
                    for i in range(1,slide_count+1):
                        if i not in existing:
                            sec=sections[(i-1)%len(sections)] if sections else {}
                            all_slides.append({"slide_num":i,"type":"conclusion" if i==slide_count else "bullets","title":sec.get("heading","") or f"Topic {i}","bullets":sec.get("keypoints",["See document"])[:5]})
                    all_slides.sort(key=lambda x:x.get("slide_num",0))

                T=THEMES[sel_theme]
                for _s in all_slides:
                    _s["_lecturer"]=lecturer or ""; _s["_institution"]=institution or ""
                prog(se, pe, f"🎨 {'بناء' if lang_ar else 'Building'} {len(all_slides)} {'شرائح' if lang_ar else 'slides'}…", 88)
                xmls=[build_slide(s,T) for s in all_slides]
                prog(se, pe, "💾 Assembling…", 96)
                pptx_bytes=assemble_pptx(xmls)
                se.empty(); pe.empty()
                st.success(f"✅ {len(xmls)} " + ("شريحة جاهزة!" if lang_ar else "slides ready!"))
                safe_n=re.sub(r"[^a-zA-Z0-9_\- ]","",doc_title)[:40].strip().replace(" ","_") or "caawiye_slides"
                st.download_button("⬇️ " + ("تنزيل الشرائح (.pptx)" if lang_ar else "Download Slides (.pptx)"),
                    data=pptx_bytes, file_name=f"{safe_n}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True)
                with st.expander("📋 " + ("مخطط الشرائح" if lang_ar else "Slide outline")):
                    for s in all_slides:
                        st.markdown(f"**{s.get('slide_num')}. {s.get('title','')}** `{s.get('type','')}`")
                        for b in s.get("bullets",[]): st.markdown(f"  - {b}")
            except Exception as e:
                se.empty(); pe.empty(); st.error(str(e))
                import traceback; st.code(traceback.format_exc())

    # ── 2. MCQ ───────────────────────────────────────────────
    elif tool == "mcq":
        st.markdown(f'<div class="tool-heading">❓ {"أسئلة الاختيار" if ar_only else "MCQ Generator"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"توليد أسئلة اختيار من متعدد مع الإجابات والشرح." if ar_only else "Generate multiple choice questions with answers and explanations."}</div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1: mcq_diff=st.selectbox("Difficulty",["Easy","Medium","Hard","Mixed"])
        with c2: mcq_type=st.selectbox("Type",["Conceptual","Calculation","Mixed"])
        with c3: show_ans=st.checkbox("Show answers",value=True)
        st.markdown(f'<div class="prompt-box"><div class="prompt-label">🎯 {"تعليمات — اختياري" if ar_only else "Instructions — Optional"}</div>', unsafe_allow_html=True)
        mcq_cp=st.text_area("",height=80,label_visibility="collapsed",key="mcq_cp",
            placeholder=("مثال: ركز على أسئلة الحساب فقط..." if ar_only else "Example: Focus only on calculation questions with real numbers..."))
        st.markdown('</div>',unsafe_allow_html=True)

        if st.button("🎯 " + ("توليد الأسئلة" if ar_only else "Generate MCQ"), type="primary", use_container_width=True):
            if not check_ready(): st.stop()
            se=st.empty(); pe=st.empty()
            try:
                prog(se,pe,"🧠 Generating…",35)
                fi=f"Focus on: {focus_topic}." if focus_topic else ""
                mcp=f"\n\nLECTURER INSTRUCTIONS:\n{mcq_cp.strip()}" if mcq_cp and mcq_cp.strip() else ""
                prompt=f"""Create {num_mcq} MCQ questions. Difficulty: {mcq_diff}. Type: {mcq_type}. {fi}
{lang_instr()}{mcp}
Never say "from the document". Write standalone academic questions.
4 options A/B/C/D, one correct answer.
Return raw JSON only:
{{"subject":"...","subject_ar":"...","questions":[
{{"num":1,"question":"...","question_ar":"...","options":{{"A":"...","B":"...","C":"...","D":"..."}},"options_ar":{{"A":"...","B":"...","C":"...","D":"..."}},"correct":"A","explanation":"...","explanation_ar":"...","difficulty":"{mcq_diff}","topic":"...","topic_ar":"..."}}
]}}
Generate exactly {num_mcq} questions."""
                raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,tokens=4000)
                prog(se,pe,"✅",90)
                data=safe_parse(raw); st.session_state.mcq_data=data
                se.empty(); pe.empty()
            except Exception as e:
                se.empty(); pe.empty(); st.error(str(e))

        if st.session_state.mcq_data:
            data=st.session_state.mcq_data; qs=data.get("questions",[])
            subj=data.get("subject","")
            st.markdown(f'<div style="margin-bottom:.8rem"><span class="kterm">📚 {subj}</span><span class="kterm">❓ {len(qs)} {"سؤال" if ar_only else "questions"}</span></div>',unsafe_allow_html=True)
            # Audio
            all_q_txt=" ".join([f"Q{q.get('num','')}. {q.get('question','')}" for q in qs])
            st.markdown('<div style="margin:.4rem 0 .9rem">'+make_audio_btn(all_q_txt,ar_only=ar_only,label_en="Listen to Questions",label_ar="استمع للأسئلة")+'</div>',unsafe_allow_html=True)
            docx=make_mcq_docx(data,show_ans,ar_only)
            st.download_button("⬇️ "+("تنزيل MCQ (.docx)" if ar_only else "Download MCQ (.docx)"),data=docx,file_name="caawiye_mcq.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
            for q in qs:
                corr=q.get("correct","")
                st.markdown(f'<div class="mcq-wrap"><div style="display:flex;justify-content:space-between;margin-bottom:.35rem"><span style="font-size:.68rem;color:#8b5cf6;font-weight:700">Q{q.get("num","")} · {q.get("topic","")}</span><span class="kterm" style="font-size:.66rem">{q.get("difficulty","")}</span></div><div class="mcq-q">{q.get("question","")}</div>{"<div class=\"mcq-ar\">"+q.get("question_ar","")+"</div>" if q.get("question_ar") and show_ar else ""}',unsafe_allow_html=True)
                opts_ar=q.get("options_ar",{})
                for k,v in q.get("options",{}).items():
                    cls="ok" if show_ans and k==corr else ""
                    ar_opt=opts_ar.get(k,"")
                    st.markdown(f'<div class="mcq-opt {cls}"><span class="mcq-ltr">{k}</span>{v}{" | "+ar_opt if ar_opt and show_ar else ""}</div>',unsafe_allow_html=True)
                if show_ans and q.get("explanation"):
                    exp_ar=q.get("explanation_ar","")
                    st.markdown(f'<div class="mcq-exp">💡 {q["explanation"]}{"<br>"+exp_ar if exp_ar and show_ar else ""}</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)

    # ── 3. EXAM ──────────────────────────────────────────────
    elif tool == "exam":
        st.markdown(f'<div class="tool-heading">📝 {"ورقة الاختبار" if ar_only else "Exam Paper"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"أنشئ اختباراً احترافياً بأقسام مخصصة وأسئلة حقيقية من الوثيقة." if ar_only else "Build a professional exam with custom sections and real questions from your document."}</div>', unsafe_allow_html=True)
        c1,c2,c3,c4=st.columns(4)
        with c1: exam_dur =st.selectbox("Duration",["30 min","1 hour","1.5 hours","2 hours","2.5 hours","3 hours"])
        with c2: total_mks=st.selectbox("Total marks",["25","50","60","80","100","120"])
        with c3: exam_diff2=st.selectbox("Difficulty",["Easy","Medium","Hard","Mixed"])
        with c4: incl_ms  =st.checkbox("Mark scheme",value=True)

        st.markdown("### "+ ("الأقسام" if ar_only else "Sections"))
        updated=[]
        for i,sec in enumerate(st.session_state.exam_sections):
            with st.expander(f"{'القسم' if ar_only else 'Section'} {i+1} — {sec['name']} ({(SECTION_TYPES_AR if ar_only else SECTION_TYPES_EN).get(sec['type'],sec['type'])})",expanded=(i==0)):
                rc1,rc2,rc3,rc4,rc5=st.columns([2,2,1,1,1])
                with rc1: sn=st.text_input("Name (EN)",sec["name"],key=f"sn{i}")
                with rc2:
                    tkeys=list(SECTION_TYPES_EN.keys()); cur=tkeys.index(sec["type"]) if sec["type"] in tkeys else 0
                    styp=st.selectbox("Type",tkeys,index=cur,format_func=lambda x:(SECTION_TYPES_AR if ar_only else SECTION_TYPES_EN).get(x,x),key=f"st{i}")
                with rc3: smk=st.number_input("Marks",1,200,sec["marks"],key=f"sm{i}")
                with rc4: snq=st.number_input("Qs",  1,30, sec["num_q"], key=f"sq{i}")
                with rc5:
                    st.markdown("<div style='height:26px'></div>",unsafe_allow_html=True)
                    if st.button("🗑️",key=f"del{i}"):
                        st.session_state.exam_sections.pop(i); st.rerun()
                req_c1,req_c2=st.columns([1,2])
                with req_c1:
                    answer_req=st.number_input("Answer only (0=all)" if not ar_only else "أجب على (0=الكل)",
                        min_value=0,max_value=sec["num_q"],value=int(sec.get("answer_req",0)),key=f"req{i}")
                with req_c2:
                    if answer_req and answer_req>0:
                        nums={"1":"ONE","2":"TWO","3":"THREE","4":"FOUR","5":"FIVE","6":"SIX","7":"SEVEN","8":"EIGHT","9":"NINE","10":"TEN"}
                        nums_ar={"1":"واحداً","2":"اثنين","3":"ثلاثة","4":"أربعة","5":"خمسة","6":"ستة","7":"سبعة","8":"ثمانية","9":"تسعة","10":"عشرة"}
                        wen=nums.get(str(answer_req),str(answer_req)); war=nums_ar.get(str(answer_req),str(answer_req))
                        st.markdown(f'<div style="margin-top:1.5rem;background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.2);border-radius:8px;padding:.4rem .75rem;font-size:.76rem;color:#a78bfa">Answer only <b>{wen}</b> questions | أجب على <b>{war}</b> فقط</div>',unsafe_allow_html=True)
                sna=st.text_input("Name (AR)",sec.get("name_ar",""),key=f"sna{i}")
                sd =st.text_input("Instructions (EN)",sec.get("desc",""),   key=f"sd{i}")
                sda=st.text_input("Instructions (AR)",sec.get("desc_ar",""),key=f"sda{i}")
                updated.append({"name":sn,"name_ar":sna,"type":styp,"marks":smk,"num_q":snq,"desc":sd,"desc_ar":sda,"answer_req":int(answer_req)})
        st.session_state.exam_sections=updated

        ac1,ac2=st.columns(2)
        with ac1:
            if st.button("➕ "+("إضافة قسم" if ar_only else "Add Section"),use_container_width=True):
                n2=len(st.session_state.exam_sections)+1
                st.session_state.exam_sections.append({"name":f"Section {chr(64+n2)}","name_ar":f"القسم {n2}","type":"short_answer","marks":20,"num_q":4,"desc":"","desc_ar":"","answer_req":0})
                st.rerun()
        with ac2:
            tot=sum(s["marks"] for s in st.session_state.exam_sections)
            st.markdown(f'<div style="background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.2);border-radius:8px;padding:.45rem .9rem;font-size:.8rem;color:#a78bfa;text-align:center">Configured: <b style="color:#f0f2ff">{tot}</b>/{total_mks} marks</div>',unsafe_allow_html=True)

        st.markdown(f'<div class="prompt-box"><div class="prompt-label">🎯 {"تعليمات — اختياري" if ar_only else "Instructions — Optional"}</div>',unsafe_allow_html=True)
        exam_cp=st.text_area("",height=80,label_visibility="collapsed",key="exam_cp",
            placeholder=("مثال: ركز على المتوسط الحسابي فقط..." if ar_only else "Example: Focus on arithmetic mean. Make Section C harder..."))
        st.markdown('</div>',unsafe_allow_html=True)

        if st.button("📝 "+("توليد الاختبار" if ar_only else "Generate Exam Paper"),type="primary",use_container_width=True):
            if not check_ready(): st.stop()
            se=st.empty(); pe=st.empty()
            try:
                prog(se,pe,"🧠 AI generating exam…",20)
                ci=f"Course: {course_name}." if course_name else ""
                li=f"Lecturer: {lecturer}." if lecturer else ""
                fi=f"Focus: {focus_topic}." if focus_topic else ""
                ecp=f"\n\nLECTURER INSTRUCTIONS:\n{exam_cp.strip()}" if exam_cp and exam_cp.strip() else ""

                def bqt(t,qnum,qmk):
                    if t=="mcq":
                        return (f'{{"num":"{qnum}","text":"WRITE MCQ question {qnum}","text_ar":"","marks":{qmk},'
                                f'"answer_lines":1,"options":{{"A":"opt A","B":"opt B","C":"opt C","D":"opt D"}},'
                                f'"correct":"A","model_answer":"A — reason","model_answer_ar":""}}')
                    elif t=="true_false":
                        return f'{{"num":"{qnum}","text":"WRITE statement {qnum}","text_ar":"","marks":{qmk},"answer_lines":1,"model_answer":"True/False — reason","model_answer_ar":""}}'
                    elif t=="fill_blank":
                        return f'{{"num":"{qnum}","text":"Complete: _______ {qnum}","text_ar":"","marks":{qmk},"answer_lines":1,"model_answer":"word","model_answer_ar":""}}'
                    elif t=="short_answer":
                        return f'{{"num":"{qnum}","text":"WRITE short answer Q{qnum}","text_ar":"","marks":{qmk},"answer_lines":4,"model_answer":"WRITE marking points","model_answer_ar":""}}'
                    elif t in ("long_answer","calculation"):
                        sub=max(1,round(qmk/3))
                        return (f'{{"num":"{qnum}","text":"WRITE question {qnum}","text_ar":"","marks":{qmk},"answer_lines":12,'
                                f'"parts":[{{"part":"a","text":"WRITE part a","text_ar":"","marks":{sub},"answer_lines":4,"model_answer":"model a","model_answer_ar":""}},'
                                f'{{"part":"b","text":"WRITE part b","text_ar":"","marks":{sub},"answer_lines":5,"model_answer":"model b","model_answer_ar":""}},'
                                f'{{"part":"c","text":"WRITE part c","text_ar":"","marks":{qmk-2*sub},"answer_lines":3,"model_answer":"model c","model_answer_ar":""}}],'
                                f'"model_answer":"WRITE full answer","model_answer_ar":""}}')
                    elif t=="matching":
                        return f'{{"num":"{qnum}","text":"Match Column A with Column B.","text_ar":"","marks":{qmk},"answer_lines":2,"model_answer":"key","model_answer_ar":""}}'
                    else:
                        return f'{{"num":"{qnum}","text":"WRITE Q{qnum}","text_ar":"","marks":{qmk},"answer_lines":6,"model_answer":"WRITE answer","model_answer_ar":""}}'

                def stmpl(sec):
                    t=sec["type"]; mk=sec["marks"]; n=sec["num_q"]; qmk=max(1,round(mk/n))
                    st_en=(SECTION_TYPES_AR if ar_only else SECTION_TYPES_EN).get(t,""); st_ar=SECTION_TYPES_AR.get(t,"")
                    req=int(sec.get("answer_req",0))
                    nums_w={1:"ONE",2:"TWO",3:"THREE",4:"FOUR",5:"FIVE",6:"SIX",7:"SEVEN",8:"EIGHT",9:"NINE",10:"TEN"}
                    nums_ar_w={1:"واحداً",2:"اثنين",3:"ثلاثة",4:"أربعة",5:"خمسة",6:"ستة",7:"سبعة",8:"ثمانية",9:"تسعة",10:"عشرة"}
                    if req>0:
                        wen=nums_w.get(req,str(req)); war=nums_ar_w.get(req,str(req))
                        instr_en=sec["desc"] if sec["desc"] else f"Answer only {wen} ({req}) questions from this section."
                        instr_ar=sec["desc_ar"] if sec["desc_ar"] else f"أجب فقط على {war} ({req}) أسئلة من هذا القسم."
                    else:
                        instr_en=sec["desc"] or "Answer all questions."
                        instr_ar=sec["desc_ar"] or "أجب على جميع الأسئلة."
                    base=(f'"name":"{sec["name"]}","name_ar":"{sec["name_ar"]}",'
                          f'"type":"{t}","description":"{st_en}","description_ar":"{st_ar}",'
                          f'"marks":{mk},"instructions":"{instr_en}","instructions_ar":"{instr_ar}"')
                    ql=",\n    ".join(bqt(t,i+1,qmk) for i in range(n))
                    if t=="matching":
                        return '{"'+base[1:]+',"col_a":["Term 1","Term 2","Term 3","Term 4","Term 5"],"col_b":["Def A","Def B","Def C","Def D","Def E"],"questions":['+ql+']}'
                    return '{'+base+',"questions":['+ql+']}'

                secs_json="["+",\n".join(stmpl(s) for s in st.session_state.exam_sections)+"]"
                total_qs=sum(s["num_q"] for s in st.session_state.exam_sections)
                lang_note="Write every word in Arabic only." if ar_only else "Write in English only."

                prompt=f"""Chief university examiner. Read PDF, fill this exam with REAL questions.
{ci} {li} Duration: {exam_dur}. Total: {total_mks} marks. Difficulty: {exam_diff2}. {fi}
{lang_note}{ecp}
Replace every "WRITE..." with a real question from the document.
Rules: Never say "from the document". MCQ: one correct, three plausible wrong. 
Calculation: real numbers, full working. Matching: real terms and definitions.
Return raw JSON only:
{{"title":"title","title_ar":"","institution":"{institution or 'University'}","institution_ar":"","course":"{course_name or 'Course'}","course_ar":"","lecturer":"{lecturer or ''}","lecturer_ar":"","duration":"{exam_dur}","total_marks":{total_mks},"date":"________________",
"instructions":[{{"en":"Read all questions carefully.","ar":"اقرأ جميع الأسئلة بعناية."}},{{"en":"Show all working.","ar":"اعرض جميع خطوات الحل."}}],
"sections":{secs_json}}}"""
                raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,tokens=7000)
                prog(se,pe,"✅",80)
                data=safe_parse(raw); st.session_state.exam_data=data
                se.empty(); pe.empty()
            except Exception as e:
                se.empty(); pe.empty(); st.error(str(e))
                import traceback; st.code(traceback.format_exc())

        if st.session_state.exam_data:
            data=st.session_state.exam_data
            docx=make_exam_docx(data,incl_ms,ar_only)
            st.success("✅ "+("ورقة الاختبار جاهزة!" if ar_only else "Exam paper ready!"))
            safe=re.sub(r"[^a-zA-Z0-9_\- ]","",data.get("title","exam"))[:40].strip().replace(" ","_") or "caawiye_exam"
            st.download_button("⬇️ "+("تنزيل الاختبار" if ar_only else "Download Exam (.docx)"),data=docx,file_name=f"{safe}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
            d=data
            for sec in d.get("sections",[]):
                stype=sec.get("type","short_answer")
                name_ar_s=f" | {sec.get('name_ar','')}" if sec.get("name_ar") and show_ar else ""
                st.markdown(f'<div class="exam-sec">{sec.get("name","")}{name_ar_s} — {sec.get("description","")} ({sec.get("marks","")} marks)</div>',unsafe_allow_html=True)
                if stype=="matching" and sec.get("col_a"):
                    mc1,mc2=st.columns(2)
                    with mc1:
                        st.markdown("**Column A**")
                        for i2,v in enumerate(sec["col_a"]): st.markdown(f"{i2+1}. {v}")
                    with mc2:
                        st.markdown("**Column B**")
                        for i2,v in enumerate(sec.get("col_b",[])): st.markdown(f"{chr(65+i2)}. {v}")
                for q in sec.get("questions",[]):
                    qar=q.get("text_ar","")
                    st.markdown(f'<div class="exam-q"><span class="exam-qn">Q{q.get("num","")}.&nbsp;</span>{q.get("text","")}<span class="mktag">[{q.get("marks","")} marks]</span></div>',unsafe_allow_html=True)
                    if qar and show_ar: st.markdown(f'<div style="font-family:Amiri,serif;direction:rtl;text-align:right;font-size:.82rem;color:#8b5cf6;padding:.16rem 0">{qar}</div>',unsafe_allow_html=True)
                    if stype=="mcq" and q.get("options"):
                        for k,v in q["options"].items():
                            st.markdown(f'<div style="padding:.14rem .5rem .14rem 1.3rem;font-size:.79rem;color:#64748b">{k}) {v}</div>',unsafe_allow_html=True)
                    elif q.get("parts"):
                        for pt in q.get("parts",[]):
                            pt_ar=pt.get("text_ar","")
                            st.markdown(f'<div class="exam-q" style="padding-left:1.5rem"><span class="exam-qn">({pt.get("part","")})&nbsp;</span>{pt.get("text","")}<span class="mktag">[{pt.get("marks","")} mk]</span></div>',unsafe_allow_html=True)
                            if pt_ar and show_ar: st.markdown(f'<div style="font-family:Amiri,serif;direction:rtl;text-align:right;font-size:.79rem;color:#8b5cf6;padding-right:1.4rem">{pt_ar}</div>',unsafe_allow_html=True)
                            for _ in range(min(pt.get("answer_lines",3),4)): st.markdown('<div class="ans-ln"></div>',unsafe_allow_html=True)
            if incl_ms:
                with st.expander("📋 "+("مخطط التصحيح" if ar_only else "Mark Scheme")):
                    for sec in d.get("sections",[]):
                        st.markdown(f"**{sec.get('name','')}**")
                        for q in sec.get("questions",[]):
                            st.markdown(f"**Q{q.get('num','')}** [{q.get('marks','')} mk]: {q.get('model_answer','')}")
                            if show_ar and q.get("model_answer_ar"): st.markdown(f"*{q['model_answer_ar']}*")
                            if q.get("correct"):
                                c2=q["correct"]; opts2=q.get("options",{})
                                st.markdown(f"  ✓ **{c2}**: {opts2.get(c2,'')}")
                            if q.get("parts"):
                                for pt in q["parts"]: st.markdown(f"  **({pt.get('part','')})** {pt.get('model_answer','')}")

    # ── 4. SUMMARY ───────────────────────────────────────────
    elif tool == "summary":
        st.markdown(f'<div class="tool-heading">📋 {"الملخص الذكي" if ar_only else "Smart Summary"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"مصطلحات · صيغ · خريطة ذهنية · استنتاجات رئيسية — مع خيار الاستماع الصوتي." if ar_only else "Key terms · formulas · mind map · conclusions — with audio listen."}</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            sum_depth=st.selectbox("Depth",["Quick overview","Standard","Detailed"])
            incl_kw=st.checkbox("Key terms",value=True)
        with c2:
            incl_fo=st.checkbox("Formulas",value=True)
            incl_mm=st.checkbox("Mind map",value=True)
        st.markdown(f'<div class="prompt-box"><div class="prompt-label">🎯 {"تعليمات — اختياري" if ar_only else "Instructions — Optional"}</div>',unsafe_allow_html=True)
        sum_cp=st.text_area("",height=80,label_visibility="collapsed",key="sum_cp",
            placeholder=("مثال: ركز على المصطلحات والصيغ فقط..." if ar_only else "Example: Focus on key formulas and definitions only..."))
        st.markdown('</div>',unsafe_allow_html=True)

        if st.button("📋 "+("توليد الملخص" if ar_only else "Generate Summary"),type="primary",use_container_width=True):
            if not check_ready(): st.stop()
            se=st.empty(); pe=st.empty()
            try:
                prog(se,pe,"🧠 Summarizing…",35)
                fi=f"Focus: {focus_topic}." if focus_topic else ""
                scp=f"\n\nLECTURER INSTRUCTIONS:\n{sum_cp.strip()}" if sum_cp and sum_cp.strip() else ""
                prompt=f"""Create a {sum_depth} academic summary. {fi}
{lang_instr()}
Never say "from the document".{scp}
Return raw JSON only:
{{"title":"...","title_ar":"...","subject":"...","subject_ar":"...",
"overview":"2-3 sentence overview","overview_ar":"نظرة عامة",
"sections":[{{"heading":"...","heading_ar":"...","summary":"3-5 sentences","summary_ar":"...","key_points":["p1","p2","p3"],"key_points_ar":["ن1","ن2","ن3"]}}],
"key_terms":[{{"term":"...","term_ar":"...","definition":"...","definition_ar":"...","example":"..."}}],
"formulas":[{{"name":"...","name_ar":"...","formula":"...","meaning":"...","meaning_ar":"...","variables":"..."}}],
"mind_map":{{"center":"topic","center_ar":"الموضوع","branches":[{{"topic":"b","topic_ar":"فرع","subtopics":["s1","s2"],"subtopics_ar":["ف1","ف2"]}}]}},
"key_conclusions":["c1","c2","c3"],"key_conclusions_ar":["ن1","ن2","ن3"]}}"""
                raw=call_gemini(api_key,prompt,st.session_state.pdf_b64,tokens=4000)
                prog(se,pe,"✅",90)
                data=safe_parse(raw); st.session_state.sum_data=data
                se.empty(); pe.empty()
            except Exception as e:
                se.empty(); pe.empty(); st.error(str(e))

        if st.session_state.sum_data:
            data=st.session_state.sum_data
            docx=make_summary_docx(data,ar_only)
            st.download_button("⬇️ "+("تنزيل الملخص" if ar_only else "Download Summary (.docx)"),data=docx,file_name="caawiye_summary.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
            # Audio
            ov=data.get("overview",""); secs_txt=" ".join(s.get("summary","") for s in data.get("sections",[]))
            conc_txt=" ".join(data.get("key_conclusions",[]))
            speak_txt=f"{data.get('title','')}. {ov} {secs_txt} {conc_txt}"
            speak_txt_ar=f"{data.get('title_ar','')}. {data.get('overview_ar','')}"
            st.markdown('<div style="margin:.5rem 0 1rem;display:flex;align-items:center;gap:.8rem">'+
                make_audio_btn(speak_txt_ar if ar_only else speak_txt,ar_only=ar_only,
                    label_en="Listen to Summary",label_ar="استمع للملخص")+
                f'<span style="font-size:.7rem;color:#4b5280">{"قراءة صوتية" if ar_only else "Browser TTS"}</span></div>',
                unsafe_allow_html=True)
            ov_ar=data.get("overview_ar","")
            st.markdown(f'<div class="content-card"><div class="card-title">📌 {"نظرة عامة" if ar_only else "Overview"}</div><div style="font-size:.87rem;color:#64748b;line-height:1.8">{data.get("overview","")}</div>{"<div class=\"sum-ar\" style=\"margin-top:.5rem\">"+ov_ar+"</div>" if ov_ar and show_ar else ""}</div>',unsafe_allow_html=True)
            for sec in data.get("sections",[]):
                h_ar=sec.get("heading_ar",""); s_ar=sec.get("summary_ar","")
                st.markdown(f'<div class="sum-s"><div class="sum-h">{sec.get("heading","")}</div>{"<div class=\"sum-ar\">"+h_ar+"</div>" if h_ar and show_ar else ""}<div class="sum-txt">{sec.get("summary","")}</div>{"<div class=\"sum-txt\" style=\"direction:rtl;text-align:right;font-family:Amiri,serif;margin-top:.4rem\">"+s_ar+"</div>" if s_ar and show_ar else ""}</div>',unsafe_allow_html=True)
                kps=sec.get("key_points",[]); kps_ar=(sec.get("key_points_ar") or [])+[""]*20
                for kp,kp_ar in zip(kps,kps_ar):
                    st.markdown(f'<div style="padding:.12rem .5rem .12rem .9rem;font-size:.81rem;color:#64748b">▸ {kp}{" | "+kp_ar if kp_ar and show_ar else ""}</div>',unsafe_allow_html=True)
            c1_s,c2_s=st.columns(2)
            with c1_s:
                if incl_kw and data.get("key_terms"):
                    st.markdown(f'<div class="content-card"><div class="card-title">📚 {"المصطلحات" if ar_only else "Key Terms"}</div>',unsafe_allow_html=True)
                    for kt in data["key_terms"]:
                        t_ar=kt.get("term_ar",""); d_ar=kt.get("definition_ar","")
                        st.markdown(f'<div style="margin-bottom:.6rem"><span class="kterm">{kt.get("term","")}</span>{"<span class=\"kterm\" style=\"font-family:Amiri,serif\">"+t_ar+"</span>" if t_ar and show_ar else ""}<div style="font-size:.77rem;color:#64748b;margin-top:.2rem">{kt.get("definition","")}</div>{"<div style=\"font-size:.75rem;color:#4b5280;direction:rtl;text-align:right;font-family:Amiri,serif\">"+d_ar+"</div>" if d_ar and show_ar else ""}</div>',unsafe_allow_html=True)
                    st.markdown('</div>',unsafe_allow_html=True)
            with c2_s:
                if incl_fo and data.get("formulas"):
                    st.markdown(f'<div class="content-card"><div class="card-title">📐 {"الصيغ" if ar_only else "Formulas"}</div>',unsafe_allow_html=True)
                    for f in data["formulas"]:
                        n_ar=f.get("name_ar",""); m_ar=f.get("meaning_ar","")
                        st.markdown(f'<div style="margin-bottom:.72rem"><div style="font-family:monospace;font-size:.91rem;color:#a78bfa;background:rgba(124,58,237,.08);padding:.3rem .65rem;border-radius:6px;margin-bottom:.2rem">{f.get("formula","")}</div><div style="font-size:.72rem;color:#4b5280">{f.get("name","")}{" | "+n_ar if n_ar and show_ar else ""} — {f.get("meaning","")}</div></div>',unsafe_allow_html=True)
                    st.markdown('</div>',unsafe_allow_html=True)
            if incl_mm and data.get("mind_map"):
                mm=data["mind_map"]; c_ar=mm.get("center_ar","")
                st.markdown(f'<div class="content-card"><div class="card-title">🗺️ {"خريطة ذهنية" if ar_only else "Mind Map"}</div><div style="text-align:center;font-family:Syne,sans-serif;font-size:1rem;font-weight:700;color:#8b5cf6;padding:.55rem;background:rgba(124,58,237,.08);border-radius:7px;margin-bottom:.65rem">{mm.get("center","")}{" | "+c_ar if c_ar and show_ar else ""}</div>',unsafe_allow_html=True)
                brc=st.columns(min(len(mm.get("branches",[])),4))
                for i2,br in enumerate(mm.get("branches",[])):
                    with brc[i2%len(brc)]:
                        t_ar=br.get("topic_ar","")
                        st.markdown(f'<div style="background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.14);border-radius:8px;padding:.6rem;margin-bottom:.4rem"><div style="font-weight:600;color:#a78bfa;font-size:.79rem;margin-bottom:.3rem">{br.get("topic","")}{" | "+t_ar if t_ar and show_ar else ""}</div>',unsafe_allow_html=True)
                        subs=br.get("subtopics",[]); subs_ar=(br.get("subtopics_ar") or [])+[""]*20
                        for s2,s2_ar in zip(subs,subs_ar):
                            st.markdown(f'<div style="font-size:.72rem;color:#4b5280;padding:1px 0">· {s2}{" | "+s2_ar if s2_ar and show_ar else ""}</div>',unsafe_allow_html=True)
                        st.markdown('</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
            st.markdown(f'<div class="content-card"><div class="card-title">✅ {"الاستنتاجات" if ar_only else "Key Conclusions"}</div>',unsafe_allow_html=True)
            concs=data.get("key_conclusions",[]); concs_ar=(data.get("key_conclusions_ar") or [])+[""]*20
            for c3,c3_ar in zip(concs,concs_ar):
                st.markdown(f'<div style="padding:.18rem 0;font-size:.85rem;color:#64748b">✓ &nbsp;{c3}{" | "+c3_ar if c3_ar and show_ar else ""}</div>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

    # ── 5. FLASHCARDS ────────────────────────────────────────
    elif tool == "flashcards":
        st.markdown(f'<div class="tool-heading">🃏 {"البطاقات التعليمية" if ar_only else "Flashcards"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"بطاقات تفاعلية للمذاكرة — اقلب لترى الإجابة." if ar_only else "Interactive study cards — flip to reveal the answer."}</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: fc_type=st.selectbox("Type",["Definition","Concept","Formula & Application","Mixed"])
        with c2: fc_lvl =st.selectbox("Level",["Introductory","Intermediate","Advanced"])
        st.markdown(f'<div class="prompt-box"><div class="prompt-label">🎯 {"تعليمات — اختياري" if ar_only else "Instructions — Optional"}</div>',unsafe_allow_html=True)
        fc_cp=st.text_area("",height=80,label_visibility="collapsed",key="fc_cp",
            placeholder=("مثال: ركز على صيغ التعريف فقط..." if ar_only else "Example: Focus on formula cards with worked examples..."))
        st.markdown('</div>',unsafe_allow_html=True)

        if st.button("🃏 "+("توليد البطاقات" if ar_only else "Generate Flashcards"),type="primary",use_container_width=True):
            if not check_ready(): st.stop()
            se=st.empty(); pe=st.empty()
            try:
                prog(se,pe,"🧠 Creating cards…",40)
                fi=f"Focus: {focus_topic}." if focus_topic else ""
                fcp=f"\n\nLECTURER INSTRUCTIONS:\n{fc_cp.strip()}" if fc_cp and fc_cp.strip() else ""
                lang_fc="Write ALL text in Arabic only." if ar_only else "Write in English only."
                prompt=f"""Create {num_fc} study flashcards. {lang_fc} {fi} Type: {fc_type}. Level: {fc_lvl}.{fcp}
Never say "from the document". Write standalone academic content.
Use this EXACT format, separated by ===:

CARD: 1
TOPIC: topic name
FRONT: question or term the student must know
BACK: complete accurate answer with all key details
HINT: memory aid or key word
===
CARD: 2
TOPIC: topic name
FRONT: next question
BACK: complete answer
HINT: memory tip
===

Generate all {num_fc} cards. Make FRONT and BACK specific and detailed."""
                raw_fc=call_gemini(api_key,prompt,st.session_state.pdf_b64,tokens=5000,json_mode=False)
                prog(se,pe,"✅",90)
                cards_list=[]
                for block in raw_fc.split("==="):
                    block=block.strip()
                    if not block: continue
                    card={"num":len(cards_list)+1,"type":fc_type,"topic":"","front":"","back":"","hint":"","front_ar":"","back_ar":"","topic_ar":"","hint_ar":""}
                    for line in block.splitlines():
                        line=line.strip()
                        if not line or ":" not in line: continue
                        key,_,val=line.partition(":"); key=key.strip().upper(); val=val.strip()
                        if   key=="CARD":  card["num"]=int(val) if val.isdigit() else card["num"]
                        elif key=="TOPIC": card["topic"]=val
                        elif key=="FRONT": card["front"]=val
                        elif key=="BACK":  card["back"]=val
                        elif key=="HINT":  card["hint"]=val
                    if card.get("front") and card.get("back"): cards_list.append(card)
                data={"subject":"","subject_ar":"","cards":cards_list}
                st.session_state.fc_data=data; st.session_state.fc_idx=0; st.session_state.fc_show=False
                se.empty(); pe.empty()
            except Exception as e:
                se.empty(); pe.empty(); st.error(str(e))

        if st.session_state.fc_data:
            data=st.session_state.fc_data; cards=data.get("cards",[]); idx=st.session_state.fc_idx; show=st.session_state.fc_show
            if cards:
                card=cards[idx%len(cards)]; pct=int((idx+1)/len(cards)*100)
                top_ar=card.get("topic_ar","")
                st.markdown(f'<div class="pb"><div class="pf" style="width:{pct}%"></div></div>',unsafe_allow_html=True)
                st.markdown(f'<div style="text-align:center;font-size:.7rem;color:#4b5280;margin-bottom:.4rem">Card {idx+1}/{len(cards)} · {card.get("topic","")}{" | "+top_ar if top_ar and show_ar else ""} · <span style="color:#8b5cf6">{card.get("type","")}</span></div>',unsafe_allow_html=True)
                main_text=card.get("back","") if show else card.get("front","")
                main_ar  =card.get("back_ar","") if show else card.get("front_ar","")
                hint=card.get("hint","")
                st.markdown(f'<div class="fc"><div class="fc-lbl">{"✅ الإجابة" if show else "❓ السؤال"}</div><div class="fc-txt">{main_text}</div>{"<div class=\"fc-ar\">"+main_ar+"</div>" if main_ar and show_ar else ""}{"<div style=\"font-size:.7rem;color:#4b5280;margin-top:.6rem\">💡 "+hint+"</div>" if show and hint else ""}</div>',unsafe_allow_html=True)
                bc1,bc2,bc3,bc4=st.columns(4)
                with bc1:
                    if st.button("⬅️",use_container_width=True): st.session_state.fc_idx=max(0,idx-1); st.session_state.fc_show=False; st.rerun()
                with bc2:
                    if st.button("🔄 "+("اقلب" if ar_only else "Flip"),use_container_width=True,type="primary"): st.session_state.fc_show=not show; st.rerun()
                with bc3:
                    if st.button("➡️",use_container_width=True): st.session_state.fc_idx=min(len(cards)-1,idx+1); st.session_state.fc_show=False; st.rerun()
                with bc4:
                    if st.button("🔀",use_container_width=True):
                        random.shuffle(cards); st.session_state.fc_data["cards"]=cards; st.session_state.fc_idx=0; st.session_state.fc_show=False; st.rerun()
                # Audio
                read_txt=main_text
                st.markdown('<div style="margin:.4rem 0">'+make_audio_btn(read_txt,ar_only=ar_only,label_en="Read Card",label_ar="اقرأ البطاقة")+'</div>',unsafe_allow_html=True)
            txt=f"CAAWIYE FLASHCARDS\n{'='*40}\n\n"
            for c in cards:
                txt+=f"Card {c.get('num','')} — {c.get('topic','')}\nQ: {c.get('front','')}\nA: {c.get('back','')}\n💡 {c.get('hint','')}\n\n"
            st.download_button("⬇️ "+("تنزيل البطاقات" if ar_only else "Download Cards (.txt)"),data=txt.encode(),file_name="caawiye_flashcards.txt",mime="text/plain")
            with st.expander("📋 "+("عرض الكل" if ar_only else "View All Cards")):
                for c in cards:
                    with st.expander(f"Card {c.get('num','')} · {str(c.get('front',''))[:50]}"):
                        st.markdown(f"**Q:** {c.get('front','')}"); st.markdown(f"**A:** {c.get('back','')}")
                        if c.get("hint"): st.markdown(f"💡 *{c['hint']}*")

    # ── 6. QUIZ ──────────────────────────────────────────────
    elif tool == "quiz":
        st.markdown(f'<div class="tool-heading">🎯 {"اختبرني!" if ar_only else "Quiz Me!"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"أجب على الأسئلة ثم اضغط تسليم لترى نتيجتك الكاملة." if ar_only else "Answer questions then submit to get your full scored result with review."}</div>', unsafe_allow_html=True)
        c1q,c2q=st.columns(2)
        with c1q:
            num_quiz=st.slider("Questions",3,20,8)
            quiz_diff=st.selectbox("Difficulty",["Mixed","Easy","Medium","Hard"])
        with c2q:
            quiz_topic=st.text_input("Topic",placeholder="e.g. sampling methods" if not ar_only else "مثال: طرق أخذ العينات")

        if st.button("🎯 "+("توليد الاختبار" if ar_only else "Generate Quiz"),type="primary",use_container_width=True):
            if not check_ready(): st.stop()
            se=st.empty(); pe=st.empty()
            try:
                prog(se,pe,"🧠 "+("توليد الأسئلة…" if ar_only else "Generating quiz…"),40)
                lang_q="Write ALL text in Arabic only." if ar_only else "Write in English only."
                tf=f"Focus on: {quiz_topic}." if quiz_topic else ""
                qprompt=f"""Create {num_quiz}-question MCQ quiz. {tf}
{lang_q} Difficulty: {quiz_diff}.
4 options (A B C D), one correct. Never say "from the document".
Return raw JSON only:
{{"questions":[{{"num":1,"question":"text","options":{{"A":"...","B":"...","C":"...","D":"..."}},"correct":"A","explanation":"why A"}}]}}
Generate exactly {num_quiz} questions."""
                raw=call_gemini(api_key,qprompt,st.session_state.pdf_b64,tokens=4000)
                qdata=safe_parse(raw); st.session_state.quiz_data=qdata; st.session_state.quiz_answers={}; st.session_state.quiz_submitted=False
                se.empty(); pe.empty()
            except Exception as e:
                se.empty(); pe.empty(); st.error(str(e))

        if st.session_state.quiz_data and not st.session_state.quiz_submitted:
            qs=st.session_state.quiz_data.get("questions",[])
            st.markdown("---")
            for q in qs:
                qn=q.get("num",""); qtxt=q.get("question",""); opts=q.get("options",{})
                st.markdown(f'<div class="quiz-q"><span style="color:#8b5cf6;font-weight:700">Q{qn}.  </span><span style="color:#e8eaf0">{qtxt}</span></div>',unsafe_allow_html=True)
                chosen=st.radio(f"q{qn}",list(opts.keys()),format_func=lambda k,o=opts:f"{k})  {o[k]}",key=f"quiz_ans_{qn}",label_visibility="collapsed")
                if chosen: st.session_state.quiz_answers[str(qn)]=chosen
            st.markdown("---")
            answered=len(st.session_state.quiz_answers); total_q=len(qs)
            pct_done=int(answered/total_q*100) if total_q else 0
            st.markdown(f'<div class="pb"><div class="pf" style="width:{pct_done}%"></div></div>',unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:.74rem;color:#4b5280;text-align:center;margin-bottom:.75rem">{"أجبت على" if ar_only else "Answered"} {answered}/{total_q}</div>',unsafe_allow_html=True)
            if st.button("✅ "+("تسليم الاختبار" if ar_only else "Submit Quiz"),type="primary",use_container_width=True):
                st.session_state.quiz_submitted=True; st.rerun()

        elif st.session_state.quiz_data and st.session_state.quiz_submitted:
            qs=st.session_state.quiz_data.get("questions",[]); ans=st.session_state.quiz_answers
            score=sum(1 for q in qs if ans.get(str(q.get("num",""))) == q.get("correct",""))
            total=len(qs); pct=int(score/total*100) if total else 0
            grade=("ممتاز 🌟" if pct>=90 else "جيد جداً ✅" if pct>=75 else "جيد 👍" if pct>=60 else "تحتاج مراجعة 📚") if ar_only else \
                  ("Excellent 🌟" if pct>=90 else "Very Good ✅" if pct>=75 else "Good 👍" if pct>=60 else "Needs Review 📚")
            st.markdown(f'<div class="score-card"><div class="score-num">{pct}%</div><div class="score-label">{score}/{total} {"صحيح" if ar_only else "correct"}</div><div style="font-size:1.1rem;margin-top:.5rem;color:#e8eaf0;font-weight:600">{grade}</div></div>',unsafe_allow_html=True)
            # Audio score
            score_txt=f"Your score is {pct} percent. {score} out of {total} correct. {grade}"
            score_txt_ar=f"نتيجتك {pct} بالمئة. {score} من أصل {total} إجابة صحيحة."
            st.markdown('<div style="display:flex;justify-content:center;margin:.5rem 0">'+
                make_audio_btn(score_txt_ar if ar_only else score_txt,ar_only=ar_only,label_en="Hear Score",label_ar="استمع للنتيجة")+
                '</div>',unsafe_allow_html=True)
            st.markdown("### "+("مراجعة الإجابات" if ar_only else "Answer Review"))
            for q in qs:
                qn=str(q.get("num","")); qtxt=q.get("question",""); opts=q.get("options",{})
                correct=q.get("correct",""); chosen=ans.get(qn,""); exp=q.get("explanation","")
                is_right=chosen==correct
                border="rgba(16,185,129,.3)" if is_right else "rgba(239,68,68,.3)"
                icon="✅" if is_right else "❌"
                st.markdown(f'<div style="background:#1a1b27;border:1px solid {border};border-radius:10px;padding:.8rem 1rem;margin-bottom:.65rem"><div style="margin-bottom:.45rem"><span style="color:#8b5cf6;font-weight:700">{icon} Q{qn}.</span> <span style="color:#e8eaf0">{qtxt}</span></div>',unsafe_allow_html=True)
                for k,v in opts.items():
                    if k==correct:  col="#34d399"; bg="rgba(16,185,129,.09)";  tag=" ✓ "+("صحيح" if ar_only else "Correct")
                    elif k==chosen and k!=correct: col="#f87171"; bg="rgba(239,68,68,.07)"; tag=" ✗ "+("إجابتك" if ar_only else "Your answer")
                    else: col="#4b5280"; bg="transparent"; tag=""
                    st.markdown(f'<div style="padding:.23rem .55rem;border-radius:6px;background:{bg};color:{col};font-size:.82rem;margin-bottom:2px"><b>{k})</b> {v}{tag}</div>',unsafe_allow_html=True)
                if exp: st.markdown(f'<div class="mcq-exp">💡 {exp}</div>',unsafe_allow_html=True)
                st.markdown('</div>',unsafe_allow_html=True)
            col_r1,col_r2=st.columns(2)
            with col_r1:
                if st.button("🔄 "+("محاولة أخرى" if ar_only else "Try Again"),use_container_width=True):
                    st.session_state.quiz_answers={}; st.session_state.quiz_submitted=False; st.rerun()
            with col_r2:
                if st.button("🆕 "+("اختبار جديد" if ar_only else "New Quiz"),use_container_width=True):
                    st.session_state.quiz_data=None; st.session_state.quiz_answers={}; st.session_state.quiz_submitted=False; st.rerun()

    # ── 7. AI TUTOR ──────────────────────────────────────────
    elif tool == "qa":
        st.markdown(f'<div class="tool-heading">💬 {"المعلم الذكي" if ar_only else "AI Tutor"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="tool-subheading">{"اسأل أي سؤال عن ملف PDF — يجيب كمحاضر جامعي." if ar_only else "Ask anything about your PDF — answers like a university professor."}</div>', unsafe_allow_html=True)
        if not st.session_state.pdf_b64:
            st.warning("📄 "+("ارفع ملف PDF للبدء." if ar_only else "Upload a PDF to start chatting."))
        else:
            st.markdown(f'<div style="font-size:.75rem;color:#4b5280;margin-bottom:.45rem">{"أسئلة سريعة:" if ar_only else "Quick questions:"}</div>',unsafe_allow_html=True)
            qcols=st.columns(4)
            quick_qs=[("Summarise main topics","لخص الموضوعات"),("List all formulas","اذكر الصيغ"),("All definitions","التعريفات"),("Key conclusions","الاستنتاجات"),("Create study plan","خطة دراسة"),("Explain hardest concept","أصعب مفهوم"),("3 practice questions","3 أسئلة"),("Explain in Arabic","شرح عربي")]
            for i2,(qq_en,qq_ar) in enumerate(quick_qs):
                lbl=qq_ar if ar_only else qq_en
                with qcols[i2%4]:
                    if st.button(lbl,key=f"qq{i2}",use_container_width=True):
                        if api_key: st.session_state.chat.append({"role":"user","content":qq_ar if ar_only else qq_en})
            for msg in st.session_state.chat:
                if msg["role"]=="user":
                    st.markdown(f'<div class="qmsg quser"><div class="qlbl">{"أنت" if ar_only else "You"}</div>{msg["content"]}</div>',unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="qmsg qai"><div class="qlbl">🤖 Caawiye AI Tutor</div>{msg["content"]}</div>',unsafe_allow_html=True)
            if st.session_state.chat and st.session_state.chat[-1]["role"]=="user" and api_key:
                with st.spinner("🤖 "+("جاري التفكير…" if ar_only else "Thinking…")):
                    try:
                        history="\n".join([f"{'Student' if m['role']=='user' else 'Professor'}: {m['content']}" for m in st.session_state.chat[-6:]])
                        ar_instr="Answer in Arabic only." if ar_only else ""
                        prompt2=f"""You are an expert university professor and tutor.
Answer academically but clearly. Include formulas, examples, calculations where relevant.
Never say "from the document" — answer as a knowledgeable professor.
{ar_instr}
Conversation:\n{history}"""
                        response=call_gemini(api_key,prompt2,st.session_state.pdf_b64,tokens=1500,json_mode=False)
                        st.session_state.chat.append({"role":"assistant","content":response}); st.rerun()
                    except ValueError as e: st.error(str(e))
            c1i,c2i=st.columns([5,1])
            with c1i:
                user_input=st.text_input("",placeholder="اسأل أي سؤال…" if ar_only else "Ask anything about your document…",label_visibility="collapsed",key="ci")
            with c2i:
                send=st.button("📨",use_container_width=True,type="primary")
            if send and user_input.strip():
                if not api_key: st.warning("Enter API key.")
                else: st.session_state.chat.append({"role":"user","content":user_input.strip()}); st.rerun()
            if st.session_state.chat:
                if st.button("🗑️ "+("مسح" if ar_only else "Clear")):
                    st.session_state.chat=[]; st.rerun()
