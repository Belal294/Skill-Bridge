from djoser.email import ActivationEmail
from django.conf import settings

class CustomActivationEmail(ActivationEmail):
    def get_context_data(self):
        context = super().get_context_data()

        # Optional: remove leading slash if exists
        if context['url'].startswith('/'):
            context['url'] = context['url'][1:]

        # Proper activation link
        context["url"] = f"/activate/{context['uid']}/{context['token']}"
        
        print("Activation link being sent:", context["url"])  
        return context
