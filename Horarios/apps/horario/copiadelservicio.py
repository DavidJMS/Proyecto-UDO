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
    HorarioCombinacion = Pensum(materiasPorCursarDiccionario) 
    HorarioCombinacion.generarTodasPosibilidades()
    resultado = HorarioCombinacion.asigna_puntuacion()
    #HorarioPersonal = Horario()
    #HorarioPersonal.cargar_horario(5) #Cambiar esto por un verdaero id que se le pase el nombre mejor de la carrera
    #resultado = HorarioPersonal.comprobar_combinacion_horario(resultado[0]['combinacion'])
    return resultado

class Pensum():
    """
        Clase de Pensum para delimitar en que nivel de la carrera se encuentra la petición
        en que carrera y encontrar la mejor combinación de materias la cual cumpla con
        la mayor cantidad de créditos posibles, pasando esta combinacion por un sistema
        de puntuación y filtros.
    """
    datos:list
    materias_por_cursar:list 
    electivas_elejidas:list 
    minimo_creditos:int    
    limite_creditos:int 
    creditos_aprobados:int
    posibles_combinaciones:list=[]
    tamanio_materias_Por_cursar:int 
    tamanio_grupo:int=0
    tamanio_minimo_grupo:int=0
    contador_creditos:int=0  
    contador:int=1
    valor_para_ordenar:int=0
    cuentame:int=0
    suma_creditos:int= 0
    posibles_combinaciones_puntuadas:list
    carrera:str
    ciclo:int = 0
    tamanio_new_combinacion=0

    def __init__(self,materias_por_cursar_diccionario:dict):
        self.datos = horario_validations.validate_datos(materias_por_cursar_diccionario)
        self.materias_por_cursar = horario_validations.validate_lista(materias_por_cursar_diccionario)
        self.electivas_elejidas  = horario_validations.validate_lista_electivas_elejidas(self.materias_por_cursar)
        self.materias_por_cursar = horario_validations.validate_lista_mayor(self.materias_por_cursar,len(self.materias_por_cursar))
        self.minimo_creditos     = self.datos[0]['minimoCreditos']
        self.limite_creditos     = self.datos[0]['limiteCreditos']
        self.creditos_aprobados  = self.datos[0]['creditosaprobados']
        self.tamanio_materias_por_cursar = len(self.materias_por_cursar)
        self.carrera = self.datos[0]['carrera']

    def generarTodasPosibilidades(self):
        """
            Comienza el proceso para generar las posibles combinaciones, es la encargada de
            rellenar la lista de combinaciones finalistas.
        """
        try:
            for materia in self.materias_por_cursar:
                self.contador_creditos = self.contador_creditos + materia['creditos']
                if self.contador_creditos <= self.minimo_creditos:
                    self.tamanio_minimo_grupo+=1
                elif self.contador_creditos >= self.limite_creditos:
                    break
                self.contador+=1
            if self.contador_creditos >= self.limite_creditos:
                if self.contador_creditos == self.limite_creditos:
                    self.tamanio_grupo = self.contador
                else:
                    self.tamanio_grupo = self.contador - 1
            else:
                self.tamanio_grupo = self.tamanio_materias_por_cursar
            self.contador_creditos = 0
            self.contador = 1
            self.materias_por_cursar = horario_validations.validate_lista_menor(self.materias_por_cursar)
            for materia in self.materias_por_cursar:
                self.contador_creditos = self.contador_creditos + materia['creditos']
                if(self.contador_creditos>=self.minimo_creditos):
                     break
                self.contador+=1
            if (self.contador_creditos >= self.minimo_creditos):
                self.tamanio_minimo_grupo = self.contador
            else:
                self.tamanio_minimo_grupo = 1
            while(self.tamanio_grupo >= self.tamanio_minimo_grupo-1):
                print('----------Tamanio minimo grupo ---',self.tamanio_minimo_grupo)
                print('---------------Esta es taanio grupo:',self.tamanio_grupo)
                resultado = self.iniciar_calculo_combinaciones_grupo(self.tamanio_grupo, self.materias_por_cursar)
                ##print('Esta es combinaciones_del_grupo pero en el while de generarTodasPosibilidades',resultado)
                if len(resultado)!=0:
                    self.posibles_combinaciones.extend(resultado)
                    #print('-------------------------- posiblesCombinaciones a la vista --------------')
                    ##print(self.posibles_combinaciones)
                self.tamanio_grupo-=1
                self.cuentame+=1
                #print('Cuentame papapapapaappaapa---',self.cuentame)
                #print('Cuentame papapapapaappaapa--- tamanioGrupo--: ',self.tamanio_grupo,'Tmbien es : minimo',self.tamanioMinimoGrupo)
            print(self.tamanio_minimo_grupo,'',self.tamanio_grupo)
            #print('----------Salio del while de generarTodasPosibilidades----------------')
            ##print(self.posibles_combinaciones)
            #print('------------------ tamano ----------: ',len(self.posibles_combinaciones))
            return 0
            if(len(self.posibles_combinaciones) == 0):
                self.suma_creditos= 0
            for materia in  self.materias_por_cursar:
                self.suma_creditos += materia['creditos']
            veces=1
            while(self.suma_creditos > 18):
                self.suma_creditos -= self.materias_por_cursar[self.tamanio_materias_por_cursar - veces]['creditos']
                veces+=1
        except ValueError as e:
            raise ValueError(e)
    
    def iniciar_calculo_combinaciones_grupo(self, tamanio:int, materias_por_cursar:list):
        """
            Función para calcular el total de combinaciones.
        """
        #print('Entro en iniciar_calculo_combinaciones_grupo')
        combinacion_base = list(range(tamanio))
        for i in combinacion_base:
            combinacion_base[i] = self.materias_por_cursar[i]
        resultado = self.calcular_combinaciones_grupo(combinacion_base, tamanio, self.materias_por_cursar)
        return resultado

    def calcular_combinaciones_grupo(self, combinacion_base:list , tamanio:int, materias_por_cursar:list):
        print('Entro en calcular_combinaciones_grupo')
        combinaciones_del_grupo = []
        combinacion = combinacion_base
        if self.comprueba_creditos_y_electivas(combinacion):
            combinaciones_del_grupo.append(combinacion.copy())
        total_combinaciones = self.numero_combinaciones_grupo(len(materias_por_cursar), tamanio)
        print('Esta es total_combinaciones: ',total_combinaciones)
        self.tamanio_new_combinacion = tamanio
        for i in range(total_combinaciones):
            print('Este el el tamanio-------------------------------------',tamanio)
            if tamanio == self.tamanio_new_combinacion:
                self.tamanio_new_combinacion -=1
                continue
            combinacion = self.new_combinacion(combinacion, materias_por_cursar, tamanio)
            print('Este es el total de combinaciones:',total_combinaciones,'Esta es la combinacion: ',i)
            self.tamanio_new_combinacion -=1
            if self.tamanio_new_combinacion <= 0:
                self.tamanio_new_combinacion == tamanio
            if self.comprueba_creditos_y_electivas(combinacion):
                combinaciones_del_grupo.append(combinacion.copy())
        print('Va a salir de calcular_combinaciones_grupo')
        #print('Minimo creditos',self.minimo_creditos)
        #print(combinaciones_del_grupo)
        return combinaciones_del_grupo

    def comprueba_creditos_y_electivas(self, combinacion:list)->bool:
        #print('Entro en comprueba_creditos_y_electivas')
        suma = 0
        electivas_incluidas = 0
        #print('Y entramos en el el for de comprueba_creditos_y_electivas')
        for i,materia in enumerate(combinacion):
            #print('Esta es el credito en esa materia que se itera',materia['creditos'])
            suma = suma + materia['creditos']
            if(materia['semestre'] == 99 or materia['semestre'] ==88 or materia['semestre'] == 77):
                electivas_incluidas +=1
            #print('Esta es suma: ',suma)
            #print(self.limite_creditos)
            if suma > self.limite_creditos:
                return False
        if (suma < self.minimo_creditos or electivas_incluidas != len(self.electivas_elejidas)):
            return False
        #print('va a salir de comprueba_creditos_y_electivas')
        return True

    def numero_combinaciones_grupo(self, m:int, n:int)->int:
        #print('Entro en numero_combinaciones_grupo')
        #print('Este ese el valor de m ---------: ',m)
        #print('Este ese el valor de n ---------: ',n)
        return int(self.cal_factorial(m) / (self.cal_factorial(n)*self.cal_factorial(m-n)))

    def cal_factorial(self, n:int)->int:
        if n==0:
            return 1
        return n*self.cal_factorial(n-1)
    
    def new_combinacion(self, combinacion:list, materias_por_cursar:list, tamanio:int):
        print('Entro en new_combinacion')
        new_combinacion = combinacion 
        posicion = tamanio
        #print('Esta es posicion antes de reducirla',posicion)
        posicion_superior_materia = 0
        opcion_final = False
        print('Esta es posicion_superior_materia antes del while')
        #print('Esta es combinacion','\n',combinacion)
        while(opcion_final == False):
            posicion -=1
            print(posicion)
            try:
                posicion_superior_materia = materias_por_cursar.index(combinacion[posicion])+1
            except IndexError:
                print('EL PRIMER TRY DENTRO DEL WHILE DIO ERROR')
            print('Esta es posicion en el whie:',posicion,'Esta es posicion_superior_materia en el while',posicion_superior_materia,'Esta es tamanio_new_combinacion',self.tamanio_new_combinacion)
            try:
                opcion_final = type(materias_por_cursar[posicion_superior_materia + ((tamanio - 1) - posicion)])
            except IndexError:
                print('Entro en el index error de la nueva condicion')
                pass
        print('Salio del while')
        print('Esta es posicion superior:',posicion_superior_materia,'Esta es posicion:',posicion)
        if (posicion<=0):
            posicion = posicion * -1
        if (posicion_superior_materia<0):
            posicion_superior_materia = posicion_superior_materia*-1
        for i in range(posicion,tamanio):
            try:
                new_combinacion[i] = materias_por_cursar[posicion_superior_materia]
            except IndexError:
                print('ERROR EN EL FOR INDICE FUERA DEL RANGO ESTABLECIDO; PRIMER TRY')
            #print('Este es new_combinacion[i]:','\n',new_combinacion[i])
            try:
                posicion_superior_materia = materias_por_cursar.index(new_combinacion[i])+1
            except IndexError:
                print('ERROR EN EL FOR INDICE FUERA DEL RANGO ESTABLECIDO; PRIMER TRY')
            #print('Esta es posicion_superior_materia: ',posicion_superior_materia)
        #print('Esta es new_combinacion:---------------------------------------------------',new_combinacion)
        return new_combinacion 

    def asigna_puntuacion(self)->list:
        nivel = round(((self.creditos_aprobados/132)*10))
        combinaciones_puntuadas = []
        for combinacion in self.posibles_combinaciones:
            puntos_combinacion =0
            materias_a_desbloquear = self.cantidad_materias_a_desbloquear(combinacion)
            numero_creditos = self.creditos_combinacion(combinacion)
            puntos_nivel = self.puntos_por_nivel(combinacion, nivel)
            puntos_combinacion = ((materias_a_desbloquear*10)*0.5) + ((numero_creditos*10)*0.4) + ((puntos_nivel*10)*0.1)
            combinaciones_puntuadas.append({
            'combinacion': combinacion,
            'puntaje': puntos_combinacion})
        return combinaciones_puntuadas

    def cantidad_materias_a_desbloquear(self, combinacion:list)->float:
        desbloqueadas:list = self.secuencia_desbloqueo(combinacion)
        del_pensum = 0
        electivas = 0
        for materia in desbloqueadas:
            if(materia['semestre'] != 99 and materia['semestre']!=88):
                del_pensum+=1
            else:
                electivas+=1
        return del_pensum + (electivas/2)

    def secuencia_desbloqueo(self,combinacion:list):
        pensum = horario_validations.validate_pensum(self.carrera)
        agregada = True
        desbloqueadas = []
        materias_desbloqueadas=[]
        TAMANIOPENSUM:int = len(pensum)
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
                materias_desbloqueadas = materias_desbloqueadas+desbloqueadas
                desbloqueadas=[]
        return materias_desbloqueadas
  
    def creditos_combinacion(self, combinacion:list):
        creditos:int=0
        for materia in combinacion:
            creditos += materia['creditos']
        return creditos
  
    def puntos_por_nivel(self, combinacion:list, nivel:int):
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



