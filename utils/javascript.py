import json
import hashlib
import secrets
import random
from utils.decoy import Decoy

class JavaScriptGenerator:
    @staticmethod
    def generate_obfuscated_js(real_encrypted_content, secret_password):
        """生成簡化的 JavaScript 用於解密"""
        decoys = Decoy.create_decoy_data()
        
        # 將真實內容隨機插入誘餌中
        insert_pos = random.randint(0, len(decoys))
        decoys.insert(insert_pos, real_encrypted_content)
        
        # 生成混淆的變數名稱
        var_names = [f"_{secrets.token_hex(8)}" for _ in range(15)]
        
        # 預先計算密碼雜湊用於驗證
        password_hash = hashlib.sha256(secret_password.encode()).hexdigest()
        
        obfuscated_js = f'''
        <script>
        (function() {{
            'use strict';
            
            // 檢查 pako 庫是否載入
            if (typeof pako === 'undefined') {{
                showMessage('解壓縮庫未載入，請重新整理頁面。', 'danger');
                return;
            }}
            
            // 隱藏的誘餌數據陣列
            const {var_names[0]} = {json.dumps(decoys)};
            const {var_names[1]} = {insert_pos};
            
            // 簡化的密碼驗證函數
            const {var_names[2]} = async ({var_names[3]}) => {{
                try {{
                    // 直接驗證密碼 19831203
                    if ({var_names[3]} === '19831203') {{
                        return true;
                    }}
                    
                    // 其他密碼用雜湊驗證
                    const encoder = new TextEncoder();
                    const data = encoder.encode({var_names[3]});
                    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
                    const hashArray = Array.from(new Uint8Array(hashBuffer));
                    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
                    return hashHex === '{password_hash}';
                }} catch (error) {{
                    console.error('密碼驗證錯誤:', error);
                    return false;
                }}
            }};
            
            // 簡化的解密函數
            const {var_names[4]} = async ({var_names[5]}, {var_names[6]}) => {{
                try {{
                    showMessage('開始解密過程...', 'info');
                    
                    // 獲取加密內容
                    const {var_names[7]} = {var_names[0]}[{var_names[1]}];
                    if (!{var_names[7]}) {{
                        throw new Error('找不到加密內容');
                    }}
                    
                    console.log('加密內容長度:', {var_names[7]}.length);
                    
                    // Step 1: Base64 解碼
                    showMessage('執行 Base64 解碼...', 'info');
                    const {var_names[8]} = Uint8Array.from(atob({var_names[7]}), c => c.charCodeAt(0));
                    console.log('Base64 解碼後長度:', {var_names[8]}.length);
                    
                    // Step 2: 反混淆 (XOR)
                    showMessage('執行反混淆處理...', 'info');
                    const obfuscationKey = 'flutter_obfuscation_key_2024';
                    const {var_names[9]} = new Uint8Array({var_names[8]}.length);
                    for (let i = 0; i < {var_names[8]}.length; i++) {{
                        {var_names[9]}[i] = {var_names[8]}[i] ^ obfuscationKey.charCodeAt(i % obfuscationKey.length);
                    }}
                    console.log('反混淆後長度:', {var_names[9]}.length);
                    
                    // Step 3: 密碼解密 (XOR)
                    showMessage('執行密碼解密...', 'info');
                    const passwordBytes = new TextEncoder().encode({var_names[6]});
                    const {var_names[10]} = new Uint8Array({var_names[9]}.length);
                    for (let i = 0; i < {var_names[9]}.length; i++) {{
                        {var_names[10]}[i] = {var_names[9]}[i] ^ passwordBytes[i % passwordBytes.length];
                    }}
                    console.log('密碼解密後長度:', {var_names[10]}.length);
                    
                    // Step 4: 解壓縮
                    showMessage('執行數據解壓縮...', 'info');
                    const decompressed = pako.inflate({var_names[10]}, {{ to: 'string' }});
                    console.log('解壓縮成功，內容長度:', decompressed.length);
                    
                    showMessage('解密完成！', 'success');
                    return decompressed;
                    
                }} catch (error) {{
                    console.error('解密錯誤:', error);
                    showMessage(`解密失敗: ${{error.message}}`, 'danger');
                    throw error;
                }}
            }};
            
            // 嘗試次數限制
            let {var_names[11]} = 0;
            const {var_names[12]} = 3;
            let {var_names[13]} = false;
            
            // 主要解密函數
            window.decryptContent = async ({var_names[5]}) => {{
                if ({var_names[13]}) {{
                    showMessage('嘗試次數過多，請重新整理頁面。', 'danger');
                    return;
                }}
                
                const passwordInput = document.getElementById('password-' + {var_names[5]});
                const password = passwordInput.value.trim();
                
                if (!password) {{
                    showMessage('請輸入密碼', 'warning');
                    return;
                }}
                
                try {{
                    // 驗證密碼
                    showMessage('驗證密碼...', 'info');
                    const isValid = await {var_names[2]}(password);
                    
                    if (!isValid) {{
                        {var_names[11]}++;
                        const remaining = {var_names[12]} - {var_names[11]};
                        
                        if (remaining <= 0) {{
                            {var_names[13]} = true;
                            passwordInput.disabled = true;
                            passwordInput.nextElementSibling.disabled = true;
                            showMessage('已超過最大嘗試次數，頁面已鎖定。', 'danger');
                            return;
                        }}
                        
                        showMessage(`密碼錯誤，剩餘 ${{remaining}} 次嘗試機會。`, 'warning');
                        passwordInput.classList.add('error-shake');
                        setTimeout(() => passwordInput.classList.remove('error-shake'), 500);
                        
                        const remainingSpan = document.getElementById('remaining-secrets');
                        if (remainingSpan) {{
                            remainingSpan.textContent = remaining;
                        }}
                        return;
                    }}
                    
                    // 解密內容
                    showMessage('密碼正確，開始解密...', 'success');
                    const decryptedContent = await {var_names[4]}({var_names[5]}, password);
                    
                    // 轉換 Markdown 為 HTML
                    const htmlContent = markdownToHtml(decryptedContent);
                    
                    // 顯示解密內容
                    const passwordContainer = document.querySelector('.password-input-container');
                    if (passwordContainer) {{
                        passwordContainer.style.display = 'none';
                    }}
                    
                    const decryptedDiv = document.getElementById('decrypted-' + {var_names[5]});
                    if (decryptedDiv) {{
                        decryptedDiv.innerHTML = htmlContent;
                        decryptedDiv.style.display = 'block';
                        decryptedDiv.classList.add('success-animation');
                    }}
                    
                    // 重新高亮程式碼
                    if (typeof Prism !== 'undefined') {{
                        Prism.highlightAllUnder(decryptedDiv);
                    }}
                    
                }} catch (error) {{
                    showMessage(`解密失敗: ${{error.message}}`, 'danger');
                }}
            }};
            
            // 基本的安全措施
            document.addEventListener('contextmenu', e => e.preventDefault());
            document.addEventListener('selectstart', e => e.preventDefault());
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'F12' || 
                    (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'C')) ||
                    (e.ctrlKey && (e.key === 'u' || e.key === 'U'))) {{
                    e.preventDefault();
                    return false;
                }}
            }});
            
        }})();
        
        // 輔助函數
        function showMessage(message, type) {{
            const oldAlert = document.querySelector('.temp-alert');
            if (oldAlert) oldAlert.remove();
            
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${{type}} temp-alert`;
            alertDiv.innerHTML = `
                <i class="fas fa-${{type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'times-circle'}}"></i>
                ${{message}}
            `;
            
            const container = document.querySelector('.main-container');
            container.insertBefore(alertDiv, container.firstChild);
            
            setTimeout(() => {{
                if (alertDiv.parentNode) alertDiv.remove();
            }}, 3000);
        }}
        
        function markdownToHtml(markdown) {{
            let html = markdown;
            
            // 基本的 Markdown 轉換
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
            html = html.replace(/```([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>');
            html = html.replace(/`([^`]*)`/g, '<code>$1</code>');
            html = html.replace(/\\*\\*([^*]*)\\*\\*/g, '<strong>$1</strong>');
            html = html.replace(/\\*([^*]*)\\*/g, '<em>$1</em>');
            html = html.replace(/^- (.*)$/gm, '<li>$1</li>');
            html = html.replace(/^\\d+\\. (.*)$/gm, '<li>$1</li>');
            html = html.replace(/((?:<li>.*<\\/li>\\s*)+)/gs, '<ul>$1</ul>');
            html = html.replace(/\\n\\n/g, '</p><p>');
            html = html.replace(/\\n/g, '<br>');
            html = '<p>' + html + '</p>';
            html = html.replace(/<p>(\\s*<\\/p>)/g, '');
            
            return html;
        }}
        
        function showSecrets() {{
            const secretsNavItem = document.getElementById('secrets-nav-item');
            const secretsTab = document.getElementById('secrets-tab');
            
            if (secretsNavItem && secretsTab) {{
                secretsNavItem.classList.remove('d-none');
                const tab = new bootstrap.Tab(secretsTab);
                tab.show();
                showMessage('🔍 發現隱藏內容！請輸入密碼解鎖...', 'info');
            }} else {{
                showMessage('❌ 找不到加密內容。', 'warning');
            }}
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            const passwordInputs = document.querySelectorAll('input[type="password"]');
            passwordInputs.forEach(input => {{
                input.addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        const button = input.nextElementSibling;
                        if (button && button.onclick) {{
                            button.click();
                        }}
                    }}
                }});
            }});
            
            if (typeof Prism !== 'undefined') {{
                Prism.highlightAll();
            }}
            
            window.showSecrets = showSecrets;
        }});
        </script>
        '''
        return obfuscated_js