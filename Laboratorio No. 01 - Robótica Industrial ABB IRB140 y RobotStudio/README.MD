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
En esta etapa era fundamental tener en cuenta 2 elementos en particular para favorecer la resistencia de la herramienta ante los golpes, el primero fueron los **redondeos** en cada uno de los bordes entre las geometrias, y el segundo y más importante era un margen de tolerancia en la dirección normal brindada por la implementación de un **resorte**.

### Modelo CAD

<div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 40px;">
  <!-- Columna 1 -->
  <div style="text-align: center; width: 40%;">
    <img src="Imagenes/AgarreSeccion.png" style="width: 100%;" />
    <p><b>Figura 1:</b> Vista en sección</p>
  </div>
  
  <!-- Columna 2 -->
  <div style="text-align: center; width: 50%;">
    <img src="Imagenes/AgarreRender.png" style="width: 100%;" />
    <p><b>Figura 2:</b> Render 3D</p>
  </div>
</div>

Adicionalmente se exploró un estilo distinto de agarre para la tapa trasera, y dejaba en el lugar correcto todo el mecanismo sin la posibilidad de salirse debido a vibraciones:

<p align="center">
  <img src="Imagenes/AnimacionTapa.gif" alt="Animación del sistema en Fusion" width="300"/>
</p>

---

## Diagrama de Flujo

Diagrama explicativo de la secuencia completa del sistema:

![Diagrama de Flujo](ruta/a/tu/imagen_diagrama.png)

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