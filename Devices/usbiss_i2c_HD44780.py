"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""
""" GdH - Using inheritance of I2CDevice)                          """
""" Based on https://github.com/dhylands/python_lcd/blob/master/lcd/pyb_i2c_lcd.py """


from Devices import lcd_api
from usbiss import i2c as I2C
# import I2CDevice as I2CDevice 
import time

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

# Defines shifts or masks for the various LCD line attached to the PCF8574

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4


class I2cLcd(lcd_api.LcdApi, I2C.I2CDevice):
    """Implements a HD44780 character LCD connected via PCF8574 on I2C."""

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        # self.pcf8574 = I2CDevice.I2CDevice(self.i2c, self.i2c_addr)
        I2C.I2CDevice.__init__(self, self.i2c, self.i2c_addr)
        # pyb self.pcf8574.writeRaw8(0)
        # self.pcf8574.writeRaw8(0)
        self.writeRaw8(0)
        time.sleep(20/1000.0)   # Allow LCD time to powerup
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(5/1000.0)    # need to time.sleep at least 4.1 msec
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(1/1000.0)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(1/1000.0)
        # Put LCD into 4 bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep(1/1000.0)
        lcd_api.LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD.

        This particular function is only used during intiialization.
        """
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        # pyb self.i2c.send(byte | MASK_E, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte | MASK_E)
        self.writeRaw8(byte | MASK_E)
        # pyb self.i2c.send(byte, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte)
        self.writeRaw8(byte)

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        # pyb self.i2c.send(1 << SHIFT_BACKLIGHT, self.i2c_addr)
        # self.pcf8574.writeRaw8(1 << SHIFT_BACKLIGHT)
        self.writeRaw8(1 << SHIFT_BACKLIGHT)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        # pyb self.i2c.send(0, self.i2c_addr)
        # self.pcf8574.writeRaw8(0)
        self.writeRaw8(0)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.

        Data is latched on the falling edge of E.
        """
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        # pyb self.i2c.send(byte | MASK_E, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte | MASK_E)
        self.writeRaw8(byte | MASK_E)
        # pyb self.i2c.send(byte, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte)
        self.writeRaw8(byte)


        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        # pyb self.i2c.send(byte | MASK_E, self.i2c_addr, )
        # self.pcf8574.writeRaw8(byte | MASK_E)
        self.writeRaw8(byte | MASK_E)
        # pyb self.i2c.send(byte, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte)
        self.writeRaw8(byte)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case time.sleep of 4.1 msec
            time.sleep(5/1000.0)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        # pyb self.i2c.send(byte | MASK_E, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte | MASK_E)
        self.writeRaw8(byte | MASK_E)
        # pyb self.i2c.send(byte, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte)
        self.writeRaw8(byte)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        # pyb self.i2c.send(byte | MASK_E, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte | MASK_E)
        self.writeRaw8(byte | MASK_E)
        # pyb self.i2c.send(byte, self.i2c_addr)
        # self.pcf8574.writeRaw8(byte)
        self.writeRaw8(byte)
