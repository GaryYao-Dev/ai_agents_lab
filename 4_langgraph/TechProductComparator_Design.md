# 数码产品对比分析工具 (TechProductComparator) — 完整方案设计

## 1. 项目概述

### 1.1 核心定位

一个 AI 驱动的智能数码产品对比工具，帮助消费者在购买手机、电脑、平板、相机等电子产品时做出更明智的决策。

### 1.2 用户痛点

- **信息碎片化**：同一产品在不同网站的数据不一致（价格、配置、评价）
- **难以对比**：用户需要在多个网站来回跳转，手工对比参数
- **忽视隐性指标**：价格便宜但可能续航差、散热差等
- **缺乏个性化建议**：没有根据个人需求的定制推荐
- **无法追踪价格变化**：不知道是否买在最佳时机

### 1.3 核心优势

- **多源数据聚合**：爬取京东、Amazon、B 站测评、AnandTech 等多个来源
- **智能对比**：不只是参数堆砌，而是基于用户需求的加权对比
- **性能翻译**：将原始参数（如 AntuTu 跑分）转化为实际用户体验
- **价格动态追踪**：历史价格、降价通知、最佳购买时机提示
- **个性化推荐**：根据预算、用途、偏好推荐最适合的产品

---

## 2. 系统架构

### 2.1 数据流

```
用户输入
  ↓
[Query Parser] → 理解用户需求（产品类型、预算、用途、优先级）
  ↓
[Data Collector] → 从多源爬取数据
  ├─ 官网规格
  ├─ 电商平台（价格、库存、评价）
  ├─ 专业评测（AnandTech、Tom's Hardware、GSMA、B站UP主）
  ├─ 社交媒体反馈（Reddit、微博、知乎）
  └─ 价格历史数据库
  ↓
[Data Normalizer] → 统一数据格式
  ├─ 参数标准化（如不同网站的屏幕规格统一单位）
  ├─ 评分归一化（不同评测机构的评分映射到 0-100）
  └─ 缺失数据补全或标记
  ↓
[Analysis Engine] → 多维度分析
  ├─ 性能对比（CPU、GPU、内存、存储、续航等）
  ├─ 价格分析（单位性能成本、价格趋势、最佳性价比）
  ├─ 用户体验评分（综合专业评测和用户评论）
  ├─ 生态适配性（OS 版本、软件支持、更新周期）
  └─ 隐性成本（维修、保修、配件价格）
  ↓
[Recommendation Engine] → 个性化推荐
  ├─ 根据用户预算过滤
  ├─ 根据用途（游戏/工作/日常）权重调整
  ├─ 考虑二手价值
  └─ 给出理由
  ↓
[Report Generator] → 生成对比报告
  ├─ 交互式对比表格
  ├─ 图表化展示（价格vs性能、用户评分分布等）
  ├─ 优缺点分析
  ├─ 购买建议（何时购买、从哪购买、风险提示）
  └─ 导出为 PDF/Excel/JSON
```

### 2.2 LangGraph 工作流

```
START
  ↓
[Query Understanding] (Worker 1)
  ├─ 解析用户输入（产品类型、预算、关键需求）
  ├─ 调用工具：搜索、文件读取（配置库）
  └─ 生成搜索策略
  ↓
[Multi-Source Data Collection] (Worker 2)
  ├─ Playwright 爬取各大电商平台
  ├─ 搜索 API 查询专业评测
  ├─ 数据库查询历史价格
  ├─ Python REPL 解析和清洗数据
  └─ 返回结构化数据集
  ↓
[Data Analysis & Enrichment] (Worker 3)
  ├─ Python REPL 运行统计分析
  ├─ 计算性价比、评分排行
  ├─ 识别性能瓶颈和优势
  ├─ 预测价格趋势（若有历史数据）
  └─ 生成对比矩阵
  ↓
[Evaluator] 检查
  ├─ 数据完整性（是否所有关键参数都被收集）
  ├─ 准确性（价格是否最新、配置是否官方）
  ├─ 对比公平性（是否在同一时间点、同一地区采集）
  ├─ 分析深度（是否超越表面参数）
  ├─ 用户需求满足度（是否回答了用户的核心问题）
  └─ 如果不满足，反馈给 Worker 进行补充或修正
  ↓
[Report & Recommendation Generation] (Worker 4)
  ├─ 生成结论性对比报告
  ├─ 根据不同用户角色给出推荐（游戏玩家/办公工作者/摄影师等）
  ├─ 提出"如果你关心 X，选择产品 Y"的决策树
  ├─ 标注重要的权衡（如便宜但续航短）
  └─ 生成可视化和导出
  ↓
END
```

