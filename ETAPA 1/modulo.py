import random

# Solicitá al usuario un número entero, validando rango opcional
def leer_entero(mensaje, minimo=None, maximo=None):
    """Lee un entero por consola, validando opcionalmente rango [minimo..maximo]."""
    valido = False
    valor = None

    while not valido:
        entrada = input(mensaje).strip()

        # Validar entero (acepta negativos con un solo '-')
        if entrada.lstrip("-").isdigit() and entrada.count("-") <= 1 and not (len(entrada) > 0 and entrada[-1] == "-"):
            v = int(entrada)

            if minimo is not None and v < minimo:
                print("Valor mínimo permitido:", minimo)
            elif maximo is not None and v > maximo:
                print("Valor máximo permitido:", maximo)
            else:
                valor = v
                valido = True
        else:
            print("Entrada inválida. Debe ser un número entero.")

    return valor

# Solicitá al usuario una opción válida de un conjunto dado
def leer_opcion(mensaje, opciones_validas):
    """Lee una opción de un conjunto permitido. Devuelve en mayúsculas."""
    opciones = [o.upper() for o in opciones_validas]
    valido = False
    valor = None

    while not valido:
        v = input(mensaje).strip().upper()
        if v in opciones:
            valor = v
            valido = True
        else:
            print("Opción inválida. Valores válidos:", ", ".join(opciones))

    return valor

# Normaliza el nombre de un equipo o jugador para impresión
def normalizar_nombre(s):
    s = s.strip()
    if len(s) >= 22:
        resultado=""
        resultado+=s[0]
        while " " in s:
            pos=s.index(" ")
            resultado+=s[pos+1]
            s=s[pos+1:]
        return resultado.upper()
    else:
        return s.title()

# -----------------------------
# Equipos y jugadores
# -----------------------------

# Permite ingresar los nombres de los equipos y jugadores
def ingresar_equipos_y_jugadores(equipos, jugadores_nombres, goles_jug, amar_jug, rojas_jug):
    """
    Carga 10 equipos y 10 jugadores por equipo.
    - equipos: lista de 10 nombres de equipo (str)
    - jugadores_nombres: matriz 10x10 de nombres (str)
    - goles_jug, amar_jug, rojas_jug: matrices 10x10 (int) inicializadas en 0
    """
    print("\n=== Ingreso de Equipos y Jugadores ===")
    usados = []  # nombres de equipos ya usados
    i = 0
    while i < 10:
        nombre = input(f"Nombre para Equipo {i+1} (enter = 'Equipo {i+1}'): ").strip()
        if nombre == "":
            nombre = f"Equipo {i+1}"
        nombre = normalizar_nombre(nombre)

        # verificar unicidad
        existe = False
        k = 0
        while k < len(usados) and not existe:
            if usados[k].lower() == nombre.lower():
                existe = True
            k += 1

        if existe:
            print("Ese nombre de equipo ya existe. Ingrese otro.")
        else:
            equipos[i] = nombre
            usados.append(nombre)

            # jugadores del equipo i
            print(f"  > Ingresar 10 jugadores para {equipos[i]}:")
            j = 0
            usados_j = []
            while j < 10:
                defecto = f"J{i+1:02d}-{j+1:02d}"
                nombre_j = input(f"    Jugador {j+1} (enter = '{defecto}'): ").strip()
                if nombre_j == "":
                    nombre_j = defecto
                nombre_j = nombre_j.strip().title()

                # unicidad dentro del equipo
                existe_j = False
                t = 0
                while t < len(usados_j) and not existe_j: 
                    if usados_j[t].lower() == nombre_j.lower():
                        existe_j = True
                    t += 1

                if existe_j:
                    print("    Ese nombre ya existe en este equipo. Ingrese otro.")
                else:
                    jugadores_nombres[i][j] = nombre_j
                    goles_jug[i][j] = 0
                    amar_jug[i][j] = 0
                    rojas_jug[i][j] = 0
                    usados_j.append(nombre_j)
                    j += 1  # avanzar solo si se aceptó el jugador

            i += 1  # avanzar solo si se aceptó el equipo
    print("Ingreso completado.\n")

# -----------------------------
# Fixture (todos contra todos) + matriz de IDs por comprensión
# -----------------------------

