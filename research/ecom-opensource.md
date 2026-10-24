# 电商零售财务 / 对账 / 选品 / 库存分析：GitHub 开源可复用件调研

> 调研时间：2026-10-24（Asia/Shanghai）
> 取数方式：`api.github.com/repos/<owner>/<repo>`（star / license / pushed_at）、`ungh.cc/repos/<owner>/<repo>`（star 复核）、`raw` / `contents API` 取 README 与 SKILL.md 正文。
> 口径说明：
> - **star** 为 2026-10-24 当日快照的精确值，同时给出量级（k）。
> - **license** 为 GitHub API 返回的 SPDX 标识；`NOASSERTION` 表示 GitHub 无法归类，本文按仓库 LICENSE 文件正文补注（已读文件头）。
> - **最近更新** = 默认分支最近一次 push 时间（不是 release 时间）。
> - 未实际打开验证的内容一律标注「未核实」，不臆测 star / license。
> 用途：为「电商 CFO agent」筛选可直接借鉴的数据模型、对账规则、指标口径、SKILL 结构。

---

## 0. 总览（按建议优先级排序）

| # | 仓库 | 方向 | star | license | 最近 push | 建议 |
|---|------|------|------|---------|-----------|------|
| 1 | `rongk989-art/ecom-recon-lite` | 对账 | 0 | MIT + 模板 CC BY-NC 4.0 | 2026-09-10 | ★★★ 对账规则直接抄 |
| 2 | `jishenghua/jshERP` | 电商 ERP | 4,675（4.7k） | Apache-2.0 | 2026-10-21 | ★★★ 进销存+财务表结构 |
| 3 | `zeasin/qihang-erp-open` | 多平台订单中台 | 313 | AGPL-3.0 | 2026-10-22 | ★★★ 多平台店铺/订单模型 |
| 4 | `didilili/shopkeeper-agent` | 问数 Agent | 477 | MIT | 2026-10-14 | ★★★ Agent 编排参考 |
| 5 | `FJ-OMS/oms-erp` | OMS/WMS/财务 | 1,928（1.9k） | Apache-2.0 | 2025-12-24 | ★★★ 全渠道一盘货 |
| 6 | `frappe/erpnext` | ERP 底座 | 40,515（40k） | GPL-3.0 | 2026-10-24 | ★★☆ 会计+库存+变体 |
| 7 | `yanhangqi77-hub/Influencer-GMV-Monthly-Update` | 经营 SKILL | 0 | 无 LICENSE | 2026-09-17 | ★★☆ SKILL.md 范本 |
| 8 | `rohitguta2432/ledgermatch` | 支付对账 | 0 | MIT | 2026-09-04 | ★★☆ 三方核对引擎 |
| 9 | `apache/superset` | BI 看板 | 75,278（75k） | Apache-2.0 | 2026-10-24 | ★★☆ 看板层 |
| 10 | `metabase/metabase` | BI 看板 | 49,825（50k） | AGPL-3.0 + 商业双许可 | 2026-10-24 | ★★☆ 轻量看板 |
| 11 | `odoo/odoo` | ERP/电商 | 55,288（55k） | LGPL-3.0（社区版） | 2026-10-24 | ★★☆ 变体/多规格 |
| 12 | `juejin-wuyang/memberclub` | 交易/结算 SDK | 591 | Apache-2.0 | 2025-08-30 | ★★☆ 结算状态机 |
| 13 | `YunaiV/ruoyi-vue-pro` | 中台脚手架 | 40,022（40k） | MIT | 2026-10-23 | ★★☆ ERP/财务模块 |
| 14 | `MrSuiChuan/data-warehouse-learning` | 电商数仓 | 1,265（1.3k） | Artistic-2.0 | 2026-04-26 | ★★☆ 数仓分层 |
| 15 | `roncoo/roncoo-pay` | 对账清结算 | 4,996（5k） | Apache-2.0 | 2022-12-31 | ★☆☆ 架构参考（停更） |
| 16 | `macrozheng/mall` | 电商后台 | 84,951（85k） | Apache-2.0 | 2026-09-15 | ★☆☆ 报表/财务菜单参照 |
| 17 | `vivy-yi/xiaohongshu-skills` | Skill 集合 | 504 | 无 LICENSE | 2026-01-23 | ★☆☆ 结构参考 |
| 18 | `anthropics/skills` | Skill 规范 | 183,321（183k） | 无 LICENSE | 2026-10-09 | ★★☆ SKILL.md 规范 |
| 19 | `PainterAnkry/doujin-retail-analysis` | 售罄率/ROI | 1 | 无 LICENSE | 2026-09-07 | ★☆☆ 分析框架 |
| 20 | `zexian406-cloud/ops-os-review` | SKU 利润/库存健康 | 4 | 无 LICENSE | 2026-10-23 | ★☆☆ 指标清单 |
| 21 | `youngwoner45/FASHION-DASHBOARD` | 服装看板 demo | 0 | 无 LICENSE | 2026-07-20 | ☆ 仅版式参考 |

