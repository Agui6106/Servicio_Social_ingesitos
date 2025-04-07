import serial
import time
import sys
import glob

# -- Encontrar los puertos seriales disponibles -- #
import serial.tools.list_ports

def find_ports() -> list[str]:
    ports = serial.tools.list_ports.comports()
    serial_ports = []
    for port in ports:
        serial_ports.append(port.device)
    return serial_ports

class SerialArduino:
    def __init__(self, port: str = None, baudrate: int = 9600, timeout: float = 1):
        """
        Inicializa la comunicación serial con el Arduino.
        :param port: Puerto serial (Ejemplo: 'COM3' en Windows, '/dev/ttyUSB0' en Linux). Si es None, intenta detectar automáticamente.
        :param baudrate: Velocidad de comunicación (por defecto 9600)
        :param timeout: Tiempo de espera para lectura en segundos
        """
        self.port = port 
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

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
    
    def get_command(self):
        if self.ser.in_waiting > 0:
            try:
                return self.ser.readline().decode().strip()
            except Exception as e:
                print(f"Error leyendo del puerto serial: {e}")
                return None
        return None  # No hay datos

    def close(self):
        """Cierra la conexión serial."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Conexión cerrada")

if __name__ == "__main__":    
    print("Puertos seriales disponibles:")
    ports = find_ports()
    
    for port in ports:
        print(port)
    arduino_port = ports[0]
        
    arduino = SerialArduino(port=ports[0], baudrate=115200)  # Ahora detecta automáticamente si no se da un puerto
    arduino.send_data("Hola Arduino")
    time.sleep(1)
    response = arduino.read_data()
    print(f"Respuesta: {response}")
    arduino.close()
    
    
