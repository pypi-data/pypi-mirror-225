__all__ = ["get_logger"]

from api_compose.core.logging.adapter import LoggerAdapter
from api_compose.core.utils.settings import GlobalSettings


def get_logger(
        name: str,
        overwrite=True,
) -> LoggerAdapter:
    log_file_path = GlobalSettings.get().LOG_FILE_PATH
    logger_level = GlobalSettings.get().LOGGER_LEVEL
    return LoggerAdapter(name=name, log_file_path=log_file_path, overwrite=overwrite, logger_level=logger_level)
