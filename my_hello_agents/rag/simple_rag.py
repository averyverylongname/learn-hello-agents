import re
from pathlib import Path
from typing import Any, Dict, List


class SimpleRAGIndex:
    def __init__(
        self,
        base_dir: str = ".",
        chunk_size: int = 300,
        chunk_overlap: int = 50
    ):
        self.base_dir = Path(base_dir).resolve()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunks: List[Dict[str, Any]] = []

    def build_from_dir(self, dir_path: str):
        target_dir = (self.base_dir / dir_path).resolve()

        if not self._is_safe_path(target_dir):
            raise ValueError("不允许加载 base_dir 之外的目录")

        if not target_dir.exists():
            raise FileNotFoundError(f"目录不存在：{dir_path}")

        for file_path in target_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in [".txt", ".md"]:
                self.add_file(str(file_path.relative_to(self.base_dir)))

    def add_file(self, path: str):
        file_path = (self.base_dir / path).resolve()

        if not self._is_safe_path(file_path):
            raise ValueError("不允许加载 base_dir 之外的文件")

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在：{path}")

        text = file_path.read_text(encoding="utf-8")

        for index, chunk_text in enumerate(self._split_text(text), start=1):
            self.chunks.append({
                "source": path,
                "chunk_id": index,
                "text": chunk_text
            })

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        results = []

        for chunk in self.chunks:
            score = self._score(query, chunk["text"])

            if score > 0:
                results.append({
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "score": score,
                    "text": chunk["text"]
                })

        results.sort(key=lambda item: item["score"], reverse=True)

        return results[:top_k]

    def _split_text(self, text: str) -> List[str]:
        text = text.strip()

        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

            if start < 0:
                start = 0

            if start >= len(text):
                break

        return chunks

    def _score(self, query: str, text: str) -> int:
        query_lower = query.lower()
        text_lower = text.lower()

        score = 0

        if query_lower in text_lower:
            score += 5

        terms = self._extract_terms(query_lower)

        for term in terms:
            if term in text_lower:
                score += 2

        # 对中文问题做一个简单兜底：按单字重合计分
        chinese_chars = re.findall(r"[\u4e00-\u9fff]", query)
        for char in chinese_chars:
            if char in text:
                score += 1

        return score

    def _extract_terms(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9_\-]+|[\u4e00-\u9fff]{2,}", text)

    def _is_safe_path(self, path: Path) -> bool:
        try:
            path.relative_to(self.base_dir)
            return True
        except ValueError:
            return False