---

## 1. 电商 ERP / 多平台订单管理

### 1.1 jishenghua/jshERP（管伊佳 ERP，原华夏 ERP）
- URL：https://github.com/jishenghua/jshERP
- 用途：SpringBoot + SaaS 模式的中小企业 ERP，专注**进销存 + 财务**：零售、采购、销售、仓库、财务、报表、权限。
- star：**4,675**（4.7k）；license：**Apache-2.0**；最近更新：**2026-10-21**。
- 可复用点：
  - 零售/批发两套单据流（订单→出库→收款→退货），适合映射成 CFO agent 的「业务单据 → 会计凭证」链路；
  - 预付款、收入支出、仓库调拨、组装拆卸的单据模型，可直接借字段设计；
  - 「库存状况 / 出入库统计」报表口径，是库存周转指标的现成起点；
  - 权限粒度到按钮/菜单，可参考做 agent 的数据权限边界（财务数据只读 vs 可写）。
- 限制：Java + MySQL 单体，财务偏「流水记账」而非权责发生制总账，做 CFO 报表需二次加工。

### 1.2 YunaiV/ruoyi-vue-pro（芋道 yudao）
- URL：https://github.com/YunaiV/ruoyi-vue-pro
- 用途：Spring Boot + MyBatis-Plus + Vue 的后台管理/中台脚手架，内含 **ERP、CRM、商城、支付、报表** 等业务模块。
- star：**40,022**（40k）；license：**MIT**；最近更新：**2026-10-23**。
- 可复用点：
  - `yudao-module-erp` 的采购/销售/库存/财务模块表结构（含库存流水、往来单位），是中文语境下最完整的 MIT 授权 ERP 模型之一；
  - 支付模块的「支付单 / 退款单 / 渠道」三层抽象，对账时可直接承接渠道流水；
  - 多租户 + 数据权限，天然适配「一个 agent 服务多个店铺/公司」。
- 限制：模块多、体量大，抽取单模块成本不低。

### 1.3 zeasin/qihang-erp-open（启航电商 ERP）
- URL：https://github.com/zeasin/qihang-erp-open
- 用途：电商业务中台底座，覆盖**多平台多店铺**的商品、订单、售后、库存、电子面单；对接淘宝、京东、拼多多、抖店、微信小店、快手、小红书；已集成 Spring AI 2.0 与 11 个 AI Tool（可让模型直查 ERP 数据）。
- star：**313**；license：**AGPL-3.0**；最近更新：**2026-10-22**。
- 可复用点：
  - **平台适配层设计**（每平台一个 shop/order 适配器 + 统一内部订单模型），这正是 CFO agent 处理「抖音/淘宝/拼多多字段各不同」的关键抽象；
  - 店铺授权、拉单、发货、售后的任务编排，可参考其幂等与重试；
  - AI Tool（`@Tool` 注解）与 ERP 结构化数据结合的写法，是「agent 读账」最贴近的工程样例。
- 风险：AGPL-3.0，若做 SaaS 对外提供服务需评估开源义务；项目自称仍在重构，稳定性需自测。

### 1.4 FJ-OMS/oms-erp
- URL：https://github.com/FJ-OMS/oms-erp
- 用途：全渠道「一盘货」订单中台（OMS）+ 库存统一管理（WMS）+ 对接 SAP 财务，微服务架构。
- star：**1,928**（1.9k）；license：**Apache-2.0**；最近更新：**2025-12-24**（近一年无 push，活跃度下降）。
- 可复用点：
  - 全渠道订单归集与拆合单、库存占用/释放的状态机；
  - README 明确提出「财务无法实时统计、资金周转率过低」的痛点与「库存共享」解法，可作为 CFO agent 的业务叙事；
  - 订单/库存/财务/商品/营销的领域划分，适合画 agent 的能力边界图。
- 限制：文档以宣传为主，代码可读性未逐一核实。

### 1.5 juejin-wuyang/memberclub
- URL：https://github.com/juejin-wuyang/memberclub
- 用途：电商 C 端交易系统「工具箱」SDK，覆盖交易提单、履约、售后、**结算**、库存管理。
- star：**591**；license：**Apache-2.0**；最近更新：**2025-08-30**。
- 可复用点：结算单与履约单的分离、流程引擎/扩展点引擎（适合把「对账规则」做成可插拔扩展点）、分库分表下的订单号设计。
- 限制：偏教学型 SDK，非完整可运行系统。

