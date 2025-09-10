# =============================================================
# Torneo de Liga Amateur - Programación 1 (UADE)
# Un solo módulo, sin clases ni librerías externas (solo builtins).
# Consola (texto). Estructuras homogéneas (listas y matrices).
# =============================================================

# -----------------------------
# Utilidades de lectura / validación
# -----------------------------

def leer_entero(mensaje, minimo=None, maximo=None):
    """Lee un entero por consola, validando opcionalmente rango [minimo..maximo]."""
    while True:
        try:
            v = int(input(mensaje).strip())
            if minimo is not None and v < minimo:
                print("Valor mínimo permitido:", minimo)
                continue
            if maximo is not None and v > maximo:
                print("Valor máximo permitido:", maximo)
                continue
            return v
        except ValueError:
            print("Entrada inválida. Debe ser un número entero.")


def leer_opcion(mensaje, opciones_validas):
    """Lee una opción de un conjunto permitido. Devuelve en mayúsculas."""
    opciones = [o.upper() for o in opciones_validas]
    while True:
        v = input(mensaje).strip().upper()
        if v in opciones:
            return v
        print("Opción inválida. Valores válidos:", ", ".join(opciones))
""

# -----------------------------
# 1) Equipos y jugadores
# -----------------------------

def normalizar_nombre(s):
    s = s.strip()
    # Usar el método title() para capitalizar cada palabra automáticamente:
    return s.title()


def ingresar_equipos_y_jugadores(equipos, jugadores_nombres, goles_jug, amar_jug, rojas_jug):
    """
    Carga 10 equipos y 10 jugadores por equipo.
    - equipos: lista de 10 nombres de equipo (str)
    - jugadores_nombres: matriz 10x10 de nombres (str)
    - goles_jug, amar_jug, rojas_jug: matrices 10x10 (int) inicializadas en 0
    """
    print("\n=== Ingreso de Equipos y Jugadores ===")
    # nombres de equipos (únicos)
    usados = []
    i = 0
    while i < 10:
        nombre = input(f"Nombre para Equipo {i+1} (enter = 'Equipo {i+1}'): ").strip()
        if nombre == "":
            nombre = f"Equipo {i+1}"
        nombre = normalizar_nombre(nombre)
        # unicidad (case-insensitive)
        existe = False
        k = 0
        while k < len(usados):
            if  usados[k].lower() == nombre.lower():
                existe = True
                k=len(usados) # salir
            k += 1
        if existe:
            print("Ese nombre de equipo ya existe. Ingrese otro.")
            continue
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
            while t < len(usados_j):
                if usados_j[t].lower() == nombre_j.lower():
                    existe_j = True
                    break
                t += 1
            if existe_j:
                print("    Ese nombre ya existe en este equipo. Ingrese otro.")
                continue
            jugadores_nombres[i][j] = nombre_j
            goles_jug[i][j] = 0
            amar_jug[i][j] = 0
            rojas_jug[i][j] = 0
            usados_j.append(nombre_j)
            j += 1
        i += 1
    print("Ingreso completado.\n")


# -----------------------------
# 2) Fixture (todos contra todos) + matriz de IDs por comprensión
# -----------------------------

