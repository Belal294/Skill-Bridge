# users/email.py
from djoser.email import ActivationEmail
from django.conf import settings

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()
        frontend_url = settings.FRONTEND_URL  
        
        if context['url'].startswith('/'):
            context['url'] = context['url'][1:] 
        
    
        context["url"] = f"{frontend_url}/{context['url']}"
        # context["url"] = f"{context['url']}"
        
        print(" Activation link being sent:", context["url"])  
        
        return context
