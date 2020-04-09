from apps.horario import models as horario_models
from apps.horario import serializers as horario_serializers
from django.db import transaction
from apps.horario import validations as horario_validations
import json

def registrar_horario_del_semestre(data:dict)->horario_models.HorarioGeneral:
    """
        Servicio para registrar los horarios semestralmente

        :parametro data: contiene la informacion y los campos que seran guardados
        :tipo de parametro data: dict
        :return: un nuevo horario
        :raises: ValueError

        Validaciones implicitas:
        1.El tamaño del campo "carrera" sea el apropiado y este dentro de las opciones disponibles
        2.La fecha tenga el formato correcto
    """
    if data.get('carrera') is not None:
        horario_validations.validate_carrera(data.get('carrera'))
    else:
        raise ValueError(str("Debe de indicar para que carrera es este horario"))
    if data.get('fecha') is not None:
        horario_validations.validate_fecha(data.get('fecha'))
    else:
        raise ValueError(str("Debe de indicar para que semestre es el horario por medio de la fecha"))
    with transaction.atomic():
        try:
            nuevo_horario = horario_models.HorarioGeneral.objects.create(
                carrera = data.get('carrera').lower(),
                horario = data.get('horario'),
                fecha   = data.get('fecha')
            )
        except Exception as e:
            raise ValueError(e)
    return nuevo_horario

def eliminar_horario_del_semestre(id:int):
    """
        Servicio para eliminar los horarios de cada periodo semestral por el id

        :parametro id: es el id del objeto horario en la tabla a eliminar
        :tipo de parametro id: int
        :raises: ValueError

        Validaciones implicitas:
        1.El objeto solicitado exista
    """
    try:
        horario_a_eliminar = horario_models.HorarioGeneral.objects.get(id=id)
        with transaction.atomic():
            horario_a_eliminar.delete()
    except horario_models.HorarioGeneral.DoesNotExist:
        raise ValueError(str("El horario solicitado no existe"))
    except Exception as e:
        raise ValueError(str("Hubo un error eliminando el horario"))

def obtener_horario_del_semestre(id:int)->horario_models.HorarioGeneral:
    """
        Servicio para obtener horarios por medio de su id

        :parametro id: es el id del objeto horario en la tabla a obtener
        :tipo de parametro id: int
        :raises: ValueError
        :return: HorarioGeneral

        Validaciones implicitas:
        1.El objeto solicitado exista
    """
    try:
        horario = horario_models.HorarioGeneral.objects.get(id=id)
    except horario_models.HorarioGeneral.DoesNotExist:
        raise ValueError(str("El horario solicitado no existe"))
    except Exception as e:
        raise ValueError(str("Hubo un error al obtener el horario"))
    return horario

def editar_horario_del_semestre(data:dict,id:int)->horario_models.HorarioGeneral:
    """
        Servicio para editar horarios por medio de su id
        
        :parametro data: contiene la informacion para editar el horario
        :tipo de parametro data: dict
        :parametro id: es el id del objeto horario en la tabla a obtener
        :tipo de parametro id: int
        :raises: ValueError
        :return: HorarioGeneral

        Validaciones implicitas:
        1.El horario exista.
        2.La fecha este en el formato correcto.
        3.El tamaño del campo "carrera" sea el apropiado y este dentro de las opciones disponibles
    """
    try:
        horario_a_editar = horario_models.HorarioGeneral.objects.get(id=id)
        if data.get('carrera') is not None:
            horario_validations.validate_carrera(data.get('carrera'))
            horario_a_editar.carrera = data.get('carrera').lower()
        if data.get('horario') is not None:
            horario_a_editar.horario = data.get('horario')
        if data.get('fecha') is not None:
            horario_validations.validate_fecha(data.get('fecha'))
            horario_a_editar.fecha = data.get('fecha')
        with transaction.atomic():
            horario_a_editar.save()
    except horario_models.HorarioGeneral.DoesNotExist:
        raise ValueError(str('El horario solicitado no existe'))
    except Exception as e:
        raise ValueError(str('Hubo un error editando el horario'))
    return horario_a_editar

def guardar_horario_particular(data:dict) -> horario_models.HorarioParticular:
    """
        Servicio para guardar horarios generados por el sistema
        
        :parametro data: contiene la informacion de las materias las secciones y los horarios a guardar
        :tipo de parametro data: dict
        :raises: ValueError
        :return: HorarioParticular

        Validaciones implicitas:
        1.El horario exista.
        2.La fecha este en el formato correcto.
        3.El tamaño del campo "carrera" sea el apropiado y este dentro de las opciones disponibles   
    """
    with transaction.atomic():
        try:
            new_schedule = horario_models.HorarioParticular.objects.create(
                horario = data
            )
        except Exception as e:
                raise ValueError(str('Hubo un error guardando el horario'))
    return new_schedule


