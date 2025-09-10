def leer_entero(mensaje, minimo=None, maximo=None):
    """Lee un entero por consola, validando opcionalmente rango [minimo..maximo]."""
    valido = False
    valor = None

    while not valido:
        entrada = input(mensaje).strip()

        # Validar entero (acepta negativos con un solo '-')
        if entrada.lstrip("-").isdigit() and entrada.count("-") <= 1 and not entrada.endswith("-"):
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


def normalizar_nombre(s):
    s = s.strip()
    # Usar el método title() para capitalizar cada palabra automáticamente:
    return s.title()

# -----------------------------
# 1) Equipos y jugadores
# -----------------------------

def ingresar_EyJ(equipos, jugadores_nombres, goles_jug, amar_jug, rojas_jug):
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
                nombre_j = normalizar_nombre(nombre_j)

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
# 2) Fixture (todos contra todos) + matriz de IDs por comprensión
# -----------------------------

def generar_fixture(partidos, fechas, fixture_ids):
    """
    Genera fixture con 10 equipos (1..10) en formato liga (método del círculo).
    - Llena 'partidos': dic {id: {id, fecha, local, visitante, jugado, eventos:[], gl, gv}}
    - Llena 'fechas': dic {fecha: [ids]}
    - Llena 'fixture_ids' (10x10) con el id del partido para cada par (i,j). Diagonal en 0.
    """
    print("\n=== Generación automática de Fixture (todos contra todos) ===")
    # Creación matriz fixture_ids en 0
    fixture_ids = [[0] * 10 for _ in range(10)]
    # lista de códigos 1..10
    cods = list(range(1, 11))
    rot = cods[1:]  # rotación, sin el primero

    id_counter = 1
    fecha = 1
    while fecha <= 9:
        izquierda = [cods[0]] + rot[:4]
        derecha = rot[4:][::-1]
        i = 0
        while i < 5:
            a = izquierda[i]
            b = derecha[i]
            # Alternamos localía por fecha
            if fecha % 2 == 0:
                local = b
                visitante = a
            else:
                local = a
                visitante = b
            # Crear partido como lista: [id, fecha, local, visitante, jugado, eventos, gl, gv]
            p = [id_counter, fecha, local, visitante, False, [], 0, 0]
            partidos[id_counter] = p
            if fecha not in fechas:
                fechas[fecha] = []
            fechas[fecha].append(id_counter)
            # matriz fixture (simétrica)
            fixture_ids[local-1][visitante-1] = id_counter
            fixture_ids[visitante-1][local-1] = id_counter
            id_counter += 1
            i += 1
        # rotar
        if len(rot) > 0:
            rot = [rot[-1]] + rot[:-1]
        fecha += 1



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
# 3) Registro de partidos y eventos + validaciones
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

    fin = False
    while not fin:
        pid = leer_entero("ID de partido: ", minimo=0)
        if pid == 0:
            print("Fin de registro.\n")
            fin = True
        else:
            existe = False
            for k in partidos:
                if k == pid:
                    existe = True
            if not existe:
                print("ID inexistente en el fixture.")
            else:
                partido = partidos[pid]
                jugado = False
                # partido como lista: [id, fecha, local, visitante, jugado, eventos, gl, gv]
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


"FALTA DESDE INFOMES, MENU Y MAIN"

