import logging
from logging.config import dictConfig
from pathlib import Path
from typing import Any


def get_logging_config(
        log_level: str = "INFO",
        log_name: str = "app.log",
        log_dir: str = "logs",
        console_output: bool = True
) -> dict[str, Any]:
    """获取日志配置字典"""
    # 创建logs目录
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": log_dir / log_name,
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5,
                "encoding": "utf-8"
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "multitool_office_ai": {
                "level": log_level,
                "handlers": ["file"] if not console_output else ["file", "console"],
                "propagate": False
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["file"] if not console_output else ["file", "console"]
        }
    }

    return config


def setup_logging(
        log_level: str = "INFO",
        log_file: str = "app.log",
        log_dir: str = "logs",
        console_output: bool = True
):
    """使用dictConfig配置日志"""
    config = get_logging_config(log_level, log_file, log_dir, console_output)
    logging.config.dictConfig(config)
