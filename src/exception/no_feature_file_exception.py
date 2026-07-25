"""
没有特征文件异常
"""


class NoFeatureFileException(Exception):
    def __init__(self, message="没有找到特征文件"):
        self.message = message
        super().__init__(message)
