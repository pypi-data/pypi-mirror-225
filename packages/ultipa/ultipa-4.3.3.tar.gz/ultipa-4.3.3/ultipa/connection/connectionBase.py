# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 09:20
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : connectionBase.py

import logging
import time
import schedule
from ultipa import ParameterException
from ultipa.connection.clientInfo import ClientInfo
from ultipa.connection.clientType import ClientType
from ultipa.connection.hostManagerControl import HostManagerControl, RAFT_GLOBAL
from ultipa.connection.uqlHelper import UQLHelper
from ultipa.proto import ultipa_pb2
from ultipa.types.types import UltipaConfig
from ultipa.types.types_response import PropertyTable
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.common import GETLEADER_TIMEOUT
from ultipa.utils.convert import convertTableToDict, convertToListAnyObject
from ultipa.utils.format import FormatType
from ultipa.utils.logger import LoggerConfig
from ultipa.types import ULTIPA, ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.utils.ultipaSchedule import run_continuously

class ConnectionBase:
	hostManagerControl: HostManagerControl
	username: str
	password: str
	crtPath: str
	defaultConfig: UltipaConfig
	runSchedule: object = None

	def __init__(self, host: str, defaultConfig: UltipaConfig, crtFilePath: str = None):
		self.host = host
		self.username = defaultConfig.username
		self.password = defaultConfig.password
		self.crtPath = crtFilePath
		self.defaultConfig = defaultConfig
		self.crt = None
		if crtFilePath:
			try:
				with open(f'{crtFilePath}', 'rb') as f:
					self.crt = f.read()
			except Exception as e:
				raise ParameterException(err=e)
		self.hostManagerControl = HostManagerControl(self.host, self.username, self.password,
													 self.defaultConfig.maxRecvSize, self.crt,
													 consistency=defaultConfig.consistency)

		self.defaultConfig.defaultGraph = defaultConfig.defaultGraph or "default"
		self.defaultConfig.timeoutWithSeconds = defaultConfig.timeoutWithSeconds or 15
		self.defaultConfig.responseWithRequestInfo = defaultConfig.responseWithRequestInfo or False
		self.defaultConfig.consistency = defaultConfig.consistency
		self.graphSetName = self.defaultConfig.defaultGraph
		self.count = 0

		if not self.defaultConfig.uqlLoggerConfig and self.defaultConfig.Debug:
			self.defaultConfig.uqlLoggerConfig = LoggerConfig(name="ultipa", fileName="",
															  isStream=self.defaultConfig.Debug, isWriteToFile=False,
															  level=logging.INFO)

	def getGraphSetName(self, currentGraphName: str, uql: str = "", isGlobal: bool = False):
		if isGlobal:
			return RAFT_GLOBAL
		if uql:
			parse = UQLHelper(uql)
			if parse.uqlIsGlobal():
				return RAFT_GLOBAL
			c1 = parse.parseRet.getFirstCommands()
			c2 = f"{c1}().{parse.parseRet.getSecondCommands()}"
			if c2 in [CommandList.mount, CommandList.unmount, CommandList.truncate]:
				graphName = parse.parseRet.getCommandsParam(1)
				if graphName:
					return graphName
		return currentGraphName or self.defaultConfig.defaultGraph

	def getTimeout(self, timeout: int):
		return timeout or self.defaultConfig.timeoutWithSeconds

	def getClientInfo(self, clientType: int = ClientType.Default, graphSetName: str = '', uql: str = '',
					  isGlobal: bool = False, ignoreRaft: bool = False, useHost: str = None, useMaster: bool = False,
					  timezone=None, timeZoneOffset=None):
		goGraphName = self.getGraphSetName(currentGraphName=graphSetName, uql=uql, isGlobal=isGlobal)
		if not ignoreRaft and not self.hostManagerControl.getHostManger(goGraphName).raftReady:
			refreshRet = self.refreshRaftLeader(self.hostManagerControl.initHost,
												ULTIPA_REQUEST.RequestConfig(graphName=goGraphName))
			self.hostManagerControl.getHostManger(goGraphName).raftReady = refreshRet

		clientInfo = self.hostManagerControl.chooseClientInfo(type=clientType, uql=uql, graphSetName=goGraphName,
															  useHost=useHost, useMaster=useMaster)
		metadata = clientInfo.getMetadata(goGraphName, timezone, timeZoneOffset)
		return ClientInfo(Rpcsclient=clientInfo.Rpcsclient, Controlsclient=clientInfo.Controlsclient, metadata=metadata,
						  graphSetName=goGraphName, host=clientInfo.host)



	def getRaftLeader(self, requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()):
		resRaftLeader = self.__autoGetRaftLeader(host=self.host, requestConfig=requestConfig)
		RaftStatus = FormatType.getRaftStatus(resRaftLeader)
		return ULTIPA_RESPONSE.Response(RaftStatus)

	def __getRaftLeader(self, requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()):
		if requestConfig == None:
			graphSetName = None
		else:
			if not requestConfig.graphName:
				graphSetName = 'default'
			else:
				graphSetName = requestConfig.graphName

		clientInfo = self.getClientInfo(clientType=ClientType.Leader, graphSetName=graphSetName, ignoreRaft=True,
										useMaster=requestConfig.useMaster)
		res = clientInfo.Controlsclient.GetLeader(ultipa_pb2.GetLeaderRequest(), metadata=clientInfo.metadata,
												  timeout=GETLEADER_TIMEOUT)

		return FormatType.Response(_res=res, host=self.host)

	def __autoGetRaftLeader(self, host: str, requestConfig: ULTIPA_REQUEST.RequestConfig, retry=0):
		'''内部用，所以返回值自定义'''
		conn = ConnectionBase(host=host, crtFilePath=self.crtPath, defaultConfig=self.defaultConfig)
		try:
			res = conn.__getRaftLeader(requestConfig)
		except Exception as e:
			self.hostManagerControl.initHost = ""
			if host in self.defaultConfig.hosts:
				self.defaultConfig.hosts.remove(host)
			return {
				"code": ULTIPA.Code.FAILED,
				"message": str(e._state.code) + ' : ' + str(e._state.details)
			}
		status = res.status
		if status.code == ULTIPA.Code.SUCCESS:
			# status.clusterInfo.raftPeers.remove(host)  # 不要主节点
			self.hostManagerControl.initHost = host
			for i in status.clusterInfo.raftPeers:
				if i.host == host:
					status.clusterInfo.raftPeers.remove(i)
			return {
				"code": status.code,
				"message": status.message,
				'leaderHost': host,
				"followersPeerInfos": list(filter(lambda x: x != host, status.clusterInfo.raftPeers)),
				"leaderInfos": status.clusterInfo.leader,
			}
		elif status.code == ULTIPA.Code.NOT_RAFT_MODE:
			return {
				"code": status.code,
				"message": status.message,
				"leaderHost": host,
				"followersPeerInfos": [],
				"leaderInfos": status.clusterInfo.leader
			}
		elif status.code in [ULTIPA.Code.RAFT_REDIRECT, ULTIPA.Code.RAFT_LEADER_NOT_YET_ELECTED,
							 ULTIPA.Code.RAFT_NO_AVAILABLE_FOLLOWERS, ULTIPA.Code.RAFT_NO_AVAILABLE_ALGO_SERVERS]:
			if retry > 2:
				return {
					"code": status.code,
					"message": status.message,
					"redirectHost": res.status.clusterInfo.redirect
				}
			if status.code != ULTIPA.Code.RAFT_REDIRECT:
				time.sleep(0.3)
			if status.code == ULTIPA.Code.RAFT_REDIRECT:
				host = res.status.clusterInfo.redirect
			return self.__autoGetRaftLeader(host=host, requestConfig=requestConfig, retry=retry + 1)

		return {
			"code": status.code,
			"message": status.message
		}

	def refreshRaftLeader(self, redirectHost: str, requestConfig: ULTIPA_REQUEST.RequestConfig):
		# hosts = [redirectHost] if redirectHost else self.hostManagerControl.getAllHosts()
		hosts = [redirectHost] if redirectHost else []
		goGraphName = self.getGraphSetName(requestConfig.graphName)

		for h in self.defaultConfig.hosts:
			if h not in hosts:
				hosts.append(h)
		for host in hosts:
			resRaftLeader = self.__autoGetRaftLeader(host=host, requestConfig=requestConfig)
			code = resRaftLeader["code"]
			if code == ULTIPA.Code.SUCCESS:
				leaderHost = resRaftLeader["leaderHost"]
				followersPeerInfos = resRaftLeader["followersPeerInfos"]
				leaderInfos = resRaftLeader["leaderInfos"]
				hostManager = self.hostManagerControl.upsetHostManger(goGraphName, leaderHost)
				hostManager.setClients(leaderHost=leaderHost, followersPeerInfos=followersPeerInfos,
									   leaderInfos=leaderInfos)
				return True
		# elif code == ULTIPA.Code.RAFT_REDIRECT:
		# 	return False
		return False

	def stopConnectionAlive(self):
		if self.runSchedule != None:
			self.runSchedule.set()

	def keepConnectionAlive(self, timeIntervalSeconds: int = None):
		timeIntervalSeconds = self.defaultConfig.heartBeat if timeIntervalSeconds == None else timeIntervalSeconds

		def test_allconn():
			goGraphName = self.defaultConfig.defaultGraph
			for host in self.hostManagerControl.getAllClientInfos(goGraphName):
				res = host.Controlsclient.SayHello(ultipa_pb2.HelloUltipaRequest(name="test"),
												   metadata=host.getMetadata(goGraphName, None, None))
				# print(host.host,res.message)
				if self.defaultConfig.uqlLoggerConfig is None:
					self.defaultConfig.uqlLoggerConfig = LoggerConfig(name="HeartBeat", fileName=None,
																	  isWriteToFile=False,
																	  isStream=True)
				self.defaultConfig.uqlLoggerConfig.getlogger().info(f"HeartBeat:{host.host}--{res.message}")

		schedule.every().second.do(test_allconn)
		self.runSchedule = run_continuously(timeIntervalSeconds)

