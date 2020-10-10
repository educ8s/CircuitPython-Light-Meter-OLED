import time
import board
import busio as io
import adafruit_ssd1306
from analogio import AnalogIn

def displayBar(previousVoltage, voltage):
    previousLength = voltageToPixel(previousVoltage)
    length = voltageToPixel(voltage)

    if(previousLength<length and previousLength>0):
        for x in range (40, 50):
            display.line(previousLength, x, length, x, 1)

    if(previousLength>length and previousLength>0):
        for x in range (40, 50):
            display.line(length, x, previousLength, x, 0)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

def voltageToPixel(voltage):
    pixelValue = round((128*voltage)/3.3)
    return pixelValue

def voltageToPercent(voltage):
    percent = round((100*voltage)/3.3,1)
    return str(percent) +" %"

i2c = io.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

previousVoltage = 0.02
voltage = 0.02
analog_in = AnalogIn(board.A10)
display.text("LIGHT INTENSITY", 15, 0, 1)

while True:
    previousVoltage = voltage
    voltage = round(get_voltage(analog_in),2)
    if(voltage != previousVoltage):
        display.text(voltageToPercent(previousVoltage), 42, 20, 0)
        display.text(voltageToPercent(voltage), 42, 20, 1)
        displayBar(previousVoltage, voltage)
        display.show()
    time.sleep(0.1)