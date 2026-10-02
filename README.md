# Investment

投资研究工作区，保存研究报告、研究方案、历史数据，以及研究运行器和网站源码。仓库用于版本管理、在线查阅，并为后续多电脑使用提供共同入口。

## 目录

- [基本面](基本面/)：公司、行业和特征量化研究。
- [分析报告](分析报告/)：公司情景决策、对比和排序。
- [金融资料](金融资料/)：新闻、行情、估值和每日金融快照。
- [技术面](技术面/)：因子研究、数据和脚本。
- [情绪面](情绪面/)：公司情绪和市场叙事。
- [tools](tools/)：研究运行器、共享队列和网站源码。
- [备份](备份/)：历史存档、迁移记录和一次性研究成果。

先阅读根目录 [AGENTS.md](AGENTS.md)，进入子目录后遵守该目录的说明。研究方案以现行入口为准，历史报告保留其原始日期和含义。

## 版本管理

本机直接使用 `D:\investment` 作为 [chenyan159/investment](https://github.com/chenyan159/investment) 的工作目录，Git 历史保存在根目录的 `.git/` 中。日常编辑、运行和提交都在同一个目录完成。

先检查改动，确认需要保存的文件已经写完，再提交和上传：

```powershell
git -C D:/investment status --short
git -C D:/investment add -A
git -C D:/investment commit -m "Update investment research"
git -C D:/investment push
```

文件修改后需要提交并推送才会出现在 GitHub；目前没有设置定时上传。多电脑使用时，开始工作前在工作区干净的情况下运行 `git pull --ff-only`，结束工作后提交并推送。

本机 `tools/site` 仍保留独立的网站发布仓库，指向 `chenyan159/projectananta-research`，只记录 `docs/` 发布包。在该子目录运行 Git 命令会操作网站发布仓库；整个项目的提交应从根目录执行，或像上面一样明确使用 `git -C D:/investment`。网站源码由根目录仓库正常跟踪，网站发布操作见 [DEPLOYMENT.md](tools/site/DEPLOYMENT.md)。

## 在其他电脑使用

```sh
git clone https://github.com/chenyan159/investment.git
cd investment
```

阅读报告不需要安装开发依赖。运行工具时，先安装 Node.js 22 或更新版本，再在需要使用的工具目录安装依赖：

```sh
npm --prefix tools/research-runner ci
npm --prefix tools/site ci
```

研究运行器的登录、队列和执行说明见 [Research Runner](tools/research-runner/README.md)；网站构建说明见 [Site](tools/site/README.md)。Python 研究脚本的依赖因任务而异，应按对应脚本和目录说明准备。

当前主要运行环境是 Windows，部分脚本和历史资料仍包含本机绝对路径。克隆仓库并不代表全部脚本已经完成跨平台适配；在新电脑启动研究或重建数据前，应先检查路径、依赖、登录状态和队列内容。

## 收录范围

仓库保留研究成果、方案、必要数据、源码、配置和依赖锁文件。`node_modules`、`tmp`、`_work`、缓存、日志和网站构建发布副本由 [.gitignore](.gitignore) 排除；不因排除而删除本地工具依赖。

`tools/site/public/data` 暂时保留，其中包含原始音频清理后仍需保存的发布资产。本机 `tools/site/.git` 指针不随本仓库上传或克隆；网站源码在本仓库中作为普通文件保存。其他电脑可以构建和预览网站，发布到现有站点前需另行配置网站发布仓库。

历史报告中的部分本地绝对链接不能直接在 GitHub 网页打开，可通过对应目录定位文件。敏感凭据和登录状态不随仓库分发，需要在每台电脑上单独配置。
