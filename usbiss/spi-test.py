from spi import SPI

# t=SPI('COM3', spi_mode = 1, freq = 25000)
# TypeError: __init__() got an unexpected keyword argument 'spi_mode'
t=SPI('COM3', 1, 25000)
print(t.__repr__)