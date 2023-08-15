from ultipa import ParameterException
from ultipa.operate.download_extra import DownloadExtra
from ultipa.operate.edge_extra import EdgeExtra
from ultipa.operate.export_extra import ExportExtra
from ultipa.operate.graph_extra import GraphExtra
from ultipa.operate.index_extra import IndexExtra
from ultipa.operate.lte_ufe_extra import LteUfeExtra
from ultipa.operate.node_extra import NodeExtra
from ultipa.operate.policy_extra import PolicyExtra
from ultipa.operate.property_extra import PropertyExtra
from ultipa.operate.schema_extra import SchemaExtra
from ultipa.operate.task_extra import TaskExtra
from ultipa.operate.truncate_extra import TruncateExtra
from ultipa.operate.user_extra import UserExtra
from ultipa.operate.base_extra import BaseExtra
from ultipa.operate.algo_extra import AlgoExtra
from ultipa.types.types import UltipaConfig
from ultipa.utils.logger import LoggerConfig


class Connection(DownloadExtra, UserExtra, PropertyExtra, NodeExtra, EdgeExtra, LteUfeExtra, IndexExtra, PolicyExtra,
				 TaskExtra, ExportExtra, GraphExtra, SchemaExtra, TruncateExtra,AlgoExtra):

	def RunHeartBeat(self, time: int):
		self.keepConnectionAlive(time)

	def StopHeartBeat(self):
		self.stopConnectionAlive()

	@staticmethod
	def NewConnection(defaultConfig: UltipaConfig = UltipaConfig()):
		conn = None
		if not defaultConfig.hosts:
			raise ParameterException(err="hosts is a required parameter")
		if not defaultConfig.username:
			raise ParameterException(err="username is a required parameter")
		if not defaultConfig.password:
			raise ParameterException(err="password is a required parameter")
		for host in defaultConfig.hosts:
			conn = Connection(host=host, defaultConfig=defaultConfig, crtFilePath=defaultConfig.crtFilePath)
			testRes = conn.test()
			if testRes.status.code == 0:
				if defaultConfig.heartBeat > 0:
					conn.RunHeartBeat(defaultConfig.heartBeat)
				return conn
		return conn

	@staticmethod
	def GetConnection(defaultConfig: UltipaConfig = UltipaConfig()):
		if defaultConfig.uqlLoggerConfig is not None:
			defaultConfig.uqlLoggerConfig.getlogger().warning("The GetConnection method will be removed in a later version. we recommend using NewConnection instead")
		else:
			log = LoggerConfig(name="GetConnection warn", fileName=None,isWriteToFile=False,isStream=True)
			log.getlogger().warning("The GetConnection method will be removed in a later version. we recommend using NewConnection instead")
		return Connection.NewConnection(defaultConfig)

	def __del__(self):
		self.StopHeartBeat()