### 1.6 frappe/erpnext
- URL：https://github.com/frappe/erpnext
- 用途：Python 全栈开源 ERP（会计、库存、制造、零售 POS、CRM、采购）。
- star：**40,515**（40k）；license：**GPL-3.0**；最近更新：**2026-10-24**（当日有 push，非常活跃）。
- 可复用点（对 CFO agent 价值最高的一件）：
  - **复式记账内核**：GL Entry / Journal Entry / Payment Ledger Entry，天然支持「业务单据 → 会计凭证」；
  - **Item Variant + Attribute**（颜色/尺码属性组合生成 SKU），是服装 SKU 矩阵的成熟实现；
  - Stock Ledger Entry（永续盘存）+ Stock Reconciliation（盘盈亏）+ 存货估值（FIFO/移动加权），库存周转与跌价准备的底座；
  - 「Payment Reconciliation」工具本身就是应收/应付与银行流水核销的交互范式。
- 限制：GPL-3.0，若分发衍生作品需开源；Frappe 框架学习曲线陡。

### 1.7 odoo/odoo
- URL：https://github.com/odoo/odoo
- 用途：全模块开源 ERP（电商 website_sale、库存、发票、会计、POS）。
- star：**55,288**（55k）；license：**LGPL-3.0**（社区版，LICENSE 文件正文明确 LGPLv3；GitHub 标为 NOASSERTION，因含商业条款说明）；最近更新：**2026-10-24**。
- 可复用点：
  - 电商订单 → 发票 → 收款的标准化流程；
  - 产品变体（attribute / variant）与「按变体管库存」的模型，适合服装色码/尺码；
  - 多公司、多币种、税项（tax）配置，跨境场景可参考。
- 限制：社区版功能裁剪，企业版模块闭源；代码量巨大，抽取成本高。

### 1.8 macrozheng/mall
- URL：https://github.com/macrozheng/mall
- 用途：SpringBoot 电商系统（前台商城 + 后台管理），后台含**统计报表、财务管理**菜单。
- star：**84,951**（85k）；license：**Apache-2.0**；最近更新：**2026-09-15**。
- 可复用点：中文电商后台的信息架构（订单/退货/报表/财务）与指标看板布局；作为「agent 输出报告」的界面语言参照。
- 限制：财务模块较浅，不构成真正的账务系统。

---

## 2. 平台账单导出 / 对账工具

> 说明：这一方向的开源生态**普遍小而散**——真正商用的对账逻辑多在闭源 SaaS 或 Excel 模板里。下面 3 个是能核实存在、且逻辑可用的。

### 2.1 rongk989-art/ecom-recon-lite（电商对账 Lite）
- URL：https://github.com/rongk989-art/ecom-recon-lite
- 用途：抖音 / 淘宝 / 拼多多 / 京东的订单表 × 结算账单**自动核对**；提供 GitHub Pages 在线版（纯浏览器计算、不上传数据）+ 无宏 Excel 模板（100 行引擎，红黄绿高亮，内置 12 单演示数据含 2 处埋错）。
- star：**0**（2026-09 新建仓库）；license：**MIT（代码）+ CC BY-NC 4.0（Excel 模板）**（LICENSE 文件正文如此写）；最近更新：**2026-09-10**。
- 可复用点（**本调研中性价比最高的对账知识源**）：
  - 对账恒等式写得非常干净：`应收（实付 + 运费） = 实际到账 + 佣金 + 推广费 + 退款扣回`，误差 > 0.01 元即标红；
  - 差异分类直接可用：⚠未结算 / ❌金额差异 / ❌重复结算 / ❌退款未同步 / 🔔疑似多结算孤儿账单；
  - 「先自测引擎再上真实数据」的思路（埋错样本）值得抄进 agent 的回归测试。
- 限制：star 为 0、仓库带 Pro 版引流；只有 100 行规模，不能直接处理十万级订单；模板为 CC BY-NC，**不可转售**。

### 2.2 rohitguta2432/ledgermatch
- URL：https://github.com/rohitguta2432/ledgermatch
- 用途：自托管的**支付对账**工具：把「订单导出 + Stripe/Square/PayPal 导出 + 银行流水」丢进去，得到匹配台账、手续费汇总、逐笔 payout 与银行入账核对、以及「钱没到」的红名单。FastAPI + Next.js。
- star：**0**；license：**MIT**；最近更新：**2026-09-04**。
- 可复用点：
  - **三方核对（订单 / 支付渠道 / 银行）** 的完整差异清单：missing payments、orphan payments、amount mismatches、unlinked refunds、fees、payout 未到账、payout 短款；
  - 手续费单独成账（不是简单从收入里减），这正是电商 CFO 要的「净额口径」；
  - 匹配键与容差设计（金额容差、时间窗）可直接搬。
