import logging

FORMAT = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(FORMAT)
console_handler1 = logging.StreamHandler()
console_handler1.setFormatter(formatter)
logger.addHandler(console_handler1)







