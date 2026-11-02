"""
make_sample_data.py — Membuat folder `sample_data/` berisi file dummy yang berantakan,
untuk latihan menjalankan organize.py. Aman dijalankan berulang kali.
"""

from pathlib import Path

SAMPLE_FILES = [
    "batas_desa.shp", "batas_desa.shx", "batas_desa.dbf", "batas_desa.prj",
    "jalan_kabupaten.geojson", "titik_survey.gpkg", "jalur_pendakian.kml",
    "dem_merapi.tif", "sentinel2_B04.jp2", "ortofoto_2024.TIF",
    "koordinat_patok.csv", "rekap_luas.xlsx",
    "laporan_pengukuran.pdf", "catatan_lapangan.txt",
    "foto_patok_01.jpg", "foto_patok_02.JPG",
    "backup_project.qgz", "titik_awan.laz", "random_file.xyz",
]


def main() -> None:
    folder = Path(__file__).parent / "sample_data"
    folder.mkdir(exist_ok=True)
    for name in SAMPLE_FILES:
        (folder / name).write_text(f"dummy content for {name}\n", encoding="utf-8")
    print(f"Dibuat {len(SAMPLE_FILES)} file dummy di: {folder}")


if __name__ == "__main__":
    main()
