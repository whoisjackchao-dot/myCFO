# myCFO

> 面向中国大陆小微企业（默认**服装电商零售**：拼多多 / 淘宝天猫 / 抖音）的 **CFO Agent 技能包**，同时是一个**可直接装进 DSH 的插件**。
> 让 AI 以 CFO 视角回答：这个月交多少税、钱够不够、哪个款在亏、要不要转一般纳税人。

不是 SaaS，不是记账软件。它由三部分组成：**技能文件**（Agent 读的流程与专业口径）+ **可执行脚本**（确定性的计算）+ **DSH 插件壳**（一次安装，自动出现在技能目录）。

## 一键部署到 DSH

### 方式 A：从 GitHub 直接装（推荐）

```bash
dsh plugin --profile desktop add github:whoisjackchao-dot/myCFO
```

DSH 会用 pnpm 把本仓库装进 profile，并自动加入 `dsh.profile.bundles`。**重启 DSH** 后生效。

### 方式 B：克隆后运行安装脚本

```powershell
git clone https://github.com/whoisjackchao-dot/myCFO.git
cd myCFO
.\install.ps1              # Windows；默认装到 desktop profile
# 或
bash install.sh            # macOS / Linux
```

卸载：`dsh plugin --profile desktop remove dsh-mycfo`（或 `.\install.ps1 -Uninstall`）。

### 方式 C：不用插件，只当技能用

```bash
git clone https://github.com/whoisjackchao-dot/myCFO.git /tmp/myCFO
cp -r /tmp/myCFO/skill ~/.dsh/skills/company-ops
```

适用于任何支持 `SKILL.md` 的 Agent（Claude Code、OpenCode、Cursor 等），把 `skill/` 目录放进去即可。

### 装好后怎么用

任意会话里自然语言触发：

> 「帮我做一次公司体检」「这个月要交多少税」「赚钱但没钱为什么」「有没有合法的节税办法」「要不要转一般纳税人」「这个款还赚不赚钱」

### 插件是怎么工作的

```
package.json          dsh.bundle.patch → cordis.patch.yml   （声明为 profile 的一层）
cordis.patch.yml      - insert: { id: mycfo-skill, name: dsh-mycfo }
lib/index.js          apply(ctx) → ctx.skills.register({...}) 读自带 skill/SKILL.md
```

- **只读注册**：插件不写用户文件、不改 profile 配置、不联网。
- **资源路径自动解析**：注册时把 `skill/` 设为资源基目录，Agent 看到的是「Base directory for this skill: …」，`references/`、`scripts/`、`assets/` 都能按相对路径找到并执行。
- **失败隔离**：`SKILL.md` 缺失或 frontmatter 不合法时只打印告警，不会影响 profile 启动。
- **不受位置影响**：从 npm、GitHub、本地目录安装都能工作，因为路径取自 `import.meta.url`。

## 能做什么

| 能力 | 入口 | 说明 |
|---|---|---|
| 报税与合规日历 | `skill/references/tax-cn.md` | 2026 年度官方征期（税总办征科函〔2025〕64 号）、各税种税率、优惠、处罚 |
| 税负测算 | `skill/scripts/checkup.py` | 增值税 + 附加税费 + 印花税 + 企业所得税预缴，含红黄绿灯预警 |
| 税务筹划（合法） | `skill/references/tax-planning.md` | T1–T9 工具箱（免征额、500 万临界、小微 5%、年终奖、加计扣除…）+ 7 条禁区 |
| 小规模 vs 一般纳税人 | `skill/scripts/tax_mode_compare.py` | 税负断崖、进项票敏感性、临界比例、**300 万所得税悬崖**、500 万双口径 |
| 电商经营模型 | `skill/references/ecommerce-retail.md` | GMV→收入桥、平台费率与账期、退货准备金、库存与售罄、爆量现金流陷阱 |
| 单元经济 | `skill/scripts/ecom_unit_econ.py` | 单品贡献率、保本 ROAS、保本售价、退货敏感性、SKU ABC/滞销预警 |
| CPA 级会计 | `skill/references/ecommerce-accounting.md` | 总额法/净额法、10 类分录、月末结账 10 步、成本核算、三表编制、三方对账 |
| 电商税务专题 | `skill/references/ecommerce-tax.md` | 无票采购五条合规路径、500 万/300 万双悬崖、达人佣金、刷单、稽查关注点 |
| 财务分析与预算 | `skill/references/financial-analysis.md`、`budget-cashflow.md` | 三表勾稽、40+ 比率、杜邦、诊断树、13 周现金流、保本点 |
| 开源资源地图 | `skill/references/open-source-map.md` | 会计/税务/ERP/对账/BI 可复用项目（star/license 已核实） |

## 直接跑脚本（不经过 Agent）

三个脚本无第三方依赖（Python 3.8+ 标准库），Windows 控制台自动切 UTF-8：

```bash
python skill/scripts/checkup.py skill/assets/sample-company.json
python skill/scripts/tax_mode_compare.py skill/assets/sample-ecommerce-tax.json
python skill/scripts/ecom_unit_econ.py skill/assets/sample-ecommerce-unit.json

# 机器可读输出
python skill/scripts/tax_mode_compare.py skill/assets/sample-ecommerce-tax.json --format json
```

自定义数据：按 `skill/assets/company-profile.md`（通用）或 `skill/assets/ecommerce-profile.md`（电商）填 JSON。电商场景要三份，分别给三个脚本用。

## 目录结构

```
myCFO/
├── package.json          # DSH 插件清单：dsh.bundle / dshWorkshop
├── cordis.patch.yml      # bundle patch：把插件作为一层挂进 profile
├── lib/index.js          # Cordis 插件：注册 company-ops 技能
├── install.ps1 / .sh     # 一键安装脚本
├── test/smoke.mjs        # 冒烟测试（node test/smoke.mjs）
├── skill/                # 技能本体（可单独复制到任意 skills 目录）
│   ├── SKILL.md
│   ├── references/       # 8 篇专业口径
│   ├── scripts/          # 3 个计算脚本
│   └── assets/           # 档案模板、申报日历、示例数据
├── research/             # 6 份 GitHub / 平台 / 政策调研笔记（含核实状态）
└── docs/                 # 测试与缺陷修复记录 + 基线/回归原始输出
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

- 插件冒烟测试：`node test/smoke.mjs`（校验注册出的 skill 定义、17 个资源文件、包清单）
- 技能行为回归：RED（不带技能）→ GREEN（带技能），差异与 9 个已修复缺陷见 [docs/test-evidence.md](docs/test-evidence.md)
- 脚本回归：三个示例数据均 0 退出码

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
