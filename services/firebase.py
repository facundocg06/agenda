import firebase_admin
from firebase_admin import credentials, messaging
import logging
import os

_logger = logging.getLogger(__name__)

class FirebaseNotification:
    @staticmethod
    def initialize_firebase():
        """Inicializa Firebase si no está ya inicializado."""
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), '../config/sw1-p2-odoo-firebase-adminsdk-yylv8-14cd24107e.json'))
            firebase_admin.initialize_app(cred)

    @staticmethod
    def send_notification(title, body, data=None, token=None):
        """Envía una notificación push a través de FCM.

        :param title: Título de la notificación.
        :param body: Cuerpo de la notificación.
        :param data: Diccionario con datos adicionales.
        :param token: Token del dispositivo destino.
        """
        try:
            FirebaseNotification.initialize_firebase()

            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=token,
            )
            response = messaging.send(message)
            _logger.info(f'Notificación enviada con éxito: {response}')
            return response
        except Exception as e:
            _logger.error(f'Error al enviar la notificación: {e}')
            return None
