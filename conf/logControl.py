#coding=utf-8
####定义单例的日志logger模块
import sys
import os
sys.path.append("..")
import  logging
import logging.config
class logControl:
	print os.path.join(os.path.dirname(os.path.abspath(__file__)),"logger.conf")
	logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)),"logger.conf"))
	##create logger
	def getLogger(self):
		logger = logging.getLogger('run')
		return logger