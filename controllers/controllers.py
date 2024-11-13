from odoo import http
from odoo.http import request, route


class UserController(http.Controller):

    @route('/api/register', type='json', auth='public', methods=['POST'])
    def register_user(self, **kwargs):
        required_fields = ['name', 'login', 'password', 'role']
        missing_fields = [field for field in required_fields if field not in kwargs]

        if missing_fields:
            return {'error': f"Faltan los campos requeridos: {', '.join(missing_fields)}"}

        user_vals = {
            'name': kwargs['name'],
            'login': kwargs['login'],
            'password': kwargs['password'],
            'es_profesor': kwargs.get('role') == 'profesor',
            'es_administrativo': kwargs.get('role') == 'administrativo'
        }

        user = request.env['res.users'].sudo().create(user_vals)
        return {'success': True, 'user_id': user.id}


class ComunicadoController(http.Controller):

    @route('/api/comunicados', type='json', auth='user', methods=['GET'])
    def list_comunicados(self, **kwargs):
        user = request.env.user
        comunicados = request.env['agenda.comunicado'].sudo().search([
            ('grados_ids', 'in', user.grados_ids.ids)
        ])

        return [
            {
                'id': comunicado.id,
                'asunto': comunicado.asunto,
                'contenido': comunicado.contenido,
                'fecha_envio': comunicado.fecha_envio,
                'estado': comunicado.estado,
            }
            for comunicado in comunicados
        ]
    
    @route('/api/comunicados/<int:comunicado_id>', type='json', auth='user', methods=['GET'])
    def get_comunicado(self, comunicado_id, **kwargs):
        comunicado = request.env['agenda.comunicado'].sudo().browse(comunicado_id)

        if not comunicado.exists():
            return {'error': 'Comunicado no encontrado'}

        return {
            'id': comunicado.id,
            'asunto': comunicado.asunto,
            'contenido': comunicado.contenido,
            'fecha_envio': comunicado.fecha_envio,
            'estado': comunicado.estado,
            'grados': [grado.nombre for grado in comunicado.grados_ids],
        }
    
    @route('/api/comunicados/create', type='json', auth='user', methods=['POST'])
    def create_comunicado(self, **kwargs):
        if not (request.env.user.es_profesor or request.env.user.es_administrativo):
            return {'error': 'No tienes permisos para crear comunicados'}

        comunicado_vals = {
            'asunto': kwargs.get('asunto'),
            'contenido': kwargs.get('contenido'),
            'grados_ids': [(6, 0, kwargs.get('grados_ids', []))],
            'destinatario_tipo': [(6, 0, kwargs.get('destinatario_tipo', []))],
        }

        comunicado = request.env['agenda.comunicado'].sudo().create(comunicado_vals)
        comunicado._enviar_notificaciones()
        return {'success': True, 'comunicado_id': comunicado.id}


