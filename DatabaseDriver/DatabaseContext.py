import psycopg2 as pc

from Modelos.Plan import Plan
from Modelos.Asignatura import Asignatura
from Modelos.EstadisticaAsignatura import EstadisticaAsignatura

class DatabaseContext():

    def __init__(self):
        self.conn,self.cursor = self.connection()

    def connection(self):
        try:
            conn = pc.connect(database="",host="0.0.0.0",user="",password="",port=0000)
            cursor = conn.cursor()
            return conn,cursor
        except:
            print("Error en la conexión a la base de datos")
            return None,None

    def disconnect(self):
        try:
            self.conn.close()
            print("Conexión finalizada")
        except:
            print("Error al cerrar la conexión a la base de datos")

    def obtenerPlanes(self):
        try:
            if self.conn != None:
                planes = {}
                query = "SELECT plan.id, nombre, version, duracion_semestres, cod_asignatura, nivel FROM plan INNER JOIN plan_asignatura ON plan.id = plan_asignatura.id_plan ORDER BY plan.id,nivel;" 
                self.cursor.execute(query)
                resultados = self.cursor.fetchall()
                for resultado in resultados:
                    idPlan = resultado[0]
                    nombre = resultado[1]
                    version = resultado[2]
                    duracion = resultado[3]
                    codigoAsignatura = resultado[4]
                    nivelAsignatura = resultado[5]
                    if idPlan in planes:
                        planes[idPlan].agregarAsignatura(codigoAsignatura,nivelAsignatura)
                    else:
                        plan = Plan(idPlan, nombre, version, duracion)
                        plan.agregarAsignatura(codigoAsignatura, nivelAsignatura)
                        planes[idPlan] = plan
                return planes
            else:
                return None
        except:
            print("Error en la conexión a la base de datos")
            return None

    def ingresarEstadisticasAsignaturas(self, ano, periodo, asignaturas):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
            else:
                estadisticasExistentes = self.obtenerEstadisticasPeriodo(ano, periodo)
                query = ""
                for codigo in asignaturas:
                    if codigo in estadisticasExistentes:
                        updateQuery = "UPDATE estadistica_asignatura SET " + \
                        "inscritos_teoria = " + str(asignaturas[codigo].inscritosTeoria) + \
                        ",aprobados_teoria = " + str(asignaturas[codigo].aprobadosTeoria) + \
                        ",reprobados_teoria = " + str(asignaturas[codigo].reprobadosTeoria) + \
                        ",inscritos_laboratorio = " + str(asignaturas[codigo].inscritosLaboratorio) + \
                        ",aprobados_laboratorio = " + str(asignaturas[codigo].aprobadosLaboratorio) + \
                        ",reprobados_laboratorio = " + str(asignaturas[codigo].reprobadosLaboratorio) + \
                        ",tasa_aprobacion_teoria = " + str(asignaturas[codigo].tasaAprobacionTeoria) + \
                        ",tasa_aprobacion_laboratorio = " + str(asignaturas[codigo].tasaAprobacionLaboratorio) + \
                        ",tasa_desinscripcion = " + str(asignaturas[codigo].tasaDesinscripcion) + \
                        "WHERE cod_asignatura = " + str(codigo) + " and ano = " + str(ano) + " and semestre = " + str(periodo) + ";"
                        query = query + updateQuery
                    else:
                        insertQuery = "INSERT INTO estadistica_asignatura " + \
                        "(cod_asignatura, ano, semestre,inscritos_teoria,aprobados_teoria,reprobados_teoria,inscritos_laboratorio,aprobados_laboratorio,reprobados_laboratorio,tasa_aprobacion_teoria,tasa_aprobacion_laboratorio,tasa_desinscripcion) "+ \
                        "VALUES (" + str(codigo)+"," + str(ano)+"," + str(periodo)+"," + str(asignaturas[codigo].inscritosTeoria)+","+ str(asignaturas[codigo].aprobadosTeoria)+","+ str(asignaturas[codigo].reprobadosTeoria) + \
                        "," + str(asignaturas[codigo].inscritosLaboratorio)+","+ str(asignaturas[codigo].aprobadosLaboratorio)+"," + str(asignaturas[codigo].reprobadosLaboratorio) + \
                        "," + str(asignaturas[codigo].tasaAprobacionTeoria)+","+ str(asignaturas[codigo].tasaAprobacionLaboratorio)+","+ str(asignaturas[codigo].tasaDesinscripcion) + ");"
                        query = query + insertQuery
                self.cursor.execute(query)
                self.conn.commit()
            return
        except:
            print("Error en la conexión a la base de datos")
            return None

    def obtenerTasasHistoricas(self):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
            else:
                query = "select cod_asignatura,avg(tasa_aprobacion_teoria),avg(tasa_aprobacion_laboratorio),avg(tasa_desinscripcion) from estadistica_asignatura group by cod_asignatura;"
                self.cursor.execute(query)
                resultados = self.cursor.fetchall()
                diccionario = {}
                for resultado in resultados:
                    diccionario[resultado[0]] = {
                                                "tasaAprobacionTeoria": resultado[1],
                                                "tasaAprobacionLaboratorio": resultado[2],
                                                "tasaDesinscripcion": resultado[3]
                                                }
                return diccionario
        except:
            print("Error en la conexión a la base de datos")
            return None

    def obtenerEstadisticasPeriodo(self, ano, semestre):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
            else:
                query = "select cod_asignatura,inscritos_teoria,aprobados_teoria,reprobados_teoria,inscritos_laboratorio,aprobados_laboratorio,reprobados_laboratorio,tasa_aprobacion_teoria,tasa_aprobacion_laboratorio,tasa_desinscripcion from estadistica_asignatura where ano =" + str(ano) + "and semestre ="+ str(semestre) + ";"
                self.cursor.execute(query)
                resultados = self.cursor.fetchall()
                diccionario = {}
                for resultado in resultados:
                    diccionario[resultado[0]] = {   
                                                "inscritosTeoria": resultado[1],
                                                "aprobadosTeoria": resultado[2],
                                                "reprobadosTeoria": resultado[3],
                                                "inscritosLaboratorio": resultado[4],
                                                "aprobadosLaboratorio": resultado[5],
                                                "reprobadosLaboratorio": resultado[6],
                                                "tasaAprobacionTeoria": resultado[7],
                                                "tasaAprobacionLaboratorio": resultado[8],
                                                "tasaDesinscripcion": resultado[9]
                                                }
                return diccionario
        except:
            print("Error en la conexión a la base de datos")
            return None

    def obtenerAsignaturas(self):
        try:
            if self.conn == None:
                return None
            else:
                queryAsignaturas = "select * from asignatura Order by codigo;"
                self.cursor.execute(queryAsignaturas)
                resultados = self.cursor.fetchall()
                asignaturas = {}
                for resultado in resultados:
                    codigoAsignatura = resultado[0]
                    nombre = resultado[1]
                    tipo = resultado[2]
                    asignaturas[codigoAsignatura] = Asignatura(codigoAsignatura, nombre, tipo)

                queryRequisitos = "select cod_asignatura,cod_asignatura_requisito,nivel_requisito from requisito;"
                self.cursor.execute(queryRequisitos)
                resultados = self.cursor.fetchall()
                for resultado in resultados:
                    codigoAsignatura = resultado[0]
                    codigoRequisito = resultado[1]
                    nivelRequisito = resultado[2]
                    asignaturas[codigoAsignatura].agregarAsignaturaRequisito(codigoRequisito, nivelRequisito)

                queryEquivalentes = "select cod_asignatura, cod_asignatura_analoga from analoga;"
                self.cursor.execute(queryEquivalentes)
                resultados = self.cursor.fetchall()
                for resultado in resultados:
                    codigoAsignatura = resultado[0]
                    codigoAsignaturaEquivalente = resultado[1]
                    asignaturas[codigoAsignatura].agregarAsignaturaEquivalente(codigoAsignaturaEquivalente)
                return asignaturas
        except:
            print("Error en la conexión a la base de datos")
            return None

    def obtenerPlan(self, idPlan):
        try:
            if self.conn != None:
                query = "SELECT nombre, version, duracion_semestres, cod_asignatura, nivel FROM plan INNER JOIN plan_asignatura ON plan.id = plan_asignatura.id_plan where plan.id = " + str(idPlan) + "ORDER BY nivel;" 
                self.cursor.execute(query)
                resultados = self.cursor.fetchall()
                resultado = resultados[0]
                nombre = resultado[0]
                version = resultado[1]
                duracion = resultado[2]
                plan = Plan(idPlan, nombre, version, duracion)
                for resultado in resultados:
                    codigoAsignatura = resultado[3]
                    nivelAsignatura = resultado[4]
                    plan.agregarAsignatura(codigoAsignatura, nivelAsignatura)
                return plan
        except:
            print("Error en la conexión a la base de datos")
            return None

    def obtenerEstadisticasAsignatura(self, codigo):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
            else:
                query = "select * from estadistica_asignatura where cod_asignatura = " + str(codigo) + " ORDER BY ano desc, semestre desc;"
                self.cursor.execute(query)
                resultados = self.cursor.fetchall()
                estadisticas = []
                for resultado in resultados:
                    estadistica = EstadisticaAsignatura(resultado[2], resultado[3], codigo)
                    estadistica.setInscritosTeoria(resultado[4])
                    estadistica.setAprobadosTeoria(resultado[5])
                    estadistica.setReprobadosTeoria(resultado[6])
                    estadistica.setInscritosLaboratorio(resultado[7])
                    estadistica.setAprobadosLaboratorio(resultado[8])
                    estadistica.setReprobadosLaboratorio(resultado[9])
                    estadistica.setTasaAprobacionTeoria(resultado[10])
                    estadistica.setTasaAprobacionLaboratorio(resultado[11])
                    estadistica.setTasaDesinscripcion(resultado[12])
                    estadisticas.append(estadistica)
                return estadisticas
        except:
            print("Error en la conexión a la base de datos")
            return None

    def insertarNuevaAsignatura(self, asignatura):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                queryCompleta = ""
                queryAsignatura = "INSERT INTO asignatura(codigo, nombre, tipo) values (" + str(asignatura.getCodigo()) + ",'" + asignatura.getNombre() + "','" + asignatura.getTipoAsignatura()  + "');\n"
            
                queryEquivalentes = ""
                equivalentes = asignatura.getAsignaturasEquivalentes()
                equivalentes.append(asignatura.getCodigo())
                for codigoA in equivalentes:
                    for codigoB in equivalentes:
                        if codigoA!= codigoB:
                            insertQuery = "INSERT INTO analoga(cod_asignatura, cod_asignatura_analoga) values (" + str(codigoA) + "," + str(codigoB) + ");\n"
                            queryEquivalentes += insertQuery

                queryRequisitos = ""
                nivelesRequisitos = asignatura.getAsignaturasRequisitos()
                for nivel in nivelesRequisitos:
                    for codigoRequisito in nivelesRequisitos[nivel]:
                        insertQuery = "INSERT INTO requisito(cod_asignatura, cod_asignatura_requisito, nivel_requisito) values (" + str(asignatura.getCodigo()) + "," + str(codigoRequisito) + "," + str(nivel) + ");\n"
                        queryRequisitos += insertQuery
                queryCompleta = queryAsignatura + queryEquivalentes + queryRequisitos
                self.cursor.execute(queryCompleta)
                self.conn.commit()
                return True
        except:
            print("Error en la conexión a la base de datos")
            return False

    def insertarNuevoPlan(self, plan):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                queryPlan = "INSERT INTO Plan(nombre, version, duracion_semestres) values ('"+ plan.getNombre() + "','" + plan.getVersion() + "'," + str(plan.getDuracion())  + ");\n"
                self.cursor.execute(queryPlan)
                self.conn.commit() 
                return True
        except:
            print("Error en la conexión a la base de datos")
            return False

    def insertarAsignaturasPlan(self, plan):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                queryAsignaturas = ""
                nivelesAsignaturas = plan.getAsignaturas()
                for nivel in nivelesAsignaturas:
                    for codigo in nivelesAsignaturas[nivel]:
                        insertQuery = "INSERT INTO plan_asignatura(id_plan, cod_asignatura, nivel) values (" + str(plan.getId()) + "," + str(codigo) + "," + str(nivel) + ");\n"
                        queryAsignaturas += insertQuery
                self.cursor.execute(queryAsignaturas)
                self.conn.commit()
                return True
        except:
            print("Error en la conexión a la base de datos")
            return False

    def getIdPlan(self, plan):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                nombre = plan.getNombre()
                version = plan.getVersion()
                duracion = plan.getDuracion()
                queryId = "Select id from plan where nombre = '" + nombre + "' and version = '"+ version + "' and duracion_semestres = " + str(duracion) +";"
                self.cursor.execute(queryId)
                idPlan = self.cursor.fetchone()[0]
                return idPlan
        except:
            print("Error en la conexión a la base de datos")
            return False

    def actualizarEstadisticaAsignatura(self, estadistica):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                updateQuery = "UPDATE estadistica_asignatura SET " + \
                "inscritos_teoria = " + str(estadistica.getInscritosTeoria()) + \
                ", aprobados_teoria = " + str(estadistica.getAprobadosTeoria()) + \
                ", reprobados_teoria = " + str(estadistica.getReprobadosTeoria()) + \
                ", inscritos_laboratorio = " + str(estadistica.getInscritosLaboratorio()) + \
                ", aprobados_laboratorio = " + str(estadistica.getAprobadosLaboratorio()) + \
                ", reprobados_laboratorio = " + str(estadistica.getReprobadosLaboratorio())+ \
                ", tasa_aprobacion_teoria = " + str(estadistica.getTasaAprobacionTeoria()) + \
                ", tasa_aprobacion_laboratorio = " + str(estadistica.getTasaAprobacionLaboratorio()) + \
                ", tasa_desinscripcion = " + str(estadistica.getTasaDesinscripcion()) + \
                " WHERE cod_asignatura = " + str(estadistica.getCodigo()) + " and ano = " + str(estadistica.getAno()) + " and semestre = " + str(estadistica.getSemestre()) + ";"
                self.cursor.execute(updateQuery)
                self.conn.commit()
                return True
        except:
            print("Error en la conexión a la base de datos")
            return False

    def registrarEstadisticaAsignatura(self, estadistica):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                insertQuery = "INSERT INTO estadistica_asignatura " + \
                    "(cod_asignatura, ano, semestre,inscritos_teoria,aprobados_teoria,reprobados_teoria,inscritos_laboratorio,aprobados_laboratorio,reprobados_laboratorio,tasa_aprobacion_teoria,tasa_aprobacion_laboratorio,tasa_desinscripcion) "+ \
                    "VALUES (" + str(estadistica.getCodigo())+"," + str(estadistica.getAno()) +"," + str(estadistica.getSemestre()) +"," + str(estadistica.getInscritosTeoria())+","+ str(estadistica.getAprobadosTeoria())+","+ str(estadistica.getReprobadosTeoria()) + \
                    "," + str(estadistica.getInscritosLaboratorio())+","+ str(estadistica.getAprobadosLaboratorio()) +"," + str(estadistica.getReprobadosLaboratorio()) + \
                    "," + str(estadistica.getTasaAprobacionTeoria())+","+ str(estadistica.getTasaAprobacionLaboratorio())+","+ str(estadistica.getTasaDesinscripcion()) + ");"
                self.cursor.execute(insertQuery)
                self.conn.commit()
                return True
        except:
            print("Error en la conexión a la base de datos")
            return False

    def eliminarEstadistica(self, estadistica):
        try:
            if self.conn == None:
                print("Error en la conexión a la base de datos")
                return False
            else:
                deleteQuery = "DELETE FROM estadistica_asignatura WHERE cod_asignatura = " + str(estadistica.getCodigo()) + " and ano = " + str(estadistica.getAno()) + " and semestre = " + str(estadistica.getSemestre()) + ";"
                self.cursor.execute(deleteQuery)
                self.conn.commit()
                return True
        except:
            print("Error en la conexión a la base de datos")
            return False
        