def obtener_horario_particular(id:int) -> horario_models.HorarioParticular:
    """
        Servicio para obtener horarios generados por el sistema por medio de su id
        
        :parametro id: id del horario 
        :tipo de parametro id: int
        :raises: ValueError
        :return: HorarioParticular

        Validaciones implicitas:
        1.El horario exista.
    """
    try:
         horario = horario_models.HorarioParticular.objects.get(id=id)
    except horario_models.HorarioParticular.DoesNotExist:
        raise ValueError(str("El horario no existe"))
    except Exception as e:
        raise ValueError(e)
    return horario


def eliminar_horarios():
    """
        Servicio para eliminar todos los horarios generados por el sistema para un perido semestral
        
        :raises: ValueError
    """
    try:
        with transaction.atomic():
            horario_models.HorarioParticular.objects.all().delete()
    except Exception as e:
        raise ValueError("Hubo un error eliminando los horarios")



def iniciate(materiasPorCursarDiccionario:dict):
    Horario = Pensum(materiasPorCursarDiccionario) 
    Horario.generarTodasPosibilidades()
    #print('------------------ peto -----------------')
    resultado = Horario.asignaPuntuacion()
    #return resultado
    #Horario2 = HorarioServicio()
    #Horario2.cargar_horario(5)
    # Aqui va un ciclo
    #resultado =Horario2.comprobarCombinacionHorario(resultado[0]['combinacion'])
    return resultado

