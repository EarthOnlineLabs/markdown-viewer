# Markdown Viewer

> 一个**单文件**的 Markdown 美化阅读器。零构建、零后端，一个 `md-viewer.html` 打开即用。
> A single-file, zero-build Markdown reader. Open the file — that's the whole app.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
&nbsp;Built by [EarthOnline](https://earthonline.site)

线上体验 / Live: **https://md.earthonline.site**

---

## 功能

- **两套阅读样式**（工具栏右上角切换，记忆在 `localStorage`，刷新不闪烁）
  - **光谱**（默认）— 取自 AISelf 设计规范：纯白纸底 + 宋体阅读 + 苹方界面，墨为底、彩虹色作边框/点缀。
  - **经典蓝** — 原始蓝色样式，保留为可选主题。
- **多种打开方式**：拖放 / 点击选择文件、粘贴路径或 URL、**从剪贴板粘贴**、粘贴文本框、直接 `Cmd/Ctrl+V`。
- **手机可用（PWA）**：可「添加到主屏幕」安装；Android 支持从微信/飞书 **分享 → Markdown Viewer** 直接打开 md 文件；含离线缓存。
- **目录（TOC）**：≥3 个标题自动生成左侧栏 + 滚动高亮，可折叠。
- **GitHub 链接**自动转 raw 加载；**本地文件**配合本地服务按绝对路径读取。
- **图片**：拖入文件夹自动解析相对路径图片，或手动填目录。
- **复制**为富文本 + 纯文本；内置 **A4 打印**样式（代码块/表头自动转浅底省墨）。

## 📱 手机上在微信 / 飞书收到 md 文件怎么打开？

微信/飞书不渲染 Markdown，把内容送进本工具有三条路：

- **通用（含 iOS）· 复制文本**：在微信/飞书点开该 md → **全选复制** → 回到本页点 **「从剪贴板粘贴」**。
- **Android · 分享**：把本页 **添加到主屏幕** 安装后，对文件选 **分享 → Markdown Viewer** 直接打开。
- **iOS · 存到「文件」**：对文件选 **「存储到‘文件’」**，回到本页用 **「打开文件」** 选择。

> iOS 不支持网页接收"分享来的文件"，所以 iOS 走"复制文本"或"存到文件"两条路；Android 额外支持系统分享直达。

## 两套样式

| | 光谱（默认 `aiself`） | 经典蓝（`classic`） |
|---|---|---|
| 纸底 | 纯白 `#FFFFFF` | `#faf9f7` |
| 阅读 / 界面字体 | 宋体·Noto Serif SC / 苹方 | Noto Serif SC / Inter |
| 强调色 | 五段光谱，仅作边框/点缀 | 蓝 `#2563eb` |
| 引用块 / 徽章 | 描边卡片 / 描边式 | 蓝色填充 / 填充式 |
| 代码块 / 分隔线 | 浅底描边 / 彩虹渐变 | 浅底描边 / 灰线 |

设计原则：**墨为底、色作点缀；用边框，不用大面积色块。**

## 本地使用

```bash
./mdview                 # 启动本地服务并打开浏览器
./mdview path/to/file.md # 启动并直接打开指定文件
# 或
python3 server.py [file.md]
```

本地服务监听 `http://127.0.0.1:9274/`，提供：
- `/api/read?path=<绝对路径>` — 读取本地 Markdown（带 CORS，便于线上版回连本地）。
- `/manifest.webmanifest`、`/sw.js`、`/favicon.svg`、`/icons/*` — 本地与线上 PWA 行为一致。

## 部署

托管在 Vercel（团队 `earthonlinedevs-projects`，项目 `md-viewer`），自定义域名 `md.earthonline.site`（备用 `md-viewer-theta.vercel.app`）。

```bash
vercel deploy --prod --yes      # CLI 直接发布
# 或：连上本仓库后 push 到 main 自动部署（Vercel Git Integration）
```

`vercel.json` 将 `/` 重写到 `/md-viewer.html`，并给 `sw.js` 设 no-cache。

## 设计来源

光谱样式的视觉规范来源于 AISelf 的 `design-exploration`（设计令牌、∞ 光谱标记、配色叙事）。修改光谱样式前请先对齐该规范，不要自创色值。

## 文件结构

```
md-viewer.html        主体（HTML + CSS + JS 全部内联）
manifest.webmanifest  PWA 清单（含 share_target / file_handlers）
sw.js                 Service Worker（离线缓存 + 接收分享）
favicon.svg           站点图标（∞ 光谱标记）
icons/                PWA 图标（192/512/maskable/apple + 源 SVG）
server.py             本地阅读服务（/api/read + 静态资源）
mdview                启动脚本
vercel.json           Vercel 重写规则与响应头
```

## 贡献

欢迎 issue / PR。本项目刻意保持**单文件、零依赖**（仅 CDN 引入 `marked`）——新功能请优先以纯 HTML/CSS/JS 内联实现，避免引入构建步骤。

## License

[MIT](LICENSE) © 2026 EarthOnline
