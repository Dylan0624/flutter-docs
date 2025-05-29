import base64
import hashlib
import zlib

class Encryption:
    # 固定的鹽值和 IV，基於密碼生成
    @staticmethod
    def get_fixed_salt(password):
        """根據密碼生成固定的鹽值"""
        return hashlib.sha256(f"salt_{password}_flutter".encode()).digest()[:32]
    
    @staticmethod
    def get_fixed_iv(password):
        """根據密碼生成固定的 IV"""
        return hashlib.sha256(f"iv_{password}_2024".encode()).digest()[:16]
    
    @staticmethod
    def advanced_encrypt(content, password):
        """執行簡化的固定加密（壓縮 + Base64 + 簡單混淆）。"""
        # 第一層：壓縮
        compressed = zlib.compress(content.encode('utf-8'))
        
        # 第二層：簡單的 XOR 加密（使用密碼）
        password_bytes = password.encode('utf-8')
        encrypted = bytearray()
        for i, byte in enumerate(compressed):
            encrypted.append(byte ^ password_bytes[i % len(password_bytes)])
        
        # 第三層：混淆 (XOR with fixed key)
        obfuscated = Encryption.obfuscate_data(bytes(encrypted))
        
        # 第四層：Base64 編碼
        return base64.b64encode(obfuscated).decode()
    
    @staticmethod
    def obfuscate_data(data):
        """使用 XOR 混淆數據。"""
        key = b'flutter_obfuscation_key_2024'
        return bytes(a ^ key[i % len(key)] for i, a in enumerate(data))