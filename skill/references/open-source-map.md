# 开源资源地图（可复用/可借鉴）

> 数据来源：2026-10-24 GitHub API 逐个核实 star / license / 最近推送；未核实项已标注。
> 用途：需要自建工具、抄作业、或评估"要不要上系统"时查这张表。**不建议直接把 AGPL/无 LICENSE 项目用于生产。**

## 一、记账与会计引擎

| 仓库 | 星 | 许可 | 一句话 | 可复用点 |
|---|---:|---|---|---|
| [beancount/beancount](https://github.com/beancount/beancount) | 6.1k | GPL-2.0 | 纯文本复式记账 | 科目树、凭证校验、账本即代码的思路；适合做数据层 |
| [ledger/ledger](https://github.com/ledger/ledger) | 6.1k | 未核实 | 命令行复式记账鼻祖 | 复式记账规则与报表生成逻辑 |
| [hledgerorg/hledger](https://github.com/hledgerorg/hledger) | 4.8k | GPL-3.0 | Haskell 版复式记账 CLI | 多币种、预算报告的实现参考 |
| [firefly-iii/firefly-iii](https://github.com/firefly-iii/firefly-iii) | 2.5万 | AGPL-3.0 | 个人/小企业财务管家 | 预算、分类、报表的 UI 与数据模型 |
| [actualbudget/actual](https://github.com/actualbudget/actual) | 3.0万 | MIT | 本地优先预算工具 | 信封预算（envelope budgeting）交互 |
| [mayswind/ezbookkeeping](https://github.com/mayswind/ezbookkeeping) | 5.8k | MIT | 中文轻量记账 | 中文场景的科目与报表翻译 |
| [Gnucash/gnucash](https://github.com/Gnucash/gnucash) | 4.4k | 未核实 | 桌面复式记账 | 小企业账簿结构 |

## 二、财务/ERP 系统

| 仓库 | 星 | 许可 | 一句话 | 可复用点 |
|---|---:|---|---|---|
| [frappe/erpnext](https://github.com/frappe/erpnext) | 4.1万 | GPL-3.0 | 全栈开源 ERP | 单据→分录→三表的完整链路；科目与成本核算 |
| [akaunting/akaunting](https://github.com/akaunting/akaunting) | 1.0万 | 未核实 | 中小企业财务/发票 | 发票-账单-报表模型 |
| [jishenghua/jshERP](https://github.com/jishenghua/jshERP) | 4.7k | Apache-2.0 | 中文进销存+财务 | 采购/销售/库存/应收应付的本土单据流 |
| [jinbooks/jinbooks](https://github.com/jinbooks/jinbooks) | 77 | Apache-2.0 | 中文财务/代账 | 月结、结转、代账流程骨架 |

## 三、税务与计算

| 仓库 | 星 | 许可 | 一句话 | 可复用点 |
|---|---:|---|---|---|
| [next-1688/1688-finance-tax](https://github.com/next-1688/1688-finance-tax) | 452 | 无（未声明） | 财税税负测算 skill | **只借鉴结构**：三入口（算增值税/四税联算/整体税负）+ 意图路由 + JSON 输出；真实测算走云端，算法不公开 |
| [kylin985ti/china-accounting-skills](https://github.com/kylin985ti/china-accounting-skills) | 80 | MIT | 中国会计准则技能包 | `shared/tax-rates-reference/` 税率速查表（2025–2026 口径）与技能分层组织 |
| [guanshuicheng/invoice](https://github.com/guanshuicheng/invoice) | 2.0k | MIT | 增值税发票 OCR（YOLO+CRNN） | 发票版式定位→字段抽取链路；已停更（2024-09），需自行升级依赖 |
| [liriansu-opus/chinese-calendar](https://github.com/liriansu-opus/chinese-calendar) | 1.4k | MIT | 中国节假日/调休判定（原 LKI/chinese-calendar） | 判断截止日是否顺延；征期表仍需自己维护 |
| [chensheng86668/Accounting-software](https://github.com/chensheng86668/Accounting-software) | <10 | MIT | 中文记账软件（Docker + AI 记账 + Excel 报表） | 小微企业流水台账的最小数据模型 |
| [PSLmodels/Tax-Calculator](https://github.com/PSLmodels/Tax-Calculator) | 314 | NOASSERTION（需读 LICENSE） | 美国联邦个税微模拟 | 参数与代码分离、reform 叠加、与官方样例对拍的测试体系 |
| [openfisca/openfisca-core](https://github.com/openfisca/openfisca-core) | 248 | AGPL-3.0 | "立法即代码"规则引擎 | entity/role、period 语义、参数树——**中国税制最该抄的架构**；AGPL 只可借鉴不可集成 |
| [PolicyEngine/policyengine-us](https://github.com/PolicyEngine/policyengine-us) | 170 | AGPL-3.0 | 美国税制/福利规则引擎 + 微观模拟 | 计算内核与展示层分离、参数变更走 PR+测试的变更管理 |
| [ctkqiang/ChineseTaxSystem](https://github.com/ctkqiang/ChineseTaxSystem) | <10 | 无 | COBOL 个税计算器 | 七级累进与速算扣除数的交叉验证样本，无工程复用价值 |
| [hello2sherlei/salary-calculator](https://github.com/hello2sherlei/salary-calculator) | <10 | 无 | 工资倒推计算器 | "到手反推税前"的交互范式 |

> 关键结论：**中国没有宽松许可的全税种计税引擎**（最接近的 1688-finance-tax 是云端黑盒且无 license）。计税逻辑必须自建 —— 这也是本技能自带 `scripts/checkup.py` 的原因。

## 四、企业运营系统（选型参考）

| 仓库 | 星 | 许可 | 一句话 | 可复用点 |
|---|---:|---|---|---|
| [YunaiV/ruoyi-vue-pro](https://github.com/YunaiV/ruoyi-vue-pro) | 4.0万 | MIT | 后台+工作流底座 | 权限/多租户/审批骨架 |
| [jeecgboot/JeecgBoot](https://github.com/jeecgboot/JeecgBoot) | 4.8万 | Apache-2.0 | AI 低代码平台 | 快速搭审批类单据 |
| [dromara/skyeye](https://github.com/dromara/skyeye) | 1.2k | MIT | 一体化企业平台 | "企业该有哪些管理模块"清单 |
| [InvenTree/InvenTree](https://github.com/InvenTree/InvenTree) | 7.8k | MIT | 库存/物料管理 | BOM、批次、库位模型 |
| [flowable/flowable-engine](https://github.com/flowable/flowable-engine) | 9.6k | Apache-2.0 | BPMN 工作流 | 审批流建模 |
| [paperless-ngx/paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) | 4.7万 | GPL-3.0 | 文档 OCR 归档 | 合同/发票/证照归档检索 |

## 五、法条与合同（超出本技能范围，备查）

| 仓库 | 星 | 许可 | 一句话 | 可复用点 |
|---|---:|---|---|---|
| [LawRefBook/Laws](https://github.com/LawRefBook/Laws) | 1.9k | 未核实 | 中国法律法规 Markdown | 公司法/劳动合同法条文，可做 RAG 语料 |
| [lawtext/laws](https://github.com/lawtext/laws) | 111 | 未指定 | 法律在线文库 | 源自 flk.npc.gov.cn 的权威正文，核对条号 |
| [cncases/cases](https://github.com/cncases/cases) | 1.1k | MPL-2.0 | 裁判文书本地检索 | 类案支撑 |
| [cat-xierluo/contract-copilot.skill](https://github.com/cat-xierluo/contract-copilot.skill) | 51 | 未核实 | 合同审查 skill | 三层分析+四步流程+审查意见书模板 |

## 六、同类 skill（直接借鉴写法）

| 仓库 | 说明 | 借鉴点 |
|---|---|---|
| [kylin985ti/china-accounting-skills](https://github.com/kylin985ti/china-accounting-skills) | 中国会计准则技能包（记账/报表/税务/审计） | 技能拆分粒度、参考文件组织 |
| [Geeksfino/finskills](https://github.com/Geeksfino/finskills) | 财务分析 skill 集 | SKILL.md 结构、财报分析口径 |
| [cat-xierluo/legal-skills](https://github.com/cat-xierluo/legal-skills) | 法律技能集合 | 触发词、输出格式设计 |
| [next-1688/1688-finance-tax](https://github.com/next-1688/1688-finance-tax) | 税负测算 skill | 四税联算的场景拆法 |

## 八、电商对账与 ERP（服装零售）

| 仓库 | 星 | 许可 | 一句话 | 可复用点 |
|---|---:|---|---|---|
| [jishenghua/jshERP](https://github.com/jishenghua/jshERP) | 4.7k | Apache-2.0 | 中文进销存+财务 ERP | 零售/退货单据流→收付款链路；库存报表口径 |
| [frappe/erpnext](https://github.com/frappe/erpnext) | 4.1万 | GPL-3.0 | Python 全栈 ERP | **会计内核**（GL Entry）、Item Attribute/Variant 生成色码×尺码 SKU、永续盘存与盘盈亏 |
| [odoo/odoo](https://github.com/odoo/odoo) | 5.5万 | LGPL-3.0 | 全模块 ERP | 变体库存、订单→发票→收款流程 |
| [zeasin/qihang-erp-open](https://github.com/zeasin/qihang-erp-open) | 313 | AGPL-3.0 | 多平台电商 ERP | **平台适配层**（淘宝/拼多多/抖店字段各异）、Spring AI Tool「agent 读账」写法 |
| [FJ-OMS/oms-erp](https://github.com/FJ-OMS/oms-erp) | 1.9k | Apache-2.0 | 全渠道订单中台 | 订单归集/拆合单、库存占用释放状态机 |
| [juejin-wuyang/memberclub](https://github.com/juejin-wuyang/memberclub) | 591 | Apache-2.0 | 交易/结算 SDK | 结算单与履约单分离、对账规则做成可插拔扩展点 |
| [macrozheng/mall](https://github.com/macrozheng/mall) | 8.5万 | Apache-2.0 | 中文电商系统 | 后台信息架构与报表看板布局（财务较浅） |
| [rongk989-art/ecom-recon-lite](https://github.com/rongk989-art/ecom-recon-lite) | 0 | MIT（模板 CC BY-NC） | 电商对账 Lite | **对账恒等式**：应收（实付+运费）= 到账+佣金+推广+退款扣回；5 类差异、0.01 元容差 |
| [rohitguta2432/ledgermatch](https://github.com/rohitguta2432/ledgermatch) | 0 | MIT | 支付对账 | 订单/渠道/银行三方核对 7 类「钱没到」；手续费单独成账 |
| [roncoo/roncoo-pay](https://github.com/roncoo/roncoo-pay) | 5k | Apache-2.0 | 支付清结算 | 对账文件→比对→差错池→人工处理流水线（停更，仅架构参考） |
| [didilili/shopkeeper-agent](https://github.com/didilili/shopkeeper-agent) | 477 | MIT | 电商问数 Agent | **元数据+指标口径库先行，再生成 SQL 并校验**——治「GMV 口径理解错」 |
| [apache/superset](https://github.com/apache/superset) | 7.5万 | Apache-2.0 | BI 看板 | 指标数据集 + 行级权限（多店铺） |
| [metabase/metabase](https://github.com/metabase/metabase) | 5万 | AGPL + 商用许可 | 自助 BI | 一页式经营看板的信息层级 |
| [MrSuiChuan/data-warehouse-learning](https://github.com/MrSuiChuan/data-warehouse-learning) | 1.3k | Artistic-2.0 | 电商数仓 | 订单/支付/退款事实表粒度（GMV 口径落地） |

> 关键结论：**电商 ERP 有真件，但财务深度不足**（jshERP 偏流水记账，不是权责发生制总账）；**对账没有大而全的开源件**，价值集中在两个 0 星小仓库的规则里；**服装垂直几乎空白**（SKU 矩阵、售罄率、尺码曲线要自建）。账务底座建议直接参考 ERPNext 的 GL Entry + Item Variant。

## 九、避坑

- **AGPL**（firefly-iii、docuseal、openfisca-core、steedos、espocrm）：商用/闭源集成前必须评估，SaaS 场景有传染性。
- **无 LICENSE**（WukongCRM、vhr、LawBench 类）：默认保留所有权利，只能读不能抄。
- **停更**（WukongCRM 2021 停更）：数据模型可参考，代码不要上生产。
- **star 数不等于质量**：财税类项目小众但业务价值高（如 jinbooks 77 星，流程却比很多大项目完整）。

> 调研明细（含每个仓库的核实状态与缺口）见本仓库 `research/` 目录：tax.md / finance.md / operations.md / ecom-platforms.md / ecom-accounting.md / ecom-opensource.md。
