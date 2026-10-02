# Investment Research Site Deployment

站点通过 GitHub Pages 发布，`docs/` 是发布目录，Cloudflare 只用于域名注册和 DNS。

## 公开入口

- `https://projectananta.com/`
- `https://chenyan159.github.io/projectananta-research/`

## 发布

以下命令用于本机独立的网站发布仓库 `chenyan159/projectananta-research`。整个研究项目由根目录的 `chenyan159/investment` 仓库管理；从该仓库新克隆的目录没有本机的网站 `.git` 指针，需要先配置发布仓库。发布前先核对 Git 工作目录和远端，避免把发布提交送到研究项目仓库。

```powershell
cd "D:\investment\tools\site"
$siteRoot = (Get-Location).Path.Replace('\', '/')
$gitRoot = git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0 -or $gitRoot -ne $siteRoot) {
    throw "请先配置 tools/site 的独立网站发布仓库。"
}
$origin = git remote get-url origin
if ($LASTEXITCODE -ne 0 -or $origin -ne 'https://github.com/chenyan159/projectananta-research.git') {
    throw "当前远端不是预期的网站发布仓库。"
}
npm run pages:prepare
git status --short
git add -- docs
git commit -m "Update research dashboard"
git push
```

发布前检查 `public/data/meta.json` 和质量页面；不要手工修改 `public/data/`、`docs/` 或其中的生成 JSON。

GitHub Pages 应使用：

- Repository：`chenyan159/projectananta-research`
- Source：`main` 分支的 `/docs`
- Custom domain：`projectananta.com`
- HTTPS：证书可用后启用 `Enforce HTTPS`

## DNS

Cloudflare 中的 GitHub Pages 记录应保持 DNS-only：

```text
@    A      185.199.108.153
@    A      185.199.109.153
@    A      185.199.110.153
@    A      185.199.111.153
@    AAAA   2606:50c0:8000::153
@    AAAA   2606:50c0:8001::153
@    AAAA   2606:50c0:8002::153
@    AAAA   2606:50c0:8003::153
www  CNAME  chenyan159.github.io
```

域名或托管方式变更前，应先按 GitHub Pages 与 Cloudflare 当前官方要求重新核对这些记录。

## 维护边界

- 研究原文在 `D:\investment\基本面` 维护，站点只消费生成结果。
- 保持 `PROJECTANANTA.COM` 域名续费和 GitHub Pages 配置有效。
- 当前静态部署不需要 Cloudflare Tunnel、Access、Workers 或 R2；除非明确改变部署模型，不恢复旧 Tunnel 文件和启动脚本。
- 发布后检查主页和 `/data/meta.json` 是否可访问。