class Horario():
    horarios:list = []
    estadohorario:list=[]
    posiblesCombinaciones:list=[]
    horariosfinales:list=[]
    materiasquechocan:list=[]
    intentos:int
    stop:bool
    tamanio_new_combinacion=0


    def cargar_horario(self,id):
        horarios_generales = horario_models.HorarioGeneral.objects.get(id=5)
        horarios_generales_serializados = horario_serializers.HorarioGeneral(horarios_generales,many=False).data
        #print('----------')
        horarios_generales_json = horarios_generales_serializados['horario'].replace("\'", "\"")
        self.horarios = json.loads(horarios_generales_json)
        #print(len(self.horarios),type(self.horarios))

    def comprobar_combinacion_horario(self,combinacion:list)->bool:
        print('entro en comprobarCombinacionHorario')
        all_materias_secciones = []
        for indice, materia in enumerate(combinacion):
            codifo_materia = materia['codigo']
            HMATERIA = []
            for index,materia_general in enumerate(self.horarios):
                if self.horarios[materia_general]['codigo'] == codifo_materia:
                    HMATERIA.append(self.horarios[materia_general])
                secciones_materia = []
                for indice,item in enumerate(HMATERIA):
                    if not item['seccion'] in secciones_materia:
                        secciones_materia.append({
                            'codigo': materia['codigo'],
                            'materia': materia['materia'],
                            'creditos': materia['creditos'],
                            'seccion': item['seccion']
                            })
            all_materias_secciones.append(secciones_materia)
        horario_base = []
        print('El error')
        for indice, materia in enumerate(all_materias_secciones):
            print(materia,'\n',type(materia),'\n',materia[0])
            horario_base.append(materia[0]) #Creo que dara error, en dado caso cambiar por 'codigo'
        print('Estos son los horario_base','\n',horario_base)
        self.posiblesCombinaciones = self.find_all_horarios(horario_base, len(combinacion), all_materias_secciones)
        print('no era')
        return self.posiblesCombinaciones
        for indice, horario in enumerate(self.posiblesCombinaciones):
            resultado = self.comprobar_posible_horario(horario)
            if resultado == True:
                estadohorario = self.estadohorario
                self.horariosfinales.append(estadohorario)
        if len(self.horariosfinales)==0:
            return False
        return self.horariosfinales


    def find_all_horarios(self,horario_base, tamanio ,all_materias_secciones):
        print('Entro en find_all_horarios')
        new_horario = horario_base
        all_horarios = []
        all_horarios.append(new_horario.copy())
        total_combinaciones = 1
        print(all_materias_secciones)
        print('antes del for en find_all_horarios')
        for i in range(len(all_materias_secciones)):
            print('estamos en el range de all_materias_secciones:',i)
            total_combinaciones = total_combinaciones * len(all_materias_secciones[i])
        self.tamanio_new_combinacion = tamanio
        print('total_combinaciones: ',total_combinaciones)
        for i in range(total_combinaciones-1):
            print('estamos en el range de total_combinaciones:',i)
            new_horario = self.new_horario(new_horario, tamanio, all_materias_secciones,i)
            all_horarios.append(new_horario.copy())
            self.tamanio_new_combinacion -=1
        print('Salimos de find_all_horarios este es el tamano de all_horarios: ',len(all_horarios))
        #print('\n','\n',all_horarios,'\n','\n')
        for indice,cuerpo1 in enumerate(all_horarios):
            print('Combinacion----------------')
            for indice2,cuerpo2 in enumerate(cuerpo1):
                print(cuerpo2['seccion'])
                print('-----------------------------------')
        return all_horarios

    def new_horario(self,old_horario, tamanio , all_materias_secciones,i):
        #print('Ya en new_horario')
        new_horario = old_horario
        posicion = tamanio #posicion de la seccion a remplazar
        posicion_seccion_superior = 0 #para remplazar la seccion actual 
        estado=False #para comprobar si el horario en la posicion ya no puede subir posicion
        #print('all_materias_secciones:\n',all_materias_secciones)
        posicion_seccion=0
        while(estado == False):
            #print('Esta es posicion: ',posicion,'Esta es estado: ',estado)
            posicion -=1
            if posicion == -1:
                print(posicion)
                print(len(all_materias_secciones)-1,len(all_materias_secciones)-1-1)
                posicion_seccion = (len(all_materias_secciones[posicion])- 1)
                posicion_seccion -=1
            else:
                posicion_seccion = (len(all_materias_secciones[posicion])- 1)
            ##print(posicion)
            print(all_materias_secciones[posicion][posicion_seccion])
            print(old_horario[posicion])
            if len(all_materias_secciones[posicion])>2:
                print(all_materias_secciones[posicion].index(new_horario[posicion]))
                posicion_seccion = all_materias_secciones[posicion].index(new_horario[posicion])
                estado = True if (all_materias_secciones[posicion][posicion_seccion]['seccion'] != old_horario[posicion]['seccion']) else False
                posicion_seccion-=1
            else:
                estado = True if (all_materias_secciones[posicion][posicion_seccion]['seccion'] != old_horario[posicion]['seccion']) else False
            #print('Esta es estado: ',estado)
        #print('Esta es posicion: ',posicion,'Esta es estado: ',estado)
        #print(all_materias_secciones[posicion])
        #print(all_materias_secciones[posicion][posicion_seccion],'\n',old_horario[posicion]['seccion'])
        #print(all_materias_secciones[posicion].index(all_materias_secciones[posicion][posicion_seccion]) +1)
        #print('hola')
        print(posicion)
        posicion_seccion_superior = all_materias_secciones[posicion].index(all_materias_secciones[posicion][posicion_seccion]) + 1
        #print(posicion_seccion_superior)
        new_horario[posicion] = all_materias_secciones[posicion][posicion_seccion_superior-1]
        #print(new_horario[posicion])
        #print('tamanio de all_materias_secciones----------',len(all_materias_secciones),'el tamanio de old_horario: ',len(old_horario),old_horario)

        #las posiciones posteriores se llenan con la primera opcion
        for i in range(posicion+1,tamanio):
            if len(all_materias_secciones[i])>2:    
                print('--------------- Ah cambiar esa materia   --------:')
                print(new_horario[i])
                print(all_materias_secciones[i])
                seccion_arriba = all_materias_secciones[i].index(new_horario[i])-1
                new_horario[i] = all_materias_secciones[i][seccion_arriba]
            else:
                new_horario[i] = all_materias_secciones[i][0]
        print(new_horario)
        return new_horario

    def comprobar_posible_horario(self,combinacion:list)->bool:
        if(self.comprueba_existencia_de_choque(combinacion))==True: 
            return False
        self.estadohorario = []
        for i in range(5):
            self.estadohorario.append([])
            for j in range(34):
                self.estadohorario[i].append({
                                                'estado': False,
                                                'materia': '',
                                                'codigo': '',
                                                'creditos': '',
                                                'seccion': '',
                                                'dia': '',
                                                'desde': '',
                                                'hasta': '',
                                                'aula': '',
                                                'profesor': ''})
        for indice,materia in enumerate(combinacion):
            HorarioMateria = []
            diasClase = []
            for i,horario in enumerate(self.horarios):
                if self.horarios[horario]['codigo'] == materia['codigo']:
                    HorarioMateria.append(self.horarios[horario])
            for i,h in enumerate(HorarioMateria):
                if h['seccion'] == materia['seccion']:
                    diasClase.append(h)
            for i, dia in enumerate(diasClase):
                DIA = self.dia(dia['dia'])
                DESDE = self.desde(dia['desde'])
                HASTA = self.hasta(dia['hasta'])
                a=DESDE
                while (a<=HASTA):
                    if self.estadohorario[DIA][a]['estado']==True:
                        choque = {
                                  'materia1':{
                                                'codigo': dia['codigo'],
                                                'seccion': dia['seccion']
                                  },
                                  'materia2':{
                                                'codigo': self.estadohorario[DIA][i]['codigo'],
                                                'seccion': self.estadohorario[DIA][i]['seccion']
                                  }
                                }
                        self.materiasquechocan.append(choque)
                        return False
                    else:
                        self.estadohorario[DIA][a]={
                                                      'estado': True,
                                                      'materia': dia['materia'],
                                                      'codigo': dia['codigo'],
                                                      'creditos': materia['creditos'],
                                                      'seccion': dia['seccion'],
                                                      'dia': dia['dia'],
                                                      'desde': dia['desde'],
                                                      'hasta': dia['hasta'],
                                                      'aula': dia['aula'],
                                                      'profesor': dia['profesor']
                                                    }
                    a+=1
        return True

    def comprueba_existencia_de_choque(self,combinacion:list)->bool:
        for  indice,choqueGuardado in enumerate(self.materiasquechocan):
            for indice2,materia in enumerate(combinacion):
                if materia['codigo'] == choqueGuardado['materia1']['codigo'] and materia['seccion'] == choqueGuardado['materia1']['seccion']:
                    if materia['codigo'] == choqueGuardado['materia2']['codigo'] and materia['seccion'] == choqueGuardado['materia2']['seccion']:
                        return True
        #print('Salimos de compruebaExistenciaDeChoque')
        return False

    def dia(self,dia:str):
        #print('Entro en dia')
        DIA:int
        if dia == 'Lun':
            DIA = 0
        elif dia == 'Mar':
            DIA = 1
        elif dia == 'Mie':
            DIA = 2
        elif dia == 'Jue':
            DIA = 3
        else:
            DIA = 4
        return DIA

    def desde(self,desde:str):
        #print('entro en desde')
        DESDE:int
        if desde == '07:00':
            DESDE = 0
        elif desde == '07:50':
            DESDE = 1
        elif desde == '08:35':
            DESDE = 2 
        elif desde == '08:40':
            DESDE = 3
        elif desde == '09:25':
            DESDE = 4 
        elif desde == '09:30':
            DESDE = 5
        elif desde == '10:15':
            DESDE = 6 
        elif desde == '10:20':
            DESDE = 7
        elif desde == '11:05':
            DESDE = 8 
        elif desde == '11:10':
            DESDE = 9
        elif desde == '11:55':
            DESDE = 10 
        elif desde == '12:00':
            DESDE = 11
        elif desde == '12:45':
            DESDE = 12 
        elif desde == '12:50':
            DESDE = 13
        elif desde == '13:35':
            DESDE = 14 
        elif desde == '13:40':
            DESDE = 15
        elif desde == '14:00':
            DESDE = 16 
        elif desde == '14:25':
            DESDE = 17
        elif desde == '14:35':
            DESDE = 18
        elif desde == '14:45':
            DESDE = 19 
        elif desde == '14:50':
            DESDE = 20
        elif desde == '15:15':
            DESDE = 21 
        elif desde == '15:20':
            DESDE = 22
        elif desde == '15:35':
            DESDE = 23  
        elif desde == '15:40':
            DESDE = 24
        elif desde == '16:05':
            DESDE = 25 
        elif desde == '16:25':
            DESDE = 26
        elif desde == '16:30':
            DESDE = 27 
        elif desde == '16:55':
            DESDE = 28
        elif desde == '17:15':
            DESDE = 29 
        elif desde == '17:20':
            DESDE = 30
        elif desde == '18:05':
            DESDE = 31 
        elif desde == '18:55':
            DESDE = 32
        else:
            DESDE = 33
            #print('Hora no determinada en Desde',desde)
        return DESDE

    def hasta(self,hasta:str):
        HASTA:int
        if hasta == '07:00':
            HASTA = 0
        elif hasta == '07:50':
            HASTA = 1
        elif hasta == '08:35':
            HASTA = 2 
        elif hasta == '08:40':
            HASTA = 3
        elif hasta == '09:25':
            HASTA = 4 
        elif hasta == '09:30':
            HASTA = 5
        elif hasta == '10:15':
            HASTA = 6 
        elif hasta == '10:20':
            HASTA = 7
        elif hasta == '11:05':
            HASTA = 8 
        elif hasta == '11:10':
            HASTA = 9
        elif hasta == '11:55':
            HASTA = 10 
        elif hasta == '12:00':
            HASTA = 11
        elif hasta == '12:45':
            HASTA = 12 
        elif hasta == '12:50':
            HASTA = 13
        elif hasta == '13:35':
            HASTA = 14 
        elif hasta == '13:40':
            HASTA = 15
        elif hasta == '14:00':
            HASTA = 16 
        elif hasta == '14:25':
            HASTA = 17
        elif hasta == '14:35':
            HASTA = 18
        elif hasta == '14:45':
            HASTA = 19 
        elif hasta == '14:50':
            HASTA = 20
        elif hasta == '15:15':
            HASTA = 21 
        elif hasta == '15:20':
            HASTA = 22
        elif hasta == '15:35':
            HASTA = 23  
        elif hasta == '15:40':
            HASTA = 24
        elif hasta == '16:05':
            HASTA = 25 
        elif hasta == '16:25':
            HASTA = 26
        elif hasta == '16:30':
            HASTA = 27 
        elif hasta == '16:55':
            HASTA = 28
        elif hasta == '17:15':
            HASTA = 29 
        elif hasta == '17:20':
            HASTA = 30
        elif hasta == '18:05':
            HASTA = 31 
        elif hasta == '18:55':
            HASTA = 32
        else:
            HASTA = 33
            #print('Hora no determinada en hasta',hasta)
        return HASTA