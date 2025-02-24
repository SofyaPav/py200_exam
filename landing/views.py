from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ContactForm

class LandingView(View):
    template_name = 'landing/index.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')

            response_data = {
                "name": data["name"],
                "email": data["email"],
                "message": data["message"],
                "ip": ip,
                "user_agent": user_agent,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"error": "Invalid form data"}, status=400)