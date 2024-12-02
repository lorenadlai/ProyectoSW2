from django.urls import path
from vehicular_requests.views import SaveRequestView, LoginView,PersonaDetallesView, VehicularRequestsByStatus, SendMessageToBot, UpdateStatusView, VehiculoDetallesView, VehiculosListView, IncidenciasAPIView

urlpatterns = [
    path('save-request/', SaveRequestView.as_view(), name='save-request'),
    path('login/', LoginView.as_view(),  name='login'),
    path('vehicular-requests/', VehicularRequestsByStatus.as_view(), name='open-vehicular-requests'),
    path('send-message/', SendMessageToBot.as_view(), name='send_message_to_bot'),
    path('update-status/', UpdateStatusView.as_view(), name='update-status'),
    path('vehiculo-detalles/', VehiculoDetallesView.as_view(), name='vehiculo-detalles'),
    path('get-all-vehiculos/', VehiculosListView.as_view(), name='get-all-vehiculos'),
    path('get_incidencias/', IncidenciasAPIView.as_view(), name='get_incidencias'),
    path('persona-detalles/', PersonaDetallesView.as_view(), name='persona_detalles'),
]