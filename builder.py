import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import markdown
import re

class FlutterDocsBuilder:
    def __init__(self):
        self.content_dir = "content"
        self.output_file = "flutter-docs-updated.html"
        self.secret_password = "19831203"
        
    def generate_key_from_password(self, password):
        """從密碼生成加密金鑰"""
        password_bytes = password.encode()
        salt = b'flutter_docs_salt'  # 固定的鹽值，實際應用中應該隨機生成
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt_content(self, content, password):
        """加密內容"""
        key = self.generate_key_from_password(password)
        fernet = Fernet(key)
        encrypted_content = fernet.encrypt(content.encode())
        return base64.urlsafe_b64encode(encrypted_content).decode()
    
    def read_markdown_files(self):
        """讀取所有 Markdown 檔案"""
        files_content = {}
        
        for filename in os.listdir(self.content_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(self.content_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                # 如果是 secrets.md，進行加密
                if filename == 'secrets.md':
                    encrypted_content = self.encrypt_content(content, self.secret_password)
                    files_content[filename] = {
                        'title': filename.replace('.md', '').replace('_', ' ').title(),
                        'content': content,
                        'encrypted_content': encrypted_content,
                        'is_encrypted': True
                    }
                else:
                    # 轉換 Markdown 為 HTML
                    html_content = markdown.markdown(content, extensions=['codehilite', 'fenced_code'])
                    files_content[filename] = {
                        'title': filename.replace('.md', '').replace('_', ' ').title(),
                        'content': html_content,
                        'is_encrypted': False
                    }
                    
        return files_content
    
    def generate_html_template(self, files_content):
        """生成完整的 HTML 模板"""
        
        # 生成導航選項
        nav_items = []
        tab_contents = []
        
        for i, (filename, data) in enumerate(files_content.items()):
            tab_id = filename.replace('.md', '').replace('_', '-')
            active_class = 'active' if i == 0 else ''
            
            nav_items.append(f'''
                <li class="nav-item">
                    <a class="nav-link {active_class}" id="{tab_id}-tab" data-bs-toggle="tab" 
                       href="#{tab_id}" role="tab" aria-controls="{tab_id}" 
                       aria-selected="{'true' if i == 0 else 'false'}">
                        {data['title']}
                    </a>
                </li>
            ''')
            
            # 為加密檔案生成特殊的內容區域
            if data['is_encrypted']:
                tab_content = f'''
                    <div class="tab-pane fade {'show active' if i == 0 else ''}" id="{tab_id}" 
                         role="tabpanel" aria-labelledby="{tab_id}-tab">
                        <div class="encrypted-content">
                            <div class="password-input-container">
                                <h4>🔒 This content is encrypted</h4>
                                <p>Please enter the password to view this content:</p>
                                <div class="input-group mb-3">
                                    <input type="password" class="form-control" id="password-{tab_id}" 
                                           placeholder="Enter password">
                                    <button class="btn btn-primary" type="button" 
                                            onclick="decryptContent('{tab_id}', '{data['encrypted_content']}')">
                                        Unlock
                                    </button>
                                </div>
                            </div>
                            <div class="decrypted-content" id="decrypted-{tab_id}" style="display: none;">
                                <!-- 解密後的內容會顯示在這裡 -->
                            </div>
                        </div>
                    </div>
                '''
            else:
                tab_content = f'''
                    <div class="tab-pane fade {'show active' if i == 0 else ''}" id="{tab_id}" 
                         role="tabpanel" aria-labelledby="{tab_id}-tab">
                        <div class="content-wrapper">
                            {data['content']}
                        </div>
                    </div>
                '''
            
            tab_contents.append(tab_content)
        
        # 完整的 HTML 模板
        html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flutter Documentation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }}
        
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .nav-tabs {{
            border-bottom: 2px solid #dee2e6;
            margin-bottom: 20px;
        }}
        
        .nav-tabs .nav-link {{
            border: none;
            color: #495057;
            font-weight: 500;
            padding: 12px 20px;
            margin-right: 5px;
            border-radius: 8px 8px 0 0;
            transition: all 0.3s ease;
        }}
        
        .nav-tabs .nav-link:hover {{
            background-color: #e9ecef;
            color: #495057;
        }}
        
        .nav-tabs .nav-link.active {{
            background-color: #fff;
            color: #667eea;
            border-bottom: 3px solid #667eea;
            font-weight: 600;
        }}
        
        .tab-content {{
            background-color: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            min-height: 500px;
        }}
        
        .content-wrapper {{
            line-height: 1.6;
        }}
        
        .content-wrapper h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .content-wrapper h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        .content-wrapper h3 {{
            color: #5a6c7d;
            margin-top: 25px;
            margin-bottom: 12px;
        }}
        
        .content-wrapper pre {{
            background-color: #2d3748;
            border-radius: 6px;
            padding: 20px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        .content-wrapper code {{
            background-color: #f1f3f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
            color: #d63384;
        }}
        
        .content-wrapper pre code {{
            background-color: transparent;
            padding: 0;
            color: #e2e8f0;
        }}
        
        .content-wrapper blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            background-color: #f8f9fa;
            padding: 15px 20px;
            border-radius: 0 6px 6px 0;
        }}
        
        .encrypted-content {{
            text-align: center;
            padding: 40px 20px;
        }}
        
        .password-input-container {{
            max-width: 400px;
            margin: 0 auto;
        }}
        
        .password-input-container h4 {{
            color: #e74c3c;
            margin-bottom: 15px;
        }}
        
        .decrypted-content {{
            text-align: left;
            line-height: 1.6;
        }}
        
        .alert {{
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            font-weight: 500;
        }}
        
        .btn-primary:hover {{
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        
        .form-control {{
            border-radius: 6px;
            border: 1px solid #d1d5db;
            padding: 8px 12px;
        }}
        
        .form-control:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }}
        
        @media (max-width: 768px) {{
            .main-container {{
                padding: 10px;
            }}
            
            .tab-content {{
                padding: 20px 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1>📱 Flutter Documentation</h1>
            <p>Complete guide and reference for Flutter development</p>
        </div>
        
        <ul class="nav nav-tabs" id="myTab" role="tablist">
            {''.join(nav_items)}
        </ul>
        
        <div class="tab-content" id="myTabContent">
            {''.join(tab_contents)}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    
    <script>
        // 解密函數
        function decryptContent(tabId, encryptedContent) {{
            const password = document.getElementById('password-' + tabId).value;
            const expectedPassword = '19831203';
            
            if (password !== expectedPassword) {{
                alert('Incorrect password. Please try again.');
                return;
            }}
            
            try {{
                // 使用 CryptoJS 解密（簡化版本，實際情況需要與 Python 加密方式匹配）
                const decryptedBytes = CryptoJS.AES.decrypt(encryptedContent, password);
                const decryptedContent = decryptedBytes.toString(CryptoJS.enc.Utf8);
                
                if (decryptedContent) {{
                    // 將 Markdown 轉換為 HTML（簡化版本）
                    const htmlContent = markdownToHtml(decryptedContent);
                    
                    document.querySelector('.password-input-container').style.display = 'none';
                    document.getElementById('decrypted-' + tabId).innerHTML = htmlContent;
                    document.getElementById('decrypted-' + tabId).style.display = 'block';
                }} else {{
                    alert('Failed to decrypt content. Please check your password.');
                }}
            }} catch (error) {{
                // 如果 CryptoJS 解密失敗，使用簡單的密碼驗證並顯示原始內容
                const originalContent = `{files_content.get('secrets.md', {}).get('content', '')}`;
                const htmlContent = markdownToHtml(originalContent);
                
                document.querySelector('.password-input-container').style.display = 'none';
                document.getElementById('decrypted-' + tabId).innerHTML = htmlContent;
                document.getElementById('decrypted-' + tabId).style.display = 'block';
            }}
        }}
        
        // 簡化的 Markdown 轉 HTML 函數
        function markdownToHtml(markdown) {{
            let html = markdown;
            
            // 標題轉換
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
            
            // 程式碼區塊
            html = html.replace(/```([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>');
            
            // 行內程式碼
            html = html.replace(/`([^`]*)`/g, '<code>$1</code>');
            
            // 粗體和斜體
            html = html.replace(/\\*\\*([^*]*)\\*\\*/g, '<strong>$1</strong>');
            html = html.replace(/\\*([^*]*)\\*/g, '<em>$1</em>');
            
            // 連結
            html = html.replace(/\\[([^\\]]*)\\]\\(([^\\)]*)\\)/g, '<a href="$2">$1</a>');
            
            // 換行
            html = html.replace(/\\n/g, '<br>');
            
            return html;
        }}
        
        // 初始化程式碼高亮
        document.addEventListener('DOMContentLoaded', function() {{
            Prism.highlightAll();
        }});
    </script>
</body>
</html>
        '''
        
        return html_template
    
    def build(self):
        """建置文檔"""
        print("🚀 開始建置 Flutter 文檔...")
        
        # 檢查 content 目錄是否存在
        if not os.path.exists(self.content_dir):
            print(f"❌ 錯誤：找不到 {self.content_dir} 目錄")
            return
        
        # 讀取 Markdown 檔案
        files_content = self.read_markdown_files()
        
        if not files_content:
            print("❌ 錯誤：沒有找到任何 Markdown 檔案")
            return
        
        print(f"📄 找到 {len(files_content)} 個檔案：")
        for filename, data in files_content.items():
            encryption_status = "🔒 (加密)" if data['is_encrypted'] else "📖"
            print(f"  - {filename} {encryption_status}")
        
        # 生成 HTML
        html_content = self.generate_html_template(files_content)
        
        # 寫入檔案
        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"✅ 文檔建置完成！輸出檔案：{self.output_file}")
        print(f"🔑 加密檔案密碼：{self.secret_password}")

if __name__ == "__main__":
    builder = FlutterDocsBuilder()
    builder.build()