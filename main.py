import json
import os

saldo = 0
akun_aktif = ""
FILE_SALDO = "akun_data.json"
total_pemasukan = 0
total_pengeluaran = 0
riwayat = []
akun_database = {}

def simpan_data():
    akun_database[akun_aktif] = {
        "saldo": saldo,
        "total_pemasukan": total_pemasukan,
        "total_pengeluaran": total_pengeluaran,
        "riwayat": riwayat,
        "pin": akun_database[akun_aktif].get("pin", "0000")
    }
    with open(FILE_SALDO, 'w') as file:
        json.dump(akun_database, file)

def muat_data():
    global saldo, total_pemasukan, total_pengeluaran, riwayat, akun_database
    if os.path.exists(FILE_SALDO):
        with open(FILE_SALDO, 'r') as file:
            akun_database = json.load(file)
    return akun_database

def muat_akun(nama_akun):
    global saldo, total_pemasukan, total_pengeluaran, riwayat
    if nama_akun in akun_database:
        data = akun_database[nama_akun]
        saldo = data.get("saldo", 0)
        total_pemasukan = data.get("total_pemasukan", 0)
        total_pengeluaran = data.get("total_pengeluaran", 0)
        riwayat = data.get("riwayat", [])
    else:
        saldo = 0
        total_pemasukan = 0
        total_pengeluaran = 0
        riwayat = []

def login_akun():
    global akun_aktif
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + " " * 15 + "LOGIN KE AKUN ANDA" + " " * 16 + "║")
    print("╚" + "═" * 48 + "╝")
    
    if akun_database:
        print("\nAkun yang tersedia:")
        akun_list = list(akun_database.keys())
        for i, akun in enumerate(akun_list, 1):
            print(f"{i}. {akun}")
        print(f"{len(akun_list) + 1}. Buat Akun Baru")
        
        try:
            pilihan = int(input("\nPilih akun atau buat baru: "))
            if 1 <= pilihan <= len(akun_list):
                akun_dipilih = akun_list[pilihan - 1]
                
                # Verifikasi PIN
                pin_akun = akun_database[akun_dipilih].get("pin", "0000")
                print("\n" + "=" * 50)
                print("              VERIFIKASI PIN")
                print("=" * 50)
                
                max_percobaan = 3
                for percobaan in range(max_percobaan):
                    pin_input = input("Masukkan PIN (4 digit): ")
                    
                    if pin_input == pin_akun:
                        akun_aktif = akun_dipilih
                        muat_akun(akun_aktif)
                        print(f"\n✓ Login berhasil sebagai {akun_aktif}\n")
                        return True
                    else:
                        sisa = max_percobaan - percobaan - 1
                        if sisa > 0:
                            print(f"❌ PIN salah! Sisa percobaan: {sisa}\n")
                        else:
                            print("❌ PIN salah! Akses ditolak!\n")
                            return False
                
            elif pilihan == len(akun_list) + 1:
                nama_baru = input("Masukkan nama akun baru: ").strip()
                if nama_baru and nama_baru not in akun_database:
                    print("\n" + "=" * 50)
                    print("            BUAT PIN AKUN BARU")
                    print("=" * 50)
                    
                    while True:
                        pin_baru = input("Masukkan PIN (4 digit angka): ")
                        if len(pin_baru) == 4 and pin_baru.isdigit():
                            konfirmasi_pin = input("Konfirmasi PIN: ")
                            if pin_baru == konfirmasi_pin:
                                akun_aktif = nama_baru
                                akun_database[akun_aktif] = {
                                    "saldo": 0,
                                    "total_pemasukan": 0,
                                    "total_pengeluaran": 0,
                                    "riwayat": [],
                                    "pin": pin_baru
                                }
                                muat_akun(akun_aktif)
                                simpan_data()
                                print(f"\n✓ Akun {akun_aktif} berhasil dibuat dengan PIN!\n")
                                return True
                            else:
                                print("❌ PIN tidak cocok! Coba lagi.\n")
                        else:
                            print("❌ PIN harus 4 digit angka!\n")
                else:
                    print("❌ Nama akun tidak valid atau sudah ada!\n")
                    return False
        except ValueError:
            print("❌ Input tidak valid!\n")
            return False
    else:
        nama_baru = input("Masukkan nama akun baru Anda: ").strip()
        if nama_baru:
            print("\n" + "=" * 50)
            print("            BUAT PIN AKUN BARU")
            print("=" * 50)
            
            while True:
                pin_baru = input("Masukkan PIN (4 digit angka): ")
                if len(pin_baru) == 4 and pin_baru.isdigit():
                    konfirmasi_pin = input("Konfirmasi PIN: ")
                    if pin_baru == konfirmasi_pin:
                        akun_aktif = nama_baru
                        akun_database[akun_aktif] = {
                            "saldo": 0,
                            "total_pemasukan": 0,
                            "total_pengeluaran": 0,
                            "riwayat": [],
                            "pin": pin_baru
                        }
                        muat_akun(akun_aktif)
                        simpan_data()
                        print(f"\n✓ Akun {akun_aktif} berhasil dibuat dengan PIN!\n")
                        return True
                    else:
                        print("❌ PIN tidak cocok! Coba lagi.\n")
                else:
                    print("❌ PIN harus 4 digit angka!\n")
    return False

