import os
import re
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import markdown

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
    
    def extract_order_from_filename(self, filename):
        """從檔案名稱提取排序數字"""
        # 尋找檔案名稱開頭的數字
        match = re.match(r'^(\d+)', filename)
        if match:
            return int(match.group(1))
        return 999  # 沒有數字的檔案排在最後
    
    def extract_title_from_content(self, content):
        """從內容中提取標題（第一個 # 標題）"""
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        return None
    
    def read_markdown_files(self):
        """讀取所有 Markdown 檔案並依照數字排序"""
        files_content = {}
        
        # 獲取所有 .md 檔案
        md_files = [f for f in os.listdir(self.content_dir) if f.endswith('.md')]
        
        # 依照檔案名稱開頭的數字排序
        md_files.sort(key=self.extract_order_from_filename)
        
        for filename in md_files:
            filepath = os.path.join(self.content_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # 從內容中提取標題，如果沒有則使用檔案名稱
            title = self.extract_title_from_content(content)
            if not title:
                # 移除檔案副檔名和數字前綴，格式化為標題
                title = re.sub(r'^\d+\.\s*', '', filename.replace('.md', '').replace('_', ' ')).title()
            
            # 如果是 secrets.md，進行特殊處理
            if filename == 'secrets.md':
                encrypted_content = self.encrypt_content(content, self.secret_password)
                files_content[filename] = {
                    'title': '',  # 完全隱藏標題
                    'original_title': title,
                    'content': content,
                    'encrypted_content': encrypted_content,
                    'is_encrypted': True,
                    'is_hidden': True,  # 標記為隱藏標籤
                    'order': self.extract_order_from_filename(filename)
                }
            else:
                # 轉換 Markdown 為 HTML
                html_content = markdown.markdown(content, extensions=['codehilite', 'fenced_code'])
                files_content[filename] = {
                    'title': title,
                    'content': html_content,
                    'is_encrypted': False,
                    'order': self.extract_order_from_filename(filename)
                }
                    
        return files_content
    
    def generate_html_template(self, files_content):
        """生成完整的 HTML 模板"""
        
        # 依照 order 欄位排序
        sorted_files = sorted(files_content.items(), key=lambda x: x[1]['order'])
        
        # 生成導航選項
        nav_items = []
        tab_contents = []
        
        for i, (filename, data) in enumerate(sorted_files):
            tab_id = filename.replace('.md', '').replace('_', '-').replace(' ', '-')
            active_class = 'active' if i == 0 else ''
            
            # 檢查是否為隱藏標籤
            if data.get('is_hidden', False):
                nav_items.append(f'''
                    <li class="nav-item hidden-tab">
                        <a class="nav-link {active_class} invisible-tab" id="{tab_id}-tab" data-bs-toggle="tab" 
                           href="#{tab_id}" role="tab" aria-controls="{tab_id}" 
                           aria-selected="{'true' if i == 0 else 'false'}" title="🤫">
                            &nbsp;
                        </a>
                    </li>
                ''')
            else:
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
                                <h4>🔒 此內容需要密碼存取</h4>
                                <div class="password-hint">
                                    <div class="alert alert-info">
                                        <i class="fas fa-lightbulb"></i>
                                        <strong>提示：</strong>閱讀完整份文件即可知道密碼 😉
                                        <br>
                                        <small class="text-muted">仔細觀察其他章節的內容，密碼可能就在某個地方...</small>
                                        <br>
                                        <small class="text-success">🎉 恭喜您發現了這個隱藏的標籤頁！</small>
                                    </div>
                                </div>
                                <div class="input-group mb-3">
                                    <input type="password" class="form-control" id="password-{tab_id}" 
                                           placeholder="請輸入密碼" maxlength="8">
                                    <button class="btn btn-primary" type="button" 
                                            onclick="decryptContent('{tab_id}', '{data['encrypted_content']}')">
                                        <i class="fas fa-unlock"></i> 解鎖
                                    </button>
                                </div>
                                <div class="password-attempts" id="attempts-{tab_id}">
                                    <small class="text-muted">剩餘嘗試次數：<span id="remaining-{tab_id}">3</span></small>
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
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flutter 開發文檔</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            line-height: 1.6;
        }}
        
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .nav-tabs {{
            border-bottom: 3px solid #dee2e6;
            margin-bottom: 25px;
            background: white;
            border-radius: 10px 10px 0 0;
            padding: 5px 5px 0 5px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .nav-tabs .nav-link {{
            border: none;
            color: #495057;
            font-weight: 500;
            padding: 15px 20px;
            margin-right: 5px;
            border-radius: 10px 10px 0 0;
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .nav-tabs .nav-link:hover {{
            background-color: #f8f9fa;
            color: #667eea;
            transform: translateY(-2px);
        }}
        
        .nav-tabs .nav-link.active {{
            background-color: #667eea;
            color: white;
            font-weight: 600;
            box-shadow: 0 -2px 10px rgba(102, 126, 234, 0.3);
        }}
        
        /* 隱藏標籤樣式 */
        .hidden-tab {{
            min-width: 40px;
        }}
        
        .invisible-tab {{
            background: transparent !important;
            border: 2px dashed transparent !important;
            min-width: 35px !important;
            min-height: 45px !important;
            position: relative;
            transition: all 0.3s ease;
        }}
        
        .invisible-tab:hover {{
            border-color: #667eea !important;
            background: rgba(102, 126, 234, 0.05) !important;
            transform: translateY(-1px);
        }}
        
        .invisible-tab.active {{
            background: #667eea !important;
            border-color: #667eea !important;
        }}
        
        .invisible-tab::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .invisible-tab:hover::after {{
            opacity: 0.6;
        }}
        
        .invisible-tab.active::after {{
            background: white;
            opacity: 1;
        }}
        
        .tab-content {{
            background-color: white;
            border-radius: 0 0 15px 15px;
            padding: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            min-height: 500px;
        }}
        
        .content-wrapper {{
            line-height: 1.7;
        }}
        
        .content-wrapper h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 25px;
            font-weight: 700;
        }}
        
        .content-wrapper h2 {{
            color: #34495e;
            margin-top: 35px;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .content-wrapper h3 {{
            color: #5a6c7d;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 500;
        }}
        
        .content-wrapper pre {{
            background-color: #2d3748;
            border-radius: 10px;
            padding: 25px;
            overflow-x: auto;
            margin: 25px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .content-wrapper code {{
            background-color: #f1f3f4;
            padding: 3px 8px;
            border-radius: 5px;
            font-family: 'Courier New', Courier, monospace;
            color: #d63384;
            font-size: 0.9em;
        }}
        
        .content-wrapper pre code {{
            background-color: transparent;
            padding: 0;
            color: #e2e8f0;
        }}
        
        .content-wrapper blockquote {{
            border-left: 5px solid #667eea;
            padding-left: 25px;
            margin: 25px 0;
            background-color: #f8f9fa;
            padding: 20px 25px;
            border-radius: 0 10px 10px 0;
            font-style: italic;
        }}
        
        .encrypted-content {{
            text-align: center;
            padding: 50px 20px;
        }}
        
        .password-input-container {{
            max-width: 500px;
            margin: 0 auto;
        }}
        
        .password-input-container h4 {{
            color: #e74c3c;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .password-hint {{
            margin-bottom: 25px;
        }}
        
        .password-hint .alert {{
            text-align: left;
            border-radius: 10px;
            border: none;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .password-attempts {{
            margin-top: 10px;
        }}
        
        .decrypted-content {{
            text-align: left;
            line-height: 1.7;
            animation: fadeIn 0.5s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .alert {{
            border-radius: 10px;
            margin-bottom: 25px;
            border: none;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .btn {{
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .btn-primary:hover {{
            background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .form-control {{
            border-radius: 8px;
            border: 2px solid #e9ecef;
            padding: 12px 15px;
            transition: all 0.3s ease;
        }}
        
        .form-control:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }}
        
        .input-group {{
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        /* 響應式設計 */
        @media (max-width: 768px) {{
            .main-container {{
                padding: 10px;
            }}
            
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .tab-content {{
                padding: 20px 15px;
            }}
            
            .nav-tabs .nav-link {{
                padding: 12px 15px;
                font-size: 0.9rem;
            }}
        }}
        
        /* 成功動畫 */
        .success-animation {{
            animation: success 0.6s ease-in-out;
        }}
        
        @keyframes success {{
            0% {{ transform: scale(0.8); opacity: 0; }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        /* 錯誤震動動畫 */
        .error-shake {{
            animation: shake 0.5s ease-in-out;
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1><i class="fab fa-flutter"></i> Flutter 開發文檔</h1>
            <p>完整的 Flutter 開發指南與實戰經驗分享</p>
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
        // 解密嘗試次數記錄
        const attemptCounts = {{}};
        const maxAttempts = 3;
        
        // 解密函數
        function decryptContent(tabId, encryptedContent) {{
            const passwordInput = document.getElementById('password-' + tabId);
            const password = passwordInput.value;
            const expectedPassword = '19831203';
            
            // 初始化嘗試次數
            if (!attemptCounts[tabId]) {{
                attemptCounts[tabId] = 0;
            }}
            
            if (password !== expectedPassword) {{
                attemptCounts[tabId]++;
                const remaining = maxAttempts - attemptCounts[tabId];
                
                // 更新剩餘次數顯示
                const remainingSpan = document.getElementById('remaining-' + tabId);
                remainingSpan.textContent = remaining;
                
                // 添加錯誤動畫
                passwordInput.classList.add('error-shake');
                setTimeout(() => {{
                    passwordInput.classList.remove('error-shake');
                }}, 500);
                
                if (remaining <= 0) {{
                    passwordInput.disabled = true;
                    passwordInput.nextElementSibling.disabled = true;
                    showMessage('密碼錯誤次數過多，請重新載入頁面！', 'danger');
                    return;
                }}
                
                showMessage(`密碼錯誤！還有 ${{remaining}} 次機會`, 'warning');
                passwordInput.value = '';
                passwordInput.focus();
                return;
            }}
            
            try {{
                // 簡單的密碼驗證成功，顯示原始內容
                const originalContent = `{files_content.get('secrets.md', {}).get('content', '')}`;
                const htmlContent = markdownToHtml(originalContent);
                
                // 添加成功動畫
                const container = document.querySelector('.password-input-container');
                container.style.display = 'none';
                
                const decryptedDiv = document.getElementById('decrypted-' + tabId);
                decryptedDiv.innerHTML = htmlContent;
                decryptedDiv.style.display = 'block';
                decryptedDiv.classList.add('success-animation');
                
                showMessage('解鎖成功！享受進階內容吧 🎉', 'success');
                
                // 重新初始化程式碼高亮
                if (typeof Prism !== 'undefined') {{
                    Prism.highlightAllUnder(decryptedDiv);
                }}
                
            }} catch (error) {{
                console.error('解密失敗:', error);
                showMessage('解密過程中發生錯誤，請重試', 'danger');
            }}
        }}
        
        // 顯示訊息
        function showMessage(message, type) {{
            // 移除舊的訊息
            const oldAlert = document.querySelector('.temp-alert');
            if (oldAlert) {{
                oldAlert.remove();
            }}
            
            // 創建新的訊息
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${{type}} temp-alert`;
            alertDiv.innerHTML = `
                <i class="fas fa-${{type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'times-circle'}}"></i>
                ${{message}}
            `;
            
            // 插入到頁面頂部
            const container = document.querySelector('.main-container');
            container.insertBefore(alertDiv, container.firstChild);
            
            // 3 秒後自動移除
            setTimeout(() => {{
                if (alertDiv.parentNode) {{
                    alertDiv.remove();
                }}
            }}, 3000);
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
            html = html.replace(/\\[([^\\]]*)\\]\\(([^\\)]*)\\)/g, '<a href="$2" target="_blank">$1</a>');
            
            // 列表
            html = html.replace(/^\\d+\\. (.*)$/gm, '<li>$1</li>');
            html = html.replace(/^- (.*)$/gm, '<li>$1</li>');
            
            // 包裝列表
            html = html.replace(/((?:<li>.*<\\/li>\\s*)+)/gs, '<ul>$1</ul>');
            
            // 引用區塊
            html = html.replace(/^> (.*)$/gm, '<blockquote>$1</blockquote>');
            
            // 段落和換行
            html = html.replace(/\\n\\n/g, '</p><p>');
            html = html.replace(/\\n/g, '<br>');
            html = '<p>' + html + '</p>';
            
            // 清理空段落
            html = html.replace(/<p><\\/p>/g, '');
            
            return html;
        }}
        
        // 密碼輸入框 Enter 事件
        document.addEventListener('DOMContentLoaded', function() {{
            // 為所有密碼輸入框添加 Enter 鍵監聽
            const passwordInputs = document.querySelectorAll('input[type="password"]');
            passwordInputs.forEach(input => {{
                input.addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        const button = this.nextElementSibling;
                        if (button && button.onclick) {{
                            button.click();
                        }}
                    }}
                }});
            }});
            
            // 初始化程式碼高亮
            if (typeof Prism !== 'undefined') {{
                Prism.highlightAll();
            }}
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
        
        # 依照排序顯示檔案資訊
        sorted_files = sorted(files_content.items(), key=lambda x: x[1]['order'])
        for filename, data in sorted_files:
            encryption_status = "🔒 (加密)" if data['is_encrypted'] else "📖"
            order = data['order']
            title = data['title']
            print(f"  {order:2d}. {filename} - {title} {encryption_status}")
        
        # 生成 HTML
        html_content = self.generate_html_template(files_content)
        
        # 寫入檔案
        with open(self.output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        print(f"✅ 文檔建置完成！輸出檔案：{self.output_file}")
        print(f"🔑 加密檔案密碼：{self.secret_password}")
        print("💡 提示：密碼就在文檔內容中，仔細閱讀就能找到！")

if __name__ == "__main__":
    builder = FlutterDocsBuilder()
    builder.build()