import os
from typing import Any, Dict, Optional
from fastapi import Request
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

def render(request: Request, name: str, context: Optional[Dict[str, Any]] = None, status_code: int = 200):
    if context is None:
        context = {}
    return templates.TemplateResponse(request=request, name=name, context=context, status_code=status_code)

