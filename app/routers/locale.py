from fastapi import APIRouter, Header, Query
from app.schemas.locale import LocalizedMessageResponse
from app.services import locale_service

router = APIRouter(prefix="/localization", tags=["Localization"])

@router.get("/{message_key}", response_model=LocalizedMessageResponse)
def get_localized_message(
    message_key: str,
    lang: str | None = Query(default=None, description="Dil kodu (örn: ?lang=tr)"),
    accept_language: str | None = Header(default=None, alias="Accept-Language"),
):
    requested_lang = lang or accept_language
    return locale_service.get_localized_message(message_key, requested_lang)