def generar_fixture(equipos, partidos, fechas, fixture_ids):
    """
    Genera fixture con 10 equipos (1..10) en formato liga (método del círculo).
    - Llena 'partidos': dic {id: {id, fecha, local, visitante, jugado, eventos:[], gl, gv}}
    - Llena 'fechas': dic {fecha: [ids]}
    - Llena 'fixture_ids' (10x10) con el id del partido para cada par (i,j). Diagonal en 0.
    """
    print("\n=== Generación automática de Fixture (todos contra todos) ===")
    partidos.clear()
    fechas.clear()
    # Reset matriz fixture_ids
    i = 0
    while i < 10:
        j = 0
        while j < 10:
            fixture_ids[i][j] = 0
            j += 1
        i += 1

    # lista de códigos 1..10
    cods = [k+1 for k in range(10)]
    n = len(cods)
    mitad = n // 2
    jornadas = n - 1
    rot = cods[1:]  # rotación, sin el primero

    id_counter = 1
    fecha = 1
    while fecha <= jornadas:
        izquierda = [cods[0]] + rot[:mitad-1]
        derecha = rot[mitad-1:][::-1]
        i = 0
        while i < mitad:
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

    # Para evitar duplicados: no permitir registrar un partido ya jugado.
    while True:
        pid = leer_entero("ID de partido: ", minimo=0)
        if pid == 0:
            print("Fin de registro.\n")
            break
        if pid not in partidos:
            print("ID inexistente en el fixture.")
            continue
        if partidos[pid]['jugado']:
            print("Ese partido ya fue registrado.")
            continue

        # Se pide también local y visitante (validación contra fixture)
        cod_local = leer_entero("Código equipo LOCAL (1..10): ", minimo=1, maximo=10)
        cod_visit = leer_entero("Código equipo VISITANTE (1..10): ", minimo=1, maximo=10)
        if cod_local == cod_visit:
            print("Local y visitante no pueden ser iguales.")
            continue
        # Consistencia con fixture: el ID debe coincidir con la matriz (aceptamos simétrica)
        esperado = fixture_ids[cod_local-1][cod_visit-1]
        if esperado != pid:
            print("El ID no coincide con el fixture para ese cruce.")
            continue

        # Resultado declarado
        gl_decl = leer_entero("Goles del LOCAL (>=0): ", minimo=0)
        gv_decl = leer_entero("Goles del VISITANTE (>=0): ", minimo=0)

        # Carga de eventos
        print("Cargue eventos. Deje Tipo vacío para finalizar.")
        eventos = []
        while True:
            tipo = input("  Tipo (G/A/R) [enter=fin]: ").strip().upper()
            if tipo == "":
                break
            if not (tipo == 'G' or tipo == 'A' or tipo == 'R'):
                print("  Tipo inválido.")
                continue
            lado = leer_opcion("  Equipo del evento (L/V): ", ["L", "V"])  # asociación explícita
            cod_eq_ev = cod_local if lado == 'L' else cod_visit
            cod_j = leer_entero("  Código de jugador (1..10): ", minimo=1, maximo=10)
            # pertenencia al equipo (jugador 1..10 existe para cualquier equipo)
            minuto = leer_entero("  Minuto (0..90): ", minimo=0, maximo=90)
            eventos.append({'tipo': tipo, 'equipo': cod_eq_ev, 'jugador': cod_j, 'minuto': minuto})

        # Ordenar cronológicamente (burbuja para P1)
        i = 0
        while i < len(eventos) - 1:
            j = 0
            while j < len(eventos) - 1 - i:
                if eventos[j]['minuto'] > eventos[j+1]['minuto']:
                    aux = eventos[j]
                    eventos[j] = eventos[j+1]
                    eventos[j+1] = aux
                j += 1
            i += 1

        # Consistencia resultado–eventos (contar G)
        gl_ev, gv_ev = contar_goles_eventos(eventos, cod_local, cod_visit)
        if gl_ev != gl_decl or gv_ev != gv_decl:
            print("Inconsistencia: el resultado declarado no coincide con los goles de los eventos.")
            print(f"Declarado: {gl_decl}-{gv_decl} | Por eventos: {gl_ev}-{gv_ev}")
            print("Registro cancelado. Vuelva a intentarlo.")
            continue

        # Aplicar al partido (usar el id real del fixture)
        p = partidos[pid]
        p['eventos'] = eventos
        p['gl'] = gl_decl
        p['gv'] = gv_decl
        p['jugado'] = True

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
        k = 0
        while k < len(eventos):
            e = eventos[k]
            i_eq = e['equipo'] - 1
            j_jug = e['jugador'] - 1
            if e['tipo'] == 'G':
                goles_jug[i_eq][j_jug] += 1
            elif e['tipo'] == 'A':
                amar_jug[i_eq][j_jug] += 1
            elif e['tipo'] == 'R':
                rojas_jug[i_eq][j_jug] += 1
            k += 1

        print(f"Partido registrado: ID {pid} -> {equipos[cod_local-1]} {gl_decl}-{gv_decl} {equipos[cod_visit-1]}\n")


# -----------------------------
# 4) Informes
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
        filas.append((pts, i))
        i += 1
    # Orden: por PTS desc (sin desempates adicionales). Estable por índice.
    filas = sorted(filas, key=lambda x: (-x[0], x[1]))
    for pts, i in filas:
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
                filas.append((g, i, j))
            j += 1
        i += 1
    # Orden: goles desc, luego por equipo y jugador (estable)
    filas = sorted(filas, key=lambda x: (-x[0], x[1], x[2]))
    if len(filas) == 0:
        print(" (sin goles registrados)")
        return
    for g, i, j in filas:
        print(" %5d  %2d  %3d  %-22s %-20s" % (g, i+1, j+1, equipos[i], jugadores_nombres[i][j]))


