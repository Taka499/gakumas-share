"""SuperTokens initialisation helpers."""

from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.recipe import session

from .config import Settings

_initialised = False


def init_supertokens(settings: Settings) -> None:
    """Initialise the SuperTokens SDK if it hasn't been initialised yet."""

    global _initialised
    if _initialised:
        return

    init(
        app_info=InputAppInfo(
            app_name="Gakumas Share",
            api_domain=str(settings.api_base_url),
            website_domain=str(settings.web_app_url),
            api_base_path="/api/auth",
            website_base_path="/",
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=str(settings.supertokens_core_url),
            api_key=settings.supertokens_core_api_key,
        ),
        framework="fastapi",
        recipe_list=[
            session.init(
                anti_csrf="VIA_TOKEN",
                cookie_same_site="lax",
                cookie_secure=settings.cookie_secure,
            )
        ],
    )

    _initialised = True
