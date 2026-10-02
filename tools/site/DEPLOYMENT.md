# Investment Research Site Deployment

站点通过 GitHub Pages 发布，`docs/` 是发布目录，Cloudflare 只用于域名注册和 DNS。

## 公开入口

- `https://projectananta.com/`
- `https://chenyan159.github.io/projectananta-research/`

## 发布

```powershell
cd "D:\investment\tools\site"
npm run pages:prepare
git status --short
git add .
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
