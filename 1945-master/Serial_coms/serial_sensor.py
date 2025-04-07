import serial
import time
import sys
import glob

class SerialArduino:
    def __init__(self, port: str = None, baudrate: int = 9600, timeout: float = 1):
        """
        Inicializa la comunicación serial con el Arduino.
        :param port: Puerto serial (Ejemplo: 'COM3' en Windows, '/dev/ttyUSB0' en Linux). Si es None, intenta detectar automáticamente.
        :param baudrate: Velocidad de comunicación (por defecto 9600)
        :param timeout: Tiempo de espera para lectura en segundos
        """
        self.port = port or self.find_first_available_port()
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

    def find_first_available_port(self) -> str:
        """Busca y retorna el primer puerto serie disponible."""
        if sys.platform.startswith('win'):
            platform = 'win'
            ports = [f'COM{i}' for i in range(1, 256)]
        elif sys.platform.startswith('linux'):
            platform = 'linux'
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            platform = 'darwin'
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Plataforma no soportada')

        for port in ports:
            early_stop = True if platform == 'win' else False
            try:
                s = serial.Serial(port)
                s.close()
                print(f"Puerto encontrado: {port}")
                return port
            except (OSError, serial.SerialException):
                if early_stop:
                    break
                continue

        raise IOError("No se encontraron puertos seriales disponibles")

    def connect(self):
        """Intenta conectar con el puerto serie."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Espera a que Arduino se inicie
            print(f"Conectado a {self.port} a {self.baudrate} baudios")
        except serial.SerialException as e:
            print(f"Error al conectar con el puerto {self.port}: {e}")

    def send_data(self, data: str):
        """Envía datos al Arduino."""
        if self.ser and self.ser.is_open:
            self.ser.write(data.encode('utf-8'))
            print(f"Enviado: {data}")
        else:
            print("Error: Conexión serial no establecida")

    def read_data(self) -> str:
        """Lee datos del Arduino."""
        if self.ser and self.ser.is_open:
            response = self.ser.readline().decode('utf-8').strip()
            return response
        return ""

    def close(self):
        """Cierra la conexión serial."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    arduino = SerialArduino(baudrate=9600)  # Ahora detecta automáticamente si no se da un puerto
    arduino.send_data("Hola Arduino")
    time.sleep(1)
    response = arduino.read_data()
    print(f"Respuesta: {response}")
    arduino.close()
