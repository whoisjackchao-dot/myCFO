#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""company-ops 月度财务体检脚本（无第三方依赖）。

用法:
    python checkup.py assets/sample-company.json
    python checkup.py data.json --format json
    python checkup.py data.json --out report.md

输入: 一个 JSON 文件（结构见 assets/company-profile.md 与 assets/sample-company.json）。
输出: Markdown 体检报告或 JSON 结果，包含
  1) 税负测算（增值税 + 附加税费 + 印花税 + 企业所得税预缴）
  2) 报表指标（毛利率/净利率/流动比率/现金安全月数/保本收入等）
  3) 红黄绿灯预警
  4) 13 周现金流预测（若提供 cashflow 段）

设计原则:
  - 只做算术，不替代判断：口径不清时给出警告，不猜。
  - 金额单位: 元；税率用小数（0.01 = 1%）。
  - 缺字段不报错，记为缺失并在报告末尾列出补齐清单。
"""

import argparse
import json
import sys

MISSING = []


def fnum(obj, *path, default=0.0):
    """按路径取数值；缺失记入 MISSING 并返回 default。"""
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            MISSING.append(".".join(path))
            return default
        cur = cur[key]
    if cur is None:
        MISSING.append(".".join(path))
        return default
    try:
        return float(cur)
    except (TypeError, ValueError):
        MISSING.append(".".join(path))
        return default


def money(x):
    return f"{x:,.2f}"


def pct(x):
    return f"{x * 100:.1f}%"


def safe_div(a, b, default=0.0):
    return a / b if b else default


# --------------------------------------------------------------------------- #
# 税负测算
# --------------------------------------------------------------------------- #

def compute_tax(data):
    """返回 (税负明细, 警告列表)。简化口径见 references/tax-cn.md。"""
    warnings = []
    company = data.get("company", {})
    period = data.get("period", {})
    pl = data.get("pl", {})

    taxpayer = company.get("taxpayer", "small_scale")
    vat_rate = fnum(company, "vat_rate", default=0.01)
    city_rate = fnum(company, "city_tax_rate", default=0.07)
    month_rev = fnum(pl, "revenue_excl_tax")
    if "quarter_sales_excl_tax" in period:
        quarter_sales = fnum(period, "quarter_sales_excl_tax")
    else:
        quarter_sales = month_rev * 3
        warnings.append(
            "未提供 quarter_sales_excl_tax（季度累计不含税销售额），已按当月收入 × 3 粗估；"
            "请用实际季度累计数核对，否则免征额判断会错。"
        )

    tax = {}

    # 增值税
    if taxpayer == "small_scale":
        if quarter_sales <= 0:
            tax["vat"] = 0.0
            warnings.append("季度销售额为 0 或缺失，增值税按 0 计，请核对输入。")
        elif quarter_sales <= 300000:
            tax["vat"] = 0.0
            tax["vat_note"] = "季度销售额 ≤ 30 万，享受小规模纳税人免征增值税（月 10 万 / 季 30 万以下）"
        else:
            tax["vat"] = quarter_sales * vat_rate
            tax["vat_note"] = f"季度销售额 {money(quarter_sales)} > 30 万，按减按 {pct(vat_rate)} 征收率全额计税"
        if "special_invoice_sales" in period:
            warnings.append("存在增值税专用发票销售额时，专票部分不能免税，需按专票金额单独计算。")
    else:
        tax["vat"] = month_rev * fnum(company, "general_vat_rate", default=0.06)
        tax["vat_note"] = "一般纳税人：仅按销项税率粗算，未抵扣进项税，实际以申报表为准。"
        warnings.append("一般纳税人未计算进项税抵扣，结果仅为销项税上限估计。")

    # 附加税费
    surcharge_rate = city_rate + 0.03 + 0.02  # 城建税 + 教育费附加 + 地方教育附加
    half = 0.5 if taxpayer == "small_scale" else 1.0
    tax["surcharge"] = tax["vat"] * surcharge_rate * half
    tax["surcharge_note"] = (
        f"= 增值税 × ({pct(city_rate)}+3%+2%) × {'50%（六税两费减半）' if half == 0.5 else '100%'}"
    )

    # 印花税（按应税合同估算；B2C 零售通常不缴买卖合同印花税，可传 0）
    stamp_rate = fnum(company, "stamp_duty_rate", default=0.0003) * half
    tax["stamp_duty"] = month_rev * stamp_rate
    tax["stamp_duty_note"] = (
        "按合同金额估算（买卖/承揽/技术合同同档，默认万分之三）" + ("（六税两费减半）" if half == 0.5 else "") + "，需按实际应税凭证核对"
        if stamp_rate > 0 else "已按配置置零（B2C 零售通常不缴买卖合同印花税）"
    )

    # 企业所得税（季度预缴；小型微利企业实际税负 5%）
    profit = (
        fnum(pl, "revenue_excl_tax")
        - fnum(pl, "cost_of_sales")
        - fnum(pl, "operating_expenses")
        - fnum(pl, "payroll")
        - fnum(pl, "social_insurance")
        - fnum(pl, "depreciation")
        - fnum(pl, "interest_expense")
        - fnum(pl, "other_expenses")
    )
    tax["estimated_profit"] = profit
    annual_cap = fnum(company, "annual_taxable_income_cap", default=3000000)
    if profit <= 0:
        tax["cit"] = 0.0
        tax["cit_note"] = "当期利润 ≤ 0，企业所得税为 0；亏损可结转以后年度弥补（一般 5 年）。"
    elif profit * 4 <= annual_cap:
        tax["cit"] = profit * 0.25 * 0.20
        tax["cit_note"] = (
            "按当期利润 × 5% 估算（小型微利：应纳税所得额减按 25% 计入、20% 税率）；"
            "季度预缴须用季度累计利润重算，不要用单月利润 ×3 直接申报。"
        )
    else:
        tax["cit"] = profit * 0.25
        tax["cit_note"] = "超出小型微利企业标准，按 25% 法定税率粗算，需按汇算口径调整。"

    total = tax["vat"] + tax["surcharge"] + tax["stamp_duty"] + tax["cit"]
    tax["total_tax"] = total
    tax["tax_burden"] = safe_div(total, month_rev)
    tax["profit_after_tax"] = profit - total

    if "employees" in company:
        warnings.append("未计算工资薪金个人所得税与社保公积金单位部分；需按实际工资表补算。")
    return tax, warnings


# --------------------------------------------------------------------------- #
# 指标分析
# --------------------------------------------------------------------------- #

def compute_ratios(data, tax):
    pl = data.get("pl", {})
    bs = data.get("balance", {})
    warnings = []

    rev = fnum(pl, "revenue_excl_tax")
    cogs = fnum(pl, "cost_of_sales")
    opex = fnum(pl, "operating_expenses")
    payroll = fnum(pl, "payroll")
    social = fnum(pl, "social_insurance")
    depreciation = fnum(pl, "depreciation")
    interest = fnum(pl, "interest_expense")

    gross_profit = rev - cogs
    operating_profit = gross_profit - opex - payroll - social - depreciation
    net_profit = tax.get("profit_after_tax", operating_profit)
    fixed_costs = opex + payroll + social + depreciation + interest

    cash = fnum(bs, "cash")
    ar = fnum(bs, "accounts_receivable")
    inventory = fnum(bs, "inventory")
    prepaid = fnum(bs, "prepaid")
    fixed_assets = fnum(bs, "fixed_assets")
    other_assets = fnum(bs, "other_assets")

    ap = fnum(bs, "accounts_payable")
    accrued = fnum(bs, "accrued_payroll")
    short_loans = fnum(bs, "short_term_loans")
    other_liab = fnum(bs, "other_liabilities")

    current_assets = cash + ar + inventory + prepaid
    total_assets = current_assets + fixed_assets + other_assets
    current_liab = ap + accrued + short_loans + other_liab
    total_liab = current_liab
    equity = total_assets - total_liab

    monthly_cash_out = cogs + opex + payroll + social
    gross_margin = safe_div(gross_profit, rev)
    runway = safe_div(cash, monthly_cash_out) if monthly_cash_out > 0 else 99.0
    if monthly_cash_out <= 0:
        warnings.append("缺少成本/费用/人工数据，现金安全月数不可靠（按 99 个月兜底），请补齐。")

    r = {
        "revenue": rev,
        "gross_profit": gross_profit,
        "operating_profit": operating_profit,
        "net_profit": net_profit,
        "fixed_costs": fixed_costs,
        "gross_margin": gross_margin,
        "net_margin": safe_div(net_profit, rev),
        "opex_ratio": safe_div(opex + payroll + social, rev),
        "cash": cash,
        "current_assets": current_assets,
        "current_liab": current_liab,
        "total_assets": total_assets,
        "total_liab": total_liab,
        "equity": equity,
        "current_ratio": safe_div(current_assets, current_liab),
        "quick_ratio": safe_div(current_assets - inventory, current_liab),
        "cash_ratio": safe_div(cash, current_liab),
        "debt_ratio": safe_div(total_liab, total_assets),
        "runway_months": runway,
        "breakeven_rev": safe_div(fixed_costs, gross_margin) if gross_margin > 0 else 0.0,
        "ar_days": safe_div(ar, rev / 30.0),
        "monthly_cash_out": monthly_cash_out,
    }

    if gross_margin <= 0:
        warnings.append("毛利率 ≤ 0：收入覆盖不了直接成本，先查报价、采购价与亏本订单。")
    if current_liab > 0 and r["current_ratio"] < 1:
        warnings.append("流动比率 < 1：短期负债超过可变现流动资产，存在周转断裂风险。")
    if rev and gross_margin > 0 and rev < r["breakeven_rev"]:
        warnings.append("当期收入低于保本收入，经营处于亏损区间。")
    return r, warnings


def build_alerts(data, tax, r):
    """红黄绿灯，返回 [(级别, 项目, 说明)]，级别: red / yellow / green。"""
    alerts = []

    def add(level, item, msg):
        alerts.append((level, item, msg))

    if r["cash"] <= 0:
        add("red", "现金", "账面现金 ≤ 0：立即停止非必要支出并安排回款/融资。")
    elif r["monthly_cash_out"] <= 0:
        add("yellow", "数据完整性", "缺少成本/费用/人工数据，现金安全月数不可用；先补齐再判断现金是否安全。")
    elif r["runway_months"] < 1:
        add("red", "现金安全月数", f"现金仅够 {r['runway_months']:.1f} 个月支出（<1），需立刻处理回款与付款节奏。")
    elif r["runway_months"] < 3:
        add("yellow", "现金安全月数", f"现金安全月数 {r['runway_months']:.1f} 个月，低于 3 个月安全线。")
    else:
        add("green", "现金安全月数", f"现金安全月数 {r['runway_months']:.1f} 个月，安全。")

    if tax["total_tax"] > max(r["cash"], 0) * 0.5 and tax["total_tax"] > 0:
        add("red", "税负", "本期应纳税额超过账上现金的一半，需提前确认缴税资金。")
    elif tax["total_tax"] > 0:
        add("yellow", "税负", f"本期预计应纳税额 {money(tax['total_tax'])} 元，记得在征期内预留资金。")

    if r["net_margin"] < 0:
        add("red", "净利润", "当期净亏损：拆解是收入不足、毛利太低还是固定费用过高。")
    elif r["net_margin"] < 0.05 and r["revenue"] > 0:
        add("yellow", "净利润", f"净利率 {pct(r['net_margin'])}，低于 5%，抗风险能力弱。")
    else:
        add("green", "净利润", f"净利率 {pct(r['net_margin'])}。")

    if r["ar_days"] > 60:
        add("yellow", "应收周转", f"应收周转约 {r['ar_days']:.0f} 天，超过 60 天，回款偏慢。")
    if r["current_liab"] > 0 and r["quick_ratio"] < 0.8:
        add("yellow", "速动比率", f"速动比率 {r['quick_ratio']:.2f}，短期偿债依赖存货/回款。")
    if r["debt_ratio"] > 0.7:
        add("yellow", "资产负债率", f"资产负债率 {pct(r['debt_ratio'])}，高于 70%。")
    if r["revenue"] > 0 and tax["tax_burden"] > 0.15:
        add("yellow", "综合税负率", f"综合税负率 {pct(tax['tax_burden'])}，偏高，复核税种口径与优惠享受情况。")

    return alerts


# --------------------------------------------------------------------------- #
# 13 周现金流
# --------------------------------------------------------------------------- #

def project_cashflow(data, r, tax=None):
    cf = data.get("cashflow")
    if not cf:
        return None, []
    warnings = []
    opening = r["cash"]
    weekly_fixed = fnum(cf, "weekly_fixed_costs", default=safe_div(r["monthly_cash_out"], 4.33))
    buffer = fnum(cf, "safety_buffer", default=0.0)

    inflow = [0.0] * 13
    outflow = [0.0] * 13
    payables = list(cf.get("payables") or [])
    tax_payments = cf.get("tax_payments") or []
    payables.extend(tax_payments)
    if tax and tax.get("total_tax", 0) > 0 and not tax_payments:
        warnings.append(
            f"13 周现金流未包含税款（本期约 {money(tax['total_tax'])} 元）；"
            "请在 cashflow.tax_payments 中按实际缴纳周次补充，否则现金低点会被低估。"
        )
    for bucket, items in ((inflow, cf.get("receivables") or []), (outflow, payables)):
        for item in items:
            try:
                w = int(item.get("due_week", 1))
                if 1 <= w <= 13:
                    bucket[w - 1] += float(item.get("amount", 0))
                else:
                    warnings.append(f"{item.get('name', '?')} 的 due_week 超出 1-13，已忽略。")
            except (TypeError, ValueError, AttributeError):
                warnings.append(f"{item} 格式错误，已忽略。")

    rows = []
    cash = opening
    for i in range(13):
        cash += inflow[i] - outflow[i] - weekly_fixed
        rows.append({"week": i + 1, "cash_in": inflow[i], "cash_out": outflow[i] + weekly_fixed, "closing": cash})

    alerts = []
    for row in rows:
        if row["closing"] < 0:
            alerts.append(("red", f"第{row['week']}周", f"现金流出缺口，期末现金 {money(row['closing'])}"))
            break
    if not alerts and buffer:
        for row in rows:
            if row["closing"] < buffer:
                alerts.append(("yellow", f"第{row['week']}周", f"期末现金低于安全垫 {money(buffer)}"))
                break
    return {"opening": opening, "rows": rows, "weekly_fixed": weekly_fixed, "buffer": buffer}, alerts


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #

def build_report(data, tax, ratios, alerts, cf, cf_alerts, warnings):
    company = data.get("company", {})
    period = data.get("period", {})
    icon = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
    cn = ["零", "一", "二", "三", "四", "五", "六"]
    taxpayer_label = {
        "small_scale": "小规模纳税人",
        "general": "一般纳税人",
    }.get(company.get("taxpayer", "small_scale"), company.get("taxpayer", ""))
    lines = []
    w = lines.append

    w(f"# 财务体检报告：{company.get('name', '未命名公司')}")
    w("")
    w(f"- 期间：{period.get('month', '未填写')}（{period.get('quarter', '未填写')}）")
    w(f"- 纳税人类型：{taxpayer_label}；行业：{company.get('industry', '未填写')}")
    w("")

    red = [a for a in alerts if a[0] == "red"]
    yellow = [a for a in alerts if a[0] == "yellow"]
    w("## 一句话结论")
    if red:
        w(f"**红灯 {len(red)} 项**，最紧急：{red[0][2]}")
    elif yellow:
        w(f"整体可控，**黄灯 {len(yellow)} 项**，优先处理：{yellow[0][2]}")
    else:
        w("各项指标正常，按计划经营即可；重点仍是按期申报与回款跟踪。")
    w("")

    w("## 一、本期税负测算")
    w("")
    w("| 税种 | 金额（元） | 口径说明 |")
    w("|---|---:|---|")
    w(f"| 增值税 | {money(tax['vat'])} | {tax.get('vat_note', '')} |")
    w(f"| 附加税费 | {money(tax['surcharge'])} | {tax.get('surcharge_note', '')} |")
    w(f"| 印花税 | {money(tax['stamp_duty'])} | {tax.get('stamp_duty_note', '')} |")
    w(f"| 企业所得税（季度预缴） | {money(tax['cit'])} | {tax.get('cit_note', '')} |")
    w(f"| **合计** | **{money(tax['total_tax'])}** | 综合税负率 {pct(tax['tax_burden'])} |")
    w("")
    w(f"- 估算税前利润：{money(tax['estimated_profit'])} 元；扣税后利润：{money(tax['profit_after_tax'])} 元")
    w("")

    w("## 二、经营指标")
    w("")
    w("| 指标 | 数值 | 参考线 |")
    w("|---|---:|---|")
    w(f"| 收入（不含税） | {money(ratios['revenue'])} | — |")
    w(f"| 毛利 / 毛利率 | {money(ratios['gross_profit'])} / {pct(ratios['gross_margin'])} | 服务 ≥50%，贸易 ≥20% |")
    w(f"| 净利润 / 净利率 | {money(ratios['net_profit'])} / {pct(ratios['net_margin'])} | ≥5% 为健康 |")
    w(f"| 费用率（含人工） | {pct(ratios['opex_ratio'])} | 与上月、去年同期比 |")
    w(f"| 保本收入 | {money(ratios['breakeven_rev'])} | 当期收入需高于此线 |")
    if ratios["monthly_cash_out"] > 0:
        runway_display = f"{ratios['runway_months']:.1f} 月"
    else:
        runway_display = "—（缺成本/费用数据）"
    w(f"| 现金 / 现金安全月数 | {money(ratios['cash'])} / {runway_display} | ≥3 个月 |")
    w(f"| 流动比率 | {ratios['current_ratio']:.2f} | ≥1.5 |")
    w(f"| 速动比率 | {ratios['quick_ratio']:.2f} | ≥1.0 |")
    w(f"| 资产负债率 | {pct(ratios['debt_ratio'])} | ≤70% |")
    w(f"| 应收周转天数 | {ratios['ar_days']:.0f} 天 | ≤60 天 |")
    w("")

    w("## 三、预警")
    w("")
    w("| 级别 | 项目 | 说明 |")
    w("|---|---|---|")
    for level, item, msg in alerts:
        w(f"| {icon.get(level, level)} | {item} | {msg} |")
    w("")

    if cf:
        sec = 4
        w(f"## {cn[sec]}、13 周现金流预测")
        w("")
        w(f"期初现金 {money(cf['opening'])} 元；每周固定支出 {money(cf['weekly_fixed'])} 元；安全垫 {money(cf['buffer'])} 元。")
        w("")
        w("> 口径说明：上方「现金安全月数」按全部经营支出（成本+费用+人工）计算；本表按实际付款周次排布，两者口径不同，不要直接对比。")
        w("")
        w("| 周次 | 流入 | 流出 | 期末现金 |")
        w("|---|---:|---:|---:|")
        for row in cf["rows"]:
            w(f"| 第{row['week']}周 | {money(row['cash_in'])} | {money(row['cash_out'])} | {money(row['closing'])} |")
        w("")
        if cf_alerts:
            for level, item, msg in cf_alerts:
                w(f"- {icon.get(level, level)} {item}：{msg}")
        else:
            w("- 13 周内现金均可覆盖支出。")
        w("")

    if warnings:
        sec = 5 if cf else 4
        w(f"## {cn[sec]}、口径提醒与待确认")
        w("")
        seen = set()
        for msg in warnings:
            if msg in seen:
                continue
            seen.add(msg)
            w(f"- {msg}")
        missing = sorted({m for m in MISSING if m})
        if missing:
            w(f"- 输入中缺失/非数字字段：{', '.join(missing)}（按 0 处理，补齐后重跑）")
        w("")

    w("---")
    w("本报告由 checkup.py 按 references/tax-cn.md 的简化口径计算，仅供经营参考；")
    w("正式申报以电子税务局申报表与主管税务机关口径为准。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="company-ops 月度财务体检")
    parser.add_argument("data", help="输入 JSON 文件路径")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="输出格式（默认 md）")
    parser.add_argument("--out", help="输出文件路径（默认打印到 stdout）")
    args = parser.parse_args()

    # Windows 控制台默认 GBK，报告含 emoji/中文，强制 UTF-8 输出
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    try:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"读取输入失败: {e}", file=sys.stderr)
        return 2

    tax, tax_warnings = compute_tax(data)
    ratios, ratio_warnings = compute_ratios(data, tax)
    alerts = build_alerts(data, tax, ratios)
    cf, cf_alerts = project_cashflow(data, ratios, tax)
    warnings = tax_warnings + ratio_warnings

    if args.format == "json":
        result = {
            "company": data.get("company", {}),
            "period": data.get("period", {}),
            "tax": tax,
            "ratios": ratios,
            "alerts": [{"level": l, "item": i, "message": m} for l, i, m in alerts],
            "cashflow": cf,
            "cashflow_alerts": [{"level": l, "item": i, "message": m} for l, i, m in cf_alerts],
            "warnings": warnings,
            "missing_fields": sorted({m for m in MISSING if m}),
        }
        out = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        out = build_report(data, tax, ratios, alerts, cf, cf_alerts, warnings)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入 {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
