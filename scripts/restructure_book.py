#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import os
import re
import shutil
from collections import defaultdict
from bs4 import BeautifulSoup
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
ASSETS_DIR = ROOT / "assets"
CSS_DIR = ASSETS_DIR / "css"
PDF_DIR = ASSETS_DIR / "pdf"
DOCS_DIR = ASSETS_DIR / "docs"
IMG_DIR = ASSETS_DIR / "images"
COMMON_IMG_DIR = IMG_DIR / "common"
BUILD_DIR = ROOT / "archive" / "build-artifacts"
SOURCE_DIR = ROOT / "source" / "latex"


def ensure_dirs():
    for p in [CHAPTERS_DIR, CSS_DIR, PDF_DIR, DOCS_DIR, COMMON_IMG_DIR, BUILD_DIR, SOURCE_DIR, ROOT / "scripts"]:
        p.mkdir(parents=True, exist_ok=True)


def find_chapter_files() -> list[Path]:
    in_root = sorted(ROOT.glob("chapter-*.html"))
    in_chapters = sorted(CHAPTERS_DIR.glob("chapter-*.html"))
    return in_chapters if in_chapters else in_root


def chapter_code(ch_path: Path) -> str:
    m = re.search(r"chapter-(\d+)", ch_path.name)
    return f"ch{int(m.group(1)):02d}" if m else "common"


