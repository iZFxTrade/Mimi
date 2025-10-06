# Mimi Firmware Blueprint

## System Architecture

- **MCU**: [Specify microcontroller, e.g., STM32F4]
- **Peripherals**: UART, SPI, I2C, GPIO, etc.
- **Bootloader**: [If any]
- **Firmware Features**:
  - Peripheral drivers
  - Communication protocols
  - Application logic

## Build System

- Uses `make` for building firmware
- Source code in `src/`
- Output binaries in `build/`

## Dependencies

- GCC toolchain for ARM (or target MCU)
- Make
- Optional: CMake, OpenOCD (for flashing/debugging)

## Directory Structure

- `src/` - Firmware source code
- `include/` - Header files
- `build/` - Output binaries
- `Makefile` - Build instructions