- 限制：面向 Stripe/PayPal 生态，国内平台需换适配器；star 0，工程成熟度需自测。

### 2.3 roncoo/roncoo-pay（龙果支付）
- URL：https://github.com/roncoo/roncoo-pay
- 用途：开源互联网支付系统，含独立账户体系、支付接入/交易体系、**对账清结算体系**。
- star：**4,996**（5k）；license：**Apache-2.0**；最近更新：**2022-12-31**（已停更 3 年+）。
- 可复用点：对账文件下载 → 解析 → 与本地交易比对 → 差错池 → 人工处理的**批处理流水线骨架**；账户/记账分录的表设计。
- 限制：技术栈老旧（Spring MVC 时代），只能当架构参考，不要直接部署。

---

## 3. 电商数据分析（GMV / 退货 / ROI / 库存周转）

### 3.1 apache/superset
- URL：https://github.com/apache/superset
- 用途：开源 BI / 数据探索平台，SQL 直连数仓出看板。
- star：**75,278**（75k）；license：**Apache-2.0**；最近更新：**2026-10-24**。
- 可复用点：把 CFO agent 算好的指标表（GMV、退款率、毛利率、周转天数）落成标准数据集 + 看板；行级权限（RLS）适配多店铺；SQL Lab 便于 agent 生成 SQL 后人工复核。
- 限制：需要数仓/数据集市，不能直接读 Excel。

### 3.2 metabase/metabase
- URL：https://github.com/metabase/metabase
- 用途：轻量自助 BI，非技术同学可点选出报表。
- star：**49,825**（50k）；license：**AGPL-3.0 + 商业双许可**（仓库内 `LICENSE-AGPL.txt` / `LICENSE-MCL.txt` / `LICENSE-EMBEDDING.txt` 并存，商用条款需逐条核实）；最近更新：**2026-10-24**。
- 可复用点：面向老板的「一页式经营看板」信息层级；嵌入式分析（embedded analytics）可把看板塞进 agent 的输出页；告警订阅适合「毛利异常/退款率超阈」推送。
- 限制：AGPL 对 SaaS 分发有约束，闭源商用需买 MCL。

### 3.3 didilili/shopkeeper-agent（电商问数）
- URL：https://github.com/didilili/shopkeeper-agent
- 用途：电商数仓「智能问数」AI Agent：LangGraph 编排 + Qdrant（字段/指标语义召回）+ Elasticsearch（字段取值检索）+ MySQL（元数据权威源），流程为「混合检索 → 多阶段推理 → SQL 生成/校验/修正/执行 → 流式返回」。
- star：**477**；license：**MIT**；最近更新：**2026-10-14**。
- 可复用点（**CFO agent 最该抄的架构**）：
  - **元数据知识库 + 指标口径库先行**，再让模型生成 SQL——直接解决「GMV 口径理解错」的幻觉；
  - 字段/指标/取值三类信息协同召回，比表级 RAG 更贴近真实取数；
  - SQL 生成后的校验与自我修正环节，可加「金额必须可追溯到订单号」的硬校验；
  - 配套教程与分支演进，可当团队培训材料。

### 3.4 MrSuiChuan/data-warehouse-learning
- URL：https://github.com/MrSuiChuan/data-warehouse-learning
- 用途：电商系统实时/离线数仓建设方案与实战代码（Flink、Paimon、Doris、SeaTunnel 等）。
- star：**1,265**（1.3k）；license：**Artistic-2.0**；最近更新：**2026-04-26**。
- 可复用点：ODS→DWD→DWS→ADS 分层里，订单、支付、退款、商品维度的建模样例；GMV 事实表粒度（订单/子订单/商品行）选择。
- 限制：偏大数据组件教学，轻量场景过重。

### 3.5 zexian406-cloud/ops-os-review
- URL：https://github.com/zexian406-cloud/ops-os-review
- 用途：亚马逊卖家运营操作系统：**SKU 利润分析、自动补货建议、库存健康监控、成本核算看板**，一键导入后台数据替代每周手工 Excel。
- star：**4**；license：**无 LICENSE 文件**（默认版权保留）；最近更新：**2026-10-23**。
- 可复用点：SKU 级利润表字段（售价、平台佣金、FBA 费、广告费、退货、头程、采购成本 → 净利）+ 库存健康分级（滞销/断货风险/超储）的阈值清单。
- 限制：无 README（仅仓库描述可见），代码质量未核实；license 缺失，只能读思路。

---

## 4. 服装行业：SKU / 尺码色码 / 售罄率

