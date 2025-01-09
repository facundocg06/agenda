from odoo import models, fields, api

class Actividad(models.Model):
    _name = 'school.actividad'
    _description = 'Actividad Escolar'

    titulo = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción', required=True)
    fecha_entrega = fields.Date(string='Fecha de Entrega', required=True)
    recursos_ids = fields.Many2many('ir.attachment', string='Recursos Adjuntos')
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
        """ Lógica personalizada al crear una actividad."""
        actividad = super(Actividad, self).create(vals)
        # Agregar lógica adicional aquí si es necesario
        return actividad
    