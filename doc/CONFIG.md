# Build the Docker Image for Google Cloud Platform

gcloud builds submit --tag gcr.io/recipe-quality-validator/recipe-validator

# Deploy to Google Cloud Platform (Cloud Run)

gcloud run deploy recipe-validator \
--image gcr.io/recipe-quality-validator/recipe-validator \
--platform managed \
--region europe-west1 \
--allow-unauthenticated \
--memory 2Gi \
--port 8080 \
--min-instances=1 \
--set-env-vars="LLM_BACKEND=GEMINI" \
--set-secrets="GEMINI_STUDIO_API_KEY=gemini-api-key:latest"

# Manual commit to RazumAI-ch

git push origin main
git push public main
