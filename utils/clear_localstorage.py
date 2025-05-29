#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文檔加密系統 - LocalStorage 清除工具
用於清除瀏覽器中的安全狀態記錄，復原被永久銷毀的文檔

版本: 1.0.0
作者: Flutter Docs Security Team
"""

import os
import sys
import json
import sqlite3
import shutil
import platform
from pathlib import Path
from typing import List, Dict, Optional

class LocalStorageCleaner:
    """LocalStorage 清除器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.cleaned_items = []
        self.errors = []
        
    def get_browser_paths(self) -> Dict[str, List[str]]:
        """獲取各瀏覽器的 LocalStorage 路徑"""
        paths = {}
        
        if self.system == "windows":
            user_home = os.path.expanduser("~")
            paths = {
                "Chrome": [
                    f"{user_home}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Storage",
                    f"{user_home}\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1\\Local Storage",
                ],
                "Edge": [
                    f"{user_home}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Storage",
                ],
                "Firefox": [
                    f"{user_home}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles",
                ],
                "Opera": [
                    f"{user_home}\\AppData\\Roaming\\Opera Software\\Opera Stable\\Local Storage",
                ],
            }
        elif self.system == "darwin":  # macOS
            user_home = os.path.expanduser("~")
            paths = {
                "Chrome": [
                    f"{user_home}/Library/Application Support/Google/Chrome/Default/Local Storage",
                    f"{user_home}/Library/Application Support/Google/Chrome/Profile 1/Local Storage",
                ],
                "Safari": [
                    f"{user_home}/Library/Safari/LocalStorage",
                ],
                "Firefox": [
                    f"{user_home}/Library/Application Support/Firefox/Profiles",
                ],
                "Opera": [
                    f"{user_home}/Library/Application Support/com.operasoftware.Opera/Local Storage",
                ],
            }
        else:  # Linux
            user_home = os.path.expanduser("~")
            paths = {
                "Chrome": [
                    f"{user_home}/.config/google-chrome/Default/Local Storage",
                    f"{user_home}/.config/google-chrome/Profile 1/Local Storage",
                ],
                "Firefox": [
                    f"{user_home}/.mozilla/firefox",
                ],
                "Opera": [
                    f"{user_home}/.config/opera/Local Storage",
                ],
            }
        
        return paths
    
    def find_flutter_docs_entries(self, db_path: str) -> List[Dict]:
        """在 LocalStorage 資料庫中尋找相關條目"""
        entries = []
        
        try:
            if not os.path.exists(db_path):
                return entries
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 查詢包含 flutter_docs 相關的鍵
            cursor.execute("""
                SELECT key, value FROM ItemTable 
                WHERE key LIKE '%flutter_docs%' 
                   OR key LIKE '%security_status%' 
                   OR key LIKE '%attempt_count%'
            """)
            
            for row in cursor.fetchall():
                entries.append({
                    'key': row[0],
                    'value': row[1],
                    'db_path': db_path
                })
            
            conn.close()
            
        except Exception as e:
            self.errors.append(f"讀取資料庫失敗 {db_path}: {str(e)}")
        
        return entries
    
    def clear_entries(self, entries: List[Dict]) -> int:
        """清除指定的 LocalStorage 條目"""
        cleared_count = 0
        
        for entry in entries:
            try:
                conn = sqlite3.connect(entry['db_path'])
                cursor = conn.cursor()
                
                # 刪除條目
                cursor.execute("DELETE FROM ItemTable WHERE key = ?", (entry['key'],))
                conn.commit()
                conn.close()
                
                self.cleaned_items.append({
                    'key': entry['key'],
                    'db_path': entry['db_path']
                })
                cleared_count += 1
                
            except Exception as e:
                self.errors.append(f"清除條目失敗 {entry['key']}: {str(e)}")
        
        return cleared_count
    
    def scan_and_clean(self, target_browsers: List[str] = None, dry_run: bool = False) -> Dict:
        """掃描並清除 LocalStorage 資料"""
        print("🔍 開始掃描瀏覽器 LocalStorage...")
        
        browser_paths = self.get_browser_paths()
        found_entries = []
        
        # 如果沒有指定瀏覽器，掃描所有支援的瀏覽器
        if target_browsers is None:
            target_browsers = list(browser_paths.keys())
        
        for browser in target_browsers:
            if browser not in browser_paths:
                print(f"⚠️  不支援的瀏覽器: {browser}")
                continue
                
            print(f"\n📋 檢查 {browser}...")
            
            for path in browser_paths[browser]:
                if browser == "Firefox":
                    # Firefox 使用不同的資料庫結構
                    found_entries.extend(self._scan_firefox(path))
                else:
                    # Chrome/Edge/Opera 等基於 Chromium 的瀏覽器
                    db_file = os.path.join(path, "leveldb")
                    if os.path.exists(db_file):
                        # LevelDB 格式較複雜，使用備用方法
                        found_entries.extend(self._scan_chromium_alternative(path))
                    else:
                        # 嘗試舊版 SQLite 格式
                        db_file = os.path.join(path, "Local Storage", "leveldb")
                        if os.path.exists(db_file):
                            found_entries.extend(self._scan_chromium_alternative(path))
        
        print(f"\n📊 掃描結果:")
        print(f"   找到 {len(found_entries)} 個相關條目")
        
        if found_entries:
            print("\n🔍 發現的條目:")
            for i, entry in enumerate(found_entries, 1):
                print(f"   {i}. {entry['key']} ({entry.get('browser', 'Unknown')})")
        
        if dry_run:
            print("\n🔒 試運行模式 - 不會實際刪除資料")
            return {
                'found_count': len(found_entries),
                'cleared_count': 0,
                'dry_run': True,
                'entries': found_entries
            }
        
        # 執行清除
        if found_entries:
            response = input(f"\n❓ 確定要清除這 {len(found_entries)} 個條目嗎? (y/N): ")
            if response.lower() in ['y', 'yes', '是']:
                cleared_count = self._manual_clear_entries(found_entries)
                print(f"\n✅ 成功清除 {cleared_count} 個條目")
            else:
                print("\n❌ 取消清除操作")
                cleared_count = 0
        else:
            print("\n💡 沒有找到需要清除的條目")
            cleared_count = 0
        
        return {
            'found_count': len(found_entries),
            'cleared_count': cleared_count,
            'dry_run': False,
            'entries': found_entries,
            'errors': self.errors
        }
    
    def _scan_firefox(self, profiles_path: str) -> List[Dict]:
        """掃描 Firefox 的 LocalStorage"""
        entries = []
        
        if not os.path.exists(profiles_path):
            return entries
        
        try:
            # 找到所有 profile 目錄
            for item in os.listdir(profiles_path):
                profile_path = os.path.join(profiles_path, item)
                if os.path.isdir(profile_path):
                    storage_path = os.path.join(profile_path, "webappsstore.sqlite")
                    if os.path.exists(storage_path):
                        # Firefox 使用不同的資料庫結構
                        conn = sqlite3.connect(storage_path)
                        cursor = conn.cursor()
                        
                        cursor.execute("""
                            SELECT key, value FROM webappsstore2
                            WHERE key LIKE '%flutter_docs%' 
                               OR key LIKE '%security_status%' 
                               OR key LIKE '%attempt_count%'
                        """)
                        
                        for row in cursor.fetchall():
                            entries.append({
                                'key': row[0],
                                'value': row[1],
                                'db_path': storage_path,
                                'browser': 'Firefox'
                            })
                        
                        conn.close()
        except Exception as e:
            self.errors.append(f"Firefox 掃描失敗: {str(e)}")
        
        return entries
    
    def _scan_chromium_alternative(self, storage_path: str) -> List[Dict]:
        """掃描 Chromium 系瀏覽器的 LocalStorage (替代方法)"""
        entries = []
        
        try:
            # 檢查 LevelDB 資料夾
            leveldb_path = os.path.join(storage_path, "leveldb")
            if os.path.exists(leveldb_path):
                # 使用檔案搜尋的方式尋找相關資料
                for file in os.listdir(leveldb_path):
                    if file.endswith(('.log', '.ldb')):
                        file_path = os.path.join(leveldb_path, file)
                        try:
                            with open(file_path, 'rb') as f:
                                content = f.read()
                                # 搜尋包含關鍵字的資料
                                if b'flutter_docs' in content or b'security_status' in content:
                                    entries.append({
                                        'key': 'flutter_docs_related_data',
                                        'value': 'Found in binary data',
                                        'file_path': file_path,
                                        'browser': 'Chromium-based'
                                    })
                        except Exception:
                            continue
        except Exception as e:
            self.errors.append(f"Chromium 掃描失敗: {str(e)}")
        
        return entries
    
    def _manual_clear_entries(self, entries: List[Dict]) -> int:
        """手動清除條目"""
        cleared = 0
        
        for entry in entries:
            try:
                if 'file_path' in entry:
                    # 針對 LevelDB 檔案，我們需要更謹慎的處理
                    print(f"   警告: 無法直接清除 LevelDB 格式的資料")
                    print(f"   建議: 關閉瀏覽器後刪除整個 LocalStorage 資料夾")
                    print(f"   路徑: {os.path.dirname(entry['file_path'])}")
                elif 'db_path' in entry:
                    # SQLite 資料庫格式
                    conn = sqlite3.connect(entry['db_path'])
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM webappsstore2 WHERE key = ?", (entry['key'],))
                    conn.commit()
                    conn.close()
                    cleared += 1
                    print(f"   ✅ 已清除: {entry['key']}")
            except Exception as e:
                self.errors.append(f"清除失敗 {entry.get('key', 'Unknown')}: {str(e)}")
                print(f"   ❌ 清除失敗: {entry.get('key', 'Unknown')}")
        
        return cleared
    
    def generate_manual_instructions(self) -> str:
        """生成手動清除指南"""
        instructions = """
🔧 手動清除 LocalStorage 指南

如果自動清除工具無法正常工作，您可以手動清除瀏覽器資料：

📋 方法一：使用瀏覽器開發者工具
1. 開啟包含加密文檔的網頁
2. 按 F12 開啟開發者工具
3. 切換到 "Application" 或"應用程式" 標籤
4. 在左側選擇 "Local Storage"
5. 找到並刪除以下鍵值：
   - flutter_docs_security_status
   - flutter_docs_attempt_count
   - 或任何包含 "flutter_docs" 的項目

📋 方法二：清除瀏覽器所有資料
Chrome/Edge:
1. 按 Ctrl+Shift+Delete (Windows) 或 Cmd+Shift+Delete (Mac)
2. 選擇 "所有時間"
3. 勾選 "Cookie 和其他網站資料"
4. 點擊 "清除資料"

Firefox:
1. 按 Ctrl+Shift+Delete (Windows) 或 Cmd+Shift+Delete (Mac)
2. 選擇 "所有內容"
3. 勾選 "Cookie" 和 "網站資料"
4. 點擊 "立即清除"

📋 方法三：直接刪除資料夾（需關閉瀏覽器）
"""
        
        browser_paths = self.get_browser_paths()
        for browser, paths in browser_paths.items():
            instructions += f"\n{browser}:\n"
            for path in paths:
                instructions += f"   {path}\n"
        
        instructions += """
⚠️  注意事項：
- 關閉所有瀏覽器視窗後再刪除資料夾
- 這會清除所有網站的 LocalStorage 資料
- 建議先備份重要的瀏覽器資料

🔄 清除後：
重新開啟加密文檔即可正常使用（需要原始 HTML 檔案）
"""
        
        return instructions