class Pensum():
    """
        Clase de hoarios a generar
    """
    datos:list
    materiasPorCursar:list 
    electivasElejidas:list 
    minimoCreditos:int    
    limiteCreditos:int 
    creditosaprobados:int
    posiblesCombinaciones=[]
    tamanioMateriasPorCursar:int 
    tamanioGrupo:int=0
    tamanioMinimoGrupo:int=0
    contadorCreditos:int=0  
    contador:int=1
    valorparaordenar:int=0
    cuentame:int=0
    sumaCreditos:int= 0
    posiblesCombinacionesPuntuadas:list
    carrera:str
    ciclo:int = 0

    def __init__(self,materiasPorCursarDiccionario):
        self.datos = horario_validations.validate_datos(materiasPorCursarDiccionario)
        self.materiasPorCursar = horario_validations.validate_lista(materiasPorCursarDiccionario)
        self.electivasElejidas = horario_validations.validate_lista_electivas_elejidas(self.materiasPorCursar)
        self.materiasPorCursar = horario_validations.validate_lista_mayor(self.materiasPorCursar,len(self.materiasPorCursar))
        self.minimoCreditos    = self.datos[0]['minimoCreditos']
        self.limiteCreditos    = self.datos[0]['limiteCreditos']
        self.creditosaprobados = self.datos[0]['creditosaprobados']
        self.tamanioMateriasPorCursar = len(self.materiasPorCursar)
        self.carrera = self.datos[0]['carrera']

    def generarTodasPosibilidades(self):
        """
            materias contine el codigo de las materias que se pueden
        """
        try:
            for materia in self.materiasPorCursar:
                self.contadorCreditos = self.contadorCreditos + materia['creditos']
                if self.contadorCreditos <= self.minimoCreditos:
                    self.tamanioMinimoGrupo+=1
                elif self.contadorCreditos >= self.limiteCreditos:
                    break
                self.contador+=1
            if self.contadorCreditos >= self.limiteCreditos:
                if self.contadorCreditos == self.limiteCreditos:
                    self.tamanioGrupo = self.contador
                else:
                    self.tamanioGrupo = self.contador - 1
            else:
                self.tamanioGrupo = self.tamanioMateriasPorCursar
            self.contadorCreditos = 0
            self.contador = 1
            self.materiasPorCursar = horario_validations.validate_lista_menor(self.materiasPorCursar)
            for materia in self.materiasPorCursar:
                self.contadorCreditos = self.contadorCreditos + materia['creditos']
                if(self.contadorCreditos>=self.minimoCreditos):
                     break
                self.contador+=1
            if (self.contadorCreditos >= self.minimoCreditos):
                self.tamanioMinimoGrupo = self.contador
            else:
                self.tamanioMinimoGrupo = 1
            while(self.tamanioGrupo+1 >= self.tamanioMinimoGrupo):
                self.generarPermutacionNoSust(self.materiasPorCursar, self.tamanioMateriasPorCursar, [], self.tamanioGrupo,self.electivasElejidas)
                self.tamanioGrupo-=1
                self.cuentame+=1
            return 0
            if(len(self.posiblesCombinaciones) == 0):
                self.sumaCreditos= 0
            for materia in  self.materiasPorCursar:
                self.sumaCreditos += materia['creditos']
            veces=1
            while(self.sumaCreditos > 18):
                self.sumaCreditos -= self.materiasPorCursar[self.tamanioMateriasPorCursar - veces]['creditos']
                veces+=1
        except ValueError as e:
            raise ValueError(str('Hubo un problema en el request'))

    def generarPermutacionNoSust(self,elementos:dict, tamanioMateriasPorCursar:int, actual:list, cantidad:int,electivasElejidas:list):
        if(cantidad==0):
            electivasIncluidas:int=0
            for electiva in electivasElejidas:
                for indice in actual:
                    if indice['codigo']==electiva['codigo']:
                        electivasIncluidas+=1
                        break
            if(electivasIncluidas == len(electivasElejidas)):  
                compruebaexisteciabool=self.compruebaExistencia(actual)
                if(not compruebaexisteciabool):
                    compruebacreditosbool = self.CompruebaCreditos(actual)
                    if(compruebacreditosbool):
                        self.posiblesCombinaciones.append(actual)
                        elementos.append(actual)
                        self.ciclo +=1
        else:
            for i in range(0,tamanioMateriasPorCursar):
                resultado = elementos[i] in actual
                if resultado == False:
                    cantidad2= cantidad - 1
                    elemento_lista = [elementos[i]]
                    self.ciclo +=1
                    self.generarPermutacionNoSust(elementos, tamanioMateriasPorCursar, actual+elemento_lista,cantidad2,electivasElejidas)                    


    def compruebaExistencia(self,combinacion:list):
        tamanioPosiblesCombinaciones:int = len(self.posiblesCombinaciones)
        tamanioCombinacion:int = len(combinacion)
        for comparacombinacion in self.posiblesCombinaciones:
            if(tamanioCombinacion == len(comparacombinacion)):
                coincidencias=0
                for i in range(tamanioCombinacion):
                    if not combinacion[i] in comparacombinacion:
                        break
                    coincidencias+=1
                    if(coincidencias == tamanioCombinacion):
                        return True
        return False
            
    def CompruebaCreditos(self,combinacion:list):
        suma =0
        for materia in combinacion:
            suma = suma + materia['creditos']
            if(suma > self.limiteCreditos):
                return False
        if(suma < self.minimoCreditos):
            return False
        return True

    def asignaPuntuacion(self):
        nivel = round(((self.creditosaprobados/132)*10))
        combinacionesPuntuadas=[]
        for combinacion in self.posiblesCombinaciones:
            puntosCombinacion=0
            materiasADesbloquear= self.cantidadMateriasADesbloquear(combinacion)
            numeroCreditos= self.creditosCombinacion(combinacion)
            puntosNivel= self.puntosPorNivel(combinacion,nivel)
            puntosCombinacion = ((materiasADesbloquear*10)*0.5) + ((numeroCreditos*10)*0.4) + ((puntosNivel*10)*0.1)
            combinacionesPuntuadas.append({
            'combinacion': combinacion,
            'puntaje': puntosCombinacion})
        return combinacionesPuntuadas
  
    def creditosCombinacion(self,combinacion):
        creditos:int=0
        for materia in combinacion:
            creditos += materia['creditos']
        return creditos
  

    def puntosPorNivel(self,combinacion:list, nivel:int):
        puntos:int = 0
        for materia in combinacion:
            if(materia['semestre'] != 99 and materia['semestre'] != 88):
                if(materia['semestre'] <= nivel):
                    pass
                else:
                    diferencia = materia['semestre'] - nivel
                    if(diferencia>2):
                        puntos -= diferencia
        return puntos

    def cantidadMateriasADesbloquear(self,combinacion):
        desbloqueadas:list= self.secuenciaDesbloqueo(combinacion)
        delPensum=0
        electivas=0
        for materia in desbloqueadas:
            if(materia['semestre'] != 99 and materia['semestre']!=88):
                delPensum+=1
            else:
                electivas+=1
        return delPensum + (electivas/2)

    def secuenciaDesbloqueo(self,combinacion:list):
        pensum = horario_validations.validate_pensum(self.carrera)
        agregada = True
        desbloqueadas = []
        materiasDesbloqueadas=[]
        TAMANIOPENSUM:int= len(pensum)
        while(agregada==True):
            agregada=False
            k=0
            for j in range(len(combinacion)):
                l=0
                for i in range(TAMANIOPENSUM):
                    if pensum[l]['presedentes']['p2'] == '' and pensum[l]['presedentes']['p1'] != '':
                        if combinacion[k]['codigo'] == pensum[l]['presedentes']['p1'] and not pensum[l]['aprobada']:
                            desbloqueadas.append(pensum[l])
                            pensum[l]['aprobada'] = True
                            agregada = True
                    l+=1
                k+=1
            for i in range(TAMANIOPENSUM):
                if pensum[i]['presedentes']['p2'] != '' and pensum[i]['presedentes']['p1'] != '':
                    coincide=0
                    mats:list=[]
                    for materia in combinacion:
                        if pensum[i]['presedentes']['p1'] == materia['codigo'] or pensum[i]['presedentes']['p2'] == materia['codigo']:
                            if not pensum[i]['aprobada']:
                                coincide+=1
                                mats.append(materia)
                                if coincide==2:
                                    desbloqueadas.append(pensum[i])
                                    pensum[i]['aprobada']=True
                                    agregada =True
                                    coincide=0
                                    mats=[]
            if len(desbloqueadas)==0:
                agregada = False
            else:
                combinacion = desbloqueadas
                materiasDesbloqueadas = materiasDesbloqueadas+desbloqueadas
                desbloqueadas=[]
        return materiasDesbloqueadas