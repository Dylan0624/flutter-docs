import os
import re
import json
import markdown
from utils.encryption import Encryption


class MarkdownProcessor:
    @staticmethod
    def extract_order_from_filename(filename):
        """從文件名中提取順序號。"""
        match = re.match(r'^(\d+)', filename)
        return int(match.group(1)) if match else 999

    @staticmethod
    def extract_title_from_content(content):
        """從 Markdown 內容中提取標題。"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):  # 修正：移除多餘的括號
                return line[2:].strip()
        return None

    @staticmethod
    def read_markdown_files(content_dir, secret_password):
        """從目錄讀取並處理 Markdown 文件。"""
        files_content = {}
        if not os.path.exists(content_dir):
            print(f"❌ Error: Directory {content_dir} not found")
            return files_content

        try:
            md_files = [f for f in os.listdir(content_dir) if f.endswith('.md')]
            md_files.sort(key=lambda x: MarkdownProcessor.extract_order_from_filename(x))

            for filename in md_files:
                filepath = os.path.join(content_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                except (IOError, UnicodeDecodeError) as e:
                    print(f"❌ Error reading {filename}: {str(e)}")
                    continue

                # 修正：使用 MarkdownProcessor.extract_title_from_content
                title = MarkdownProcessor.extract_title_from_content(content)
                if not title:
                    title = re.sub(r'^\d+\.\s*', '', filename.replace('.md', '').replace('_', ' ')).title()

                if filename == 'secrets.md':
                    encrypted_content = Encryption.advanced_encrypt(content, secret_password)
                    files_content[filename] = {
                        'title': '',  # 修正：secrets 檔案的 title 為空
                        'original_title': title,
                        'content': content,
                        'encrypted_content': encrypted_content,
                        'is_encrypted': True,
                        'is_hidden': True,
                        'order': MarkdownProcessor.extract_order_from_filename(filename)  # 修正：加上類別名稱
                    }
                    print(f"🔒 Encrypted secrets content from {filename}")
                    print(json.dumps(files_content[filename], indent=2, ensure_ascii=False))
                else:
                    html_content = markdown.markdown(content, extensions=['codehilite', 'fenced_code'])
                    files_content[filename] = {
                        'title': title,  # 修正：一般檔案的 title 應該是 title 而不是 content
                        'content': html_content,
                        'is_encrypted': False,
                        'order': MarkdownProcessor.extract_order_from_filename(filename)  # 修正：加上類別名稱
                    }
        except Exception as e:
            print(f"❌ Error processing directory {content_dir}: {str(e)}")

        return files_content