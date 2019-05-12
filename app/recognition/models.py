from typing import List, Optional, Dict


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

    def serizalize(self) -> Dict:
        return {
            'userId': self.user_id
        }


class EncodingsResult:
    def __init__(self, file_paths: List[str]) -> None:
        self.file_paths = file_paths

    def serialize(self) -> Dict:
        return {
            'files': self.file_paths
        }
