import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"
DEFAULT_LANGUAGE = "en"


def _load_json(file_path: Path) -> dict:
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Aliases eşlemelerini yükle
LANGUAGE_ALIASES: dict[str, str] = _load_json(LOCALES_DIR / "aliases.json")


# "locales/" altındaki aliases.json hariç tüm dil dosyalarını dinamik oku
def _load_all_translations() -> dict[str, dict[str, str]]:
    translations = {}
    if LOCALES_DIR.exists():
        for file_path in LOCALES_DIR.glob("*.json"):
            if file_path.name == "aliases.json":
                continue
            lang_code = file_path.stem  # Örn: "tr.json" -> "tr"
            translations[lang_code] = _load_json(file_path)
    return translations


TRANSLATIONS = _load_all_translations()


def normalize_language(raw_lang: str | None) -> str:
    if not raw_lang:
        return DEFAULT_LANGUAGE

    primary_lang = raw_lang.split(",")[0].split(";")[0].strip().lower()
    return LANGUAGE_ALIASES.get(primary_lang, DEFAULT_LANGUAGE)


def get_translation(key: str, lang: str) -> str:
    # 1. İstenen dil dosyasında key'i ara
    lang_dict = TRANSLATIONS.get(lang)
    if lang_dict and key in lang_dict:
        return lang_dict[key]

    # 2. Bulunamazsa varsayılan dilde (en) ara (Fallback)
    default_dict = TRANSLATIONS.get(DEFAULT_LANGUAGE, {})
    return default_dict.get(key, "Message not found")