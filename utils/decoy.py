import base64
import secrets
import hashlib
import json

class Decoy:
    @staticmethod
    def create_decoy_data(real_length=None):
        """生成更逼真的誘餌數據"""
        decoys = []
        
        # 如果沒有指定長度，使用隨機長度
        if real_length is None:
            real_length = secrets.randbelow(2000) + 500
        
        # 生成多個不同類型的誘餌
        decoy_types = [
            Decoy._create_base64_decoy,
            Decoy._create_json_decoy,
            Decoy._create_compressed_decoy,
            Decoy._create_hex_decoy,
            Decoy._create_mixed_decoy
        ]
        
        for i in range(8):  # 生成8個誘餌
            decoy_func = secrets.choice(decoy_types)
            fake_length = real_length + secrets.randbelow(400) - 200
            fake_length = max(fake_length, 100)  # 確保最小長度
            decoy = decoy_func(fake_length)
            decoys.append(decoy)
        
        return decoys
    
    @staticmethod
    def _create_base64_decoy(length):
        """創建 Base64 格式的誘餌"""
        fake_data = secrets.token_bytes(length * 3 // 4)
        return base64.b64encode(fake_data).decode()
    
    @staticmethod
    def _create_json_decoy(length):
        """創建 JSON 格式的誘餌（模擬真實加密數據結構）"""
        fake_salt = base64.b64encode(secrets.token_bytes(32)).decode()
        fake_iv = base64.b64encode(secrets.token_bytes(12)).decode()
        fake_data = base64.b64encode(secrets.token_bytes(length // 2)).decode()
        fake_tag = base64.b64encode(secrets.token_bytes(16)).decode()
        
        fake_structure = {
            "salt": fake_salt,
            "iv": fake_iv,
            "data": fake_data,
            "tag": fake_tag,
            "method": "aes-256-gcm"
        }
        
        json_str = json.dumps(fake_structure, separators=(',', ':'))
        return base64.b64encode(json_str.encode()).decode()
    
    @staticmethod
    def _create_compressed_decoy(length):
        """創建壓縮數據格式的誘餌"""
        # 創建看起來像壓縮數據的模式
        fake_data = bytearray()
        for _ in range(length):
            if secrets.randbelow(10) < 3:  # 30% 機率重複字節
                fake_data.append(fake_data[-1] if fake_data else 0)
            else:
                fake_data.append(secrets.randbelow(256))
        
        return base64.b64encode(bytes(fake_data)).decode()
    
    @staticmethod
    def _create_hex_decoy(length):
        """創建十六進制格式的誘餌"""
        fake_hex = secrets.token_hex(length // 2)
        return base64.b64encode(fake_hex.encode()).decode()
    
    @staticmethod
    def _create_mixed_decoy(length):
        """創建混合格式的誘餌"""
        # 模擬多層編碼的數據
        stage1 = secrets.token_bytes(length // 3)
        stage2 = base64.b64encode(stage1).decode().encode()
        stage3 = hashlib.sha256(stage2).digest() + stage2
        return base64.b64encode(stage3).decode()
    
    @staticmethod
    def create_realistic_metadata():
        """創建逼真的元數據"""
        fake_timestamps = [
            secrets.randbelow(1000000) + 1600000000,  # 2020年後的時間戳
            secrets.randbelow(1000000) + 1640000000   # 2022年後的時間戳
        ]
        
        fake_versions = ["1.0", "1.1", "2.0", "2.1", "3.0"]
        fake_methods = ["aes-256-gcm", "chacha20-poly1305", "aes-256-cbc"]
        
        return {
            "created": secrets.choice(fake_timestamps),
            "modified": secrets.choice(fake_timestamps),
            "version": secrets.choice(fake_versions),
            "method": secrets.choice(fake_methods),
            "checksum": hashlib.md5(secrets.token_bytes(32)).hexdigest()
        }