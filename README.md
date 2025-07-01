# 🧪 OpenAI Healthcare Recipe Quality Validator

This Streamlit app audits healthcare manufacturing recipes using OpenAI GPT-4o or your own internal LLM backend. After
analysis, it generates a downloadable PDF report with findings and suggestions.

## 🚀 Features

- ✅ Upload JSON or CSV recipe files
- ✅ Analyze structure, completeness, and formatting
- ✅ Get a downloadable PDF audit report
- ✅ Switch between OpenAI and Azure (Portkey) backends
- ✅ Limit entries or audit the full dataset with cost estimation
- ✅ Automatically categorizes deviations by severity (Critical, Moderate, Minor)

---

## ⚙️ Setup (Local)

```bash
git clone https://github.com/your-username/openai-recipe-quality-validator.git
cd openai-recipe-quality-validator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --break-system-packages
```

### Environment Configuration

Create one of the following `.env` files in the project root:

#### Example `.env.openai`

```env
LLM_BACKEND=OPENAI
OPENAI_API_KEY=sk-...
MAX_ENTRIES=100
```

#### Example `.env.internal`

```env
LLM_BACKEND=INTERNAL
INTERNAL_API_PORT_KEY=your-portkey-api-key
INTERNAL_API_URL=https://your-azure-api-endpoint
PORTKEY_VIRTUAL_KEY=default-azure-v-xxxxxx
PORTKEY_PROVIDER=azure-openai
PORTKEY_RETRY_ATTEMPTS=5
MAX_ENTRIES=100
```

Then run:

```bash
# Set which environment config to load (default is 'openai')
export ENV_MODE=openai  # or 'internal'
streamlit run src/app.py
```

---

## 🐳 Running with Docker

To build and run the app with Docker:

### 1. Create a `.env.openai` or `.env.internal` file as shown above

Then build and run:

```bash
# Build Docker image
docker build -t recipe-validator .

# Run container (OpenAI mode)
docker run --env ENV_MODE=openai --env-file .env.openai -p 8501:8501 recipe-validator
```

You can access the app at: [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure

```
.
├── src/
│   ├── app.py              # Main Streamlit app
│   ├── audit.py            # Core LLM audit logic
│   ├── audit_runner.py     # Orchestration and PDF generation
│   ├── controls.py         # Sidebar controls
│   ├── layout.py