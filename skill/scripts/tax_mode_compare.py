#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""电商小规模 vs 一般纳税人 税负对比 + 500 万临界点测算（无第三方依赖）。

用法:
    python tax_mode_compare.py assets/sample-ecommerce-tax.json
    python tax_mode_compare.py data.json --format json --out result.json

解决的问题（服装电商最常见的一次性致命决策）:
  档口进货拿不到进项专票时，一旦销售额超过 500 万被强制转一般纳税人，
  销项 13%、进项几乎为 0，增值税会从小规模的 1% 跳到接近 11.5%，
  税负断崖可能吃掉全部利润。本脚本把两种身份、不同进项票比例算清楚。

口径（详见 references/ecommerce-tax.md）:
  - 金额单位: 元；税率用小数（0.01 = 1%）。
  - 销售额: 含税 GMV，先扣退货得到净 GMV。
  - 平台佣金/快递/投流均按净 GMV（含税）比例估算。
  - 采购成本按净 GMV 的比例估算；invoice_ratio = 能取得增值税专用发票的比例。
  - 小规模: 征收率 1%，附加税费减半；一般纳税人: 销项 13%，进项按专票抵扣，
    若同时符合小型微利企业条件，附加税费同样减半（六税两费）。
  - 企业所得税: 小型微利实际税负 5%（应纳税所得额 ≤ 300 万）；
    **无票采购对应的成本不得税前扣除**，本脚本将其加回应纳税所得额。
  - 不考虑留抵退税、跨期、差额征税；仅作经营决策参考。
