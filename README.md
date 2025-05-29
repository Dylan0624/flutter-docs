# Flutter 文檔加密系統

> 🔐 為有交接需求但希望保護敏感資訊的開發者量身打造的安全文檔系統

## 🎯 專案目標

這個專案專為以下情境設計：
- **技術交接**：離職前需要留下完整的技術文檔給後續同事
- **知識傳承**：希望分享經驗但需要保護敏感資訊（如密碼、API 金鑰、內部流程）
- **分層授權**：公開基礎知識，重要內容需要密碼驗證
- **安全分享**：既要方便閱讀，又要確保機密資訊不會被輕易獲取

## ✨ 主要特色

### 🛡️ 多層加密保護
- **四層加密機制**：壓縮 → XOR 加密 → 混淆 → Base64 編碼
- **密碼雜湊驗證**：使用 PBKDF2 + SHA256 確保密碼安全
- **誘餌數據混淆**：生成多個假加密數據迷惑攻擊者
- **防調試保護**：檢測開發者工具，增加破解難度

### 📖 優秀的使用體驗
- **響應式設計**：支援桌面、平板、手機等各種設備
- **分頁式介面**：清晰的內容組織，易於導航
- **程式碼高亮**：自動語法高亮和複製功能
- **隱藏內容發現**：點擊火箭圖標🚀發現加密內容

### 🔧 簡單易用
- **一鍵建置**：執行 Python 腳本即可生成完整的 HTML 文檔
- **單檔案輸出**：所有內容打包成一個 HTML 檔案，方便分享
- **無需伺服器**：可以直接在瀏覽器中開啟，無需架設伺服器

## 🚀 快速開始

### 環境需求

```bash
Python 3.7+
pip install markdown cryptography
```

### 目錄結構

```
project/
├── main.py                 # 主執行檔案
├── utils/
│   ├── __init__.py
│   ├── builder.py         # 主要建構器
│   ├── config.py          # 配置檔案
│   ├── encryption.py      # 加密功能
│   ├── html_template.py   # HTML 模板生成
│   ├── javascript.py      # JavaScript 生成
│   ├── markdown_processor.py # Markdown 處理
│   └── decoy.py          # 誘餌數據生成
├── content/               # 您的 Markdown 文檔目錄
│   ├── 01_introduction.md
│   ├── 02_setup.md
│   ├── ...
│   └── secrets.md        # 機密內容（會被加密）
└── flutter-docs.html     # 生成的文檔（輸出）
```

### 使用步驟

1. **準備您的文檔**
   ```bash
   mkdir content
   # 將您的 Markdown 檔案放入 content 目錄
   ```

2. **配置密碼**（可選）
   ```python
   # 編輯 utils/config.py
   class Config:
       SECRET_PASSWORD = "your_secret_password"  # 修改為您的密碼
   ```

3. **執行建置**
   ```bash
   python main.py
   ```

4. **開啟文檔**
   ```bash
   # 在瀏覽器中開啟生成的 flutter-docs.html
   ```

## 📝 文檔格式要求

### 檔案命名規則

文檔檔案需要遵循特定的命名格式以確保正確的排序：

```
格式：數字前綴 + 描述性名稱 + .md
範例：
├── 01_introduction.md        # 第1章：介紹
├── 02_environment_setup.md   # 第2章：環境設置
├── 03_basic_concepts.md      # 第3章：基本概念
├── 10_advanced_topics.md     # 第10章：進階主題
└── secrets.md               # 機密內容（固定檔名，會被加密）
```

### Markdown 格式規範

#### 標題結構
```markdown
# 主標題（會成為分頁標題）
每個檔案應該有一個主標題作為分頁名稱。

## 二級標題
### 三級標題
#### 四級標題
```

#### 程式碼區塊
````markdown
```python
# Python 程式碼範例
def hello_world():
    print("Hello, World!")
```

```dart
// Dart/Flutter 程式碼範例
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      home: MyHomePage(),
    );
  }
}
```
````

#### 重要資訊標記
```markdown
**重要：** 這是重要資訊

*斜體強調*

> 引用區塊
> 用於提醒或警告資訊

- 無序列表項目1
- 無序列表項目2

1. 有序列表項目1
2. 有序列表項目2
```

#### 連結和圖片
```markdown
[文字連結](https://example.com)

![圖片說明](image-url.png)
```

### 機密內容檔案

特殊檔案 `secrets.md` 會被自動加密：

```markdown
# 機密資訊

## 資料庫密碼
- 生產環境：your_production_password
- 測試環境：your_test_password

## API 金鑰
```
FLUTTER_API_KEY=your_secret_api_key
FIREBASE_CONFIG=your_firebase_config
```

## 內部流程
1. 部署流程的詳細步驟
2. 緊急處理程序
3. 聯絡人資訊
```

## 🔧 自定義配置

