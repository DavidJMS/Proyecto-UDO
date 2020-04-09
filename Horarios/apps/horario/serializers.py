import serpy

class HorarioParticular(serpy.Serializer):
    id 		= serpy.Field()
    horario = serpy.Field()
		
class HorarioGeneral(serpy.Serializer):
	id 		= serpy.Field()
	carrera = serpy.Field()
	horario = serpy.Field()
	fecha 	= serpy.Field()

		