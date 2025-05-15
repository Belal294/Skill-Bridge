
from djoser.email import ActivationEmail
from django.conf import settings

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        
        context = super().get_context_data()
        print("check:", context["url"])
        frontend_url = settings.FRONTEND_URL 
        print("check2343", frontend_url) 
        
        if context['url'].startswith('/'):
            context['url'] = context['url'][1:] 
        
        a = frontend_url
        b = context["url"]
        # context["url"] = f"{a}/{b}"
        context["url"] = f"{context['url']}"
        
        
        print("Activation link being sent:", context["url"])  
        
        return context
