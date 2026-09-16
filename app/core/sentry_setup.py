import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from app.config import settings


def init_sentry(extra_integrations: list | None = None):
    if not settings.sentry_dsn:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        integrations=[
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
            *(extra_integrations or []),
        ],
        traces_sample_rate=0.2,
        send_default_pii=False,
    )