> 现实：**服装垂直开源项目极少且多为教学/毕设级**。稳妥做法是「通用 ERP 的变体模型 + 零售分析脚本」组合，而不是找现成服装 ERP。

### 4.1 PainterAnkry/doujin-retail-analysis
- URL：https://github.com/PainterAnkry/doujin-retail-analysis
- 用途：谷子店「淘宝店 + 漫展」双渠道经营分析（Python pandas/scipy/matplotlib）：品类 ABC、价格带、IP 生命周期、**售罄率复盘**、展会 ROI、双渠道引流。
- star：**1**；license：**无**；最近更新：**2026-09-07**。
- 可复用点：
  - 售罄率/断货/压货/清仓效果的单场复盘模板（正是服装季末复盘的同一套逻辑）；
  - ABC 分类 + 价格带分析脚本，可直接换数据用于选品；
  - 数据字典与「一页纸结论报告」结构，适合做 agent 的输出模板。
- 限制：数据为按真实结构构造的模拟数据（作者已注明）；仅 1 star，代码需自读。

### 4.2 youngwoner45/FASHION-DASHBOARD
- URL：https://github.com/youngwoner45/FASHION-DASHBOARD
- 用途：服装运营数据自动化看板，直观展示各品类**售罄率**与销售情况。
- star：**0**；license：**无**；最近更新：**2026-07-20**。
- 可复用点：仅 `README.md + index.html` 的单页 demo，可看指标卡与图表排版（售罄率、品类对比）。
- 限制：无数据处理逻辑，**不建议作为实现依赖**。

### 4.3 借通用 ERP 解决服装 SKU（推荐路径）
- `frappe/erpnext`：Item Attribute（颜色/尺码）→ Item Variant 自动生成 SKU 矩阵，变体级库存与变体级成本：https://github.com/frappe/erpnext
- `odoo/odoo`：product.attribute / product.variant + 变体级库存与条码：https://github.com/odoo/odoo
- 服装特有的「色码/尺码曲线、断码率、首单深度、补单、季末清仓」在开源里**没有现成实现**，需自建（见第 6 节口径）。

---

## 5. 可借鉴的 agent skill（SKILL.md 类项目）

### 5.1 anthropics/skills
- URL：https://github.com/anthropics/skills
- 用途：Anthropic 官方 Agent Skills 仓库，含 `xlsx`、`docx`、`pptx`、`pdf`、`skill-creator` 等技能与 `spec/`、`template/`。
- star：**183,321**（183k）；license：**无 LICENSE 文件**（默认版权保留，可读不可直接复制分发）；最近更新：**2026-10-09**。
- 可复用点：
  - **SKILL.md 的目录规范与 frontmatter**（`name` / `description` 触发词写法）——CFO agent 的每个能力都应按此封装；
  - `xlsx` skill 的「读表 → 改公式 → 重算 → 校验」流程，可直接用于月度对账表；
  - `skill-creator` 提供了新建/校验 skill 的元流程，适合团队批量产出财务技能。

### 5.2 yanhangqi77-hub/Influencer-GMV-Monthly-Update（达人 GMV 更新 Skill）
- URL：https://github.com/yanhangqi77-hub/Influencer-GMV-Monthly-Update
- 用途：Codex 工作流 skill：清洗 TikTok Shop 原始订单 → 按 Paid Time 归月 → 汇总达人 GMV/订单数/SKU 数/渠道占比 → 写入飞书表格（月度归档 + 滚动最新两组 sheet）。
- star：**0**；license：**无**；最近更新：**2026-09-17**。
- 可复用点（**SKILL.md 写法的最佳样本**）：
  - frontmatter 里用 `description` 写清触发语（"当用户要求更新某月达人 GMV…"），并声明 `metadata.requires.bins`；
  - **指令路由表**：不同说法 → 不同写入范围，且明确「不得顺带更新另一组」；
  - **口径写死在文档里**：GMV 用 Order Amount；涨佣用「已付款扣除取消/退款退货的净件数」，按单个产品判档；空达人归 Unattributed 不参与排名；
  - 数据安全约束：默认不写入买家姓名/电话/地址；
  - 幂等与覆盖规则：复用稳定 `sheet_id`，不按日期新建表。
- 限制：0 star、绑定飞书与 `lark-cli`，代码不可直接复用，**但文档结构 100% 可抄**。

### 5.3 vivy-yi/xiaohongshu-skills
- URL：https://github.com/vivy-yi/xiaohongshu-skills
- 用途：139 个小红书运营技能的 Claude Code 插件集合，覆盖内容创作、账号运营、数据分析、**电商转化**、平台规则等 9 大类。
- star：**504**；license：**无**；最近更新：**2026-01-23**。
- 可复用点：多 skill 的组织方式（`skills/` + `skills-guide.md` + `.claude-plugin` 清单）、技能之间的引用与分工；电商转化类技能可作话术/漏斗分析的素材。
- 限制：偏运营增长，非财务；license 缺失，商用需谨慎。

