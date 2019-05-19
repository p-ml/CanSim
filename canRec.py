import can
import socket
import threading
import serial
import time
from queue import Queue, LifoQueue
from canSim import arbID

# CAN Interface data
interface = 'socketcan'
channel = 'vcan0'

# TCP client data
host = socket.gethostname()
port = 12345

# Initialise bus
bus = can.Bus(interface=interface, channel=channel, bitrate=500000)

# Initialise USB serial
usb_serial = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

# Initialise queues
tcp_q = Queue()
serial_q = LifoQueue()


# Initialise vehicle data variables
class VehicleInformation:
    """Local store for vehicle parameters."""
    def __init__(self):
        self.speed = 0
        self.batterySoC = 0
        self.batteryHealth = 0
        self.fuelRange = 0
        self.tripmeter = 0
        self.batteryVoltage = 0
        self.batteryTemperature = 0
        self.chargeState = 0


def decode_CAN(vehicle, msg):
    """Decode CAN messages using their arbitration ID, assign to
     VehicleInformation instance."""
    if msg.arbitration_id == arbID['vehSpeed']:
        vehicle.speed = int.from_bytes(msg.data, byteorder='little',
                                       signed=False)

    elif msg.arbitration_id == arbID['batSoC']:
        vehicle.batterySoC = int.from_bytes(msg.data, byteorder='little',
                                            signed=False)

    elif msg.arbitration_id == arbID['batHea']:
        vehicle.batteryHealth = int.from_bytes(msg.data, byteorder='little',
                                               signed=False)

    elif msg.arbitration_id == arbID['fuelR']:
        vehicle.fuelRange = int.from_bytes(msg.data, byteorder='little',
                                           signed=False)

    elif msg.arbitration_id == arbID['trip']:
        vehicle.tripmeter = int.from_bytes(msg.data, byteorder='little',
                                           signed=False)

    elif msg.arbitration_id == arbID['batVol']:
        vehicle.batteryVoltage = int.from_bytes(msg.data, byteorder='little',
                                                signed=False)

    elif msg.arbitration_id == arbID['batTemp']:
        vehicle.batteryTemperature = int.from_bytes(msg.data, byteorder='little',
                                                    signed=False)

    elif msg.arbitration_id == arbID['charSta']:
        vehicle.chargeState = int.from_bytes(msg.data, byteorder='little',
                                             signed=False)


def encode(vehicle):
    """Encode vehicle data before transmission via TCP or serial."""
    vehicleSpeed_ = "0{}{}".format(arbID['vehSpeed'],
                                   str(vehicle.speed).zfill(3))
    batterySoC_ = "0{}{}".format(arbID['batSoC'],
                                 str(vehicle.batterySoC).zfill(3))
    batteryHealth_ = "0{}{}".format(arbID['batHea'],
                                    str(vehicle.batteryHealth).zfill(3))
    fuelRange_ = "0{}{}".format(arbID['fuelR'],
                                str(vehicle.fuelRange).zfill(3))
    tripmeter_ = "0{}{}".format(arbID['trip'],
                                str(vehicle.tripmeter).zfill(3))

    batteryVol_ = "0{}{}".format(arbID['batVol'],
                                 str(vehicle.batteryVoltage).zfill(3))
    batteryTemp_ = "0{}{}".format(arbID['batTemp'],
                                  str(vehicle.batteryTemperature).zfill(3))

    chargeState_ = "0{}{}".format(arbID['charSta'],
                                  str(vehicle.chargeState).zfill(3))

    encodedMsg = ":".join([vehicleSpeed_, batterySoC_, batteryHealth_, fuelRange_,
                           tripmeter_, batteryVol_, batteryTemp_,
                           chargeState_]) + ":"

    return encodedMsg


def transmit_TCP(tcp_queue):
    """Get data from tcp_queue and send it via TCP to Driver GUI subsystem."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            s.send(str(tcp_queue.get()).encode('utf-8'))


def transmit_serial(serial_queue):
    """Get data from serial_queue and send it via USB serial
     to Telemetry subsystem."""

    # Initialise USB serial
    usb_serial = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
    time.sleep(2)

    while True:
        msg_serial = serial_queue.get().encode()
        usb_serial.write(msg_serial)
        time.sleep(0.1)


def main():
    # Instantiate vehicle class
    vehicle = VehicleInformation()

    # Initialise TCP thread
    tcpThread = threading.Thread(target=transmit_TCP, args=(tcp_q,),
                                 daemon=True)
    tcpThread.start()

    # Initialise serial thread
    serialThread = threading.Thread(target=transmit_serial, args=(serial_q,),
                                    daemon=True)
    serialThread.start()

    while True:
        # Receive message from virtual CAN bus
        msg = bus.recv()

        # Assign CAN messages to vehicle attributes
        decode_CAN(vehicle, msg)

        # Encode vehicle data for TCP & serial transmission
        msg = encode(vehicle)

        # Place encoded message into TCP queue
        tcp_q.put(msg)
        serial_q.put(msg)


if __name__ == '__main__':
    main()
