import json
import os

saldo = 0
FILE_SALDO = "saldo.json"
total_pemasukan = 0
total_pengeluaran = 0
riwayat = []

def simpan_data():
    with open(FILE_SALDO, 'w') as file:
        json.dump({
            "saldo": saldo, 
            "total_pemasukan": total_pemasukan,
            "total_pengeluaran": total_pengeluaran,
            "riwayat": riwayat
        }, file)

def muat_data():
    global saldo, total_pemasukan, total_pengeluaran, riwayat
    if os.path.exists(FILE_SALDO):
        with open(FILE_SALDO, 'r') as file:
            data = json.load(file)
            saldo = data.get("saldo", 0)
            total_pemasukan = data.get("total_pemasukan", 0)
            total_pengeluaran = data.get("total_pengeluaran", 0)
            riwayat = data.get("riwayat", [])
    return saldo

def tambah_pemasukan():
    global saldo, total_pemasukan
    print("\n" + "=" * 50)
    print("                  SETOR UANG")
    print("=" * 50)
    try:
        jumlah = int(input("Masukkan jumlah setor: Rp "))
        if jumlah <= 0:
            print("❌ Jumlah harus lebih dari 0!\n")
            return
        
        print("-" * 50)
        print(f"Jumlah setor     : Rp {jumlah:,}")
        print(f"Saldo sebelumnya : Rp {saldo:,}")
        print("-" * 50)
        
        konfirmasi = input("Lanjutkan transaksi? (y/n): ")
        if konfirmasi.lower() == 'y':
            saldo = saldo + jumlah
            total_pemasukan = total_pemasukan + jumlah
            riwayat.append({"tipe": "Setor", "jumlah": jumlah})
            simpan_data()
            print("\n✓ Transaksi berhasil!")
            print(f"Saldo sekarang   : Rp {saldo:,}")
            print("=" * 50 + "\n")
        else:
            print("\n❌ Transaksi dibatalkan\n")
    except ValueError:
        print("❌ Input tidak valid!\n")

def tambah_pengeluaran():
    global saldo, total_pengeluaran
    print("\n" + "=" * 50)
    print("                  TARIK UANG")
    print("=" * 50)
    try:
        jumlah = int(input("Masukkan jumlah tarik: Rp "))
        if jumlah <= 0:
            print("❌ Jumlah harus lebih dari 0!\n")
            return
        
        if jumlah > saldo:
            print("-" * 50)
            print("❌ SALDO TIDAK CUKUP!")
            print(f"Saldo Anda      : Rp {saldo:,}")
            print(f"Jumlah yang diminta : Rp {jumlah:,}")
            print("=" * 50 + "\n")
        else:
            print("-" * 50)
            print(f"Jumlah tarik    : Rp {jumlah:,}")
            print(f"Saldo sebelumnya : Rp {saldo:,}")
            print("-" * 50)
            
            konfirmasi = input("Lanjutkan transaksi? (y/n): ")
            if konfirmasi.lower() == 'y':
                saldo = saldo - jumlah
                total_pengeluaran = total_pengeluaran + jumlah
                riwayat.append({"tipe": "Tarik", "jumlah": jumlah})
                simpan_data()
                print("\n✓ Transaksi berhasil!")
                print(f"Saldo sekarang   : Rp {saldo:,}")
                print("=" * 50 + "\n")
            else:
                print("\n❌ Transaksi dibatalkan\n")
    except ValueError:
        print("❌ Input tidak valid!\n")

def lihat_saldo():
    print("\n" + "=" * 50)
    print("              INFORMASI SALDO")
    print("=" * 50)
    print(f"Saldo Anda saat ini : Rp {saldo:,}")
    print("=" * 50 + "\n")

def laporan():
    print("\n" + "=" * 50)
    print("         RINGKASAN TRANSAKSI KEUANGAN")
    print("=" * 50)
    print(f"Setor Masuk      : Rp {total_pemasukan:,}")
    print(f"Penarikan        : Rp {total_pengeluaran:,}")
    print(f"Saldo Akhir      : Rp {saldo:,}")
    print("=" * 50)
    
    if riwayat:
        print("\nRiwayat Transaksi (Terbaru ke Terlama):")
        print("-" * 50)
        for i, item in enumerate(riwayat[-10:], 1):  # Tampilkan 10 transaksi terbaru
            tipe_transaksi = "SETOR" if item['tipe'] == "Setor" else "TARIK"
            print(f"{i}. {tipe_transaksi:6} : Rp {item['jumlah']:>15,}")
        if len(riwayat) > 10:
            print(f"...dan {len(riwayat) - 10} transaksi lainnya")
        print("-" * 50 + "\n")
    else:
        print("\nBelum ada transaksi\n")

def menu():
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + " " * 10 + "SELAMAT DATANG DI ATM UANG SAKU" + " " * 8 + "║")
    print("╠" + "═" * 48 + "╣")
    print("║ 1. Setor Uang" + " " * 36 + "║")
    print("║ 2. Tarik Uang" + " " * 36 + "║")
    print("║ 3. Lihat Saldo" + " " * 35 + "║")
    print("║ 4. Lihat Riwayat Transaksi" + " " * 22 + "║")
    print("║ 5. Selesai / Keluar" + " " * 29 + "║")
    print("╚" + "═" * 48 + "╝")

def pesan_keluar():
    print("\n" + "=" * 50)
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "      Terima kasih telah menggunakan ATM      ".center(48) + "║")
    print("║" + "           UANG SAKU ".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("║" + f"  Saldo Akhir Anda : Rp {saldo:>20,}  ".ljust(48) + "║")
    print("║" + " " * 48 + "║")
    print("║" + "    Semoga hari Anda menyenangkan!".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "═" * 48 + "╝")
    print("=" * 50 + "\n")

# Muat data dari file saat program dimulai
saldo = muat_data()

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        laporan()
    elif pilihan == "5":
        simpan_data()
        pesan_keluar()
        break
    else:
        print("Pilihan tidak valid")