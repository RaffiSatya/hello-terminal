# Project 01 — `hello-terminal`

**Durasi:** 2 hari · **Fase:** 0 (Fondasi Tools)

## 🎯 Tujuan
Setelah project ini kamu bisa:
1. Bergerak di terminal tanpa mouse (pindah folder, lihat isi, buat/hapus file).
2. Paham apa itu **virtual environment (venv)** dan kenapa setiap project punya venv sendiri.
3. Install library dengan **pip** dan mencatatnya di `requirements.txt`.
4. Menjalankan script Python dengan **argumen** dari terminal (`python organize.py folder --dry-run`).

**Hasil akhir:** CLI `organize.py` yang merapikan folder data GIS berantakan ke subfolder Vektor/Raster/Tabel/dst.

---

## 📚 Bagian 1 — Konsep

### 1.1 Terminal itu apa?
Terminal = cara ngobrol dengan komputer pakai teks, bukan klik. Di Windows kamu punya dua:
- **PowerShell** (bawaan Windows) — yang kita pakai di project ini.
- **Git Bash** (ikut terinstall bersama Git) — perintahnya ala Linux, nanti dipakai saat masuk server.

Kenapa penting? Hampir semua tools developer (git, docker, pip, npm, deploy) dijalankan lewat terminal. Server di cloud juga **tidak punya mouse**.

### 1.2 Path (alamat file)
- **Absolute path:** alamat lengkap dari root drive → `E:\03_Raffi's Project\01-hello-terminal\organize.py`
- **Relative path:** alamat relatif dari posisi kamu sekarang → `.\organize.py`
- `.` = folder saat ini, `..` = folder induk (satu tingkat ke atas)

> ⚠️ Nama folder kamu mengandung spasi dan tanda petik (`03_Raffi's Project`). Di terminal, path seperti ini **wajib dibungkus tanda kutip ganda**: `cd "E:\03_Raffi's Project"`. Ke depan, biasakan nama folder project tanpa spasi (pakai `-` atau `_`).

### 1.3 Perintah dasar PowerShell
| Perintah | Fungsi | Padanan Linux/Git Bash |
|---|---|---|
| `pwd` | Tampilkan folder posisi sekarang | `pwd` |
| `ls` | Lihat isi folder | `ls` |
| `cd <folder>` | Pindah folder | `cd` |
| `cd ..` | Naik satu folder | `cd ..` |
| `mkdir <nama>` | Buat folder | `mkdir` |
| `ni <nama>` | Buat file kosong (New-Item) | `touch` |
| `cat <file>` | Tampilkan isi file | `cat` |
| `rm <file>` | Hapus file (**permanen, tidak masuk Recycle Bin!**) | `rm` |
| `cls` | Bersihkan layar | `clear` |
| `code .` | Buka folder ini di VS Code | `code .` |

Tips: tekan **Tab** untuk auto-complete nama file/folder, **↑** untuk perintah sebelumnya.

### 1.4 Virtual environment (venv)
Bayangkan setiap project butuh versi library berbeda: project A butuh `geopandas 0.14`, project B butuh `geopandas 1.0`. Kalau semua diinstall ke Python global, mereka **bentrok**.

**venv** = "Python pribadi" untuk satu project, berupa folder `.venv/` di dalam project. Library yang diinstall saat venv **aktif** hanya masuk ke folder itu.

```
Python global (C:\Program Files\Python312)
 ├── 01-hello-terminal\.venv   → rich
 ├── 05-geo-data-cleaner\.venv → pandas, geopandas
 └── 13-fastapi-hello\.venv    → fastapi, uvicorn
```

### 1.5 pip & requirements.txt
- `pip` = installer library Python (mirip "Play Store" untuk Python).
- `requirements.txt` = daftar library + versi yang dibutuhkan project. Orang lain cukup menjalankan `pip install -r requirements.txt` untuk mendapatkan library yang sama persis.

### 1.6 Argumen command line
`python organize.py sample_data --dry-run`
- `organize.py` → script yang dijalankan
- `sample_data` → **argumen posisi** (wajib)
- `--dry-run` → **flag/opsi** (opsional, nyala/mati)

Di Python, argumen ini dibaca dengan modul bawaan `argparse`.

---

## 🛠️ Bagian 2 — Praktik (kamu yang ketik semua perintah)

