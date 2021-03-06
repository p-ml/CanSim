import tkinter as tk
import can

# Virtual CAN interface configuration
interface = 'socketcan'
channel = 'vcan0'

# Initialise bus
bus = can.Bus(interface=interface, channel=channel, bitrate=500000)

# Define each CAN arbitration ID
arbID = {'vehSpeed': 0x01,
         'batSoC': 0x02,
         'batHea': 0x03,
         'fuelR': 0x04,
         'trip': 0x05,
         'batVol': 0x06,
         'batTemp': 0x07,
         'charSta': 0x08}

# Frequency of application update
freq = 20  

# Main Tkinter window
win = tk.Tk()
win.title("CAN Sim")
winLabel = tk.Label(win, text="CAN Simulator", font="Arial 28 bold")
winLabel.pack(side=tk.TOP)
win.resizable(False, False)

# Initialise Tkinter variables
transmitState = tk.BooleanVar(value=False)

vehicleSpeed = tk.IntVar()
batterySoC = tk.IntVar()
batteryHealth = tk.IntVar()
fuelRange = tk.IntVar()
tripmeter = tk.IntVar()

batteryVol = tk.IntVar()
batteryTemp = tk.IntVar()

chargeState = tk.IntVar(value=0)


def start_transmit():
    """Start transmission of CAN frames when 'Start' button is clicked."""
    print("Transmitting...")
    transmitState.set(True)


def stop_transmit():
    """Stop transmission of CAN frames when 'Stop' button is clicked."""
    print("No longer transmitting.")
    transmitState.set(False)


def encode():
    """Encode Tkinter window variables into CAN frames."""
    vehicleSpeed_msg = can.Message(arbitration_id=arbID['vehSpeed'],
                                   data=[vehicleSpeed.get()],
                                   is_extended_id=False)
    batterySoC_msg = can.Message(arbitration_id=arbID['batSoC'],
                                 data=[batterySoC.get()],
                                 is_extended_id=False)
    batteryHealth_msg = can.Message(arbitration_id=arbID['batHea'],
                                    data=[batteryHealth.get()],
                                    is_extended_id=False)
    fuelRange_msg = can.Message(arbitration_id=arbID['fuelR'],
                                data=[fuelRange.get()],
                                is_extended_id=False)
    tripmeter_msg = can.Message(arbitration_id=arbID['trip'],
                                data=[tripmeter.get()],
                                is_extended_id=False)
    batteryVol_msg = can.Message(arbitration_id=arbID['batVol'],
                                 data=[batteryVol.get()],
                                 is_extended_id=False)
    batteryTemp_msg = can.Message(arbitration_id=arbID['batTemp'],
                                  data=[batteryTemp.get()],
                                  is_extended_id=False)
    chargeState_msg = can.Message(arbitration_id=arbID['charSta'],
                                  data=[chargeState.get()],
                                  is_extended_id=False)

    msg_list = [vehicleSpeed_msg, batterySoC_msg, batteryHealth_msg,
                fuelRange_msg, tripmeter_msg, batteryVol_msg, batteryTemp_msg,
                chargeState_msg]

    transmit(msg_list)

    win.after(int(1000/freq), encode)


def transmit(msg_list):
    """Transmit each of the CAN messages via pre-defined CAN interface."""
    if transmitState.get():
        for msg in msg_list:
            bus.send(msg)


class FunctionButtons:
    """TKinter function button template."""
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack(side=tk.BOTTOM)

        self.start = tk.Button(frame, text='Start', command=start_transmit)
        self.start.pack(side=tk.LEFT)

        self.start = tk.Button(frame, text='Stop', command=stop_transmit)
        self.start.pack(side=tk.LEFT)

        self.quitButton = tk.Button(frame, text='Quit', command=master.destroy)
        self.quitButton.pack(side=tk.LEFT)


class VehicleSliders:
    """TKinter template for sliders."""
    def __init__(self, master, desc, lowerlim, upperlim, variable):
        frame = tk.Frame(master, padx=10, pady=10)
        frame.pack(side=tk.TOP)

        self.slider = tk.Scale(frame, from_=lowerlim, to=upperlim,
                               orient=tk.HORIZONTAL, var=variable)
        self.slider.pack()
        self.sliderLabel = tk.Label(frame, text=desc)
        self.sliderLabel.pack()


class CheckButton:
    """Tkinter template for check buttons."""
    def __init__(self, master, desc, variable, value):
        self.checkButton = tk.Radiobutton(master, text=desc, var=variable,
                                          value=value)
        self.checkButton.pack(anchor=tk.W)


def main():
    # Vehicle Data Frame
    vdFrame = tk.Frame(win, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    vdLabel = tk.Label(vdFrame, text='Vehicle Data', font='Arial 18 bold')
    vdLabel.pack(side=tk.TOP)

    VehicleSliders(vdFrame, 'Vehicle Speed', 0, 100, vehicleSpeed)
    VehicleSliders(vdFrame, 'Battery State of Charge', 0, 100, batterySoC)
    VehicleSliders(vdFrame, 'Battery Health', 0, 100, batteryHealth)
    VehicleSliders(vdFrame, 'Range', 0, 100, fuelRange)
    VehicleSliders(vdFrame, 'Tripmeter', 0, 100, tripmeter)

    # Battery Data Frame
    batteryFrame = tk.Frame(win, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    batteryLabel = tk.Label(batteryFrame, text='Battery Data',
                            font='Arial 18 bold')
    batteryLabel.pack(side=tk.TOP)

    VehicleSliders(batteryFrame, 'Battery Voltage', 0, 100, batteryVol)
    VehicleSliders(batteryFrame, 'Battery Temperature', 0, 100, batteryTemp)

    # Charging Data Frame
    chargingFrame = tk.Frame(win, bd=2, relief=tk.RIDGE, padx=10, pady=10)
    chargingLabel = tk.Label(chargingFrame, text='Charging Data',
                             font='Arial 18 bold')
    chargingLabel.pack(side=tk.TOP)

    CheckButton(chargingFrame, 'Charging', variable=chargeState, value=1)
    CheckButton(chargingFrame, 'Not Charging', variable=chargeState, value=0)

    # Initialise buttons
    FunctionButtons(win)

    # Pack frames
    vdFrame.pack(side=tk.LEFT, padx=10, pady=10)
    batteryFrame.pack(side=tk.TOP, padx=10, pady=10)
    chargingFrame.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.CENTER)

    # Start main loop
    win.after(int(1000/freq), encode)
    win.mainloop()


if __name__ == '__main__':
    main()