---

## 3. 核心模块设计

### 3.1 Query Understanding（查询理解）

**输入示例：**

```
"我想买一部 5000 块以下的安卓手机，主要用来打游戏和看视频，需要长续航"
```

**输出应该包含：**

```json
{
  "product_type": "smartphone",
  "os_preference": ["android"],
  "budget": { "min": 0, "max": 5000, "currency": "CNY" },
  "primary_use": ["gaming", "video_watching"],
  "secondary_use": ["photography", "work"],
  "priorities": {
    "performance": 0.8,
    "battery_life": 0.9,
    "screen_quality": 0.7,
    "price": 0.6,
    "camera": 0.5,
    "design": 0.3
  },
  "constraints": ["must_have_5g", "no_curved_screen"],
  "compare_against": null // 如果用户提了具体机型，记录下来
}
```

**实现方式：**

- Worker 使用 LLM 从自然语言提取结构化需求
- 调用文件工具查询"产品类型" taxonomy（支持哪些产品分类）
- 使用 Python REPL 验证参数有效性（预算范围、已知的品牌等）

---

### 3.2 Multi-Source Data Collection（多源数据收集）

#### 3.2.1 电商平台爬取

**目标网站：**

- 京东（JD.com）- 最全中国科技产品
- 苏宁、天猫 - 备选中文电商
- Amazon - 国际定价参考
- Best Buy - 北美定价
- Flipkart/Amazon.in - 印度市场参考

**爬取的数据：**

```json
{
  "product_name": "iPhone 15 Pro Max",
  "sku": "MJQV3CH/A",
  "price": 9999,
  "price_history": [
    { "date": "2024-10-01", "price": 10999 },
    { "date": "2024-10-15", "price": 9999 }
  ],
  "in_stock": true,
  "stock_quantity": 100,
  "specifications": {
    "color": "Black",
    "storage": 256,
    "ram": 8
  },
  "ratings": {
    "average": 4.8,
    "count": 1234,
    "distribution": { "5": 0.7, "4": 0.15, "3": 0.1, "2": 0.03, "1": 0.02 }
  },
  "top_reviews": ["...", "..."],
  "seller_info": "Official Store",
  "shipping": "2-day delivery",
  "warranty": "12 months official"
}
```

**Playwright 工具集：**

- 动态加载页面（处理 JavaScript 渲染）
- 截图产品图片
- 点击"规格"标签页获取完整参数
- 提取评价树状结构

#### 3.2.2 专业评测数据

**目标来源：**

- AnandTech（深度评测、性能跑分）
- Tom's Hardware（电脑硬件权威）
- GSMA Intelligence（手机基准测试）
- 知乎、小红书、微博（用户真实体验）
- YouTube/B 站评测 UP 主（综合评估）
- Reddit（英文社区讨论）

**爬取的数据：**

```json
{
  "review_source": "AnandTech",
  "review_date": "2024-10-01",
  "reviewer": "Andrei Frumusanu",
  "headline": "Detailed Performance Analysis",
  "scores": {
    "cpu_performance": 95,
    "gpu_performance": 92,
    "memory_speed": 88,
    "storage_speed": 85,
    "battery_life": 78,
    "thermals": 82,
    "overall": 88
  },
  "benchmarks": {
    "geekbench_single_core": 2850,
    "geekbench_multi_core": 7200,
    "antutu": 1450000,
    "battery_hours": 14.5,
    "throttling_time": "45 min"
  },
  "key_findings": "Excellent CPU performance, but thermal management shows improvement needed",
  "recommendation": "Best in class for productivity tasks",
  "url": "..."
}
```

**使用 Google Serper API 搜索：**

```
query: "{product_name} review benchmark test"
filters: site:anandtech.com OR site:gsmarena.com OR site:notebookcheck.net
```

#### 3.2.3 价格历史和市场数据

**数据源：**

- 历史价格数据库（可以是开源数据如 PCPartPicker 历史数据）
- 电商平台的价格 API（若提供）
- Web Archive（Wayback Machine）- 抓取历史快照

**存储结构：**

```json
{
  "product_id": "iphone_15_pro_max_256gb",
  "price_history": [
    { "date": "2023-09-22", "price": 12999, "source": "JD" },
    {
      "date": "2024-01-15",
      "price": 10999,
      "source": "JD",
      "discount": "新春特惠"
    },
    {
      "date": "2024-10-15",
      "price": 9999,
      "source": "JD",
      "discount": "双十一预热"
    }
  ],
  "price_trend": "downward",
  "best_price_ever": 9499,
  "best_price_date": "2024-03-15"
}
```

