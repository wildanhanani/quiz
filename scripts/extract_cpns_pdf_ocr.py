from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=True)


def render_pdf_page(page_pdf_path: Path, output_png_path: Path) -> None:
    subprocess.run(
        ['sips', '-s', 'format', 'png', str(page_pdf_path), '--out', str(output_png_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def ocr_png(png_path: Path) -> str:
    result = run_command(['tesseract', str(png_path), 'stdout', '-l', 'eng'])
    return result.stdout.strip()


def extract_pages(pdf_path: Path, start_page: int, end_page: int, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir / '_rendered_pages'
    temp_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf_path))

    for page_number in range(start_page, end_page + 1):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number - 1])

        page_pdf_path = temp_dir / f'page-{page_number}.pdf'
        page_png_path = temp_dir / f'page-{page_number}.png'
        page_txt_path = output_dir / f'page-{page_number}.txt'

        with page_pdf_path.open('wb') as handle:
            writer.write(handle)

        render_pdf_page(page_pdf_path, page_png_path)
        ocr_text = ocr_png(page_png_path)
        page_txt_path.write_text(ocr_text, encoding='utf-8')
        print(f'Extracted OCR for page {page_number} -> {page_txt_path}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Extract OCR text from scanned PDF pages.')
    parser.add_argument('pdf_path', type=Path)
    parser.add_argument('start_page', type=int)
    parser.add_argument('end_page', type=int)
    parser.add_argument('output_dir', type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extract_pages(args.pdf_path, args.start_page, args.end_page, args.output_dir)


if __name__ == '__main__':
    main()