Buka **PowerShell** (atau terminal di VS Code: `` Ctrl+` ``). Ketik satu per satu, perhatikan output-nya.

### Langkah 1 — Navigasi
```powershell
cd "E:\03_Raffi's Project\01-hello-terminal"
pwd
ls
```
Kamu harusnya melihat: `BRIEF.md`, `organize.py`, `make_sample_data.py`, `requirements.txt`.

### Langkah 2 — Buat & aktifkan venv
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Kalau berhasil, muncul `(.venv)` di awal baris prompt.

> Kalau muncul error *"running scripts is disabled on this system"*, jalankan sekali:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` lalu ulangi aktivasi. (Ini mengizinkan script lokal milikmu sendiri berjalan, hanya untuk user kamu.)

Cek bahwa Python yang dipakai sekarang adalah milik venv:
```powershell
(Get-Command python).Source
```

### Langkah 3 — Install library
```powershell
pip install -r requirements.txt
pip list
```

### Langkah 4 — Buat data latihan
```powershell
python make_sample_data.py
ls sample_data
```

### Langkah 5 — Jalankan organizer
```powershell
python organize.py --help
python organize.py sample_data --dry-run
ls sample_data
python organize.py sample_data
ls sample_data
ls sample_data\Raster
```
Perhatikan: setelah `--dry-run`, isi `sample_data` **belum berubah**.

### Langkah 6 — Coba-coba
```powershell
python organize.py sample_data          # jalankan lagi — apa yang terjadi?
python organize.py folder_ngawur        # folder yang tidak ada
deactivate                               # keluar dari venv
python organize.py sample_data          # tanpa venv — apa yang terjadi? kenapa?
```

---

## 🔍 Bagian 3 — Penjelasan Kode `organize.py`

Buka file-nya di VS Code (`code .`) sambil baca ini.

| Bagian | Penjelasan |
|---|---|
| `CATEGORIES = {...}` | **Dictionary**: kunci = nama kategori, nilai = list ekstensi. Mau tambah kategori cukup ubah di sini — logika lain tidak perlu disentuh. |
| `get_category(file)` | `file.suffix` mengambil ekstensi (`.tif`). `.lower()` supaya `.TIF` = `.tif`. Loop cari ekstensi di setiap kategori; kalau tidak ketemu → `"Lainnya"`. |
| `unique_destination()` | Mencegah file tertimpa. Kalau `foto.jpg` sudah ada, file baru jadi `foto_1.jpg`, `foto_2.jpg`, dst. |
| `organize(folder, dry_run)` | Inti program. `folder.iterdir()` = semua isi folder. Subfolder dilewati (`continue`). Kalau `dry_run` → hanya print; kalau tidak → `mkdir` + `shutil.move`. Mengembalikan ringkasan jumlah per kategori. |
| `print_summary()` | Pakai library `rich` untuk menampilkan tabel cantik. |
| `main()` | Membaca argumen terminal dengan `argparse`, validasi folder, panggil `organize()`. `SystemExit(1)` = keluar dengan kode error (angka ≠ 0 artinya gagal — ini konvensi semua program CLI). |
| `if __name__ == "__main__":` | `main()` hanya jalan kalau file ini **dieksekusi langsung**, bukan saat di-`import` dari file lain. |

Konsep penting: **`pathlib.Path`** — cara modern menangani path di Python. Operator `/` menggabungkan path: `folder / "Raster"` → `sample_data\Raster`, dan otomatis benar di Windows maupun Linux.

---

## ❓ Bagian 4 — Kuis

Jawab di chat. Jangan buka Google dulu, tebak berdasarkan pemahamanmu.

1. Kamu sedang di `E:\03_Raffi's Project\01-hello-terminal`. Setelah `cd ..`, kamu ada di mana?
2. Kenapa `cd E:\03_Raffi's Project` (tanpa kutip) gagal?
3. Apa beda `python -m venv .venv` dengan `.\.venv\Scripts\Activate.ps1`? Kenapa butuh dua langkah?
4. Di Langkah 6, kenapa `python organize.py sample_data` gagal setelah `deactivate`? Sebutkan nama error-nya.
5. **Tebak output:** apa hasil `get_category(Path("Peta_Final.GeoJSON"))`? Jelaskan.
6. **Tebak output:** file `backup_project.qgz` masuk ke kategori apa? Menurutmu itu benar atau perlu diperbaiki?
7. Apa yang terjadi kalau baris `if item.is_dir(): continue` dihapus, lalu organizer dijalankan **dua kali**?
8. Teman kamu clone project ini. Perintah apa saja (urut) yang dia jalankan supaya bisa memakai `organize.py`?

### 🐛 Cari Bug
Seseorang mengubah `get_category` jadi seperti ini. Apa bug-nya, dan file apa dari `sample_data` yang salah masuk kategori?
```python
def get_category(file: Path) -> str:
    extension = file.suffix
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
        return DEFAULT_CATEGORY
```
*(Petunjuk: ada 2 bug.)*

---

## ✍️ Bagian 5 — Modifikasi Kecil (bagian kamu)

1. Tambahkan kategori **`"LiDAR"`** untuk ekstensi `.las` dan `.laz`, plus kategori **`"QGIS"`** untuk `.qgz` dan `.qgs`.
2. Tambahkan `"titik_awan.laz"` ke `SAMPLE_FILES` di `make_sample_data.py`.
3. Hapus folder `sample_data`, buat ulang, jalankan organizer, dan pastikan file LiDAR & QGIS masuk ke foldernya.

```powershell
rm -r sample_data
python make_sample_data.py
python organize.py sample_data
```

**Bonus (opsional):** tambahkan flag `--verbose` yang kalau tidak dipakai, baris `✓ file → kategori` tidak ditampilkan (hanya tabel ringkasan).

---

## 🗣️ Bagian 6 — Explain-back
Jelaskan dengan kata-katamu sendiri (3–5 kalimat) di chat:
> "Apa yang terjadi dari saat aku mengetik `python organize.py sample_data` sampai tabel ringkasan muncul?"

## ✅ Kriteria Selesai
- [ ] Semua langkah praktik berhasil dijalankan
- [ ] Kuis 1–8 + Cari Bug dijawab
- [ ] Modifikasi kecil selesai dan berjalan
- [ ] Explain-back dikirim

Selanjutnya → **Project 02 `git-journal`**: folder ini akan kita jadikan repo Git pertamamu dan di-push ke GitHub.
