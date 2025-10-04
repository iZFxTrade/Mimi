import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import opuslib
import struct
import numpy as np
import sounddevice as sd
import os


def play_p3_file(input_file, stop_event=None, pause_event=None):
    """
    Phát tệp âm thanh định dạng p3
    Định dạng p3: [1 byte loại, 1 byte dự trữ, 2 byte độ dài, dữ liệu Opus]
    """
    # Khởi tạo bộ giải mã Opus
    sample_rate = 16000  # Tốc độ lấy mẫu được cố định ở 16000Hz
    channels = 1  # Đơn kênh
    decoder = opuslib.Decoder(sample_rate, channels)

    # Kích thước khung (60ms)
    frame_size = int(sample_rate * 60 / 1000)

    # Mở luồng âm thanh
    stream = sd.OutputStream(
        samplerate=sample_rate,
        channels=channels,
        dtype='int16'
    )
    stream.start()

    try:
        with open(input_file, 'rb') as f:
            print(f"Đang phát: {input_file}")

            while True:
                if stop_event and stop_event.is_set():
                    break

                if pause_event and pause_event.is_set():
                    time.sleep(0.1)
                    continue

                # Đọc tiêu đề (4 byte)
                header = f.read(4)
                if not header or len(header) < 4:
                    break

                # Phân tích cú pháp tiêu đề
                packet_type, reserved, data_len = struct.unpack('>BBH', header)

                # Đọc dữ liệu Opus
                opus_data = f.read(data_len)
                if not opus_data or len(opus_data) < data_len:
                    break

                # Giải mã dữ liệu Opus
                pcm_data = decoder.decode(opus_data, frame_size)

                # Chuyển đổi byte thành mảng numpy
                audio_array = np.frombuffer(pcm_data, dtype=np.int16)

                # Phát âm thanh
                stream.write(audio_array)

    except KeyboardInterrupt:
        print("\nĐã dừng phát")
    finally:
        stream.stop()
        stream.close()
        print("Phát xong")


class P3PlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình phát P3 đơn giản")
        self.root.geometry("500x400")

        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.loop_playback = tk.BooleanVar(value=False)  # Trạng thái hộp kiểm phát lặp lại

        # Tạo các thành phần giao diện
        self.create_widgets()

    def create_widgets(self):
        # Danh sách phát
        self.playlist_label = tk.Label(self.root, text="Danh sách phát:")
        self.playlist_label.pack(pady=5)

        self.playlist_frame = tk.Frame(self.root)
        self.playlist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.playlist_listbox = tk.Listbox(self.playlist_frame, selectmode=tk.SINGLE)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True)

        # Hộp kiểm và nút xóa
        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.pack(pady=5)

        self.remove_button = tk.Button(self.checkbox_frame, text="Xóa tệp", command=self.remove_files)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        # Hộp kiểm phát lặp lại
        self.loop_checkbox = tk.Checkbutton(self.checkbox_frame, text="Phát lặp lại", variable=self.loop_playback)
        self.loop_checkbox.pack(side=tk.LEFT, padx=5)

        # Nút điều khiển
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.add_button = tk.Button(self.control_frame, text="Thêm tệp", command=self.add_file)
        self.add_button.grid(row=0, column=0, padx=5)

        self.play_button = tk.Button(self.control_frame, text="Phát", command=self.play)
        self.play_button.grid(row=0, column=1, padx=5)

        self.pause_button = tk.Button(self.control_frame, text="Tạm dừng", command=self.pause)
        self.pause_button.grid(row=0, column=2, padx=5)

        self.stop_button = tk.Button(self.control_frame, text="Dừng", command=self.stop)
        self.stop_button.grid(row=0, column=3, padx=5)

        # Nhãn trạng thái
        self.status_label = tk.Label(self.root, text="Không phát", fg="blue")
        self.status_label.pack(pady=10)

    def add_file(self):
        files = filedialog.askopenfilenames(filetypes=[("Tệp P3", "*.p3")])
        if files:
            self.playlist.extend(files)
            self.update_playlist()

    def update_playlist(self):
        self.playlist_listbox.delete(0, tk.END)
        for file in self.playlist:
            self.playlist_listbox.insert(tk.END, os.path.basename(file))  # Chỉ hiển thị tên tệp

    def update_status(self, status_text, color="blue"):
        """Cập nhật nội dung nhãn trạng thái"""
        self.status_label.config(text=status_text, fg=color)

    def play(self):
        if not self.playlist:
            messagebox.showwarning("Cảnh báo", "Danh sách phát trống!")
            return

        if self.is_paused:
            self.is_paused = False
            self.pause_event.clear()
            self.update_status(f"Đang phát: {os.path.basename(self.playlist[self.current_index])}", "green")
            return

        if self.is_playing:
            return

        self.is_playing = True
        self.stop_event.clear()
        self.pause_event.clear()
        self.current_index = self.playlist_listbox.curselection()[0] if self.playlist_listbox.curselection() else 0
        self.play_thread = threading.Thread(target=self.play_audio, daemon=True)
        self.play_thread.start()
        self.update_status(f"Đang phát: {os.path.basename(self.playlist[self.current_index])}", "green")

    def play_audio(self):
        while True:
            if self.stop_event.is_set():
                break

            if self.pause_event.is_set():
                time.sleep(0.1)
                continue

            # Kiểm tra xem chỉ mục hiện tại có hợp lệ không
            if self.current_index >= len(self.playlist):
                if self.loop_playback.get():  # Nếu đã chọn phát lặp lại
                    self.current_index = 0  # Quay lại bài đầu tiên
                else:
                    break  # Nếu không thì dừng phát

            file = self.playlist[self.current_index]
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(self.current_index)
            self.playlist_listbox.activate(self.current_index)
            self.update_status(f"Đang phát: {os.path.basename(self.playlist[self.current_index])}", "green")
            play_p3_file(file, self.stop_event, self.pause_event)

            if self.stop_event.is_set():
                break

            if not self.loop_playback.get():  # Nếu không chọn phát lặp lại
                break  # Dừng sau khi phát xong tệp hiện tại

            self.current_index += 1
            if self.current_index >= len(self.playlist):
                if self.loop_playback.get():  # Nếu đã chọn phát lặp lại
                    self.current_index = 0  # Quay lại bài đầu tiên

        self.is_playing = False
        self.is_paused = False
        self.update_status("Đã dừng phát", "red")

    def pause(self):
        if self.is_playing:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.pause_event.set()
                self.update_status("Đã tạm dừng phát", "orange")
            else:
                self.pause_event.clear()
                self.update_status(f"Đang phát: {os.path.basename(self.playlist[self.current_index])}", "green")

    def stop(self):
        if self.is_playing or self.is_paused:
            self.is_playing = False
            self.is_paused = False
            self.stop_event.set()
            self.pause_event.clear()
            self.update_status("Đã dừng phát", "red")

    def remove_files(self):
        selected_indices = self.playlist_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tệp để xóa trước!")
            return

        for index in reversed(selected_indices):
            self.playlist.pop(index)
        self.update_playlist()


if __name__ == "__main__":
    root = tk.Tk()
    app = P3PlayerApp(root)
    root.mainloop()
