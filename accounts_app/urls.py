from django.urls import path
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from school_inventory import settings
from accounts_app.views import ( RegisterView, StudentView, LoginView,
                    lecturerView, )


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    
    path('api/token/register/', RegisterView.as_view(), name='sign_up'),
    path('api/token/login/', LoginView.as_view(), name='sign_in'),
    path('api/token/students/<int:user__id>/', StudentView.as_view(), name='student_details'),
    path('api/token/lecturers/<int:user__id>/', lecturerView.as_view(), name='lecturer_details'),
]