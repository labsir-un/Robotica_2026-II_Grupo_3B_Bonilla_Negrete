# Laboratorio No. 01 - Robótica Industrial - Trayectorias, Entradas y Salidas Digitales


<p align="center">
  <img src="Imagenes\Foto_Con_Resultado.jpeg" alt="Hola" width="400"/>
</p>

## Integrantes
- Samuel David Negrete Lancheros
- Emmanuel Bonilla Mitrotti

---

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


---

## Plano de Planta

Ubicación y distribución espacial de los elementos utilizados:
- Robot
- Banda transportadora
- Superficies de trabajo
- Demás elementos de la celda

![Plano de Planta](ruta/a/tu/imagen_plano.png)

---

## Diseño y Modelo CAD de la Herramienta

### Diseño Detallado
[Explicación de la geometría, dimensiones y características del diseño de la herramienta.]

### Modelo CAD
![Modelo CAD Herramienta](ruta/a/tu/imagen_cad.png)

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

Descripción de las instrucciones y funciones clave del lenguaje RAPID empleadas en el código:
- `MoveL` / `MoveJ`: [Explicación del uso]
- `Set` / `Reset`: [Explicación del uso]
- `WaitDI`: [Explicación del uso]
- *(Agregar las demás funciones utilizadas)*

---

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
    ! Insertar aquí el código completo en RAPID utilizado durante la práctica
ENDMODULE
