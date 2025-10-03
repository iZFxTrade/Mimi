#ifndef EMOTION_CUSTOM_H
#define EMOTION_CUSTOM_H

#include "lvgl.h"
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Emotion enumeration
typedef enum {
  EMO_HAPPY = 0,
  EMO_SAD,
  EMO_SURPRISED,
  EMO_THINKING,
  EMO_SLEEPY,
  EMO_LISTENING,
  EMO_BATTERY_LOW,
  EMO_DISCONNECTED,
  EMO_LOADING,
  EMO_EXCITED,
  EMO_BLISS,
  EMO_TICKLE_LEFT,
  EMO_SNEEZE,
  EMO_HEAD_PATTED,
  EMO_NEUTRAL,
  EMO__COUNT
} mimi_emo_t;

// Public API
lv_obj_t* mimi_emotion_create(lv_obj_t *parent, int w, int h);
void mimi_emotion_set(mimi_emo_t emo);
void mimi_touch_react(lv_coord_t x, lv_coord_t y, bool pressed);
void mimi_emotion_destroy(void);

#ifdef __cplusplus
} /*extern "C"*/
#endif

#endif // EMOTION_CUSTOM_H
