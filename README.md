# 文檔加密系統

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
- **🔥 永久銷毀機制**：密碼錯誤3次後自動永久銷毀所有加密資料

### 🔒 進階安全功能
- **持久化安全記錄**：使用 LocalStorage 永久記錄嘗試次數和銷毀狀態
- **防重置攻擊**：即使重新整理頁面或重新開啟瀏覽器，銷毀狀態依然有效
- **倒數計時銷毀**：最後一次錯誤密碼後，系統會進行3秒倒數計時再執行銷毀
- **完全不可逆**：一旦銷毀，只有清除瀏覽器所有資料才能復原（需要重新取得原始檔案）

### 📖 優秀的使用體驗
- **響應式設計**：支援桌面、平板、手機等各種設備
- **分頁式介面**：清晰的內容組織，易於導航
- **程式碼高亮**：自動語法高亮和複製功能
- **隱藏內容發現**：點擊火箭圖標🚀發現加密內容
- **視覺化銷毀警告**：精美的銷毀警告介面和倒數計時

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
│   ├── javascript.py      # JavaScript 生成（含永久銷毀功能）
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

### 🔥 永久銷毀機制

**銷毀觸發條件**：
- 密碼輸入錯誤達到 3 次時自動觸發
- 系統會進行 3 秒倒數計時後執行銷毀

**銷毀過程**：
1. **記錄銷毀狀態**：將銷毀狀態永久保存到瀏覽器 LocalStorage
2. **清空加密資料**：將所有加密數據替換為 "DESTROYED_DATA" 標記
3. **替換頁面內容**：顯示專業的銷毀提示頁面
4. **禁用所有交互**：完全禁用滑鼠和鍵盤交互

**銷毀特性**：
- ✅ **永久性**：即使重新整理頁面、關閉瀏覽器重開，銷毀狀態依然有效
- ✅ **不可逆性**：一旦銷毀，無法透過任何前端操作復原
- ✅ **持久性**：嘗試次數會被永久記錄，防止重置攻擊
- ⚠️ **復原方式**：只有清除瀏覽器的所有 LocalStorage 資料才能復原（但需要重新取得原始 HTML 檔案）

**安全提醒**：
```html
🚫 資料已永久銷毀
由於密碼輸入錯誤次數過多，基於安全考量，所有加密資料已被永久刪除。
⚠️ 此檔案已無法使用，請重新取得原始檔案
```

### 安全限制
⚠️ **重要提醒**：這是客戶端加密方案，雖然大幅提高破解難度，但理論上存在被破解的可能性。

**適用場景**：
- ✅ 防止一般使用者意外查看機密資訊
- ✅ 增加技術門檻，阻擋大部分破解嘗試
- ✅ 滿足內部交接的安全需求
- ✅ 防止密碼暴力破解攻擊（永久銷毀機制）

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

### ⚠️ 密碼輸入注意事項

**重要提醒**：請謹慎輸入密碼，因為：

- 🔢 **僅有 3 次機會**：密碼輸入錯誤超過 3 次會觸發永久銷毀
- ⏰ **倒數計時**：第3次錯誤後會有 3 秒倒數計時
- 🚫 **永久銷毀**：一旦銷毀，即使重新整理頁面也無法復原
- 🔄 **復原困難**：需要清除瀏覽器資料並重新取得原始檔案

**建議操作流程**：
1. 先完整閱讀公開內容尋找密碼線索
2. 確認密碼後再嘗試輸入
3. 如不確定，建議先備份 HTML 檔案

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
        <br>
        <small class="text-danger">⚠️ 注意：僅有3次輸入機會，錯誤3次後資料將被永久銷毀！</small>
    </div>
</div>
```

您可以在 `utils/html_template.py` 中修改這段提示文字：
```python
# 搜尋這段代碼並修改提示內容
<strong>提示：</strong>您的自定義提示文字 😉
<small class="text-muted">您的詳細提示...</small>
<small class="text-danger">⚠️ 注意：僅有3次輸入機會，錯誤3次後資料將被永久銷毀！</small>
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

### 🔒 高安全性交接場景

特別適合以下需要高安全性的場景：

**敏感資料交接**：
- 包含生產環境密碼、API 金鑰的技術文檔
- 離職交接時需要確保資料不被惡意獲取
- 限制特定人員才能存取的機密資訊

**培訓教材保護**：
- 企業內部培訓資料，防止外洩
- 付費課程內容，防止盜版分享
- 考試題庫或答案，防止作弊洩題

**臨時分享場景**：
- 需要分享給特定人員，但擔心檔案被轉發
- 會議資料包含敏感資訊，需要控制存取次數
- 緊急情況下的資料交接，確保安全性

## 🔧 故障排除

### 常見問題

**Q: 我忘記密碼了怎麼辦？**
A: 如果還有嘗試機會，請仔細閱讀公開內容尋找線索。如果已經銷毀，只能重新取得原始 HTML 檔案。

**Q: 可以增加嘗試次數嗎？**
A: 可以在 `utils/javascript.py` 中修改 `{var_names[4]} = 3` 這行，將 3 改為其他數字。

**Q: 如何清除銷毀狀態？**
A: 在瀏覽器中按 F12 → Application → Local Storage → 刪除相關項目，或者清除瀏覽器所有資料。

**Q: 能否關閉永久銷毀功能？**
A: 可以在 `utils/javascript.py` 中註解掉銷毀相關代碼，但不建議這樣做，因為會降低安全性。

### 技術支援

如果遇到技術問題，請：
1. 檢查瀏覽器控制台是否有錯誤訊息
2. 確認瀏覽器支援所需的 JavaScript 功能
3. 嘗試在不同瀏覽器中開啟

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

### 安全性改進建議

如果您想貢獻安全性相關的改進，建議的方向：

- **加密強度提升**：實作更強的加密算法
- **反調試增強**：增加更多反調試檢測
- **伺服器端驗證**：加入可選的伺服器端密碼驗證
- **多因子認證**：實作時間基準或其他驗證方式

## 📄 授權條款

MIT License - 詳見 LICENSE 檔案

## 🙋‍♂️ 支持與回饋

如果這個專案對您有幫助，歡迎：
- ⭐ 給專案加星
- 🐛 回報問題
- 💡 提出建議
- 🤝 貢獻程式碼

## 🔐 版本更新記錄

### v2.0.0 - 永久銷毀機制
- 🔥 新增永久銷毀功能，密碼錯誤3次後自動銷毀
- 💾 持久化安全記錄，防止重置攻擊
- ⏰ 倒數計時銷毀，增加視覺警告
- 🎨 美化銷毀警告介面

### v1.0.0 - 基礎版本
- 📖 多層加密文檔系統
- 🎯 響應式使用者介面
- 🔒 基本密碼保護機制

---

**記住**：好的交接不只是留下程式碼，更要留下知識和經驗。這個工具可以幫助您安全地傳承珍貴的技術資產，現在更加入了永久銷毀機制來確保最高等級的安全保護！ 🚀🔒