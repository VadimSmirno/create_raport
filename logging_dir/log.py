import logging
from logging.handlers import RotatingFileHandler

FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
log_file = 'logging_dir/bot.log'
max_log_size = 50 * 1024 * 1024  # 50 МБ
file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=1,encoding='utf-8' )
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)








