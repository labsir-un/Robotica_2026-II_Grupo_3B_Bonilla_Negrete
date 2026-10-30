# Laboratorio No. 01 - Robótica Industrial - Trayectorias, Entradas y Salidas Digitales


<p align="center">
  <img src="Imagenes\Foto_Con_Resultado.jpeg"  width="400"/>
</p>

## Video de la Práctica
[Ver Video en YouTube](https://www.youtube.com/watch?v=aElz2iVJS0k)

> **Nota:** El vídeo muestra tanto la simulación desarrollada en RobotStudio como la implementación final con el robot real.

---

## Problema 
En la industria de alimentos, particularmente en los procesos de panadería y repostería, diversas operaciones repetitivas pueden ser automatizadas utilizando robots industriales.

Una aplicación de este tipo corresponde a la decoración automática de tortas mediante el seguimiento controlado
de trayectorias

<p align="center">
  <img src="Imagenes\TortaEjemplos.png" alt="Ejemplo de torta" width="400"/>
</p>

En los siguientes enlaces pueden observarse algunos ejemplos de automatización de procesos de decoración utilizando robots industriales:

[Enlace 1](https://www.youtube.com/watch?v=ROowhMuF15s)

[Enlace 2](https://www.youtube.com/watch?v=zf44RV27WsEs)


Inspirados en estos ejemplos y considerando las características de los equipos disponibles en el laboratorio, cada grupo debía desarrollar una celda simplificada para la decoración automática de una torta virtual.


## Descripción Detallada de la Solución Implementada

La torta es representada mediante una superficie plana  rectangular ubicada inicialmente sobre una banda transportadora.

La banda transporta la torta hasta la estación de trabajo del robot. Una vez ubicada dentro de su espacio de
trabajo, la banda se detiene completamente y el robot realiza la decoración.

Finalizada la operación, el robot regresa a su posición HOME y la banda transportadora se pone nuevamente en movimiento para trasladar la torta decorada hasta el extremo final de la banda.

---

## Plano de Planta

Ubicación y distribución espacial de los elementos utilizados:

<div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
  <img src="Imagenes/RepGrafiso.png" width="48%" />
  <img src="Imagenes/RepGrafTop.png" width="48%" />
</div>

---

## Diseño y Modelo CAD de la Herramienta

### Diseño Detallado
En esta etapa fue fundamental considerar dos factores clave para optimizar la resistencia mecánica de la herramienta ante impactos:

La inclusión de redondeos en las aristas de acople entre geometrías para reducir la concentración de esfuerzos.

La integración de un resorte que proporciona un margen de tolerancia en la dirección normal, absorbiendo cargas imprevistas.

### Modelo CAD

<table border="0" align="center" style="border-collapse: collapse; margin-bottom: 40px;">
  <tr>
    <td align="center" valign="middle" style="border: none; padding: 10px;">
      <img src="Imagenes/AgarreSeccion.png" height="300" style="vertical-align: middle;" />
      <p><b>Figura 1:</b> Vista en sección</p>
    </td>
    <td align="center" valign="middle" style="border: none; padding: 10px;">
      <img src="Imagenes/AgarreRender.png" height="300" style="vertical-align: middle;" />
      <p><b>Figura 2:</b> Render 3D</p>
    </td>
  </tr>
</table>
Adicionalmente, se diseñó un mecanismo de agarre alternativo para la tapa trasera, el cual garantiza la fijación del conjunto y previene desacoples causados por vibraciones operativas:

<p align="center">
  <img src="Imagenes/AnimacionTapa.gif" alt="Animación del sistema en Fusion" width="300"/>
</p>

---

## Diagrama de Flujo

El programa corre en un ciclo infinito (WHILE TRUE). En cada vuelta el robot regresa a home y consulta, en orden, tres entradas digitales. Las condiciones no son excluyentes: se evalúan una tras otra en la misma vuelta.

| Paso | Condición | Acciones del robot y de las E/S |
|---|---|---|
| 0 | Arranque de `main` | Entra al ciclo `WHILE TRUE` |
| 1 | Siempre | `Path_20`: `MoveJ` a `Target_home` (referencia `wobj0`) |
| 2 | `DI_01 = 1` (decorar pastel) | `SET DO_01` → `SET FWD_Conveyor` → espera 3.8 s → `RESET FWD_Conveyor` → `Path_10` (trayectoria de decoración) → `Path_20` (home) → `SET FWD_Conveyor` → espera 5 s → `RESET FWD_Conveyor` → `RESET DO_01` |
| 3 | `DI_02 = 1` (modo mantenimiento) | `SET DO_02` → `Path_40` (`MoveJ` a `MANTENIMIENTO`) → espera 2 s → mientras `DI_02 = 0` espera 0.5 s → `Path_20` (home) → `RESET DO_02` |
| 4 | `DI_03 = 1` (secuencia de reorientación) | `SET DO_03` → `FarmearAura` (`Path_50`) → `Path_20` (home) → `RESET DO_03` |
| 5 | Fin de la vuelta | Regresa al paso 1 |

La figura del diagrama de flujo se incluye a continuación:



![Diagrama de flujo del sistema](docs/diagrama_flujo.png)

---

## Instrucciones y Funciones de RAPID

### 2.1 Estructura del programa

| Elemento | Descripción |
|---|---|
| `MODULE Module1 … ENDMODULE` | Módulo único que contiene datos, trayectorias y programa principal |
| `PROC main()` | Punto de entrada: ciclo infinito con la lógica |
| `PROC Path_10()` | Trayectoria de decoración del pastel (≈ 253 `MoveL` y 1 `MoveJ` inicial, más 3 `MoveJ` de reposicionamiento) |
| `PROC Path_20()` | Ir a la posición *home* |
| `PROC Path_40()` | Ir a la posición de mantenimiento |
| `PROC Path_50()` | Barrido de orientación del TCP en un punto fijo (11 `MoveJ`) |
| `PROC FarmearAura()` | Procedimiento contenedor que solo llama a `Path_50` |

Los procedimientos sin parámetros se llaman escribiendo solo su nombre (por ejemplo `Path_20;`), lo que permite estructurar el programa de forma modular.

### 2.2 Tipos de datos

| Tipo | Uso en el código | Detalle |
|---|---|---|
| `tooldata` | `marcador` | `[robhold, tframe, tload]`. `TRUE`: la herramienta va sujeta al robot. TCP en `[38.907, -1, 151.09]` mm respecto a la brida; orientación `[0.9659, 0, 0.2588, 0]` (rotación de 30° sobre Y); carga de 1 kg con centro de gravedad `[0,0,1]` |
| `wobjdata` | `Workobject_pastel` | `[robhold, ufprog, ufmec, uframe, oframe]`. `FALSE`: objeto fijo (no sujeto por el robot). `TRUE`: sistema de usuario fijo programado. `uframe` en `[644.76, -106.22, 117.65]` con orientación `[0,0,1,0]` (giro de 180° sobre Y, por lo que el eje Z del objeto apunta hacia abajo); `oframe` sin desplazamiento |
| `robtarget` | 272 objetivos (`Target_10` … `Target_2670_2`, `MANTENIMIENTO`, `Target_home`) | `[trans, rot, robconf, extax]`: posición XYZ en mm, orientación en cuaternión, configuración de ejes `[cf1, cf4, cf6, cfx]` y ejes externos sin usar (`9E+09`) |
| `speeddata` | `v100` | Velocidad del TCP de 100 mm/s |
| `zonedata` | `z5` | Zona de paso de 5 mm (trayectoria redondeada) |
| Señales | `DI_01..03`, `DO_01..03`, `FWD_Conveyor` | Entradas y salidas digitales del controlador |

`CONST` se usa para los objetivos (valores que no cambian) y `PERS` para `tooldata`/`wobjdata` (datos persistentes que el sistema puede actualizar, por ejemplo tras una calibración).

### 2.3 Instrucciones de movimiento

| Instrucción | Función | Ejemplo del código |
|---|---|---|
| `MoveJ` | Movimiento articular de un punto a otro del espacio que no sigue una trayectoria fija. Se usa para aproximaciones y cambios de zona | `MoveJ Target_home,v100,z5,marcador\WObj:=wobj0;` |
| `MoveL` | Movimiento lineal del TCP. Se usa en todo el trazado para que los trazos sean rectos | `MoveL Target_20,v100,z5,marcador\WObj:=Workobject_pastel;` |
| `\WObj` | Argumento opcional que indica el objeto de trabajo en cuyas coordenadas está definido el `robtarget`. `wobj0` es el sistema de la base del robot | `\WObj:=Workobject_pastel` |
---

### 2.4 Instrucciones y lógica

| Instrucción | Función | Uso en el código |
|---|---|---|
| `SET señal` | Pone una salida digital en 1 | `SET DO_01; SET FWD_Conveyor;` |
| `RESET señal` | Pone una salida digital en 0 | `RESET FWD_Conveyor; RESET DO_01;` |
| `IF … THEN … ENDIF` | Ejecución condicional | `IF DI_01 = 1 THEN … ENDIF` |
| `WHILE … DO … ENDWHILE` | Ciclo condicional | `WHILE TRUE DO` (ciclo principal) y `WHILE DI_02=0 DO` (espera) |
| `WaitTime t` | Pausa de t segundos | `WaitTime 3.8;` (avance de banda), `WaitTime 0.5;` |
| Llamada a procedimiento | Ejecuta un `PROC` | `Path_10;` `Path_20;` `FarmearAura;` |

### 2.5 Entradas digitales (pulsadores)

El sistema se opera con tres pulsadores conectados a las entradas digitales del controlador. Cada uno inicia una rutina distinta, y la salida digital asociada se activa mientras la rutina se ejecuta.

| Señal | Elemento | Acción que dispara | Salida asociada |
|---|---|---|---|
| `DI_01` | Entrada digital 1: Pulsador 1 | Ciclo de decoración: avanza la banda 3.8 s, ejecuta `Path_10`, vuelve a *home* y evacua el pastel con la banda 5 s | `DO_01` y `FWD_Conveyor` |
| `DI_02` | Entrada digital 2: Pulsador 2 | Modo mantenimiento: lleva el robot a la posición `MANTENIMIENTO` (`Path_40`). Una segunda pulsación lo devuelve a *home* | `DO_02` |
| `DI_03` | Entrada digital 3: Pulsador 3 | Secuencia `FarmearAura`: el TCP gira de 0° a 90° y regresa a 0° en un punto fijo (`Path_50`) | `DO_03` |


## Comparación de Calibración de la Herramienta

Análisis comparativo de los resultados obtenidos al calibrar el TCP (Tool Center Point) mediante:
1. **RobotStudio (Simulación):** [Resultados/Valores]
2. **Robot Real:** [Resultados/Valores]

**Conclusiones y diferencias observadas:**
[Insertar texto comparativo y margen de error/diferencias encobradas.]

---

## Código Completo en RAPID

```rapid
MODULE Module1
    TASK PERS wobjdata Workobject_pastel:=[FALSE,TRUE,"",[[644.76,-106.22,117.65],[0,0,1,0]],[[0,0,0],[1,0,0,0]]];
    PERS tooldata marcador:=[TRUE,[[38.907,-1,151.09],[0.965925826,0,0.258819045,0]],[1,[0,0,1],[1,0,0,0],0,0,0]];
    CONST robtarget Target_10:=[[119.278,17.377,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_20:=[[119.278,17.377,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_30:=[[97.278,17.377,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_40:=[[97.278,31.124,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_50:=[[99.874,31.124,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_60:=[[99.874,20.289,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_70:=[[119.278,20.289,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_80:=[[119.278,17.377,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_90:=[[119.278,17.377,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_100:=[[119.278,35.085,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_110:=[[97.278,35.085,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_120:=[[97.278,37.997,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_130:=[[119.278,37.997,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_140:=[[119.278,35.085,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_150:=[[119.278,35.085,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_160:=[[119.278,50.828,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_170:=[[104.121,50.828,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_180:=[[101.367,50.528,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_190:=[[99.499,47.541,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_200:=[[100.429,45.215,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_210:=[[103.881,44.27,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_220:=[[103.521,41.643,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_230:=[[98.568,43.122,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_240:=[[96.903,47.556,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_250:=[[97.698,50.955,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_260:=[[100.009,53.071,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_270:=[[104.286,53.739,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_280:=[[119.278,53.739,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_290:=[[119.278,50.828,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_300:=[[119.278,50.828,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_310:=[[119.278,64.529,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_320:=[[97.278,56.08,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_330:=[[97.278,59.171,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_340:=[[103.941,61.588,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_350:=[[103.941,70.787,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_360:=[[97.278,73.353,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_370:=[[97.278,76.669,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_380:=[[119.278,67.665,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_390:=[[119.278,64.529,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_400:=[[116.967,66.03,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_410:=[[116.967,66.03,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_420:=[[106.312,62.428,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_430:=[[106.312,69.886,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_440:=[[116.967,66.03,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_450:=[[116.967,66.03,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_460:=[[119.278,78.905,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_470:=[[119.278,83.287,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_480:=[[100.444,89.545,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_490:=[[119.278,95.983,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_500:=[[119.278,99.9,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_510:=[[97.278,99.9,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_520:=[[97.278,97.094,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_530:=[[115.691,97.094,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_540:=[[97.278,90.701,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_550:=[[97.278,88.075,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_560:=[[116.006,81.712,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_570:=[[97.278,81.712,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_580:=[[97.278,78.905,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_590:=[[119.278,78.905,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_600:=[[119.278,78.905,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_610:=[[119.278,110.63,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_620:=[[119.278,110.63,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_630:=[[97.278,102.181,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_640:=[[97.278,105.272,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_650:=[[103.941,107.689,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_660:=[[103.941,116.888,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_670:=[[97.278,119.454,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_680:=[[97.278,122.77,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_690:=[[119.278,113.766,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_700:=[[119.278,110.63,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_710:=[[119.278,110.63,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_720:=[[116.967,112.131,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_730:=[[106.312,108.529,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_740:=[[106.312,115.987,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_750:=[[116.967,112.131,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_760:=[[116.967,112.131,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_770:=[[119.278,125.066,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_780:=[[97.278,125.066,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_790:=[[97.278,127.858,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_800:=[[114.566,127.858,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_810:=[[97.278,139.413,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_820:=[[97.278,142.399,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_830:=[[119.278,142.399,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_840:=[[119.278,139.608,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_850:=[[102.005,139.608,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_860:=[[119.278,128.053,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_870:=[[119.278,125.066,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_880:=[[119.278,125.066,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_890:=[[78.744,33.36,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_900:=[[78.744,33.36,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_910:=[[82.211,32.279,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_920:=[[84.529,29.405,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_930:=[[85.317,25.091,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_940:=[[84.567,21.054,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_950:=[[82.368,18.293,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_960:=[[79.255,17.347,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_970:=[[76.516,18.12,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_980:=[[74.467,20.469,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_990:=[[73.094,24.716,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1000:=[[72.021,28.633,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1010:=[[70.723,30.613,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1020:=[[68.915,31.214,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1030:=[[67.031,30.591,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1040:=[[65.673,28.693,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1050:=[[65.178,25.751,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1060:=[[65.831,22.375,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1070:=[[67.542,20.161,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1080:=[[70.25,19.253,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1090:=[[70.01,16.507,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1100:=[[66.056,17.715,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1110:=[[63.437,20.882,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1120:=[[62.567,25.886,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1130:=[[63.43,30.126,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1140:=[[65.846,33.015,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1150:=[[69.155,34.02,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1160:=[[72.284,33.105,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1170:=[[74.527,30.268,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1180:=[[75.931,25.399,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1190:=[[77.499,21.009,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1200:=[[79.45,20.154,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1210:=[[81.783,21.362,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1220:=[[82.751,25.211,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1230:=[[81.686,29.045,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1240:=[[78.534,30.568,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1250:=[[78.744,33.36,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1260:=[[78.744,33.36,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1270:=[[84.942,44.03,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1280:=[[62.942,35.581,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1290:=[[62.942,38.672,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1300:=[[69.605,41.088,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1310:=[[69.605,50.287,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1320:=[[62.942,52.854,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1330:=[[62.942,56.17,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1340:=[[84.942,47.166,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1350:=[[84.942,44.03,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1360:=[[84.942,44.03,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1370:=[[82.631,45.53,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1380:=[[71.976,41.929,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1390:=[[71.976,49.387,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1400:=[[82.631,45.53,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1410:=[[82.631,45.53,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1420:=[[84.942,58.406,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1430:=[[62.942,58.406,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1440:=[[62.942,61.212,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1450:=[[81.671,61.212,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1460:=[[62.942,67.575,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1470:=[[62.942,70.201,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1480:=[[81.356,76.594,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1490:=[[62.942,76.594,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1500:=[[62.942,79.401,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1510:=[[84.942,79.401,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1520:=[[84.942,75.484,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1530:=[[66.109,69.046,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1540:=[[84.942,62.788,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1550:=[[84.942,58.406,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1560:=[[84.942,58.406,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1570:=[[84.942,84.143,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1580:=[[72.231,84.143,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1590:=[[66.716,84.983,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1600:=[[63.632,87.789,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1610:=[[62.567,92.847,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1620:=[[63.79,97.987,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1630:=[[66.964,100.695,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1640:=[[72.231,101.446,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1650:=[[84.942,101.446,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1660:=[[84.942,98.534,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1670:=[[72.246,98.534,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1680:=[[66.649,97.169,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1690:=[[65.193,92.592,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1700:=[[65.928,89.418,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1710:=[[68.022,87.587,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1720:=[[72.246,87.054,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1730:=[[84.942,87.054,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1740:=[[84.942,84.143,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1750:=[[84.942,84.143,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1760:=[[84.942,106.353,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1770:=[[62.942,106.353,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1780:=[[62.942,122.77,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1790:=[[65.538,122.77,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1800:=[[65.538,109.264,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1810:=[[73.027,109.264,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1820:=[[73.027,121.435,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1830:=[[75.608,121.435,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1840:=[[75.608,109.264,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1850:=[[82.346,109.264,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1860:=[[82.346,122.26,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1870:=[[84.942,122.26,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1880:=[[84.942,106.353,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1890:=[[84.942,106.353,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1900:=[[84.942,126.672,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1910:=[[62.942,126.672,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1920:=[[62.942,140.418,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1930:=[[65.538,140.418,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1940:=[[65.538,129.583,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1950:=[[84.942,129.583,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1960:=[[84.942,126.672,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1970:=[[84.942,126.672,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1980:=[[52.871,52.398,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1990:=[[52.871,52.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2000:=[[49.871,52.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2010:=[[49.871,54.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2020:=[[46.871,54.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2030:=[[46.871,56.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2040:=[[43.871,56.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2050:=[[43.871,62.749,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2060:=[[39.371,70.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2070:=[[38.371,70.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2080:=[[39.359,77.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2090:=[[38.371,77.395,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2100:=[[21.371,76.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2110:=[[15.871,72.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2120:=[[15.871,70.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2130:=[[10.371,70.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2140:=[[10.371,68.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2150:=[[9.371,68.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2160:=[[9.371,67.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2170:=[[8.371,67.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2180:=[[8.371,92.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2190:=[[9.371,92.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2200:=[[9.371,90.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2210:=[[10.371,90.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2220:=[[10.371,89.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2230:=[[15.871,89.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2240:=[[15.871,86.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2250:=[[21.371,82.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2260:=[[38.371,81.9,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2270:=[[39.359,81.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2280:=[[38.371,88.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2290:=[[39.371,88.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2300:=[[43.871,96.546,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2310:=[[43.871,103.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2320:=[[46.871,103.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2330:=[[46.871,104.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2340:=[[49.871,104.648,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2350:=[[49.871,106.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2360:=[[52.871,106.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2370:=[[52.871,96.246,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2380:=[[56.871,88.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2390:=[[56.871,70.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2400:=[[52.871,63.049,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2410:=[[52.871,52.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2420:=[[52.871,52.398,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2430:=[[52.371,70.398,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2440:=[[52.371,70.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2450:=[[52.371,70.398,5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2460:=[[43.871,70.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2470:=[[48.121,66.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2480:=[[48.121,66.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2490:=[[52.371,70.398,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2500:=[[52.371,70.398,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2510:=[[52.371,88.898,-5],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2520:=[[52.371,88.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2530:=[[43.871,88.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2540:=[[48.121,93.148,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2550:=[[52.371,88.898,0],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2560:=[[52.371,88.898,-15],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2570:=[[62.942,79.401,0],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget MANTENIMIENTO:=[[-7,-220.6,-606.5],[0.836516304,0.129409523,-0.482962913,0.224143868],[-1,-1,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2580:=[[-57,79.4,-356.5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2590:=[[-57,79.4,-356.5],[0.987688341,0.156434465,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2600:=[[-57,79.4,-356.5],[0.951056516,0.309016994,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2610:=[[-57,79.4,-356.5],[0.891006524,0.4539905,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2620:=[[-57,79.4,-356.5],[0.809016994,0.587785252,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2630:=[[-57,79.4,-356.5],[0.707106781,0.707106781,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2640:=[[-57,79.4,-356.5],[0.809016994,0.587785252,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2650:=[[-57,79.4,-356.5],[0.891006524,0.4539905,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2660:=[[-57,79.4,-356.5],[0.951056516,0.309016994,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2670:=[[-57,79.4,-356.5],[0.987688341,0.156434465,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_2670_2:=[[-57,79.4,-356.5],[1,0,0,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_home:=[[617.685929504,-1,570.260549615],[0.258819045,0,0.965925826,0],[-1,0,-1,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_880_2:=[[119.278,125.066,-10],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget Target_1970_2:=[[84.942,126.672,-15],[0.991444861,0,-0.130526192,0],[-1,-1,0,1],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PROC Path_10()
        MoveJ Target_10,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_20,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_30,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_40,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_50,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_60,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_70,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_80,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_90,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_100,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_110,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_120,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_130,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_140,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_150,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_160,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_170,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_180,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_190,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_200,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_210,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_220,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_230,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_240,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_250,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_260,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_270,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_280,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_290,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_300,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_310,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_320,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_330,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_340,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_350,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_360,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_370,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_380,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_390,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_400,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_410,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_420,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_430,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_440,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_450,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_460,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_470,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_480,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_490,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_500,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_510,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_520,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_530,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_540,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_550,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_560,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_570,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_580,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_590,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_600,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_610,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_620,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_630,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_640,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_650,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_660,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_670,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_680,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_690,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_700,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_710,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_720,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_730,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_740,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_750,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_760,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_770,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_780,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_790,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_800,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_810,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_820,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_830,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_840,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_850,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_860,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_870,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_880,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_880_2,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveJ Target_890,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_900,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_910,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_920,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_930,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_940,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_950,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_960,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_970,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_980,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_990,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1000,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1010,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1020,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1030,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1040,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1050,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1060,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1070,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1080,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1090,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1100,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1110,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1120,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1130,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1140,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1150,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1160,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1170,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1180,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1190,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1200,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1210,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1220,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1230,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1240,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1250,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1260,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1270,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1280,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1290,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1300,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1310,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1320,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1330,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1340,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1350,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1360,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1370,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1380,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1390,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1400,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1410,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1420,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1430,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1440,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1450,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1460,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1470,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1480,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1490,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1500,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1510,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1520,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1530,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1540,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1550,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1560,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1570,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1580,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1590,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1600,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1610,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1620,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1630,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1640,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1650,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1660,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1670,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1680,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1690,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1700,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1710,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1720,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1730,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1740,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1750,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1760,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1770,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1780,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1790,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1800,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1810,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1820,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1830,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1840,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1850,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1860,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1870,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1880,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1890,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1900,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1910,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1920,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1930,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1940,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1950,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1960,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1970,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveJ Target_1970_2,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveJ Target_1980,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_1990,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2000,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2010,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2020,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2030,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2040,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2050,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2060,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2070,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2080,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2090,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2100,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2110,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2120,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2130,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2140,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2150,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2160,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2170,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2180,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2190,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2200,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2210,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2220,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2230,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2240,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2250,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2260,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2270,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2280,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2290,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2300,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2310,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2320,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2330,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2340,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2350,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2360,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2370,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2380,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2390,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2400,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2410,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2420,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2430,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2440,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2450,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2460,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2470,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2480,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2490,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2500,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2510,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2520,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2530,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2540,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2550,v100,z5,marcador\WObj:=Workobject_pastel;
        MoveL Target_2560,v100,z5,marcador\WObj:=Workobject_pastel;
        

    ENDPROC
    PROC main()
        WHILE TRUE DO
            Path_20;
            
            IF DI_01 = 1 THEN  
                SET DO_01;
                SET FWD_Conveyor;
                WaitTime 3.8;
                RESET FWD_Conveyor;
                Path_10;
                Path_20;
                SET FWD_Conveyor;
                WaitTime 5;
                RESET FWD_Conveyor;
                RESET DO_01;
            ENDIF
            IF DI_02 = 1 THEN
                SET DO_02;
                Path_40;
                WaitTime 2;
                WHILE DI_02=0 DO
                    WaitTime 0.5;
                ENDWHILE
                Path_20;
                RESET DO_02;
            ENDIF
            
            IF DI_03 = 1 THEN
                SET DO_03;
                FarmearAura;
                Path_20;
                RESET DO_03;
            ENDIF
            
        ENDWHILE 
    ENDPROC
    PROC Path_20()
        MoveJ Target_home,v100,z5,marcador\WObj:=wobj0;
    ENDPROC
    PROC Path_40()
        MoveJ MANTENIMIENTO,v100,z5,marcador\WObj:=Workobject_pastel;
    ENDPROC
    PROC FarmearAura()
        Path_50;
    ENDPROC
    PROC Path_30()
    ENDPROC
    PROC Path_50()
        Movej Target_2580,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2590,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2600,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2610,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2620,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2630,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2640,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2650,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2660,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2670,v100,z5,marcador\WObj:=Workobject_pastel;
        Movej Target_2670_2,v100,z5,marcador\WObj:=Workobject_pastel;
    ENDPROC
ENDMODULE