---

## 6. 可直接沉淀为 skill 的知识

> 以下内容综合了第 2 节两个对账项目的显式规则、ERP 项目的数据模型（ERPNext/Odoo/jshERP）以及电商财务通行做法。凡是「通行做法」而非某仓库原文的，均按业务共识表述，不冒充出处。

### 6.1 三方核对流程（订单 → 账单 → 资金）

```
L0 主数据对齐
   店铺映射表 / 商品SPU-SKU映射 / 平台费用科目映射 / 汇率表
        │
L1 订单层（业务应收）        平台后台「订单导出」
   订单号、子订单号、SKU、数量、实付、运费、优惠分摊、状态、付款时间
        │  应收 = 实付 + 运费（买家实付口径）
        ▼
L2 结算层（平台应付）        平台「结算单/账单导出」
   结算单号、关联订单号、商品金额、佣金/技术服务费、推广费、运费险、
   平台补贴、退款扣回、结算周期、打款批次
        │  到账 = 应收 − 佣金 − 推广费 − 退款扣回 − 其他扣费 ± 补贴
        ▼
L3 资金层（实际到账）        支付宝/微信/银行流水
   到账金额、到账时间、对手方、摘要、批次号/打款单号
        │
   四方对齐：订单 ↔ 账单 ↔ 打款批次 ↔ 银行流水
```

**四步执行法（写进 skill 的固定步骤）**

1. **完整性核对（存在性）**：L1 有、L2 无 → 未结算；L2 有、L1 无 → 孤儿账单；L3 有、L2 无 → 来源不明入账。
2. **金额核对（数值）**：按 `订单号` 聚合后比对 `应收` 与 `账单净额 + 扣费明细`，容差 **0.01 元**（`ecom-recon-lite` 采用的口径），超差进差异池。
3. **时序核对（期间）**：下单时间 vs 结算时间 vs 到账时间，跨月订单按**结算月**确认平台收入、按**发货/签收**确认商品收入，两者差异进「跨期调节表」。
4. **归属核对（主体）**：店铺/主体/币种/打款账户是否一致；集团多主体时按法人拆分，禁止混同。

**期末调节表（bridge，CFO 最需要的产出）**

```
期初应收 + 本期新增应收 − 本期已结算 − 本期退款冲回 ± 调整 = 期末应收
期末应收 − 在途结算（已结算未到账） − 争议挂账 = 应等于 0
银行到账 = 本期结算 − 在途 − 平台预扣（保证金/服务费）
```

**闭环要求**：每笔差异必须有 `差异类型 / 金额 / 责任方（平台/物流/内部）/ 处置动作 / 截止日 / 状态`，未闭环项进「异常台账」，月末只报「新增 + 已闭环 + 超期未闭环」三个数。

### 6.2 关键字段字典

| 层 | 字段 | 用途 | 校验点 |
|----|------|------|--------|
| 订单 | `order_id` / `sub_order_id` | 主匹配键（子单粒度才对得上账单） | 全局唯一、无前后空格、大小写一致 |
| 订单 | `pay_time` | 归月/归期基准 | 时区统一（+08:00）、空值=未付款 |
| 订单 | `order_status` | 排除取消/未付款/全额退款 | 状态枚举需与平台版本对齐 |
| 订单 | `paid_amount` / `freight` | 应收 = 实付 + 运费 | 实付是否已含运费（平台差异大） |
| 订单 | `discount_alloc` | 优惠分摊到行 | 分摊后各行之和必须等于订单优惠 |
| 商品 | `spu_id` / `sku_id` / `sku_code` | 选品与库存分析主键 | 平台商品ID ↔ 内部SKU 映射表必填 |
| 商品 | `color` / `size` | 服装色码/尺码 | 尺码标准化（S/M/L vs 160/84A） |
| 账单 | `settle_id` / `settle_period` | 结算批次 | 与打款批次号一一对应 |
| 账单 | `commission` / `tech_fee` | 平台佣金/技术服务费 | 费率 × 类目，需与合同费率表比对 |
| 账单 | `ad_fee` | 推广费（直通车/千川） | 是否已在账单内扣，避免二次扣减 |
| 账单 | `refund_deduct` | 退款扣回 | 与退款单号关联，防重复扣 |
| 账单 | `subsidy` | 平台补贴/百亿补贴 | 计入毛额还是净额，口径必须固定 |
| 资金 | `bank_txn_id` / `payout_batch` | 银行流水匹配 | 一对多（一个批次含多订单） |
| 资金 | `counterparty` | 对手方（平台主体名） | 主体名与店铺授权主体一致 |
| 退货 | `return_id` / `return_qty` / `refund_amount` | 退货率、净GMV | 退款金额与退货件数**不重复扣减** |
| 达人 | `creator_id` / `channel` | 直播/达人归因 | 空达人归 Unattributed，不参与排名 |

