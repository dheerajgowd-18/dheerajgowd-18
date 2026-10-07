<div align="center">

<h3><code>dheeraj@github ~ $ ./contributions.sh</code></h3>

<img src="./contrib-heatmap.svg" width="860" alt="Animated contribution heatmap for the last year" />

<br><br>

<h3><code>dheeraj@github ~ $ whoami</code></h3>

<table>
  <tr>
    <td valign="top"><img src="./dheeraj-ascii.svg" width="370" alt="Animated ASCII portrait" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" alt="AI engineer profile card" /></td>
  </tr>
</table>

<br>

</div>

---

## Dheeraj Gowd

**B.Tech CSE · AI / GenAI Engineer in progress**  
Building practical LLM applications, RAG systems, and agentic workflows with Python.

### What I build

- **Enterprise Agentic RAG** — a production-oriented RAG pipeline with guardrails, retrieval, routing, and evaluation.
- **Verified Research Agent** — a domain-agnostic LangChain + LangGraph research workflow designed for traceable, defensible answers.
- **NEXORA 2026** — a leakage-safe predictive-maintenance pipeline that turns large-scale telemetry into weekly high-yield dispatch predictions.

### Current focus

`Python` · `FastAPI` · `LangChain` · `LangGraph` · `RAG` · `Embeddings` · `Vector Search` · `LLM Applications`

### Selected projects

- [Enterprise Agentic RAG](https://github.com/dheerajgowd-18/agentic-rag)
- [NEXORA 2026](https://github.com/dheerajgowd-18/lpdg-nexora-2026)
- [Vireo Audio Support Intelligence](https://github.com/dheerajgowd-18/vireo-audio)

---

<details>
<summary><b>How this profile art works</b></summary>

<br>

Everything at the top is generated locally as self-contained SVG assets. The README is only the layout layer; the animations live inside the SVG files.

| File | Generator | Refresh |
| --- | --- | --- |
| `contrib-heatmap.svg` | `fetch_contributions.py` → `render_heatmap_svg.py` | daily via GitHub Actions |
| `dheeraj-ascii.svg` | `prep_photo.py` → `make_ascii_svg.py` | when the photo changes |
| `info-card.svg` | `make_info_card.py` | when profile details change |

Contribution data is read from GitHub's public contribution-calendar HTML endpoint. No personal access token is required by this workflow. GitHub documents the contribution calendar as the public visual record of profile contributions. See [GitHub profile contributions](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile).

### Local commands

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -r scripts/requirements.txt
pip install -r scripts/requirements-portrait.txt

# contribution graph
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py

# profile card
python scripts/make_info_card.py

# portrait: add your own source-photo.jpg first
python scripts/prep_photo.py source-photo.jpg --aspect 1.59
python scripts/make_ascii_svg.py
```

Use `STATIC=1` when you want a frozen SVG for local previews.

</details>