### 修改主題樣式

您可以編輯 `utils/html_template.py` 中的 CSS 樣式：

```python
# 修改主題顏色
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  # 漸層背景
color: #2c3e50;  # 文字顏色
```

### 更改密碼

```python
# utils/config.py
class Config:
    SECRET_PASSWORD = "your_new_password"  # 更改此處
```

### 自定義輸出檔名

```python
# utils/config.py
class Config:
    OUTPUT_FILE = "my-custom-docs.html"  # 更改輸出檔名
```

## 🛡️ 安全性說明

### 加密強度
- **多層加密**：使用壓縮+XOR+混淆+編碼的四層保護
- **密碼強化**：PBKDF2 + SHA256，5000次迭代
- **誘餌防護**：生成8個假數據混淆攻擊者
- **前端保護**：禁用右鍵、F12、選取等功能

### 安全限制
⚠️ **重要提醒**：這是客戶端加密方案，雖然大幅提高破解難度，但理論上存在被破解的可能性。

**適用場景**：
- ✅ 防止一般使用者意外查看機密資訊
- ✅ 增加技術門檻，阻擋大部分破解嘗試
- ✅ 滿足內部交接的安全需求

**不適用場景**：
- ❌ 對抗專業駭客的攻擊
- ❌ 處理極度機密的國家機密資訊
- ❌ 法律合規要求的最高等級加密

## 📱 使用方式

### 開啟文檔
1. 在瀏覽器中開啟生成的 HTML 檔案
2. 瀏覽公開內容
3. 點擊右上角的🚀圖標發現隱藏內容
4. 輸入密碼解鎖機密資訊

### 密碼提示機制

系統預設密碼為 `19831203`，但您可以透過以下方式自定義密碼和提示：

#### 修改密碼位置
```python
# utils/config.py
class Config:
    SECRET_PASSWORD = "your_custom_password"  # 在此修改密碼
```

#### 密碼提示策略
建議在公開內容中自然地埋入密碼線索，例如：

**數字暗示**：
```markdown
# 02_project_history.md
這個專案於 1983年12月03日 開始規劃...
## 🎯 實作練習
請嘗試使用日期格式 YYYYMMDD 完成以下任務...
```

**程式碼註解暗示**：
```markdown
# 03_configuration.md
```python
# 專案創建日期：19831203
def initialize_project():
    pass
```

**自然文字暗示**：
```markdown
# 01_introduction.md
...記住重要的里程碑日期，它們往往是開啟下一階段的鑰匙 🔑
特別是 🎯 實作練習 部分，完成後您將獲得更多深入資訊。
```

#### 提示文字位置
提示會顯示在加密內容的解鎖頁面：
```html
<div class="password-hint">
    <div class="alert alert-info">
        <i class="fas fa-lightbulb"></i>
        <strong>提示：</strong>閱讀完整份文件即可知道密碼 😉
        <br>
        <small class="text-muted">仔細的做完每個練習 (🎯 實作練習)，密碼可能就在某個地方...</small>
    </div>
</div>
```

您可以在 `utils/html_template.py` 中修改這段提示文字：
```python
# 搜尋這段代碼並修改提示內容
<strong>提示：</strong>您的自定義提示文字 😉
<small class="text-muted">您的詳細提示...</small>
```

## 🎯 使用場景

### 技術交接
```markdown
# 01_project_overview.md
這個專案使用 Flutter 開發，主要功能包括...
請特別注意 secrets 部分的配置資訊。

# secrets.md (加密)
生產環境資料庫：
username: admin
password: prod_password_2024
```

### 教學文檔
```markdown
# 02_flutter_basics.md
Flutter 基礎教學內容...

# secrets.md (加密)
高級技巧和最佳實踐：
- 性能優化秘訣
- 常見陷阱避免
- 內部工具使用方法
```

### 團隊知識庫
```markdown
# 03_team_processes.md
團隊開發流程...

# secrets.md (加密)
內部工具賬號：
- Jenkins: admin/password123
- 監控系統: monitor/secret456
- 部署腳本位置和使用方法
```

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 開發環境設置
```bash
git clone <repository>
cd flutter-docs-builder
pip install -r requirements.txt
python main.py
```

### 測試
```bash
# 建立測試內容
mkdir content
echo "# Test Document" > content/01_test.md
echo "# Secret Content" > content/secrets.md
python main.py
```

## 📄 授權條款

MIT License - 詳見 LICENSE 檔案

## 🙋‍♂️ 支持與回饋

如果這個專案對您有幫助，歡迎：
- ⭐ 給專案加星
- 🐛 回報問題
- 💡 提出建議
- 🤝 貢獻程式碼

---

**記住**：好的交接不只是留下程式碼，更要留下知識和經驗。這個工具可以幫助您安全地傳承珍貴的技術資產！ 🚀