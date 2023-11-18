import uvicorn

from reworkd_platform.settings import settings


def ssl_key_path() -> str:
    return settings.ssl_key_path


def ssl_cert_path() -> str:
    return settings.ssl_cert_path


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "reworkd_platform.web.application:get_app",
        workers=settings.workers_count,
        ssl_keyfile=ssl_key_path(),
        ssl_certfile=ssl_cert_path(),
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        factory=True
    )


if __name__ == "__main__":
    main()
