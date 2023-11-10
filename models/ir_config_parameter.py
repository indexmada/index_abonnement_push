# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

INDEX_ABONNEMENT_VAL = "index.expiration_date"

# Date Format dd-mm-YYYY H:M:S

class IrConfigParameter(models.Model):
	_inherit = "ir.config_parameter"

	# Return 'none' or 'flex'
	def check_index_subscription_date(self):
		param = self.search([('key', '=', INDEX_ABONNEMENT_VAL)], limit = 1)
		res = 'none'
		is_subsc_user = self.env.user.index_subscription
		if not is_subsc_user:
			return 'none'
		if not param:
			res = 'flex'
		else:
			date_format = '%d/%m/%Y %H:%M:%S'
			date_value = param.value
			print(date_value)
			if date_value:
				try:
					d = datetime.strptime(date_value, date_format)
				except:
					return 'flex'
				if d < datetime.now():
					res = 'flex'
				else:
					res = 'none'
			else:
				res = 'flex'
		return res


	def get_date_value(self):
		param = self.search([('key', '=', INDEX_ABONNEMENT_VAL)], limit = 1)
		try:
			date_format = '%d/%m/%Y %H:%M:%S'
			d = datetime.strptime(param.value, date_format)
		except:
			return "<Format date non reconnue>"

		return param.value