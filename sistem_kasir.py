"""Sistem Kasir Sederhana - UTS Pemrograman Berorientasi Objek"""


class Produk:
    jumlah_produk = 0  # class attribute

    def __init__(self, nama, harga, stok):  # constructor
        self.nama = nama          # attribute
        self.__harga = 0          # private (encapsulation)
        self.__stok = 0
        self.harga = harga        # lewat setter (ada validasi)
        self.stok = stok
        Produk.jumlah_produk += 1

    # ---- property / setter ----
    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai):
        if nilai <= 0:
            raise ValueError("Harga harus lebih dari 0")
        self.__harga = nilai

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif")
        self.__stok = nilai

    # ---- method biasa ----
    def kurangi_stok(self, jumlah):
        if jumlah > self.__stok:
            raise ValueError(f"Stok {self.nama} tidak cukup (sisa {self.__stok})")
        self.__stok -= jumlah

    # ---- class method ----
    @classmethod
    def dari_string(cls, data):
        """Buat objek dari string 'nama,harga,stok'"""
        nama, harga, stok = data.split(",")
        return cls(nama.strip(), int(harga), int(stok))

    @classmethod
    def total_produk(cls):
        return cls.jumlah_produk

    # ---- static method ----
    @staticmethod
    def format_rupiah(angka):
        return f"Rp{angka:,.0f}".replace(",", ".")

    def __str__(self):
        return f"{self.nama} - {self.format_rupiah(self.harga)} (stok: {self.stok})"


class Kasir:
    def __init__(self, nama_kasir):
        self.nama_kasir = nama_kasir
        self.__keranjang = []  # private

    def tambah_item(self, produk, jumlah):
        try:
            produk.kurangi_stok(jumlah)
            self.__keranjang.append((produk, jumlah))
            print(f"+ {jumlah} x {produk.nama} ditambahkan")
        except ValueError as e:
            print(f"! Gagal: {e}")

    def hitung_total(self):
        return sum(p.harga * j for p, j in self.__keranjang)

    def cetak_struk(self):
        print("\n===== STRUK BELANJA =====")
        print(f"Kasir: {self.nama_kasir}")
        for p, j in self.__keranjang:
            print(f"{p.nama:<12} {j} x {Produk.format_rupiah(p.harga):<10} "
                  f"= {Produk.format_rupiah(p.harga * j)}")
        print("-" * 25)
        print(f"TOTAL: {Produk.format_rupiah(self.hitung_total())}")
        print("=========================")


if __name__ == "__main__":
    # membuat object
    p1 = Produk("Indomie", 3500, 20)
    p2 = Produk("Teh Botol", 5000, 15)
    p3 = Produk.dari_string("Roti, 8000, 5")  # pakai class method

    print("Daftar produk:")
    for p in (p1, p2, p3):
        print(" ", p)
    print("Total jenis produk:", Produk.total_produk())

    kasir = Kasir("Budi")
    kasir.tambah_item(p1, 3)
    kasir.tambah_item(p2, 2)
    kasir.tambah_item(p3, 10)  # stok kurang -> ditolak
    kasir.tambah_item(p3, 2)
    kasir.cetak_struk()

    # demo setter
    p1.harga = 4000
    print("\nHarga Indomie baru:", Produk.format_rupiah(p1.harga))
