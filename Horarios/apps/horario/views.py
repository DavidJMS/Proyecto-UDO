from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from apps.horario import services as horario_services
from apps.horario import serializers as horario_serializers

class HorarioParticular(APIView):
    """
        
    """
    def post(self,request):
        try:
            horario = horario_services.guardar_horario_particular(request.data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = horario_serializers.HorarioParticular(horario,many=False).data
        serializer['detail'] = str("Has guardado correctamente el horario")
        return Response(serializer, status=status.HTTP_201_CREATED)

    def get(self,request,id):
        try:
            horario = horario_services.obtener_horario_particular(id)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = horario_serializers.HorarioParticular(horario,many=False).data
        serializer['detail'] = str("Has obtenido el horario correctamente")
        return Response(serializer, status=status.HTTP_200_OK)

@api_view(['POST'])
def GenerarHorarioParticular(request):
    try:
        horario = horario_services.iniciate(request.data)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(horario, status=status.HTTP_200_OK)

class HorarioGeneral(APIView):

    def post(self,request):
        try:
            horario_del_semestre = horario_services.registrar_horario_del_semestre(request.data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = horario_serializers.HorarioGeneral(horario_del_semestre,many=False).data
        serializer['detail'] = str("Has registrado un nuevo horario exitosamente")
        return Response(serializer, status=status.HTTP_201_CREATED)

    def get(self,request,id):
        try:
            horario_a_obtener = horario_services.obtener_horario_del_semestre(id=id)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = horario_serializers.HorarioGeneral(horario_a_obtener,many=False).data
        serializer['detail'] = str("Has obtenido el horario exitosamente")
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self,request,id):
        try:
            horario_services.eliminar_horario_del_semestre(id=id)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = str("Has eliminado el horario exitosamente")
        return Response(serializer, status=status.HTTP_200_OK)

    def put(self,request,id):
        try:
            horario_a_editar = horario_services.editar_horario_del_semestre(request.data,id)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = horario_serializers.HorarioGeneral(horario_a_editar,many=False).data
        serializer['detail'] = str("Has editado el horario exitosamente")
        return Response(serializer, status=status.HTTP_200_OK)