"""
organize.py — Merapikan isi folder berdasarkan jenis file (khusus data geospasial).

Cara pakai:
    python organize.py <folder>              # benar-benar memindahkan file
    python organize.py <folder> --dry-run    # hanya simulasi, tidak memindahkan apa pun
"""

import argparse
import shutil
from pathlib import Path

from rich.console import Console
from rich.table import Table

# Peta: nama kategori -> daftar ekstensi file.
# Shapefile terdiri dari banyak file (.shp, .shx, .dbf, .prj, ...) — semuanya
# masuk kategori yang sama supaya tidak terpisah.
CATEGORIES = {
    "Vektor": [".shp", ".shx", ".dbf", ".prj", ".cpg", ".geojson", ".gpkg", ".kml", ".kmz"],
    "Raster": [".tif", ".tiff", ".jp2", ".ecw", ".img"],
    "Tabel": [".csv", ".xlsx", ".xls"],
    "Dokumen": [".pdf", ".docx", ".txt", ".md"],
    "Gambar": [".jpg", ".jpeg", ".png"],
    "LiDAR": [".las", ".laz"],
    "QGIS": [".qgz", ".qgs"],
}
DEFAULT_CATEGORY = "Lainnya"

console = Console()


def get_category(file: Path) -> str:
    """Kembalikan nama kategori untuk sebuah file berdasarkan ekstensinya."""
    extension = file.suffix.lower()  # ".TIF" dan ".tif" dianggap sama
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return DEFAULT_CATEGORY


def unique_destination(destination: Path) -> Path:
    """Kalau file tujuan sudah ada, tambahkan _1, _2, ... supaya tidak menimpa."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool) -> dict[str, int]:
    """Pindahkan setiap file di `folder` ke subfolder sesuai kategorinya.

    Mengembalikan jumlah file per kategori, misalnya {"Vektor": 5, "Raster": 2}.
    """
    summary: dict[str, int] = {}

    for item in sorted(folder.iterdir()):
        # Lewati subfolder (termasuk folder kategori hasil run sebelumnya)
        if item.is_dir():
            continue

        category = get_category(item)
        target_folder = folder / category
        destination = unique_destination(target_folder / item.name)

        if dry_run:
            console.print(f"[yellow][DRY-RUN][/] {item.name} → {category}/")
        else:
            target_folder.mkdir(exist_ok=True)
            shutil.move(item, destination)
            console.print(f"[green]✓[/] {item.name} → {category}/{destination.name}")

        summary[category] = summary.get(category, 0) + 1

    return summary


def print_summary(summary: dict[str, int]) -> None:
    """Tampilkan ringkasan dalam bentuk tabel."""
    table = Table(title="Ringkasan")
    table.add_column("Kategori")
    table.add_column("Jumlah file", justify="right")
    for category, count in sorted(summary.items()):
        table.add_row(category, str(count))
    table.add_row("[bold]Total[/]", f"[bold]{sum(summary.values())}[/]")
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rapikan folder berdasarkan jenis file.")
    parser.add_argument("folder", type=Path, help="Folder yang mau dirapikan")
    parser.add_argument("--dry-run", action="store_true", help="Simulasi saja, jangan pindahkan file")
    args = parser.parse_args()

    if not args.folder.is_dir():
        console.print(f"[red]Error:[/] '{args.folder}' bukan folder yang valid.")
        raise SystemExit(1)

    summary = organize(args.folder, args.dry_run)
    if not summary:
        console.print("Folder sudah rapi — tidak ada file untuk dipindahkan.")
        return
    print_summary(summary)


if __name__ == "__main__":
    main()
