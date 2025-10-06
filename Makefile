TARGET = mimi-firmware
SRC_DIR = src
BUILD_DIR = firmware_builds

SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

CC = gcc
CFLAGS = -Iinclude -Wall -Werror

$(BUILD_DIR)/$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)/*.o $(BUILD_DIR)/$(TARGET).elf

.PHONY: all
all: $(BUILD_DIR)/$(TARGET).elf
