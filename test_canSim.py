import unittest
import canSim
import can
import tkinter


class CanSimTest(unittest.TestCase):
    def test_types(self):
        """Test data types."""
        self.assertIsInstance(canSim.interface, str)
        self.assertIsInstance(canSim.channel, str)
        self.assertIsInstance(canSim.freq, int)
        self.assertIsInstance(canSim.bus, can.BusABC)
        self.assertIsInstance(canSim.arbID, dict)

        self.assertIsInstance(canSim.transmitState, tkinter.BooleanVar)
        self.assertIsInstance(canSim.vehicleSpeed, tkinter.IntVar)
        self.assertIsInstance(canSim.batterySoC, tkinter.IntVar)
        self.assertIsInstance(canSim.batteryHealth, tkinter.IntVar)
        self.assertIsInstance(canSim.fuelRange, tkinter.IntVar)
        self.assertIsInstance(canSim.tripmeter, tkinter.IntVar)
        self.assertIsInstance(canSim.batteryVol, tkinter.IntVar)
        self.assertIsInstance(canSim.batteryTemp, tkinter.IntVar)
        self.assertIsInstance(canSim.chargeState, tkinter.IntVar)

    def test_values(self):
        """Test initial values of variables."""
        self.assertEqual(canSim.interface, 'socketcan')
        self.assertEqual(canSim.channel, 'vcan0')
        self.assertEqual(canSim.freq, 20)

        self.assertEqual(canSim.transmitState.get(), False)
        self.assertEqual(canSim.chargeState.get(), 0)

        self.assertEqual(canSim.arbID['vehSpeed'], 0x01)
        self.assertEqual(canSim.arbID['batSoC'], 0x02)
        self.assertEqual(canSim.arbID['batHea'], 0x03)
        self.assertEqual(canSim.arbID['fuelR'], 0x04)
        self.assertEqual(canSim.arbID['trip'], 0x05)
        self.assertEqual(canSim.arbID['batVol'], 0x06)
        self.assertEqual(canSim.arbID['batTemp'], 0x07)
        self.assertEqual(canSim.arbID['charSta'], 0x08)

    def test_sizes(self):
        """Test variable lengths."""
        self.assertEqual(len(canSim.arbID), 8)

    def test_encode(self):
        """Test encode function to ensure CAN frames are constructed correctly."""
        self.assertIsInstance(canSim.encode(), list)
        self.assertEqual(len(canSim.encode()), 8)

        self.assertIsInstance(canSim.encode()[0], can.Message)
        self.assertIsInstance(canSim.encode()[1], can.Message)
        self.assertIsInstance(canSim.encode()[2], can.Message)
        self.assertIsInstance(canSim.encode()[3], can.Message)
        self.assertIsInstance(canSim.encode()[4], can.Message)
        self.assertIsInstance(canSim.encode()[5], can.Message)
        self.assertIsInstance(canSim.encode()[6], can.Message)
        self.assertIsInstance(canSim.encode()[7], can.Message)

        self.assertEqual(canSim.encode()[0].arbitration_id, 0x01)
        self.assertEqual(canSim.encode()[1].arbitration_id, 0x02)
        self.assertEqual(canSim.encode()[2].arbitration_id, 0x03)
        self.assertEqual(canSim.encode()[3].arbitration_id, 0x04)
        self.assertEqual(canSim.encode()[4].arbitration_id, 0x05)
        self.assertEqual(canSim.encode()[5].arbitration_id, 0x06)
        self.assertEqual(canSim.encode()[6].arbitration_id, 0x07)
        self.assertEqual(canSim.encode()[7].arbitration_id, 0x08)

        self.assertIsInstance(canSim.encode()[0].data, bytearray)
        self.assertIsInstance(canSim.encode()[1].data, bytearray)
        self.assertIsInstance(canSim.encode()[2].data, bytearray)
        self.assertIsInstance(canSim.encode()[3].data, bytearray)
        self.assertIsInstance(canSim.encode()[4].data, bytearray)
        self.assertIsInstance(canSim.encode()[5].data, bytearray)
        self.assertIsInstance(canSim.encode()[6].data, bytearray)
        self.assertIsInstance(canSim.encode()[7].data, bytearray)

        self.assertFalse(canSim.encode()[0].is_extended_id)
        self.assertFalse(canSim.encode()[1].is_extended_id)
        self.assertFalse(canSim.encode()[2].is_extended_id)
        self.assertFalse(canSim.encode()[3].is_extended_id)
        self.assertFalse(canSim.encode()[4].is_extended_id)
        self.assertFalse(canSim.encode()[5].is_extended_id)
        self.assertFalse(canSim.encode()[6].is_extended_id)
        self.assertFalse(canSim.encode()[7].is_extended_id)


if __name__ == '__main__':
    unittest.main()
