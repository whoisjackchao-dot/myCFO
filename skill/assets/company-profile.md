# 公司档案模板

首次为一家公司服务时，把下面的信息问全，落到工作目录 `company-profile.md` + `company-data.json`（后者给 `scripts/checkup.py` 用）。

## 一、基本信息（问老板，5 分钟）

| 字段 | 示例 | 为什么重要 |
|---|---|---|
| 公司名称 | 杭州某某设计有限公司 | 报告抬头 |
| 成立时间 | 2021-06 | 判断优惠资格、亏损弥补年限 |
| 纳税人身份 | 小规模纳税人 / 一般纳税人 | 决定增值税算法 |
| 申报周期 | 按季 / 按月 | 决定申报日历 |
| 征收方式 | 查账征收 / 核定征收 | 决定企业所得税/个税算法 |
| 行业 | 设计服务 / 贸易 / 制造 | 决定毛利率参考线 |
| 员工人数 | 3 | 判断小微、残保金、社保 |
| 社保基数 | 最低基数 / 实际工资 | 用工合规风险 |
| 注册地/经营地 | 杭州市西湖区 | 城建税税率（7%/5%/1%）、地方优惠 |
| 开户行/基本户 | 工行 xx 支行 | 资金流核对 |
| 是否有研发活动 | 有 / 无 | 研发加计扣除 |
| 上年度应纳税所得额 | 86 万 | 判断小微资格 |

## 二、月度数据 JSON 结构

```json
{
  "company": {
    "name": "公司名称",
    "taxpayer": "small_scale",
    "vat_rate": 0.01,
    "city_tax_rate": 0.07,
    "employees": 3,
    "industry": "设计服务"
  },
  "period": {
    "month": "2026-09",
    "quarter": "2026Q3",
    "quarter_sales_excl_tax": 820000
  },
  "pl": {
    "revenue_excl_tax": 277227.72,
    "cost_of_sales": 120000,
    "operating_expenses": 30000,
    "payroll": 45000,
    "social_insurance": 6000,
    "depreciation": 2000,
    "interest_expense": 0,
    "other_expenses": 0
  },
  "balance": {
    "cash": 50000,
    "accounts_receivable": 80000,
    "inventory": 0,
    "prepaid": 0,
    "fixed_assets": 20000,
    "other_assets": 0,
    "accounts_payable": 40000,
    "accrued_payroll": 15000,
    "short_term_loans": 0,
    "other_liabilities": 0
  },
  "cashflow": {
    "weekly_fixed_costs": 14000,
    "safety_buffer": 30000,
    "receivables": [{"name": "A 客户尾款", "amount": 30000, "due_week": 2}],
    "payables": [{"name": "办公室房租", "amount": 15000, "due_week": 1}],
    "tax_payments": [{"name": "Q3 增值税及附加", "amount": 8692, "due_week": 1}]
  }
}
```

字段规则：
- 金额单位**元**，税率用小数（0.01 = 1%）。
- `revenue_excl_tax` 是不含税收入；只有含税数时除以 (1+征收率)。
- `quarter_sales_excl_tax` 是本季度累计不含税销售额，用来判断 30 万免征。**没填时脚本会按当月收入×3 粗估并警告**，季度申报前必须换成实际累计数。
- 缺失字段留空即可，脚本会列出来让你补。
- `cashflow` 段可选；给了才会输出 13 周预测。
- `tax_payments` 把税款按缴纳周次排进现金流；不填时脚本会警告"现金低点被低估"。

## 三、取数清单（缺数据时按这个要）

| 数据 | 来源 | 用途 |
|---|---|---|
| 收入（含税/不含税、已开票/未开票） | 开票系统 + 银行流水 | 增值税 |
| 成本发票 | 发票勾选平台 | 增值税进项、企业所得税 |
| 工资表 + 社保明细 | 工资表、社保缴费记录 | 个税、社保、费用 |
| 银行流水（对公 + 老板个人卡） | 网银导出 | 公私不分核查 |
| 应收/应付明细（按客户/供应商、账龄） | 台账或 ERP | 营运资金诊断 |
| 存货明细 | 进销存 | 存货周转、成本 |
| 固定资产清单 | 台账 | 折旧、一次性扣除 |
| 已申报记录 | 电子税务局 | 申报连续性、欠税 |