### 6.3 常见差异类型（差异池分类法）

| # | 差异类型 | 典型成因 | 处置动作 |
|---|----------|----------|----------|
| 1 | **未结算**（订单有、账单无） | 未到结算周期 / 平台漏打款 / 订单被风控冻结 | 标记账龄，>1 个结算周期升级 |
| 2 | **金额差异** | 佣金费率错、优惠分摊方式不同、运费口径不同、抹零 | 拆到费用行逐项比，超 0.01 元才报 |
| 3 | **重复结算** | 同一订单号在账单出现 ≥2 次 | 全额挂账，向平台申诉 |
| 4 | **退款未同步** | 订单已退款、账单未扣回（或反之） | 按退款单号配对，跨期需做调节 |
| 5 | **孤儿账单**（账单有、订单无） | 历史订单补结、跨店铺串账、刷单被剔除后余额 | 反查订单号前缀/时间，确认归属期 |
| 6 | **跨期错配** | 下单在 3 月、结算在 4 月 | 收入按结算月确认，建跨期调节表 |
| 7 | **补贴口径不一致** | 平台补贴计入 GMV 毛额 vs 净额 | 固定「GMV 含补贴、净收入不含」并全表统一 |
| 8 | **费用漏计** | 运费险、软件服务费、支付通道费未入账 | 建费用科目清单，逐项打勾 |
| 9 | **拆单/组合装/赠品** | 一件代发多包裹、套装拆行、赠品 0 元行 | 按子单+商品行匹配，赠品单独标记 |
| 10 | **跨境汇率与四舍五入** | 币种换算、平台按本币结算 | 锁定结算日汇率，差额进汇兑损益 |
| 11 | **虚假交易/刷单剔除** | 平台事后剔除订单 | 单独科目，不计入经营 GMV |
| 12 | **达人佣金/坑位费未入账** | 直播带货佣金线下结算 | 建「达人应付」台账，与 GMV 归因对齐 |

### 6.4 指标口径（写死在 skill 里，禁止临场发挥）

| 指标 | 公式 | 关键约定 |
|------|------|----------|
| GMV（成交） | Σ 订单实付金额（含运费，含平台补贴） | 是否含退款/取消必须声明；建议同时给「毛 GMV / 净 GMV」 |
| 净 GMV | GMV − 退款金额 − 取消金额 | 按**退款发生月**冲减，不追溯修改历史月 |
| 退款率 | 退款金额 / GMV | 与「退货率（件数）」分开报 |
| 客单价 AOV | 净 GMV / 有效订单数 | 有效订单需剔除刷单与全额退款 |
| 毛利 / 毛利率 | (净 GMV − 商品成本 − 平台佣金 − 推广费 − 物流 − 达人佣金) / 净 GMV | 成本口径：含税/不含税须固定；佣金按实际账单而非费率估算 |
| ROI / ROAS | 净 GMV / 推广费 | 归因窗口写明（当日/7 日/15 日） |
| 库存周转天数 | 平均库存成本 / 日均销售成本（近 30/90 天） | 用**成本**不用零售价；季节性品类需分季看 |
| 库存周转率 | 销售成本 / 平均库存成本 | 与周转天数互为倒数年化 |
| 售罄率 | 累计销售数量 /（累计销售 + 期末库存） | 区分「正价期售罄率」与「含清仓售罄率」 |
| 动销率 | 有销售 SKU 数 / 在库 SKU 数 | 按月滚动，识别滞销 |
| 库销比 | 期末库存金额 / 当月销售金额 | 服装健康区间通常 2–4（需按品类校准） |
| 断码率 | 断码 SKU 数 / 在售 SKU 数 | 服装专属，按尺码维度算 |

### 6.5 服装行业专属处理

1. **SKU 编码**：`品牌-品类-款号-颜色-尺码`，颜色/尺码用标准码表（禁止自由文本），否则无法做尺码曲线。
2. **尺码曲线**：按品类维护 S/M/L/XL 销售占比基准，实际偏离 >15% 时提示补单/调价。
3. **售罄率分两段**：正价期（衡量选品与首单深度）+ 清仓期（衡量清货效率），混算会掩盖选品失误。
4. **退货归因**：尺码不符/色差/质量分类统计，尺码类退货要回写到「尺码曲线」修正首单深度。
5. **跌价准备**：季末按库龄（0–30/31–60/61–90/90+ 天）计提，CFO 报表需与存货周转天数联动。
6. **首单深度与补单**：`首单量 = 预计销量 × (1 − 目标售罄率)`；补单周期受面料交期约束，需在 skill 里内置交期参数。

