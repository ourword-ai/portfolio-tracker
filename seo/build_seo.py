#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO/GEO build for Market Watch. Run from the repo root: python seo/build_seo.py

This one is a tool, not a corpus: the numbers on screen are the visitor's own and are
none of a crawler's business. So it gets page-level work only — a correct canonical, a
WebApplication description that explains what the tool does and what it deliberately
does not store, and an llms.txt that tells an answer engine the same thing in one read.
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo_kit as G

SITE = G.Site(
    path="portfolio-tracker",
    name="Market Watch", name_zh="投资观察仪表盘",
    tagline="watch the shape of your portfolio, never the amount",
    tagline_zh="只看持仓占比与买卖区间，不含金额",
    description=(
        "A portfolio dashboard that deliberately refuses to know what you are worth. You "
        "enter weights, not amounts: it shows concentration, allocation, an indexed net-worth "
        "line starting at 100, and live crypto prices, so you can see the shape of the "
        "portfolio and the buy/sell bands without a number on screen that hurts to look at. "
        "Everything stays in the browser."),
    description_zh=(
        "一个故意不知道你有多少钱的投资看板。你输入的是占比不是金额：它显示集中度、"
        "资产分布、以 100 为起点的指数化净值曲线，以及实时加密价格——让你看到组合的形状"
        "和买卖区间，而屏幕上没有一个看着难受的数字。数据全部留在浏览器里。"),
    keywords=("投资组合 看板, 持仓 占比, 资产配置 集中度, 加密 价格 实时, portfolio dashboard, "
              "allocation concentration, privacy-first portfolio tracker"),
    item_type="WebApplication", item_noun="tool", item_noun_zh="工具",
    lang="zh-Hans", changefreq="weekly",
)

HOW = ("A single static page. Prices are fetched client-side from public endpoints; holdings "
       "are stored in the browser only and are never sent anywhere, which is also why there "
       "is nothing here for a crawler to index beyond this description.")

CITE = "Cite the page itself. There is no dataset behind it — the numbers belong to whoever is looking."


def main():
    today = datetime.date.today().isoformat()
    secs = [
        ("What does it show?",
         "Concentration (how much of the portfolio sits in its largest position), allocation "
         "across assets, an indexed net-worth line that starts at 100 so trends are readable "
         "without amounts, and live prices for the crypto positions."),
        ("Why are there no amounts?",
         "Because the amount is the part that makes people either complacent or miserable, and "
         "it is not the part that informs a decision. Weights, concentration and the distance "
         "to your own buy/sell bands are. Entering percentages also means the page never holds "
         "anything worth stealing."),
        ("Where is the data stored?",
         "In the browser, on the device it was typed into. There is no account, no server-side "
         "store and no sync."),
    ]
    doc = G.Item(slug="portfolio-tracker", title=SITE.name, summary=SITE.description,
                 blocks=secs, title_zh=SITE.name_zh, summary_zh=SITE.description_zh,
                 blocks_zh=secs, updated=today, url_override=SITE.base,
                 source_url="https://github.com/ourword-ai/portfolio-tracker")

    app_ld = {"@context": "https://schema.org", "@type": "WebApplication",
              "name": SITE.name_zh, "alternateName": SITE.name, "url": SITE.base,
              "applicationCategory": "FinanceApplication",
              "operatingSystem": "Any (web browser)",
              "description": G.plain(SITE.description_zh, 500),
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
              "publisher": {"@type": "Organization", "name": "OurWord AI",
                            "url": "https://ourword.ai/"}}
    ld = [app_ld]
    f = G.faq_ld(doc, False)
    if f:
        ld.append(f)

    rep = G.build(SITE, [doc], root=".", today=today, how_built=HOW, cite_as=CITE,
                  item_pages=False, extra_ld=ld,
                  extra_sitemaps=["https://ourword.ai/sitemap.xml"])
    print("portfolio-tracker seo/geo:", json.dumps(rep, ensure_ascii=False))
    return rep


if __name__ == "__main__":
    main()
