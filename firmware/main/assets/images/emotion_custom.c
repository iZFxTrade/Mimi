// emotion_custom.c
// MiMi Neon Face - Fullscreen Emotions (LVGL v8+)
// Author: you & ChatGPT
#include "lvgl.h"
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// =================== CONFIG ===================
#ifndef EMO_CANVAS_W
#define EMO_CANVAS_W 320
#endif

#ifndef EMO_CANVAS_H
#define EMO_CANVAS_H 240
#endif

// Màu neon & nền
#define EMO_BG_COLOR      lv_color_black()
#define EMO_NEON          lv_color_hex(0x44F5F5)
#define EMO_NEON_GLOW     lv_color_hex(0x22A5A5)
#define EMO_TEXT_COLOR    EMO_NEON

// Độ dày nét trong/ngoài (giả lập glow)
#define EMO_STROKE        4
#define EMO_GLOW_EXTRA    9   // halo

// Vị trí/ tỷ lệ bố cục gương mặt
#define FACE_RX           26      // corner radius khung mặt
#define EYE_R             26
#define EYE_OFFSET_X      64
#define EYE_Y             (EMO_CANVAS_H/2 - 6)
#define EYE_L_X           (EMO_CANVAS_W/2 - EYE_OFFSET_X)
#define EYE_R_X           (EMO_CANVAS_W/2 + EYE_OFFSET_X)
#define BROW_Y            (EYE_Y - 42)
#define MOUTH_Y           (EMO_CANVAS_H/2 + 38)
#define NOSE_X            (EMO_CANVAS_W/2)
#define NOSE_Y            (EMO_CANVAS_H/2 + 4)
#define HEAD_PAD_Y        (BROW_Y - 34)

// =================== EMOTION SET ===================
typedef enum {
  EMO_HAPPY = 0,
  EMO_SAD,
  EMO_SURPRISED,
  EMO_THINKING,     // có dấu ?
  EMO_SLEEPY,       // mắt nhắm + 'Z'
  EMO_LISTENING,    // sóng mic
  EMO_BATTERY_LOW,  // pin yếu
  EMO_DISCONNECTED, // wifi lỗi
  EMO_LOADING,      // ...
  EMO_EXCITED,      // thích thú (spark)
  EMO_BLISS,        // “đang phê” (mắt nhắm cong lên)
  EMO_TICKLE_LEFT,  // nhột: chạm mắt trái => mắt trái nhắm
  EMO_SNEEZE,       // hắt xì: chạm mũi
  EMO_HEAD_PATTED,  // sờ đầu => khoái chí
  EMO_NEUTRAL,
  EMO__COUNT
} mimi_emo_t;

// =================== STATE ===================
typedef struct {
  lv_obj_t   *cont;          // container của MiMi
  lv_obj_t   *canvas;        // canvas vẽ vector
  mimi_emo_t  current;
  lv_color_format_t cf;
  lv_color_t  neon, glow;
  lv_font_t  *font;          // dùng font mặc định
  // buffer canvas (ARGB8888 khuyến nghị cho glow mượt)
  void *buf;
  int   w, h;
} MimiFace;

static MimiFace g_mimi = {0};

// =================== INTERNAL DRAW HELPERS ===================
static void canvas_clear(MimiFace *f) {
  lv_canvas_fill_bg(f->canvas, EMO_BG_COLOR, LV_OPA_COVER);
}

// Vẽ nét có glow: vẽ halo to mờ + nét sáng
static void draw_glow_arc(MimiFace *f, lv_coord_t x, lv_coord_t y,
                          uint16_t r, int start, int end) {
  lv_draw_arc_dsc_t dsc;
  lv_draw_arc_dsc_init(&dsc);

  // halo
  dsc.color = f->glow;
  dsc.width = EMO_GLOW_EXTRA;
  dsc.opa   = LV_OPA_60;
  dsc.rounded = 1;
  lv_canvas_draw_arc(f->canvas, x, y, r, start, end, &dsc);

  // nét chính
  dsc.color = f->neon;
  dsc.width = EMO_STROKE;
  dsc.opa   = LV_OPA_COVER;
  lv_canvas_draw_arc(f->canvas, x, y, r, start, end, &dsc);
}

