"""
竞品报告生成模块
把采集到的数据整理成结构化的 Markdown 报告
"""
from typing import List, Dict
from datetime import datetime
import os


class ReportGenerator:
    def __init__(self, competitor_name: str):
        self.competitor_name = competitor_name
        self.report_date = datetime.now().strftime("%Y-%m-%d")

    def generate(self, collect_results: List[Dict], kb_stats: Dict = None) -> str:
        """生成完整的竞品分析报告"""
        lines = []

        # 报告头
        lines.append(f"# {self.competitor_name} 竞品分析报告")
        lines.append(f"\n> 生成时间：{self.report_date}")
        lines.append("")

        # 采集概况
        success_pages = [r for r in collect_results if r["status"] == "success"]
        lines.append("## 一、采集概况")
        lines.append(f"- 采集页面总数：{len(collect_results)}")
        lines.append(f"- 成功页面数：{len(success_pages)}")
        lines.append(f"- 采集成功率：{len(success_pages)/len(collect_results)*100:.1f}%")
        lines.append("")

        # 产品与定价信息
        lines.append("## 二、产品与定价信息")
        all_prices = []
        all_products = []
        for page in success_pages:
            structured = page.get("structured", {})
            all_prices.extend(structured.get("prices", []))
            all_products.extend(structured.get("product_names", []))

        if all_products:
            lines.append("### 识别到的产品/套餐：")
            for p in list(set(all_products))[:10]:
                lines.append(f"- {p}")
        else:
            lines.append("- 未识别到明确的产品名称")

        lines.append("")
        if all_prices:
            lines.append("### 识别到的价格点：")
            for price in sorted(list(set(all_prices)))[:10]:
                lines.append(f"- ¥{price}")
        else:
            lines.append("- 未识别到明确的价格信息")

        lines.append("")

        # 各页面摘要
        lines.append("## 三、各页面内容摘要")
        for i, page in enumerate(success_pages):
            lines.append(f"### {i+1}. {page['title']}")
            lines.append(f"- 地址：{page['url']}")
            # 取前200字作为摘要
            summary = page["content"][:200].replace("\n", " ")
            lines.append(f"- 摘要：{summary}...")
            lines.append("")

        # 知识库统计
        if kb_stats:
            lines.append("## 四、知识库状态")
            lines.append(f"- 文档切片总数：{kb_stats.get('total_chunks', 0)}")
            lines.append("")

        # 结论与建议
        lines.append("## 五、初步观察")
        lines.append("- 建议持续监控该竞品的官网更新和定价变化")
        lines.append("- 可通过知识库问答功能深入了解具体产品细节")

        return "\n".join(lines)

    def save(self, report_content: str, output_dir: str = "output") -> str:
        """保存报告到文件"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = f"{self.competitor_name}_report_{self.report_date}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_content)

        return filepath


if __name__ == "__main__":
    gen = ReportGenerator("示例竞品公司")
    # 测试
    test_results = [
        {"url": "/", "title": "首页", "content": "这是示例内容...", "status": "success",
         "structured": {"prices": [99, 199], "product_names": ["基础版", "专业版"]}}
    ]
    report = gen.generate(test_results)
    print(report)
