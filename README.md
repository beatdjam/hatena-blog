# hatena-blog

[B-Teck!](https://blog.beatdjam.com/) のスタイル。GitHub Pages 経由で配信している。

| ファイル | 読まれ方 |
|---|---|
| `blog.css` | PC版。デザインCSSの先頭で `@import`。テーマCSSより**先**に読まれるため、テーマの指定を上書きするには `!important` が必要 |
| `mobile.css` | スマートフォン版。記事上フリースペースの `<style>` から `@import`。冒頭で `blog.css` も読む。touchテーマ（`normal.css`）より**後**に読まれる |

スマートフォン版は PC 版と DOM・クラス体系が別（`#blog-title` ではなく `.header-image`、
`#container`/`#box2` は無い等）なので、PC版のID指定は空振りする。
touch 版固有の配色は `mobile.css` 側に書く。

ダークモードは両ファイルの `@media (prefers-color-scheme: dark)` ブロック。
色はブロック先頭の `--dm-*` 変数にまとめてある。

## プレビュー

本番のHTMLを取得し、`blog.css` / `mobile.css` だけローカルの内容に差し替えて表示する
（読み込み順＝カスケードは本番と同じ）。

```sh
python3 preview.py                  # トップページ
python3 preview.py <記事URL>        # 指定ページ
```

PC版・SP版が1枚ずつブラウザで開く。OSのダークモードを切り替えて確認する。

## 反映

master に push すると GitHub Pages 経由で本番に反映される。
CDN キャッシュがあるので、すぐ変わらなければスーパーリロードで確認する。
