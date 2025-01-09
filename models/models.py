# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class school(models.Model):
    _name = 'school.school'
    _description = 'school.school'

    name = fields.Char()



class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def make_all_attachments_public(self):
        """Hace públicos todos los adjuntos en el sistema."""
        attachments = self.search([])
        attachments.write({'public': True})
        return f"{len(attachments)} adjuntos ahora son públicos."
