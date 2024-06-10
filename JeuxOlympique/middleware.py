import datetime
import json
from django.conf import settings
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        current_time = datetime.datetime.now()
        last_activity_str = request.session.get('last_activity')
        if last_activity_str:
            last_activity = datetime.datetime.fromisoformat(last_activity_str)
            elapsed_time = (current_time - last_activity).total_seconds()
            if elapsed_time > settings.SESSION_COOKIE_AGE:
                logout(request)
                request.session.flush()

        # Convertir l'objet datetime en chaîne de caractères avant de le stocker dans la session
        request.session['last_activity'] = current_time.isoformat()
