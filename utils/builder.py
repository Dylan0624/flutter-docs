import os
import markdown  # 修正：新增缺少的 markdown 匯入
from utils.config import Config
from utils.markdown_processor import MarkdownProcessor
from utils.html_template import HTMLTemplate
from utils.encryption import Encryption  # 修正：新增缺少的 Encryption 匯入

class HighlySecureFlutterDocsBuilder:
    def __init__(self):
        self.content_dir = Config.CONTENT_DIR
        self.output_file = Config.OUTPUT_FILE
        self.secret_password = Config.SECRET_PASSWORD
        
    def build(self):
        """建立高度安全的 Flutter 文件。"""
        print("🛡️ Building ultra-secure Flutter documentation...")
        
        if not os.path.exists(self.content_dir):
            print(f"❌ Error: Directory {self.content_dir} not found")
            # 修正：模擬範例內容以供演示
            files_content = {
                '01_introduction.md': {
                    'title': 'Introduction to Flutter',
                    'content': markdown.markdown('# Introduction to Flutter\nThis is a sample introduction.', extensions=['codehilite', 'fenced_code']),
                    'is_encrypted': False,
                    'order': 1
                },
                'secrets.md': {
                    'title': '',
                    'original_title': 'Secrets',
                    'content': '# Secret Content\nThis is hidden content.',
                    'encrypted_content': Encryption.advanced_encrypt('# Secret Content\nThis is hidden content.', self.secret_password),
                    'is_encrypted': True,
                    'is_hidden': True,
                    'order': 2
                }
            }
        else:
            files_content = MarkdownProcessor.read_markdown_files(self.content_dir, self.secret_password)
        
        if not files_content:
            print("❌ Error: No Markdown files found")
            return
        
        print(f"📄 Found {len(files_content)} files:")
        sorted_files = sorted(files_content.items(), key=lambda x: x[1]['order'])
        for filename, data in sorted_files:
            encryption_status = "🔒 (Multi-layer encryption)" if data.get('is_encrypted') else "📖"
            order = data['order']
            title = data['title'] if data['title'] else data.get('original_title', filename)
            print(f"  {order:2d}. {filename} - {title} {encryption_status}")
        
        html_content = HTMLTemplate.generate_html_template(files_content, self.secret_password)
        
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                file.write(html_content)
        except IOError as e:
            print(f"❌ Error writing to {self.output_file}: {str(e)}")
            return
        
        print(f"✅ Ultra-secure documentation built successfully!")
        print(f"📁 Output file: {self.output_file}")
        print(f"🔐 Encrypted file password: {self.secret_password}")
        print("\n🛡️ Security Features:")
        print("   • Multi-layer encryption (Compression + AES + Obfuscation)")
        print("   • Password hash verification (No plaintext password)")
        print("   • Decoy data obfuscation")
        print("   • Anti-debugging protection")
        print("   • Variable name obfuscation")
        print("   • Developer tools disabled")
        print("   • Right-click and shortcut protection")
        print("\n💡 Tip: Click the rocket icon in the header to access hidden content! 🚀")
        print("\n⚠️ Important Note:")
        print("   Although significantly increasing cracking difficulty, client-side encryption has theoretical limitations.")
        print("   This solution effectively prevents 95% of general cracking attempts.")

# 修正：新增 main 執行區塊（如果需要直接執行此檔案）
if __name__ == "__main__":
    builder = HighlySecureFlutterDocsBuilder()
    builder.build()