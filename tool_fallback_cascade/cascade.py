"""Cascade orchestrator trying handlers in sequence."""
from typing import List, Callable, Any, Dict, Optional


class FallbackCascade:
    def __init__(self, name: str):
        self.name = name
        self._handlers: List[Tuple[str, Callable[..., Any]]] = []

    def add_handler(self, name: str, handler: Callable[..., Any]):
        self._handlers.append((name, handler))

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        if not self._handlers:
            raise RuntimeError(f"No handlers registered in cascade '{self.name}'")

        errors = []
        for idx, (h_name, handler) in enumerate(self._handlers):
            try:
                result = handler(*args, **kwargs)
                return {
                    "success": True,
                    "handler_used": h_name,
                    "degraded": idx > 0,
                    "result": result,
                    "prior_errors": errors
                }
            except Exception as e:
                errors.append(f"{h_name}: {type(e).__name__}({e})")

        return {
            "success": False,
            "handler_used": None,
            "degraded": True,
            "result": None,
            "prior_errors": errors
        }
