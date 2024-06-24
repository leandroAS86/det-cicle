#!/usr/bin/env python3

import os
import time
import smbus2
import logging
from ina219 import INA219,DeviceRangeError


# Define I2C bus
DEVICE_BUS = 1

# Define device i2c slave address.
DEVICE_ADDR = 0x17

# Set the threshold of UPS automatic power-off to prevent damage caused by battery over-discharge, unit: mV.
PROTECT_VOLT = 3700  

# Set the sample period, Unit: min default: 2 min.
SAMPLE_TIME = 2

class Ups():
    
    def __init__(self):
        # Instance INA219 and getting information from it.
        self.ina_supply = INA219(0.00725, busnum=DEVICE_BUS, address=0x40)
        self.ina_supply.configure()
        
        self.ina_batt = INA219(0.005, busnum=DEVICE_BUS, address=0x45)
        self.ina_batt.configure()
        
        # Raspberry Pi Communicates with MCU via i2c protocol.
        self.bus = smbus2.SMBus(DEVICE_BUS)

    def get_raspberry_info(self):    
        supply_voltage = self.ina_supply.voltage()
        supply_current = self.ina_supply.current()
        supply_power = self.ina_supply.power()
        
        return supply_voltage, supply_current, supply_power

    def print_raspberry_info(self):
        
        supply_voltage, supply_current, supply_power = self.get_raspberry_info()
        
        print("-"*60)
        print("------Current information of the detected Raspberry Pi------")
        print("-"*60)
        print("Raspberry Pi Supply Voltage: %.3f V" % supply_voltage)
        print("Raspberry Pi Current Current Consumption: %.3f mA" % supply_current)
        print("Raspberry Pi Current Power Consumption: %.3f mW" % supply_power)
        print("-"*60)

    # Batteries information
    def get_batteries_info(self):
        batt_voltage = self.ina_batt.voltage()
        batt_current = self.ina_batt.current()
        batt_power = self.ina_batt.power()
        
        return batt_voltage, batt_current, batt_power

    def print_batteries_info(self):
        
        batt_voltage, batt_current, batt_power = self.get_batteries_info()
        
        print("-------------------Batteries information-------------------")
        print("-"*60)
        print("Voltage of Batteries: %.3f V" % batt_voltage)
        try:
            if batt_current > 0:
                print("Battery Current (Charging) Rate: %.3f mA"% batt_current)
                print("Current Battery Power Supplement: %.3f mW"% batt_power)
            else:
                print("Battery Current (Discharge) Rate: %.3f mA"% batt_current)
                print("Current Battery Power Consumption: %.3f mW"% batt_power)
                print("-"*60)
        except DeviceRangeError:
             print("-"*60)
             print('Battery power is too high.')


    def mcu(self):

        aReceiveBuf = []
        aReceiveBuf.append(0x00)
        
        batt_voltage, batt_current, batt_power = self.get_batteries_info()

        # Read register and add the data to the list: aReceiveBuf
        for i in range(1, 255):
            aReceiveBuf.append(self.bus.read_byte_data(DEVICE_ADDR, i))

        # Enable Back-to-AC fucntion.
        # Enable: write 1 to register 0x19 == 25
        # Disable: write 0 to register 0x19 == 25

        self.bus.write_byte_data(DEVICE_ADDR, 25, 1)

        # Reset Protect voltage
        self.bus.write_byte_data(DEVICE_ADDR, 17, PROTECT_VOLT & 0xFF)
        self.bus.write_byte_data(DEVICE_ADDR, 18, (PROTECT_VOLT >> 8)& 0xFF)
        
        print("Successfully set the protection voltage to: %d mV" % PROTECT_VOLT)

        if (aReceiveBuf[8] << 8 | aReceiveBuf[7]) > 4000:
            print('-'*60)
            print('Currently charging via Type C Port.')
        elif (aReceiveBuf[10] << 8 | aReceiveBuf[9])> 4000:
            print('-'*60)
            print('Currently charging via Micro USB Port.')
        else:
            print('-'*60)
            print('Currently not charging.')
        # Consider shutting down to save data or send notifications
            if ((batt_voltage * 1000) < (PROTECT_VOLT + 200)):
                print('-'*60)
                print('The battery is going to dead! Ready to shut down!')
        # It will cut off power when initialized shutdown sequence.
                self.bus.write_byte_data(DEVICE_ADDR, 24,240)
                os.system("sudo sync && sudo halt")
                while True:
                    time.sleep(10)
   