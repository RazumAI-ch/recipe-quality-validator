 # 🧪 OpenAI Healthcare Recipe Quality Validator  
[![Docker Hub](https://img.shields.io/docker/pulls/igorrazumny/openai-recipe-quality-validator?style=flat-square)](https://hub.docker.com/r/igorrazumny/openai-recipe-quality-validator)

A containerized Streamlit app that audits healthcare manufacturing recipes using OpenAI or Portkey-based LLMs.  
Each commit triggers a GitHub Actions build and push to Docker Hub with multi-platform support (arm64 + amd64).

---

## ✅ Highlights

1. **Upload JSON or CSV recipe files**
2. **Audit using OpenAI GPT or Azure via Portkey**
3. **Flag structure, formatting, and completeness issues**
4. **Categorize deviations by severity (Critical, Moderate, Minor)**
5. **Download PDF audit reports**
6. **Prebuilt Docker image for Apple Silicon & Intel**
7. **Runs locally or from [Docker Hub](https://hub.docker.com/r/igorrazumny/openai-recipe-quality-validator)**

---

## 🐳 Run from Docker Hub

```bash
docker run --env-file .env.openai -p 8501:8501 igorrazumny/openai-recipe-quality-validator
```

---

## ⚙️ Local Dev

```bash
git clone https://github.com/igorrazumny/openai-recipe-quality-validator.git
cd openai-recipe-quality-validator
docker-compose up
```

---

## 🔐 .env Config

Use either `.env.openai` or `.env.internal` — only one is loaded:

```env
# .env.openai
LLM_BACKEND=OPENAI
OPENAI_API_KEY=sk-...
MAX_ENTRIES=100
```

---

⚠️ Demo project using synthetic data. No proprietary information included.
