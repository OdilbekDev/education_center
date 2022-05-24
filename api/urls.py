from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('groups/', GroupView.as_view()),
    path('teachers/', TeacherView.as_view()),
    path('groups/filter/', Filter_Group),
    path('groups/get/<int:pk>', Get_Group),
    path('groups/search/', Search_Group),
    path('teachers/filter/', Filter_Teacher),
    path('teachers/filter/money/', Filter_Money_Teacher),
    path('pupils/<int:pk>', PupilView.as_view()),
    path('pupils/delete/<int:pk>', PupilDelView.as_view()),
    path('pupils/davomat/<int:pk>', Davomat),
    path('pupils/pay/', Payment_Pupil),
    path('teachers/payment/', Payment_Teacher),
    path('pupils/payment/filter/', Filter_Payment_Pupil),
    path('teachers/payment/filter/', Filter_Payment_Teacher),
    path('davomat/send/message/', Davomat_Bot),
    path('lessons/', LessonView.as_view())
]
