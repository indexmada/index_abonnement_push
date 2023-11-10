# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
	_inherit = "res.users"

	index_subscription = fields.Boolean("Abonnement")