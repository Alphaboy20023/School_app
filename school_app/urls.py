from django.urls import path

from school_inventory import settings
from school_app.views import (PaymentView, IdCardView, ResultView,
                    AnnouncementView, PostView, RepostView, CommentView, LectureView, ExamView,
                    NotificationView, DepartmentView, CalendarView, CourseView  )


urlpatterns = [
    path('api/token/payments/', PaymentView.as_view(), name='payments'),
    path('api/token/identity-cards/', IdCardView.as_view(), name='Id_cards'),
    path('api/token/departments/', DepartmentView.as_view(), name='departments'),
    path('api/token/courses/', CourseView.as_view(), name='courses'),
    path('api/token/exams/', ExamView.as_view(), name='exams'),
    path('api/token/results/', ResultView.as_view(), name='view_result'),
    path('api/token/lectures/', LectureView.as_view(), name='lectures'),
    path('api/token/posts/', PostView.as_view(), name='posts'),
    path('api/token/notifications/', NotificationView.as_view(), name='notifications'),
    path('api/token/reposts/', RepostView.as_view(), name='reposts'),
    path('api/token/comments/', CommentView.as_view(), name='comments'),
    path('api/token/public-announcements/<int:pk>/', AnnouncementView.as_view(), name='public_announcements'),
    path('api/token/calendars/', CalendarView.as_view(), name='calendars'),
]