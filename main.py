# Competitor Insight Agent
# 入口文件

import argparse
from src.collector import WebCollector
from src.knowledge_base import KnowledgeBase
from src.report_generator import ReportGenerator


def cmd_collect(args):
    """采集竞品网站并生成报告"""
    print(f"开始采集: {args.url}")
    collector = WebCollector(args.url)
    results = collector.collect_common_pages()

    # 存入知识库
    kb = KnowledgeBase()
    kb.add_documents(results)

    # 生成报告
    from urllib.parse import urlparse
    domain = urlparse(args.url).netloc.replace("www.", "")
    gen = ReportGenerator(competitor_name=domain)
    report = gen.generate(results, kb_stats=kb.get_stats())
    filepath = gen.save(report)

    success = len([r for r in results if r["status"] == "success"])
    print(f"采集完成: {success}/{len(results)} 个页面成功")
    print(f"报告已生成: {filepath}")


def cmd_ask(args):
    """向知识库提问"""
    kb = KnowledgeBase()
    result = kb.ask(args.question, n_results=args.top_k)
    print(f"\n问题: {result['question']}")
    print(f"\n回答: {result['answer']}")
    if result.get("sources"):
        print(f"\n信息来源:")
        for s in result["sources"]:
            print(f"  - {s}")


def cmd_stats(args):
    """查看知识库统计"""
    kb = KnowledgeBase()
    print(f"知识库统计: {kb.get_stats()}")


def main():
    parser = argparse.ArgumentParser(description="Competitor Insight Agent")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # collect 命令
    collect_parser = subparsers.add_parser("collect", help="采集竞品网站并生成报告")
    collect_parser.add_argument("--url", required=True, help="竞品官网地址")

    # ask 命令
    ask_parser = subparsers.add_parser("ask", help="向知识库提问")
    ask_parser.add_argument("--question", required=True, help="问题内容")
    ask_parser.add_argument("--top-k", type=int, default=3, help="检索结果数量")

    # stats 命令
    subparsers.add_parser("stats", help="查看知识库统计")

    args = parser.parse_args()

    if args.command == "collect":
        cmd_collect(args)
    elif args.command == "ask":
        cmd_ask(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
