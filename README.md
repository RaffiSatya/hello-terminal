# hello-terminal 🗂️

CLI sederhana untuk merapikan folder data GIS yang berantakan. File dipindah ke subfolder berdasarkan jenisnya: Vektor, Raster, LiDAR, QGIS, Tabel, Dokumen, Gambar, dan Lainnya.

Komponen shapefile (`.shp`, `.shx`, `.dbf`, `.prj`, `.cpg`) selalu masuk ke folder yang sama supaya tidak terpisah.

## Instalasi

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Cara pakai

```powershell
python make_sample_data.py                  # buat data latihan di sample_data/
python organize.py sample_data --dry-run    # simulasi, tidak ada file yang dipindah
python organize.py sample_data              # pindahkan file
```

Contoh output:

```
        Ringkasan
┌──────────┬─────────────┐
│ Kategori │ Jumlah file │
├──────────┼─────────────┤
│ Raster   │           3 │
│ Vektor   │           7 │
│ ...      │         ... │
└──────────┴─────────────┘
```

## Yang dipelajari
Terminal (PowerShell), path, virtual environment, pip, `requirements.txt`, `argparse`, `pathlib`, `shutil`.

---
Project 01 dari [roadmap belajar](../ROADMAP.md) saya.
