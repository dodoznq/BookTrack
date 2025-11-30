import os, sys
import customtkinter as ctk
import json
from datetime import datetime


file = "kitaplar.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class BookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BookTrack")
        self.geometry("600x600")
        self.iconbitmap(resource_path("booktrack.ico"))

        self.user_name = os.getlogin()

        self.header_label = ctk.CTkLabel(self, text=self.get_greeting(), font=("Arial", 20))
        self.header_label.pack(pady=10)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=10)
        self.tabview.add("Kitap Ekle")
        self.tabview.add("Kitapları Güncelle")
        self.tabview.add("Kitap Sil")
        self.tabview.add("Kitap Listesi")

        self.create_add_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_list_tab()
        self.footer_label = ctk.CTkLabel(self, text="")
        self.footer_label.pack(pady=10)
        self.update_footer()

    def get_greeting(self):
        hour = datetime.now().hour

        if 5 <= hour < 12:
            return f"Günaydın, {self.user_name}! ☀️"
        elif 12 <= hour < 18:
            return f"İyi günler, {self.user_name}! 🌤️"
        else:
            return f"İyi akşamlar, {self.user_name}! 🌙"

    def create_add_tab(self):
        tab = self.tabview.tab("Kitap Ekle")
        ctk.CTkLabel(tab, text="Kitap Adı:").pack(pady=5)
        self.add_name_entry = ctk.CTkEntry(tab)
        self.add_name_entry.pack(pady=5)

        ctk.CTkLabel(tab, text="Toplam Sayfa:").pack(pady=5)
        self.add_pages_entry = ctk.CTkEntry(tab)
        self.add_pages_entry.pack(pady=5)

        self.add_result = ctk.CTkLabel(tab, text="")
        self.add_result.pack(pady=5)

        ctk.CTkButton(tab, text="Ekle", command=self.add_book_gui).pack(pady=10)

    def add_book_gui(self):
        kitap_ad = self.add_name_entry.get()
        try:
            toplam_sayfa = int(self.add_pages_entry.get())
        except ValueError:
            self.add_result.configure(text="Toplam sayfa sayı olmalı!")
            return

        try:
            with open(file, "r") as f:
                kitaplar = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            kitaplar = []

        for kitap in kitaplar:
            if kitap["kitap_ad"].lower() == kitap_ad.lower():
                self.add_result.configure(text="Bu isimde zaten kitap var!")
                return

        kitaplar.append({
            "kitap_ad": kitap_ad,
            "toplam_sayfa": toplam_sayfa,
            "okunan_sayfa": 0
        })

        with open(file, "w") as f:
            json.dump(kitaplar, f, indent=4)

        self.add_result.configure(text=f"{kitap_ad} eklendi!")
        self.add_name_entry.delete(0, "end")
        self.add_pages_entry.delete(0, "end")
        self.refresh_list()
        self.update_footer()

    def create_update_tab(self):
        tab = self.tabview.tab("Kitapları Güncelle")
        ctk.CTkLabel(tab, text="Kitap Adı:").pack(pady=5)
        self.update_name_entry = ctk.CTkEntry(tab)
        self.update_name_entry.pack(pady=5)

        ctk.CTkLabel(tab, text="Okunan Sayfa:").pack(pady=5)
        self.update_pages_entry = ctk.CTkEntry(tab)
        self.update_pages_entry.pack(pady=5)

        self.update_result = ctk.CTkLabel(tab, text="")
        self.update_result.pack(pady=5)

        ctk.CTkButton(tab, text="Güncelle", command=self.update_book_gui).pack(pady=10)

    def update_book_gui(self):
        kitap_ad = self.update_name_entry.get()
        try:
            sayfa = int(self.update_pages_entry.get())
        except ValueError:
            self.update_result.configure(text="sayfa sayı olmalı!")
            return

        try:
            with open(file, "r") as f:
                kitaplar = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.update_result.configure(text="henüz kitap eklenmemiş.")
            return

        for kitap in kitaplar:
            if kitap["kitap_ad"].lower() == kitap_ad.lower():
                if sayfa > kitap["toplam_sayfa"]:
                    self.update_result.configure(text=f"Kitap toplam {kitap['toplam_sayfa']} sayfa!")
                    return
                kitap["okunan_sayfa"] = sayfa
                break
        else:
            self.update_result.configure(text="kitap bulunamadı!")
            return

        with open(file, "w") as f:
            json.dump(kitaplar, f, indent=4)
        self.update_result.configure(text=f"{kitap_ad} güncellendi!")
        self.update_name_entry.delete(0, "end")
        self.update_pages_entry.delete(0, "end")
        self.refresh_list()
        self.update_footer()

    def create_delete_tab(self):
        tab = self.tabview.tab("Kitap Sil")
        ctk.CTkLabel(tab, text="Kitap Adı:").pack(pady=5)
        self.delete_name_entry = ctk.CTkEntry(tab)
        self.delete_name_entry.pack(pady=5)

        self.delete_result = ctk.CTkLabel(tab, text="")
        self.delete_result.pack(pady=5)

        ctk.CTkButton(tab, text="Sil", command=self.delete_book_gui).pack(pady=10)

    def delete_book_gui(self):
        kitap_ad = self.delete_name_entry.get()

        try:
            with open(file, "r") as f:
                kitaplar = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.delete_result.configure(text="henüz kitap eklenmemiş.")
            return

        for i, kitap in enumerate(kitaplar):
            if kitap["kitap_ad"].lower() == kitap_ad.lower():
                del kitaplar[i]
                with open(file, "w") as f:
                    json.dump(kitaplar, f, indent=4)
                self.delete_result.configure(text=f"{kitap_ad} silindi!")
                self.delete_name_entry.delete(0, "end")
                self.refresh_list()
                self.update_footer()
                return

        self.delete_result.configure(text="kitap bulunamadı!")

    def create_list_tab(self):
        tab = self.tabview.tab("Kitap Listesi")
        self.list_frame = ctk.CTkFrame(tab)
        self.list_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.refresh_list_button = ctk.CTkButton(tab, text="Yenile", command=self.refresh_list)
        self.refresh_list_button.pack(pady=5)
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        try:
            with open(file, "r") as f:
                kitaplar = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            kitaplar = []

        if not kitaplar:
            ctk.CTkLabel(self.list_frame, text="henüz kitap eklenmemiş.").pack()
            return

        for k in kitaplar:
            kitap_label = ctk.CTkLabel(self.list_frame, text=f"{k['kitap_ad']} ({k['okunan_sayfa']}/{k['toplam_sayfa']})")
            kitap_label.pack(pady=2)

            progress = ctk.CTkProgressBar(self.list_frame, width=400)
            progress.set(k["okunan_sayfa"]/k["toplam_sayfa"])
            progress.pack(pady=2)

    def update_footer(self):
        try:
            with open(file, "r") as f:
                kitaplar = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            kitaplar = []

        if kitaplar:
            last = kitaplar[-1]["kitap_ad"]
            self.footer_label.configure(text=f"son eklenen kitap: {last}")
        else:
            self.footer_label.configure(text="henüz kitap eklenmemiş.")

if __name__ == "__main__":
    app = BookApp()
    app.mainloop()
