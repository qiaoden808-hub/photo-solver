import json
import logging
import re

import httpx

import config as app_config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """你是一位非常有耐心、擅长用简单语言讲解的小学老师。你的任务是帮助小学生解答题目。

请仔细分析用户上传的图片中的题目，然后按以下步骤完成：

1. **识别题目类型**：判断题目属于哪个科目（数学、语文、英语、科学、其他）
2. **提取题目文本**：准确识别图片中的题目内容
3. **分步骤讲解**：用适合小学生理解的简单语言，把解题过程分成清晰的步骤
4. **给出最终答案**：在最后一步给出明确的答案
5. **提供解题小技巧**：分享一个记忆口诀或解题技巧

输出格式必须是严格的 JSON 格式（不要包含 markdown 代码块标记，直接返回纯 JSON）：

{
  "problem": "提取的题目文本",
  "subject": "数学/语文/英语/科学/其他",
  "solution": [
    {"step": 1, "title": "理解题目", "content": "..."},
    {"step": 2, "title": "分析问题", "content": "..."},
    {"step": 3, "title": "计算过程", "content": "..."},
    {"step": 4, "title": "得出答案", "content": "..."}
  ],
  "tips": "解题小技巧或记忆口诀"
}

要求：
- 步骤数量根据题目难度灵活调整（2-6步）
- 每步的 title 要简明扼要，反映该步骤的核心内容
- content 要详细解释，语言简单生动
- 遇到数学题要体现具体的计算过程
- tips 要实用、好记，可以是口诀或联想记忆法
- 步骤编号从1开始连续递增"""


def _is_gemini(api_key: str) -> bool:
    """Detect if the API key is a Google Gemini key."""
    return api_key.startswith("AIza") or "googleapis" in app_config.get_endpoint()


async def solve_problem(image_base64: str, filename: str) -> dict:
    """Call the AI Vision API to solve a problem from an image."""
    api_key = app_config.get_api_key()
    if not api_key:
        raise ValueError("API Key not configured")

    if _is_gemini(api_key):
        return await _solve_with_gemini(image_base64, filename)
    else:
        return await _solve_with_openai(image_base64, filename)


async def _solve_with_gemini(image_base64: str, filename: str) -> dict:
    """Call Google Gemini API to solve the problem."""
    api_key = app_config.get_api_key()
    model = app_config.get_model()
    if model == "gpt-4o":
        model = "gemini-3-flash-preview"  # default Gemini model

    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "png"
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                 "gif": "image/gif", "webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/png")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": [{
            "parts": [
                {"text": "请解答图片中的题目，并严格按照要求的JSON格式输出。"},
                {"inline_data": {"mime_type": mime_type, "data": image_base64}}
            ]
        }],
        "generationConfig": {
            "maxOutputTokens": 4096,
            "temperature": 0.3,
        }
    }

    logger.info(f"Calling Gemini API: {model}")

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
    except httpx.TimeoutException:
        raise RuntimeError("AI API request timeout")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"API error (HTTP {e.response.status_code}): {_extract_gemini_error(e.response)}")
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error: {str(e)}")

    try:
        content = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected Gemini response: {result}")
        raise RuntimeError("Failed to parse API response")

    return _parse_response(content)


async def _solve_with_openai(image_base64: str, filename: str) -> dict:
    """Call OpenAI-compatible API to solve the problem."""
    api_key = app_config.get_api_key()
    endpoint = app_config.get_endpoint().rstrip("/")
    model = app_config.get_model()

    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else "png"
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                 "gif": "image/gif", "webp": "image/webp"}
    media_type = mime_map.get(ext, "image/png")

    data_url = f"data:{media_type};base64,{image_base64}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": data_url, "detail": "high"}},
                {"type": "text", "text": "请解答图片中的题目，并严格按照要求的JSON格式输出。"},
            ]},
        ],
        "max_tokens": 4096,
        "temperature": 0.3,
    }

    url = f"{endpoint}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    logger.info(f"Calling OpenAI API at {url} with model {model}")

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
    except httpx.TimeoutException:
        raise RuntimeError("AI API request timeout")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"API error (HTTP {e.response.status_code}): {_extract_openai_error(e.response)}")
    except httpx.RequestError as e:
        raise RuntimeError(f"Network error: {str(e)}")

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        logger.error(f"Unexpected API response: {result}")
        raise RuntimeError("Failed to parse API response")

    return _parse_response(content)


def _parse_response(content: str) -> dict:
    """Parse and validate the AI response content."""
    try:
        parsed = _extract_json(content)
        _validate_solution(parsed)
        return parsed
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse AI response: {content}")
        raise RuntimeError(f"Response parse error: {str(e)}")


def _extract_gemini_error(response) -> str:
    try:
        body = response.json()
        return body.get("error", {}).get("message", str(response.text)[:200])
    except Exception:
        return str(response.text)[:200]


def _extract_openai_error(response) -> str:
    try:
        body = response.json()
        return body.get("error", {}).get("message", str(response.text)[:200])
    except Exception:
        return str(response.text)[:200]


def _extract_json(text: str) -> dict:
    """Try to extract a JSON object from the AI response text."""
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1).strip())
    json_match = re.search(r"\{[\s\S]*\}", text)
    if json_match:
        return json.loads(json_match.group(0).strip())
    return json.loads(text.strip())


def _validate_solution(parsed: dict):
    """Validate that the parsed solution has all required fields."""
    required = ["problem", "subject", "solution"]
    for field in required:
        if field not in parsed:
            raise ValueError(f"Missing field: {field}")
    if not isinstance(parsed["solution"], list):
        raise ValueError("solution must be an array")
    for i, step in enumerate(parsed["solution"]):
        if not isinstance(step, dict):
            raise ValueError(f"solution[{i}] must be an object")
        step["step"] = i + 1
        step.setdefault("title", f"Step {i+1}")
        step.setdefault("content", "")
    valid_subjects = {"数学", "语文", "英语", "科学", "其他"}
    if parsed["subject"] not in valid_subjects:
        parsed["subject"] = "其他"
    parsed.setdefault("tips", "")
