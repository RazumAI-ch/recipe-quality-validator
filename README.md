# 🧪 OpenAI Healthcare Recipe Quality Validator  
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)  
[![Docker Hub](https://img.shields.io/docker/pulls/igorrazumny/openai-recipe-quality-validator?style=flat-square)](https://hub.docker.com/r/igorrazumny/openai-recipe-quality-validator)

Audits healthcare recipes using OpenAI or custom LLMs and generates a PDF report with findings.

---

## 🚀 Features

- ✅ Upload JSON or CSV recipe files  
- ✅ Analyze structure, completeness, and formatting  
- ✅ Get a downloadable PDF audit report  
- ✅ Switch between OpenAI and Azure (Portkey) backends  
- ✅ Limit entries or audit the full dataset with cost estimation  
- ✅ Automatically categorize deviations by severity (Critical, Moderate, Minor)

---

## ⚙️ Local Setup

```bash
git clone https://github.com/igorrazumny/openai-recipe-quality-validator.git
cd openai-recipe-quality-validator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --break-system-packages
```

---

### 🔐 Environment Configuration

You must create either a `.env.openai` **or** a `.env.internal` file in the project root, depending on which backend you want to use.

> ⚠️ Only one backend is active at a time — if you're using `.env.openai`, then `.env.internal` will be ignored (and vice versa).

#### 👉 Use `.env.openai` if:

You want to connect **directly to OpenAI APIs** using your own API key.

```env
LLM_BACKEND=OPENAI
OPENAI_API_KEY=sk-...
MAX_ENTRIES=100
```

#### 👉 Use `.env.internal` if:

You want to route requests through an **intermediate API layer** like **Portkey**, for example with Azure OpenAI.

```env
LLM_BACKEND=INTERNAL
INTERNAL_API_PORT_KEY=your-portkey-api-key
INTERNAL_API_URL=https://your-azure-api-endpoint
PORTKEY_VIRTUAL_KEY=default-azure-v-xxxxxx
PORTKEY_PROVIDER=azure-openai
PORTKEY_RETRY_ATTEMPTS=5
MAX_ENTRIES=100
```

You do **not** need to configure both files.  
Just pick one — the app will ignore the other.

Then run the app:

```bash
# Optional: choose which env file to use (default is .env.openai)
export ENV_MODE=openai  # or 'internal'
streamlit run src/app.py
```

---

## 🐳 Docker Setup

You can run the app entirely in Docker without installing local dependencies.

### 1. Prepare your environment config

Create either `.env.openai` or `.env.internal` in the project root, as shown above.

### 2. Build the image

```bash
docker build -t igorrazumny/openai-recipe-quality-validator .
```

### 3. Run with Docker Compose

```bash
docker-compose up
```

Then open your browser: [http://localhost:8501](http://localhost:8501)

---

## 📦 Prebuilt Docker Image

You can skip local builds and run the app directly using the prebuilt Docker Hub image:

```bash
docker pull igorrazumny/openai-recipe-quality-validator:latest
docker run --env-file .env.openai -p 8501:8501 igorrazumny/openai-recipe-quality-validator:latest
```

> Use `.env.internal` instead of `.env.openai` if you're routing through Portkey.

---

## 📁 Project Structure

```
.
├── public_assets/         # Sample data files and logos
├── src/
│   ├── app.py             # Main Streamlit app
│   ├── audit.py           # Core LLM audit logic
│   ├── audit_runner.py    # Orchestration and PDF generation
│   ├── controls.py        # Sidebar controls
│   ├── layout.py          # UI layout and download links
│   └── utils.py           # Helpers (e.g., JSON parsing, hashing)
├── .env.example           # Sample config file
├── .gitignore
├── .pre-commit hook       # Prevents secrets from being committed
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧪 Developer Checklist

- [x] Clone the repo
- [x] Create `.env.openai` or `.env.internal`
- [x] Add your OpenAI or Azure API key
- [x] Run locally with Docker:
  ```bash
  docker-compose up
  ```
- [x] Use `.gitignore` to keep secrets out of version control
- [x] ✅ Pre-commit hook blocks commits with `sk-...` keys

---

## ⚙️ CI/CD Notes

A GitHub Actions workflow for automatic Docker builds can be added to publish to Docker Hub on every push to `main`.

---

⚠️ This is a portfolio demonstration project built with mock data only.  
It is not affiliated with any employer, client, or production system.  
No confidential or proprietary information is included.
