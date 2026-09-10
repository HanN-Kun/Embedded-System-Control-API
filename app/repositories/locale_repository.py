import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"

def _load_json(filename: str) -> dict:
    file_path = LOCALES_DIR / filename
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

TRANSLATIONS: dict[str, dict[str, str]] = _load_json("translations.json")
LANGUAGE_ALIASES: dict[str, str] = _load_json("aliases.json")
DEFAULT_LANGUAGE = "en"

def normalize_language(raw_lang: str | None) -> str:
    if not raw_lang:
        return DEFAULT_LANGUAGE

    # Accept-Language header'ındaki öncelikli dili ayıklar (Örn: "tr-TR,tr;q=0.9" -> "tr-tr")
    primary_lang = raw_lang.split(",")[0].split(";")[0].strip().lower()
    
    return LANGUAGE_ALIASES.get(primary_lang, DEFAULT_LANGUAGE)

def get_translation(key: str, lang: str) -> str:
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang) or entry.get(DEFAULT_LANGUAGE) or "Message not found"