### 6.6 CFO agent 的 SKILL.md 骨架（建议直接套用）

```markdown
---
name: ecom-reconciliation
description: "电商多平台对账与差异分析。当用户要求对账、核对订单与账单、查未结算/多结算/退款未同步、
  出月末资金调节表时使用。"
metadata:
  requires:
    files: ["订单导出.xlsx", "结算账单.xlsx", "银行流水.csv"]
---

# 电商对账

## 输入契约
- 必需：订单导出、结算账单；可选：银行流水、退款明细、费用率表
- 缺字段时先列「缺失清单」并停止，不猜字段

## 口径（不得改动）
- 应收 = 实付 + 运费；到账 = 应收 − 佣金 − 推广费 − 退款扣回 ± 补贴
- 容差 0.01 元；跨期按结算月；退款按发生月冲减

## 步骤
1. 主数据对齐（店铺/SKU/费用科目映射）→ 输出未映射清单
2. 完整性核对 → 未结算 / 孤儿账单
3. 金额核对 → 金额差异（拆到费用行）
4. 时序核对 → 跨期调节表
5. 归属核对 → 多主体拆分
6. 输出：差异台账 + 期末调节表 + 三个数（新增/已闭环/超期）

## 输出模板
| 差异类型 | 订单号 | 金额 | 责任方 | 处置动作 | 截止日 | 状态 |

## 硬性约束
- 每个数字必须能追溯到「文件 + 行号 + 字段」
- 不编造缺失数据；无法核实的项标「待核实」
- 不覆盖原始文件，输出新文件并保留处理日志
```

### 6.7 从这些仓库直接可搬的「零件」

| 需求 | 直接借用 | 出处 |
|------|----------|------|
| 对账恒等式与差异分类 | 五类差异 + 0.01 容差 | `ecom-recon-lite` |
| 三方（订单/渠道/银行）核对清单 | 7 类 money-miss 检查 | `ledgermatch` |
| 多平台订单统一模型 | 平台适配器 + 内部订单 | `qihang-erp-open` |
| 变体级 SKU/库存/成本 | Item Attribute → Variant | `erpnext` / `odoo` |
| 业务单据 → 会计凭证 | GL Entry / Journal Entry | `erpnext` |
| 指标问数（NL2SQL） | 元数据+指标库 → 检索 → 生成 → 校验 | `shopkeeper-agent` |
| 结算状态机 | 交易/履约/结算分离 | `memberclub` |
| SKILL.md 写法 | frontmatter + 指令路由 + 口径锁定 | `Influencer-GMV-Monthly-Update` |
| 看板呈现 | 一页式经营看板 | `metabase` / `superset` |

---

## 7. 核实记录与未核实项

**已核实（2026-10-24 通过 GitHub API 实取）**：上表 21 个仓库的 star、license、pushed_at；已读 LICENSE 正文的：`odoo`（LGPLv3）、`ecom-recon-lite`（MIT + CC BY-NC）、`metabase`（LICENSE-AGPL / MCL / EMBEDDING 三文件并存）。

**未核实**：
- `zexian406-cloud/ops-os-review`、`youngwoner45/FASHION-DASHBOARD` 的代码质量与可运行性（前者无 README，后者仅单页 HTML）；
- `FJ-OMS/oms-erp` 的实际代码完整度（README 以方案宣传为主）；
- Metabase 商业条款（`LICENSE-MCL.txt` 仅 425 字节，未逐条读）；
- 各仓库 issue 活跃度、CI 状态、生产可用性。

**结论性判断**：
1. 中文电商 ERP/订单中台有真实可用件（jshERP、启航、OMS、memberclub），**但财务深度普遍不足**，做 CFO agent 应以 ERPNext 的复式记账 + 存货模型为账务底座，中文项目提供业务单据字段。
2. **对账这一环没有「大而全」的开源件**，价值集中在两份小仓库的**规则与差异分类**上——这恰好是最适合沉淀成 SKILL 的部分。
3. 服装垂直方向几乎空白，必须自建「SKU 矩阵 + 售罄率 + 尺码曲线」逻辑，不要指望现成项目。
4. Agent 侧最值得抄的是 `shopkeeper-agent` 的「元数据库先行 + 检索增强 + SQL 校验」和 `Influencer-GMV` 的「口径写死 + 指令路由」。
