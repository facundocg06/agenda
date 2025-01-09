from odoo import models, fields, api
from ..services.firebase import FirebaseNotification
 # Importa la clase FirebaseNotification

class Comunicado(models.Model):
    _name = 'school.comunicado'
    _description = 'Comunicado Escolar'

    asunto = fields.Char(string='Asunto', required=True)
    contenido = fields.Text(string='Contenido', required=True)
    fecha_envio = fields.Datetime(string='Fecha de Envío', default=fields.Datetime.now, required=True)
    destinatarios_tipo = fields.Selection([
        ('individual', 'Estudiantes Específicos'),
        ('grupo', 'Curso y Paralelo'),
        ('todos', 'Todos los Estudiantes')
    ], string='Tipo de Destinatarios', required=True, default='todos')

    estudiantes_ids = fields.Many2many('school.estudiante', string='Estudiantes Específicos')
    curso_id = fields.Many2one('school.curso', string='Curso')
    paralelo = fields.Selection([
        ('a', 'Paralelo A'),
        ('b', 'Paralelo B')
    ], string='Paralelo')

    archivos_ids = fields.Many2many('ir.attachment', string='Archivos Adjuntos')

    @api.onchange('destinatarios_tipo')
    def _onchange_destinatarios_tipo(self):
        """ Limpia los campos no relevantes según el tipo de destinatarios."""
        if self.destinatarios_tipo != 'individual':
            self.estudiantes_ids = False
        if self.destinatarios_tipo != 'grupo':
            self.curso_id = False
            self.paralelo = False

    @api.model
    def create(self, vals):
        """ Lógica personalizada al crear un comunicado."""
        comunicado = super(Comunicado, self).create(vals)

        # Asegurar que los archivos sean públicos
        if comunicado.archivos_ids:
            comunicado.archivos_ids.write({'public': True})

        # Enviar la notificación
        self._send_push_notification(comunicado)

        return comunicado

    def write(self, vals):
        """ Lógica personalizada al actualizar un comunicado."""
        res = super(Comunicado, self).write(vals)

        # Asegurar que los archivos sean públicos
        if 'archivos_ids' in vals:
            for comunicado in self:
                comunicado.archivos_ids.write({'public': True})

        return res

    def _send_push_notification(self, comunicado):
        """Envía la notificación push a los destinatarios del comunicado."""
        title = comunicado.asunto
        body = comunicado.contenido

        # Definir los datos adicionales de la notificación
        data = {
            'comunicado_id': str(comunicado.id),
            'asunto': title,
            'contenido': body,
        }

        # Aquí definimos el token constante para las pruebas
        # constant_token =  para pruebas

        # Enviar la notificación al token constante
        FirebaseNotification.send_notification(
            title=title,
            body=body,
            data=data,
            token=constant_token
        )
