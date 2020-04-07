from django.contrib import admin
from django.urls import path, include
from apps.horario import views 

urlpatterns = [
    path('particular/guardar', views.HorarioParticular.as_view(), name='guardar_horario_particular'),
    path('particular/generar/', views.GenerarHorarioParticular, name='generar_horario_particular'),
    path('particular/obtener/<int:id>', views.HorarioParticular.as_view(), name='obtener_horario_particular'),
    path('general/eliminar/<int:id>', views.HorarioGeneral.as_view(), name='eliminar_horario_general'),
    path('general/editar/<int:id>', views.HorarioGeneral.as_view(), name='editar_horario_general'),
    path('general/registrar/',views.HorarioGeneral.as_view(), name='registrar_horario_general'),
    path('general/obtener/<int:id>', views.HorarioGeneral.as_view(), name='obtener_horario_general'),
]