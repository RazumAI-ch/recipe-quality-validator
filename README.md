# 🧪 Gemini Healthcare Recipe Quality Validator

[![Docker Hub](https://img.shields.io/docker/pulls/igorrazumny/recipe-quality-validator?style=flat-square)](https://hub.docker.com/r/igorrazumny/recipe-quality-validator)

A containerized Streamlit app that audits healthcare manufacturing recipes using Gemini or Portkey-based LLMs.  
Each commit triggers a GitHub Actions build and push to Docker Hub with multi-platform support (arm64 + amd64).

---

## ✅ Highlights

1. **Upload JSON or CSV recipe files**
2. **Audit using Gemini or Azure via Portkey**
3. **Flag structure, formatting, and completeness issues**
4. **Categorize deviations by severity (Critical, Moderate, Minor)**
5. **Download PDF audit reports**
6. **Prebuilt Docker image for Apple Silicon & Intel**
7. **Runs locally or from [Docker Hub](https://hub.docker.com/r/igorrazumny/openai-recipe-quality-validator)**

---


---

## 🔐 .env Config

Use either `.env.gemini` or `.env.internal` — only one is loaded:

---

⚠️ Demo project using synthetic data. No proprietary information included.
