#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from bs4 import BeautifulSoup
import re


def chapter_sort_key(path: Path):
    m = re.search(r"chapter-(\d+)", path.name)
    return int(m.group(1)) if m else 10**9


def first_h1_text(html_path: Path) -> str:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    h1 = soup.find("h1")
    return h1.get_text(" ", strip=True) if h1 else html_path.stem


def build_nav_html(chapters: list[tuple[Path, str]], href_prefix: str, current_name: str | None) -> BeautifulSoup:
    nav = BeautifulSoup('', 'html.parser')
    nav_tag = nav.new_tag("nav", attrs={"class": "chapter-nav", "aria-label": "章节导航"})
    h2 = nav.new_tag("h2")
    h2.string = "章节目录"
    nav_tag.append(h2)

    ul = nav.new_tag("ul")
    intro_idx = next((i for i, (_, t) in enumerate(chapters) if "引言" in t), 0)
    for idx, (ch, title) in enumerate(chapters, start=1):
        li = nav.new_tag("li")
        a = nav.new_tag("a", href=f"{href_prefix}{ch.name}")
        if current_name == ch.name:
            a["class"] = ["is-current"]
        chapter_no = idx - intro_idx
        if chapter_no >= 1:
            a.string = f"第{chapter_no}章：{title}"
        else:
            a.string = title
        li.append(a)
        ul.append(li)

    nav_tag.append(ul)
    nav.append(nav_tag)
    return nav


def upsert_root_nav(page_path: Path, chapters: list[tuple[Path, str]]):
    soup = BeautifulSoup(page_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    nav = soup.find("nav", class_="chapter-nav")
    new_nav = build_nav_html(chapters, "chapters/", None).find("nav")

    if nav:
        nav.replace_with(new_nav)
    else:
        body = soup.body
        if body:
            body.append(new_nav)

    page_path.write_text(str(soup), encoding="utf-8")


def upsert_chapter_nav(chapter_path: Path, chapters: list[tuple[Path, str]]):
    soup = BeautifulSoup(chapter_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    aside = soup.find("aside", class_="sidebar-nav")
    if aside is None:
        page_shell = soup.find("div", class_="page-shell")
        if page_shell is None and soup.body is not None:
            page_shell = soup.new_tag("div", attrs={"class": "page-shell"})
            for child in list(soup.body.find_all(recursive=False)):
                page_shell.append(child.extract())
            soup.body.append(page_shell)
        aside = soup.new_tag("aside", attrs={"class": "sidebar-nav"})
        if page_shell:
            page_shell.insert(0, aside)

    new_nav = build_nav_html(chapters, "", chapter_path.name).find("nav")
    old_nav = aside.find("nav", class_="chapter-nav")
    if old_nav:
        old_nav.replace_with(new_nav)
    else:
        aside.append(new_nav)

    # Ensure back-home link exists and correct.
    main = soup.find("main", class_="chapter-main")
    if main:
        back = main.find("p", class_="back-home")
        if back is None:
            back = soup.new_tag("p", attrs={"class": "back-home"})
            a = soup.new_tag("a", href="../index.html")
            a.string = "← 返回封面"
            back.append(a)
            main.insert(0, back)
        else:
            a = back.find("a")
            if a is None:
                a = soup.new_tag("a", href="../index.html")
                a.string = "← 返回封面"
                back.append(a)
            else:
                a["href"] = "../index.html"

    chapter_path.write_text(str(soup), encoding="utf-8")


def main():
    root = Path(__file__).resolve().parents[1]
    chapters_dir = root / "chapters"
    index_path = root / "index.html"
    module2_path = root / "cover-module-2.html"

    chapter_files = sorted(chapters_dir.glob("chapter-*.html"), key=chapter_sort_key)
    chapter_meta = [(ch, first_h1_text(ch)) for ch in chapter_files]

    if index_path.exists():
        upsert_root_nav(index_path, chapter_meta)
    if module2_path.exists():
        upsert_root_nav(module2_path, chapter_meta)

    for ch in chapter_files:
        upsert_chapter_nav(ch, chapter_meta)

    print(f"updated_nav_for={len(chapter_files)}")


if __name__ == "__main__":
    main()
