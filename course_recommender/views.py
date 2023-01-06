from django.db.models import Q
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import *

from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()


class AuthAPIView(APIView):
    permission_classes = [AnonPermissionOnly]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "You are already authenticated"}, status=400)
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if not username or not password:
            return Response({"detail": "Please specify a username and password"}, status=401)

        qs = User.objects.filter(Q(Q(username__exact=username) | Q(email__exact=username)), is_active=True).distinct()
        print(f'qs{qs}')
        if qs.count() == 1:
            user_obj = qs.first()
            print(user_obj)
            user = None
            if user_obj.check_password(password):
                user = user_obj
                print(user)

            if user is not None:
                payload = jwt_payload_handler(user)

                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                if response is not None:
                    print(f'response{response}')
                    return Response(response, status=200)
                return Response({"detail": "Invalid login details"}, status=401)
        return Response({"detail": "Invalid login details"}, status=401)


class StudentCreateAPIView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Student.objects.get_queryset().order_by('pk')
    permission_classes = [AnonPermissionOnly]
    serializer_class = StudentSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = User.objects.get(email=request.data['user']['email'])
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response = jwt_response_payload_handler(token, user, request=request)
        return Response(response, status=200)


class StudentDetailAPIView(generics.RetrieveUpdateAPIView, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'

    def get_object(self):
        kwargs = self.kwargs
        kw_id = kwargs.get('id')
        return Student.objects.get(user=kw_id)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, instance=request.user.customer,
                                         context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.object = self.get_object()

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourserListApiView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # def post(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


# class CourseDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     lookup_field = 'id'
#
#     def get_object(self):
#         kwargs = self.kwargs
#         kw_id = kwargs.get('id')
#         return Category.objects.get(id=kw_id)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class CategoryListAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_object(self):
        kwargs = self.kwargs
        kw_id = kwargs.get('id')
        return Category.objects.get(id=kw_id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
