import os
from utils.builder import HighlySecureFlutterDocsBuilder
from utils.config import Config

def main():
    """執行超安全 Flutter 文件建構程式。"""
    builder = HighlySecureFlutterDocsBuilder()
    builder.build()

if __name__ == "__main__":
    main()