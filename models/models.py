# -*- coding: utf-8 -*-

from odoo import models, fields, api
from pyfcm import FCMNotification

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
    device_token = fields.Char(string="Token del Dispositivo", help="Token FCM para notificaciones push")
    grados_ids = fields.Many2many(
    'agenda.grado', 
    string="Grados Asignados", 
    help="Grados asignados al profesor o administrativo"
    )


    @api.depends('es_administrativo', 'es_profesor')
    def _compute_grados_ids(self):
        """Asignar grados automáticamente según el rol"""
        for user in self:
            if user.es_administrativo:
                
                user.grados_ids = self.env['agenda.grado'].search([])
            elif user.es_profesor:
               
                pass
            else:
                user.grados_ids = [(5, 0, 0)]  


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
    def create(self, vals):
        comunicado = super(Comunicado, self).create(vals)
        
        # Buscar usuarios asociados a los grados seleccionados
        usuarios_destinatarios = self.env['res.users'].search([
            ('grados_ids', 'in', comunicado.grados_ids.ids)
        ])

        # Crear notificaciones para cada usuario destinatario
        for usuario in usuarios_destinatarios:
            self.env['agenda.notificacion'].create({
                'comunicado_id': comunicado.id,
                'user_id': usuario.id,
                'estado': 'enviado',
            })            
            
            #self.env['agenda.notificacion'].send_notification(usuario, comunicado)
        
        return comunicado



class Notificacion(models.Model):
    _name = 'agenda.notificacion'
    _description = 'Registro de Notificaciones'

    comunicado_id = fields.Many2one('agenda.comunicado', string="Comunicado", required=True)
    user_id = fields.Many2one('res.users', string="Usuario", required=True)
    estado = fields.Selection([
        ('enviado', 'Enviado'),
        ('recibido', 'Recibido'),
        ('no_enviado', 'No Enviado'),
        ('leido', 'Leído')
    ], default='enviado', string="Estado")
    fecha_envio = fields.Datetime(string="Fecha de Envío", default=fields.Datetime.now)

    @api.model
    def send_notification(self, user, comunicado):
        # Configurar FCM
        fcm_api_key = 'coloque aqui su apikey'
        push_service = FCMNotification(api_key=fcm_api_key)

        # Obtener el token del dispositivo del usuario
        device_token = user.device_token
        if not device_token:
            return False

        # Mensaje de la notificación
        message_title = f"Nuevo Comunicado: {comunicado.asunto}"
        message_body = comunicado.contenido

        try:
            result = push_service.notify_single_device(
                registration_id=device_token,
                message_title=message_title,
                message_body=message_body
            )
            estado = 'enviado' if result.get('success') == 1 else 'no_enviado'
        except Exception as e:
            estado = 'no_enviado'

        # Registrar la notificación
        self.create({
            'comunicado_id': comunicado.id,
            'user_id': user.id,
            'estado': estado,
        })
        return True

    
    



