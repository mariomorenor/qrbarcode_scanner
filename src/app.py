from tkinter import *
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
from pyzbar import pyzbar
from threading import Timer


class MainApp:

    window_width = 1000
    window_height = 700
    barcode_info = None

    def __init__(self) -> None:

        self.main_window = Tk()
        self.main_window.bind('<Escape>', lambda e: self.main_window.quit())
        self.set_initial_settings()
        self.set_styles()
        self.GUI()
        self.main_window.mainloop()

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
        self.input_lab.insert(0,"LABORATORIO 1")
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
                self.register(self.barcode_info)

        return frame

    def register(self, info):
        
        print(info)

        self.input_message_info.delete(0,END)
        self.input_message_info.insert(0,"REGISTRO EXITOSO!")

        t = Timer(self.time_to_reset_gui, self.reset_gui)
        t.start()


    def reset_gui(self):
        self.barcode_info = None
        self.input_student_name.delete(0, END)
        self.input_student_dni.delete(0, END)
        self.input_student_email.delete(0, END)
        self.input_student_career.delete(0, END)
        self.input_message_info.delete(0,END)

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

    def set_site(self, site):
        self.input_lab.delete(0, END)
        self.input_lab.insert(0, site)
        self.input_message_info.delete(0,END)


MainApp()
