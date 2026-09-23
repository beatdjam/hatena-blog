#!/usr/bin/env python3
"""ローカルの blog.css / mobile.css で本番ページをプレビューする。

はてなブログの CSS は
  PC   : usercss (テーマ + デザインCSS) の先頭で blog.css を @import
  SP   : 記事上フリースペースの <style> で mobile.css を @import（さらに blog.css を @import）
という読み込み順になっている。カスケード順が変わると見え方も変わるため、
本番の HTML / CSS を取得したうえで blog.css・mobile.css の該当部分だけを
ローカルの内容に差し替えて出力する。

使い方:
    python3 preview.py                # トップページ（PC / SP）
    python3 preview.py <記事URL>      # 指定ページ（PC / SP）

出力先は ./preview/ 。生成物は .gitignore 済み。
"""

import pathlib
import re
import sys
import urllib.request
import webbrowser

BLOG_URL = "https://blog.beatdjam.com/"
BLOG_CSS_URL = "https://beatdjam.github.io/hatena-blog/blog.css"
MOBILE_CSS_URL = "https://beatdjam.github.io/hatena-blog/mobile.css"

UA_PC = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
UA_SP = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "preview"


def fetch(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    return urllib.request.urlopen(req).read().decode("utf-8", "ignore")


def build_pc(url, blog_css):
    """PC版: usercss を取得し、先頭の blog.css @import をローカル内容に展開する。"""
    html = fetch(url, UA_PC)
    m = re.search(r'href="(https://usercss\.blog\.st-hatena\.com[^"]*)"', html)
    if not m:
        sys.exit("usercss のリンクが見つからない。テンプレートが変わったかも")

    usercss = fetch(m.group(1), UA_PC)
    usercss = usercss.replace(f'@import "{BLOG_CSS_URL}";', "")
    # @charset はファイル先頭にしか置けないため、展開後に付け直す
    usercss = usercss.replace('@charset "utf-8";', "")
    (OUT / "usercss-local.css").write_text(
        '@charset "utf-8";\n' + blog_css + "\n" + usercss
    )

    html = html.replace(m.group(1), "usercss-local.css")
    return html


def build_sp(url, blog_css):
    """SP版: mobile.css の @import をローカル内容に差し替える。"""
    html = fetch(url, UA_SP)
    mobile_css = (ROOT / "mobile.css").read_text()
    mobile_css = mobile_css.replace(f'@import url("{BLOG_CSS_URL}");', blog_css)
    (OUT / "mobile-local.css").write_text(mobile_css)

    replaced = html.replace(
        f'@import url("{MOBILE_CSS_URL}");', '@import url("mobile-local.css");'
    )
    if replaced == html:
        print("警告: mobile.css の @import が見つからなかった", file=sys.stderr)
    return replaced


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else BLOG_URL
    OUT.mkdir(exist_ok=True)
    blog_css = (ROOT / "blog.css").read_text()

    pc = OUT / "pc.html"
    sp = OUT / "sp.html"
    pc.write_text(build_pc(url, blog_css))
    sp.write_text(build_sp(url, blog_css))

    print(f"{url}\n  PC: {pc}\n  SP: {sp}")
    print("SP版は開発者ツールのデバイスモードで幅を絞ると実機に近くなる")
    for path in (pc, sp):
        webbrowser.open(path.as_uri())


if __name__ == "__main__":
    main()
