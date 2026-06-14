# Markdown Viewer

> 一个**单文件**的 Markdown 美化阅读器。零构建、零后端，一个 `md-viewer.html` 打开即用。
> A single-file, zero-build Markdown reader. Open the file — that's the whole app.

[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](LICENSE)
&nbsp;Built by [EarthOnline](https://earthonline.site)

线上体验 / Live: **https://md.earthonline.site**

---

## 功能

- **光谱阅读样式**：取自 AISelf 设计规范——纯白纸底 + 宋体阅读 + 苹方界面，**墨为底、彩虹色只作边框/点缀**（标题圆点、引用左条、徽章描边、彩虹分隔线、深色代码块改为浅底描边）。
- **多种打开方式**：点击 / 拖放选择文件、粘贴路径或 URL、粘贴 Markdown 文本（先试读剪贴板，失败再展开文本框）。
- **手机可用（PWA）**：可「添加到主屏幕」安装；Android 支持从微信/飞书 **分享 → Markdown Viewer** 直接打开 md；含离线缓存。
- **目录（TOC）**：≥3 个标题自动生成左侧栏 + 滚动高亮，可折叠。
- **GitHub 链接**自动转 raw 加载；**本地文件**配合本地服务按绝对路径读取。
- **图片**：拖入文件夹自动解析相对路径图片，或手动填目录。
- **复制**为富文本 + 纯文本；内置 **A4 打印**样式（代码块/表头自动转浅底省墨）。

## 📱 手机上在微信 / 飞书收到 md 文件怎么打开？

微信/飞书移动端基本不渲染 Markdown（飞书新版能渲染但样式很普通），所以**走文件**最稳：

- **iOS / 通用**：在微信/飞书里点开该 md → 选 **「用其他应用打开」** → **存到「文件」** → 回本页点 **「打开 Markdown 文件」** 选它。
- **Android**：把本页 **添加到主屏幕** 安装后，对文件选 **分享 → Markdown Viewer** 直接打开（PWA share target / 打开方式）。

> 注意：iOS 不支持网页接收"分享来的文件"，且文件框**不能设 `accept`**（否则「文件」App 会把 `.md` 置灰、选不中）——本项目已据此处理。本工具的价值是"打开后好看"，不抢"能不能打开"。

## 样式与设计原则

只有一套 **光谱** 样式：纯白 `#FFFFFF` 纸底、墨色 `#1B1B1B` 结构、宋体/苹方/JetBrains Mono/Fraunces 字体；五段光谱（紫→蓝→绿→橙→红）只以**边框、小圆点、渐变细线**等点缀形式出现。

设计原则：**墨为底、色作点缀；用边框，不用大面积色块。** 视觉规范来源见下方「设计来源」。

## Logo

- **产品 logo** = 彩虹「**MD**」字标（工具栏 / 落地页 / favicon / PWA 图标）。
- **彩虹无限符号 ∞** = **EarthOnline 的 logo**，仅出现在页脚 "Built by ∞ EarthOnline"。
- 两者统一使用**硬边五段光谱**（紫→蓝→绿→橙→红），保持品牌一致。改图标见「文件结构」下的 `icons/`。

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
# 或：push 到 main 自动部署（已连 Vercel Git Integration）
```

`vercel.json` 将 `/` 重写到 `/md-viewer.html`，并给 `sw.js` 设 no-cache。

## 设计来源

光谱样式的视觉规范来源于 AISelf 的 `design-exploration`（设计令牌、配色叙事）。修改样式前请先对齐该规范，不要自创色值。

## 文件结构

```
md-viewer.html        主体（HTML + CSS + JS 全部内联）
manifest.webmanifest  PWA 清单（含 share_target / file_handlers）
sw.js                 Service Worker（离线缓存 + 接收分享）
favicon.svg           站点图标（方型彩虹「MD」，浏览器标签页用）
favicon.ico           标签页图标兜底（16/32，老浏览器 / 自动请求 /favicon.ico）
icons/                PWA 图标（192/512/maskable/apple）+ favicon-16/32.png + 源 SVG，均为彩虹「MD」
server.py             本地阅读服务（/api/read + 静态资源）
mdview                启动脚本
vercel.json           Vercel 重写规则与响应头
```

## 贡献

欢迎 issue / PR。本项目刻意保持**单文件、零依赖**（仅 CDN 引入 `marked`）——新功能请优先以纯 HTML/CSS/JS 内联实现，避免引入构建步骤。

## License

[MIT](LICENSE) © 2026 EarthOnline
