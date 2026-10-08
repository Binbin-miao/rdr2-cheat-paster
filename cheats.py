# -*- coding: utf-8 -*-
"""
荒野大镖客 2 (Red Dead Redemption 2) 全部官方作弊码数据。

字段说明：
    cat   : 分类名称
    name  : 中文名称（效果说明）
    code  : 英文作弊短语（游戏内"设置 - 密码"里输入的原文，标点必须一致）
    req   : 前置条件（需要先拥有对应报纸 / 无）
    type  : paste=需要输入到密码框；action=仅需在密码列表里勾选启用
"""

CHEATS = [
    # ---------------- 金钱 / 属性 ----------------
    {"cat": "金钱与属性", "name": "获得 500 美元", "code": "Greed is now a virtue", "req": "无", "type": "paste"},
    {"cat": "金钱与属性", "name": "生命/体力/死眼 全满", "code": "You flourish before you die", "req": "无", "type": "paste"},
    {"cat": "金钱与属性", "name": "永久提升生命/体力/死眼上限", "code": "Seek all the bounty of this place", "req": "无", "type": "paste"},
    {"cat": "金钱与属性", "name": "补满并强化三条核心(黄圈)", "code": "You seek more than the world offers", "req": "第6章「国王之子」后买报纸", "type": "paste"},
    {"cat": "金钱与属性", "name": "无限体力（人和马）", "code": "The lucky be strong evermore", "req": "第5章通关后买报纸", "type": "paste"},
    {"cat": "金钱与属性", "name": "无限死眼 (Dead Eye)", "code": "Be greedy only for foresight", "req": "无", "type": "paste"},
    {"cat": "金钱与属性", "name": "无限弹药", "code": "Abundance is the dullest desire", "req": "第1章起购买报纸", "type": "paste"},

    # ---------------- 死眼等级 ----------------
    {"cat": "死眼等级", "name": "死眼等级 1", "code": "Guide me better", "req": "无", "type": "paste"},
    {"cat": "死眼等级", "name": "死眼等级 2", "code": "Make me better", "req": "无", "type": "paste"},
    {"cat": "死眼等级", "name": "死眼等级 3", "code": "I shall be better", "req": "无", "type": "paste"},
    {"cat": "死眼等级", "name": "死眼等级 4", "code": "I still seek more", "req": "无", "type": "paste"},
    {"cat": "死眼等级", "name": "死眼等级 5", "code": "I seek and I find", "req": "无", "type": "paste"},

    # ---------------- 武器 ----------------
    {"cat": "武器", "name": "基础武器一套", "code": "A simple life, a beautiful death", "req": "无", "type": "paste"},
    {"cat": "武器", "name": "重型武器一套", "code": "Greed is American virtue", "req": "第3章「广告，崭新的美国艺术」后买报纸", "type": "paste"},
    {"cat": "武器", "name": "潜行武器一套", "code": "Death is silence", "req": "无", "type": "paste"},
    {"cat": "武器", "name": "神枪手武器一套", "code": "History is written by fools", "req": "无", "type": "paste"},

    # ---------------- 马匹与载具 ----------------
    {"cat": "马匹与载具", "name": "提升所有马的默契度", "code": "My kingdom is a horse", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "口哨召唤马匹无距离限制", "code": "Better than my dog", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成赛马", "code": "Run! Run! Run!", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成战马", "code": "You are a beast built for war", "req": "终章通关后买报纸", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成上等马（阿拉伯马）", "code": "You want more than you have", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成一匹随机马", "code": "You want something new", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成驿站马车", "code": "The best of the old ways", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成货运马车", "code": "Keep your dreams simple", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成轻便马车", "code": "Keep your dreams light", "req": "无", "type": "paste"},
    {"cat": "马匹与载具", "name": "生成马戏团马车", "code": "Would you be happier as a clown?", "req": "终章通关后买报纸", "type": "paste"},

    # ---------------- 荣誉与通缉 ----------------
    {"cat": "荣誉与通缉", "name": "荣誉值拉满", "code": "Virtue unearned is not virtue", "req": "第4章「都市乐趣」后买报纸", "type": "paste"},
    {"cat": "荣誉与通缉", "name": "荣誉值降到最低", "code": "You revel in your disgrace, I see", "req": "无", "type": "paste"},
    {"cat": "荣誉与通缉", "name": "荣誉值重置为中立", "code": "Balance. All is balance", "req": "无", "type": "paste"},
    {"cat": "荣誉与通缉", "name": "提升通缉等级", "code": "You want punishment", "req": "无", "type": "paste"},
    {"cat": "荣誉与通缉", "name": "降低通缉等级", "code": "You want freedom", "req": "无", "type": "paste"},
    {"cat": "荣誉与通缉", "name": "清除所有悬赏与封锁区", "code": "You want everyone to go away", "req": "无", "type": "paste"},

    # ---------------- 地图 / 外观 / 制作 ----------------
    {"cat": "地图与外观", "name": "去除地图迷雾（全图可见）", "code": "You long for sight and see nothing", "req": "第3章「血脉深仇，源远流长」后买报纸", "type": "paste"},
    {"cat": "地图与外观", "name": "解锁全部服装", "code": "Vanity. All is vanity", "req": "无", "type": "paste"},
    {"cat": "地图与外观", "name": "学会全部制作配方", "code": "Eat of knowledge", "req": "无", "type": "paste"},
    {"cat": "地图与外观", "name": "解锁全部营地升级", "code": "Share", "req": "无", "type": "paste"},
    {"cat": "地图与外观", "name": "让自己喝醉", "code": "A fool on command", "req": "无", "type": "paste"},
]
