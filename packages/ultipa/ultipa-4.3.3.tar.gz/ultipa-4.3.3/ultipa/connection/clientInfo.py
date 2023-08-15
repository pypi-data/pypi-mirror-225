# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 09:21
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : clientInfo.py
from datetime import datetime
import grpc
import copy
import pytz
from tzlocal import get_localzone
from ultipa.proto import ultipa_pb2_grpc
from ultipa.utils.password2md5 import passwrod2md5


class ClientInfo:
	def __init__(self, Rpcsclient: ultipa_pb2_grpc.UltipaRpcsStub, Controlsclient: ultipa_pb2_grpc.UltipaControlsStub,
				 metadata: any, graphSetName: str, host: str):
		self.Rpcsclient = Rpcsclient
		self.Controlsclient = Controlsclient
		self.host = host
		self.metadata = metadata
		self.graphSetName = graphSetName


class GrpcClientInfo:
	Rpcsclient: ultipa_pb2_grpc.UltipaRpcsStub
	Controlsclient: ultipa_pb2_grpc.UltipaControlsStub
	host: str
	username: str
	password: str

	def __init__(self, host: str, username: str, password: str, crt: str, maxRecvSize: int = -1):
		self.host = host
		self._metadata = [('user', username), ('password', passwrod2md5(password))]
		if self.host.startswith("http"):
			channel = grpc.secure_channel(self.host.replace("https://","").replace("http://",""), grpc.ssl_channel_credentials(), options=(
				('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', maxRecvSize),
				("grpc.keepalive_timeout_ms", 1500)
			))
			self.Rpcsclient = ultipa_pb2_grpc.UltipaRpcsStub(channel=channel, )
			self.Controlsclient = ultipa_pb2_grpc.UltipaControlsStub(channel=channel, )
			return
		if crt:
			credentials = grpc.ssl_channel_credentials(root_certificates=crt)
			channel = grpc.secure_channel(self.host, credentials, options=(
				('grpc.ssl_target_name_override', 'ultipa'), ('grpc.default_authority', 'ultipa'),
				('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', maxRecvSize),
				("grpc.keepalive_timeout_ms", 1500)
			))
			self.Rpcsclient = ultipa_pb2_grpc.UltipaRpcsStub(channel=channel, )
			self.Controlsclient = ultipa_pb2_grpc.UltipaControlsStub(channel=channel, )
		else:
			channel = grpc.insecure_channel(self.host, options=(
				('grpc.max_send_message_length', -1), ('grpc.max_receive_message_length', maxRecvSize),
				("grpc.keepalive_timeout_ms", 1500)))
			self.Rpcsclient = ultipa_pb2_grpc.UltipaRpcsStub(channel=channel, )
			self.Controlsclient = ultipa_pb2_grpc.UltipaControlsStub(channel=channel, )

	def getMetadata(self, graphSetName, timeZone, timeZoneOffset):
		metadata = copy.deepcopy(self._metadata)
		metadata.append(('graph_name', graphSetName))
		if timeZone is None and timeZoneOffset is None:
			timeZone = get_localzone().__dict__.get("_key")
			tz = pytz.timezone(timeZone)
			timeZoneOffset = tz.utcoffset(datetime.now()).total_seconds()
			metadata.append(('tz_offset', str(timeZoneOffset)))
		if timeZone is not None and timeZoneOffset is None:
			metadata.append(('tz', timeZone))
		if timeZone is None and timeZoneOffset is not None:
			metadata.append(('tz_offset', str(timeZoneOffset)))
		return metadata
