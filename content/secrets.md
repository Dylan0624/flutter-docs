# 私人開發秘訣

## 🤫 專案經驗

### 客戶 A 專案
- API 回應慢，需要增加 timeout 處理
- iOS 審核被拒絕過一次，原因是缺少隱私權說明

### 踩過的坑
1. **initState 陷阱**：不要在 initState 中直接呼叫 setState
2. **記憶體洩漏**：記得在 dispose 中取消訂閱
3. **鍵盤遮擋**：使用 Scaffold 的 resizeToAvoidBottomInset

## 💰 接案經驗
- 報價要包含測試和上架時間
- 客戶需求變更要另外收費
- 保留原始碼的權利很重要

> **💡 重要**  
> 這些經驗來自實際專案，非常寶貴！