static void draw_glow_circle(MimiFace *f, lv_area_t a) {
  lv_draw_rect_dsc_t d;
  lv_draw_rect_dsc_init(&d);
  d.radius = LV_RADIUS_CIRCLE;

  // halo
  d.bg_color = f->glow; d.bg_opa = LV_OPA_40;
  lv_canvas_draw_rect(f->canvas, a.x1-5, a.y1-5, (a.x2-a.x1)+10, (a.y2-a.y1)+10, &d);

  // outline
  d.bg_opa = LV_OPA_TRANSP;
  d.border_color = f->neon;
  d.border_width = EMO_STROKE;
  d.border_opa = LV_OPA_COVER;
  lv_canvas_draw_rect(f->canvas, a.x1, a.y1, (a.x2-a.x1), (a.y2-a.y1), &d);
}

static void draw_glow_round_rect(MimiFace *f, lv_coord_t x, lv_coord_t y, lv_coord_t w, lv_coord_t h, lv_coord_t r) {
  lv_draw_rect_dsc_t d; lv_draw_rect_dsc_init(&d);
  // halo
  d.radius = r;
  d.bg_color = f->glow; d.bg_opa = LV_OPA_30;
  lv_canvas_draw_rect(f->canvas, x-4, y-4, w+8, h+8, &d);

  // border
  d.bg_opa = LV_OPA_TRANSP;
  d.border_color = f->neon;
  d.border_width = EMO_STROKE;
  d.border_opa = LV_OPA_COVER;
  lv_canvas_draw_rect(f->canvas, x, y, w, h, &d);
}

static void draw_text(MimiFace *f, const char *txt, lv_coord_t x, lv_coord_t y, int size_mul) {
  // dùng font mặc định; có thể thay bằng font custom nếu cần ký tự đặc biệt
  lv_draw_label_dsc_t d; lv_draw_label_dsc_init(&d);
  d.color = EMO_TEXT_COLOR;
  d.opa   = LV_OPA_90;
  // scale bằng transform (LVGL v9 có font transform; v8: dùng style text letter_space/line_space)
  d.letter_space = 1;
  lv_canvas_draw_text(f->canvas, x, y, EMO_CANVAS_W, &d, txt);
}

static void draw_eyelashes(MimiFace *f, int cx, int cy, bool left_side) {
  // 2–3 sợi lông mi cong nhẹ ở góc trên ngoài
  int dir = left_side ? -1 : 1;
  draw_glow_arc(f, cx + dir*18, cy - 16, 16, left_side? 200: -20, left_side? 240: 20);
  draw_glow_arc(f, cx + dir*24, cy - 10, 14, left_side? 200: -20, left_side? 235: 15);
}

static void draw_eye_open(MimiFace *f, int cx, int cy, bool with_lash, bool highlight) {
  // nhãn cầu
  draw_glow_arc(f, cx, cy, EYE_R, 0, 360);
  // highlight
  if (highlight) {
    lv_area_t a = { .x1=cx-6, .y1=cy-10, .x2=cx+2, .y2=cy-2 };
    draw_glow_circle(f, a);
  }
  if (with_lash) {
    draw_eyelashes(f, cx, cy, cx < EMO_CANVAS_W/2);
  }
}

static void draw_eye_closed(MimiFace *f, int cx, int cy, bool smile_curve) {
  // mắt nhắm: cung cong
  if (smile_curve) draw_glow_arc(f, cx, cy, EYE_R-2, 200, 340);
  else             draw_glow_arc(f, cx, cy, EYE_R-2, 180, 360);
}

static void draw_brows(MimiFace *f, int tilt) {
  // tilt: -30 buồn, +30 vui
  draw_glow_arc(f, EYE_L_X, BROW_Y, 24, 200-tilt, 340-tilt);
  draw_glow_arc(f, EYE_R_X, BROW_Y, 24, 200+tilt, 340+tilt);
}

