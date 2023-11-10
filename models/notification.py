# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta, datetime

from dateutil.relativedelta import *

# Format rappel avant expiration: JJ/MM (nom clé: index.periode_rappel)
INDEX_PERIOD_RAPPEL = "index.periode_rappel"

# nom clé: index.message_notif.
INDEX_MESSAGE_NOTIF = "index.message_notif"

INDEX_ABONNEMENT_VAL = "index.expiration_date"

class SendNotification(models.Model):
	_name = "send.notification"
	_inherit = ["mail.thread"]

	last_date = fields.Date("Date dérnier envoye")

	@api.multi
	def send_notification_subscription(self):
		if not self.env.user.has_group('base.group_user'):
			return False
		today = date.today()
		is_notified = self.sudo().search([('last_date', '=', today)])
		if is_notified:
			return False

		# Check if param system ok
		date_format = '%d/%m/%Y %H:%M:%S'
		param = self.env['ir.config_parameter'].sudo().search([('key', '=', INDEX_PERIOD_RAPPEL)], limit = 1)
		date_key = self.env['ir.config_parameter'].sudo().search([('key', '=', INDEX_ABONNEMENT_VAL)], limit = 1)
		date_value = datetime.strptime(date_key.value, date_format) if date_key and date_key.value else False
		if param.value and date_value:
			d = int(param.value.split('/')[0])
			m = int(param.value.split('/')[1])

			date_subs_notif = date_value - timedelta(d) if d else date_value
			if m:
				date_subs_notif = date_subs_notif - relativedelta(months=+m)

			if date_subs_notif > datetime.now():
				return False
		else:
			return False

		message = False
		if date_key.value:
			message_notif = self.env['ir.config_parameter'].sudo().search([('key', '=', INDEX_MESSAGE_NOTIF)], limit = 1)
			message_temp = "Votre abonnement sera expiré le "+date_key.value+". Veuillez contacter votre administrateur."

			message = message_notif.value.replace('<date>', date_key.value) if message_notif else message_temp

		partner_ids = self.env['res.users'].sudo().search([]).filtered(lambda x: x.has_group('base.group_user')).mapped('partner_id')
		# self.message_post(body="Index Message Notification", partner_ids=partner_ids)
		self.env['mail.message'].sudo().create({'message_type':"notification",
                "subtype_id": self.env.ref("mail.mt_comment").id,
                'body': message or 'Aucun message généré!',
                'subject': "Notification d'abonnement",
                'needaction_partner_ids': [(6, 0, partner_ids.ids)],
                'model': self._name,
                'res_id': self.id,
                })

		self.sudo().create({
			"last_date" : today
			})

		return True