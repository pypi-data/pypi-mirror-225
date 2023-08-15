# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 09:20
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : hostManagerControl.py
from typing import List
from ultipa.types import ULTIPA
from ultipa.connection.hostManager import HostManager

RAFT_GLOBAL = "global"

class HostManagerControl:
	initHost: str = None
	username: str = None
	password: str = None
	crt: str = None
	allHostManager: dict = {}
	consistency: bool = False

	def __init__(self, initHost: str, username: str, password: str, maxRecvSize: int = -1, crt: str = None,
				 consistency: bool = False):
		self.initHost = initHost
		self.username = username
		self.password = password
		self.maxRecvSize = maxRecvSize
		self.consistency = consistency
		self.crt = crt
		self.allHostManager = {}

	def chooseClientInfo(self, type: int, uql: str, graphSetName: str, useHost: str = None, useMaster: bool = False):
		hostManager = self.getHostManger(graphSetName)
		return hostManager.chooseClientInfo(type, uql, consistency=self.consistency,
											useHost=useHost, useMaster=useMaster)

	def upsetHostManger(self, graphSetName: str, initHost: str):
		hostManager = HostManager(graphSetName=graphSetName, host=initHost, username=self.username,
								  password=self.password, crt=self.crt, maxRecvSize=self.maxRecvSize)
		self.allHostManager[graphSetName] = hostManager
		return hostManager

	def getHostManger(self, graphSetName: str):
		hostManager = self.allHostManager.get(graphSetName)
		if not hostManager:
			hostManager = self.upsetHostManger(graphSetName=graphSetName, initHost=self.initHost)
		return hostManager

	def getAllHosts(self):
		hostManager = self.getHostManger(RAFT_GLOBAL)
		return hostManager.getAllHosts()

	def getAllClientInfos(self, graph):
		return self.getHostManger(graph).getAllClientInfos(ignoreAlgo=True)

	def getAllHostStatusInfo(self, graph):
		all: List[ULTIPA.RaftPeerInfo] = []
		all.extend(self.getHostManger(graph).followersPeerInfos)
		all.append(self.getHostManger(graph).leaderInfos)
		return all