static void draw_mouth_smile(MimiFace *f, int happy) {
  // happy: 0..40 (độ cười)
  draw_glow_arc(f, EMO_CANVAS_W/2, MOUTH_Y, 36, 200-happy, 340+happy);
}
static void draw_mouth_sad(MimiFace *f) {
  draw_glow_arc(f, EMO_CANVAS_W/2, MOUTH_Y+10, 36, 20, 160);
}
static void draw_mouth_O(MimiFace *f) {
  lv_area_t a = { .x1=EMO_CANVAS_W/2-10, .y1=MOUTH_Y-10, .x2=EMO_CANVAS_W/2+10, .y2=MOUTH_Y+10 };
  draw_glow_circle(f, a);
}

// Sóng mic nghe
static void draw_listen_waves(MimiFace *f) {
  draw_glow_arc(f, EMO_CANVAS_W/2, MOUTH_Y+22, 46, 210, 330);
  draw_glow_arc(f, EMO_CANVAS_W/2, MOUTH_Y+22, 56, 210, 330);
}

// Pin yếu (ô chữ nhật bo tròn + mức thấp)
static void draw_battery_low(MimiFace *f) {
  int w=42, h=18;
  draw_glow_round_rect(f, EMO_CANVAS_W/2 - w/2, BROW_Y-6, w, h, 6);
  // cực dương
  draw_glow_round_rect(f, EMO_CANVAS_W/2 + w/2 + 2, BROW_Y-6 + (h/3), 6, h/3, 3);
  // mức thấp
  lv_draw_rect_dsc_t d; lv_draw_rect_dsc_init(&d);
  d.bg_color = f->neon; d.bg_opa = LV_OPA_80; d.radius = 4;
  lv_canvas_draw_rect(f->canvas, EMO_CANVAS_W/2 - w/2 + 4, BROW_Y-6 + 4, 10, h-8, &d);
}

// WiFi lỗi
static void draw_wifi_lost(MimiFace *f) {
  draw_glow_arc(f, EMO_CANVAS_W/2, BROW_Y-4, 30, 210, 330);
  draw_glow_arc(f, EMO_CANVAS_W/2, BROW_Y-4, 20, 210, 330);
  draw_glow_arc(f, EMO_CANVAS_W/2, BROW_Y-4, 10, 210, 330);
  // gạch chéo
  lv_draw_line_dsc_t l; lv_draw_line_dsc_init(&l);
  l.color = f->neon; l.width = EMO_STROKE;
  lv_point_t p1 = {EMO_CANVAS_W/2-34, BROW_Y+12};
  lv_point_t p2 = {EMO_CANVAS_W/2+34, BROW_Y-18};
  lv_canvas_draw_line(f->canvas, &p1, &p2, &l);
}

// Spark cảm xúc
static void draw_spark(MimiFace *f, int cx, int cy, int r, int rays) {
  lv_draw_line_dsc_t l; lv_draw_line_dsc_init(&l);
  l.color = f->neon; l.width = EMO_STROKE;
  for (int i=0;i<rays;i++){
    float a = (LV_TRIGO_PI*2 * i)/rays;
    int x1 = cx + (r-6) * lv_trigo_sin(a) / LV_TRIGO_SIN_MAX;
    int y1 = cy + (r-6) * lv_trigo_cos(a) / LV_TRIGO_SIN_MAX;
    int x2 = cx + (r+10) * lv_trigo_sin(a) / LV_TRIGO_SIN_MAX;
    int y2 = cy + (r+10) * lv_trigo_cos(a) / LV_TRIGO_SIN_MAX;
    lv_point_t p1 = {x1,y1}, p2 = {x2,y2};
    lv_canvas_draw_line(f->canvas, &p1, &p2, &l);
  }
}

// Dấu ba chấm
static void draw_ellipsis(MimiFace *f) {
  for(int i=-1;i<=1;i++){
    lv_area_t a = {.x1=EMO_CANVAS_W/2 + i*14 - 3, .y1=MOUTH_Y-3, .x2=EMO_CANVAS_W/2 + i*14 + 3, .y2=MOUTH_Y+3};
    draw_glow_circle(f, a);
  }
}

// =================== RENDER EACH EMOTION ===================
static void draw_frame(MimiFace *f) {
  // khung mặt bo tròn
  draw_glow_round_rect(f, 22, 18, EMO_CANVAS_W-44, EMO_CANVAS_H-36, FACE_RX);
}

