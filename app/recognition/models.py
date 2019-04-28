from typing import List, Optional


class Sample:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path


class BiometricPattern:
    def __init__(self, user_id: str, file_paths: List[str]) -> None:
        self.user_id = user_id
        self.file_paths = file_paths


class MatchResult:
    def __init__(self, user_id: Optional[str] = None) -> None:
        self.user_id = user_id
