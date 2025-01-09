from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Estudiante(models.Model):
    _name = 'school.estudiante'
    _description = 'Estudiante'

    name = fields.Char(string='Nombre Completo', required=True)
    curso_id = fields.Many2one('school.curso', string='Curso', required=True)
    paralelo_id = fields.Many2one('school.paralelo', string='Paralelo', required=True)

    # Campos de usuario (si necesitas campos adicionales para el usuario)
    user_id = fields.Many2one('res.users', string='Usuario', ondelete='set null')

    @api.model
    def create(self, vals):
        """ Override create method to automatically create a user for the student. """

        # Verificamos si el estudiante ya tiene un usuario
        if 'user_id' not in vals:
            student_name = vals.get('name', '').strip()  # Obtenemos el nombre y eliminamos espacios al inicio y final
            login = student_name.lower().replace(' ', '.')

            user_vals = {
                'name': vals.get('name'),  # Nombre del estudiante como nombre de usuario
                # 'login': f"estudiante_{self.env['ir.sequence'].next_by_code('school.estudiante.login')}",  # Login único
                'login': login,
                'password': '123456',  # Contraseña predeterminada (puedes cambiarla o hacerla aleatoria)
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],  # Asignación del grupo de usuario normal
            }
            user = self.env['res.users'].create(user_vals)  # Crea el usuario
            vals['user_id'] = user.id  # Asociamos el usuario al estudiante

        student = super(Estudiante, self).create(vals)
        return student
