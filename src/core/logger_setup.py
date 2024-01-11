import logging
import logging.handlers

import logstash
import sentry_sdk
import structlog
from sentry_sdk.integrations.fastapi import FastApiIntegration


def configure_structlog(
    logstash_level: str,
    console_logging_level: str,
    logstash_host: str,
    logstash_port: int,
):
    sentry_sdk.init(integrations=[FastApiIntegration()])
    logging.getLogger("uvicorn.access").disabled = True
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        # context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer(),
            ],
            keep_exc_info=True,
            keep_stack_info=True,
        ),
    )
    stream_handler.setLevel(console_logging_level)

    app_logger = logging.getLogger()
    app_logger.addHandler(stream_handler)
    app_logger.setLevel(logging.DEBUG)

    logstash_handler = logstash.UDPLogstashHandler(logstash_host, logstash_port)
    logstash_handler.setLevel(logstash_level)
    app_logger.addHandler(logstash_handler)
