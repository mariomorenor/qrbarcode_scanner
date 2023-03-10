from tkinter import *
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from pyzbar import pyzbar
from threading import Timer
import json
import odoo
from datetime import datetime, timedelta
from playsound import playsound


class MainApp:

    window_width = 1000
    window_height = 700
    barcode_info = None
    users = []

    def __init__(self) -> None:

        self.get_users()

        self.main_window = Tk()
        self.main_window.bind('<Escape>', lambda e: self.main_window.quit())
        self.set_initial_settings()
        self.set_styles()
        self.GUI()
        self.main_window.mainloop()

    def get_users(self):
        print("ss")
        self.users = odoo.get_users()

    def GUI(self):

        main_panel = Frame(self.main_window)
        main_panel.pack(fill="both")

        # Camera Widget
        self.image_widget = Label(main_panel)
        self.image_widget.grid(row=0, column=0)

        self.panel_data = LabelFrame(
            main_panel, text="INFORMACIÓN", font=('Arial', 35, 'bold'))
        self.panel_data.grid(row=0, column=1,  sticky=N,  pady=10)

        Label(self.panel_data, text="Lugar:", font=(
            'Arial', 25, 'bold'),).grid(row=0, column=0, sticky=E)
        self.input_lab = ttk.Entry(
            self.panel_data, font=('Arial', 20, 'normal'))
        self.input_lab.grid(row=0, column=1, sticky=EW)
        self.input_lab.insert(0, "LABORATORIO 1")
        Label(self.panel_data, text="Nombre:", font=(
            'Arial', 25, 'bold'),).grid(row=1, column=0, sticky=E)
        self.input_student_name = ttk.Entry(
            self.panel_data, width=45, font=('Arial', 20, 'normal'))
        self.input_student_name.grid(row=1, column=1, sticky=EW)

        Label(self.panel_data, text="Cédula:", font=(
            'Arial', 25, 'bold'),).grid(row=2, column=0, sticky=E)
        self.input_student_dni = ttk.Entry(
            self.panel_data, width=45, font=('Arial', 20, 'normal'))
        self.input_student_dni.grid(row=2, column=1, sticky=EW)

        Label(self.panel_data, text="Correo:", font=(
            'Arial', 25, 'bold'),).grid(row=3, column=0, sticky=E)
        self.input_student_email = ttk.Entry(
            self.panel_data, width=45, font=('Arial', 20, 'normal'))
        self.input_student_email.grid(row=3, column=1, sticky=EW)

        Label(self.panel_data, text="Carrera:", font=(
            'Arial', 25, 'bold'),).grid(row=4, column=0, sticky=E)
        self.input_student_career = ttk.Entry(
            self.panel_data, width=45, font=('Arial', 20, 'normal'))
        self.input_student_career.grid(row=4, column=1, sticky=EW)

        # SUCCESSFULL MESSAGE
        Label(self.panel_data, text="INFO:", font=(
            'Arial', 25, 'bold'),).grid(row=5, column=0, sticky=E)
        self.input_message_info = ttk.Entry(
            self.panel_data, width=45, font=('Arial', 20, 'normal'))
        self.input_message_info.grid(row=5, column=1, sticky=EW, pady=50)

        ttk.Button(self.panel_data, text="ACTUALIZAR", style="update.TButton",
                   command=lambda: self.get_users()).grid(row=6, column=0, ipadx=15, ipady=10, sticky=EW)

        panel = Frame(self.main_window)
        panel.pack(pady=10)

        cont_lab = 0
        for i in range(3):
            for j in range(3):

                ttk.Button(panel, style="labs.TButton", text=f"LABORATORIO {cont_lab+1}", command=lambda id=cont_lab: self.set_site(f"LABORATORIO {id+1}")).grid(
                    row=i, column=j, padx=20, pady=8, ipadx=50, ipady=35)
                cont_lab = cont_lab + 1
                if cont_lab >= 7:
                    break
        self.connect_cam()

    def connect_cam(self):
        self.cap = cv2.VideoCapture(0)
        self.open_camera()

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            if not self.barcode_info or self.barcode_info != barcode.data.decode('utf-8'):
                self.barcode_info = barcode.data.decode('utf-8')
                qr = True if 'usuario_id' in self.barcode_info else False
                self.register(self.barcode_info, qr=qr)

        return frame

    def register(self, info, qr=False):
        self.reset_gui()
        if qr:
            info = info.replace("\'", "\"")
            info = json.loads(info)
            dni = info['usuario_id']
            self.input_lab.delete(0,END)
            self.input_lab.insert(0,info['laboratorio'])
        else:
            dni = info[2:12]

        for user in self.users:
            if dni == user['id'] or dni == user['cedula']:
                o = Timer(0.1, lambda: odoo.register_user({
                    'fecha': (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
                    'usuario_id': user['id'],
                    'laboratorio': info['laboratorio'] if qr else self.input_lab.get()
                }))
                o.start()
                self.show_info(user)
                break

        t = Timer(self.time_to_reset_gui, self.reset_barcode_info)
        t.start()

    def reset_barcode_info(self):
        self.barcode_info = None

    def show_info(self, data):
        self.reset_gui()

        self.input_student_name.insert(
            0, f"{data['nombres']} {data['apellidos']}")
        self.input_student_dni.insert(0, data['cedula'])
        self.input_student_email.insert(0, data['email'])
        self.input_student_career.insert(0, data['carrera'])
        self.input_message_info.insert(0, "REGISTRO EXITOSO!")
        t = Timer(0.1, lambda: playsound("c:\\qr\\success.mp3"))
        t.start()

    def reset_gui(self):

        self.input_student_name.delete(0, END)
        self.input_student_dni.delete(0, END)
        self.input_student_email.delete(0, END)
        self.input_student_career.delete(0, END)
        self.input_message_info.delete(0, END)

    def open_camera(self):

        # Capture the video frame by frame
        _, frame = self.cap.read()

        frame = self.read_barcodes(frame)

        # Convert image from one color space to other
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photoimage in the label
        self.image_widget.photo_image = photo_image

        # Configure image in the label
        self.image_widget.configure(image=photo_image)

        # Repeat the same process after every 10 seconds
        self.image_widget.after(10, self.open_camera)

    def set_initial_settings(self):
        # Título de la ventana principal
        self.main_window.title("Registro de Asistencia")
        # *****FULL SCREEN****
        self.main_window.overrideredirect(True)
        self.window_width = self.main_window.winfo_screenwidth()
        self.window_height = self.main_window.winfo_screenheight()
        # Establecer la dimensión de la ventana
        self.main_window.geometry(
            f"{self.window_width}x{self.window_height}+0+0")

        # Establecer Tiempo para limpieza de pantalla
        self.time_to_reset_gui = 5

        # Estilos
        self.styles = ttk.Style()

    def set_styles(self):
        # Labs Buttons
        self.styles.configure("labs.TButton", font=(None, 20))
        self.styles.configure("update.TButton", font=(None, 15))

    def set_site(self, site):
        self.reset_gui()
        self.input_lab.delete(0, END)
        self.input_lab.insert(0, site)


MainApp()