---

### 3.3 Data Normalization（数据标准化）

#### 3.3.1 参数映射表

创建一个 JSON 配置文件，定义每个产品类型的标准参数：

```json
{
  "smartphone": {
    "cpu": {
      "standard_name": "processor",
      "sources": ["官方规格", "AnandTech", "GSMArena"],
      "parse_rules": ["提取品牌和型号", "查询已知 CPU 数据库"],
      "display_priority": 1
    },
    "ram": {
      "standard_name": "memory",
      "unit": "GB",
      "parse_rules": ["提取数字"],
      "display_priority": 2
    },
    "battery": {
      "standard_name": "battery_capacity",
      "unit": "mAh",
      "derived_fields": ["battery_life_hours"],
      "display_priority": 3
    },
    "screen": {
      "standard_name": "display",
      "sub_fields": ["size", "resolution", "refresh_rate", "panel_type"],
      "display_priority": 2
    }
  },
  "laptop": {
    "cpu": {...},
    "gpu": {...},
    "ram": {...},
    "storage": {...},
    "screen": {...},
    "weight": {...},
    "battery_life": {...}
  }
}
```

#### 3.3.2 评分归一化

不同来源的评分标准不一致，需要映射到统一的 0-100 分：

```python
# 映射规则示例
def normalize_score(score, source, max_value):
    """
    将不同来源的评分转换为 0-100 分
    """
    if source == "anandtech":  # 通常 0-100
        return score
    elif source == "gsmarena":  # 0-10 分
        return score * 10
    elif source == "user_rating":  # 五星制
        return score / 5 * 100
    else:
        return (score / max_value) * 100
```

#### 3.3.3 缺失数据处理

```python
strategy = {
    "critical_fields": ["price", "processor", "ram"],  # 缺失则跳过此产品
    "estimated_fields": {
        "battery_life": "从容量和功耗推算",
        "thermal_performance": "从 TDP 和评测报道推算",
        "color_options": "从官网查询"
    },
    "optional_fields": ["design", "warranty_duration"]  # 可以缺失
}
```

---

### 3.4 Analysis Engine（分析引擎）

#### 3.4.1 多维度性能打分

**维度 1：原始性能**

```json
{
  "dimension": "raw_performance",
  "sub_scores": {
    "cpu": 92,
    "gpu": 88,
    "memory_bandwidth": 85,
    "storage_speed": 82
  },
  "weight": 0.25, // 用户可调
  "final_score": 86.75
}
```

**维度 2：体验质量**

```json
{
  "dimension": "user_experience",
  "sub_scores": {
    "screen_quality": 95,
    "audio_quality": 88,
    "interface_smoothness": 90,
    "thermal_management": 78 // 游戏时是否会烫手
  },
  "weight": 0.25,
  "final_score": 87.75
}
```

**维度 3：性价比**

```json
{
  "dimension": "value_for_money",
  "calculation": {
    "performance_score": 86,
    "price_rmb": 5000,
    "value_score": 86 / (5000 / 1000) = 17.2  // 每千元得分
  },
  "weight": 0.25,
  "final_score": 72  // 相对较低说明价格偏高
}
```

**维度 4：长期价值**

```json
{
  "dimension": "long_term_value",
  "sub_scores": {
    "software_support_years": 95, // 更新支持期限长
    "resale_value": 80, // 保值率
    "repairability": 65, // 维修成本
    "ecosystem_lock_in": 75 // 生态粘性
  },
  "weight": 0.25,
  "final_score": 78.75
}
```

**综合评分 = 86.75 × 0.25 + 87.75 × 0.25 + 72 × 0.25 + 78.75 × 0.25 = 81.31**

#### 3.4.2 对比分析

**并排对比：**

```
产品          性能  体验  性价比  长期价值  综合评分  推荐度
iPhone 15P    92    95    72      78.75    81.31   ★★★★☆
小米14 Ultra  90    88    85      82        86.25   ★★★★★
三星 S24      88    92    78      80        84.5    ★★★★☆
```

**雷达图对比：**

```
参数维度上绘制 radar chart，直观展示产品强弱项
```

**权衡分析：**

