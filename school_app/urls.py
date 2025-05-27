from django.urls import path
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from school_inventory import settings
from .views import ( RegisterView, StudentView, PaymentView, LoginView, IdCardView, ResultView,
                    AnnouncementView, PostView, RepostView, CommentView, LectureView, ExamView,
                    lecturerView, NotificationView, DepartmentView  )


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/register/', RegisterView.as_view(), name='sign_up'),
    path('api/token/login/', LoginView.as_view(), name='sign_in'),
    path('api/token/students/<int:user__id>/', StudentView.as_view(), name='student_details'),
    path('api/token/lecturers/<int:user__id>/', lecturerView.as_view(), name='lecturer_details'),
    path('api/token/payments/', PaymentView.as_view(), name='payments'),
    path('api/token/identity-cards/', IdCardView.as_view(), name='Id_cards'),
    path('api/token/departments/', DepartmentView.as_view(), name='departments'),
    path('api/token/announcements/<int:pk>/', AnnouncementView.as_view(), name='public_announcements'),
    path('api/token/posts/', PostView.as_view(), name='posts'),
    path('api/token/notifications/', NotificationView.as_view(), name='notifications'),
    path('api/token/reposts/', RepostView.as_view(), name='reposts'),
    path('api/token/comments/', CommentView.as_view(), name='comments'),
    path('api/token/lectures/', LectureView.as_view(), name='lectures'),
    path('api/token/exams/', ExamView.as_view(), name='exams'),
    path('api/token/results/', ResultView.as_view(), name='view_result'),
] + static(settings.MEDIA_URL,
           document_root = settings.MEDIA_ROOT)