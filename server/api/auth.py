import requests
from rest_framework.response import Response
from rest_framework import status
from .models import ModelRefreshToken

def verify_token(token):
    url = 'http://localhost:8000/api/token/verify/'
    response = requests.post(url, data={'Token': token})
    return response.status_code == 400
    
def get_refresh_token(index):
    try:
        # 리프레시 토큰 가져오기.
        refresh_token = ModelRefreshToken.objects.get(user_id=index)
        return refresh_token
    except:
        # 못 가져올 경우
        return ConnectionError
    
def re_generate_access_token(refresh_token):
    url = 'http://localhost:8000/api/token/refresh/'
    try:
        response = requests.post(url, data={'refresh': refresh_token})
        return response.json()['access']
    except:
        return ConnectionError

# Full Logic  
def auth(request):
    # 토큰 가져오기
    token = request.headers.get('Authorization')
    index = request.headers.get('refreshIndex')
    # 토큰 유효성 검사
    if verify_token(token):
        return Response({'message': 'token is valid', 'new_token': ""}, status=status.HTTP_200_OK)
    else: # 토큰 만료시
        refresh_token = get_refresh_token(index)
        # 리프레시 유효성 검사
        if verify_token(refresh_token):
            # 리프레시 유효: 리프레시로 새로운 토큰 생성
            new_token = re_generate_access_token(refresh_token)
            return Response({'message': 'token is expired', 'new_token': new_token}, status=status.HTTP_200_OK)
        else:
            # 리프레시 유효하지 않을 때
            return Response({'message': 'refresh token is expired, need to login', 'new_token': ""}, status=status.HTTP_401_UNAUTHORIZED)