static void render_emotion(MimiFace *f, mimi_emo_t e) {
  canvas_clear(f);
  draw_frame(f);

  switch(e) {
    case EMO_NEUTRAL:
      draw_brows(f, 0);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, true);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, true);
      draw_mouth_smile(f, 4);
      break;

    case EMO_HAPPY:
      draw_brows(f, 18);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, true);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, true);
      draw_mouth_smile(f, 28);
      break;

    case EMO_SAD:
      draw_brows(f, -20);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, false);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, false);
      draw_mouth_sad(f);
      break;

    case EMO_SURPRISED:
      draw_brows(f, 0);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, false);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, false);
      draw_mouth_O(f);
      break;

    case EMO_THINKING:
      draw_brows(f, -5);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, true);
      draw_eye_closed(f, EYE_R_X, EYE_Y, false); // nhíu 1 mắt
      draw_mouth_smile(f, 6);
      draw_text(f, "?", EMO_CANVAS_W/2 + 56, BROW_Y+12, 1);
      break;

    case EMO_SLEEPY:
      draw_brows(f, -10);
      draw_eye_closed(f, EYE_L_X, EYE_Y, true);
      draw_eye_closed(f, EYE_R_X, EYE_Y, true);
      draw_mouth_O(f);
      draw_text(f, "Z", EMO_CANVAS_W - 26, HEAD_PAD_Y, 1);
      break;

    case EMO_LISTENING:
      draw_brows(f, 5);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, true);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, true);
      draw_mouth_smile(f, 10);
      draw_listen_waves(f);
      break;

    case EMO_BATTERY_LOW:
      draw_brows(f, -18);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, false);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, false);
      draw_mouth_sad(f);
      draw_battery_low(f);
      break;

    case EMO_DISCONNECTED:
      draw_brows(f, -6);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, false);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, false);
      draw_mouth_sad(f);
      draw_wifi_lost(f);
      break;

    case EMO_LOADING:
      draw_brows(f, 0);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, false);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, false);
      draw_ellipsis(f);
      break;

    case EMO_EXCITED:
      draw_brows(f, 24);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, true);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, true);
      draw_mouth_smile(f, 36);
      draw_spark(f, EMO_CANVAS_W/2, HEAD_PAD_Y+6, 12, 8);
      break;

    case EMO_BLISS: // “đang phê”
      draw_brows(f, 12);
      draw_eye_closed(f, EYE_L_X, EYE_Y, true);
      draw_eye_closed(f, EYE_R_X, EYE_Y, true);
      draw_mouth_smile(f, 30);
      break;

    case EMO_TICKLE_LEFT: // nhột mắt trái
      draw_brows(f, 10);
      draw_eye_closed(f, EYE_L_X, EYE_Y, true);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, true);
      draw_mouth_smile(f, 18);
      break;

    case EMO_SNEEZE:
      draw_brows(f, -8);
      draw_eye_closed(f, EYE_L_X, EYE_Y, false);
      draw_eye_closed(f, EYE_R_X, EYE_Y, false);
      // mũi: nổ nhỏ
      draw_mouth_O(f);
      draw_text(f, "*achoo*", NOSE_X-26, NOSE_Y-10, 1);
      break;

    case EMO_HEAD_PATTED:
      draw_brows(f, 26);
      draw_eye_open(f, EYE_L_X, EYE_Y, true, true);
      draw_eye_open(f, EYE_R_X, EYE_Y, true, true);
      draw_mouth_smile(f, 34);
      // vệt “pat” trên đầu
      draw_spark(f, EMO_CANVAS_W/2, HEAD_PAD_Y, 14, 6);
      break;

    default:
      break;
  }
}

// =================== PUBLIC API ===================
/*
 * Khởi tạo mặt MiMi: tạo container + canvas nền đen.
 * parent: màn hình hoặc obj chứa
 * w/h   : kích thước (mặc định 320x240)
 */
