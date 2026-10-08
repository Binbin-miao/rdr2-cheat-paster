# -*- coding: utf-8 -*-
"""
RDR2 作弊码速贴器 (Red Dead Redemption 2 Cheat Paster)
--------------------------------------------------------
一个常驻托盘的小工具，帮你把《荒野大镖客 2》的作弊码短语
一键"粘贴"进游戏内的「设置 - 密码」输入框。

全局热键（在游戏里也能用）：
    Ctrl + ,            把【当前选中】的作弊码输入游戏
    Ctrl + ↑            上一条
    Ctrl + ↓            下一条
    Ctrl + Home         跳到第一条
    Ctrl + End          跳到最后一条
    Ctrl + Shift + ,    只复制到剪贴板（不模拟输入）
    Ctrl + Shift + C    显示 / 隐藏主窗口
    Ctrl + Shift + Q    退出程序

依赖：pynput（全局热键与按键模拟）；GUI 用标准库 tkinter。
"""

import os
import sys
import json
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from cheats import CHEATS
except ImportError:
    CHEATS = [{"cat": "默认", "name": "示例", "code": "Greed is now a virtue", "req": "无", "type": "paste"}]

try:
    from pynput import keyboard as pk
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False

APP_TITLE = "荒野大镖客 2 · 作弊码速贴器"
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".rdr2_cheat_paster.json")

# ----------------------------------------------------------------------------
# 配置读写
# ----------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "paste_key": "<ctrl>+,",        # 主粘贴热键
    "prev_key": "<ctrl>+<up>",
    "next_key": "<ctrl>+<down>",
    "first_key": "<ctrl>+<home>",
    "last_key": "<ctrl>+<end>",
    "copy_key": "<ctrl>+<shift>+,",
    "toggle_key": "<ctrl>+<shift>+c",
    "quit_key": "<ctrl>+<shift>+q",
    "type_mode": "type",            # type = 模拟逐字输入；paste = 仅复制到剪贴板
    "key_interval": 0.012,          # 模拟打字时每个字符的间隔(秒)
    "last_index": 0,
}


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception:
            pass
    return cfg


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ----------------------------------------------------------------------------
# 主程序
# ----------------------------------------------------------------------------

