from odoo import api, SUPERUSER_ID

def create_profesor(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Buscar los grados en la base de datos
    grado_1 = env['agenda.grado'].search([('nombre', '=', '1ro Secundaria')], limit=1)
    grado_3 = env['agenda.grado'].search([('nombre', '=', '3ro Secundaria')], limit=1)
    
    if not grado_1 or not grado_3:
        raise ValueError("Grados 1ro Secundaria o 3ro Secundaria no encontrados.")
    
    # Crear el usuario con los grados asignados
    user_vals = {
        'name': 'Miguel',
        'login': 'miguel',
        'password': '12345678',
        'es_profesor': True,
        'grados_ids': [(6, 0, [grado_1.id, grado_3.id])]
    }
    
    env['res.users'].create(user_vals)
