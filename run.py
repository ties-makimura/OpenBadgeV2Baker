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

logger.info('start logging.info()')
logger.error('start logging.error()')

ControlCenter()

logger.info('End logging.info()')
logger.error('End logging.error()')
