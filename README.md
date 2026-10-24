# myCFO

> 面向中国大陆小微企业（默认**服装电商零售**：拼多多 / 淘宝天猫 / 抖音）的 **CFO Agent 技能包**。
> 让 AI 以 CFO 视角回答：这个月交多少税、钱够不够、哪个款在亏、要不要转一般纳税人。

不是 SaaS，不是记账软件。它是一套给 AI Agent 用的**技能文件 + 可执行计算脚本**：
Agent 读 `SKILL.md` 决定流程，读 `references/` 拿专业口径，跑 `scripts/` 出确定性的数字。

## 能做什么

| 能力 | 入口 | 说明 |
|---|---|---|
| 报税与合规日历 | `references/tax-cn.md` | 2026 年度官方征期（税总办征科函〔2025〕64 号）、各税种税率、优惠、处罚 |
| 税负测算 | `scripts/checkup.py` | 增值税 + 附加税费 + 印花税 + 企业所得税预缴，含红黄绿灯预警 |
| 税务筹划（合法） | `references/tax-planning.md` | T1–T9 工具箱（免征额、500 万临界、小微 5%、年终奖、加计扣除…）+ 7 条禁区 |
| 小规模 vs 一般纳税人 | `scripts/tax_mode_compare.py` | 税负断崖、进项票敏感性、临界比例、**300 万所得税悬崖**、500 万双口径 |
| 电商经营模型 | `references/ecommerce-retail.md` | GMV→收入桥、平台费率与账期、退货准备金、库存与售罄、爆量现金流陷阱 |
| 单元经济 | `scripts/ecom_unit_econ.py` | 单品贡献率、保本 ROAS、保本售价、退货敏感性、SKU ABC/滞销预警 |
| CPA 级会计 | `references/ecommerce-accounting.md` | 总额法/净额法、10 类分录、月末结账 10 步、成本核算、三表编制、三方对账 |
| 电商税务专题 | `references/ecommerce-tax.md` | 无票采购五条合规路径、500 万/300 万双悬崖、达人佣金、刷单、稽查关注点 |
| 财务分析与预算 | `references/financial-analysis.md`、`budget-cashflow.md` | 三表勾稽、40+ 比率、杜邦、诊断树、13 周现金流、保本点 |
| 开源资源地图 | `references/open-source-map.md` | 会计/税务/ERP/对账/BI 可复用项目（star/license 已核实） |

## 快速开始

### 1. 安装成技能

```bash
# DeepSeek Harness
git clone https://github.com/whoisjackchao-dot/myCFO.git ~/.dsh/skills/company-ops

# Claude Code
git clone https://github.com/whoisjackchao-dot/myCFO.git ~/.claude/skills/company-ops

# OpenCode / 其他支持 skills 的 Agent
git clone https://github.com/whoisjackchao-dot/myCFO.git .opencode/skills/company-ops
```

也可以直接把本仓库复制到任意 skills 目录，或让 Agent 直接读取 `SKILL.md`。

### 2. 首次使用：建档

按 `assets/company-profile.md`（通用）或 `assets/ecommerce-profile.md`（电商）填一份 JSON。电商场景要三份：

| 文件 | 给谁用 |
|---|---|
| `company-data.json` | `checkup.py`（月度体检） |
| `tax-data.json` | `tax_mode_compare.py`（身份决策） |
| `unit-data.json` | `ecom_unit_econ.py`（单元经济） |

仓库里带了三份示例：`assets/sample-company.json`、`assets/sample-ecommerce-tax.json`、`assets/sample-ecommerce-unit.json`。

### 3. 跑起来

```bash
python scripts/checkup.py assets/sample-company.json            # 月度体检报告
python scripts/tax_mode_compare.py assets/sample-ecommerce-tax.json
python scripts/ecom_unit_econ.py assets/sample-ecommerce-unit.json

# 机器可读输出
python scripts/tax_mode_compare.py data.json --format json --out result.json
```

三个脚本都**无第三方依赖**（Python 3.8+ 标准库），Windows 控制台自动切 UTF-8。

## 目录结构