```
如果选择 iPhone 15 Pro Max：
  + 最好的屏幕质量
  + 最长的软件支持（7年）
  + 最好的游戏体验
  - 最高的价格
  - 续航一般
  - 无法拓展存储

如果选择小米14 Ultra：
  + 最好的性价比
  + 最好的续航
  + 最好的摄像头
  - 系统更新不如 Apple
  - UI 植入广告
```

---

### 3.5 Recommendation Engine（推荐引擎）

#### 3.5.1 用户角色匹配

```json
{
  "user_profiles": [
    {
      "name": "游戏玩家",
      "priorities": {
        "performance": 0.9,
        "screen_quality": 0.8,
        "thermal": 0.8,
        "battery": 0.5,
        "price": 0.4
      },
      "budget_typical": 3000-5000
    },
    {
      "name": "办公族",
      "priorities": {
        "battery": 0.9,
        "screen": 0.8,
        "performance": 0.6,
        "weight": 0.7,
        "price": 0.7
      },
      "budget_typical": 3000-6000
    },
    {
      "name": "摄影爱好者",
      "priorities": {
        "camera": 0.95,
        "screen": 0.8,
        "performance": 0.6,
        "battery": 0.6,
        "price": 0.5
      },
      "budget_typical": 4000-8000
    }
  ]
}
```

#### 3.5.2 推荐逻辑

```
对每个候选产品计算匹配度：
  match_score = Σ(priority_weight[i] × product_score[i])

例如，对游戏玩家推荐 iPhone 15 Pro Max：
  match_score = 0.9×92 + 0.8×95 + 0.8×78 + 0.5×65 + 0.4×20 = 224/250 = 89.6%

推荐输出：
  "iPhone 15 Pro Max 是最适合你的选择，匹配度 89.6%，主要原因：
   - 性能最强（GPU 性能超越竞品 15%）
   - 屏幕最佳（120Hz Pro Motion，色准 ΔE < 1）
   - 游戏体验最稳定（长期游戏不降频）
   - 唯一不足：价格最高，续航 10h（你可能需要充电宝）"
```

#### 3.5.3 替代方案推荐

```
如果你想降低成本，这是我的 Top 3 替代方案：

1. 小米14 Ultra（节省 2000 元）
   - 性能相差不大（GPU 仅慢 5%）
   - 续航更长 3-4 小时
   - 摄像头更强
   - 风险：系统稳定性不如 iOS
   - 匹配度：85%

2. 三星 S24 Ultra（节省 1500 元）
   - 性能相当
   - 屏幕几乎一样好（120Hz AMOLED）
   - 电池容量大 500mAh
   - 风险：发热可能更严重
   - 匹配度：82%

3. OnePlus 12（节省 2500 元）
   - 性能几乎相同
   - 游戏优化不错
   - 价格最便宜
   - 风险：品牌保值率较低
   - 匹配度：78%
```

---

### 3.6 Report Generation（报告生成）

#### 3.6.1 报告结构

```
1. Executive Summary（执行摘要）
   - 3-5 句话总结对比结果
   - Top 推荐和理由

2. Detailed Comparison（详细对比）
   - 表格：所有关键参数
   - 图表：性能对比、价格趋势、用户评分分布

3. Deep Dive Analysis（深度分析）
   - 各维度详解（为什么选这个不选那个）
   - 隐性成本分析（维修、配件、软件生态成本）
   - 市场动态（新品发布计划、价格预测）

4. Risk Assessment（风险评估）
   - 已知缺陷
   - 长期支持风险
   - 二手价值预测

5. Purchase Recommendation（购买建议）
   - 何时购买（价格最低点预测）
   - 从哪买（比较不同商家）
   - 如何验证真伪
   - 保修和退货政策对比

6. Alternatives & Fallback Plans（替代方案）
   - 如果上面的都缺货/涨价，选什么
   - Budget 版本、高端版本、同价位竞品

7. References（数据来源）
   - 所有引用的网址
   - 数据采集时间
   - 更新频率
```

#### 3.6.2 可视化元素

```
- 参数对比表（sortable、filterable）
- Radar chart：多维度性能可视化
- Price history line chart：价格趋势
- User ratings distribution：评分分布
- Feature matrix：功能矩阵（✓/✗）
- Timeline：发布时间线
- Heatmap：性能热力图（绿=好，红=差）
```

#### 3.6.3 导出格式

```
- Interactive HTML（可在浏览器中操作）
- PDF（可打印）
- Excel（便于本地分析）
- JSON（开放数据格式）
- Markdown（便于分享）
```

---

## 4. 工具集成方案

### 4.1 Playwright 工具组

