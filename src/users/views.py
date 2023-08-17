import random
import time
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from datetime import datetime
import string
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

last_request_time = None
last_sent_code = None


def generate_invite_code():
    invite_code = ''.join(random.choices(string.digits, k=2))
    invite_code += ''.join(random.choices(string.ascii_letters, k=3))
    invite_code += ''.join(random.choices(string.digits + string.ascii_letters, k=1))
    return invite_code

def is_valid_phone_number(phone_number):
    return (
        phone_number
        and phone_number.startswith('+7')
        and len(phone_number) == 11
        and phone_number[1:].isdigit())


def generate_authorization_code():
    return str(random.randint(1000, 9999))


def send_authorization_code(phone_number, authorization_code):
    # Здесь можно добавить логику для отправки кода на телефон
    time.sleep(1)


@api_view(['POST'])
def request_phone_number(request):
    global last_request_time, last_sent_code

    phone_number = request.data.get('phone_number')

    if not is_valid_phone_number(phone_number):
        return Response(
            {'message': 'Invalid phone number format ru +7.'},
            status=status.HTTP_400_BAD_REQUEST)

    current_time = datetime.now()

    if last_request_time and (current_time - last_request_time).seconds < 30:
        return Response(
            {'message': 'Please wait 30 seconds before requesting a new code'},
            status=status.HTTP_429_TOO_MANY_REQUESTS)

    if CustomUser.objects.filter(phone_number=phone_number).exists():
        return Response(
            {'message': 'User already exists'},
            status=status.HTTP_400_BAD_REQUEST)
    authorization_code = generate_authorization_code()
    send_authorization_code(phone_number, authorization_code)

    request.session['phone_number'] = phone_number
    request.session['authorization_code'] = authorization_code
    last_request_time = current_time
    last_sent_code = authorization_code

    response_data = {
        'message': 'Authorization code sent',
        'phone_number': phone_number,
        'authorization_code': authorization_code
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_code(request):
    phone_number = request.data.get('phone_number')
    received_code = request.data.get('code')
    saved_phone_number = request.session.get('phone_number')
    saved_authorization_code = request.session.get('authorization_code')

    if not is_valid_phone_number(phone_number):
        return Response(
            {'message': 'Invalid phone number format'},
            status=status.HTTP_400_BAD_REQUEST)

    if (phone_number
        != saved_phone_number
        or received_code != saved_authorization_code):
        return Response(
            {'message': 'Invalid authorization code'},
            status=status.HTTP_400_BAD_REQUEST)

    user, created = CustomUser.objects.get_or_create(
        phone_number=phone_number,
        activation_code=saved_authorization_code
    )
    if created:
        invite_code = generate_invite_code()
        user.invite_code = invite_code
        user.save()

        # Создание токена аутентификации
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'message': 'User registered', 'token': token.key},
                        status=status.HTTP_201_CREATED)
    else:
        # Если пользователь уже существует, проверьте, есть ли у него токен.
        try:
            token = Token.objects.get(user=user)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user)

        return Response({'message': 'User logged in', 'token': token.key},
                        status=status.HTTP_200_OK)


@api_view(['GET'])
def user_profile(request):
    user = request.user
    profile_data = {
        'phone_number': user.phone_number,
        'invite_code': user.invite_code,
        'activated_invite_code': user.activated_invite_code
    }
    return Response(profile_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def activate_invite_code(request):
    user = request.user
    received_invite_code = request.data.get('invite_code')

    if user.activated_invite_code:
        return Response(
            {'message': 'You have already activated an invite code'},
            status=status.HTTP_400_BAD_REQUEST)

    try:
        invite_code_owner = CustomUser.objects.get(
            invite_code=received_invite_code)
    except CustomUser.DoesNotExist:
        return Response(
            {'message': 'Invalid invite code'},
            status=status.HTTP_400_BAD_REQUEST)

    if invite_code_owner == user:
        return Response(
            {'message': "You can't activate your own invite code"},
            status=status.HTTP_400_BAD_REQUEST)

    invite_code_owner.activated_invite_code =user.invite_code
    invite_code_owner.save()

    return Response(
        {'message': 'Invite code activated successfully'},
        status=status.HTTP_200_OK)


@api_view(['GET'])
def invited_users_list(request):
    user = request.user
    invited_users = CustomUser.objects.filter(
        activated_invite_code=user.invite_code)
    user_list = [{'phone_number': invited_user.phone_number} for invited_user in invited_users]
    return Response(user_list, status=status.HTTP_200_OK)