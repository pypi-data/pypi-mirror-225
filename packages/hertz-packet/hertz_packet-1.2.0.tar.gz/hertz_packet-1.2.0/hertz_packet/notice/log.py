# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : log.py
@Date    : 2023/5/19 17:56:47
@Author  : zhchen
@Desc    : 
"""
import logging
import os
import sys
from datetime import datetime


class Logger:
    def __init__(self, log_path=None, file_name=None):
        self.logger = logging.getLogger(__name__)  # 创建日志记录器
        self.logger.setLevel(logging.INFO)  # 日志记录器的等级

        _format = logging.Formatter('%(asctime)s [%(filename)s] %(levelname)s: %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')

        file_name_date = datetime.now().strftime("%H_%M_%S")
        filename = file_name or f"{os.path.basename(sys.argv[0]).split('.')[0]}_{file_name_date}.log"
        path_name_date = datetime.now().strftime("%Y_%m_%d")
        log_path = log_path or f'./log/{path_name_date}'
        os.path.exists(log_path) or os.makedirs(log_path)
        file_handler = logging.FileHandler(f"{log_path}/{filename}", encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(_format)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger
