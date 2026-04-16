# 路由與頁面設計文件 (ROUTES)

本文件描述整個食譜收藏夾系統的 URL 路由規劃與 Blueprint 模組切分。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | Blueprint 模組 | 對應模板 (Jinja2) | 說明 |
| --- | --- | --- | --- | --- | --- |
| 首頁 / 最新食譜牆 | GET | `/` | `main` | `templates/index.html` | 顯示最新與推薦食譜 |
| 一般瀏覽與分類搜尋 | GET | `/recipes` | `main` | `templates/recipe/list.html` | 依條件瀏覽公開食譜 |
| 我的收藏夾 | GET | `/collections` | `main` | `templates/recipe/collections.html` | 顯示登入者的收藏 |
| 註冊帳號 | GET, POST | `/auth/register` | `auth` | `templates/auth/register.html` | 處理註冊邏輯 |
| 登入帳號 | GET, POST | `/auth/login` | `auth` | `templates/auth/login.html` | 處理登入邏輯 |
| 登出 | GET | `/auth/logout` | `auth` | — | 登出並重導向至首頁 |
| 單一食譜詳細頁 | GET | `/recipe/<int:id>` | `recipe` | `templates/recipe/detail.html` | 檢視食譜完整資訊 |
| 新增食譜 | GET, POST | `/recipe/new` | `recipe` | `templates/recipe/new.html` | 填寫與建立自創食譜 |
| 編輯食譜 | GET, POST | `/recipe/<int:id>/edit` | `recipe` | `templates/recipe/edit.html` | 修改自己的食譜內容 |
| 刪除食譜 | POST | `/recipe/<int:id>/delete` | `recipe` | — | 刪除並重導向回我的頁面 |
| 加入/移除收藏 | POST | `/recipe/<int:id>/collect` | `recipe` | — | 在收藏與取消間切換，重導回原頁 |
| 提交留言與評分 | POST | `/recipe/<int:id>/comment` | `recipe` | — | 送出留言後重導回詳細頁 |
| 食材快搜區 | GET, POST | `/search/ingredients` | `search` | `templates/search/ingredients.html`| 輸入現有食材找食譜 |
| 後台首頁 | GET | `/admin` | `admin` | `templates/admin/index.html` | 管理員 Dashboard |
| 管理員強制編輯食譜 | GET, POST | `/admin/recipe/<int:id>/edit` | `admin` | `templates/admin/edit_recipe.html`| 管理員修改違規內容 |
| 管理員強制刪除食譜 | POST | `/admin/recipe/<int:id>/delete` | `admin` | — | 強制刪除違規內容 |
| 使用者帳號管理 | GET, POST | `/admin/users` | `admin` | `templates/admin/users.html` | 停權或變更權限狀態 |

## 2. Jinja2 模板清單

- 共用版型：
  - `templates/layout.html`: 所有網頁都會繼承的 Base template（包含 Navigation Bar、Footer、Flash Messages 顯示區塊）。
- 首頁與一般呈現：
  - `templates/index.html`: 首頁主視覺與推薦清單。
- 登入註冊區 (`auth/`)：
  - `templates/auth/login.html`
  - `templates/auth/register.html`
- 食譜與互動展演區 (`recipe/`)：
  - `templates/recipe/list.html`: 列表式瀏覽區。
  - `templates/recipe/collections.html`: 收藏夾頁面。
  - `templates/recipe/detail.html`: 單一食譜瀏覽、留言與評分表單呈現處。
  - `templates/recipe/new.html`: 新增表單。
  - `templates/recipe/edit.html`: 編輯表單。
- 搜尋區 (`search/`)：
  - `templates/search/ingredients.html`: 大區塊的食材輸入 UI 介面與搜尋結果面板。
- 後台管理 (`admin/`)：
  - `templates/admin/index.html`
  - `templates/admin/edit_recipe.html`
  - `templates/admin/users.html`

## 3. 路由詳細說明 (Data Flow)

1. **認證相關 (/auth)**
   - 預期輸入：`username`, `email` (Register 專用), `password`。
   - 處理：利用 Flask-Login 或 session 實作 Auth state，並用 `werkzeug.security` 進行密碼比對。如果錯誤，在頁首渲染 flash message。

2. **建立與編輯食譜 (/recipe/new, /recipe/.../edit)**
   - 預期輸入：表單傳遞 `title`, `description`, `instructions`, 動態陣列的 `ingredients` 列表, 還有 `image` 檔案上傳。
   - 處理：
     - 若為新增：將食譜存入 `Recipe`，若有未見過的食材寫入 `Ingredient` 再關聯到中介表 `RecipeIngredient`。
     - 若為編輯：必須驗證 `current_user.id == recipe.author_id` 或該 user 目視具有 admin 角色，否則拋出 403 Forbidden。

3. **食材快搜區 (/search/ingredients)**
   - 預期輸入：以 POST (或 GET 帶 query params) 接收一批字串 `ingredients=["高麗菜", "雞蛋"]`。
   - 處理：透過 `RecipeIngredient` 聯集或交集找出 `Recipe` ID，渲染 `templates/search/ingredients.html` 內的結果部分。
