import logging

from pythonjsonlogger import jsonlogger

log_handler = logging.StreamHandler()
log_handler.setFormatter(
    jsonlogger.JsonFormatter(  # type: ignore[no-untyped-call]
        rename_fields={"levelname": "severity"},
        fmt="%(name)s %(threadName) %(message)s '%(asctime)s %(levelname)",
    )
)
logger = logging.getLogger("offchain")
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)
