#!/usr/bin/python3
# -*- encoding: UTF-8 -*-
# vim: fileencode=utf-8

"""
実行用
"""

from BakeBadgeV2 import setup_logger
from BakeBadgeV2 import ControlCenter




# 各モジュールの最初のほうで、グローバルに宣言しておく
logger = setup_logger(__name__)

logger.info('hoge')
logger.error('logfile:moge')

# def _init_logger():
#     logger = logging.getLogger('run')  #1
#     logger.setLevel(logging.INFO)  #2
#     handler = logging.StreamHandler(sys.stderr)  #3
#     handler.setLevel(logging.INFO)  #4
#     formatter = logging.Formatter(  
#            '%(asctime)s:LEVEL:%(levelname)s:FILENAME:%(name)s:MODULENAME:%(module)s:MESSAGE:%(message)s') #5
#     handler.setFormatter(formatter)  #6
#     logger.addHandler(handler)  #7
    


# _init_logger()
# _logger = logging.getLogger('run.py')
# _logger.info('python script started in %s', os.getcwd())

ControlCenter()


