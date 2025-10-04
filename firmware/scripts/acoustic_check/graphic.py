import sys
import numpy as np
import asyncio
import wave
from collections import deque
import qasync

import matplotlib
matplotlib.use('qtagg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar  # noqa: F401
from matplotlib.figure import Figure

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit)
from PyQt6.QtCore import QTimer

# Nhập bộ giải mã
from demod import RealTimeAFSKDecoder


class UDPServerProtocol(asyncio.DatagramProtocol):
    """Lớp giao thức máy chủ UDP"""
    def __init__(self, data_queue):
        self.client_address = None
        self.data_queue: deque = data_queue

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        # Nếu chưa có địa chỉ client, ghi lại client kết nối đầu tiên
        if self.client_address is None:
            self.client_address = addr
            print(f"Chấp nhận kết nối từ {addr}")

        # Chỉ xử lý dữ liệu từ client đã được ghi lại
        if addr == self.client_address:
            # Thêm dữ liệu âm thanh đã nhận vào hàng đợi
            self.data_queue.extend(data)
        else:
            print(f"Bỏ qua dữ liệu từ địa chỉ không xác định {addr}")


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Tạo đối tượng Figure của Matplotlib
        self.figure = Figure()

        # Tạo đối tượng FigureCanvas, là một QWidget container cho Figure
        self.canvas = FigureCanvas(self.figure)

        # Tạo thanh công cụ điều hướng của Matplotlib
        # self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar = None

        # Tạo layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Khởi tạo các tham số dữ liệu âm thanh
        self.freq = 16000  # Tần số lấy mẫu
        self.time_window = 20  # Cửa sổ thời gian hiển thị
        self.wave_data = deque(maxlen=self.freq * self.time_window * 2) # Hàng đợi bộ đệm, dùng để phân phối tính toán/vẽ
        self.signals = deque(maxlen=self.freq * self.time_window)  # Hàng đợi hai đầu để lưu trữ dữ liệu tín hiệu

        # Tạo canvas với hai biểu đồ con
        self.ax1 = self.figure.add_subplot(2, 1, 1)
        self.ax2 = self.figure.add_subplot(2, 1, 2)

        # Biểu đồ con miền thời gian
        self.ax1.set_title('Dạng sóng âm thanh thời gian thực')
        self.ax1.set_xlabel('Chỉ số mẫu')
        self.ax1.set_ylabel('Biên độ')
        self.line_time, = self.ax1.plot([], [])
        self.ax1.grid(True, alpha=0.3)

        # Biểu đồ con miền tần số
        self.ax2.set_title('Phổ tần số thời gian thực')
        self.ax2.set_xlabel('Tần số (Hz)')
        self.ax2.set_ylabel('Độ lớn')
        self.line_freq, = self.ax2.plot([], [])
        self.ax2.grid(True, alpha=0.3)

        self.figure.tight_layout()

        # Hẹn giờ để cập nhật biểu đồ
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # Cập nhật mỗi 100 mili giây
        self.timer.timeout.connect(self.update_plot)

        # Khởi tạo bộ giải mã AFSK
        self.decoder = RealTimeAFSKDecoder(
            f_sample=self.freq,
            mark_freq=1800,
            space_freq=1500,
            bitrate=100,
            s_goertzel=9,
            threshold=0.5
        )

        # Callback kết quả giải mã
        self.decode_callback = None

    def start_plotting(self):
        """Bắt đầu vẽ"""
        self.timer.start()

    def stop_plotting(self):
        """Dừng vẽ"""
        self.timer.stop()

    def update_plot(self):
        """Cập nhật dữ liệu vẽ"""
        if len(self.wave_data) >= 2:
            # Thực hiện giải mã thời gian thực
            # Lấy dữ liệu âm thanh mới nhất để giải mã
            even = len(self.wave_data) // 2 * 2
            print(f"Độ dài của wave_data: {len(self.wave_data)}")
            drained = [self.wave_data.popleft() for _ in range(even)]
            signal = np.frombuffer(bytearray(drained), dtype='<i2') / 32768
            decoded_text_new = self.decoder.process_audio(signal) # Xử lý tín hiệu mới, trả về toàn bộ văn bản đã giải mã
            if decoded_text_new and self.decode_callback:
                self.decode_callback(decoded_text_new)
            self.signals.extend(signal.tolist())  # Thêm dữ liệu sóng vào dữ liệu vẽ

        if len(self.signals) > 0:
            # Chỉ hiển thị một đoạn dữ liệu gần đây để tránh biểu đồ quá dày đặc
            signal = np.array(self.signals)
            max_samples = min(len(signal), self.freq * self.time_window)
            if len(signal) > max_samples:
                signal = signal[-max_samples:]

            # Cập nhật biểu đồ miền thời gian
            x = np.arange(len(signal))
            self.line_time.set_data(x, signal)

            # Tự động điều chỉnh phạm vi trục thời gian
            if len(signal) > 0:
                self.ax1.set_xlim(0, len(signal))
                y_min, y_max = np.min(signal), np.max(signal)
                if y_min != y_max:
                    margin = (y_max - y_min) * 0.1
                    self.ax1.set_ylim(y_min - margin, y_max + margin)
                else:
                    self.ax1.set_ylim(-1, 1)

            # Tính toán phổ (biến đổi Fourier rời rạc thời gian ngắn)
            if len(signal) > 1:
                # Tính toán FFT
                fft_signal = np.abs(np.fft.fft(signal))
                frequencies = np.fft.fftfreq(len(signal), 1/self.freq)

                # Chỉ lấy phần tần số dương
                positive_freq_idx = frequencies >= 0
                freq_positive = frequencies[positive_freq_idx]
                fft_positive = fft_signal[positive_freq_idx]

                # Cập nhật biểu đồ miền tần số
                self.line_freq.set_data(freq_positive, fft_positive)

                # Tự động điều chỉnh phạm vi trục tần số
                if len(fft_positive) > 0:
                    # Giới hạn phạm vi hiển thị tần số đến 0-4000Hz để tránh quá dày đặc
                    max_freq_show = min(4000, self.freq // 2)
                    freq_mask = freq_positive <= max_freq_show
                    if np.any(freq_mask):
                        self.ax2.set_xlim(0, max_freq_show)
                        fft_masked = fft_positive[freq_mask]
                        if len(fft_masked) > 0:
                            fft_max = np.max(fft_masked)
                            if fft_max > 0:
                                self.ax2.set_ylim(0, fft_max * 1.1)
                            else:
                                self.ax2.set_ylim(0, 1)

            self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kiểm tra âm thanh")
        self.setGeometry(100, 100, 1000, 800)

        # Widget chính của cửa sổ
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout chính
        main_layout = QVBoxLayout(main_widget)

        # Khu vực vẽ
        self.matplotlib_widget = MatplotlibWidget()
        main_layout.addWidget(self.matplotlib_widget)

        # Bảng điều khiển
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # Nhập địa chỉ và cổng lắng nghe
        control_layout.addWidget(QLabel("Địa chỉ lắng nghe:"))
        self.address_input = QLineEdit("0.0.0.0")
        self.address_input.setFixedWidth(120)
        control_layout.addWidget(self.address_input)

        control_layout.addWidget(QLabel("Cổng:"))
        self.port_input = QLineEdit("8000")
        self.port_input.setFixedWidth(80)
        control_layout.addWidget(self.port_input)

        # Nút lắng nghe
        self.listen_button = QPushButton("Bắt đầu lắng nghe")
        self.listen_button.clicked.connect(self.toggle_listening)
        control_layout.addWidget(self.listen_button)

        # Nhãn trạng thái
        self.status_label = QLabel("Trạng thái: Chưa kết nối")
        control_layout.addWidget(self.status_label)

        # Nhãn thống kê dữ liệu
        self.data_label = QLabel("Dữ liệu đã nhận: 0 bytes")
        control_layout.addWidget(self.data_label)

        # Nút lưu
        self.save_button = QPushButton("Lưu âm thanh")
        self.save_button.clicked.connect(self.save_audio)
        self.save_button.setEnabled(False)
        control_layout.addWidget(self.save_button)

        control_layout.addStretch()  # Thêm không gian co giãn

        main_layout.addWidget(control_panel)

        # Khu vực hiển thị giải mã
        decode_panel = QWidget()
        decode_layout = QVBoxLayout(decode_panel)

        # Tiêu đề giải mã
        decode_title = QLabel("Kết quả giải mã AFSK thời gian thực:")
        decode_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        decode_layout.addWidget(decode_title)

        # Hiển thị văn bản giải mã
        self.decode_text = QTextEdit()
        self.decode_text.setMaximumHeight(150)
        self.decode_text.setReadOnly(True)
        self.decode_text.setStyleSheet("font-family: 'Courier New', monospace; font-size: 12px;")
        decode_layout.addWidget(self.decode_text)

        # Nút điều khiển giải mã
        decode_control_layout = QHBoxLayout()

        # Nút xóa
        self.clear_decode_button = QPushButton("Xóa giải mã")
        self.clear_decode_button.clicked.connect(self.clear_decode_text)
        decode_control_layout.addWidget(self.clear_decode_button)

        # Nhãn thống kê giải mã
        self.decode_stats_label = QLabel("Thống kê giải mã: 0 bits, 0 ký tự")
        decode_control_layout.addWidget(self.decode_stats_label)

        decode_control_layout.addStretch()
        decode_layout.addLayout(decode_control_layout)

        main_layout.addWidget(decode_panel)

        # Đặt callback giải mã
        self.matplotlib_widget.decode_callback = self.on_decode_text

        # Thuộc tính liên quan đến UDP
        self.udp_transport = None
        self.is_listening = False

        # Hẹn giờ thống kê dữ liệu
        self.stats_timer = QTimer(self)
        self.stats_timer.setInterval(1000)  # Cập nhật thống kê mỗi giây
        self.stats_timer.timeout.connect(self.update_stats)

    def on_decode_text(self, new_text: str):
        """Callback văn bản giải mã"""
        if new_text:
            # Thêm văn bản mới được giải mã
            current_text = self.decode_text.toPlainText()
            updated_text = current_text + new_text

            # Giới hạn độ dài văn bản, giữ lại 1000 ký tự mới nhất
            if len(updated_text) > 1000:
                updated_text = updated_text[-1000:]

            self.decode_text.setPlainText(updated_text)

            # Cuộn xuống dưới cùng
            cursor = self.decode_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.decode_text.setTextCursor(cursor)

    def clear_decode_text(self):
        """Xóa văn bản giải mã"""
        self.decode_text.clear()
        if hasattr(self.matplotlib_widget, 'decoder'):
            self.matplotlib_widget.decoder.clear()
        self.decode_stats_label.setText("Thống kê giải mã: 0 bits, 0 ký tự")

    def update_decode_stats(self):
        """Cập nhật thống kê giải mã"""
        if hasattr(self.matplotlib_widget, 'decoder'):
            stats = self.matplotlib_widget.decoder.get_stats()
            stats_text = (
                f"Tiền tố: {stats['prelude_bits']} , Đã nhận {stats['total_chars']} ký tự, "
                f"Bộ đệm: {stats['buffer_bits']} bits, Trạng thái: {stats['state']}"
            )
            self.decode_stats_label.setText(stats_text)

    def toggle_listening(self):
        """Chuyển đổi trạng thái lắng nghe"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    async def start_listening_async(self):
        """Bắt đầu lắng nghe UDP không đồng bộ"""
        try:
            address = self.address_input.text().strip()
            port = int(self.port_input.text().strip())

            loop = asyncio.get_running_loop()
            self.udp_transport, protocol = await loop.create_datagram_endpoint(
                lambda: UDPServerProtocol(self.matplotlib_widget.wave_data),
                local_addr=(address, port)
            )

            self.status_label.setText(f"Trạng thái: Đang lắng nghe ({address}:{port})")
            print(f"Máy chủ UDP đã khởi động, đang lắng nghe tại {address}:{port}")

        except Exception as e:
            self.status_label.setText(f"Trạng thái: Khởi động thất bại - {str(e)}")
            print(f"Khởi động máy chủ UDP thất bại: {e}")
            self.is_listening = False
            self.listen_button.setText("Bắt đầu lắng nghe")
            self.address_input.setEnabled(True)
            self.port_input.setEnabled(True)

    def start_listening(self):
        """Bắt đầu lắng nghe"""
        try:
            int(self.port_input.text().strip())  # Xác thực định dạng cổng
        except ValueError:
            self.status_label.setText("Trạng thái: Cổng phải là một số")
            return

        self.is_listening = True
        self.listen_button.setText("Dừng lắng nghe")
        self.address_input.setEnabled(False)
        self.port_input.setEnabled(False)
        self.save_button.setEnabled(True)

        # Xóa hàng đợi dữ liệu
        self.matplotlib_widget.wave_data.clear()

        # Bắt đầu vẽ và cập nhật thống kê
        self.matplotlib_widget.start_plotting()
        self.stats_timer.start()

        # Bắt đầu máy chủ UDP không đồng bộ
        loop = asyncio.get_event_loop()
        loop.create_task(self.start_listening_async())

    def stop_listening(self):
        """Dừng lắng nghe"""
        self.is_listening = False
        self.listen_button.setText("Bắt đầu lắng nghe")
        self.address_input.setEnabled(True)
        self.port_input.setEnabled(True)

        # Dừng máy chủ UDP
        if self.udp_transport:
            self.udp_transport.close()
            self.udp_transport = None

        # Dừng vẽ và cập nhật thống kê
        self.matplotlib_widget.stop_plotting()
        self.matplotlib_widget.wave_data.clear()
        self.stats_timer.stop()

        self.status_label.setText("Trạng thái: Đã dừng")

    def update_stats(self):
        """Cập nhật thống kê dữ liệu"""
        data_size = len(self.matplotlib_widget.signals)
        self.data_label.setText(f"Dữ liệu đã nhận: {data_size} mẫu")

        # Cập nhật thống kê giải mã
        self.update_decode_stats()

    def save_audio(self):
        """Lưu dữ liệu âm thanh"""
        if len(self.matplotlib_widget.signals) > 0:
            try:
                signal_data = np.array(self.matplotlib_widget.signals)

                # Lưu dưới dạng tệp WAV
                with wave.open("received_audio.wav", "wb") as wf:
                    wf.setnchannels(1)  # Kênh đơn
                    wf.setsampwidth(2)  # Độ rộng mẫu là 2 byte
                    wf.setframerate(self.matplotlib_widget.freq)  # Đặt tần số lấy mẫu
                    wf.writeframes(signal_data.tobytes())  # Ghi dữ liệu

                self.status_label.setText("Trạng thái: Âm thanh đã được lưu vào received_audio.wav")
                print("Âm thanh đã được lưu vào received_audio.wav")

            except Exception as e:
                self.status_label.setText(f"Trạng thái: Lưu thất bại - {str(e)}")
                print(f"Lưu âm thanh thất bại: {e}")
        else:
            self.status_label.setText("Trạng thái: Không có đủ dữ liệu để lưu")


async def main():
    """Hàm chính không đồng bộ"""
    app = QApplication(sys.argv)

    # Đặt vòng lặp sự kiện không đồng bộ
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    try:
        with loop:
            await loop.run_forever()
    except KeyboardInterrupt:
        print("Chương trình bị người dùng ngắt")
    finally:
        # Đảm bảo dọn dẹp tài nguyên
        if window.udp_transport:
            window.udp_transport.close()