- 动态爬取电商平台（处理 JS 渲染、动态加载）
- 截图产品图片和规格表
- 自动点击展开评价、规格参数
- 处理反爬虫（User-Agent 轮换、延时、代理）

### 4.2 Search 工具（Google Serper）

- 查询专业评测网站（AnandTech、Tom's Hardware）
- 搜索用户讨论（知乎、Reddit）
- 找价格历史数据

### 4.3 Python REPL 工具

- 数据清洗和标准化（正则提取、单位转换）
- 统计分析（平均值、方差、分布）
- 性价比计算、排序、排名
- 绘图（matplotlib/plotly）生成对比图
- 价格趋势预测（简单线性回归或时间序列）

### 4.4 File Management 工具

- 保存对比报告（HTML、PDF、JSON）
- 读取配置文件（产品参数映射表、用户偏好）
- 存储爬取的原始数据用于后续分析

### 4.5 可选：数据库

- SQLite：存储价格历史、产品基本信息
- 支持查询如"过去一个月内这个产品的最低价"

---

## 5. Evaluator 评估标准

### 5.1 数据完整性检查

```
□ 是否收集了 10+ 个产品？
□ 是否每个产品都有价格数据？
□ 是否有来自 2+ 个权威评测来源的数据？
□ 是否所有价格数据都是同一天期的？
□ 是否标注了数据来源？
```

### 5.2 分析深度检查

```
□ 是否超越了表面参数对比（只看 CPU、内存）？
□ 是否分析了隐性因素（系统优化、续航真实表现）？
□ 是否考虑了用户的具体场景（游戏 vs 办公）？
□ 是否识别了真正的权衡（如便宜但发热、贵但省心）？
□ 是否给出了优缺点的具体数字支撑？
```

### 5.3 推荐合理性检查

```
□ 推荐的产品是否真的最符合用户需求？
□ 是否有清晰的理由说明为什么选这个不选那个？
□ 是否提到了替代方案和它们的权衡？
□ 价格是否最新（不超过 3 天）？
□ 购买建议是否可行（库存、发货、退货政策）？
```

### 5.4 如果评估失败

```
反馈给 Worker：
"你的对比缺少以下信息：
 1. 小米 14 Ultra 的最新价格（当前来源 3 天前）
 2. 真实续航对比（你提了参数但没有实测数据）
 3. 游戏帧率对比（这很重要因为用户优先级是游戏）

请补充这些数据并重新分析。"

Worker 再次调用 Playwright 爬取最新价格、搜索专业评测中的帧率数据等。
```

---

## 6. 系统特色功能

### 6.1 价格预测和购买时机提示

```
基于历史数据，给出购买建议：
"这个产品在过去 6 个月最低价是 4299（黑五期间）
当前价格 5999（高于平均 15%）
预测：双十一 (11/11) 可能降到 4800-5200
建议：等待 11 月促销，或 12 月新品发布后清库存"
```

### 6.2 "如果...那么..." 决策树

```
如果你优先续航      → 推荐小米、三星（容量更大）
如果你玩最新大作    → 推荐 iPhone、一加（性能最强）
如果你经常维修      → 推荐三星（维修网点最多）
如果你在乎隐私      → 推荐 iPhone（闭源系统）
如果你要求便宜      → 推荐红米（子品牌最便宜）
```

### 6.3 二手保值率提示

```
iPhone 15 Pro Max：一年后保值率 ~65%
小米 14 Ultra：一年后保值率 ~40%

计算真实成本：
iPhone：5000 × (1 - 0.65) = 1750 元/年
小米：3500 × (1 - 0.40) = 2100 元/年

从"使用成本"角度，iPhone 反而更划算！
```

### 6.4 配置对标

```
"你提到想对标 iPhone 15 Pro Max，
看看这三款安卓机如何与它对抗：

维度      iPhone 15P  小米14U   三星S24U  OnePlus12
CPU       A18 Pro     SD 8 Gen 3 SD 8 Gen 3 SD 8 Gen 3
GPU       Apple 6c    Adreno 8.5 Adreno 8.5 Adreno 8.5
屏幕      6.7" 120Hz  6.82" 120Hz 6.8" 120Hz 6.7" 120Hz
续航      20h        18h       19h       16h
价格      9999       5999      8999      4999
性价比    1.67       5.83      2.89      7.49 ✓ 最佳
"
```

---

## 7. 数据安全和更新策略

### 7.1 数据来源标注

