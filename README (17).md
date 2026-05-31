# 🤖 Caawiye AI — Academic Platform
### كوييه — منصة الذكاء الاصطناعي الأكاديمية

> Built for university lecturers · Somalia & beyond

---

## What is Caawiye AI?

Upload any PDF lecture material and instantly get 7 powerful academic tools — in **English or Arabic**.

---

## 7 Tools

| Tool | Output | What it does |
|------|--------|-------------|
| 📊 **Lecture Slides** | `.pptx` | Premium slides with formulas, worked examples, real tables |
| ❓ **MCQ Generator** | `.docx` + 🔊 | MCQ with answers, explanations, audio read-aloud |
| 📝 **Exam Paper** | `.docx` | Full exam — MCQ, Short/Long Answer, Calculation, Matching. "Answer only X" per section |
| 📋 **Smart Summary** | `.docx` + 🔊 | Key concepts, terms, formulas, mind map. Audio listen |
| 🃏 **Flashcards** | `.txt` + 🔊 | Interactive flip cards with audio per card |
| 🎯 **Quiz Me!** | Scored | Quiz with instant marking, score card, audio score |
| 💬 **AI Tutor** | Chat | Ask any question — answers like a professor |

---

## Key Features

- ✅ Bilingual English / Arabic — fully separated, no mixing
- ✅ Visible input text — white text on dark backgrounds
- ✅ Audio buttons on MCQ, Summary, Flashcards, Quiz
- ✅ Custom instructions box on every tool
- ✅ Exam "Answer only X questions" per section
- ✅ Premium PPTX design — dark headers, gold accents, footer branding
- ✅ Real Word + PPTX tables with colored headers
- ✅ Auto rate-limit retry across 4 Gemini models
- ✅ Zero extra packages — only streamlit + requests

---

## Files

```
app.py            ← full platform
requirements.txt  ← streamlit + requests
README.md         ← this file
```

---

## Setup

**1. Get free Gemini API key**
https://aistudio.google.com/app/apikey — free, no credit card

**2. Deploy on Streamlit Cloud**
- Push all 3 files to a GitHub repo
- Go to share.streamlit.io → New app → select repo → main file: app.py → Deploy

---

## requirements.txt content

```
streamlit
requests
```

No version pins — Streamlit Cloud uses its pre-installed versions.

---

*Caawiye AI — Knowledge for everyone · كوييه — المعرفة للجميع*
