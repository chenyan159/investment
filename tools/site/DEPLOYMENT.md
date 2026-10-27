# Project Ananta 发布

公开站点：https://projectananta.com/ 。GitHub Pages 从 chenyan159/projectananta-research 的 main 分支 /docs 发布。域名注册与 DNS 由 Cloudflare 保留，网站部署不更改 DNS，也不需要 Tunnel。

## 检查仓库

本机 tools/site/.git 指向独立的发布仓库，发布仓库只跟踪 docs/。源码与研究侧清理由 D:\investment 根仓库保存；从其他电脑克隆根仓库后，需要另外配置发布仓库，不能把研究根仓库当作站点部署仓库。

```powershell
cd D:\investment\tools\site
git rev-parse --show-toplevel
git remote get-url origin
git branch --show-current
git fetch origin main
git rev-list --left-right --count main...origin/main
git status --short
```

确认工作目录为 tools/site、远端为 https://github.com/chenyan159/projectananta-research.git 、分支为 main。远端如有新提交先处理分歧，不重置或强制覆盖。源码开发变更由根仓库独立检查与提交。

## 构建与发布

```powershell
npm test
npm run pages:prepare
node etl/validate-data.mjs --dir=docs/data
npm run verify:publish
git add -A -- docs
git diff --cached --stat
git commit -m "Update Project Ananta research workspace"
git push origin main
```

确认暂存文件全部属于 docs/。禁止手工改生成 JSON 或向发布仓库加入研究运行器、凭据与运行状态。构建输入仅限 README 指明的五个研究目录。

## 线上验收

GitHub Pages 完成部署后执行：

```powershell
node qa/verify-publish.mjs --origin=https://projectananta.com
```

校验主页、索引、元数据和入口 JS/CSS 与本地产物 SHA-256 一致；还应在浏览器检查公司选择、情景切换、公司对比、全文阅读与移动布局。收到 HTTP 200 但仍为旧内容不能算发布成功，等待 Pages/CDN 更新后重试。

## 域名与回滚

- 保持 public/CNAME 与 docs/CNAME 为 projectananta.com，GitHub Pages 自定义域名保持相同值。
- Cloudflare 的根域名 A/AAAA 和 www CNAME 继续指向 GitHub Pages，保持现有 DNS-only 设置。本项目的构建与发布不管理这些记录。
- 发布前记录站点提交与根仓库源码提交。需要回滚时用新的 Git revert 提交恢复发布包，再推送并复验；不要强制推送或删除域名。
- 2026-10-26 重做前的源码/发布提交及旧网站专用文件归档在 备份/projectananta重做_2026-10-26/，归档不作为构建来源。