"""

import argparse
import json
import sys


def fnum(obj, *path, default=0.0):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    try:
        return float(cur)
    except (TypeError, ValueError):
        return default


def money(x):
    return f"{x:,.0f}"


def pct(x):
    return f"{x * 100:.1f}%"


def scenario(data, mode):
    """mode: 'small' 或 'general'。返回该身份下的一年测算。"""
    y = data.get("year", {})
    gmv = fnum(y, "gmv_incl_tax")
    ret = fnum(y, "return_rate")
    net_gmv = gmv * (1 - ret)

    fee_rate = fnum(y, "platform_fee_rate")
    log_rate = fnum(y, "logistics_rate")
    ad_rate = fnum(y, "ad_rate")
    labor_rent = fnum(y, "labor_rent")
    cost_rate = fnum(y, "purchase_cost_rate")
    inv_ratio = min(max(fnum(y, "invoice_ratio"), 0.0), 1.0)
    city = fnum(y, "city_tax_rate", default=0.07)
    # 六税两费减半：符合条件时附加税费系数 0.5，否则 1.0
    surcharge_factor = 0.5 if y.get("surcharge_half", True) else 1.0

    purchase_incl = net_gmv * cost_rate
    fee = net_gmv * fee_rate
    logistics = net_gmv * log_rate
    ad = net_gmv * ad_rate
    extra = net_gmv * fnum(y, "extra_cost_rate", default=0.0)  # 退货损耗/清仓跌价/达人佣金等未建模成本

    if mode == "small":
        vat_rate = fnum(y, "small_scale_rate", default=0.01)
        revenue = net_gmv / (1 + vat_rate)
        cogs = purchase_incl                      # 小规模：进项不可抵扣，价税合计入成本
        vat = revenue * vat_rate
        surcharge = vat * (city + 0.03 + 0.02) * surcharge_factor
        non_deductible = purchase_incl * (1 - inv_ratio)
    else:
        vat_rate = fnum(y, "general_rate", default=0.13)
        revenue = net_gmv / (1 + vat_rate)
        inv_excl = purchase_incl * inv_ratio / (1 + vat_rate)
        cogs = inv_excl + purchase_incl * (1 - inv_ratio)
        output_vat = revenue * vat_rate
        input_vat = inv_excl * vat_rate
        vat = max(output_vat - input_vat, 0.0)
        surcharge = vat * (city + 0.03 + 0.02) * surcharge_factor
        non_deductible = purchase_incl * (1 - inv_ratio)

    expenses = fee + logistics + ad + labor_rent + extra
    accounting_profit = revenue - cogs - expenses - surcharge
    taxable = accounting_profit + non_deductible              # 无票成本纳税调增

    cit_rate = fnum(y, "cit_rate", default=0.05)
    small_cit_cap = fnum(y, "small_cit_cap", default=3000000)
    if taxable <= 0:
        cit = 0.0
        cit_regime = "亏损或为零"
    elif taxable <= small_cit_cap:
        cit = taxable * cit_rate
        cit_regime = f"小型微利 {pct(cit_rate)}"
    else:
        cit = taxable * 0.25
        cit_regime = "超过 300 万，全额 25%"
    net = accounting_profit - cit

    return {
        "mode": "小规模纳税人" if mode == "small" else "一般纳税人",
        "revenue": revenue,
        "net_gmv": net_gmv,
        "cogs": cogs,
        "expenses": expenses,
        "vat": vat,
        "surcharge": surcharge,
        "accounting_profit": accounting_profit,
        "non_deductible": non_deductible,
        "taxable": taxable,
        "cit": cit,
        "cit_regime": cit_regime,
        "net_profit": net,
        "net_margin": net / revenue if revenue else 0.0,
        "tax_total": vat + surcharge + cit,
        "tax_burden": (vat + surcharge + cit) / revenue if revenue else 0.0,
    }


def compare(small, general):
    return {
        "delta_net": general["net_profit"] - small["net_profit"],
        "delta_tax": general["tax_total"] - small["tax_total"],
    }


def sensitivity(data):
    """一般纳税人在不同进项票比例下的净利与税负。"""
    rows = []
    for ratio in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        d = json.loads(json.dumps(data))
        d.setdefault("year", {})["invoice_ratio"] = ratio
        rows.append((ratio, scenario(d, "general")))
    return rows


def growth_table(data):
    """小规模身份下，GMV 增长对 300 万所得税悬崖的影响。"""
    rows = []
    base_gmv = fnum(data.get("year", {}), "gmv_incl_tax")
    for g in (0.0, 0.1, 0.2, 0.3, 0.4):
        d = json.loads(json.dumps(data))
        d.setdefault("year", {})["gmv_incl_tax"] = base_gmv * (1 + g)
        rows.append((g, scenario(d, "small")))
    return rows


def report(data, small, general, diff, sens, growth):
    y = data.get("year", {})
    name = data.get("company", {}).get("name", "未命名公司")
    lines = []
    w = lines.append

    w(f"# 税负对比：{name}")
    w("")
    w(f"- 含税 GMV：{money(fnum(y, 'gmv_incl_tax'))} 元；退货率 {pct(fnum(y, 'return_rate'))}；净 GMV {money(small['net_gmv'])} 元")
    w(f"- 采购成本率 {pct(fnum(y, 'purchase_cost_rate'))}；可取得专票比例 {pct(fnum(y, 'invoice_ratio'))}")
    w(f"- 平台费率 {pct(fnum(y, 'platform_fee_rate'))}；快递/包材 {pct(fnum(y, 'logistics_rate'))}；投流 {pct(fnum(y, 'ad_rate'))}；固定人工房租 {money(fnum(y, 'labor_rent'))} 元/年")
    w("")

    w("## 结论先行")
    if small["net_margin"] > 0.20:
        w(f"> ⚠️ 净利率 {pct(small['net_margin'])} 偏高，通常意味着漏算了成本：退货损耗、清仓跌价、达人佣金、"
          "仓储人工。请检查 `extra_cost_rate`（建议 3%–8%），否则结论会过于乐观。")
        w("")
    if general["net_profit"] < small["net_profit"]:
        w(f"**不要贸然转一般纳税人**：按当前进项票比例，转制后年净利少 {money(-diff['delta_net'])} 元，"
          f"综合税负从 {pct(small['tax_burden'])} 升到 {pct(general['tax_burden'])}。")
        w("")
        w("这不是「税率高」的问题，是**进项票缺失**的问题——先解决采购票据，再谈身份。")
    else:
        w(f"转一般纳税人后净利反而多 {money(diff['delta_net'])} 元，说明进项票充足、且能开 13% 专票给客户。")
    w("")

    w("## 两种身份对比（全年）")
    w("")
    w("| 项目 | 小规模纳税人 | 一般纳税人 | 差额 |")
    w("|---|---:|---:|---:|")
    fields = [
        ("营业收入（不含税）", "revenue"),
        ("营业成本", "cogs"),
        ("平台/物流/投流/人工", "expenses"),
        ("增值税", "vat"),
        ("附加税费", "surcharge"),
        ("会计利润", "accounting_profit"),
        ("其中：无票成本（不得税前扣除）", "non_deductible"),
        ("应纳税所得额", "taxable"),
        ("企业所得税", "cit"),
        ("**净利润**", "net_profit"),
    ]
    for label, key in fields:
        w(f"| {label} | {money(small[key])} | {money(general[key])} | {money(general[key] - small[key])} |")
    w(f"| 净利率 | {pct(small['net_margin'])} | {pct(general['net_margin'])} | {pct(general['net_margin'] - small['net_margin'])} |")
    w(f"| 综合税负率 | {pct(small['tax_burden'])} | {pct(general['tax_burden'])} | — |")
    w("")

    w("## 一般纳税人：进项票比例敏感性")
    w("")
    w("| 可取得专票比例 | 增值税 | 所得税 | 净利润 | 净利率 |")
    w("|---:|---:|---:|---:|---:|")
    for ratio, s in sens:
        w(f"| {pct(ratio)} | {money(s['vat'])} | {money(s['cit'])} | {money(s['net_profit'])} | {pct(s['net_margin'])} |")
    w("")

    # 找与"小规模净利持平"的临界进项票比例
    breakeven = None
    prev = None
    for ratio, s in sens:
        if prev is not None and prev[1]["net_profit"] >= small["net_profit"] >= s["net_profit"]:
            lo, hi = prev[0], ratio
            for _ in range(20):
                mid = (lo + hi) / 2
                d = json.loads(json.dumps(data))
                d.setdefault("year", {})["invoice_ratio"] = mid
                if scenario(d, "general")["net_profit"] >= small["net_profit"]:
                    lo = mid
                else:
                    hi = mid
            breakeven = lo
            break
        prev = (ratio, s)
    if breakeven is not None:
        w(f"> 临界点：可取得专票比例约 **{pct(breakeven)}** 时，两种身份净利持平；低于此线，保持小规模更划算。")
    elif general["net_profit"] >= small["net_profit"]:
        w("> 即使 0% 进项票，一般纳税人净利仍不低于小规模——需复核输入（售价/成本/税率）。")
    else:
        w("> 即使 100% 进项票，一般纳税人净利仍低于小规模——说明该业务不适合一般纳税人（可能售价含税固定、下游不需要专票）。")
    w("")

    w("## 300 万所得税悬崖（往往比 500 万更近）")
    w("")
    w("小型微利企业条件之一是**年应纳税所得额 ≤ 300 万**；超过 1 元即全额按 25% 征税（不是超额累进）。")
    w("无票采购的纳税调增会把应纳税所得额推高，所以这个悬崖比 500 万更早触发。")
    w("")
    w("| 情景 | 含税 GMV | 应纳税所得额 | 所得税 | 税率档 | 净利润 |")
    w("|---|---:|---:|---:|---|---:|")
    for g, s in growth:
        label = "当前" if g == 0 else f"+{pct(g)}"
        w(f"| {label} | {money(fnum(y, 'gmv_incl_tax') * (1 + g))} | {money(s['taxable'])} | "
          f"{money(s['cit'])} | {s['cit_regime']} | {money(s['net_profit'])} |")
    w("")
    base = growth[0][1]
    risky = [s for g, s in growth if s["cit_regime"].startswith("超过")]
    if base["cit_regime"].startswith("超过"):
        w("> ⚠️ 当前已越过 300 万：所得税按 25% 全额计，先解决无票成本调增问题。")
    elif risky:
        step = next(g for g, s in growth if s["cit_regime"].startswith("超过"))
        w(f"> ⚠️ GMV 再增长约 {pct(step)} 就会越过 300 万，所得税从 5% 跳到 25%（全额）。"
          "这比 500 万增值税红线更近，优先处理。")
    else:
        w("> 当前及 40% 增长范围内未越过 300 万；仍需每季度复核。")
    w("")

    w("## 500 万红线")
    net_gmv = small["net_gmv"]
    gmv_gross = fnum(y, "gmv_incl_tax")
    w("")
    w(f"- 增值税口径：应征增值税销售额为**不含税**，当前约 {money(small['revenue'])} 元，"
      f"距 500 万约 {money(max(5000000 - small['revenue'], 0))} 元。")
    w(f"- 更保守的含税口径：平台净成交额 {money(net_gmv)} 元（扣退货后），"
      f"距 500 万约 {money(max(5000000 - net_gmv, 0))} 元——**增长空间更小，按这个做预算更安全**。")
    w(f"- 原始 GMV（未扣退货）{money(gmv_gross)} 元；退货退款的销售额是否被税局按毛额认定，取决于退款凭证与红字发票是否齐全。")
    w(f"- 小规模标准：连续 12 个月应征增值税销售额 ≤ 500 万；超过会被强制登记为一般纳税人。")
    w("- **提前 6–12 个月规划**：要么把进项票解决掉，要么在合规前提下控制规模/调整业务结构；不要等税局通知。")
    w("")

    w("## 行动清单（按优先级）")
    w("")
    w("1. 先算清「能取得专票的采购占比」——这是决定身份的唯一关键变量，不是销售额。")
    w("2. 能开票的供应商优先；档口无票采购尝试自然人代开/税务代开/更换供应商。")
    w("3. 若进项票比例长期低于临界点，保持小规模并控制增速；考虑多主体前先确认业务真实性。")
    w("4. 每年 3 月、9 月各重算一次（政策与进项结构会变）。")
    w("")
    w("---")
    w("本测算为决策参考，不构成税务意见；正式方案需税务师结合当地口径出具。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="电商小规模 vs 一般纳税人税负对比")
    parser.add_argument("data", help="输入 JSON 路径")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--out", help="输出文件路径")
    args = parser.parse_args()

    try:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"读取输入失败: {e}", file=sys.stderr)
        return 2

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    small = scenario(data, "small")
    general = scenario(data, "general")
    diff = compare(small, general)
    sens = sensitivity(data)
    growth = growth_table(data)

    if args.format == "json":
        out = json.dumps(
            {"small": small, "general": general, "diff": diff,
             "sensitivity": [{"invoice_ratio": r, "result": s} for r, s in sens],
             "growth": [{"gmv_growth": g, "result": s} for g, s in growth]},
            ensure_ascii=False, indent=2,
        )
    else:
        out = report(data, small, general, diff, sens, growth)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入 {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
