from rest_framework              import generics, status
from rest_framework.response     import Response
from rest_framework.views        import APIView
from rest_framework.permissions  import IsAuthenticated, AllowAny

from .models       import User
from .serializers  import RegisterSerializer, UserSerializer, UpdateUserSerializer
from .permissions  import IsAdmin


class RegisterView(generics.CreateAPIView):
    """POST /api/users/register/  — public endpoint"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'User registered successfully.',
                'user':    UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED
        )


class UserListView(generics.ListAPIView):
    """GET /api/users/  — admin only"""
    serializer_class   = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset           = User.objects.all().order_by('-created_at')


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    GET    /api/users/<id>/  — admin only
    PATCH  /api/users/<id>/  — admin only (update role / active status)
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset           = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateUserSerializer
        return UserSerializer


class MeView(APIView):
    """GET /api/users/me/  — any authenticated user (see their own profile)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)