from djoser.email import ActivationEmail
from django.conf import settings

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        frontend_url = settings.FRONTEND_URL 
        context["url"] = f"{frontend_url}{context['link']}" 
        return context
