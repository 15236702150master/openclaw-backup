#!/usr/bin/env python3
"""
记忆重要性评分和管理
根据访问频率、时间衰减等计算记忆重要性
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
IMPORTANCE_LOG = WORKSPACE / "memory" / "importance-log.json"


class MemoryImportanceManager:
    """记忆重要性管理器"""
    
    def __init__(self):
        self.log_file = IMPORTANCE_LOG
        self.logs = self.load_logs()
    
    def load_logs(self):
        """加载访问日志"""
        if self.log_file.exists():
            with open(self.log_file, encoding='utf-8') as f:
                return json.load(f)
        return {"accesses": [], "updates": []}
    
    def record_access(self, memory_id, memory_text, context="search"):
        """记录记忆访问"""
        access = {
            "memory_id": memory_id,
            "memory_text": memory_text[:100],
            "timestamp": datetime.now().isoformat(),
            "context": context
        }
        self.logs["accesses"].append(access)
        
        # 保留最近 1000 条记录
        self.logs["accesses"] = self.logs["accesses"][-1000:]
        self.save_logs()
    
    def calculate_importance(self, memory_id, memory_text, created_at):
        """计算记忆重要性分数 (0-1)"""
        # 1. 访问频率分数 (0-0.4)
        access_count = sum(1 for a in self.logs["accesses"] if a["memory_id"] == memory_id)
        access_score = min(0.4, access_count * 0.05)  # 每次访问 +0.05，最高 0.4
        
        # 2. 时间衰减分数 (0-0.3)
        try:
            created = datetime.fromisoformat(created_at)
            age_days = (datetime.now() - created).days
            recency_score = max(0, 0.3 * (1 - age_days / 90))  # 90 天内线性衰减
        except:
            recency_score = 0.1
        
        # 3. 内容质量分数 (0-0.3)
        quality_score = 0.1  # 基础分
        
        # 关键词加分
        important_keywords = ["偏好", "习惯", "重要", "项目", "决定", "配置"]
        for keyword in important_keywords:
            if keyword in memory_text:
                quality_score += 0.05
        
        quality_score = min(0.3, quality_score)
        
        # 总分
        total_score = access_score + recency_score + quality_score
        return round(total_score, 3)
    
    def get_importance_label(self, score):
        """将分数转换为标签"""
        if score >= 0.8:
            return "⭐⭐⭐⭐⭐ 极重要"
        elif score >= 0.6:
            return "⭐⭐⭐⭐ 重要"
        elif score >= 0.4:
            return "⭐⭐⭐ 中等"
        elif score >= 0.2:
            return "⭐⭐ 次要"
        else:
            return "⭐ 可清理"
    
    def save_logs(self):
        """保存日志"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)
    
    def generate_importance_report(self):
        """生成重要性报告"""
        # 统计所有记忆的重要性
        memory_stats = {}
        
        for access in self.logs["accesses"]:
            mid = access["memory_id"]
            if mid not in memory_stats:
                memory_stats[mid] = {
                    "text": access["memory_text"],
                    "access_count": 0,
                    "last_access": None
                }
            memory_stats[mid]["access_count"] += 1
            memory_stats[mid]["last_access"] = access["timestamp"]
        
        # 计算重要性并排序
        report = []
        for mid, stats in memory_stats.items():
            importance = self.calculate_importance(
                mid,
                stats["text"],
                stats["last_access"] or datetime.now().isoformat()
            )
            report.append({
                "memory_id": mid,
                "text": stats["text"],
                "access_count": stats["access_count"],
                "importance": importance,
                "label": self.get_importance_label(importance)
            })
        
        # 按重要性排序
        report.sort(key=lambda x: x["importance"], reverse=True)
        
        return report
    
    def cleanup_recommendations(self, min_age_days=30, max_importance=0.3):
        """生成清理建议"""
        report = self.generate_importance_report()
        
        recommendations = []
        cutoff_date = datetime.now() - timedelta(days=min_age_days)
        
        for item in report:
            if item["importance"] <= max_importance:
                recommendations.append(item)
        
        return recommendations
    
    def save_logs(self):
        """保存日志"""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)


def main():
    """命令行界面"""
    import sys
    
    manager = MemoryImportanceManager()
    
    if len(sys.argv) < 2:
        print("用法：memory-importance.py <命令>")
        print("\n命令:")
        print("  report            - 生成重要性报告")
        print("  cleanup           - 生成清理建议")
        print("  stats             - 显示统计")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "report":
        print("\n📊 记忆重要性报告\n")
        print("=" * 70)
        report = manager.generate_importance_report()
        
        for i, item in enumerate(report[:20], 1):  # 显示前 20 条
            print(f"{i:2d}. [{item['label']}]")
            print(f"    {item['text']}")
            print(f"    访问：{item['access_count']} 次 | 分数：{item['importance']:.3f}")
            print()
        
        print("=" * 70)
        print(f"总计：{len(report)} 条记忆")
    
    elif command == "cleanup":
        print("\n🗑️  清理建议\n")
        recommendations = manager.cleanup_recommendations()
        
        if recommendations:
            print(f"发现 {len(recommendations)} 条可清理的记忆:\n")
            for item in recommendations[:10]:
                print(f"- {item['text']}")
                print(f"  重要性：{item['importance']:.3f} | 访问：{item['access_count']} 次\n")
        else:
            print("✓ 没有需要清理的记忆")
    
    elif command == "stats":
        print("\n📈 访问统计")
        print("=" * 50)
        print(f"总访问记录：{len(manager.logs['accesses'])}")
        print(f"唯一记忆数：{len(set(a['memory_id'] for a in manager.logs['accesses']))}")
        print("=" * 50)


if __name__ == "__main__":
    main()
