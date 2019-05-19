import unittest
import canRec
import can
import queue


class CanRecTest(unittest.TestCase):
    def test_types(self):
        """Test data types."""
        self.assertIsInstance(canRec.interface, str)
        self.assertIsInstance(canRec.channel, str)
        self.assertIsInstance(canRec.host, str)
        self.assertIsInstance(canRec.port, int)
        self.assertIsInstance(canRec.bus, can.BusABC)
        self.assertIsInstance(canRec.tcp_q, queue.Queue)
        self.assertIsInstance(canRec.serial_q, queue.LifoQueue)

    def test_values(self):
        """Test initial values of variables."""
        self.assertEqual(canRec.interface, 'socketcan')
        self.assertEqual(canRec.channel, 'vcan0')
        self.assertEqual(canRec.host, 'raspberrypi')
        self.assertEqual(canRec.port, 12345)

    def test_VehicleInformation(self):
        """Test VehicleInformation class."""
        vehicle = canRec.VehicleInformation()

        self.assertIsInstance(vehicle, canRec.VehicleInformation)
        self.assertEqual(vehicle.speed, 0)
        self.assertEqual(vehicle.batterySoC, 0)
        self.assertEqual(vehicle.batteryHealth, 0)
        self.assertEqual(vehicle.fuelRange, 0)
        self.assertEqual(vehicle.tripmeter, 0)
        self.assertEqual(vehicle.batteryVoltage, 0)
        self.assertEqual(vehicle.batteryTemperature, 0)
        self.assertEqual(vehicle.chargeState, 0)

        self.assertIsInstance(vehicle.speed, int)
        self.assertIsInstance(vehicle.batterySoC, int)
        self.assertIsInstance(vehicle.batteryHealth, int)
        self.assertIsInstance(vehicle.fuelRange, int)
        self.assertIsInstance(vehicle.tripmeter, int)
        self.assertIsInstance(vehicle.batteryVoltage, int)
        self.assertIsInstance(vehicle.batteryTemperature, int)
        self.assertIsInstance(vehicle.chargeState, int)

    def test_decode(self):
        """Test decode_CAN function."""
        vehicle = canRec.VehicleInformation()
        speed_msg = can.Message(arbitration_id=0x01, data=[80],
                                is_extended_id=False)
        soc_msg = can.Message(arbitration_id=0x02, data=[70],
                              is_extended_id=False)
        health_msg = can.Message(arbitration_id=0x03, data=[60],
                                 is_extended_id=False)
        fuel_msg = can.Message(arbitration_id=0x04, data=[50],
                               is_extended_id=False)
        trip_msg = can.Message(arbitration_id=0x05, data=[40],
                               is_extended_id=False)
        voltage_msg = can.Message(arbitration_id=0x06, data=[30],
                                  is_extended_id=False)
        temp_msg = can.Message(arbitration_id=0x07, data=[20],
                               is_extended_id=False)
        charge_msg = can.Message(arbitration_id=0x08, data=[10],
                                 is_extended_id=False)

        self.assertEqual(canRec.decode_CAN(vehicle,
                                           speed_msg).speed, 80)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           soc_msg).batterySoC, 70)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           health_msg).batteryHealth, 60)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           fuel_msg).fuelRange, 50)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           trip_msg).tripmeter, 40)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           voltage_msg).batteryVoltage, 30)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           temp_msg).batteryTemperature, 20)
        self.assertEqual(canRec.decode_CAN(vehicle,
                                           charge_msg).chargeState, 10)

    def test_encode(self):
        """Test encode function correctly converts vehicle data into
         the desired format."""
        vehicle = canRec.VehicleInformation()
        vehicle.speed = 10
        vehicle.batterySoC = 20
        vehicle.batteryHealth = 30
        vehicle.fuelRange = 40
        vehicle.tripmeter = 50
        vehicle.batteryVoltage = 60
        vehicle.batteryTemperature = 70
        vehicle.chargeState = 80

        self.assertIsInstance(canRec.encode(vehicle), str)
        self.assertEqual(canRec.encode(vehicle),
                         "01010:02020:03030:04040:05050:06060:07070:08080:")

    def test_tcp_q(self):
        """Test TCP queue works as intended."""
        canRec.tcp_q.put(10)
        self.assertEqual(canRec.tcp_q.get(), 10)

    def test_serial_q(self):
        """Test serial queue works as intended."""
        canRec.serial_q.put(20)
        self.assertEqual(canRec.serial_q(), 20)


if __name__ == '__main__':
    unittest.main()
