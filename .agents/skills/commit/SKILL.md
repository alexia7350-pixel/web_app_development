---
name: commit
description: 儲存變更（Commit）。用於專案的各個階段完成後，自動將程式碼變更或文件產出提交到 Git 儲存庫，並撰寫具結構化的提交訊息。
---

# Commit Skill — 儲存變更

這個 skill 會引導 AI agent 將目前工作區的所有變更（包含新增或修改的檔案）記錄並提交（commit）到 Git 儲存庫中，並自動產生符合 Conventional Commits 規範的提交訊息。

## When to use this skill

- 當一個階段的任務（例如完成 PRD、實作完特定功能、修復 Bug）結束時
- 需要儲存目前的進度，以便後續回溯或切換任務
- 收到使用者要求「儲存變更」或「commit」時

## How to use it

請在你的 prompt 裡使用以下指示自動化整個提交流程：

```
請檢查目前的檔案狀態，並將所有變更提交到 Git 中。

流程如下：
1. 檢視工作區變更
   使用 `git status` 與 `git diff` 了解有哪些檔案被修改、新增或刪除。
2. 決定 Commit 類型
   根據變更的內容，選擇適合的 Conventional Commits 類型，例如：
   - `feat`: 新增功能或文件（例如新增 PRD、路由設計或新功能原始碼）
   - `fix`: 修復錯誤
   - `docs`: 專純修改或新增說明文件（例如 README）
   - `style`: 程式碼格式調整（不影響邏輯）
   - `refactor`: 重構（既不是新增功能也不是修復 bug 的程式碼更改）
   - `chore`: 建置過程或輔助工具的變動、儲存進度
3. 撰寫 Commit Message
   - 標題要簡潔有力，格式為 `<type>: <subject>`
   - 若變更較多可以補充 description 說明主要的影響。
4. 執行命令
   - 設定身份（如果是首次提交可能需要配置 `git config`）
   - 使用 `git add .` 或者選擇性加入檔案
   - 使用 `git commit -m "<你的訊息>"` 完成提交
```

## 注意事項
- 若使用者尚未配置任何 git 使用者資訊，可先主動設定本機環境變數或設定 local config 以完成操作。
- 務必確保提交訊息明確地反映了剛才完成的變更內容。
