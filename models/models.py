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

class estudiante(models.Model):
    _name = 'agenda.estudiante'
    _description = 'Estudiantes en la agenda estudiantil'
    
    nombre = fields.Char(string="Nombre del Estudiante", required=True)
    grado_id = fields.Many2one('agenda.grado', string="Grado", required=True)
    padres_ids = fields.Many2many('res.partner', string="Padres", domain=[('is_parent', '=', True)])
    usuario_id = fields.Many2one('res.users', string="Usuario (Alumno)", help="Usuario asignado al estudiante para el portal")

    

class tipo_comunicado(models.Model):
    _name = 'agenda.tipo_comunicado'
    _description = 'tabla de tipos de comunicado'
    nombre = fields.Char(string="Nombre", required=True)
    descripcion = fields.Char(string="Descripcion", required=True)


class comunicado(models.Model):
    _name = "agenda.comunicado"
    _description = "clase comunicado"
    
    asunto = fields.Char(string="Asunto", required=True)
    contenido = fields.Text(string="Contenido", required=True)    
    fecha_envio = fields.Datetime(string="Fecha de Envío", default=fields.Datetime.now)   
    estado = fields.Selection([('borrador', 'Borrador'), ('enviado', 'Enviado')], default='borrador')    
    destinatarios_ids = fields.Many2many('res.partner', string="Destinatarios", domain=[('is_parent', '=', True)])
    estudiantes_ids = fields.Many2many('agenda.estudiante', string="Estudiantes Destinatarios")
    grados_ids = fields.Many2many('agenda.grado', string="Grados Destinatarios")     
    creado_por_id = fields.Many2one('res.users', string="Creado por", default=lambda self: self.env.user)     
    profesores_checkbox = fields.Boolean(string="Profesores")
    padres_checkbox = fields.Boolean(string="Padres")
    administrativos_checkbox = fields.Boolean(string="Administrativos")
 
    
class parent_estudiante(models.Model):
    _name = 'agenda.parent_estudiante'
    _description = 'Relación entre padres y estudiantes'
    
    padre_id = fields.Many2one('res.partner', string="Padre", required=True)
    estudiante_id = fields.Many2one('agenda.estudiante', string="Estudiante", required=True)
    grado_id = fields.Many2one('agenda.grado', string="Grado del Estudiante")
    
    

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

