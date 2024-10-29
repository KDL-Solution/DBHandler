from abc import ABC, abstractmethod


class FileHandler(ABC):
    @abstractmethod
    def put_data(self, img, annots, idx):
        pass

    @abstractmethod
    def get_data(self, idx):
        pass

    @abstractmethod
    def get_length(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __del__(self):
        pass
