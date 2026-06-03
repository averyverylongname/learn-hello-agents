import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4


class JsonMemoryStore:
    def __init__(self, file_path: str = "examples/data/memory.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def add(self, content: str, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
        memories = self._load()

        item = {
            "id": str(uuid4()),
            "content": content,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(timespec="seconds")
        }

        memories.append(item)
        self._save(memories)

        return item

    def list_all(self) -> List[Dict[str, Any]]:
        return self._load()

    def search(self, keyword: str) -> List[Dict[str, Any]]:
        memories = self._load()
        keyword_lower = keyword.lower()

        return [
            item for item in memories
            if keyword_lower in item["content"].lower()
        ]

    def _load(self) -> List[Dict[str, Any]]:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _save(self, memories: List[Dict[str, Any]]):
        self.file_path.write_text(
            json.dumps(memories, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )