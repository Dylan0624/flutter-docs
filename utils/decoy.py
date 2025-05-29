import base64
import secrets

class Decoy:
    @staticmethod
    def create_decoy_data():
        """生成誘餌數據用於混淆。"""
        decoys = []
        for i in range(5):
            fake_content = f"Fake Content {i}: This is not the real content!"
            fake_encrypted = base64.b64encode(secrets.token_bytes(200)).decode()
            decoys.append(fake_encrypted)
        return decoys