# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    is_parent = fields.Boolean(string="Es Padre", default=False)
    estudiante_ids = fields.Many2many('agenda.estudiante', string="Estudiantes", help="Estudiantes asociados a este padre")

class grado(models.Model):
    _name = 'agenda.grado'
    _description = 'Grados o Cursos de los estudiantes'
    
    nombre = fields.Char(string="Nombre del Grado", required=True)
    descripcion = fields.Text(string="Descripción")
    _rec_name = 'nombre'

class estudiante(models.Model):
    _name = 'agenda.estudiante'
    _description = 'Estudiantes en la agenda estudiantil'
    
    nombre = fields.Char(string="Nombre del Estudiante", required=True)
    grado_id = fields.Many2one('agenda.grado', string="Grado", required=True)
    padres_ids = fields.Many2many('res.partner', string="Padres", domain=[('is_parent', '=', True)])
    usuario_id = fields.Many2one('res.users', string="Usuario (Alumno)", help="Usuario asignado al estudiante para el portal")

class DestinatarioTipo(models.Model):
    _name = 'agenda.destinatario_tipo'
    _description = 'Tipos de destinatarios para los comunicados'

    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")


    

class tipo_comunicado(models.Model):
    _name = 'agenda.tipo_comunicado'
    _description = 'tabla de tipos de comunicado'
    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Char(string="Descripcion", required=True)


class DestinatarioTipo(models.Model):
    _name = 'agenda.destinatario_tipo'
    _description = 'Tipos de destinatarios para los comunicados'

    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Text(string="Descripción")
    _rec_name = 'nombre'


from odoo import models, fields, api

class Comunicado(models.Model):
    _name = "agenda.comunicado"
    _description = "Clase comunicado"

    asunto = fields.Char(string="Asunto", required=True)
    contenido = fields.Text(string="Contenido", required=True)
    multimedia_ids = fields.Many2many(
        'ir.attachment',
        string='Archivos',
        help='Cargar imágenes, videos, audios o enlaces.'
    )
    fecha_envio = fields.Datetime(string="Fecha de Envío", default=fields.Datetime.now)
    estado = fields.Selection([('borrador', 'Borrador'), ('enviado', 'Enviado')], default='borrador')    
    grados_ids = fields.Many2many('agenda.grado', string="Grados Destinatarios")
    creado_por_id = fields.Many2one('res.users', string="Creado por", default=lambda self: self.env.user)
    destinatario_tipo = fields.Many2many('agenda.destinatario_tipo', string="Destinatarios")

    @api.model
    def default_get(self, fields):
        res = super(Comunicado, self).default_get(fields)
        user = self.env.user
        res['uid_grados_ids'] = user.grados_ids.ids
        return res



    
class parent_estudiante(models.Model):
    _name = 'agenda.parent_estudiante'
    _description = 'Relación entre padres y estudiantes'
    
    padre_id = fields.Many2one('res.partner', string="Padre", required=True)
    estudiante_id = fields.Many2one('agenda.estudiante', string="Estudiante", required=True)
    grado_id = fields.Many2one('agenda.grado', string="Grado del Estudiante")

class ResUsers(models.Model):
    _inherit = 'res.users'

    es_profesor = fields.Boolean(string="Es Profesor", default=False)
    es_administrativo = fields.Boolean(string="Es Administrativo", default=False)
    grados_ids = fields.Many2many(
        'agenda.grado', 
        string="Grados Asignados", 
        help="Grados asignados al profesor",
        compute='_compute_grados_ids', 
        store=True
    )

    @api.depends('es_administrativo', 'es_profesor')
    def _compute_grados_ids(self):
        """Asignar grados automáticamente según el rol"""
        for user in self:
            if user.es_administrativo:
                # Si es administrativo, asignar todos los grados
                user.grados_ids = self.env['agenda.grado'].search([])
            elif user.es_profesor:
                # Los grados deben ser seleccionados manualmente para profesores
                pass
            else:
                user.grados_ids = [(5, 0, 0)]  # Limpiar grados si no es profesor ni administrativo

    
    

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

