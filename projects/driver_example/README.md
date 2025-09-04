# Driver Example Project

This is a peripheral driver example project that demonstrates how to use various driver interfaces in the SDK.

## Features

* UART communication driver
* SPI interface usage
* I2C device access
* ADC data acquisition

## Quick Start

### Hardware Requirements

* One development board
* USB-to-serial module
* SPI/I2C peripheral modules
* Analog signal source

### Build Steps

1. Configure hardware interfaces
2. Modify driver parameters
3. Compile the project
4. Download and run

### Running Result

The program will initialize various peripheral drivers and output test results via the serial port.

## Code Structure

```
driver_example/
├── src/
│   ├── main.c          # Main program
│   ├── uart_drv.c      # UART driver
│   ├── spi_drv.c       # SPI driver
│   ├── i2c_drv.c       # I2C driver
│   └── adc_drv.c       # ADC driver
├── inc/
│   ├── uart_drv.h
│   ├── spi_drv.h
│   ├── i2c_drv.h
│   └── adc_drv.h
└── README.md
```

## Driver Interfaces

### UART Driver

```c
// Initialize UART
uart_init(115200);

// Send data
uart_send("Hello World\n");

// Receive data
char data = uart_receive();
```

### SPI Driver

```c
// Initialize SPI
spi_init(SPI_MODE0, 1000000);

// Send data
spi_send(0x55);

// Receive data
uint8_t data = spi_receive();
```

### I2C Driver

```c
// Initialize I2C
i2c_init(100000);

// Write data
i2c_write(0x50, 0x00, 0x55);

// Read data
uint8_t data = i2c_read(0x50, 0x00);
```

### ADC Driver

```c
// Initialize ADC
adc_init(ADC_CH0);

// Read data
uint16_t value = adc_read(ADC_CH0);
```

## Notes

* Check hardware connections
* Confirm driver parameters
* Observe serial output
* Verify data correctness

## Troubleshooting

Common issues and solutions:

1. **No serial output** – Check baud rate settings
2. **SPI communication failure** – Verify clock polarity and phase
3. **No response from I2C device** – Check address and timing
4. **Abnormal ADC data** – Verify reference voltage