```
myCFO/
├── SKILL.md                  # Agent 入口：铁律、流程、路由表、CFO 简报模板、合规红线
├── references/               # 专业口径（Agent 按需加载）
│   ├── tax-cn.md             # 中国小微税制 + 2026 征期
│   ├── tax-planning.md       # 合法节税工具箱 + 禁区
│   ├── financial-analysis.md # 三表勾稽、比率、杜邦、诊断树
│   ├── budget-cashflow.md    # 预算、13 周现金流、保本点
│   ├── ecommerce-retail.md   # 电商经营模型
│   ├── ecommerce-accounting.md # CPA 会计处理
│   ├── ecommerce-tax.md      # 无票采购 / 500 万 / 300 万悬崖
│   └── open-source-map.md    # 开源资源地图
├── scripts/
│   ├── checkup.py            # 月度财务体检
│   ├── tax_mode_compare.py   # 小规模 vs 一般纳税人
│   └── ecom_unit_econ.py     # 电商单元经济
├── assets/                   # 档案模板 + 示例数据 + 申报日历
├── research/                 # 6 份 GitHub / 平台 / 政策调研笔记（含核实状态）
└── docs/
    ├── test-evidence.md      # 测试与缺陷修复记录
    └── evidence/             # 基线（无技能）与回归（带技能）原始输出
```

## 一个真实画像的结论示例

客户：拼多多 + 淘宝卖卫衣/内衣，小规模，年 GMV 420 万（含税），退货 25%，档口进货无票。

`tax_mode_compare.py` 输出（含演示假设）：

| | 小规模（现状） | 转一般纳税人 |
|---|---:|---:|
| 增值税 | 3.1 万 | 36.2 万 |
| 附加税费 | 0.2 万 | 2.2 万 |
| 企业所得税 | 10.7 万 | 8.8 万 |
| **净利润** | **82.5 万** | **49.2 万** |
| 综合税负 | 4.3% | **16.8%** |

三个结论：

1. **无票采购时转一般纳税人，年净利少 33 万**；即使 100% 拿到专票仍不如小规模——B2C 客户转嫁不了 13%。
2. **比 500 万更近的是 300 万应纳税所得额悬崖**：无票成本的纳税调增会把应纳税所得额推高，越线后所得税从 5% 直接到 25% 全额。
3. **退货率是服装电商第一大参数**：女装货架 50%–60%、直播 70%–85%；报 25% 要先核对统计口径。

## 设计原则

1. **数字必须有出处**：来自用户数据、脚本计算或 references 公式；没有数据就说"需要先取数"。
2. **合规边界不可越过**：虚开发票、两套账、隐匿收入、公私不分、社保挂靠——明确拒绝并给合法替代。
3. **假设显式化**：用了什么假设、哪些口径没确认，单独列一节。
4. **政策带文号与有效期**：税率/优惠/征期均注明依据与截止日，会变的数字做成参数。
5. **简报要短**：CFO 简报一页，明细放附录。

## 测试与验证

按"先看失败，再写技能"的流程做：

- **基线（不带技能）**：两个独立 Agent 做同一题，都卡在 2026-10 征期（一个给错日期、一个不确定）；另一次基线给出了 300 万悬崖洞察——已吸收进模型。
- **回归（带技能）**：按技能流程实跑，输出七段式 CFO 简报，并抓出脚本 4 个缺陷（附加税减半系数写反、季度销售额静默 ×3、13 周表缺税款科目、投流按 SKU 重复分摊）。

明细见 [docs/test-evidence.md](docs/test-evidence.md)。

## 数据来源与时效

- 增值税与起征点：**财政部 税务总局公告 2026 年第 10 号**（2026-01-01 施行；2023 年第 19 号已停止执行）
- 2026 年度征期：**税总办征科函〔2025〕64 号**
- 小微所得税：财政部 税务总局公告 2023 年第 6 号、第 12 号
- 平台费率/账期/退货率：`research/ecom-platforms.md`（2026-10 核实，含置信度标注）
- GitHub 项目 star/license：`research/*.md`（经 GitHub API 核实，未核实项已标注）

> 上述政策均有有效期（多数至 2027-12-31），使用前请复核最新公告。

## 边界

- 只覆盖小微企业常见税种；不处理差额征税、跨区预缴、出口退税、企业重组。
- 平台费率为公开口径与二手来源混合，落库前请以商家后台"费率中心/账单"为准。
- 本仓库提供经营与税务测算参考，**不构成税务、法律或审计意见**；正式申报以电子税务局与主管税务机关口径为准。

## License

MIT，见 [LICENSE](LICENSE)。
