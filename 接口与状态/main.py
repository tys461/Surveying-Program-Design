from abc import ABC, abstractmethod

class Executable(ABC):
    @abstractmethod
    def run(self): pass

    @abstractmethod
    def is_ready(self) -> bool: pass   # 参数是否存在