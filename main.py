import json
from os.path import exists

file = "kitaplar.json"

# kitap ekleme
def add_book():
    kitap_ad = input("kitap adı: ")
    while True:
        try:
            toplam_sayfa = int(input("toplam sayfa sayısı: "))
            break
        except ValueError:
            print("lütfen sadece sayı giriniz!")
    try:
        with open(file, "r") as f:
            try:
                kitaplar = json.load(f)
            except json.decoder.JSONDecodeError:
                kitaplar = []
    except FileNotFoundError:
        kitaplar = []

    for kitap in kitaplar:
        if kitap["kitap_ad"].lower() == kitap_ad.lower():
            print("bu isimde zaten bir kitap var!")
            return

    kitaplar.append({
        "kitap_ad": kitap_ad,
        "toplam_sayfa": toplam_sayfa,
        "okunan_sayfa": 0
    })

    with open(file, "w") as f:
        json.dump(kitaplar, f, indent=4)

    print(f"{kitap_ad} eklendi!")


def sayfa_guncelle(kitap_ad, sayfa):
    try:
        with open(file, "r") as f:
            try:
                kitaplar = json.load(f)
            except json.decoder.JSONDecodeError:
                kitaplar = []
    except FileNotFoundError:
        print("henüz hiç kitap eklenmemiş.")
        return

    if not kitaplar:
        print("henüz hiç kitap eklenmemiş.")
        return

    for kitap in kitaplar:
        if kitap["kitap_ad"].lower() == kitap_ad.lower():
            if sayfa > kitap["toplam_sayfa"]:
                print(f"kitap toplam {kitap['toplam_sayfa']} sayfa, daha fazla okuyamazsın!")
                return  # menüye geri dön
            kitap["okunan_sayfa"] = sayfa
            break
    else:
        print("kitap bulunamadı!")
        return

    with open(file, "w") as f:
        json.dump(kitaplar, f, indent=4)
    print(f"{kitap_ad} güncellendi!")

def kitap_sil():
    kitap_ad = input("silmek istediğiniz kitabın adı: ")

    try:
        with open(file, "r") as f:
            try:
                kitaplar = json.load(f)
            except json.decoder.JSONDecodeError:
                kitaplar = []
    except FileNotFoundError:
        print("henüz hiç kitap eklenmemiş.")
        return

    if not kitaplar:
        print("henüz hiç kitap eklenmemiş.")
        return

    # kitap silme
    for i, kitap in enumerate(kitaplar):
        if kitap["kitap_ad"].lower() == kitap_ad.lower():
            del kitaplar[i]  # listeden çıkar
            with open(file, "w") as f:
                json.dump(kitaplar, f, indent=4)
            print(f"{kitap_ad} silindi!")
            return  # menüye dön

    print("kitap bulunamadı!")

def listele():
    try:
        with open(file, "r") as f:
            kitaplar = json.load(f)
    except FileNotFoundError:
        print("henüz kitap eklenmemiş.")
        return
    except json.decoder.JSONDecodeError:
        print("kitap listesi boş veya bozuk..")
        kitaplar = []
        return
    if not kitaplar:
        print("henüz kitap eklenmemiş.")
        return
    for k in kitaplar:
        kalan = k["toplam_sayfa"] - k["okunan_sayfa"]
        print(f"{k['kitap_ad']}: {k['okunan_sayfa']}/{k['toplam_sayfa']} sayfa okundu, {kalan} sayfa kaldı")

# menü
def menu():
    print("\nwelcome to BookTrack.")
    print("press 1 to add a book.")
    print("press 2 to delete a book.")
    print("press 3 to view book list.")
    print("press 4 to update read pages.")
    print("press 5 to exit")

    selection = int(input("please select a section: "))
    return selection

while True:
    selection = menu()
    if selection == 1:
        add_book()
    elif selection == 2:
        kitap_sil()
    elif selection == 3:
        listele()
    elif selection == 4:
        kitap_ad = input("kitap adı: ")
        sayfa = int(input("kaç sayfa okundu: "))
        sayfa_guncelle(kitap_ad, sayfa)
    elif selection == 5:
        print("exiting...")
        break
    else:
        print("please select a valid option.")
