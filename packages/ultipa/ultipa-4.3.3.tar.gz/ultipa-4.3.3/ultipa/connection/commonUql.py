# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 11:59
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : commonUql.py

class GetProperty():
	node: str = 'show().node_property()'
	edge: str = 'show().edge_property()'


class GetPropertyBySchema():
	node: str = 'show().node_schema()'
	edge: str = 'show().edge_schema()'