def generar_fixture(equipos,partidos, fechas, fixture_ids):
    """
    Genera fixture con 10 equipos (1..10) en formato liga (método del círculo).
    - Llena 'partidos': dic {id: {id, fecha, local, visitante, jugado, eventos:[], gl, gv}}
    - Llena 'fechas': dic {fecha: [ids]}
    - Llena 'fixture_ids' (10x10) con el id del partido para cada par (i,j). Diagonal en 0.
    """
    print("\n=== Generación automática de Fixture (todos contra todos) ===")
    # La matriz fixture_ids ya viene inicializada, solo se modifica su contenido
    # lista de códigos 1..10
    # Generar todos los pares posibles (local, visitante) donde local < visitante
    pares = []
    i = 0
    while i < 10:
        j = i + 1
        while j < 10:
            pares.append([i, j])
            j += 1
        i += 1
    # Crear lista de IDs del 1 al 45 y mezclar aleatoriamente
    ids = [x+1 for x in range(45)]
    # Mezclar usando asignación aleatoria de valores y .sort()
    valores_aleatorios = [random.randint(1, 100000) for _ in range(45)]
    ids.sort(key=lambda x: valores_aleatorios[x-1])
    # Asignar los IDs mezclados a los pares
    k = 0
    while k < 45:
        i = pares[k][0]
        j = pares[k][1]
        id_partido = ids[k]
        # Asignar en la matriz (simétrica)
        fixture_ids[i][j] = id_partido
        fixture_ids[j][i] = id_partido
        # Crear partido y asignar a la lista de partidos y fechas
        fecha = (k // 5) + 1
        p = [id_partido, fecha, i+1, j+1, False, [], 0, 0]
        partidos.append(p)
        fechas[fecha-1].append(id_partido)
        k += 1
    # Diagonal en cero
    i = 0
    while i < 10:
        fixture_ids[i][i] = 0
        i += 1

    # Mostrar matriz de fixture (IDs)
    print("\nMATRIZ DE FIXTURE (IDs)")
    cab = "     "
    c = 1
    while c <= 10:
        cab += "%4d" % c
        c += 1
    print(cab)
    print("    " + "-" * 40)
    i = 0
    while i < 10:
        fila = "%3d |" % (i+1)
        j = 0
        while j < 10:
            fila += "%4d" % fixture_ids[i][j]
            j += 1
        print(fila)
        i += 1
    print("\nFixture generado.\n")

# -----------------------------
# Registro de partidos y eventos + validaciones
# -----------------------------

def contar_goles_eventos(eventos, cod_local, cod_visitante):
    gl = 0
    gv = 0
    i = 0
    while i < len(eventos):
        e = eventos[i]
        if e['tipo'] == 'G':
            if e['equipo'] == cod_local:
                gl += 1
            elif e['equipo'] == cod_visitante:
                gv += 1
        i += 1
    return gl, gv

def registrar_partidos_y_eventos(equipos, jugadores_nombres, partidos, fixture_ids,
                                  PJ, PG, PE, PP, GF, GC,
                                  goles_jug, amar_jug, rojas_jug):
    print("\n=== Registro de Partidos y Eventos ===")
    print("(Ingrese ID de partido = 0 para finalizar)")

    # Mostrar matriz de fixture para ayudar al usuario
    print("\nMATRIZ DE FIXTURE (IDs)")
    cab = "     "
    for c in range(1, 11):
        cab += "%4d" % c
    print(cab)
    print("    " + "-" * 40)
    for i in range(10):
        fila = "%3d |" % (i+1)
        for j in range(10):
            fila += "%4d" % fixture_ids[i][j]
        print(fila)

    fin = False
    while not fin:
        pid = leer_entero("ID de partido: ", minimo=0)
        if pid == 0:
            print("Fin de registro.\n")
            fin = True
        else:
            partido = None
            for p in partidos:
                if p[0] == pid:
                    partido = p
                    fin = True
            if partido is None:
                print("ID inexistente en el fixture.")
            else:
                jugado = False
                if len(partido) > 4:
                    jugado = partido[4]
                if jugado:
                    print("Ese partido ya fue registrado.")
                else:
                    cod_local = leer_entero("Código equipo LOCAL (1..10): ", minimo=1, maximo=10)
                    cod_visit = leer_entero("Código equipo VISITANTE (1..10): ", minimo=1, maximo=10)
                    if cod_local == cod_visit:
                        print("Local y visitante no pueden ser iguales.")
                    else:
                        esperado = fixture_ids[cod_local-1][cod_visit-1]
                        if esperado != pid:
                            print("El ID no coincide con el fixture para ese cruce.")
                        else:
                            gl_decl = leer_entero("Goles del LOCAL (>=0): ", minimo=0)
                            gv_decl = leer_entero("Goles del VISITANTE (>=0): ", minimo=0)
                            print("Cargue eventos. Deje Tipo vacío para finalizar.")
                            eventos = []
                            fin_eventos = False
                            while not fin_eventos:
                                tipo = input("  Tipo (G/A/R) [enter=fin]: ").strip().upper()
                                if tipo == "":
                                    fin_eventos = True
                                else:
                                    valido_tipo = False
                                    for t in ['G', 'A', 'R']:
                                        if tipo == t:
                                            valido_tipo = True
                                    if not valido_tipo:
                                        print("  Tipo inválido.")
                                    else:
                                        lado = leer_opcion("  Equipo del evento (L/V): ", ["L", "V"])
                                        cod_eq_ev = cod_local if lado == 'L' else cod_visit
                                        cod_j = leer_entero("  Código de jugador (1..10): ", minimo=1, maximo=10)
                                        minuto = leer_entero("  Minuto (0..90): ", minimo=0, maximo=90)
                                        eventos.append([tipo, cod_eq_ev, cod_j, minuto])

                            # Ordenar eventos por minuto (sort)
                            eventos.sort(key=lambda x: x[3])

                            # Consistencia resultado–eventos (contar G)
                            gl_ev = 0
                            gv_ev = 0
                            for e in eventos:
                                if e[0] == 'G':
                                    if e[1] == cod_local:
                                        gl_ev += 1
                                    elif e[1] == cod_visit:
                                        gv_ev += 1
                            if gl_ev != gl_decl or gv_ev != gv_decl:
                                print("Inconsistencia: el resultado declarado no coincide con los goles de los eventos.")
                                print(f"Declarado: {gl_decl}-{gv_decl} | Por eventos: {gl_ev}-{gv_ev}")
                                print("Registro cancelado. Vuelva a intentarlo.")
                            else:

                                # Actualizar partido
                                partido[4] = True
                                partido[5] = eventos
                                partido[6] = gl_decl
                                partido[7] = gv_decl

                                # Actualizar estadísticas de equipos
                                idxL = cod_local - 1
                                idxV = cod_visit - 1
                                PJ[idxL] += 1
                                PJ[idxV] += 1
                                GF[idxL] += gl_decl
                                GC[idxL] += gv_decl
                                GF[idxV] += gv_decl
                                GC[idxV] += gl_decl
                                if gl_decl > gv_decl:
                                    PG[idxL] += 1
                                    PP[idxV] += 1
                                elif gl_decl < gv_decl:
                                    PG[idxV] += 1
                                    PP[idxL] += 1
                                else:
                                    PE[idxL] += 1
                                    PE[idxV] += 1

                                # Actualizar estadísticas individuales
                                for e in eventos:
                                    i_eq = e[1] - 1
                                    j_jug = e[2] - 1
                                    if e[0] == 'G':
                                        goles_jug[i_eq][j_jug] += 1
                                    elif e[0] == 'A':
                                        amar_jug[i_eq][j_jug] += 1
                                    elif e[0] == 'R':
                                        rojas_jug[i_eq][j_jug] += 1
                                print(f"Partido registrado: ID {pid} -> {equipos[cod_local-1]} {gl_decl}-{gv_decl} {equipos[cod_visit-1]}\n")

# -----------------------------
# Informes
# -----------------------------

def puntos_equipo(PG, PE):
    return PG * 3 + PE


def ListadoPosiciones(equipos, PJ, PG, PE, PP, GF, GC):
    print("\nTABLA DE POSICIONES")
    print(" COD EQUIPO                  PJ  PG  PE  PP  GF  GC  DG  PTS")
    filas = []
    i = 0
    while i < 10:
        pts = puntos_equipo(PG[i], PE[i])
        dg = GF[i] - GC[i]
        filas.append([pts, i])
        i += 1

    # Orden: por PTS desc (sin desempates adicionales). Estable por índice.
    filas.sort(key=lambda x: (-x[0])*100 + x[1])
    for fila in filas:
        pts = fila[0]
        i = fila[1]
        dg = GF[i] - GC[i]
        print(" %3d %-22s %3d %3d %3d %3d %3d %3d %3d %4d" % (
            i+1, equipos[i], PJ[i], PG[i], PE[i], PP[i], GF[i], GC[i], dg, pts
        ))
    print("-" * 64)


def ListadoGoleadores(equipos, jugadores_nombres, goles_jug): 
    print("\nRANKING DE GOLEADORES")
    print(" GOLES  EQ  JUG  EQUIPO                 JUGADOR")
    filas = []
    i = 0
    while i < 10:
        j = 0
        while j < 10:
            g = goles_jug[i][j]
            if g > 0:
                filas.append([g, i, j])
            j += 1
        i += 1

    # Orden: goles desc, luego por equipo y jugador (estable
    filas.sort(key=lambda x: (-x[0])*10000 + x[1]*100 + x[2])
    if len(filas) == 0:
        print(" (No se registraron goles)")
        return
    for fila in filas:
        g = fila[0] 
        i = fila[1]
        j = fila[2]
        print(" %5d  %2d  %3d  %-22s %-20s" % (g, i+1, j+1, equipos[i], jugadores_nombres[i][j]))


def EquipoLider(equipos, PG, PE):
    # Máximo PTS (único según alcance). Si hubiera empate, toma el primero por índice.
    mejor_pts = -1
    idx = -1
    i = 0
    while i < 10:
        pts = puntos_equipo(PG[i], PE[i])
        if pts > mejor_pts:
            mejor_pts = pts
            idx = i
        i += 1
    if idx == -1:
        print("\nEquipo líder: (no disponible)")
    else:
        print("\nEQUIPO LÍDER: #%d - %s | Puntos: %d" % (idx+1, equipos[idx], mejor_pts))


def TotalesTorneo(equipos, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug):
    
    # Totales de tarjetas y goles a partir de matrices
    goles_total = 0
    amar_total = 0
    rojas_total = 0
    i = 0
    while i < 10:
        j = 0
        while j < 10:
            goles_total += goles_jug[i][j]
            amar_total += amar_jug[i][j]
            rojas_total += rojas_jug[i][j]
            j += 1
        i += 1

    # Promedio de goles por equipo (GF/PJ) por equipo
    print("\nTOTALES DEL TORNEO")
    print(" Goles totales:", goles_total)
    print(" Amarillas totales:", amar_total)
    print(" Rojas totales:", rojas_total)
    print("\nPROMEDIO DE GOLES POR EQUIPO (GF/PJ)")
    i = 0
    while i < 10:
        prom = GF[i] / PJ[i] if PJ[i] > 0 else 0.0

        # Limitar a 2 decimales en impresión manual
        prom_txt = ("%.2f" % prom)
        print(" %2d %-22s PJ=%2d GF=%3d  Prom=%s" % (i+1, equipos[i], PJ[i], GF[i], prom_txt))
        i += 1
        
    # Porcentaje de empates sobre total de partidos jugados
    # Total de partidos jugados = cantidad de 'p' con jugado=True
    jugados = 0
    empates = 0
    for partido in partidos:
        if partido[4]:
            jugados += 1
            if partido[6] == partido[7]:
                empates += 1
    if jugados > 0:
        porc_emp = (empates * 100.0) / jugados
    else:
        porc_emp = 0.0
    print("\nPorcentaje de empates sobre partidos jugados: %.2f%%" % porc_emp)

# -----------------------------
# Menús
# -----------------------------

def menu_informes(equipos, jugadores_nombres, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug):
    seguir = True
    while seguir:
        print("""
=== INFORMES ===
1) Tabla de posiciones
2) Ranking de goleadores
3) Equipo líder
4) Totales del torneo (incluye promedio GF/PJ y % de empates)
0) Volver
""")
        op = leer_opcion("Opción: ", ["0","1","2","3","4"])
        if op == '1':
            ListadoPosiciones(equipos, PJ, PG, PE, PP, GF, GC)
        elif op == '2':
            ListadoGoleadores(equipos, jugadores_nombres, goles_jug)
        elif op == '3':
            EquipoLider(equipos, PG, PE)
        elif op == '4':
            TotalesTorneo(equipos, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug)
        elif op == '0':
            seguir = False

