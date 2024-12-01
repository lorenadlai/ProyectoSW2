from django.urls import path
from vehicular_requests.views import SaveRequestView, LoginView, VehicularRequestsByStatus, SendMessageToBot

urlpatterns = [
    path('save-request/', SaveRequestView.as_view(), name='save-request'),
    path('login/', LoginView.as_view(),  name='login'),
    path('vehicular-requests/', VehicularRequestsByStatus.as_view(), name='open-vehicular-requests'),
    path('send-message/', SendMessageToBot.as_view(), name='send_message_to_bot')
]