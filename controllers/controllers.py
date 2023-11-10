# -*- coding: utf-8 -*-
from odoo import http

# class IndexAbonnementPush(http.Controller):
#     @http.route('/index_abonnement_push/index_abonnement_push/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/index_abonnement_push/index_abonnement_push/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('index_abonnement_push.listing', {
#             'root': '/index_abonnement_push/index_abonnement_push',
#             'objects': http.request.env['index_abonnement_push.index_abonnement_push'].search([]),
#         })

#     @http.route('/index_abonnement_push/index_abonnement_push/objects/<model("index_abonnement_push.index_abonnement_push"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('index_abonnement_push.object', {
#             'object': obj
#         })