class CheatPaster:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg = load_config()
        self.rows = []          # 过滤后的行索引
        self.cur = 0            # 在 rows 中的位置
        self.hotkey_listener = None
        self._flash_after = None

        self._build_ui()
        self._refresh_list()
        self._select_by_global_index(self.cfg.get("last_index", 0), save=False)

        self._start_hotkeys()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<Escape>", lambda e: self.root.withdraw())

    # ---------------- UI ----------------

    def _build_ui(self):
        self.root.title(APP_TITLE)
        self.root.geometry("1080x680")
        self.root.minsize(820, 480)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Treeview", rowheight=26, font=("Microsoft YaHei UI", 10))
        style.configure("Treeview.Heading", font=("Microsoft YaHei UI", 10, "bold"))
        style.configure("Big.TButton", font=("Microsoft YaHei UI", 12, "bold"), padding=(14, 10))
        style.configure("Nav.TButton", font=("Microsoft YaHei UI", 11), padding=(10, 6))

        # ---- 顶部：搜索 + 分类 ----
        top = ttk.Frame(self.root, padding=(12, 10, 12, 4))
        top.pack(fill="x")

        ttk.Label(top, text="搜索：").pack(side="left")
        self.var_search = tk.StringVar()
        self.var_search.trace_add("write", lambda *_: self._refresh_list())
        ent = ttk.Entry(top, textvariable=self.var_search, width=28)
        ent.pack(side="left", padx=(0, 14))

        ttk.Label(top, text="分类：").pack(side="left")
        self.var_cat = tk.StringVar(value="全部")
        self.var_cat.trace_add("write", lambda *_: self._refresh_list())
        cats = ["全部"] + sorted({c["cat"] for c in CHEATS})
        combo = ttk.Combobox(top, textvariable=self.var_cat, values=cats, width=16, state="readonly")
        combo.pack(side="left")

        ttk.Label(top, text=f"共 {len(CHEATS)} 条", foreground="#888").pack(side="right")

        # ---- 中部：列表 ----
        mid = ttk.Frame(self.root, padding=(12, 4))
        mid.pack(fill="both", expand=True)

        cols = ("idx", "name", "code", "req")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("idx", text="#")
        self.tree.heading("name", text="效果")
        self.tree.heading("code", text="作弊码短语（输入游戏）")
        self.tree.heading("req", text="前置条件")
        self.tree.column("idx", width=46, anchor="center", stretch=False)
        self.tree.column("name", width=280, anchor="w", stretch=False)
        self.tree.column("code", width=430, anchor="w", stretch=True)
        self.tree.column("req", width=240, anchor="w", stretch=False)

        self.tree.tag_configure("odd", background="#f7f7f9")
        self.tree.tag_configure("even", background="#ffffff")

        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.do_paste())

        # ---- 下部：大预览 + 按钮 ----
        bottom = ttk.Frame(self.root, padding=(12, 6, 12, 12))
        bottom.pack(fill="x")

        prev_box = ttk.LabelFrame(bottom, text="当前选中的作弊码（将输入游戏）", padding=(10, 6))
        prev_box.pack(fill="x")

        self.lbl_code = tk.Label(prev_box, text="", font=("Consolas", 18, "bold"),
                                 fg="#1a3d7c", anchor="w", justify="left", wraplength=980)
        self.lbl_code.pack(fill="x", pady=(2, 2))
        self.lbl_meta = tk.Label(prev_box, text="", font=("Microsoft YaHei UI", 9),
                                 fg="#666", anchor="w", justify="left", wraplength=980)
        self.lbl_meta.pack(fill="x")

        btns = ttk.Frame(bottom)
        btns.pack(fill="x", pady=(10, 0))

        ttk.Button(btns, text="▲ 上一条", style="Nav.TButton",
                   command=self.prev_item).pack(side="left", padx=(0, 6))
        ttk.Button(btns, text="▼ 下一条", style="Nav.TButton",
                   command=self.next_item).pack(side="left", padx=(0, 6))
        ttk.Button(btns, text="只复制", style="Nav.TButton",
                   command=self.do_copy).pack(side="left", padx=(0, 14))
        ttk.Button(btns, text="▶ 输入到游戏  (Ctrl + ,)", style="Big.TButton",
                   command=self.do_paste).pack(side="left")

        self.lbl_status = tk.Label(btns, text="", font=("Microsoft YaHei UI", 10),
                                   fg="#1a7f37", anchor="w")
        self.lbl_status.pack(side="left", padx=18)

        # ---- 底部：热键说明 ----
        hk = self._hotkey_text()
        foot = tk.Label(self.root, text=hk, font=("Microsoft YaHei UI", 9),
                        fg="#777", anchor="w", justify="left", bg="#f0f0f3",
                        padx=12, pady=6)
        foot.pack(fill="x", side="bottom")

        if not HAS_PYNPUT:
            self.root.after(600, lambda: messagebox.showwarning(
                "缺少依赖",
                "未检测到 pynput 模块，全局热键与自动输入将不可用。\n\n"
                "请在命令行执行：\n    pip install pynput\n然后重新启动本程序。"
            ))

    def _hotkey_text(self):
        def pretty(k):
            return (k.replace("<ctrl>", "Ctrl").replace("<shift>", "Shift")
                     .replace("<up>", "↑").replace("<down>", "↓")
                     .replace("<home>", "Home").replace("<end>", "End").replace("+", " + "))
        c = self.cfg
        return ("   ".join([
            f"【{pretty(c['paste_key'])}】输入到游戏",
            f"【{pretty(c['prev_key'])}】上一条",
            f"【{pretty(c['next_key'])}】下一条",
            f"【{pretty(c['first_key'])}】第一条",
            f"【{pretty(c['last_key'])}】最后一条",
            f"【{pretty(c['copy_key'])}】只复制",
            f"【{pretty(c['toggle_key'])}】显示/隐藏窗口",
            f"【{pretty(c['quit_key'])}】退出",
        ]))

    # ---------------- 列表逻辑 ----------------

    def _filtered(self):
        kw = self.var_search.get().strip().lower()
        cat = self.var_cat.get()
        out = []
        for i, c in enumerate(CHEATS):
            if cat != "全部" and c["cat"] != cat:
                continue
            if kw and kw not in (c["name"] + " " + c["code"] + " " + c["req"] + " " + c["cat"]).lower():
                continue
            out.append(i)
        return out

    def _refresh_list(self):
        self.rows = self._filtered()
        self.tree.delete(*self.tree.get_children())
        for n, gi in enumerate(self.rows):
            c = CHEATS[gi]
            tag = "odd" if n % 2 else "even"
            self.tree.insert("", "end", iid=str(n),
                             values=(gi + 1, c["name"], c["code"], c["req"]), tags=(tag,))
        if self.rows:
            self.cur = min(self.cur, len(self.rows) - 1)
            self._highlight()
        else:
            self.cur = 0
            self.lbl_code.config(text="（没有匹配的作弊码）")
            self.lbl_meta.config(text="")

    def _highlight(self):
        if not self.rows:
            return
        iid = str(self.cur)
        if self.tree.exists(iid):
            self.tree.selection_set(iid)
            self.tree.focus(iid)
            self.tree.see(iid)
        gi = self.rows[self.cur]
        c = CHEATS[gi]
        self.lbl_code.config(text=c["code"])
        self.lbl_meta.config(text=f"[{c['cat']}] {c['name']}    ·    前置条件：{c['req']}    ·    第 {gi + 1} / {len(CHEATS)} 条")

    def _on_tree_select(self, _evt=None):
        sel = self.tree.selection()
        if not sel:
            return
        n = int(sel[0])
        if n != self.cur:
            self.cur = n
            self._highlight()

    def _select_by_global_index(self, gi, save=True):
        """按 CHEATS 里的全局下标选中（用于恢复上次位置）。"""
        for n, g in enumerate(self.rows):
            if g == gi:
                self.cur = n
                self._highlight()
                return
        self.cur = 0
        self._highlight()

    def _remember(self):
        if self.rows:
            self.cfg["last_index"] = self.rows[self.cur]
            save_config(self.cfg)

    # ---------------- 动作 ----------------

    def prev_item(self):
        if not self.rows:
            return
        self.cur = (self.cur - 1) % len(self.rows)
        self._highlight()
        self._remember()

    def next_item(self):
        if not self.rows:
            return
        self.cur = (self.cur + 1) % len(self.rows)
        self._highlight()
        self._remember()

    def first_item(self):
        if not self.rows:
            return
        self.cur = 0
        self._highlight()
        self._remember()

    def last_item(self):
        if not self.rows:
            return
        self.cur = len(self.rows) - 1
        self._highlight()
        self._remember()

    def current_code(self):
        if not self.rows:
            return None
        return CHEATS[self.rows[self.cur]]["code"]

    def _set_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update_idletasks()

    def do_copy(self):
        code = self.current_code()
        if not code:
            return
        self._set_clipboard(code)
        self._flash(f"已复制到剪贴板：{code}")

    def do_paste(self):
        """把当前选中的作弊码输入游戏。"""
        code = self.current_code()
        if not code:
            return
        self._set_clipboard(code)
        self._remember()

        if self.cfg.get("type_mode", "type") == "paste" or not HAS_PYNPUT:
            self._flash(f"已复制（手动 Ctrl+V 粘贴）：{code}")
            return

        self._flash(f"正在输入：{code}")
        delay = float(self.cfg.get("key_interval", 0.012))

        def worker():
            time.sleep(0.45)                    # 给玩家一点时间，让游戏密码框获得焦点
            try:
                ctrl = pk.Controller()
                for ch in code:
                    ctrl.press(ch)
                    ctrl.release(ch)
                    time.sleep(delay)
                ctrl.press(pk.Key.enter)
                ctrl.release(pk.Key.enter)
            except Exception as e:
                print("输入失败:", e)

        threading.Thread(target=worker, daemon=True).start()

    def _flash(self, msg, ms=2200):
        self.lbl_status.config(text=msg)
        if self._flash_after:
            try:
                self.root.after_cancel(self._flash_after)
            except Exception:
                pass
        self._flash_after = self.root.after(ms, lambda: self.lbl_status.config(text=""))

    # ---------------- 全局热键 ----------------

    def _start_hotkeys(self):
        if not HAS_PYNPUT:
            return
        c = self.cfg
        hotkeys = {
            c["paste_key"]: self._hk_paste,
            c["prev_key"]: self._hk_prev,
            c["next_key"]: self._hk_next,
            c["first_key"]: self._hk_first,
            c["last_key"]: self._hk_last,
            c["copy_key"]: self._hk_copy,
            c["toggle_key"]: self._hk_toggle,
            c["quit_key"]: self._hk_quit,
        }
        # 热键回调在 pynput 的监听线程里触发，统一切回 Tk 主线程
        def wrap(fn):
            return lambda: self.root.after(0, fn)

        hotkeys = {k: wrap(v) for k, v in hotkeys.items()}
        try:
            self.hotkey_listener = pk.GlobalHotKeys(hotkeys)
            self.hotkey_listener.daemon = True
            self.hotkey_listener.start()
        except Exception as e:
            print("热键注册失败:", e)

    def _hk_paste(self):
        self.do_paste()

    def _hk_prev(self):
        self.prev_item()

    def _hk_next(self):
        self.next_item()

    def _hk_first(self):
        self.first_item()

    def _hk_last(self):
        self.last_item()

    def _hk_copy(self):
        self.do_copy()

    def _hk_toggle(self):
        if self.root.state() == "withdrawn" or not self.root.winfo_viewable():
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
        else:
            self.root.withdraw()

    def _hk_quit(self):
        self._on_close()

    def _on_close(self):
        self._remember()
        try:
            if self.hotkey_listener:
                self.hotkey_listener.stop()
        except Exception:
            pass
        self.root.quit()
        self.root.destroy()


def main():
    # 若未装 pynput，仍然让 GUI 能够启动（只是没有全局热键）
    root = tk.Tk()
    try:
        app = CheatPaster(root)
    except Exception as e:
        messagebox.showerror("启动失败", str(e))
        raise
    root.mainloop()


if __name__ == "__main__":
    main()
