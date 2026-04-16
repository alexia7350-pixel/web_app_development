# 使用者流程與系統流程圖

這份文件根據 PRD 與系統架構文件所規劃，視覺化展示本食譜收藏夾系統的「使用者操作路徑」及「新增食譜的資料流序列」，幫助開發時對齊功能與資料處理流程。

## 1. 使用者流程圖 (User Flow)

這張圖呈現了使用者從抵達網站開始，如何登入、瀏覽、搜尋食譜，並延伸出「收藏」、「評價」以及「從食材找靈感」的操作路徑。也包含了管理員特有的後台路徑。

```mermaid
flowchart LR
    Start([進入網站首頁]) --> Auth{已登入?}
    
    Auth -->|否| Guest[瀏覽公開食譜 / 食譜牆]
    Guest --> LoginBtn[點擊登入/註冊]
    LoginBtn --> LoginPage[登入與註冊頁面]
    LoginPage -->|成功| Main
    
    Auth -->|是| Main[會員首頁 - 最新推薦與動態]
    
    Main --> Search[一般關鍵字與分類搜尋]
    Main --> IngredientSearch[輸入現有食材組合快搜]
    Main --> Collection[我的個人收藏夾]
    Main --> Create[新增/創作食譜]
    
    Search --> RecipeDetail[食譜詳細頁面]
    IngredientSearch --> RecipeDetail
    Collection --> RecipeDetail
    Create --> RecipeDetail
    Guest --> RecipeDetail
    
    RecipeDetail --> Action1[加入 / 移除自己的收藏]
    RecipeDetail --> Action2[提交評分與實作留言]
    
    Admin([管理員登入]) --> AdminPanel[後台管理介面]
    AdminPanel --> ManageRecipe[編輯或強制刪除違規食譜]
    AdminPanel --> ManageUser[管理或停權使用者帳號]
```

## 2. 系統序列圖 (Sequence Diagram)

這張圖描述了使用者在網站上「建立並提交一份新食譜」直到「成功寫入資料庫並回到頁面」的端到端過程。採用 Flask 的 Model-View-Controller 邏輯作為拆解基準。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (Frontend)
    participant Route as Flask Route (Controller)
    participant Model as SQLAlchemy (Model)
    participant DB as SQLite Database
    
    User->>Browser: 在新增食譜頁面填寫標題、食材與步驟並送出
    Browser->>Route: POST /recipe/new (HTTP Form Data)
    
    Route->>Route: 1. 驗證使用者是否已登入
    Route->>Route: 2. 驗證表單資料 (防呆與防止 XSS)
    
    Route->>Model: 3. 呼叫 Recipe(title=..., ingredients=...) 建立實體
    Model->>DB: 4. 轉譯為 INSERT INTO recipes ... 執行寫入
    DB-->>Model: 5. 寫入成功，產生新食譜 ID
    
    Model-->>Route: 6. 回傳資料庫儲存完畢狀態
    Route-->>Browser: 7. 回傳 HTTP 302 重導向到 /recipe/<id>
    
    Browser->>Route: 8. GET /recipe/<id> 獲取新頁面
    Route-->>Browser: 9. 渲染完成的 Jinja2 HTML 樣板
    Browser-->>User: 畫面顯示新增成功，呈現該篇食譜
```

## 3. 功能清單對照表

根據上述流程，這裡列出專案預計實作的主要功能、涵蓋的 HTTP 方法與預估規劃的 URL 路徑（依 Request 動作劃分）：

| 功能 | HTTP 方法 | URL 路徑 (預估) | 對應藍圖模組 (Blueprint) |
| --- | --- | --- | --- |
| 註冊帳號頁面與處理 | GET / POST | `/auth/register` | `auth.py` |
| 登入帳號頁面與處理 | GET / POST | `/auth/login` | `auth.py` |
| 登出帳號 | GET | `/auth/logout` | `auth.py` |
| **瀏覽首頁 (食譜牆)** | GET | `/` | `main.py` |
| 一般瀏覽與分類關鍵字搜尋 | GET | `/recipes` 或 `/search` | `main.py` |
| **食材組合搜尋專區** | GET / POST | `/search/ingredients` | `search.py` |
| **檢視單一食譜詳細內容** | GET | `/recipe/<id>` | `main.py` / `recipe.py` |
| 新增食譜頁面與處理 | GET / POST | `/recipe/new` | `recipe.py` |
| 編輯自己的食譜 | GET / POST | `/recipe/<id>/edit` | `recipe.py` |
| 刪除自己的食譜 | POST | `/recipe/<id>/delete` | `recipe.py` |
| **加入或移除我的收藏** | POST | `/recipe/<id>/collect` | `recipe.py` |
| 檢視個人收藏夾列表 | GET | `/collections` | `main.py` |
| **提交對食譜的評分與留言** | POST | `/recipe/<id>/comment` | `recipe.py` |
| (管理員) 進入後台首頁 | GET | `/admin` | `admin.py` |
| (管理員) 強制編輯/刪除食譜 | GET / POST | `/admin/recipe/<id>/...` | `admin.py` |
| (管理員) 管理使用者權限狀態 | GET / POST | `/admin/users` | `admin.py` |
