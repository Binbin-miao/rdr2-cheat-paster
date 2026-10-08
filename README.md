# 荒野大镖客 2 · 作弊码速贴器

> RDR2 Cheat Paster — 把《荒野大镖客 2》全部 37 条官方作弊码一键输入游戏。

[English](README.en.md) | **简体中文**

还在一条条手打 `Abundance is the dullest desire` 这种英文短语？这个小工具把 37 条作弊码全内置好了，
按一个 `Ctrl + ,` 就自动帮你输进游戏的密码框，`Ctrl + ↑` / `Ctrl + ↓` 上下翻条。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Cheats](https://img.shields.io/badge/Cheats-37-orange)

---

## 功能特性

- **37 条官方作弊码全内置** — 标点与原版一致，不用再担心打错标点导致失效
- **全局热键** — 全屏游戏里照样能用，不用切窗口
- **逐条切换** — `Ctrl + ↑` / `Ctrl + ↓` 上下翻，`Home` / `End` 跳首尾
- **自动输入** — 模拟逐字打字 + 自动回车，直接进游戏密码框（游戏不吃 Ctrl+V 粘贴）
- **搜索 + 分类过滤** — 支持中英文搜索，按金钱/武器/马匹/荣誉等 6 类筛选
- **前置条件标注** — 哪 8 条需要先买报纸、在第几章，列表里直接写清楚
- **记住上次位置** — 下次打开自动回到你上次选的那条
- **免安装 exe** — 打包好的单文件程序，double-click 即用，不需要装 Python

---

## 快速开始

### 方式一：直接跑 exe（推荐）

1. 下载 [Releases](https://github.com/Binbin-miao/rdr2-cheat-paster/releases/latest) 里的 `RDR2_Cheat_Paster_v1.0.0.exe`
   （重命名为 `RDR2作弊码速贴器.exe` 不影响使用）
2. 双击运行
3. 进游戏 → `ESC` → **设置** → 底部 **密码**，光标停在输入框
4. 用 `Ctrl + ↑` / `Ctrl + ↓` 选好作弊码，按 `Ctrl + ,` 输入

> 首次运行如果杀软报毒，是 PyInstaller 打包程序的常见误报，添加信任即可。
> 有顾虑可以直接用源码跑（见方式二）。

### 方式二：从源码运行

```bash
git clone https://github.com/Binbin-miao/rdr2-cheat-paster.git
cd rdr2-cheat-paster
pip install pynput
python rdr2_cheat_paster.py
```

---

## 快捷键

| 快捷键 | 作用 |
|---|---|
| `Ctrl + ,` | **把当前选中的作弊码输入游戏**（主热键） |
| `Ctrl + ↑` | 上一条 |
| `Ctrl + ↓` | 下一条 |
| `Ctrl + Home` | 跳回第一条 |
| `Ctrl + End` | 跳到最后一条 |
| `Ctrl + Shift + ,` | 只复制到剪贴板，不模拟输入 |
| `Ctrl + Shift + C` | 显示 / 隐藏主窗口 |
| `Ctrl + Shift + Q` | 退出程序 |
| `ESC`（窗口内） | 最小化到后台 |

全部为**全局热键**，游戏全屏时同样有效。

---

## 内置作弊码一览

共 **37 条**，分为 6 类：

| 分类 | 条数 | 示例 |
|---|---|---|
| 金钱与属性 | 7 | `Greed is now a virtue` 获得 $500 |
| 死眼等级 | 5 | `Guide me better` 死眼等级 1 |
| 武器 | 4 | `A simple life, a beautiful death` 基础武器 |
| 马匹与载具 | 10 | `Run! Run! Run!` 生成赛马 |
| 荣誉与通缉 | 6 | `Virtue unearned is not virtue` 荣誉拉满 |
| 地图与外观 | 5 | `Vanity. All is vanity` 解锁全部服装 |

完整数据见 [`cheats.py`](cheats.py)。

---

## 重要提醒

- 作弊码**严格区分标点**，大小写不敏感。本工具已内置正确原文，不会输错。
- **8 条作弊码需要先拥有对应报纸**才能解锁，否则游戏会提示
  *"You do not meet the prerequisites to unlock this cheat"*：

  | 作弊码 | 前置条件 |
  |---|---|
  | `Abundance is the dullest desire` | 第 1 章起购买报纸 |
  | `Greed is American virtue` | 第 3 章「广告，崭新的美国艺术」后买报纸 |
  | `You long for sight and see nothing` | 第 3 章「血脉深仇，源远流长」后买报纸 |
  | `Virtue unearned is not virtue` | 第 4 章「都市乐趣」后买报纸 |
  | `The lucky be strong evermore` | 第 5 章通关后买报纸 |
  | `You seek more than the world offers` | 第 6 章「国王之子」后买报纸 |
  | `You are a beast built for war` | 终章通关后买报纸 |
  | `Would you be happier as a clown?` | 终章通关后买报纸 |

- **开启任意作弊后，本局无法存档、也无法解锁成就/奖杯**。
  想正常通关请先关闭作弊，或读一个没有用过作弊的存档。

---

## 配置

配置文件位于 `~/.rdr2_cheat_paster.json`（首次运行自动生成）：

```json
{
  "type_mode": "type",
  "key_interval": 0.012,
  "last_index": 0
}
```

| 字段 | 说明 |
|---|---|
| `type_mode` | `type` = 模拟逐字打字（默认，兼容性最好）；`paste` = 仅复制到剪贴板 |
| `key_interval` | 模拟打字时每个字符间隔（秒）。游戏掉帧漏字时可调到 `0.03` |
| `last_index` | 上次选中的作弊码下标（自动维护） |

---

## 打包 exe

双击 `build.bat`，或手动执行：

```bash
pip install pynput pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --noconsole \
  --name "RDR2作弊码速贴器" \
  --hidden-import pynput.keyboard._win32 \
  --hidden-import pynput.mouse._win32 \
  rdr2_cheat_paster.py
```

> 两个 `--hidden-import` 是必须的，否则打包后的 exe 运行时会报 pynput 后端导入失败。

---

## 项目结构

```
rdr2-cheat-paster/
├── rdr2_cheat_paster.py    # 主程序：Tkinter GUI + pynput 全局热键
├── cheats.py               # 37 条作弊码数据
├── build.bat               # 一键打包脚本
├── 使用说明.md              # 详细中文说明
├── README.md               # 中文 README（本文件）
├── README.en.md            # English README
├── requirements.txt
└── LICENSE
```

---

## 技术说明

- **GUI**：标准库 `tkinter`，无额外 UI 依赖
- **热键与按键模拟**：`pynput` —— 热键回调运行在监听线程，通过 `root.after(0, fn)` 切回 Tk 主线程更新界面
- **为什么用模拟打字而不是剪贴板粘贴**：RDR2 的密码输入框不接收 `Ctrl+V`，只能逐字模拟按键
- **输入延迟**：按下热键后会等 0.45 秒再开始输入，留出时间让你把焦点切回游戏

---

## 添加 / 修改作弊码

编辑 `cheats.py`，按格式追加即可，程序会自动加载：

```python
{"cat": "分类名", "name": "中文效果说明", "code": "Cheat Phrase Here",
 "req": "前置条件（无则填 无）", "type": "paste"},
```

---

## License

[MIT](LICENSE)

---

## 免责声明

本项目仅用于**单机游戏娱乐**，不涉及任何在线游戏作弊、存档修改或外挂功能。
使用游戏内作弊码会使当前存档无法继续保存、并禁用成就，这是游戏本身的机制，与本工具无关。
