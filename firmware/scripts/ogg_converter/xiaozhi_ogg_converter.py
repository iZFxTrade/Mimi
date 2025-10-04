import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import sys
import ffmpeg

class AudioConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Công cụ chuyển đổi hàng loạt âm thanh OGG của AI Xiaozhi")
        master.geometry("680x600")  # Điều chỉnh chiều cao cửa sổ

        # Khởi tạo biến
        self.mode = tk.StringVar(value="audio_to_ogg")
        self.output_dir = tk.StringVar()
        self.output_dir.set(os.path.abspath("output"))
        self.enable_loudnorm = tk.BooleanVar(value=True)
        self.target_lufs = tk.DoubleVar(value=-16.0)

        # Tạo các thành phần UI
        self.create_widgets()
        self.redirect_output()

    def create_widgets(self):
        # Chọn chế độ
        mode_frame = ttk.LabelFrame(self.master, text="Chế độ chuyển đổi")
        mode_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        ttk.Radiobutton(mode_frame, text="Chuyển đổi âm thanh sang OGG", variable=self.mode,
                        value="audio_to_ogg", command=self.toggle_settings,
                        width=25).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(mode_frame, text="Chuyển đổi OGG về âm thanh", variable=self.mode,
                        value="ogg_to_audio", command=self.toggle_settings,
                        width=25).grid(row=0, column=1, padx=5)

        # Cài đặt độ lớn
        self.loudnorm_frame = ttk.Frame(self.master)
        self.loudnorm_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Checkbutton(self.loudnorm_frame, text="Bật điều chỉnh độ lớn",
                       variable=self.enable_loudnorm, width=20
                       ).grid(row=0, column=0, padx=2)
        ttk.Entry(self.loudnorm_frame, textvariable=self.target_lufs,
                 width=6).grid(row=0, column=1, padx=2)
        ttk.Label(self.loudnorm_frame, text="LUFS").grid(row=0, column=2, padx=2)

        # Chọn tệp
        file_frame = ttk.LabelFrame(self.master, text="Tệp đầu vào")
        file_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Nút thao tác tệp
        ttk.Button(file_frame, text="Chọn tệp", command=self.select_files,
                  width=12).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(file_frame, text="Xóa mục đã chọn", command=self.remove_selected,
                  width=12).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(file_frame, text="Xóa danh sách", command=self.clear_files,
                  width=12).grid(row=0, column=2, padx=5, pady=2)

        # Danh sách tệp (sử dụng Treeview)
        self.tree = ttk.Treeview(file_frame, columns=("selected", "filename"),
                               show="headings", height=8)
        self.tree.heading("selected", text="Chọn", anchor=tk.W)
        self.tree.heading("filename", text="Tên tệp", anchor=tk.W)
        self.tree.column("selected", width=60, anchor=tk.W)
        self.tree.column("filename", width=600, anchor=tk.W)
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=2)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        # Thư mục đầu ra
        output_frame = ttk.LabelFrame(self.master, text="Thư mục đầu ra")
        output_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        ttk.Entry(output_frame, textvariable=self.output_dir, width=60
                 ).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(output_frame, text="Duyệt...", command=self.select_output_dir,
                  width=8).grid(row=0, column=1, padx=5)

        # Khu vực nút chuyển đổi
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Chuyển đổi tất cả", command=lambda: self.start_conversion(True),
                  width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Chuyển đổi mục đã chọn", command=lambda: self.start_conversion(False),
                  width=20).pack(side=tk.LEFT, padx=5)

        # Khu vực nhật ký
        log_frame = ttk.LabelFrame(self.master, text="Nhật ký")
        log_frame.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")

        self.log_text = tk.Text(log_frame, height=14, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Cấu hình trọng số bố cục
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(2, weight=1)
        self.master.rowconfigure(5, weight=3)
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(1, weight=1)

    def toggle_settings(self):
        if self.mode.get() == "audio_to_ogg":
            self.loudnorm_frame.grid()
        else:
            self.loudnorm_frame.grid_remove()

    def select_files(self):
        file_types = [
            ("Tệp âm thanh", "*.wav *.mogg *.ogg *.flac") if self.mode.get() == "audio_to_ogg"
            else ("Tệp OGG", "*.ogg")
        ]

        files = filedialog.askopenfilenames(filetypes=file_types)
        for f in files:
            self.tree.insert("", tk.END, values=("[ ]", os.path.basename(f)), tags=(f,))

    def on_tree_click(self, event):
        """Xử lý sự kiện nhấp vào hộp kiểm"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            if col == "#1":  # Nhấp vào cột chọn
                current_val = self.tree.item(item, "values")[0]
                new_val = "[√]" if current_val == "[ ]" else "[ ]"
                self.tree.item(item, values=(new_val, self.tree.item(item, "values")[1]))

    def remove_selected(self):
        """Xóa các tệp đã chọn"""
        to_remove = []
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == "[√]":
                to_remove.append(item)
        for item in reversed(to_remove):
            self.tree.delete(item)

    def clear_files(self):
        """Xóa tất cả các tệp"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def select_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def redirect_output(self):
        class StdoutRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
                self.original_stdout = sys.stdout

            def write(self, message):
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
                self.original_stdout.write(message)

            def flush(self):
                self.original_stdout.flush()

        sys.stdout = StdoutRedirector(self.log_text)

    def start_conversion(self, convert_all):
        """Bắt đầu chuyển đổi"""
        input_files = []
        for item in self.tree.get_children():
            if convert_all or self.tree.item(item, "values")[0] == "[√]":
                input_files.append(self.tree.item(item, "tags")[0])

        if not input_files:
            msg = "Không tìm thấy tệp để chuyển đổi" if convert_all else "Chưa chọn tệp nào"
            messagebox.showwarning("Cảnh báo", msg)
            return

        os.makedirs(self.output_dir.get(), exist_ok=True)

        try:
            if self.mode.get() == "audio_to_ogg":
                target_lufs = self.target_lufs.get() if self.enable_loudnorm.get() else None
                thread = threading.Thread(target=self.convert_audio_to_ogg, args=(target_lufs, input_files))
            else:
                thread = threading.Thread(target=self.convert_ogg_to_audio, args=(input_files,))

            thread.start()
        except Exception as e:
            print(f"Khởi tạo chuyển đổi thất bại: {str(e)}")

    def convert_audio_to_ogg(self, target_lufs, input_files):
        """Logic chuyển đổi âm thanh sang OGG"""
        for input_path in input_files:
            try:
                filename = os.path.basename(input_path)
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(self.output_dir.get(), f"{base_name}.ogg")

                print(f"Đang chuyển đổi: {filename}")
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, acodec='libopus', audio_bitrate='16k', ac=1, ar=16000, frame_duration=60)
                    .run(overwrite_output=True)
                )
                print(f"Chuyển đổi thành công: {filename}\n")
            except Exception as e:
                print(f"Chuyển đổi thất bại: {str(e)}\n")

    def convert_ogg_to_audio(self, input_files):
        """Logic chuyển đổi OGG về âm thanh"""
        for input_path in input_files:
            try:
                filename = os.path.basename(input_path)
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(self.output_dir.get(), f"{base_name}.wav") # Chuyển đổi OGG sang WAV

                print(f"Đang chuyển đổi: {filename}")
                (
                    ffmpeg
                    .input(input_path)
                    .output(output_path, acodec='pcm_s16le', ar=16000) # Chỉ định codec và tốc độ lấy mẫu
                    .run(overwrite_output=True)
                )
                print(f"Chuyển đổi thành công: {filename}\n")
            except Exception as e:
                print(f"Chuyển đổi thất bại: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
