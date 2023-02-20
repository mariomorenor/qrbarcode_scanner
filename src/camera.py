import cv2
from PIL import Image, ImageTk
from pyzbar import pyzbar



class Camera():

    def __init__(self, cam_widget) -> None:
        self.cam_widget = cam_widget
        self.cap = cv2.VideoCapture(0)

    def open(self):

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
        self.cam_widget.photo_image = photo_image

        # Configure image in the label
        self.cam_widget.configure(image=photo_image)

        # Repeat the same process after every 10 seconds
        self.cam_widget.after(10, self.open)
    
    def read_barcodes(self,frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            #1
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            #2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            
        return frame