def EquipoLider(equipos, PJ, PG, PE, PP, GF, GC):
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
    for pid in partidos:
        if partidos[pid]['jugado']:
            jugados += 1
            if partidos[pid]['gl'] == partidos[pid]['gv']:
                empates += 1
    if jugados > 0:
        porc_emp = (empates * 100.0) / jugados
    else:
        porc_emp = 0.0
    print("\nPorcentaje de empates sobre partidos jugados: %.2f%%" % porc_emp)


# -----------------------------
# 5) Menús
# -----------------------------

def mostrar_fixture(equipos, fechas, partidos):
    if len(fechas) == 0:
        print("No hay fixture generado.")
        return
    # Mostrar por fecha
    jornadas = len(fechas)
    f = 1
    while f <= jornadas:
        print(f"\nFECHA {f}")
        idx = 0
        while idx < len(fechas[f]):
            pid = fechas[f][idx]
            p = partidos[pid]
            # p = [id, fecha, local, visitante, jugado, eventos, gl, gv]
            print("  ID %02d: %s (#%d) vs %s (#%d)" % (
                p[0], equipos[p[2]-1], p[2], equipos[p[3]-1], p[3]
            ))
            idx += 1
        f += 1


def menu_informes(equipos, jugadores_nombres, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug):
    while True:
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
            EquipoLider(equipos, PJ, PG, PE, PP, GF, GC)
        elif op == '4':
            TotalesTorneo(equipos, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug)
        elif op == '0':
            break


# -----------------------------
# 6) Programa principal
# -----------------------------

def main():
    # Estructuras principales homogéneas
    equipos = [""] * 10                                       # nombres equipos
    jugadores_nombres = [[""]*10 for _ in range(10)]          # matriz 10x10 nombres
    goles_jug = [[0]*10 for _ in range(10)]                    # goles por jugador
    amar_jug = [[0]*10 for _ in range(10)]                     # amarillas por jugador
    rojas_jug = [[0]*10 for _ in range(10)]                    # rojas por jugador

    # Tabla de posiciones (por equipo)
    PJ = [0]*10; PG = [0]*10; PE = [0]*10; PP = [0]*10; GF = [0]*10; GC = [0]*10

    # Fixture
    partidos = {}      # id -> {id, fecha, local, visitante, jugado, eventos, gl, gv}
    fechas = {}        # fecha -> [ids]
    fixture_ids = [[0 for _ in range(10)] for _ in range(10)]  # matriz por comprensión

    while True:
        print("""
==============================
 Torneo de Liga (Consola)
==============================
1) Ingresar equipos y jugadores
2) Generar fixture (y matriz de IDs)
3) Registrar partidos y eventos
4) Mostrar fixture
5) Informes
0) Salir
""")
        op = leer_opcion("Opción: ", ["0","1","2","3","4","5"])
        if op == '1':
            ingresar_equipos_y_jugadores(equipos, jugadores_nombres, goles_jug, amar_jug, rojas_jug)
        elif op == '2':
            # Verificar que haya equipos cargados
            ok = True
            i = 0
            while i < 10:
                if equipos[i] == "":
                    ok = False
                    break
                j = 0
                while j < 10:
                    if jugadores_nombres[i][j] == "":
                        ok = False
                        break
                    j += 1
                i += 1
            if not ok:
                print("Primero debe cargar los 10 equipos y sus 10 jugadores cada uno (opción 1).")
            else:
                generar_fixture(equipos, partidos, fechas, fixture_ids)
        elif op == '3':
            if len(partidos) == 0:
                print("Primero genere el fixture (opción 2).")
            else:
                registrar_partidos_y_eventos(equipos, jugadores_nombres, partidos, fixture_ids,
                                             PJ, PG, PE, PP, GF, GC,
                                             goles_jug, amar_jug, rojas_jug)
        elif op == '4':
            mostrar_fixture(equipos, fechas, partidos)
        elif op == '5':
            menu_informes(equipos, jugadores_nombres, partidos, PJ, PG, PE, PP, GF, GC, goles_jug, amar_jug, rojas_jug)
        elif op == '0':
            print("¡Hasta luego!")
            break


if __name__ == '__main__':
    main()
