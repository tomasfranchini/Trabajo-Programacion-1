from modulo import leer_entero
from modulo import leer_opcion
from modulo import normalizar_nombre
from modulo import generar_fixture
from modulo import registrar_partidos_y_eventos
from modulo import menu_informes
from modulo import ingresar_equipos_y_jugadores
from modulo import ListadoPosiciones
from modulo import ListadoGoleadores
from modulo import puntos_equipo    


if __name__=="__main__":
        # Estructuras principales homogéneas
    equipos = [""] * 10                                       # nombres equipos
    jugadores_nombres = [[""]*10 for _ in range(10)]          # matriz 10x10 nombres
    goles_jug = [[0]*10 for _ in range(10)]                    # goles por jugador
    amar_jug = [[0]*10 for _ in range(10)]                     # amarillas por jugador
    rojas_jug = [[0]*10 for _ in range(10)]                    # rojas por jugador

    # Tabla de posiciones (por equipo)
    PJ = [0]*10; PG = [0]*10; PE = [0]*10; PP = [0]*10; GF = [0]*10; GC = [0]*10

    # Fixture
    partidos = []      # lista de partidos: [id, fecha, local, visitante, jugado, eventos, gl, gv]
    fechas = [[] for _ in range(9)]  # lista de fechas, cada una con lista de ids de partidos
    fixture_ids = [[0 for _ in range(10)] for _ in range(10)]  # matriz por comprensión

    seguir = True
    while seguir:
        print("""
==============================
 Torneo de Liga (Consola)
==============================
1) Ingresar equipos y jugadores
2) Generar fixture (y matriz de IDs)
3) Registrar partidos y eventos
4) Informes
0) Salir
""")
        op = leer_opcion("Opción: ", ["0","1","2","3","4"])
        if op == '1':
            ingresar_equipos_y_jugadores(equipos, jugadores_nombres, goles_jug, amar_jug, rojas_jug)
        elif op == '2':
            # Verificar que haya equipos cargados
            ok = True
            salir_i = False
            i = 0
            while i < 10 and not salir_i:
                if equipos[i] == "":
                    ok = False
                    salir_i = True
                else:
                    salir_j = False
                    j = 0
                    while j < 10 and not salir_j:
                        if jugadores_nombres[i][j] == "":
                            ok = False
                            salir_j = True
                        j += 1
                i += 1
            if not ok:
                print("Primero tenes que cargar los 10 equipos y sus 10 jugadores cada uno (opción 1).")
            else:
                generar_fixture(equipos,partidos, fechas, fixture_ids)
        elif op == '3':
            if len(partidos) == 0:
                print("Primero generá el fixture (opción 2).")
            else:
                registrar_partidos_y_eventos(equipos, jugadores_nombres, partidos, fixture_ids,
                                             PJ, PG, PE, PP, GF, GC,
                                             goles_jug, amar_jug, rojas_jug)
        elif op == '4':
            menu_informes(equipos, jugadores_nombres, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug)
        elif op == '0':
            print("¡Chau!")
            seguir = False