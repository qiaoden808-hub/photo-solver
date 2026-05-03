from pydantic import BaseModel


class SolveRequest(BaseModel):
    image: str  # base64 encoded image
    filename: str = "photo.jpg"


class SolutionStep(BaseModel):
    step: int
    title: str
    content: str


class SolveResponse(BaseModel):
    id: str
    problem: str           # AI 提取的题目文本
    subject: str           # 科目分类（数学/语文/英语/科学/其他）
    solution: list[SolutionStep]
    tips: str = ""         # 解题小技巧
    created_at: str


class HistoryItem(BaseModel):
    id: str
    problem: str
    subject: str
    created_at: str


class ApiConfig(BaseModel):
    api_key: str = ""
    endpoint: str = "https://api.openai.com/v1"
    model: str = "gpt-4o"
