import base64
import hashlib
import zlib
import secrets
import os

class Encryption:
    @staticmethod
    def advanced_encrypt(content, password):
        """
        改進但保持相容性的加密函數
        使用增強的多層加密，但確保前端能正確解密
        """
        try:
            # 第一層：壓縮（與原版保持一致）
            compressed = zlib.compress(content.encode('utf-8'), level=9)
            print(f"壓縮後長度: {len(compressed)}")
            
            # 第二層：密碼 XOR 加密（改進版）
            password_bytes = password.encode('utf-8')
            encrypted = bytearray()
            for i, byte in enumerate(compressed):
                # 使用更複雜的 XOR 模式
                key_byte = password_bytes[i % len(password_bytes)]
                pos_modifier = (i % 256) ^ 0xAA  # 添加位置相關的修飾
                encrypted.append(byte ^ key_byte ^ pos_modifier)
            
            print(f"XOR 加密後長度: {len(encrypted)}")
            
            # 第三層：混淆（增強版）
            obfuscated = Encryption.enhanced_obfuscate(bytes(encrypted), password)
            print(f"混淆後長度: {len(obfuscated)}")
            
            # 第四層：最終編碼
            final_result = base64.b64encode(obfuscated).decode()
            print(f"最終編碼長度: {len(final_result)}")
            
            return final_result
            
        except Exception as e:
            print(f"加密錯誤: {e}")
            return ""
    
    @staticmethod
    def enhanced_obfuscate(data, password):
        """增強的混淆函數"""
        # 生成基於密碼的混淆金鑰
        obfuscation_seed = hashlib.sha256(f"flutter_secure_{password}_2024".encode()).digest()
        
        # 第一次混淆：基於種子的 XOR
        result = bytearray()
        for i, byte in enumerate(data):
            seed_byte = obfuscation_seed[i % len(obfuscation_seed)]
            result.append(byte ^ seed_byte)
        
        # 第二次混淆：位元移位（改進版）
        final_result = bytearray()
        for i, byte in enumerate(result):
            # 使用密碼影響移位量
            password_influence = ord(password[i % len(password)]) % 8
            shift = ((i % 7) + 1 + password_influence) % 8
            if shift == 0:
                shift = 1
            shifted = ((byte << shift) | (byte >> (8 - shift))) & 0xFF
            final_result.append(shifted)
        
        return bytes(final_result)
    
    @staticmethod
    def generate_password_hash(password):
        """生成密碼驗證雜湊"""
        # 使用固定鹽值確保一致性
        salt = b"flutter_secure_2024_salt"
        combined = password.encode('utf-8') + salt
        
        # 多次雜湊
        hash_result = combined
        for _ in range(5000):  # 減少迭代次數以提高前端性能
            hash_result = hashlib.sha256(hash_result).digest()
        
        return base64.b64encode(hash_result).decode()[:32]
    
    @staticmethod
    def create_test_content():
        """創建測試內容用於驗證"""
        test_content = """# 測試機密內容

這是一個測試的機密文件。

## 重要信息
- 測試密碼: 19831203
- 加密狀態: 啟用
- 安全等級: 高

## 程式碼範例
```python
def secret_function():
    return "這是機密代碼"
```

記住：這只是測試內容！"""
        
        password = "19831203"
        encrypted = Encryption.advanced_encrypt(test_content, password)
        
        print("=== 測試加密結果 ===")
        print(f"原始內容長度: {len(test_content)}")
        print(f"加密結果長度: {len(encrypted)}")
        print(f"密碼雜湊: {Encryption.generate_password_hash(password)}")
        print(f"加密內容預覽: {encrypted[:100]}...")
        
        return encrypted

# 測試函數
if __name__ == "__main__":
    Encryption.create_test_content()