def ubah_pin():
    global akun_aktif
    print("\n" + "=" * 50)
    print("              UBAH PIN AKUN")
    print("=" * 50)
    
    pin_lama = akun_database[akun_aktif].get("pin", "0000")
    pin_input = input("Masukkan PIN lama: ")
    
    if pin_input != pin_lama:
        print("❌ PIN lama tidak cocok!\n")
        return
    
    while True:
        pin_baru = input("Masukkan PIN baru (4 digit angka): ")
        if len(pin_baru) == 4 and pin_baru.isdigit():
            konfirmasi_pin = input("Konfirmasi PIN baru: ")
            if pin_baru == konfirmasi_pin:
                akun_database[akun_aktif]["pin"] = pin_baru
                simpan_data()
                print("\n✓ PIN berhasil diubah!\n")
                return
            else:
                print("❌ PIN tidak cocok! Coba lagi.\n")
        else:
            print("❌ PIN harus 4 digit angka!\n")

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
            tipe_transaksi = item.get('tipe', 'TRANSFER')
            if tipe_transaksi == "Setor":
                tipe_transaksi = "SETOR"
            elif tipe_transaksi == "Tarik":
                tipe_transaksi = "TARIK"
            
            # Jika ada info penerima/pengirim, tampilkan
            keterangan = ""
            if 'penerima' in item:
                keterangan = f" ke {item['penerima']}"
            elif 'pengirim' in item:
                keterangan = f" dari {item['pengirim']}"
            
            print(f"{i}. {tipe_transaksi:10} : Rp {item['jumlah']:>15,}{keterangan}")
        if len(riwayat) > 10:
            print(f"...dan {len(riwayat) - 10} transaksi lainnya")
        print("-" * 50 + "\n")
    else:
        print("\nBelum ada transaksi\n")

