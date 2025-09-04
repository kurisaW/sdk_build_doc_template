# Basic Example Project

This is a basic example project that demonstrates the fundamental usage of the SDK.

## Features

* LED blinking control
* Button interrupt handling
* Basic timer usage

## Quick Start

### Hardware Requirements

* One development board
* USB cable
* Debugger (optional)

### Build Steps

1. Open the project files
2. Configure the build options
3. Compile the project
4. Download to the development board

### Running Result

After the program runs, the LED will blink at the configured frequency, and pressing the button will trigger an interrupt handler.

## Code Structure

```
basic_example/
├── src/
│   ├── main.c          # Main program
│   ├── led.c           # LED control
│   └── key.c           # Button handling
├── inc/
│   ├── led.h
│   └── key.h
└── README.md
```

## Notes

* Ensure hardware connections are correct
* Check that the power supply voltage is normal
* Monitor the serial output information

## Troubleshooting

If issues occur, please check:

1. Hardware connections
2. Power supply
3. Program configuration
4. Build options