def main():
    """主函數"""
    print("=" * 60)
    print("🔧 文檔加密系統 - LocalStorage 清除工具")
    print("=" * 60)
    
    cleaner = LocalStorageCleaner()
    
    # 解析命令列參數
    import argparse
    parser = argparse.ArgumentParser(description='清除文檔加密系統的 LocalStorage 資料')
    parser.add_argument('--browsers', nargs='+', 
                       help='指定要清除的瀏覽器 (Chrome, Firefox, Edge, Safari, Opera)')
    parser.add_argument('--dry-run', action='store_true',
                       help='試運行模式，不實際刪除資料')
    parser.add_argument('--manual', action='store_true',
                       help='顯示手動清除指南')
    
    args = parser.parse_args()
    
    if args.manual:
        print(cleaner.generate_manual_instructions())
        return
    
    try:
        # 執行掃描和清除
        result = cleaner.scan_and_clean(
            target_browsers=args.browsers,
            dry_run=args.dry_run
        )
        
        # 顯示結果摘要
        print("\n" + "="*50)
        print("📊 執行摘要:")
        print(f"   找到條目: {result['found_count']}")
        print(f"   清除條目: {result['cleared_count']}")
        if result['errors']:
            print(f"   錯誤數量: {len(result['errors'])}")
        print("="*50)
        
        if result['errors']:
            print("\n❌ 錯誤訊息:")
            for error in result['errors']:
                print(f"   {error}")
        
        if result['found_count'] == 0:
            print("\n💡 提示:")
            print("   - 確認瀏覽器已關閉")
            print("   - 嘗試使用 --manual 參數查看手動清除指南")
            print("   - 檢查是否在正確的作業系統上執行")
        
        if result['cleared_count'] > 0:
            print("\n✅ 清除成功！現在可以重新開啟加密文檔了。")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
    except Exception as e:
        print(f"\n❌ 執行失敗: {str(e)}")
        print("\n💡 建議使用 --manual 參數查看手動清除指南")

if __name__ == "__main__":
    main()