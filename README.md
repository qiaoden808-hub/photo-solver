# 拍照解题 App (Photo Solver App)

面向小学生的全科拍照解题 App。拍照上传题目，AI Vision API 识别并解答。

## 技术栈
- **前端**: Vue 3 (Vite)
- **后端**: Python FastAPI
- **AI API**: OpenAI 兼容接口（GPT-4 Vision 等）

## 项目结构
```
photo-solver/
├── ARCHITECTURE.md
├── README.md
├── backend/
│   ├── main.py           # FastAPI 入口, 6 个端点
│   ├── models.py         # Pydantic 模型
│   ├── solver.py         # AI Vision API 调用 + 提示词
│   ├── storage.py        # 解题历史 (JSON 持久化)
│   ├── config.py         # API Key 配置管理
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.vue            # 根组件, 页面路由
    │   ├── composables/
    │   │   └── useApi.js      # API 封装
    │   └── components/
    │       ├── HomePage.vue       # 首页: 拍照/相册入口
    │       ├── CameraCapture.vue  # 摄像头 + 相册上传
    │       ├── ImagePreview.vue   # 图片预览 + 提交
    │       ├── SolvingView.vue    # 解题等待动画
    │       ├── SolutionView.vue   # 分步骤解题展示
    │       ├── HistoryList.vue    # 历史记录
    │       └── SettingsPage.vue   # API 配置
    └── (config files)
```

## 快速启动

### 1. 启动后端
```bash
cd photo-solver/backend
pip install -r requirements.txt
python main.py
# 服务运行在 http://localhost:8000
```

### 2. 启动前端
```bash
cd photo-solver/frontend
npm install
npm run dev
# 前端运行在 http://localhost:5173
```

### 3. 配置 API Key
打开前端 → 点击右上角 ⚙️ → 输入 OpenAI API Key → 保存

支持任何 OpenAI 兼容的 API（兼容 GPT-4 Vision / Claude API 等），在设置中可修改 Endpoint 和 Model。

## 使用流程
1. 首页点击「拍题」或「从相册选择」
2. 拍照或选择题目图片
3. 点击「提交解题」
4. AI 老师识别题目并分步骤讲解
5. 查看解题过程和技巧

## API 端点
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/solve` | 上传图片解题 |
| GET | `/api/history` | 历史记录列表 |
| GET | `/api/history/{id}` | 单条记录详情 |
| DELETE | `/api/history/{id}` | 删除记录 |
| POST | `/api/config` | 保存 API 配置 |
| GET | `/api/config` | 获取配置状态 |
