#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""电商单品/店铺单元经济测算（无第三方依赖）。

用法:
    python ecom_unit_econ.py assets/sample-ecommerce-unit.json
    python ecom_unit_econ.py data.json --format json

解决什么问题:
  电商老板最常见的错觉是"售价-进货价=赚的"。真实链条上还有：退货、平台佣金、
  支付手续费、快递、包材、达人佣金、投流。本脚本把每卖一件真正赚多少算清楚，
  并给出保本 ROAS、保本售价、退货率敏感性，以及多 SKU 的 ABC/滞销分析。

输入 JSON 结构（金额单位: 元，比例用小数）:
{
  "company": {"name": "...", "category": "卫衣"},
  "assumptions": {
    "platform_fee_rate": 0.006,      // 平台佣金/支付手续费（按成交额）
    "logistics_per_order": 4.5,      // 快递单均
    "packaging_per_order": 1.5,      // 包材单均
    "return_shipping_per_return": 6, // 退货回程运费/损耗（每次退货）
    "influencer_rate": 0.0,          // 达人佣金率（按成交额）
    "ad_spend": 0,                   // 投流金额（用于整体 ROAS 测算）
    "tax_rate": 0.01                 // 小规模 1%（仅用于不含税换算）
  },
  "skus": [
    {"name": "加绒卫衣 A", "price_incl_tax": 129, "cost_incl_tax": 45,
     "return_rate": 0.25, "monthly_orders": 1200, "stock": 800, "sales_last_30d": 1200}
  ]
}

输出:
  1) 单品经济: 净收入、变动成本、边际贡献、净利、净利率、保本 ROAS、保本售价
  2) 退货率敏感性（对净利率的冲击）
  3) 多 SKU 汇总: 总销售额、总贡献、贡献占比 ABC、售罄率/动销预警
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
    return f"{x:,.2f}"


def pct(x):
    return f"{x * 100:.1f}%"


def unit_econ(sku, a, ad_per_order=None):
    """返回单件口径的经济模型。price/cost 为含税价。"""
    price = fnum(sku, "price_incl_tax")
    cost = fnum(sku, "cost_incl_tax")
    ret = min(max(fnum(sku, "return_rate"), 0.0), 0.95)
    tax_rate = fnum(a, "tax_rate", default=0.01)

    fee_rate = fnum(a, "platform_fee_rate")
    inf_rate = fnum(a, "influencer_rate")
    ship = fnum(a, "logistics_per_order")
    pack = fnum(a, "packaging_per_order")
    ret_ship = fnum(a, "return_shipping_per_return")

    # 每卖 1 单（成交口径）对应的期望回款：退货部分退回，但退货物流/损耗发生
    net_rev = price / (1 + tax_rate) * (1 - ret)                       # 不含税净收入
    cost_total = cost * (1 - ret)                                       # 退货可二次销售，成本按留存单计
    fees = price * (1 - ret) * (fee_rate + inf_rate)                     # 平台/达人按成交额
    logistics = (ship + pack) * (1 - ret) + ret_ship * ret              # 正向物流 + 退货物流
    variable = cost_total + fees + logistics
    contribution = net_rev - variable                                    # 边际贡献
    margin = contribution / net_rev if net_rev else 0.0

    # 保本 ROAS：投流每花 1 元需带来多少收入才不亏（按不含税净收入口径）
    breakeven_roas = 1 / margin if margin > 0 else float("inf")
    # 保本售价：投流=0、其他条件不变时，售价降到多少边际贡献为 0（迭代）
    lo, hi = 0.0, max(price, 1.0)
    for _ in range(60):
        mid = (lo + hi) / 2
        net = mid / (1 + tax_rate) * (1 - ret)
        var = cost * (1 - ret) + mid * (1 - ret) * (fee_rate + inf_rate) + (ship + pack) * (1 - ret) + ret_ship * ret
        if net - var > 0:
            hi = mid
        else:
            lo = mid
    breakeven_price = hi

    # 单件净利（投流按分摊到每单的获客成本扣）
    orders = fnum(sku, "monthly_orders", default=1.0)
    if ad_per_order is None:
        ad = fnum(a, "ad_spend")
        ad_per_order = ad / orders if orders else 0.0
    net_profit = contribution - ad_per_order
    net_margin = net_profit / net_rev if net_rev else 0.0

    return {
        "name": sku.get("name", "未命名 SKU"),
        "price_incl_tax": price,
        "cost_incl_tax": cost,
        "return_rate": ret,
        "net_revenue": net_rev,
        "variable_cost": variable,
        "contribution": contribution,
        "contribution_margin": margin,
        "breakeven_roas": breakeven_roas,
        "breakeven_price": breakeven_price,
        "ad_per_order": ad_per_order,
        "net_profit": net_profit,
        "net_margin": net_margin,
        "monthly_orders": orders,
        "monthly_contribution": contribution * orders,
        "monthly_net_profit": net_profit * orders,
        "monthly_revenue": net_rev * orders,
    }