def transfer_uang():
    global saldo, total_pengeluaran
    print("\n" + "=" * 50)
    print("                 TRANSFER UANG")
    print("=" * 50)
    
    # Tampilkan akun yang tersedia
    akun_tujuan_list = [akun for akun in akun_database.keys() if akun != akun_aktif]
    
    if not akun_tujuan_list:
        print("❌ Tidak ada akun lain untuk transfer!\n")
        return
    
    print("\nAkun Tujuan Transfer:")
    for i, akun in enumerate(akun_tujuan_list, 1):
        saldo_akun = akun_database[akun].get('saldo', 0)
        print(f"{i}. {akun:20} (Saldo: Rp {saldo_akun:,})")
    
    try:
        pilihan = int(input("\nPilih akun tujuan (nomor): "))
        if not (1 <= pilihan <= len(akun_tujuan_list)):
            print("❌ Pilihan tidak valid!\n")
            return
        
        akun_penerima = akun_tujuan_list[pilihan - 1]
        jumlah = int(input("\nMasukkan jumlah transfer: Rp "))
        
        if jumlah <= 0:
            print("❌ Jumlah harus lebih dari 0!\n")
            return
        
        if jumlah > saldo:
            print("-" * 50)
            print("❌ SALDO TIDAK CUKUP!")
            print(f"Saldo Anda      : Rp {saldo:,}")
            print(f"Jumlah yang diminta : Rp {jumlah:,}")
            print("=" * 50 + "\n")
            return
        
        print("-" * 50)
        print(f"Dari Akun       : {akun_aktif}")
        print(f"Ke Akun         : {akun_penerima}")
        print(f"Jumlah Transfer : Rp {jumlah:,}")
        print(f"Saldo Sebelumnya : Rp {saldo:,}")
        print("-" * 50)
        
        konfirmasi = input("Lanjutkan transfer? (y/n): ")
        if konfirmasi.lower() == 'y':
            # Update saldo pengirim
            saldo = saldo - jumlah
            total_pengeluaran = total_pengeluaran + jumlah
            riwayat.append({"tipe": "Transfer", "jumlah": jumlah, "penerima": akun_penerima})
            
            # Update saldo penerima
            data_penerima = akun_database[akun_penerima]
            data_penerima['saldo'] += jumlah
            data_penerima['total_pemasukan'] += jumlah
            data_penerima['riwayat'].append({"tipe": "Transfer", "jumlah": jumlah, "pengirim": akun_aktif})
            
            simpan_data()
            akun_database[akun_penerima] = data_penerima
            
            with open(FILE_SALDO, 'w') as file:
                json.dump(akun_database, file)
            
            print("\n✓ Transfer berhasil!")
            print(f"Saldo sekarang   : Rp {saldo:,}")
            print("=" * 50 + "\n")
        else:
            print("\n❌ Transfer dibatalkan\n")
    
    except ValueError:
        print("❌ Input tidak valid!\n")

def menu():
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║" + f" {akun_aktif:^46} " + "║")
    print("╠" + "═" * 48 + "╣")
    print("║ 1. Setor Uang" + " " * 36 + "║")
    print("║ 2. Tarik Uang" + " " * 36 + "║")
    print("║ 3. Transfer ke Akun Lain" + " " * 25 + "║")
    print("║ 4. Lihat Saldo" + " " * 35 + "║")
    print("║ 5. Lihat Riwayat Transaksi" + " " * 22 + "║")
    print("║ 6. Ubah PIN" + " " * 38 + "║")
    print("║ 7. Ganti Akun" + " " * 36 + "║")
    print("║ 8. Selesai / Keluar" + " " * 29 + "║")
    print("╚" + "═" * 48 + "╝")

def pesan_keluar():
    print("\n" + "=" * 50)
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "      Terima kasih telah menggunakan ATM      ".center(48) + "║")
    print("║" + f"           UANG SAKU SAYA ({akun_aktif})".ljust(48) + "║")
    print("║" + " " * 48 + "║")
    print("║" + f"  Saldo Akhir Anda : Rp {saldo:>20,}  ".ljust(48) + "║")
    print("║" + " " * 48 + "║")
    print("║" + "    Semoga hari Anda menyenangkan!".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "═" * 48 + "╝")
    print("=" * 50 + "\n")

# Muat data dari file saat program dimulai
muat_data()

# Login ke akun
while not login_akun():
    pass

while True:
    menu()
    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        transfer_uang()
    elif pilihan == "4":
        lihat_saldo()
    elif pilihan == "5":
        laporan()
    elif pilihan == "6":
        ubah_pin()
    elif pilihan == "7":
        simpan_data()
        while not login_akun():
            pass
    elif pilihan == "8":
        simpan_data()
        pesan_keluar()
        break
    else:
        print("❌ Pilihan tidak valid")