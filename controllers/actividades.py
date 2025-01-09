from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class ActividadController(http.Controller):

    @http.route('/api/actividades', type='json', auth='user', methods=['GET'], csrf=False)
    def get_actividades(self):
        """
        Obtiene todas las actividades disponibles.
        """
        try:
            actividades = request.env['school.actividad'].sudo().search([])

            result = []
            for actividad in actividades:
                result.append({
                    'id': actividad.id,
                    'titulo': actividad.titulo,
                    'descripcion': actividad.descripcion,
                    'fecha_entrega': actividad.fecha_entrega.isoformat() if actividad.fecha_entrega else None,
                    'recursos': [{'id': adjunto.id, 'nombre': adjunto.name} for adjunto in actividad.recursos_ids],
                    'destinatarios_tipo': actividad.destinatarios_tipo,
                    'estudiantes': [{'id': estudiante.id, 'nombre': estudiante.name} for estudiante in actividad.estudiantes_ids],
                    'curso': actividad.curso_id.name if actividad.curso_id else None,
                    'paralelo': actividad.paralelo,
                })

            return {'status': 'success', 'data': result}

        except Exception as e:
            _logger.error(f"Error al obtener actividades: {str(e)}")
            return {'status': 'error', 'message': 'Hubo un error al obtener las actividades.'}, 500

    @http.route('/api/actividades', type='json', auth='user', methods=['POST'], csrf=False)
    def create_actividad(self, **kwargs):
        """
        Crea una nueva actividad escolar.
        """
        try:
            data = request.jsonrequest

            nueva_actividad = request.env['school.actividad'].sudo().create({
                'titulo': data.get('titulo'),
                'descripcion': data.get('descripcion'),
                'fecha_entrega': data.get('fecha_entrega'),
                'recursos_ids': [(6, 0, data.get('recursos_ids', []))],  # IDs de los adjuntos
                'destinatarios_tipo': data.get('destinatarios_tipo'),
                'estudiantes_ids': [(6, 0, data.get('estudiantes_ids', []))],  # IDs de los estudiantes
                'curso_id': data.get('curso_id'),
                'paralelo': data.get('paralelo'),
            })

            return {
                'status': 'success',
                'data': {
                    'id': nueva_actividad.id,
                    'titulo': nueva_actividad.titulo,
                    'descripcion': nueva_actividad.descripcion,
                }
            }

        except Exception as e:
            _logger.error(f"Error al crear actividad: {str(e)}")
            return {'status': 'error', 'message': 'Hubo un error al crear la actividad.'}, 500

    @http.route('/api/actividades/<int:actividad_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_actividad(self, actividad_id, **kwargs):
        """
        Actualiza una actividad existente.
        """
        try:
            data = request.jsonrequest
            actividad = request.env['school.actividad'].sudo().browse(actividad_id)

            if not actividad.exists():
                return {'status': 'error', 'message': 'Actividad no encontrada.'}, 404

            actividad.sudo().write({
                'titulo': data.get('titulo', actividad.titulo),
                'descripcion': data.get('descripcion', actividad.descripcion),
                'fecha_entrega': data.get('fecha_entrega', actividad.fecha_entrega),
                'recursos_ids': [(6, 0, data.get('recursos_ids', []))] if 'recursos_ids' in data else actividad.recursos_ids,
                'destinatarios_tipo': data.get('destinatarios_tipo', actividad.destinatarios_tipo),
                'estudiantes_ids': [(6, 0, data.get('estudiantes_ids', []))] if 'estudiantes_ids' in data else actividad.estudiantes_ids,
                'curso_id': data.get('curso_id', actividad.curso_id.id),
                'paralelo': data.get('paralelo', actividad.paralelo),
            })

            return {
                'status': 'success',
                'data': {
                    'id': actividad.id,
                    'titulo': actividad.titulo,
                }
            }

        except Exception as e:
            _logger.error(f"Error al actualizar actividad: {str(e)}")
            return {'status': 'error', 'message': 'Hubo un error al actualizar la actividad.'}, 500

    @http.route('/api/actividades/<int:actividad_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_actividad(self, actividad_id, **kwargs):
        """
        Elimina una actividad.
        """
        try:
            actividad = request.env['school.actividad'].sudo().browse(actividad_id)

            if not actividad.exists():
                return {'status': 'error', 'message': 'Actividad no encontrada.'}, 404

            actividad.sudo().unlink()

            return {'status': 'success', 'message': 'Actividad eliminada exitosamente.'}

        except Exception as e:
            _logger.error(f"Error al eliminar actividad: {str(e)}")
            return {'status': 'error', 'message': 'Hubo un error al eliminar la actividad.'}, 500
