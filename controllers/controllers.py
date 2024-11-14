from odoo import http
from odoo.http import request, route, Response

from odoo import http
from odoo.http import request, route, Response

class UserController(http.Controller):

    @route('/api/register', type='http', auth='public', methods=['POST'], csrf=False)
    def register_user(self, **kwargs):
        required_fields = ['name', 'login', 'password', 'role', 'grados_ids']
        missing_fields = [field for field in required_fields if field not in kwargs]

        if missing_fields:
            return Response(f"Faltan los campos requeridos: {', '.join(missing_fields)}", status=400)

        user_vals = {
            'name': kwargs['name'],
            'login': kwargs['login'],
            'password': kwargs['password'],
            'es_profesor': kwargs.get('role') == 'profesor',
            'es_administrativo': kwargs.get('role') == 'administrativo',
            'es_padre': kwargs.get('role') == 'padre',
            'es_alumno': kwargs.get('role') == 'alumno',
            'grados_ids': [(6, 0, kwargs.get('grados_ids', []))]
        }

        try:
            user = request.env['res.users'].sudo().create(user_vals)
            return Response(f"Usuario creado con éxito, ID del usuario: {user.id}", status=200)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=500)



class ComunicadoController(http.Controller):

    @route('/api/comunicados', type='http', auth='user', methods=['GET'], csrf=False)
    def list_comunicados(self, **kwargs):
        user = request.env.user
        comunicados = request.env['agenda.comunicado'].sudo().search([
            ('grados_ids', 'in', user.grados_ids.ids)
        ])

        result = [
            f"ID: {comunicado.id}, Asunto: {comunicado.asunto}, Contenido: {comunicado.contenido}, Fecha de Envío: {comunicado.fecha_envio}, Estado: {comunicado.estado}"
            for comunicado in comunicados
        ]

        return Response(f"Comunicados:\n" + "\n".join(result), status=200)

    @route('/api/comunicados/<int:comunicado_id>', type='http', auth='user', methods=['GET'], csrf=False)
    def get_comunicado(self, comunicado_id, **kwargs):
        comunicado = request.env['agenda.comunicado'].sudo().browse(comunicado_id)

        if not comunicado.exists():
            return Response("Comunicado no encontrado", status=404)

        result = f"ID: {comunicado.id}, Asunto: {comunicado.asunto}, Contenido: {comunicado.contenido}, Fecha de Envío: {comunicado.fecha_envio}, Estado: {comunicado.estado}, Grados: {', '.join([grado.nombre for grado in comunicado.grados_ids])}"
        
        return Response(result, status=200)

    @route('/api/comunicados/create', type='http', auth='user', methods=['POST'], csrf=False)
    def create_comunicado(self, **kwargs):
        if not (request.env.user.es_profesor or request.env.user.es_administrativo):
            return Response("No tienes permisos para crear comunicados", status=403)

        comunicado_vals = {
            'asunto': kwargs.get('asunto'),
            'contenido': kwargs.get('contenido'),
            'grados_ids': [(6, 0, kwargs.get('grados_ids', []))],
            'destinatario_tipo': [(6, 0, kwargs.get('destinatario_tipo', []))],
        }

        try:
            comunicado = request.env['agenda.comunicado'].sudo().create(comunicado_vals)
            comunicado._enviar_notificaciones()
            return Response(f"Comunicado creado con éxito, ID del comunicado: {comunicado.id}", status=200)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=500)
