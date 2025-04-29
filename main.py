import tkinter as tk
from tkinter import font, filedialog
from PIL import Image, ImageTk
import datetime
import os

class DesktopClockApp:
    def __init__(self, root):
        """アプリケーションの初期化"""
        self.root = root
        self.root.title("卓上時計")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self._is_fullscreen = True

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # 日本語曜日リスト (datetime.weekday()は月曜=0, 日曜=6)
        self.weekdays_jp = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

        self.bg_label = tk.Label(self.root, bg="black")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_image_path = None
        self.bg_photo_image = None

        # --- ラベルの右下の隙間 ---
        padding_x = -20
        padding_y = -10

        # --- 時計用ラベル ---
        self.clock_font_size = int(self.screen_height / 12) # 少し小さめに調整
        self.clock_label = tk.Label(
            self.root,
            font=("Arial", self.clock_font_size, "bold"),
            fg="white",
            bg="black",
            bd=0
        )
        # 右下に配置
        self.clock_label.place(relx=1.0, rely=1.0, anchor="se", x=padding_x, y=padding_y)

        # --- 日付・曜日用ラベル ---
        self.date_font_size = int(self.clock_font_size * 0.45) # 時計より小さいフォント
        self.date_label = tk.Label(
            self.root,
            font=("Arial", self.date_font_size),
            fg="white",
            bg="black",
            bd=0
        )
        # 時計ラベルのすぐ上に配置
        # 時計ラベルの anchor='se' と relx=1.0, rely=1.0 を利用
        # y オフセットを時計ラベルの高さ分程度、さらに上にずらす
        # フォントサイズからおおよその高さを計算して調整
        date_y_offset = padding_y - int(self.clock_font_size * 1.5) # 時計ラベルの高さ分+α上にずらす
        self.date_label.place(relx=1.0, rely=1.0, anchor="se", x=padding_x, y=date_y_offset)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="背景画像を選択", command=self.select_background)
        self.menu.add_separator()
        self.menu.add_command(label="終了", command=self.root.destroy)
        self.root.bind("<Button-3>", self.show_menu)

        # 画像初期設定
        # image.pngが同じディレクトリに無ければ黒塗り背景のまま
        initial_bg_image_path = "image.png"
        if os.path.isfile(initial_bg_image_path):
            self.load_background(initial_bg_image_path)

        # ここが追加された行（ダブルクリックで終了）
        self.root.bind("<Double-Button-1>", lambda event: self.root.destroy())

        self.update_time() # 初回更新

    def toggle_fullscreen(self, event=None):
        """フルスクリーン状態を切り替える"""
        self._is_fullscreen = not self._is_fullscreen
        self.root.attributes('-fullscreen', self._is_fullscreen)
        if self.bg_image_path:
            self.root.after(100, lambda: self.load_background(self.bg_image_path))

    def show_menu(self, event):
        """右クリックメニューを表示する"""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def select_background(self):
        """ファイルダイアログを開き、背景画像を選択させる"""
        file_path = filedialog.askopenfilename(
            title="背景画像を選択してください",
            filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.gif *.bmp"), ("すべてのファイル", "*.*")]
        )
        if file_path:
            self.bg_image_path = file_path
            self.load_background(file_path)

    def load_background(self, file_path):
        """指定されたパスの画像を読み込み、背景として設定する"""
        try:
            current_width = self.root.winfo_width()
            current_height = self.root.winfo_height()
            if current_width <= 1 or current_height <= 1:
                 current_width = self.screen_width
                 current_height = self.screen_height

            image = Image.open(file_path)
            try:
                resample_filter = Image.Resampling.LANCZOS
            except AttributeError:
                resample_filter = Image.LANCZOS

            resized_image = image.resize((current_width, current_height), resample_filter)
            self.bg_photo_image = ImageTk.PhotoImage(resized_image)

            self.bg_label.config(image=self.bg_photo_image, bg=None)
            self.clock_label.lift()
            self.date_label.lift() # 日付ラベルも最前面に

            # 時計と日付ラベルの背景をデフォルト（黒）に戻す（背景画像ありの場合）
            self.clock_label.config(bg="black")
            self.date_label.config(bg="black")

        except FileNotFoundError:
             print(f"エラー: ファイルが見つかりません - {file_path}")
             self.show_error_message(f"ファイルが見つかりません:\n{file_path}")
             self.clear_background()
        except Exception as e:
            print(f"エラー: 背景画像の読み込みに失敗しました - {e}")
            self.show_error_message(f"画像の読み込みに失敗しました:\n{e}")
            self.clear_background()

    def clear_background(self):
         """背景画像をクリアし、デフォルトの黒背景に戻す"""
         self.bg_label.config(image="", bg="black")
         self.bg_photo_image = None
         self.bg_image_path = None
         # 時計と日付ラベルの背景も黒に戻す
         self.clock_label.config(bg="black")
         self.date_label.config(bg="black")

    def show_error_message(self, message):
         """エラーメッセージを小さなウィンドウで表示"""
         error_win = tk.Toplevel(self.root)
         error_win.title("エラー")
         error_win.geometry("300x100")
         msg_label = tk.Label(error_win, text=message, justify=tk.LEFT, padx=10, pady=10)
         msg_label.pack(expand=True, fill=tk.BOTH)
         ok_button = tk.Button(error_win, text="OK", command=error_win.destroy)
         ok_button.pack(pady=5)
         error_win.grab_set()
         error_win.focus_set()
         error_win.wait_window()

    def update_time(self):
        """現在時刻、日付、曜日を取得し、ラベルを更新する"""
        now = datetime.datetime.now()

        # 時刻を HH:MM:SS 形式で取得
        time_str = now.strftime("%H:%M:%S")
        # 時計ラベルのテキストを更新
        self.clock_label.config(text=time_str)

        # 日付と曜日を取得・フォーマット
        # 例: 2025-04-12 (土)
        weekday_index = now.weekday() # 月曜日が0、日曜日が6
        weekday_jp = self.weekdays_jp[weekday_index]
        date_str = now.strftime("%Y-%m-%d") + f" ({weekday_jp})" # フォーマット変更可

        # 日付・曜日ラベルのテキストを更新
        # 前回と同じ文字列なら更新しない（日付が変わった時だけ更新）ようにしても良いが、
        # ここではシンプルに毎回更新する
        self.date_label.config(text=date_str)

        # 1000ms (1秒) 後に再度この関数を呼び出す
        self.root.after(1000, self.update_time)

# --- メイン処理 ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopClockApp(root)
    root.mainloop()