# Scout Chat 聊天室

一个基于 FastAPI + WebSocket 的实时聊天室，支持多人同时在线聊天，消息持久化存储。

## 功能

- 多人实时聊天
- 消息存储到 SQLite，刷新页面不丢
- 自动记住用户名，刷新不用重新输入
- 前后端分离，结构清晰

## 技术栈

| 部分 | 技术 |
|------|------|
| 后端 | Python + FastAPI + WebSocket |
| 存储 | SQLite |
| 前端 | HTML + CSS + JavaScript |

## 项目结构

```text
scout-projects/
├── .gitignore
├── README.md
└── chatroom/
    ├── backend/
    │   ├── main.py        # 后端主程序
    │   └── chat.db        # SQLite 数据库（运行时生成）
    └── frontend/
        ├── index.html     # 页面结构
        ├── style.css      # 页面样式
        └── app.js         # 前端逻辑
   如何运行
1. 安装依赖
```bash
pip install fastapi uvicorn websockets
2. 启动后端
```bash
cd chatroom/backend
uvicorn main:app --reload
后端会运行在 http://127.0.0.1:8000。

3. 启动前端
新开一个终端：

```bash
cd chatroom/frontend
python -m http.server 5500
4. 打开浏览器
访问 http://127.0.0.1:5500，输入名字即可进入聊天室。

想测试多人聊天，可以再开一个浏览器标签页，输入不同名字。

已实现功能
☑ 多人实时收发消息
☑ 消息存入 SQLite
☑ 刷新页面后消息还在
☑ 刷新后自动登录
未完成 / 已知问题
暂无用户密码验证

暂无消息撤回功能

断线重连需要手动刷新页面

AI 使用说明
本项目在开发过程中使用了 AI 辅助，具体如下：

后端 FastAPI + WebSocket 代码框架由 AI 生成，本人理解并调试验证。

前端 HTML/CSS/JS 代码由 AI 生成，本人修改并测试。

README、设计说明文档由本人编写。     