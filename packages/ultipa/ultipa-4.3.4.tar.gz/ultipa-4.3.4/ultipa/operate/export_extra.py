from ultipa.operate.base_extra import BaseExtra
from ultipa.types import ULTIPA_REQUEST, ULTIPA_RESPONSE


class ExportExtra(BaseExtra):

	def export(self, request: ULTIPA_REQUEST.Export,
			   requestConfig: ULTIPA_REQUEST.RequestConfig = ULTIPA_REQUEST.RequestConfig()) -> ULTIPA_RESPONSE.ResponseExport:
		res = self.exportData(request, requestConfig)
		return res
