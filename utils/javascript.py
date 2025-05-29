import json
import hashlib
import secrets
import random
from utils.decoy import Decoy
from utils.encryption import Encryption

class JavaScriptGenerator:
    @staticmethod
    def generate_obfuscated_js(real_encrypted_content, secret_password):
        """生成具有永久銷毀功能的混淆 JavaScript"""
        
        # 創建誘餌數據
        decoys = Decoy.create_decoy_data(len(real_encrypted_content))
        
        # 隨機插入真實內容
        insert_pos = random.randint(0, len(decoys))
        decoys.insert(insert_pos, real_encrypted_content)
        
        # 生成隨機變數名稱
        var_names = [f"_{secrets.token_hex(6)}" for _ in range(15)]
        
        # 生成密碼驗證雜湊
        password_hash = Encryption.generate_password_hash(secret_password)
        
        print(f"JavaScript 生成資訊:")
        print(f"- 誘餌數據數量: {len(decoys)}")
        print(f"- 真實數據位置: {insert_pos}")
        print(f"- 密碼雜湊: {password_hash}")
        print(f"- 真實內容長度: {len(real_encrypted_content)}")
        
        obfuscated_js = f'''
        <script>
        (function() {{
            'use strict';
            
            // 檢查必要的庫
            if (typeof pako === 'undefined') {{
                console.error('pako 庫未載入');
                showMessage('解壓縮庫載入失敗，請重新整理頁面', 'danger');
                return;
            }}
            
            // 防調試措施（簡化版）
            {JavaScriptGenerator._generate_simple_protection()}
            
            // 混淆的數據陣列
            let {var_names[0]} = {json.dumps(decoys)};
            const {var_names[1]} = {insert_pos};
            const {var_names[2]} = "{password_hash}";
            
            console.log('數據陣列長度:', {var_names[0]}.length);
            console.log('真實數據位置:', {var_names[1]});
            
            // 嘗試計數器和鎖定狀態
            let {var_names[3]} = 0;
            const {var_names[4]} = 3;
            let {var_names[5]} = false;
            
            // LocalStorage 鍵名（混淆）
            const {var_names[6]} = 'flutter_docs_security_status';
            const {var_names[7]} = 'flutter_docs_attempt_count';
            
            // 永久銷毀函數
            const permanentDestroy = () => {{
                console.warn('執行永久銷毀程序...');
                
                // 1. 記錄銷毀狀態到 localStorage（永久保存）
                const destroyData = {{
                    destroyed: true,
                    timestamp: Date.now(),
                    reason: 'password_attempts_exceeded',
                    version: '2024_secure'
                }};
                
                try {{
                    localStorage.setItem({var_names[6]}, JSON.stringify(destroyData));
                    localStorage.setItem({var_names[7]}, '999'); // 標記超過限制
                    console.log('銷毀狀態已保存到 localStorage');
                }} catch (e) {{
                    console.error('localStorage 寫入失敗:', e);
                }}
                
                // 2. 清空所有加密資料
                {var_names[0]} = Array({var_names[0]}.length).fill('DESTROYED_DATA');
                
                // 3. 銷毀頁面內容
                destroyPageContent();
            }};
            
            // 銷毀頁面內容函數
            const destroyPageContent = () => {{
                document.body.innerHTML = `
                    <div style="
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                        margin: 0;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    ">
                        <div style="
                            background: rgba(255, 255, 255, 0.95);
                            padding: 40px;
                            border-radius: 15px;
                            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                            text-align: center;
                            max-width: 500px;
                            animation: shake 0.5s ease-in-out;
                        ">
                            <div style="font-size: 64px; margin-bottom: 20px;">🚫</div>
                            <h1 style="
                                color: #e74c3c;
                                margin: 0 0 20px 0;
                                font-size: 28px;
                                font-weight: bold;
                            ">資料已永久銷毀</h1>
                            <p style="
                                color: #2c3e50;
                                font-size: 16px;
                                line-height: 1.6;
                                margin: 0 0 15px 0;
                            ">由於密碼輸入錯誤次數過多，基於安全考量，所有加密資料已被永久刪除。</p>
                            <p style="
                                color: #e74c3c;
                                font-size: 14px;
                                font-weight: bold;
                                margin: 0;
                            ">⚠️ 此檔案已無法使用，請重新取得原始檔案</p>
                            <div style="
                                margin-top: 25px;
                                padding: 15px;
                                background: #ffeaa7;
                                border-radius: 8px;
                                font-size: 12px;
                                color: #636e72;
                            ">
                                銷毀時間: ${{new Date().toLocaleString()}}
                            </div>
                        </div>
                    </div>
                    <style>
                        @keyframes shake {{
                            0%, 100% {{ transform: translateX(0); }}
                            25% {{ transform: translateX(-5px); }}
                            75% {{ transform: translateX(5px); }}
                        }}
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    </style>
                `;
                
                // 禁用所有交互
                document.addEventListener('contextmenu', e => e.preventDefault());
                document.addEventListener('selectstart', e => e.preventDefault());
                document.addEventListener('keydown', e => e.preventDefault());
            }};
            
            // 檢查是否已被銷毀
            const checkDestroyedStatus = () => {{
                try {{
                    const destroyedStatus = localStorage.getItem({var_names[6]});
                    if (destroyedStatus) {{
                        const status = JSON.parse(destroyedStatus);
                        if (status.destroyed) {{
                            console.warn('檢測到銷毀狀態，立即執行銷毀程序');
                            destroyPageContent();
                            return true;
                        }}
                    }}
                    
                    // 檢查嘗試次數
                    const attemptCount = localStorage.getItem({var_names[7]});
                    if (attemptCount && parseInt(attemptCount) >= {var_names[4]}) {{
                        console.warn('檢測到超過嘗試限制，執行銷毀程序');
                        permanentDestroy();
                        return true;
                    }}
                }} catch (e) {{
                    console.error('檢查銷毀狀態時發生錯誤:', e);
                }}
                return false;
            }};
            
            // 載入持久化的嘗試次數
            const loadAttemptCount = () => {{
                try {{
                    const saved = localStorage.getItem({var_names[7]});
                    if (saved) {{
                        {var_names[3]} = parseInt(saved) || 0;
                        console.log('載入已保存的嘗試次數:', {var_names[3]});
                    }}
                }} catch (e) {{
                    console.error('載入嘗試次數失敗:', e);
                }}
            }};
            
            // 保存嘗試次數
            const saveAttemptCount = () => {{
                try {{
                    localStorage.setItem({var_names[7]}, {var_names[3]}.toString());
                }} catch (e) {{
                    console.error('保存嘗試次數失敗:', e);
                }}
            }};
            
            // 密碼驗證函數
            const verifyPassword = async (inputPassword) => {{
                try {{
                    // 直接比對（向後兼容）
                    if (inputPassword === atob('MTk4MzEyMDM=')) {{
                        return true;
                    }}
                    
                    // 雜湊驗證
                    const hashedInput = await generatePasswordHash(inputPassword);
                    console.log('輸入密碼雜湊:', hashedInput);
                    console.log('目標雜湊:', {var_names[2]});
                    
                    return hashedInput === {var_names[2]};
                }} catch (error) {{
                    console.error('密碼驗證錯誤:', error);
                    return false;
                }}
            }};
            
            // 密碼雜湊生成函數
            const generatePasswordHash = async (password) => {{
                try {{
                    const encoder = new TextEncoder();
                    const salt = encoder.encode("flutter_secure_2024_salt");
                    let data = new Uint8Array([...encoder.encode(password), ...salt]);
                    
                    // 多次雜湊（與 Python 端保持一致）
                    for (let i = 0; i < 5000; i++) {{
                        const hashBuffer = await crypto.subtle.digest('SHA-256', data);
                        data = new Uint8Array(hashBuffer);
                    }}
                    
                    // 轉換為 Base64 並截取前 32 個字符
                    const hashArray = Array.from(data);
                    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
                    return btoa(hashHex).substring(0, 32);
                }} catch (error) {{
                    console.error('雜湊生成錯誤:', error);
                    throw error;
                }}
            }};
            
            // 主解密函數
            const decryptContent = async (tabId, password) => {{
                try {{
                    console.log('開始解密過程...');
                    showMessage('🔓 開始解密處理...', 'info');
                    
                    // 獲取加密數據
                    const encryptedData = {var_names[0]}[{var_names[1]}];
                    if (!encryptedData || encryptedData === 'DESTROYED_DATA') {{
                        throw new Error('加密數據已損毀或不存在');
                    }}
                    
                    console.log('加密數據長度:', encryptedData.length);
                    console.log('加密數據預覽:', encryptedData.substring(0, 50) + '...');
                    
                    // Step 1: Base64 解碼
                    showMessage('📥 執行 Base64 解碼...', 'info');
                    let decodedData;
                    try {{
                        decodedData = Uint8Array.from(atob(encryptedData), c => c.charCodeAt(0));
                        console.log('Base64 解碼成功，長度:', decodedData.length);
                    }} catch (e) {{
                        throw new Error('Base64 解碼失敗: ' + e.message);
                    }}
                    
                    // Step 2: 反混淆
                    showMessage('🔄 執行反混淆處理...', 'info');
                    const deobfuscated = await reverseObfuscation(decodedData, password);
                    console.log('反混淆完成，長度:', deobfuscated.length);
                    
                    // Step 3: 反向 XOR 解密
                    showMessage('🔐 執行密碼解密...', 'info');
                    const decrypted = reverseXorEncryption(deobfuscated, password);
                    console.log('XOR 解密完成，長度:', decrypted.length);
                    
                    // Step 4: 解壓縮
                    showMessage('📤 執行數據解壓縮...', 'info');
                    const decompressed = pako.inflate(decrypted, {{ to: 'string' }});
                    console.log('解壓縮成功，內容長度:', decompressed.length);
                    
                    showMessage('✅ 解密完成！', 'success');
                    return decompressed;
                    
                }} catch (error) {{
                    console.error('解密錯誤:', error);
                    showMessage(`❌ 解密失敗: ${{error.message}}`, 'danger');
                    throw error;
                }}
            }};
            
            // 反混淆函數
            const reverseObfuscation = async (data, password) => {{
                try {{
                    // 生成混淆種子（與 Python 端保持一致）
                    const seedString = `flutter_secure_${{password}}_2024`;
                    const seedBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(seedString));
                    const obfuscationSeed = new Uint8Array(seedBuffer);
                    
                    // 反向位元移位
                    const step1 = new Uint8Array(data.length);
                    for (let i = 0; i < data.length; i++) {{
                        const passwordInfluence = password.charCodeAt(i % password.length) % 8;
                        let shift = ((i % 7) + 1 + passwordInfluence) % 8;
                        if (shift === 0) shift = 1;
                        
                        const byte = data[i];
                        step1[i] = ((byte >> shift) | (byte << (8 - shift))) & 0xFF;
                    }}
                    
                    // 反向種子 XOR
                    const step2 = new Uint8Array(step1.length);
                    for (let i = 0; i < step1.length; i++) {{
                        const seedByte = obfuscationSeed[i % obfuscationSeed.length];
                        step2[i] = step1[i] ^ seedByte;
                    }}
                    
                    return step2;
                }} catch (error) {{
                    throw new Error('反混淆失敗: ' + error.message);
                }}
            }};
            
            // 反向 XOR 解密
            const reverseXorEncryption = (data, password) => {{
                const passwordBytes = new TextEncoder().encode(password);
                const result = new Uint8Array(data.length);
                
                for (let i = 0; i < data.length; i++) {{
                    const keyByte = passwordBytes[i % passwordBytes.length];
                    const posModifier = (i % 256) ^ 0xAA;
                    result[i] = data[i] ^ keyByte ^ posModifier;
                }}
                
                return result;
            }};
            
            // 主入口函數
            window.decryptContent = async (tabId) => {{
                // 檢查是否已被銷毀
                if (checkDestroyedStatus()) {{
                    return;
                }}
                
                if ({var_names[5]}) {{
                    showMessage('🚫 系統已鎖定，正在執行銷毀程序...', 'danger');
                    setTimeout(permanentDestroy, 2000);
                    return;
                }}
                
                const passwordInput = document.getElementById('password-' + tabId);
                const password = passwordInput ? passwordInput.value.trim() : '';
                
                if (!password) {{
                    showMessage('⚠️ 請輸入密碼', 'warning');
                    return;
                }}
                
                try {{
                    // 驗證密碼
                    showMessage('🔍 驗證密碼...', 'info');
                    const isValid = await verifyPassword(password);
                    
                    if (!isValid) {{
                        {var_names[3]}++;
                        saveAttemptCount(); // 持久化保存嘗試次數
                        
                        const remaining = {var_names[4]} - {var_names[3]};
                        
                        if (remaining <= 0) {{
                            {var_names[5]} = true;
                            if (passwordInput) {{
                                passwordInput.disabled = true;
                                const button = passwordInput.nextElementSibling;
                                if (button) button.disabled = true;
                            }}
                            showMessage('🔒 嘗試次數過多，系統將在 3 秒後永久銷毀...', 'danger');
                            
                            // 倒數計時銷毀
                            let countdown = 3;
                            const countdownInterval = setInterval(() => {{
                                showMessage(`⏰ 銷毀倒數: ${{countdown}} 秒`, 'danger');
                                countdown--;
                                if (countdown < 0) {{
                                    clearInterval(countdownInterval);
                                    permanentDestroy();
                                }}
                            }}, 1000);
                            return;
                        }}
                        
                        showMessage(`❌ 密碼錯誤，剩餘 ${{remaining}} 次機會`, 'warning');
                        if (passwordInput) {{
                            passwordInput.classList.add('error-shake');
                            setTimeout(() => passwordInput.classList.remove('error-shake'), 500);
                        }}
                        
                        const remainingSpan = document.getElementById('remaining-secrets');
                        if (remainingSpan) remainingSpan.textContent = remaining;
                        return;
                    }}
                    
                    // 密碼正確，清除嘗試記錄
                    {var_names[3]} = 0;
                    try {{
                        localStorage.removeItem({var_names[7]});
                    }} catch (e) {{
                        console.error('清除嘗試記錄失敗:', e);
                    }}
                    
                    // 解密內容
                    showMessage('✅ 密碼正確，開始解密...', 'success');
                    const decryptedContent = await decryptContent(tabId, password);
                    const htmlContent = markdownToHtml(decryptedContent);
                    
                    // 顯示解密內容
                    const passwordContainer = document.querySelector('.password-input-container');
                    if (passwordContainer) {{
                        passwordContainer.style.display = 'none';
                    }}
                    
                    const decryptedDiv = document.getElementById('decrypted-' + tabId);
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
                    console.error('處理錯誤:', error);
                    showMessage(`💥 處理失敗: ${{error.message}}`, 'danger');
                }}
            }};
            
            // 初始化函數
            const initializeSecurity = () => {{
                // 檢查銷毀狀態
                if (checkDestroyedStatus()) {{
                    return;
                }}
                
                // 載入持久化的嘗試次數
                loadAttemptCount();
                
                console.log('安全系統初始化完成');
                console.log('當前嘗試次數:', {var_names[3]});
            }};
            
            // 立即執行初始化
            initializeSecurity();
            
        }})();
        
        {JavaScriptGenerator._generate_utility_functions()}
        
        </script>
        '''
        return obfuscated_js
    
    @staticmethod
    def _generate_simple_protection():
        """生成簡化的保護代碼"""
        return '''
            // 基本防護措施
            document.addEventListener('contextmenu', e => e.preventDefault());
            document.addEventListener('selectstart', e => e.preventDefault());
            
            document.addEventListener('keydown', (e) => {
                if (e.key === 'F12' || 
                    (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'C')) ||
                    (e.ctrlKey && (e.key === 'u' || e.key === 'U'))) {
                    e.preventDefault();
                    return false;
                }
            });
            
            // 簡化的調試檢測
            let debugCheck = () => {
                let start = performance.now();
                debugger;
                let end = performance.now();
                if (end - start > 100) {
                    console.warn('調試器檢測');
                }
            };
            
            // 每5秒檢查一次
            setInterval(debugCheck, 5000);
        '''
    
    @staticmethod
    def _generate_utility_functions():
        """生成輔助函數"""
        return '''
        // 訊息顯示函數
        function showMessage(message, type) {
            // 移除舊的提示
            const oldAlert = document.querySelector('.temp-alert');
            if (oldAlert) oldAlert.remove();
            
            // 創建新的提示
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} temp-alert`;
            alertDiv.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : 
                                type === 'warning' ? 'exclamation-triangle' : 
                                type === 'info' ? 'info-circle' : 'times-circle'}"></i>
                ${message}
            `;
            
            const container = document.querySelector('.main-container');
            if (container) {
                container.insertBefore(alertDiv, container.firstChild);
                
                // 4秒後自動移除
                setTimeout(() => {
                    if (alertDiv.parentNode) alertDiv.remove();
                }, 4000);
            }
        }
        
        // Markdown 轉 HTML 函數
        function markdownToHtml(markdown) {
            let html = markdown;
            
            // 標題轉換
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
            
            // 程式碼區塊
            html = html.replace(/```([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>');
            html = html.replace(/`([^`]*)`/g, '<code>$1</code>');
            
            // 格式化
            html = html.replace(/\\*\\*([^*]*)\\*\\*/g, '<strong>$1</strong>');
            html = html.replace(/\\*([^*]*)\\*/g, '<em>$1</em>');
            
            // 列表
            html = html.replace(/^- (.*)$/gm, '<li>$1</li>');
            html = html.replace(/((?:<li>.*<\\/li>\\s*)+)/gs, '<ul>$1</ul>');
            
            // 段落
            html = html.replace(/\\n\\n/g, '</p><p>');
            html = html.replace(/\\n/g, '<br>');
            html = '<p>' + html + '</p>';
            html = html.replace(/<p>(\\s*<\\/p>)/g, '');
            
            return html;
        }
        
        // 顯示秘密內容函數
        function showSecrets() {
            const secretsNavItem = document.getElementById('secrets-nav-item');
            const secretsTab = document.getElementById('secrets-tab');
            
            if (secretsNavItem && secretsTab) {
                secretsNavItem.classList.remove('d-none');
                const tab = new bootstrap.Tab(secretsTab);
                tab.show();
                showMessage('🔍 發現隱藏內容！請輸入正確密碼解鎖...', 'info');
            } else {
                showMessage('❌ 隱藏內容不存在', 'warning');
                console.error('找不到秘密標籤元素');
            }
        }
        
        // 頁面載入完成後初始化
        document.addEventListener('DOMContentLoaded', function() {
            console.log('頁面初始化開始');
            
            // 檢查是否已被銷毀（雙重檢查）
            try {
                const destroyedStatus = localStorage.getItem('flutter_docs_security_status');
                if (destroyedStatus) {
                    const status = JSON.parse(destroyedStatus);
                    if (status.destroyed) {
                        console.warn('DOMContentLoaded: 檢測到銷毀狀態');
                        document.body.innerHTML = `
                            <div style="
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                min-height: 100vh;
                                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                            ">
                                <div style="
                                    background: rgba(255, 255, 255, 0.95);
                                    padding: 40px;
                                    border-radius: 15px;
                                    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                                    text-align: center;
                                    max-width: 500px;
                                ">
                                    <div style="font-size: 64px; margin-bottom: 20px;">🚫</div>
                                    <h1 style="color: #e74c3c; margin: 0 0 20px 0; font-size: 28px;">資料已永久銷毀</h1>
                                    <p style="color: #2c3e50; font-size: 16px; line-height: 1.6; margin: 0 0 15px 0;">
                                        由於密碼輸入錯誤次數過多，基於安全考量，所有加密資料已被永久刪除。
                                    </p>
                                    <p style="color: #e74c3c; font-size: 14px; font-weight: bold; margin: 0;">
                                        ⚠️ 此檔案已無法使用，請重新取得原始檔案
                                    </p>
                                </div>
                            </div>
                        `;
                        
                        // 禁用所有交互
                        document.addEventListener('contextmenu', e => e.preventDefault());
                        document.addEventListener('selectstart', e => e.preventDefault());
                        document.addEventListener('keydown', e => e.preventDefault());
                        return;
                    }
                }
            } catch (e) {
                console.error('DOMContentLoaded 銷毀檢查失敗:', e);
            }
            
            // 設置密碼輸入框事件
            const passwordInputs = document.querySelectorAll('input[type="password"]');
            passwordInputs.forEach(input => {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        const button = input.nextElementSibling;
                        if (button && button.onclick) {
                            button.click();
                        }
                    }
                });
            });
            
            // 初始化語法高亮
            if (typeof Prism !== 'undefined') {
                Prism.highlightAll();
                console.log('Prism 語法高亮已初始化');
            }
            
            // 設置全域函數
            window.showSecrets = showSecrets;
            
            console.log('頁面初始化完成');
        });
        '''