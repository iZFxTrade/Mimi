# 🎀 MiMi – Smart Learning & Home Assistant

> **MiMi** is a **personalized AI assistant** running on the **ESP32-CYD (Cheap Yellow Display)**.
> MiMi is not just a **desktop AI speaker**, but also a **learning tutor, schedule secretary, home assistant**, and can be expanded into a **smart robot** with an ESP32-CAM.

---

## 🚀 Deployment Guide

### 1. Component Preparation

* ESP32-2432S028R (CYD) – mainboard.
* INMP441 (I2S mic).
* Integrated NS4168 speaker.
* SD Card (SPI).
* ESP32-CAM (robot option).
* Motor driver (TB6612FNG or PCA9685, if building a robot).
* Obstacle avoidance sensor, temperature/humidity sensor (optional).

### 2. Clone the Base Firmware

The MiMi project is a customization of [xiaozhi-esp32](https://github.com/78/xiaozhi-esp32):

```bash
git clone https://github.com/78/xiaozhi-esp32.git
cd xiaozhi-esp32
```

Then, customize the code to add a learning UI, schedule reminders, SD card data management, and smarthome integration.

### 3. INMP441 (I2S Mic) Wiring

| INMP441 Pin | ESP32 CYD GPIO |
| ----------- | -------------- |
| WS          | GPIO15         |
| SCK         | GPIO14         |
| SD          | GPIO32         |
| VCC         | 3.3V           |
| GND         | GND            |

### ESP32-CYD Pinout Diagram
```bash
// =================================================================
// GPIO PIN USAGE SUMMARY ON ESP32-CYD (ESP32-2432S028R)
// The board uses the ESP32-WROOM-32 module
// =================================================================

// --- PINS DEDICATED TO THE TFT DISPLAY (ILI9341) (SPI Communication) ---
#define TFT_MISO_PIN    GPIO_NUM_12   // Display Data (MISO)
#define TFT_MOSI_PIN    GPIO_NUM_13   // Display Data (MOSI)
#define TFT_SCK_PIN     GPIO_NUM_14   // Display Clock (SCK)
#define TFT_CS_PIN      GPIO_NUM_15   // Display Chip Select
#define TFT_DC_PIN      GPIO_NUM_2    // Display Data/Command
#define TFT_RST_PIN     -1            // Display Reset Pin (Usually hard-wired or not used)
#define TFT_BL_PIN      GPIO_NUM_21   // Display Backlight (PWM)

// --- PINS DEDICATED TO THE TOUCHSCREEN (XPT2046) (Shared SPI) ---
#define TOUCH_IRQ_PIN   GPIO_NUM_36   // Touch Interrupt (Input-only)
#define TOUCH_MOSI_PIN  GPIO_NUM_32   // Touch Data (MOSI)
#define TOUCH_MISO_PIN  GPIO_NUM_39   // Touch Data (MISO) (Input-only)
#define TOUCH_CLK_PIN   GPIO_NUM_25   // Touch Clock (CLK)
#define TOUCH_CS_PIN    GPIO_NUM_33   // Touch Chip Select

// --- PINS DEDICATED TO THE MICROSD CARD (VSPI Bus) ---
#define SD_MISO_PIN     GPIO_NUM_19   // SD Card Data (MISO)
#define SD_MOSI_PIN     GPIO_NUM_23   // SD Card Data (MOSI)
#define SD_SCK_PIN      GPIO_NUM_18   // SD Card Clock (SCK)
#define SD_CS_PIN       GPIO_NUM_5    // SD Card Chip Select

// --- PINS DEDICATED TO AUDIO/LED ---
#define SPEAKER_PIN     GPIO_NUM_26   // Speaker/Buzzer (Uses DAC or PWM channel)
#define LED_RED_PIN     GPIO_NUM_4    // RGB LED (Red Channel)
#define LED_GREEN_PIN   GPIO_NUM_16   // RGB LED (Green Channel)
#define LED_BLUE_PIN    GPIO_NUM_17   // RGB LED (Blue Channel)

// --- PINS USED FOR PROGRAMMING/SERIAL COMMUNICATION ---
#define UART_TX_PIN     GPIO_NUM_1    // Serial Communication (TX)
#define UART_RX_PIN     GPIO_NUM_3    // Serial Communication (RX)
#define BOOT_BUTTON_PIN GPIO_NUM_0    // BOOT Button (Should not be used)


// =================================================================
// DETAILS OF EXPANSION PORTS P3 AND CN1 (To identify available pins)
// =================================================================

// --- CONNECTOR P3 ---
// Pin 1: 3V3 (Power)
// Pin 2: GND (Ground)
// Pin 3: GPIO35 (AVAILABLE, INPUT-ONLY)
// Pin 4: GPIO22 (AVAILABLE, General Purpose)
// Pin 5: GPIO21 (Display Backlight BL)

// --- CONNECTOR CN1 ---
// Pin 1: GND (Ground)
// Pin 2: GPIO22 (AVAILABLE, General Purpose)
// Pin 3: GPIO27 (AVAILABLE, General Purpose)
// Pin 4: 3V3 (Power)


// =================================================================
// OPTIMAL AVAILABLE PINS FOR CONNECTING THE INMP441 MICROPHONE (I2S)
// (Using GPIO35, GPIO22, GPIO27)
// =================================================================

// I2S Clock (SCK): Synchronous clock pin
//   - Location: Connector CN1
#define I2S_SCK_PIN     GPIO_NUM_27   // OPTIMAL AVAILABLE PIN FOR I2S CLOCK

// I2S Word Select (WS) / L-R Clock: Channel select pin
//   - Location: Connector P3 or CN1
#define I2S_WS_PIN      GPIO_NUM_22   // OPTIMAL AVAILABLE PIN FOR I2S WORD SELECT

// I2S Serial Data (SD) / Data Input (DIN): Audio data
//   - Location: Connector P3. An ideal input pin on the ESP32.
#define I2S_SD_PIN      GPIO_NUM_35   // OPTIMAL AVAILABLE PIN FOR I2S DATA INPUT

// OTHER REQUIRED POWER PINS (Physical wiring):
// #define MIC_VCC         3V3           // Connect to 3V3 on P3/CN1
// #define MIC_GND         GND           // Connect to GND on P3/CN1
// #define MIC_L_R         GND           // Hard-wire to GND to select a channel
```

### 4. Build & Flash

* Use **ESP-IDF** or **Arduino IDE**.
* Select board: `ESP32 Dev Module`.
* Flash the customized firmware.

### 5. Prepare the SD Card

* Create the following directories on the SD card: `/learning/`, `/profiles/`, `/progress/`.
* Copy the sample JSON files (curriculum, timetable, lessons).

---

## ✨ Key Features

* 📚 **Learning Tutor**

  * Learn foreign languages, math, physics, etc., according to a curriculum.
  * Flashcards, quizzes, Q&A sessions.
  * Tests & grading after lessons.
  * Saves the learning progress of each user.

* 🗓️ **Schedule & Task Management**

  * Reminds you of lessons/homework based on `timetable.json`.
  * Users confirm with their voice or by tapping the screen.
  * For practice exercises → MiMi starts a timer and saves the completion time.

* 🎶 **Contextual Music**

  * Studying → Lo-fi focus music.
  * Sleeping → White noise/piano.
  * Exercising → Upbeat music.
  * Can play music from the SD card or send commands to Google Home (MQTT/HA).

* 🏠 **Smarthome**

  * Connects to MQTT/Home Assistant.
  * Control lights, fans, and other IoT devices with your voice.

* 👨‍👩‍👧‍👦 **Multi-user Personalization**

  * Separate profiles for each family member (father/mother/sister/brother).
  * Recognition via voice, camera (ESP32-CAM), or selection on the UI.
  * Parents can ask MiMi to report on their child's learning progress.

* 🤖 **Expandable Robot (ESP32-CAM)**

  * Patrols the house.
  * Sends video to the AI backend to recognize strangers.
  * MiMi displays an alert and plays a notification.
  * The CYD can be mounted on the robot to serve as an “expressive face”.

---

## 💾 SD Card Management

### 1. When the **SD card is not detected**

* A popup is displayed: *“⚠️ Please insert an SD card to use the full learning and data storage features.”*
* A similar voice announcement is made.
* Only runs in a minimalist mode: clock, weather, basic expressions, smarthome MQTT (if configured).

### 2. When the **SD card is inserted for the first time**

* Automatically creates the system directories:

  ```
  /profiles/
  /profiles/images/
  /progress/
  /learning/
  /music/
  /system/
  ```
* Generates default files:

  * `config.json` (WiFi, MQTT, AI backend).
  * `timetable.json` (empty).
  * `curriculum.json` (sample).
  * `lessons/` (contains a few demo lessons).

### 3. When the **SD card has old data**

* Reads the configuration files & data.
* If directories/files are missing → they are supplemented.
* If a file is corrupted → a default file is created and a notification is given: *“Some files were corrupted. MiMi has recreated the default files.”*

### 4. Data Storage

* **Learning progress**: `/profiles/<user>/progress/`.
* **Profile pictures**: `/profiles/images/<user>.jpg`.
* **Curriculum**: `/learning/curriculum.json`.
* **Music**: `/music/`.
* **System configuration**: `/system/config.json`.

👉 All data is loaded on demand to avoid consuming RAM.

---

## 📚 Data Structures

### 📖 curriculum.json

```json
{
  "program": "English Beginner",
  "levels": [
    {
      "id": "A1",
      "title": "Beginner",
      "lessons": [
        {"id": "travel", "title": "Travel Basics", "file": "lessons/travel.json"}
      ]
    }
  ]
}
```

### 📖 lesson.json

```json
{
  "lesson": "Physics - Temperature",
  "subject": "Physics",
  "objective": "Understand the concept of temperature and its units of measurement",
  "mode": "manual",
  "parts": [
    {
      "title": "Basic Concepts",
      "content": [
        {"concept": "Temperature", "explain": "The degree of hotness or coldness of an object."}
      ],
      "flashcards": [
        {"front": "Temperature", "back": "Nhiệt độ"}
      ],
      "questions": [
        {"type": "quiz", "q": "What is the SI unit of temperature?", "options": ["°C","K","°F"], "answer": "K"},
        {"type": "open", "q": "Explain the difference between °C and K."}
      ]
    }
  ]
}
```

👉 With `"mode": "ai_generated"`, you only need to enter the `lesson`, `subject`, and `objective`. The AI will generate the flashcards, quizzes, and open-ended questions.

### 🗓️ timetable.json

```json
{
  "2025-10-05": [
    {"time": "19:00", "activity": "English Lesson", "lesson": "Travel Basics", "mood": "focus", "music": "lofi.mp3"},
    {"time": "21:00", "activity": "Math Homework", "duration": 45, "type": "practice"}
  ]
}
```

### 📊 progress.json

```json
{
  "date": "2025-10-05",
  "lesson": "Math Homework - Algebra",
  "type": "practice",
  "start_time": "21:00",
  "end_time": "21:45",
  "duration_min": 45,
  "checked": true,
  "score": 9,
  "mistakes": [
    {"q": "Solve 2x+3=7", "error": "Incorrect on the first try, correct on the second"}
  ],
  "status": "completed"
}
```

---

## 🖼️ User Interface Design

### 1. **MiMi's Expressions** Page

* Displays MiMi's face (emoji-style): 😀 happy, 😐 neutral, 😴 sleepy, 😡 alert.
* Touch buttons: 🔊 toggle voice, ⚙️ go to Settings.

### 2. **Clock + Weather** Page

* Displays the time, date, and weather (icon + temperature).
* Buttons: 📅 open calendar, 🔄 refresh weather, 🎶 quick music play.

### 3. **Calendar + Timetable** Page

* Displays a monthly calendar + the day's schedule.
* Buttons: ➕ add event, ✏️ edit, ❌ delete.
* Reminder popup: ✅ Start | ⏰ Snooze | ❌ Dismiss.

### 4. **Learn + Practice** Page

* **Theory learning**: flashcards, quizzes, ▶️ play pronunciation, ✅ answer, 🔄 retry.
* **Practice**: timer, “Finished” button, a popup suggesting to double-check.

### 5. **Settings** Page

* Configuration: WiFi, MQTT, select AI backend, manage profiles, manage SD card.
* Buttons: 💾 save, 🔄 reset.

### 6. **Learning Report** Page

* Bar and pie charts (progress, scores).
* List of common mistakes.
* Buttons: 📤 export report, 🔍 select user.

### 7. **Music Player** Page

* Playlist from SD card + online, displays the currently playing song.
* Buttons: ⏮️ | ▶️ | ⏭️, 🔊 volume, 🎵 select playlist.

---

## 👨‍👩‍👧‍👦 Personalization

* Separate profiles for each family member: `/profiles/father/`, `/profiles/mother/`, `/profiles/sister/`, `/profiles/brother/`.
* Profiles contain their own learning schedules, timetables, and progress.
* Supports profile pictures in `/profiles/images/`.
* Parents can ask:

  * “MiMi, report on Nam's learning progress this week.”
  * “Did Lan finish her homework today?”

---



## 📈 Roadmap ToDo

### Phase 1 – Basics

* [ ] Configure hardware (LCD, Touch, Speaker, Mic, SD).
* [ ] WebUI for JSON uploads.
* [ ] Home UI + Reminder popup.
* [ ] Offline flashcards + quizzes.
* [ ] Save progress.

### Phase 2 – Intelligence

* [ ] Integrate AI backend (ASR/TTS, quiz generator).
* [ ] Multi-user personalization.
* [ ] Learning reports for parents.
* [ ] Review after learning or doing homework.
* [ ] Contextual music playback.
* [ ] Smarthome MQTT.

### Phase 3 – Robot Expansion

* [ ] ESP32-CAM for patrolling.
* [ ] Facial recognition, stranger alerts.
* [ ] Mount the CYD on the robot as an expressive face.

---

## 🔗 References & Customization

The MiMi project is based on [**xiaozhi-esp32**](https://github.com/78/xiaozhi-esp32) – an open-source firmware for the ESP32 that supports:

* 🎙️ ASR (Speech-to-Text)
* 🔊 TTS (Text-to-Speech)
* 🧑‍🤝‍🧑 Voiceprint Recognition
* 🌐 MQTT/WebSocket

👉 MiMi will customize this firmware by:

* Adding a **learning UI + schedule reminders** using LVGL.
* Managing SD card data (curriculum, timetable, progress).
* Personalizing for multiple users.
* Integrating smarthome MQTT.

---

## ✅ Conclusion

MiMi is a complete **AI learning & home assistant** project with the ability to:

* Provide structured learning assistance and smart reminders.
* Personalize for each family member.
* Manage learning progress and report back to parents.
* Combine Smarthome & Robot expansion.

MiMi is not just a hardware device, but **a virtual family member** – a tutor, a secretary, and a companion all in one.
