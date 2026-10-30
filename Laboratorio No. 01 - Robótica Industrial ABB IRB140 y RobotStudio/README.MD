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

Primero se tuvo que modelar la herramienta teniendo en cuenta las consideraciones más importantes mencionadas en [Diseño y modelo CAD de la herramienta](#diseño-y-modelo-cad-de-la-herramienta), posteriormente se tuvo que realizar la calibración de la herramienta, se realizó tanto la calibración manual como la calibración atomática, esto se especifica en más detalle en [Calibración de la herramienta](#calibracion).

Entonces se crea el **Objeto de trabajo**, en la vida real se hizo uso de una caja de audifonos lo suficientemente plana y rígida para que asegurara pero además debía calibrarse, para lo primero 
La torta es representada mediante una superficie plana  rectangular ubicada inicialmente sobre una banda transportadora

La banda transporta la torta hasta la estación de trabajo del robot. Una vez ubicada dentro de su espacio de
trabajo, la banda se detiene completamente y el robot realiza la decoración.

Finalizada la operación, el robot regresa a su posición HOME y la banda transportadora se pone nuevamente en movimiento para trasladar la torta decorada hasta el extremo final de la banda.

Posteriormente se 

Se realizó un path y puso problemas al llegar al punto 

---

## Plano de Planta

Ubicación y distribución espacial de los elementos utilizados:

<table border="0" align="center" style="border-collapse: collapse;">
  <tr>
    <td align="center" valign="middle" style="border: none; padding: 10px;">
      <img src="Imagenes/RepGrafiso.png" height="240" style="vertical-align: middle;" />
    </td>
    <td align="center" valign="middle" style="border: none; padding: 10px;">
      <img src="Imagenes/RepGrafTop.png" height="240" style="vertical-align: middle;" />
    </td>
  </tr>
</table>

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



![Diagrama de flujo del sistema](Imagenes/diagrama_flujo.png)

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
[Código Completo de RAPID](Modulo_RAPID_LAB1.mod)
