import joblib

from app.config import settings


try:
    model = joblib.load(settings.MODEL_PATH)
except Exception:
    model = None
