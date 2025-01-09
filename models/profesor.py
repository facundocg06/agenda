from odoo import models, fields, api

class Profesor(models.Model):
    _name = 'school.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre Completo', required=True)
    cursos_ids = fields.Many2many('school.curso', string='Cursos Asignados')

    user_id = fields.Many2one('res.users', string='Usuario', ondelete='set null')

    @api.model
    def create(self, vals):
        """ Override create method to automatically create a user for the student. """

        # Verificamos si el estudiante ya tiene un usuario
        if 'user_id' not in vals:
            profesor_name = vals.get('name', '').strip()  # Obtenemos el nombre y eliminamos espacios al inicio y final
            login = profesor_name.lower().replace(' ', '.')

            user_vals = {
                'name': vals.get('name'),  # Nombre del estudiante como nombre de usuario
                # 'login': f"estudiante_{self.env['ir.sequence'].next_by_code('school.estudiante.login')}",  # Login único
                'login': login,
                'password': '123456',  # Contraseña predeterminada (puedes cambiarla o hacerla aleatoria)
                'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],  # Asignación del grupo de usuario normal
            }
            user = self.env['res.users'].create(user_vals)  # Crea el usuario
            vals['user_id'] = user.id  # Asociamos el usuario al estudiante

        profesor = super(Profesor, self).create(vals)
        return profesor