#!/bin/bash
set -e

ESP_IDF_DIR="/workspaces/Mimi/esp-idf"

echo "Updating package lists..."
sudo apt update

echo "Installing ESP-IDF dependencies..."
sudo apt install -y git wget flex bison gperf python3 python3-pip python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0

if [ ! -d "$ESP_IDF_DIR" ]; then
    echo "Cloning ESP-IDF..."
    git clone --recursive https://github.com/espressif/esp-idf.git "$ESP_IDF_DIR"
    cd "$ESP_IDF_DIR"
    ./install.sh esp32
fi

echo "To use ESP-IDF, run:"
echo "  source /workspaces/Mimi/esp-idf/export.sh"

echo "Build environment setup complete."
echo "Build environment setup complete."
