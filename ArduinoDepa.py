import sys
import serial
import threading
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "ArduinoDepa.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # --- Serial Arduino ---
        self.arduino = None
        self.serial_thread = None
        self.serial_running = False

        try:
            self.arduino = serial.Serial('COM2', 9600, timeout=1)  # Cambia COM3 por el tuyo
            self.serial_running = True
            self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.serial_thread.start()
        except Exception as e:
            self.msj(f"No se pudo abrir el puerto serial: {e}")

        if hasattr(self, 'servo0'):
            self.servo0.clicked.connect(lambda: self.send_command("SERVO_0"))

        # Signals para suma (tu ejemplo original)
        self.suma.clicked.connect(self.sumar)

    def sumar(self):
        try:
            a = float(self.num1.text())
            b = float(self.num2.text())
            r = a + b
            self.msj("La suma es: " + str(r))
            self.resultado.setText(str(r))
        except Exception as error:
            print(error)

    def msj(self, txt):
        m = QtWidgets.QMessageBox()
        m.setText(txt)
        m.exec_()

    def send_command(self, cmd):
        if self.arduino and self.arduino.is_open:
            self.arduino.write((cmd + '\n').encode('utf-8'))
        else:
            self.msj("Puerto serial no disponible.")

    def read_serial(self):
        while self.serial_running:
            try:
                if self.arduino.in_waiting > 0:
                    line = self.arduino.readline().decode('utf-8').strip()
                    if line:
                        QtCore.QMetaObject.invokeMethod(
                            self.Return, "append", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, line)
                        )
            except Exception as e:
                print("Error leyendo serial:", e)
                break

    def closeEvent(self, event):
        self.serial_running = False
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())