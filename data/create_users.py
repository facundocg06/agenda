from odoo import api, SUPERUSER_ID

def create_users(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    if not env['res.users'].search([('login', '=', 'miguel')]):
        user_vals = {
            'name': 'Miguel Angel',
            'login': 'miguel',
            'password': '12345678',
            'es_profesor': True,
        }
        env['res.users'].create(user_vals)
