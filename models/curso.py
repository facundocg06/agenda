from odoo import models, fields, api

class Curso(models.Model):
    _name = 'school.curso'
    _description = 'Curso Escolar'

    name = fields.Char(string='Nombre del Curso', required=True)
    nivel = fields.Selection([
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria')
    ], string='Nivel Educativo', required=True)

    paralelo_id = fields.Many2one('school.paralelo', string='Paralelo')


class Paralelo(models.Model):
    _name = 'school.paralelo'
    _description = 'Paralelo Escolar'

    name = fields.Char(string='Nombre del Paralelo', required=True)
    curso_ids = fields.One2many('school.curso', 'paralelo_id', string='Cursos')