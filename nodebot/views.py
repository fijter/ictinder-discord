from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Message


@method_decorator(csrf_exempt, name='dispatch')
class MessageAPIView(View):
    """
    API View for sending messages to Discord users
    """
    def post(self, request, *args, **kwargs):
        if not request.POST.get('password') == settings.OWN_API_AUTH:
            return JsonResponse({'success': False, 'error': 'No valid authentication provided'}, status=403)

        if not request.POST.get('username'):
            return JsonResponse({'success': False, 'error': 'Please provide a username'}, status=400)
        
        if not request.POST.get('message'):
            return JsonResponse({'success': False, 'error': 'Please provide a message'}, status=400)
    
        Message(message=request.POST.get('message'), discord_id=request.POST.get('username')).save()
        return JsonResponse({'success': True}, status=201)
