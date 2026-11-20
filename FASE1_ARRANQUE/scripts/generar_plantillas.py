#!/usr/bin/env python3
"""
Genera las plantillas Excel de la Fase 1 a partir de esquema_fuentes.py:

  plantillas/PLANTILLA_CARGA_FUENTES.xlsx   → una hoja por fuente (14), con validaciones
  plantillas/FORMULARIO_ESTUDIO_TIEMPOS.xlsx → registro de observaciones, resumen y estimación de 3 puntos

Uso:  python FASE1_ARRANQUE/scripts/generar_plantillas.py
Requiere: openpyxl
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from esquema_fuentes import ENUMS, FUENTES

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "plantillas"
AZUL = PatternFill("solid", fgColor="1F3864")
GRIS = PatternFill("solid", fgColor="EDEDED")
AMARILLO = PatternFill("solid", fgColor="FFF2CC")
BLANCO_B = Font(bold=True, color="FFFFFF")
FINO = Side(style="thin", color="BFBFBF")
BORDE = Border(left=FINO, right=FINO, top=FINO, bottom=FINO)
FILAS_VALIDACION = 20000


def hoja_nombre(archivo: str) -> str:
    return archivo.replace(".csv", "")[:31]


def plantilla_fuentes():
    wb = Workbook()
    ws = wb.active
    ws.title = "LEEME"
    filas = [
        ["CAPACITY-ANALIZE · Plantilla de carga de fuentes · Fase 1"],
        [""],
        ["Cómo usar esta plantilla"],
        ["1. Cada hoja corresponde a una fuente (FTE-SRC-01 a 14). No cambie los nombres de las hojas ni de las columnas."],
        ["2. La fila 2 de cada hoja es un EJEMPLO (en gris). Bórrela antes de entregar."],
        ["3. Pase el cursor sobre cada encabezado para ver su definición. Las celdas tienen validaciones (listas, números, fechas)."],
        ["4. Fechas en formato AAAA-MM-DD y meses en AAAA-MM (como texto)."],
        ["5. PRIVACIDAD: use solo seudónimos (COL-0001). Prohibido incluir nombres, cédulas, salarios, correos o diagnósticos médicos (DEC-025, DEC-026)."],
        ["6. Antes de calcular, valide la carga:  python FASE1_ARRANQUE/scripts/validar_carga.py --excel <este_archivo.xlsx>"],
        [""],
        ["Fuente", "Hoja", "Título", "Dueño sugerido", "Llave única"],
    ]
    for f in filas:
        ws.append(f)
    for arch, meta in FUENTES.items():
        ws.append([meta["id"], hoja_nombre(arch), meta["titulo"], meta["dueno"], " + ".join(meta["llave"])])
    ws["A1"].font = Font(bold=True, size=14, color="1F3864")
    ws["A3"].font = Font(bold=True)
    for cell in ws[11]:
        cell.fill, cell.font = AZUL, BLANCO_B
    for col, w in zip("ABCDE", [12, 34, 44, 40, 40]):
        ws.column_dimensions[col].width = w

    # Hoja oculta con listas para validaciones
    li = wb.create_sheet("_listas")
    for j, (k, vals) in enumerate(ENUMS.items(), start=1):
        li.cell(1, j, k)
        for i, v in enumerate(vals, start=2):
            li.cell(i, j, v)
    li.sheet_state = "hidden"
    rango_lista = {k: f"_listas!${get_column_letter(j)}$2:${get_column_letter(j)}${len(v) + 1}"
                   for j, (k, v) in enumerate(ENUMS.items(), start=1)}

    for arch, meta in FUENTES.items():
        sh = wb.create_sheet(hoja_nombre(arch))
        for j, col in enumerate(meta["columnas"], start=1):
            h = sh.cell(1, j, col["nombre"])
            h.fill, h.font, h.border = AZUL, BLANCO_B, BORDE
            h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            nota = f"{col['descripcion']}\nTipo: {col['tipo']}" + ("" if col["requerido"] else " (opcional)")
            if col["lista"]:
                nota += "\nValores: " + ", ".join(ENUMS[col["lista"]])
            h.comment = Comment(nota, "CAPACITY-ANALIZE", width=320, height=140)
            e = sh.cell(2, j, col["ejemplo"])
            e.fill, e.font = GRIS, Font(italic=True, color="7F7F7F")
            sh.column_dimensions[get_column_letter(j)].width = max(14, min(42, len(col["nombre"]) + 6))
            letra = get_column_letter(j)
            rango = f"{letra}3:{letra}{FILAS_VALIDACION}"
            dv = None
            if col["tipo"] == "lista":
                dv = DataValidation(type="list", formula1=f"={rango_lista[col['lista']]}", allow_blank=not col["requerido"])
            elif col["tipo"] == "sn":
                dv = DataValidation(type="list", formula1='"S,N"', allow_blank=False)
            elif col["tipo"] in ("decimal", "entero"):
                mn = col["min"] if col["min"] is not None else -1e12
                mx = col["max"] if col["max"] is not None else 1e12
                dv = DataValidation(type="whole" if col["tipo"] == "entero" else "decimal", operator="between",
                                    formula1=str(mn), formula2=str(mx), allow_blank=not col["requerido"])
            elif col["tipo"] in ("fecha", "periodo"):
                largo = 10 if col["tipo"] == "fecha" else 7
                dv = DataValidation(type="textLength", operator="equal", formula1=str(largo), allow_blank=not col["requerido"])
                sh.column_dimensions[letra].number_format = "@"
                for r in range(2, 3):
                    sh.cell(r, j).number_format = "@"
            if dv is not None:
                dv.error = f"Valor no válido para {col['nombre']}. {col['descripcion']}"
                dv.errorTitle = "CAPACITY-ANALIZE"
                dv.showErrorMessage = True
                sh.add_data_validation(dv)
                dv.add(rango)
        sh.freeze_panes = "A2"
        sh.row_dimensions[1].height = 30
    OUT.mkdir(parents=True, exist_ok=True)
    ruta = OUT / "PLANTILLA_CARGA_FUENTES.xlsx"
    wb.save(ruta)
    return ruta


def formulario_tiempos():
    wb = Workbook()
    ins = wb.active
    ins.title = "Instrucciones"
    txt = [
        ["CAPACITY-ANALIZE · Formulario de estudio de tiempos (PEN-005, PEN-006, DEC-024)"],
        [""],
        ["1. Objetivo: medir el tiempo estándar (minutos por unidad de trabajo) de una actividad, sin reprocesos."],
        ["2. Registre al menos 30 observaciones por actividad, en distintos días, horarios y colaboradores."],
        ["3. Mida desde que inicia hasta que termina la unidad de trabajo; excluya esperas ajenas a la actividad."],
        ["4. Si la unidad es un reproceso, marque es_reproceso = S (se usa para tiempo_reproceso_min)."],
        ["5. Use solo el seudónimo del colaborador; nunca su nombre (DEC-025). Informe al colaborador del objetivo de la medición."],
        ["6. La hoja 'Resumen' calcula el promedio, la mediana y el número de observaciones por actividad."],
        ["7. Si no es posible medir, use la hoja 'Estimacion_3_puntos' (técnica PERT) y regístrelo como 'Estimación experta'."],
        ["8. Entregue el archivo a Capacity Management para actualizar 07_actividades (tiempo_estandar_min y metodo_medicion)."],
    ]
    for t in txt:
        ins.append(t)
    ins["A1"].font = Font(bold=True, size=13, color="1F3864")
    ins.column_dimensions["A"].width = 120

    reg = wb.create_sheet("Registro")
    cab = ["fecha (AAAA-MM-DD)", "unidad_id", "actividad_id", "observador", "colaborador_id (seudónimo)",
           "hora_inicio (hh:mm:ss)", "hora_fin (hh:mm:ss)", "duracion_min", "unidades", "min_por_unidad", "es_reproceso (S/N)", "observaciones"]
    reg.append(cab)
    for cell in reg[1]:
        cell.fill, cell.font, cell.border = AZUL, BLANCO_B, BORDE
        cell.alignment = Alignment(wrap_text=True, horizontal="center")
    for r in range(2, 1002):
        reg.cell(r, 8, f'=IF(AND(F{r}<>"",G{r}<>""),(G{r}-F{r})*1440,"")')
        reg.cell(r, 10, f'=IF(AND(H{r}<>"",I{r}>0),H{r}/I{r},"")')
        reg.cell(r, 6).number_format = "hh:mm:ss"
        reg.cell(r, 7).number_format = "hh:mm:ss"
        reg.cell(r, 8).number_format = "0.00"
        reg.cell(r, 10).number_format = "0.00"
        reg.cell(r, 8).fill = reg.cell(r, 10).fill = AMARILLO
    dv = DataValidation(type="list", formula1='"S,N"', allow_blank=False)
    reg.add_data_validation(dv)
    dv.add("K2:K1001")
    for j, w in enumerate([16, 12, 13, 14, 18, 15, 15, 12, 10, 13, 12, 40], start=1):
        reg.column_dimensions[get_column_letter(j)].width = w
    reg.freeze_panes = "A2"

    res = wb.create_sheet("Resumen")
    res.append(["actividad_id", "observaciones (sin reproceso)", "promedio min/unidad", "mediana min/unidad",
                "observaciones reproceso", "promedio min reproceso", "¿suficiente? (≥30)"])
    for cell in res[1]:
        cell.fill, cell.font = AZUL, BLANCO_B
        cell.alignment = Alignment(wrap_text=True)
    for r in range(2, 52):
        a = f"A{r}"
        res.cell(r, 2, f'=IF({a}="","",COUNTIFS(Registro!$C:$C,{a},Registro!$K:$K,"N"))')
        res.cell(r, 3, f'=IF(OR({a}="",B{r}=0),"",AVERAGEIFS(Registro!$J:$J,Registro!$C:$C,{a},Registro!$K:$K,"N"))')
        res.cell(r, 4, f'=IF(OR({a}="",B{r}=0),"",_xlfn.AGGREGATE(16,6,Registro!$J$2:$J$1001/((Registro!$C$2:$C$1001={a})*(Registro!$K$2:$K$1001="N")),0.5))')
        res.cell(r, 5, f'=IF({a}="","",COUNTIFS(Registro!$C:$C,{a},Registro!$K:$K,"S"))')
        res.cell(r, 6, f'=IF(OR({a}="",E{r}=0),"",AVERAGEIFS(Registro!$J:$J,Registro!$C:$C,{a},Registro!$K:$K,"S"))')
        res.cell(r, 7, f'=IF({a}="","",IF(B{r}>=30,"Sí","No"))')
        for j in (3, 4, 6):
            res.cell(r, j).number_format = "0.00"
    res["A2"] = "ACT-017"
    for j, w in enumerate([14, 16, 16, 16, 16, 16, 14], start=1):
        res.column_dimensions[get_column_letter(j)].width = w

    est = wb.create_sheet("Estimacion_3_puntos")
    est.append(["actividad_id", "experto (cargo)", "optimista (min)", "más probable (min)", "pesimista (min)",
                "estimación PERT = (O + 4M + P) / 6", "desviación = (P - O) / 6", "comentario"])
    for cell in est[1]:
        cell.fill, cell.font = AZUL, BLANCO_B
        cell.alignment = Alignment(wrap_text=True)
    for r in range(2, 102):
        est.cell(r, 6, f'=IF(COUNT(C{r}:E{r})=3,(C{r}+4*D{r}+E{r})/6,"")')
        est.cell(r, 7, f'=IF(COUNT(C{r}:E{r})=3,(E{r}-C{r})/6,"")')
        est.cell(r, 6).number_format = est.cell(r, 7).number_format = "0.00"
        est.cell(r, 6).fill = est.cell(r, 7).fill = AMARILLO
    for j, w in enumerate([14, 22, 14, 16, 14, 22, 18, 40], start=1):
        est.column_dimensions[get_column_letter(j)].width = w
    ruta = OUT / "FORMULARIO_ESTUDIO_TIEMPOS.xlsx"
    wb.save(ruta)
    return ruta


if __name__ == "__main__":
    for r in (plantilla_fuentes(), formulario_tiempos()):
        print("Generado:", r.relative_to(BASE.parent))