lv_obj_t* mimi_emotion_create(lv_obj_t *parent, int w, int h) {
  memset(&g_mimi, 0, sizeof(g_mimi));

  g_mimi.w = (w>0)? w : EMO_CANVAS_W;
  g_mimi.h = (h>0)? h : EMO_CANVAS_H;
  g_mimi.cf = LV_COLOR_FORMAT_ARGB8888; // glow đẹp hơn
  g_mimi.neon = EMO_NEON;
  g_mimi.glow = EMO_NEON_GLOW;
  g_mimi.font = LV_FONT_DEFAULT;

  g_mimi.cont = lv_obj_create(parent);
  lv_obj_set_size(g_mimi.cont, g_mimi.w, g_mimi.h);
  lv_obj_set_style_bg_color(g_mimi.cont, EMO_BG_COLOR, 0);
  lv_obj_set_style_bg_opa(g_mimi.cont, LV_OPA_COVER, 0);
  lv_obj_clear_flag(g_mimi.cont, LV_OBJ_FLAG_SCROLLABLE);

  // canvas
  size_t buf_sz = lv_color_format_get_size(g_mimi.cf) * g_mimi.w * g_mimi.h;
  g_mimi.buf = lv_mem_alloc(buf_sz);
  LV_ASSERT_MALLOC(g_mimi.buf);

  g_mimi.canvas = lv_canvas_create(g_mimi.cont);
  lv_canvas_set_buffer(g_mimi.canvas, g_mimi.buf, g_mimi.w, g_mimi.h, g_mimi.cf);
  lv_obj_center(g_mimi.canvas);

  // nền đen
  lv_canvas_fill_bg(g_mimi.canvas, EMO_BG_COLOR, LV_OPA_COVER);

  // render mặc định
  g_mimi.current = EMO_NEUTRAL;
  render_emotion(&g_mimi, g_mimi.current);
  return g_mimi.cont;
}

/*
 * Đổi biểu cảm
 */
void mimi_emotion_set(mimi_emo_t emo) {
  if (!g_mimi.canvas) return;
  g_mimi.current = emo;
  render_emotion(&g_mimi, emo);
}

/*
 * Event tiện dụng: gọi theo vùng chạm để tạo “nhột/ hắt xì/ sờ đầu”
 * x,y: toạ độ chạm (tương đối canvas), pressed: 1 khi down
 */
void mimi_touch_react(lv_coord_t x, lv_coord_t y, bool pressed) {
  if (!pressed) return;
  // gần mắt trái
  if (LV_ABS(x - EYE_L_X) < EYE_R && LV_ABS(y - EYE_Y) < EYE_R) {
    mimi_emotion_set(EMO_TICKLE_LEFT);
    return;
  }
  // mũi
  if (LV_ABS(x - NOSE_X) < 18 && LV_ABS(y - NOSE_Y) < 18) {
    mimi_emotion_set(EMO_SNEEZE);
    return;
  }
  // đầu
  if (y < HEAD_PAD_Y + 10) {
    mimi_emotion_set(EMO_HEAD_PATTED);
    return;
  }
  // còn lại: happy nhẹ
  mimi_emotion_set(EMO_HAPPY);
}

/*
 * Thu hồi bộ nhớ canvas (gọi khi xoá)
 */
void mimi_emotion_destroy(void) {
  if (g_mimi.buf) { lv_mem_free(g_mimi.buf); g_mimi.buf = NULL; }
  if (g_mimi.cont) { lv_obj_del_delayed(g_mimi.cont); g_mimi.cont = NULL; }
}

// =================== DEMO (tuỳ chọn) ===================
// Ví dụ sử dụng:
// lv_obj_t *root = lv_scr_act();
// mimi_emotion_create(root, 320, 240);
// mimi_emotion_set(EMO_LISTENING);
// // gán input:
// lv_obj_add_event_cb(g_mimi.canvas, [](lv_event_t *e){
//   lv_point_t p; lv_indev_t *indev = lv_indev_get_act();
//   if (indev && lv_indev_get_point(indev, &p) == LV_RES_OK) {
//     bool pressed = (lv_indev_get_state(indev) == LV_INDEV_STATE_PRESSED);
//     mimi_touch_react(p.x, p.y, pressed);
//   }
// }, LV_EVENT_PRESSING, NULL);
