# 应用计量经济学讲稿（网页版）

本目录已经是可直接发布到 GitHub Pages 的静态网站。

## 已包含的发布必需文件

- `index.html`：网站首页
- `chapters/`：章节页面
- `assets/`：样式、图片、PDF等资源
- `.nojekyll`：关闭 Jekyll 处理，避免静态资源路径问题
- `.github/workflows/deploy-pages.yml`：自动发布到 GitHub Pages

## 直接发布步骤（上传后即可部署）

1. 将当前文件夹全部内容上传到 GitHub 仓库（默认分支 `main` 或 `master`）。
2. 打开仓库 `Settings -> Pages`：
   - `Build and deployment` 选择 `Source: GitHub Actions`（首次通常只需设置一次）。
3. 回到仓库 `Actions` 页面，等待 `Deploy Book To GitHub Pages` 工作流完成。
4. 访问工作流输出中的 `page_url` 即可在线阅读。

## 后续更新

- 只要推送新提交到 `main/master`，Pages 会自动重新部署。
- 若你增删章节文件，先运行：

```bash
python3 scripts/update_nav.py
```

再提交推送即可。
