from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()


class SendPassword(APIView):
    def post(self, request):
        email = request.data['email']
        password = User.objects.make_random_password()
        new = User.create(username=email)
        new.set_password(password)
        new.save()

        send_mail(
            'Getting JWT',
            f'Use by request following data:\n"email": "{new.username}", "confirmation_code": "{new.password}"',
            'from@example.com',
            ['to@example.com'],
        )
        return Response(data={'ok': 'ok'}, status=status.HTTP_200_OK)
