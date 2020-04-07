from django.db import models

"""
	Horarios general de cada carrera por semestre, contiene el horario de cada materia,
	en sus diferentes secciones .
"""
class HorarioGeneral(models.Model):
    id 			= models.AutoField(primary_key=True) 
    carrera     = models.CharField(max_length=30,null=True)
    fecha       = models.DateTimeField(auto_now=False, auto_now_add=False,null=True,blank=True)
    horario    	= models.TextField(null=False, blank=True)
    def __str__(self):
        return self.carrera


"""
	Horario representativo para cada alumno, se borrara cada 6 meses.
"""
class HorarioParticular(models.Model):

    id 			= models.AutoField(primary_key=True)
    horario     = models.TextField(null=False, blank=True)
    puntuacion  = models.IntegerField(null=True)
    creditos    = models.IntegerField(null=True)
    carrera     = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.id