def safe_move(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return
    if dst.exists():
        if src.is_file() and dst.is_file() and src.read_bytes() == dst.read_bytes():
            src.unlink()
            return
        stem, suf = dst.stem, dst.suffix
        i = 2
        while True:
            cand = dst.with_name(f"{stem}-{i}{suf}")
            if not cand.exists():
                dst = cand
                break
            i += 1
    shutil.move(str(src), str(dst))


def resolve_ref(base_file: Path, ref: str) -> Path | None:
    if ref.startswith(("http://", "https://", "data:", "#", "mailto:")):
        return None
    return (base_file.parent / ref).resolve()


def rel_for(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, from_file.parent).replace("\\", "/")


def move_chapters_to_dir(chapter_files: list[Path]) -> list[Path]:
    moved = []
    for ch in chapter_files:
        dst = CHAPTERS_DIR / ch.name
        safe_move(ch, dst)
        moved.append(dst)
    return sorted(moved)


def classify_and_move_images(chapter_files: list[Path]):
    ref_chapters: dict[str, set[Path]] = defaultdict(set)
    ref_locations: list[tuple[Path, str]] = []

    for ch in chapter_files:
        soup = BeautifulSoup(ch.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue
            ref_locations.append((ch, src))
            ref_chapters[src].add(ch)

    dest_by_ref: dict[str, Path] = {}
    used = set()
    for ref, chs in ref_chapters.items():
        src_abs = resolve_ref(ROOT / "dummy.html", ref)
        if src_abs is None or not src_abs.exists() or not src_abs.is_file():
            continue
        if len(chs) == 1:
            code = chapter_code(next(iter(chs)))
            base_dir = IMG_DIR / code
        else:
            base_dir = COMMON_IMG_DIR
        base_dir.mkdir(parents=True, exist_ok=True)

        name = src_abs.name
        cand = base_dir / name
        if cand.as_posix() in used or (cand.exists() and cand.resolve() != src_abs.resolve()):
            stem, suf = src_abs.stem, src_abs.suffix
            i = 2
            while True:
                c2 = base_dir / f"{stem}-{i}{suf}"
                if c2.as_posix() not in used and not c2.exists():
                    cand = c2
                    break
                i += 1
        used.add(cand.as_posix())
        dest_by_ref[ref] = cand

    moved_src = set()
    for ref, dst in dest_by_ref.items():
        src_abs = resolve_ref(ROOT / "dummy.html", ref)
        if src_abs and src_abs.exists() and src_abs.is_file() and src_abs.as_posix() not in moved_src:
            safe_move(src_abs, dst)
            moved_src.add(src_abs.as_posix())

    for ch in chapter_files:
        soup = BeautifulSoup(ch.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        changed = False
        for img in soup.find_all("img"):
            src = img.get("src")
            if src in dest_by_ref:
                img["src"] = rel_for(ch, dest_by_ref[src])
                changed = True
        if changed:
            ch.write_text(str(soup), encoding="utf-8")


def move_misc_files(chapter_files: list[Path]):
    # style.css
    css_old = ROOT / "style.css"
    if css_old.exists():
        safe_move(css_old, CSS_DIR / "style.css")

    # Main pdf
    main_pdf = ROOT / "AppliedEconometrics.pdf"
    if main_pdf.exists():
        safe_move(main_pdf, PDF_DIR / "AppliedEconometrics.pdf")

    # Additional docs/pdf files (except chapter pages)
    for p in list(ROOT.glob("*.pdf")):
        if p.name == "AppliedEconometrics.pdf":
            continue
        safe_move(p, DOCS_DIR / p.name)

    for p in [ROOT / "image", ROOT / "figure"]:
        if p.exists() and p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    safe_move(f, DOCS_DIR / f.name if f.suffix.lower()==".pdf" else COMMON_IMG_DIR / f.name)
            shutil.rmtree(p)

    # LaTeX sources
    for ext in ("*.tex", "*.cls", "*.bib"):
        for p in ROOT.glob(ext):
            safe_move(p, SOURCE_DIR / p.name)

    for name in ["License", "README.md", "README-CN.md", ".gitattributes"]:
        p = ROOT / name
        if p.exists() and p.is_file() and name != "README.md":
            safe_move(p, SOURCE_DIR / p.name)

    # Build artifacts
    for pat in ("*.aux", "*.log", "*.dvi", "*.tmp", "*.4ct", "*.4tc", "*.xref", "*.bcf"):
        for p in ROOT.glob(pat):
            safe_move(p, BUILD_DIR / p.name)

    # Unassigned root images to common
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.webp", "*.JPG"):
        for p in ROOT.glob(ext):
            if p.is_file():
                safe_move(p, COMMON_IMG_DIR / p.name)


def rewrite_paths(chapter_files: list[Path]):
    # Index and chapters path rewrites for css/pdf/links
    index = ROOT / "index.html"
    files = [index] + chapter_files
    for f in files:
        if not f.exists():
            continue
        soup = BeautifulSoup(f.read_text(encoding="utf-8", errors="ignore"), "html.parser")

        # css link
        for link in soup.find_all("link", rel=lambda x: x and "stylesheet" in x):
            href = link.get("href")
            if href and href.endswith("style.css"):
                target = CSS_DIR / "style.css"
                link["href"] = rel_for(f, target)

        # PDF download links
        for a in soup.find_all("a"):
            href = a.get("href") or ""
            if href.endswith("AppliedEconometrics.pdf"):
                a["href"] = rel_for(f, PDF_DIR / "AppliedEconometrics.pdf")

        # back-home link
        for a in soup.select("p.back-home a"):
            a["href"] = rel_for(f, ROOT / "index.html")

        # Chapter links in index should point to chapters/
        if f.name == "index.html":
            for a in soup.find_all("a"):
                href = a.get("href") or ""
                if re.fullmatch(r"chapter-\d+\.html", href):
                    a["href"] = f"chapters/{href}"

        # fix chapter-to-chapter links if currently prefixed with chapters/
        if f.parent == CHAPTERS_DIR:
            for a in soup.find_all("a"):
                href = a.get("href") or ""
                if re.fullmatch(r"chapters/chapter-\d+\.html", href):
                    a["href"] = href.split("/", 1)[1]

        f.write_text(str(soup), encoding="utf-8")


def rewrite_readme():
    readme = ROOT / "README.md"
    txt = """# theeffect_book (GitHub Pages)

已重构为分层结构：

- `index.html`：封面页
- `chapters/`：章节页面（`chapter-xx.html`）
- `assets/css/style.css`：样式
- `assets/images/chXX/`：按章节图片
- `assets/images/common/`：公共图片
- `assets/pdf/AppliedEconometrics.pdf`：主 PDF
- `assets/docs/`：附加文档
- `scripts/update_nav.py`：目录自动更新脚本

## 目录自动更新

当你新增或删除 `chapters/chapter-xx.html` 后，执行：

```bash
python3 scripts/update_nav.py
```

它会自动同步：

- 封面页的章节目录
- 每个章节页左侧目录
- 当前章节高亮与“返回封面”链接

## 本地预览

```bash
python3 -m http.server 8000
```

访问 `http://localhost:8000`。
"""
    readme.write_text(txt, encoding="utf-8")


def main():
    ensure_dirs()

    chapter_files = find_chapter_files()
    if not chapter_files:
        raise SystemExit("No chapter files found.")

    chapter_files = move_chapters_to_dir(chapter_files)
    classify_and_move_images(chapter_files)
    move_misc_files(chapter_files)
    rewrite_paths(chapter_files)

    subprocess.run(["python3", str(ROOT / "scripts" / "update_nav.py")], check=True)
    rewrite_readme()

    print(f"restructured_chapters={len(chapter_files)}")


if __name__ == "__main__":
    main()
