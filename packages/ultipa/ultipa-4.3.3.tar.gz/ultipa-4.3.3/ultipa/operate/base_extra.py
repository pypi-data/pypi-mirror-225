# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 17:17
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : base_extra.py
import copy
import csv
import json
import types
from typing import List

from ultipa import ParameterException
from ultipa.connection.clientType import ClientType
from ultipa.connection.commonUql import GetPropertyBySchema
from ultipa.connection.connectionBase import ConnectionBase
from ultipa.connection.uqlHelper import UQLHelper
from ultipa.proto import ultipa_pb2
from ultipa.types import ULTIPA, ULTIPA_REQUEST, ULTIPA_RESPONSE
from ultipa.types.types_response import PropertyTable
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertTableToDict, convertToListAnyObject
from ultipa.utils.format import FormatType
from ultipa.utils.raftRetry import RetryHelp
from ultipa.utils.ultipa_datetime import getTimeZoneOffset, getTimeOffsetSeconds


class BaseExtra(ConnectionBase):

	def test(self,
			 requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()) -> ULTIPA_RESPONSE.Response:
		testResponse = ULTIPA_RESPONSE.Response()
		returnReq = ULTIPA.ReturnReq(requestConfig.graphName, "test", None, None, False)
		try:
			clientInfo = self.getClientInfo(useHost=requestConfig.useHost, useMaster=requestConfig.useMaster)
			name = 'Test'
			res = clientInfo.Controlsclient.SayHello(ultipa_pb2.HelloUltipaRequest(name=name),
													 metadata=clientInfo.metadata)
			returnReq.host = clientInfo.host
			if (res.message == name + " Welcome To Ultipa!"):
				if self.defaultConfig.uqlLoggerConfig:
					self.defaultConfig.uqlLoggerConfig.getlogger().info(res.message)

				testResponse.status = ULTIPA.Status(code=res.status.error_code, message=res.status.msg)
			else:
				testResponse.status = ULTIPA.Status(code=res.status.error_code, message=res.status.msg)
		except Exception as e:
			testResponse = ULTIPA_RESPONSE.Response()
			try:
				message = str(e._state.details)
			except:
				message = str(e)
			testResponse.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)
		if self.defaultConfig.responseWithRequestInfo:
			testResponse.req = returnReq
		return testResponse

	def stats(self,
			  requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()) -> ULTIPA_RESPONSE.ResponseStat:
		uqlMaker = UQLMAKER(command=CommandList.stat, commonParams=requestConfig)
		ret = self.UqlListSimple(uqlMaker=uqlMaker, isSingleOne=True)
		if ret.status.code == ULTIPA.Code.SUCCESS:
			ret.data = ret.data[0]
		return ret

	def exportData(self, request: ULTIPA_REQUEST.Export,
				   requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()):
		try:
			req = ultipa_pb2.ExportRequest(db_type=request.type, limit=request.limit,
										   select_properties=request.properties, schema=request.schema)

			clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, useMaster=requestConfig.useMaster)
			res = clientInfo.Controlsclient.Export(req, metadata=clientInfo.metadata)
			res = FormatType.exportResponse(_res=res, timeZone=requestConfig.timeZone,
											timeZoneOffset=requestConfig.timeZoneOffset)
			return res
		except Exception as e:
			errorRes = ULTIPA_RESPONSE.Response()
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = 'UNKNOW ERROR'

			errorRes.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)
			errorRes.req = ULTIPA.ReturnReq(self.graphSetName, "exportData",
											requestConfig.useHost if requestConfig.useHost else self.host,
											requestConfig.retry,
											False)
			return errorRes

	def uql(self, uql: str,
			requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		request = ultipa_pb2.UqlRequest()
		request.uql = uql
		request.timeout = self.getTimeout(requestConfig.timeoutWithSeconds)
		if requestConfig.threadNum is not None:
			request.thread_num = requestConfig.threadNum
		ultipaRes = ULTIPA_RESPONSE.UltipaResponse()
		uqlLoggerConfig = self.defaultConfig.uqlLoggerConfig
		if requestConfig.graphName == '' and self.defaultConfig.defaultGraph != '':
			requestConfig.graphName = self.defaultConfig.defaultGraph

		if self.defaultConfig.consistency != self.hostManagerControl.consistency:
			self.hostManagerControl.consistency = self.defaultConfig.consistency

		if self.defaultConfig.maxRecvSize != self.hostManagerControl.maxRecvSize:
			self.hostManagerControl.maxRecvSize = self.defaultConfig.maxRecvSize
		onRetry = copy.deepcopy(requestConfig.retry)
		while onRetry.current < onRetry.max:
			try:
				import pytz
				getTimeZoneOffset(requestConfig, self.defaultConfig)
				timeZone = requestConfig.timeZone if requestConfig.timeZone else self.defaultConfig.timeZone
				timeZoneOffset = requestConfig.timeZoneOffset if requestConfig.timeZoneOffset else self.defaultConfig.timeZoneOffset
				timeZoneOffset = getTimeOffsetSeconds(timeZoneOffset)
				clientInfo = self.getClientInfo(graphSetName=requestConfig.graphName, uql=uql,
												useHost=requestConfig.useHost,
												useMaster=requestConfig.useMaster, timezone=timeZone,
												timeZoneOffset=timeZoneOffset)
				if uqlLoggerConfig:
					uqlLoggerConfig.getlogger().info(
						f'Begin UQL: {uql} graphSetName: {clientInfo.graphSetName} Host: {clientInfo.host}')
				uqlIsExtra = UQLHelper.uqlIsExtra(uql)
				if uqlIsExtra:
					res = clientInfo.Controlsclient.UqlEx(request, metadata=clientInfo.metadata)
				else:
					res = clientInfo.Rpcsclient.Uql(request, metadata=clientInfo.metadata)

				if not requestConfig.stream:
					ultipaRes = FormatType.uqlMergeResponse(res, timeZone, timeZoneOffset)
				else:
					ultipaRes = FormatType.uqlResponse(res, timeZone, timeZoneOffset)

				if self.defaultConfig.responseWithRequestInfo and not requestConfig.stream:
					ultipaRes.req = ULTIPA.ReturnReq(clientInfo.graphSetName, uql, clientInfo.host, onRetry,
													 uqlIsExtra)
				if not isinstance(ultipaRes, types.GeneratorType) and RetryHelp.checkRes(ultipaRes):
					onRetry.current += 1
					continue
				else:
					return ultipaRes

			except Exception as e:
				onRetry.current += 1
				if uqlLoggerConfig:
					uqlLoggerConfig.getlogger().info(
						f'Begin Retry [{onRetry.current}]- clientInfo host: {clientInfo.host} graphSetName: {clientInfo.graphSetName}')
				self.hostManagerControl.getHostManger(requestConfig.graphName).raftReady = False
				try:
					message = str(e._state.code) + ' : ' + str(e._state.details)
				except:
					message = str(e)
				ultipaRes.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)
				ultipaRes.req = ULTIPA.ReturnReq(requestConfig.graphName, uql,
												 requestConfig.useHost if requestConfig.useHost else self.host,
												 onRetry, False)

		return ultipaRes

	def uqlSingle(self, uqlMaker: UQLMAKER) -> ULTIPA_RESPONSE.UltipaResponse:
		res = self.uql(uqlMaker.toString(), uqlMaker.commonParams)
		return res


	def UqlListSimple(self, uqlMaker: UQLMAKER, responseKeyFormat: ResponseKeyFormat = None,
					  isSingleOne: bool = True) -> ULTIPA_RESPONSE.Response:
		res = self.uqlSingle(uqlMaker)

		if res.status.code != ULTIPA.Code.SUCCESS:
			simplrRes = ULTIPA_RESPONSE.Response(res.status, res.items)
			return simplrRes

		if not isSingleOne:
			retList = []
			for alias in res.aliases:
				item = res.items.get(alias.alias)
				table = item.data
				table_rows = table.rows
				table_rows_dict = convertTableToDict(table_rows, table.headers)
				if responseKeyFormat:
					table_rows_dict = responseKeyFormat.changeKeyValue(table_rows_dict)
				data = convertToListAnyObject(table_rows_dict)
				retList.append(PropertyTable(name=table.name, data=data))
			simplrRes = ULTIPA_RESPONSE.Response(res.status, retList)
			simplrRes.req = res.req
			return simplrRes

		alisFirst = res.aliases[0].alias if len(res.aliases) > 0 else None
		firstItem = res.items.get(alisFirst)
		if firstItem:
			table_rows = firstItem.data.rows
			table_rows_dict = convertTableToDict(table_rows, firstItem.data.headers)
			if responseKeyFormat:
				table_rows_dict = responseKeyFormat.changeKeyValue(table_rows_dict)
			data = convertToListAnyObject(table_rows_dict)
			simplrRes = ULTIPA_RESPONSE.Response(res.status, data)
			simplrRes.req = res.req
			simplrRes.statistics = res.statistics
			return simplrRes
		else:
			return res

	def UqlUpdateSimple(self, uqlMaker: UQLMAKER):
		res = self.uqlSingle(uqlMaker)

		if res.status.code != ULTIPA.Code.SUCCESS:
			return ULTIPA_RESPONSE.Response(res.status, statistics=res.statistics)

		if res.req:
			ret = ULTIPA_RESPONSE.Response(res.status, statistics=res.statistics)
			ret.req = res.req
			return ret
		return ULTIPA_RESPONSE.Response(res.status, statistics=res.statistics)

	def insertNodesBatchBySchema(self, schema: ULTIPA_REQUEST.Schema, rows: List[ULTIPA.EntityRow],
								 config: ULTIPA_REQUEST.InsertConfig) -> ULTIPA_RESPONSE.InsertResponse:
		config.useMaster = True
		if config.graphName == '' and self.defaultConfig.defaultGraph != '':
			config.graphName = self.defaultConfig.defaultGraph

		clientInfo = self.getClientInfo(clientType=ClientType.Update, graphSetName=config.graphName,
										useMaster=config.useMaster)

		nodetable = FormatType.makeEntityNodeTable(schema, rows, getTimeZoneOffset(requestConfig=config,
																				   defaultConfig=self.defaultConfig))

		_nodeTable = ultipa_pb2.EntityTable(schemas=nodetable.schemas, entity_rows=nodetable.nodeRows)
		request = ultipa_pb2.InsertNodesRequest()
		request.silent = config.silent
		request.insert_type = config.insertType
		request.graph_name = config.graphName
		request.node_table.MergeFrom(_nodeTable)
		res = clientInfo.Rpcsclient.InsertNodes(request, metadata=clientInfo.metadata)

		status = FormatType.status(res.status)
		uqlres = ULTIPA_RESPONSE.Response(status=status)
		reTry = RetryHelp.check(self, config, uqlres)
		if reTry.canRetry:
			config.retry = reTry.nextRetry
			return self.insertNodesBatchBySchema(schema, rows, config)

		uRes = ULTIPA_RESPONSE.ResponseBulk()
		uRes.uuids = [i for i in res.uuids]
		errorDict = {}
		for i, data in enumerate(res.ignore_error_code):
			try:
				index = rows[res.ignore_indexes[i]]._getIndex()
			except Exception as e:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			if index is None:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			errorDict.update({index: data})
		uRes.errorItem = errorDict
		uqlres.data = uRes
		uqlres.total_time = res.time_cost
		uqlres.engine_time = res.engine_time_cost
		if self.defaultConfig.responseWithRequestInfo:
			uqlres.req = ULTIPA.ReturnReq(config.graphName, "InsertNodesBatchBySchema", clientInfo.host, reTry,
										  False)
		return uqlres

	def insertEdgesBatchBySchema(self, schema: ULTIPA_REQUEST.Schema, rows: List[ULTIPA.EntityRow],
								 config: ULTIPA_REQUEST.InsertConfig) -> ULTIPA_RESPONSE.InsertResponse:
		config.useMaster = True
		if config.graphName == '' and self.defaultConfig.defaultGraph != '':
			config.graphName = self.defaultConfig.defaultGraph

		clientInfo = self.getClientInfo(clientType=ClientType.Update, graphSetName=config.graphName,
										useMaster=config.useMaster)

		edgetable = FormatType.makeEntityEdgeTable(schema=schema, rows=rows,
												   timeZoneOffset=getTimeZoneOffset(requestConfig=config,
																					defaultConfig=self.defaultConfig))

		_edgeTable = ultipa_pb2.EntityTable(schemas=edgetable.schemas, entity_rows=edgetable.edgeRows)
		request = ultipa_pb2.InsertEdgesRequest()
		request.silent = config.silent
		request.insert_type = config.insertType
		request.graph_name = config.graphName
		request.create_node_if_not_exist = config.createNodeIfNotExist
		request.edge_table.MergeFrom(_edgeTable)
		res = clientInfo.Rpcsclient.InsertEdges(request, metadata=clientInfo.metadata)

		status = FormatType.status(res.status)
		uqlres = ULTIPA_RESPONSE.Response(status=status)
		reTry = RetryHelp.check(self, config, uqlres)
		if reTry.canRetry:
			config.retry = reTry.nextRetry
			return self.insertEdgesBatchBySchema(schema, rows, config)

		uRes = ULTIPA_RESPONSE.ResponseBulk()
		uRes.uuids = [i for i in res.uuids]
		errorDict = {}
		for i, data in enumerate(res.ignore_error_code):
			try:
				index = rows[res.ignore_indexes[i]]._getIndex()
			except Exception as e:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			if index is None:
				try:
					index = res.ignore_indexes[i]
				except Exception as e:
					index = i
			errorDict.update({index: data})
		uRes.errorItem = errorDict
		uqlres.data = uRes
		uqlres.total_time = res.time_cost
		uqlres.engine_time = res.engine_time_cost
		if self.defaultConfig.responseWithRequestInfo:
			uqlres.req = ULTIPA.ReturnReq(config.graphName, "InsertEdgesBatchBySchema", clientInfo.host, reTry,
										  False)
		return uqlres

	def insertNodesBatchAuto(self, nodes: List[ULTIPA.EntityRow],
							 config: ULTIPA_REQUEST.InsertConfig) -> ULTIPA_RESPONSE.ResponseBatchAutoInsert:
		Result = {}
		schemaDict = {}
		batches = {}
		schemaRet = self.uql(GetPropertyBySchema.node, config)
		if schemaRet.status.code == ULTIPA.Code.SUCCESS:
			for aliase in schemaRet.aliases:
				if aliase.alias == '_nodeSchema':
					schemaDict = convertTableToDict(schemaRet.alias(aliase.alias).data.rows,
													schemaRet.alias(aliase.alias).data.headers)
			if not schemaDict:
				raise ParameterException(err='Please create Node Schema.')
		else:
			raise ParameterException(err=schemaRet.status.message)
		for index, node in enumerate(nodes):
			node._index = index
			if batches.get(node.schema) is None:
				batches[node.schema] = ULTIPA_REQUEST.Batch()
				find = list(filter(lambda x: x.get('name') == node.schema, schemaDict))
				if find:
					findSchema = find[0]
					propertyList = FormatType.checkProperty(node, json.loads(findSchema.get("properties")))
					reqSchema = ULTIPA_REQUEST.Schema(node.schema, propertyList)
					batches[node.schema].Schema = reqSchema
				else:
					if node.schema is None:
						raise ParameterException(err=f"Row [{index}]:Please set schema name for node.")
					else:
						raise ParameterException(err=f"Row [{index}]:Node Schema not found {node.schema}.")

			batches.get(node.schema).Nodes.append(node)
		for key in batches:
			batch = batches.get(key)
			Result.update(
				{key: self.insertNodesBatchBySchema(schema=batch.Schema, rows=batch.Nodes, config=config)})

		newStatusMsg = ""
		newCode = None
		for i, key in enumerate(Result):
			ret = Result.get(key)
			newStatusMsg += f"{key}:{ret.status.message} "
			if ret.status.code != ULTIPA.Code.SUCCESS and not newCode:
				newCode = ret.status.code
		if newCode is None:
			newCode = ULTIPA.Code.SUCCESS
		status = ULTIPA_RESPONSE.Status(newCode, newStatusMsg)
		newResponse = ULTIPA_RESPONSE.ResponseBatchAutoInsert(status=status)
		newResponse.data = Result
		return newResponse

	def insertEdgesBatchAuto(self, edges: List[ULTIPA.EntityRow],
							 config: ULTIPA_REQUEST.InsertConfig) -> ULTIPA_RESPONSE.ResponseBatchAutoInsert:
		Result = {}
		schemaDict = []
		batches = {}
		schemaRet = self.uql(GetPropertyBySchema.edge, config)
		if schemaRet.status.code == ULTIPA.Code.SUCCESS:
			for aliase in schemaRet.aliases:
				if aliase.alias == '_edgeSchema':
					schemaDict = convertTableToDict(schemaRet.alias(aliase.alias).data.rows,
													schemaRet.alias(aliase.alias).data.headers)
			if not schemaDict:
				raise ParameterException(err='Please create Edge Schema.')
		else:
			raise ParameterException(err=schemaRet.status.message)
		for index, edge in enumerate(edges):
			edge._index = index
			if batches.get(edge.schema) == None:
				batches[edge.schema] = ULTIPA_REQUEST.Batch()
				find = list(filter(lambda x: x.get('name') == edge.schema, schemaDict))
				if find:
					findSchema = find[0]
					propertyList = FormatType.checkProperty(edge, json.loads(findSchema.get("properties")))
					reqSchema = ULTIPA_REQUEST.Schema(edge.schema, propertyList)
					batches[edge.schema].Schema = reqSchema
				else:
					if edge.schema is None:
						raise ParameterException(err=f"Row [{index}]:Please set schema name for edge.")
					else:
						raise ParameterException(err=f"Row [{index}]:Edge Schema not found {edge.schema}.")
			batches.get(edge.schema).Edges.append(edge)
		for key in batches:
			batch = batches.get(key)
			Result.update(
				{key: self.insertEdgesBatchBySchema(schema=batch.Schema, rows=batch.Edges, config=config)})

		newStatusMsg = ""
		newCode = None
		for i, key in enumerate(Result):
			ret = Result.get(key)
			newStatusMsg += f"{key}:{ret.status.message} "
			if ret.status.code != ULTIPA.Code.SUCCESS and not newCode:
				newCode = ret.status.code
		if newCode is None:
			newCode = ULTIPA.Code.SUCCESS
		status = ULTIPA_RESPONSE.Status(newCode, newStatusMsg)
		newResponse = ULTIPA_RESPONSE.ResponseBatchAutoInsert(status=status)
		newResponse.data = Result
		return newResponse

	def _InsertByCSV(self, csvPath: str, type: ULTIPA.DBType, config: ULTIPA_REQUEST.InsertConfig,
					 schemaName: str = None) -> ULTIPA_RESPONSE.ResponseBatchAutoInsert:
		rows = []
		propertyType = []
		properties = []
		types = []
		with open(csvPath, "r", encoding="utf-8-sig") as csvfile:
			reader = csv.reader(csvfile)
			for i, line in enumerate(reader):
				if i == 0:
					for i, property in enumerate(line):
						k1, k2 = property.split(":")
						propertyType.append({k1: k2})
						types.append({"index": i, "type": k2})
						properties.append(k1)
					continue
				for i in types:
					if i.get("type") in ["int", "int32", "int64"]:
						if line[i.get("index")] == "":
							line[i.get("index")] = 0
							continue
						line[i.get("index")] = int(line[i.get("index")])
					if i.get("type") in ["float", "double"]:
						if line[i.get("index")] == "":
							line[i.get("index")] = 0.0
							continue
						line[i.get("index")] = float(line[i.get("index")])
				line = dict(zip(properties, line))
				if i == 0:
					print(line.keys())
				if type == ULTIPA.DBType.DBNODE:
					if line.get("_uuid"):
						uuid = line.get("_uuid")
						line.__delitem__("_uuid")
						rows.append(ULTIPA.Node(line, schema_name=schemaName, uuid=int(uuid)))
					elif line.get("_id"):
						id = line.get("_id")
						line.__delitem__("_id")
						rows.append(ULTIPA.Node(line, schema_name=schemaName, id=id))
					else:
						rows.append(ULTIPA.Node(line, schema_name=schemaName))

				elif type == ULTIPA.DBType.DBEDGE:
					if line.get("_from_uuid") and line.get("_to_uuid"):
						from_uuid = line.get("_from_uuid")
						line.__delitem__("_from_uuid")
						to_uuid = line.get("_to_uuid")
						line.__delitem__("_to_uuid")
						line.__delitem__("_id")
						rows.append(
							ULTIPA.Edge(line, schema_name=schemaName, from_uuid=int(from_uuid),
										to_uuid=int(to_uuid)))
					elif line.get("_from_id") and line.get("_to_id"):
						from_id = line.get("_from_id")
						line.__delitem__("_from_id")
						to_id = line.get("_to_id")
						line.__delitem__("_to_id")
						if line.get("_id"):
							line.__delitem__("_id")
						rows.append(ULTIPA.Edge(line, schema_name=schemaName, from_id=from_id, to_id=to_id))

		if type == ULTIPA.DBType.DBNODE:
			return self.insertNodesBatchAuto(rows, config)
		else:
			return self.insertEdgesBatchAuto(rows, config)