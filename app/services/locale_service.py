from app.repositories import locale_repository

def get_localized_message(key: str, raw_lang: str | None) -> dict:
    lang = locale_repository.normalize_language(raw_lang)
    message = locale_repository.get_translation(key, lang)
    return {
        "key": key,
        "language": lang,
        "message": message
    }