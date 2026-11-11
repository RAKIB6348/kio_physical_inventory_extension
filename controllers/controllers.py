# -*- coding: utf-8 -*-
# from odoo import http


# class KioPhysicalInventoryExtension(http.Controller):
#     @http.route('/kio_physical_inventory_extension/kio_physical_inventory_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kio_physical_inventory_extension/kio_physical_inventory_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kio_physical_inventory_extension.listing', {
#             'root': '/kio_physical_inventory_extension/kio_physical_inventory_extension',
#             'objects': http.request.env['kio_physical_inventory_extension.kio_physical_inventory_extension'].search([]),
#         })

#     @http.route('/kio_physical_inventory_extension/kio_physical_inventory_extension/objects/<model("kio_physical_inventory_extension.kio_physical_inventory_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kio_physical_inventory_extension.object', {
#             'object': obj
#         })

