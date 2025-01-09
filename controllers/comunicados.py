from odoo import http
from odoo.http import request, Response

from datetime import datetime, timedelta
from odoo import http
from odoo.http import request

class ComunicadoController(http.Controller):

    @http.route('/api/comunicados', type='json', auth='user', methods=['GET'])
    def get_comunicados(self, **kwargs):
        """
        Endpoint para obtener la lista de comunicados filtrados por fecha.
        :param fecha: Fecha en formato 'YYYY-MM-DD' (obligatoria).
        :param kwargs: Otros parámetros opcionales.
        :return: JSON con la lista de comunicados.
        """
        try:
            # Convertir la fecha pasada como parámetro a un objeto datetime
            fecha = request.get_http_params()["fecha"]
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            print(fecha_obj)

            # Recuperar los comunicados de la base de datos cuya fecha_envio coincida
            comunicados = request.env['school.comunicado'].sudo().search([
                ('fecha_envio', '>=', fecha_obj.replace(hour=0, minute=0, second=0, microsecond=0)),
                ('fecha_envio', '<', (fecha_obj + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0))
            ])


            # Construir la respuesta
            data = []
            for comunicado in comunicados:
                data.append({
                    'id': comunicado.id,
                    'asunto': comunicado.asunto,
                    'contenido': comunicado.contenido,
                    'fecha_envio': comunicado.fecha_envio.strftime('%Y-%m-%d %H:%M:%S'),
                    'destinatarios_tipo': comunicado.destinatarios_tipo,
                    'estudiantes': [{'id': e.id, 'name': e.name} for e in comunicado.estudiantes_ids],
                    'curso': comunicado.curso_id.name if comunicado.curso_id else None,
                    'paralelo': comunicado.paralelo if comunicado.paralelo else None,
                    'archivos': [{'id': a.id, 'name': a.name, 'url': f'/web/content/{a.id}'} for a in comunicado.archivos_ids],
                })

            return {
                'status': 'success',
                'data': data
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

