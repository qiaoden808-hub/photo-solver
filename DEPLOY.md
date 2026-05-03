# 部署指南

## 一、推送到 GitHub

### 初始化本地仓库
```bash
cd D:\AI\photo-solver
git init
git add -A
git commit -m "Initial commit: Photo Solver App"
```

### 创建 GitHub 仓库
打开 https://github.com/new
- Repository name：`photo-solver`
- 选 Public
- **不要**勾选 README、.gitignore、license
- 点 Create repository

### 推送
```bash
git remote add origin https://github.com/qiaoden808-hub/photo-solver.git
git branch -M main
git push -u origin main
```

---

## 二、部署后端到 Vercel

1. 打开 https://vercel.com → 点 Import
2. 选 GitHub → 授权并选 `photo-solver` 仓库
3. Root Directory 设为 `backend`
4. 点 Deploy
5. 部署完成后得到后端地址，比如 `https://photo-solver-xxx.vercel.app`

---

## 三、部署前端到 Vercel

1. 回到 Vercel 首页 → Add New → Project
2. 再次选 `photo-solver` 仓库
3. Root Directory 设为 `frontend`
4. Framework Preset 选 Vite
5. Build Command：`npm run build`
6. Output Directory：`dist`
7. 点 Deploy
8. 得到前端地址，比如 `https://photo-solver-app.vercel.app`

---

## 四、装到手机上

1. 安卓手机用 Chrome 打开前端地址
2. 底部会出现「安装应用」横幅，点击安装
3. 桌面出现 App 图标，点击全屏打开

---

## 五、配置

打开 App → 点右上角 ⚙️ → 填入：

- **Backend URL**：第二步得到的后端地址
- **API Key**：你的 Gemini Key（`AIzaSy...`）
- **Model**：`gemini-3-flash-preview`
- 保存

---

## 之后每次修改代码

```bash
cd D:\AI\photo-solver
git add -A
git commit -m "修改说明"
git push
```

Vercel 会自动重新部署。

---

## 本地测试

双击 `start.bat` 一键启动。
