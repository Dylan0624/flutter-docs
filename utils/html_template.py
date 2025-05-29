from utils.javascript import JavaScriptGenerator

class HTMLTemplate:
    @staticmethod
    def generate_html_template(files_content, secret_password):
        """生成完整的 HTML 模板，包含動態內容。"""
        sorted_files = sorted(files_content.items(), key=lambda x: x[1]['order'])
        
        nav_items = []
        tab_contents = []
        
        has_secrets = any(data.get('is_encrypted', False) for _, data in sorted_files)
        secrets_data = None
        if has_secrets:
            for filename, data in sorted_files:
                if data.get('is_encrypted', False):
                    secrets_data = data
                    break
        
        # 修正：計算非加密文件的索引，用於確定第一個分頁
        regular_file_index = 0
        
        # Generate navigation items and tab content for regular files
        for filename, data in sorted_files:
            if data.get('is_encrypted', False):
                continue  # 跳過加密文件，但不增加索引
                
            # 修正：使用 regular_file_index 來判斷是否為第一個分頁
            tab_id = filename.replace('.md', '').replace('_', '-').replace(' ', '-').replace('(', '').replace(')', '').lower()
            active_class = 'active' if regular_file_index == 0 else ''
            
            nav_items.append(f'''
                <li class="nav-item">
                    <a class="nav-link {active_class}" id="{tab_id}-tab" data-bs-toggle="tab" 
                       href="#{tab_id}" role="tab" aria-controls="{tab_id}" 
                       aria-selected="{'true' if regular_file_index == 0 else 'false'}">
                        {data['title']}
                    </a>
                </li>
            ''')
            
            tab_contents.append(f'''
                <div class="tab-pane fade {'show active' if regular_file_index == 0 else ''}" id="{tab_id}" 
                     role="tabpanel" aria-labelledby="{tab_id}-tab">
                    <div class="content-wrapper">
                        {data['content']}
                    </div>
                </div>
            ''')
            
            # 修正：只有在處理非加密文件時才增加索引
            regular_file_index += 1
        
        # Add Secrets tab if encrypted content exists
        if secrets_data:
            nav_items.append(f'''
                <li class="nav-item d-none" id="secrets-nav-item">
                    <a class="nav-link" id="secrets-tab" data-bs-toggle="tab" 
                       href="#secrets" role="tab" aria-controls="secrets" 
                       aria-selected="false">
                        Secrets
                    </a>
                </li>
            ''')
            
            tab_contents.append(f'''
                <div class="tab-pane fade" id="secrets" role="tabpanel" aria-labelledby="secrets-tab">
                    <div class="encrypted-content">
                        <div class="password-input-container">
                            <h4>🔒 此內容需要密碼存取</h4>
                            <div class="password-hint">
                                <div class="alert alert-info">
                                    <i class="fas fa-lightbulb"></i>
                                    <strong>提示：</strong>閱讀完整份文件即可知道密碼 😉
                                    <br>
                                    <small class="text-muted">仔細的做完每個練習，密碼可能就在某個地方...</small>
                                    <br>
                                    <small class="text-success">🎉 恭喜你發現了這個隱藏的真相！</small>
                                </div>
                            </div>
                            <div class="input-group mb-3">
                                <input type="password" class="form-control" id="password-secrets" 
                                       placeholder="Enter password" maxlength="15">
                                <button class="btn btn-primary" type="button" 
                                        onclick="decryptContent('secrets')">
                                    <i class="fas fa-unlock"></i> Unlock
                                </button>
                            </div>
                            <div class="password-attempts" id="attempts-secrets">
                                <small class="text-muted">Remaining attempts: <span id="remaining-secrets">3</span></small>
                            </div>
                        </div>
                        <div class="decrypted-content" id="decrypted-secrets" style="display: none;">
                        </div>
                    </div>
                </div>
            ''')
        
        # 修正：只有在有 secrets_data 時才生成 JavaScript
        js_content = ""
        if secrets_data:
            js_content = JavaScriptGenerator.generate_obfuscated_js(
                secrets_data['encrypted_content'], secret_password
            )
        
        html_template = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flutter Development Documentation</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Add pako for decompression -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked@4.0.12/lib/marked.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
            line-height: 1.6;
            user-select: none;
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
            position: relative;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            display: inline-block;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .secret-icon {{
            position: absolute;
            top: 20px;
            right: 25px;
            color: transparent;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 10;
        }}
        
        .secret-icon:hover {{
            color: rgba(255, 255, 255, 0.1);
            transform: scale(1.1);
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
        
        .error-shake {{
            animation: shake 0.5s ease-in-out;
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-5px); }}
            75% {{ transform: translateX(5px); }}
        }}
        
        .success-animation {{
            animation: success 0.6s ease-in-out;
        }}
        
        @keyframes success {{
            0% {{ transform: scale(0.8); opacity: 0; }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
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
            
            .secret-icon {{
                top: 15px;
                right: 20px;
                font-size: 1rem;
            }}
        }}
        
        #debug-log {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: #fff;
            padding: 10px;
            border: 1px solid #ccc;
            max-height: 200px;
            overflow-y: auto;
            font-size: 0.8rem;
            display: none; /* 修正：顯示除錯日誌以便調試 */
            z-index: 1000;
            width: 300px;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1><i class="fab fa-flutter"></i> Flutter Development Documentation <i class="fas fa-rocket secret-icon" onclick="showSecrets()" title="Hidden Content"></i></h1>
            <p>Complete Flutter Development Experience Sharing</p>
        </div>
        
        <ul class="nav nav-tabs" id="myTab" role="tablist">
            {''.join(nav_items)}
        </ul>
        
        <div class="tab-content" id="myTabContent">
            {''.join(tab_contents)}
        </div>
        <div id="debug-log"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    
    {js_content}
</body>
</html>
'''
        return html_template