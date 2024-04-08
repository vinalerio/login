import cv2
from tkinter import *
from PIL import Image, ImageTk

def capture_photo():
    # Capturar un frame
    ret, frame = cap.read()
    if ret:
        # Guardar el frame como una imagen
        cv2.imwrite('foto_capturada.jpg', frame)
        # Convertir la imagen capturada a formato RGB
        image = Image.open('foto_capturada.jpg')
        # Redimensionar la imagen si es necesario
        image = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        # Mostrar la imagen capturada
        label.config(image=photo)
        label.image = photo # Mantener una referencia a la imagen
        # Mostrar un mensaje indicando que la foto ha sido capturada
        Label(root, text="Foto capturada!").pack()

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convertir el frame de BGR a RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convertir el frame a un objeto PhotoImage
        frame = Image.fromarray(frame)
        # Convertir el objeto PhotoImage a un objeto TkPhoto
        frame = ImageTk.PhotoImage(frame)
        # Actualizar el canvas con el nuevo frame
        canvas.create_image(0, 0, image=frame, anchor=NW)
        # Dibujar un rectángulo en el canvas
        canvas.create_rectangle(50, 50, 250, 250, outline="red")
        # Programar la siguiente actualización
        root.after(10, update_frame)

# Crear la ventana de Tkinter
root = Tk()
root.title("Captura de Rostro")

# Crear un canvas para mostrar el video
canvas = Canvas(root, width=300, height=300)
canvas.pack()

# Botón para capturar la foto
capture_button = Button(root, text="Capturar Foto", command=capture_photo)
capture_button.pack()

# Label para mostrar la foto capturada
label = Label(root)
label.pack()

# Iniciar la captura de video
cap = cv2.VideoCapture(0)

# Iniciar la actualización del frame
update_frame()

# Ejecutar el bucle principal de Tkinter
root.mainloop()