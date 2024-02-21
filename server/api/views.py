from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ModelRefreshToken
from .auth import auth
class SignUpView(APIView):
    def post(self, request):
        # 사용자 입력값 가져오기
        userId = request.data.get('userId')
        userPassword = request.data.get('userPassword')
        email = request.data.get('email', '')  # 이메일이 없는 경우 빈 문자열로 처리

        # 입력값 유효성 검사
        if not userId or not userPassword:
            return Response({'error': 'userId와 userPassword는 필수 입력값입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 아이디 중복성 검사
        
        if User.objects.filter(username=userId).exists():
            return Response({'error': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

        # 새로운 사용자 생성 및 저장
        try:
            user = User.objects.create_user(username=userId, email=email, password=userPassword)
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        # 사용자 입력값 가져오기
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        # 사용자 인증
        user = authenticate(username=username, email=email, password=password )
        print(user)
        if user is not None:
            # 사용자 인증 성공시 리프레시 토큰 생성
            # rest_framework_simplejwt에서 제공하는 RefreshToken 클래스를 사용하여 리프레시 토큰 생성
            refresh = RefreshToken.for_user(user)

            try:
                # 이미 존재하는 레코드를 가져옵니다.
                entry_refresh_token = ModelRefreshToken.objects.get(user=user)
            except ModelRefreshToken.DoesNotExist:
                # 존재하지 않는 경우에는 새로운 레코드를 생성합니다.
                entry_refresh_token = ModelRefreshToken.objects.create(
                    user=user,
                    refresh_token=str(refresh)
                )
            else:
                # 이미 존재하는 경우에는 해당 레코드의 필드를 업데이트합니다.
                entry_refresh_token.refresh_token = str(refresh)
                entry_refresh_token.save()

            # refresh_key로 해당하는 RefreshToken 인스턴스를 생성
            refresh_token_instance = ModelRefreshToken.objects.get(refresh_token=refresh)
            index_refresh = refresh_token_instance.user_id
            user_id = refresh_token_instance.user
            accessToken = refresh.access_token
            return Response({'message': '로그인 성공',
                            'accessToken': str(accessToken),
                            'refreshIndex': str(index_refresh)})
        else:
            # 사용자 인증 실패
            return Response({'error': '유효하지 않은 사용자 정보입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

from .auth import verify_token

class Auth(APIView):
    def post(self, request):
        return auth(request)
    
    
def index(request):
    return HttpResponse("Hello, world. You're at the api index.")