def sensitivity(sku, a, ad_per_order=None):
    """退货率 ±10 个点对贡献与净利率的影响。"""
    base = fnum(sku, "return_rate")
    rows = []
    for delta in (-0.10, -0.05, 0.0, 0.05, 0.10):
        r = min(max(base + delta, 0.0), 0.95)
        s = json.loads(json.dumps(sku))
        s["return_rate"] = r
        rows.append((r, unit_econ(s, a, ad_per_order)))
    return rows


def build_report(data, results, sens_rows, agg):
    lines = []
    w = lines.append
    company = data.get("company", {})
    a = data.get("assumptions", {})

    w(f"# 电商单元经济：{company.get('name', '未命名店铺')}")
    w("")
    w(f"- 品类：{company.get('category', '未填写')}；平台扣点 {pct(fnum(a, 'platform_fee_rate'))}；"
      f"快递 {money(fnum(a, 'logistics_per_order'))} 元/单；包材 {money(fnum(a, 'packaging_per_order'))} 元/单")
    w("")

    w("## 单品经济（每卖 1 单）")
    w("")
    w("| SKU | 含税售价 | 含税成本 | 退货率 | 不含税净收入 | 变动成本 | 边际贡献 | 贡献率 | 净利 | 净利率 |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        w(f"| {r['name']} | {money(r['price_incl_tax'])} | {money(r['cost_incl_tax'])} | {pct(r['return_rate'])} | "
          f"{money(r['net_revenue'])} | {money(r['variable_cost'])} | {money(r['contribution'])} | "
          f"{pct(r['contribution_margin'])} | {money(r['net_profit'])} | {pct(r['net_margin'])} |")
    w("")

    w("## 保本线（亏损预警）")
    w("")
    w("| SKU | 保本 ROAS | 保本售价（投流=0） | 当前售价 | 安全垫 |")
    w("|---|---:|---:|---:|---:|")
    for r in results:
        roas = "—" if r["breakeven_roas"] == float("inf") else f"{r['breakeven_roas']:.2f}"
        cushion = (r["price_incl_tax"] - r["breakeven_price"]) / r["price_incl_tax"] if r["price_incl_tax"] else 0
        w(f"| {r['name']} | {roas} | {money(r['breakeven_price'])} | {money(r['price_incl_tax'])} | {pct(cushion)} |")
    w("")
    w("> 解读：保本 ROAS = 1 / 贡献率。实际 ROAS 低于此值，投流越多亏越多；")
    w("> 安全垫 = （售价 − 保本售价）/ 售价，低于 10% 说明没有降价空间。")
    w("")

    w("## 退货率敏感性（以第一个 SKU 为例）")
    w("")
    w("| 退货率 | 边际贡献 | 贡献率 | 单件净利 | 净利率 |")
    w("|---:|---:|---:|---:|---:|")
    for r, s in sens_rows:
        w(f"| {pct(r)} | {money(s['contribution'])} | {pct(s['contribution_margin'])} | {money(s['net_profit'])} | {pct(s['net_margin'])} |")
    w("")
    if len(sens_rows) >= 2:
        drop = sens_rows[0][1]["contribution_margin"] - sens_rows[-1][1]["contribution_margin"]
        w(f"> 退货率每 +10 个点，贡献率下降约 {abs(drop) * 100 / 2:.1f} 个百分点——退货率是服装电商第一杀手。")
        w("")

    w("## 店铺汇总（按当前月订单量）")
    w("")
    w(f"- 月销售额（不含税）：{money(agg['monthly_revenue'])} 元")
    w(f"- 月边际贡献：{money(agg['monthly_contribution'])} 元（贡献率 {pct(agg['contribution_margin'])}）")
    w(f"- 月净利（扣投流）：{money(agg['monthly_net_profit'])} 元（净利率 {pct(agg['net_margin'])}）")
    w(f"- 投流合计：{money(fnum(a, 'ad_spend'))} 元；实际 ROAS（净收入/投流）："
      f"{agg['actual_roas']:.2f}" if agg["ad_spend"] else "- 未填投流金额，无法算实际 ROAS")
    w("")

    w("## SKU 结构（ABC / 动销）")
    w("")
    w("| SKU | 月销售额 | 销售占比 | ABC | 库存 | 售罄率(近30天) | 预警 |")
    w("|---|---:|---:|---|---:|---:|---|")
    for row in agg["sku_rows"]:
        w(f"| {row['name']} | {money(row['monthly_revenue'])} | {pct(row['sales_share'])} | {row['abc']} | "
          f"{row['stock']:.0f} | {pct(row['sell_through'])} | {row['warning']} |")
    w("")
    w("> ABC 按销售额累计 70%/90% 划分；售罄率 = 近 30 天销量 / (销量+库存)。")
    w("> 预警规则：A 类断货风险 / 售罄率 <20% 的 C 类滞销 / 库存 > 3 个月销量的压货。")
    w("")

    w("---")
    w("金额为含税口径的近似测算，未考虑优惠券、平台补贴、退货运费险、仓储与人工；")
    w("决策前用真实后台数据替换假设值。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="电商单元经济测算")
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

    a = data.get("assumptions", {})
    skus = data.get("skus") or []
    if not skus:
        print("输入缺少 skus 数组", file=sys.stderr)
        return 2

    results = [unit_econ(s, a) for s in skus]
    sens_rows = sensitivity(skus[0], a)

    # 多 SKU 时投流按总订单量分摊到每单，避免每个 SKU 重复承担全部投流
    total_orders = sum(fnum(s, "monthly_orders") for s in skus)
    if total_orders and fnum(a, "ad_spend") > 0:
        global_ad_per_order = fnum(a, "ad_spend") / total_orders
        results = [unit_econ(s, a, global_ad_per_order) for s in skus]
        sens_rows = sensitivity(skus[0], a, global_ad_per_order)

    total_rev = sum(r["monthly_revenue"] for r in results)
    total_contrib = sum(r["monthly_contribution"] for r in results)
    total_net = sum(r["monthly_net_profit"] for r in results)
    ad_spend = fnum(a, "ad_spend")
    actual_roas = (sum(r["net_revenue"] * r["monthly_orders"] for r in results) / ad_spend) if ad_spend else 0.0

    ranked = sorted(results, key=lambda r: r["monthly_revenue"], reverse=True)
    cumulative = 0.0
    sku_rows = []
    for r in ranked:
        share = r["monthly_revenue"] / total_rev if total_rev else 0.0
        cumulative += share
        abc = "A" if cumulative <= 0.7 else ("B" if cumulative <= 0.9 else "C")
        stock = fnum(next(s for s in skus if s.get("name", "未命名 SKU") == r["name"]), "stock")
        sold = fnum(next(s for s in skus if s.get("name", "未命名 SKU") == r["name"]), "sales_last_30d", default=r["monthly_orders"])
        sell_through = sold / (sold + stock) if (sold + stock) else 0.0
        if abc == "A" and stock < r["monthly_orders"] * 0.5:
            warning = "断货风险"
        elif sell_through < 0.2:
            warning = "滞销"
        elif stock > r["monthly_orders"] * 3:
            warning = "压货＞3个月"
        else:
            warning = "正常"
        sku_rows.append({"name": r["name"], "monthly_revenue": r["monthly_revenue"], "sales_share": share,
                         "abc": abc, "stock": stock, "sell_through": sell_through, "warning": warning})

    agg = {
        "monthly_revenue": total_rev,
        "monthly_contribution": total_contrib,
        "contribution_margin": total_contrib / total_rev if total_rev else 0.0,
        "monthly_net_profit": total_net,
        "net_margin": total_net / total_rev if total_rev else 0.0,
        "ad_spend": ad_spend,
        "actual_roas": actual_roas,
        "sku_rows": sku_rows,
    }

    if args.format == "json":
        out = json.dumps({"units": results, "aggregate": agg,
                          "return_sensitivity": [{"return_rate": r, "unit": s} for r, s in sens_rows]},
                         ensure_ascii=False, indent=2)
    else:
        out = build_report(data, results, sens_rows, agg)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入 {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