```
每个数据点都标注来源、采集时间、更新频率
确保用户了解数据的时效性

例如：
价格：来自京东官旗店，采集于 2024-10-16 14:30，每天更新
处理器性能：来自 AnandTech 2024 年评测，基本不变
用户评分：来自京东，每小时更新评价统计
```

### 7.2 数据缓存策略

```
不同数据的缓存时间不同：
- 价格：6 小时
- 库存状态：1 小时
- 规格参数：7 天（基本不变）
- 用户评分：12 小时
- 评测内容：30 天（新评测才更新）
```

### 7.3 反爬虫对策

```
- User-Agent 轮换
- 请求间隔随机化（3-10 秒）
- 使用代理池（可选）
- 尊重 robots.txt
- 不爬取禁止的页面
- 识别为"机器学习研究用途"（若需要）
```

---

## 8. 可能的扩展方向

### 8.1 短期（MVP 阶段）

- 支持 3-5 个主流产品类别（手机、笔记本、平板、相机、耳机）
- 支持 2-3 个国家/地区（中国、美国、欧洲）
- 基础对比和推荐

### 8.2 中期

- 添加专业工作站等高端产品
- 支持 10+ 品牌和 50+ 型号跟踪
- 实时价格提醒功能
- 用户账户和对比历史保存

### 8.3 长期

- 机器学习模型预测产品生命周期和价格变动
- 社区讨论集成（用户分享使用体验）
- 二手交易整合（直接对接二手平台）
- AR 产品对比（手机上虚拟放在一起对比）
- API 开放给开发者或媒体平台

---

## 9. 商业模式设想

### 9.1 免费 + 高级版本

```
免费版本：
- 基础产品对比（5 个产品以内）
- 单一用户角色推荐
- 导出为 Markdown

高级版本（$5-10/月）：
- 无限产品对比
- 多个自定义用户角色
- 导出 PDF 和 Excel
- 价格变动提醒
- 对标跟踪（关注 5 个产品的价格）
```

### 9.2 联盟模式

```
- 链接到电商平台的购买页面（赚取佣金 2-3%）
- 推荐配件（屏幕膜、壳子、充电器等）
```

### 9.3 B2B 模式

```
- 提供 API 给科技媒体、电商平台
- 数据许可给市场研究公司
- 内容许可给评测媒体
```

---

## 10. 实现难点和解决方案

| 难点             | 原因                     | 解决方案                                         |
| ---------------- | ------------------------ | ------------------------------------------------ |
| 数据爬取困难     | 反爬虫、动态加载         | Playwright（处理 JS）+ 代理 + 正常 User-Agent    |
| 数据不一致       | 不同网站参数标准不一     | 建立参数映射表、标准化脚本                       |
| 评测数据稀缺     | 不是每个产品都有专业评测 | 爬取聚合评价 + 官方 spec；缺失时标注"无官方数据" |
| 实时性要求       | 价格每分钟变化           | 缓存策略 + 后台定时爬取                          |
| 隐性成本难以量化 | 如系统优化、售后体验     | 爬取专业评测评论 + 社区讨论 + 建立评分模型       |
| 用户偏好差异大   | 一个产品对所有人不同     | 支持多个用户角色 + 自定义权重                    |
| 模型准确度       | 推荐不准确               | 迭代反馈 + Evaluator 严格把关                    |

---

## 11. MVP（最小可行产品）定义

**第一版的核心功能：**

1. **产品选择：** 仅支持智能手机对比
2. **数据源：**
   - 电商：京东、Amazon
   - 评测：GSMarena、AnandTech、知乎评测
3. **对比维度：** 性能、价格、屏幕、续航、摄像头（6 个主要维度）
4. **推荐角色：** 游戏玩家、办公族、摄影爱好者（3 个角色）
5. **输出：** Gradio 对话 + HTML 报告导出
6. **无需的功能：** 价格预测、二手保值率、反向对标（先不做）

**MVP 预期工作量：** 2-3 周（假设每天 6 小时）

---

## 12. 总结

这个项目的核心价值在于：

1. **解决真实痛点**：消费者很难做出数码产品购买决策
2. **多维度分析**：不只是参数堆砌，而是基于场景的智能对比
3. **个性化推荐**：根据用户优先级和预算给出最佳选择
4. **实时数据**：爬取最新价格和评测，确保信息不过时
5. **LangGraph 深度应用**：Worker 和 Evaluator 的紧密配合展现了 AI agent 的潜力

**后续可以演进成：** 数码产品购买决策的"一站式顾问"，甚至发展为独立的 SaaS 产品。
