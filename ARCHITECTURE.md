# 拍照解题 App 架构设计

## 概述
面向小学生的全科拍照解题 App。用户拍照上传题目，后端调用 AI Vision API 识别并解答，返回步骤清晰的解题过程。

## 技术栈
- **前端**: Vue 3 (Vite) — 拍照/上传 + 解题展示
- **后端**: Python FastAPI — 图像处理 + AI API 集成
- **AI API**: OpenAI 兼容接口（支持 GPT-4 Vision / Claude API 等）

## 项目结构
```
photo-solver/
├── backend/
│   ├── main.py           # FastAPI 入口
│   ├── models.py         # Pydantic 数据模型
│   ├── solver.py         # AI API 调用 + 提示词工程
│   ├── storage.py        # 解题历史记录
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── components/
│   │   │   ├── HomePage.vue        # 首页（拍照/上传入口 + 使用说明）
│   │   │   ├── CameraCapture.vue   # 拍照 & 相册上传
│   │   │   ├── ImagePreview.vue    # 图片预览 + 提交
│   │   │   ├── SolvingView.vue     # 解题中动画
│   │   │   ├── SolutionView.vue    # 解题结果展示（分步骤）
│   │   │   └── HistoryList.vue     # 历史记录侧栏
│   │   └── composables/
│   │       └── useApi.js           # API 调用封装
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

## 数据流
```
[用户拍照/上传] → 前端预览图片 → POST /api/solve (base64)
    → 后端接收图片 → 调用 AI Vision API
    → AI 解析题目 → 返回解题步骤
    → 后端保存历史 → 返回结构化结果
    → 前端分步展示
```

## API 设计

### POST /api/solve
接收题目图片，返回解题结果。
- Request: `{"image": "base64_string", "filename": "photo.jpg"}`
- Response: 
```json
{
  "id": "uuid",
  "problem": "题目文本（AI 提取）",
  "subject": "数学/语文/...",
  "solution": [
    {"step": 1, "title": "理解题意", "content": "..."},
    {"step": 2, "title": "解题步骤", "content": "..."},
    {"step": 3, "title": "最终答案", "content": "..."}
  ],
  "tips": "解题小技巧",
  "created_at": "2026-05-01T..."
}
```

### GET /api/history
获取解题历史列表。

### DELETE /api/history/{id}
删除单条历史记录。

### POST /api/config
配置 AI API (API Key, Endpoint, Model)。
- Request: `{"api_key": "...", "endpoint": "...", "model": "..."}`
- Response: `{"status": "ok"}`

### GET /api/config
获取当前配置状态（隐藏 API Key）。

## AI 提示词设计
系统提示词面向小学生，要求：
1. 先识别题目类型（数学/语文/英语/科学等）
2. 用简单易懂的语言分步骤讲解
3. 每步都有详细解释
4. 最终给出清晰答案
5. 鼓励性语言，适合小学生理解
