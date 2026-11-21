from robodk.robolink import *    # API para comunicarte con RoboDK
from robodk.robomath import *    # Funciones matemáticas
import math
from matplotlib.textpath import TextPath

#fp = FontProperties(family="Helvetica", style="italic")
Lijaman = TextPath((-60, -40), "LIJAMAN", size=30)
x_lij,y_lij = Lijaman.vertices.T

Samuel = TextPath((-60, -70), "SAMUEL", size=30)
x_sam,y_sam = Samuel.vertices.T

#path2 = TextPath((0, 0), r"$\frac{1}{2}$", size=12, usetex=True)

# Crear patch con el path
#patch = PathPatch(path2, ec="white", fc="black", lw=3)

#------------------------------------------------
# 1) Conexión a RoboDK e inicialización
#------------------------------------------------
RDK = Robolink()

# Elegir un robot (si hay varios, aparece un popup)
robot = RDK.ItemUserPick("Selecciona un robot", ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("No se ha seleccionado un robot válido.")

# Simulación: ejecutar desde RoboDK sin seleccionar "Ejecutar en robot".
# Comentar este mensaje al habilitar el bloque de ejecución física.
print("Modo simulación: sin conexión al robot físico.")

# Ejecución física: descomentar este bloque solo con la celda verificada.
# if not robot.Connect():
#     raise Exception("No se pudo conectar al robot. Verifica el modo remoto y la configuración.")
#
# Corrección posterior al laboratorio: ConnectedState devuelve (estado, mensaje).
# estado, mensaje = robot.ConnectedState()
# if estado != ROBOTCOM_READY:
#     raise Exception("El robot no está listo: " + mensaje)
#
# print("Robot conectado y listo para ejecución física.")

#------------------------------------------------
# 2) Cargar el Frame (ya existente) donde quieres dibujar
#    Ajusta el nombre si tu Frame se llama diferente
#------------------------------------------------
frame_name = "Frame_from_Target1"
frame = RDK.Item(frame_name, ITEM_TYPE_FRAME)
if not frame.Valid():
    raise Exception(f'No se encontró el Frame "{frame_name}" en la estación.')

# Asignamos este frame al robot
robot.setPoseFrame(frame)
# Solo simulación: comentar setPoseTool para ejecución física con el driver Motoman.
# En el controlador, configurar y seleccionar previamente el TCP correspondiente.
robot.setPoseTool(robot.PoseTool())

# Ajustes de velocidad y blending
robot.setSpeed(100)   # mm/s - Ajusta según necesites
robot.setRounding(5)  # blending (radio de curvatura)

#------------------------------------------------
# 3) Parámetros de la figura (rosa polar)
#------------------------------------------------
num_points = 200       # Cuántos puntos muestreamos (mayor = más suave)
A = 100               # Amplitud (300 mm = radio máximo)
# Figura: r=cos(cθ)sin(bθ)+d; d = 1.5,c = 2 recomendado
b = 5
c = 2
d = 1.5
offset = 300
z_surface = 0          # Z=0 en el plano del frame
z_safe = 50            # Altura segura para aproximarse y salir

#------------------------------------------------
# 4) Movimiento al centro en altura segura
#------------------------------------------------
Target_home = "Home"
T_H = RDK.Item(Target_home,ITEM_TYPE_TARGET)
robot.MoveJ(T_H)

robot.MoveJ(transl(0, 0, z_surface - z_safe))

# Bajamos a la "superficie" (Z=0)
robot.MoveL(transl(0, 0, z_surface))

#------------------------------------------------
# 5) Dibujar la rosa polar
#    r = A * sin(k*theta)
#    x = r*cos(theta), y = r*sin(theta)
#------------------------------------------------
# Recorremos theta de 0 a 2*pi (una vuelta completa)
full_turn = 2*math.pi

for i in range(num_points+1):
    # Fracción entre 0 y 1
    t = i / num_points
    # Ángulo actual
    theta = full_turn * t

    # Calculamos r
    r = A * (math.cos(c * theta)*math.sin(b * theta)+d)

    # Convertimos a coordenadas Cartesianas X, Y
    y = r * math.cos(theta)
    x = r * math.sin(theta)+ offset

    # Movemos linealmente (MoveL) en el plano del Frame
    robot.MoveJ(transl(x, y, z_surface))

for i in range(len(x_lij+1)):
    t = i/len(x_lij)
    robot.MoveL(transl(y_lij[i],x_lij[i], z_surface))
    
for i in range(len(x_sam+1)):
    t = i/len(x_sam)
    robot.MoveL(transl(y_sam[i],x_sam[i], z_surface))

# Al terminar, subimos de nuevo para no chocar
robot.MoveL(transl(x, y, z_surface - z_safe))
robot.MoveJ(T_H)
print(f"¡Figura (rosa polar) completada en el frame '{frame_name}'!")
