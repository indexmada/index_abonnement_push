# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

INDEX_ABONNEMENT_VAL = "index.expiration_date"
INDEX_ABONNEMENT_MESSAGE_KEY = "index.expiration_message"

# Date Format dd-mm-YYYY H:M:S

class IrConfigParameter(models.Model):
	_inherit = "ir.config_parameter"

	# Return 'none' or 'flex'
	def check_index_subscription_date(self):
		if not self.env.user.has_group('base.group_user'):
			return 'none'
		param = self.sudo().search([('key', '=', INDEX_ABONNEMENT_VAL)], limit = 1)
		res = 'none'
		is_subsc_user = self.env.user.index_subscription
		if not is_subsc_user:
			return 'none'
		if not param:
			res = 'flex'
		else:
			date_format = '%d/%m/%Y %H:%M:%S'
			date_value = param.value
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


	def get_message_value(self):
		param = self.sudo().search([('key', '=', INDEX_ABONNEMENT_VAL)], limit = 1)
		message = self.sudo().search([('key', '=', INDEX_ABONNEMENT_MESSAGE_KEY)], limit = 1)

		if param and message:
			date_format = '%d/%m/%Y %H:%M:%S'
			d = datetime.strptime(param.value, date_format)
			if message:
				val = message.value.replace('<date>', param.value)
			else:
				val = "Votre Abonnement a été expiré le: "+param.value+". Veuillez Contacter votre Administrateur."

		else:
			val = 'Aucun message!'
		return val