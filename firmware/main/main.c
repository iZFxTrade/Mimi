#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"

void app_main(void)
{
    printf("Hello from MiMi ESP32-CYD firmware!\n");
    while (1) {
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}
