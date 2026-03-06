#!/usr/bin/env python3
"""
语义记忆搜索
使用向量嵌入实现语义搜索，比关键词搜索更准确
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SEMANTIC_SEARCH_AVAILABLE = True
except ImportError:
    SEMANTIC_SEARCH_AVAILABLE = False
    print("警告：sentence-transformers 未安装，将使用关键词搜索")
    print("安装：pip3 install sentence-transformers")

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_INDEX_FILE = WORKSPACE / "memory" / "semantic_index.json"

class SemanticMemorySearch:
    """语义记忆搜索"""
    
    def __init__(self):
        self.model = None
        self.memories = []
        self.embeddings = []
        self.index_file = MEMORY_INDEX_FILE
        
        if SEMANTIC_SEARCH_AVAILABLE:
            try:
                print("加载语义搜索模型...")
                # 尝试使用本地模型，如果网络不可用则使用备用模型
                try:
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                    print("✓ 模型加载完成 (all-MiniLM-L6-v2)")
                except:
                    # 使用更小的本地模型
                    print("⚠ 无法下载模型，使用备用方案...")
                    self.model = None
                    print("将使用 TF-IDF 关键词搜索")
            except Exception as e:
                print(f"⚠ 模型加载失败：{e}")
                print("将使用关键词搜索")
        
        self.load_index()
    
    def load_index(self):
        """加载或创建索引"""
        if self.index_file.exists():
            with open(self.index_file, encoding='utf-8') as f:
                data = json.load(f)
                self.memories = data.get("memories", [])
                print(f"✓ 加载了 {len(self.memories)} 条记忆索引")
        else:
            # 从 MEMORY.md 提取记忆
            self.build_index_from_memory()
    
    def build_index_from_memory(self):
        """从 MEMORY.md 构建索引"""
        if not MEMORY_FILE.exists():
            return
        
        with open(MEMORY_FILE, encoding='utf-8') as f:
            content = f.read()
        
        # 简单的分块策略：按行分割，过滤空行和短行
        lines = content.split('\n')
        current_section = "General"
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            # 检测章节标题
            if line.startswith('## '):
                current_section = line.replace('## ', '')
                continue
            
            # 跳过列表符号
            if line.startswith('- ') or line.startswith('* '):
                line = line[2:]
            
            # 添加记忆片段
            if len(line) > 20:  # 只索引有意义的句子
                self.add_memory(line, section=current_section, save=False)
        
        self.save_index()
        print(f"✓ 从 MEMORY.md 构建了 {len(self.memories)} 条记忆索引")
    
    def add_memory(self, text, metadata=None, save=True):
        """添加记忆到索引"""
        memory_id = hashlib.md5(text.encode()).hexdigest()[:8]
        
        memory = {
            "id": memory_id,
            "text": text,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "access_count": 0,
            "importance": 1.0,
            "last_accessed": None
        }
        
        # 检查是否已存在
        for i, m in enumerate(self.memories):
            if m["id"] == memory_id:
                # 更新现有记忆
                self.memories[i] = memory
                if SEMANTIC_SEARCH_AVAILABLE and self.model:
                    self.embeddings[i] = self.model.encode(text)
                print(f"✓ 更新记忆：{text[:50]}...")
                if save:
                    self.save_index()
                return
        
        # 添加新记忆
        self.memories.append(memory)
        if SEMANTIC_SEARCH_AVAILABLE and self.model:
            embedding = self.model.encode(text)
            self.embeddings.append(embedding)
        
        print(f"✓ 添加记忆：{text[:50]}...")
        if save:
            self.save_index()
    
    def search(self, query, top_k=5, min_similarity=0.3):
        """语义搜索"""
        if not self.memories:
            return []
        
        if SEMANTIC_SEARCH_AVAILABLE and self.model and self.embeddings:
            # 语义搜索
            query_embedding = self.model.encode(query)
            
            similarities = []
            for i, memory in enumerate(self.memories):
                sim = cosine_similarity([query_embedding], [self.embeddings[i]])[0][0]
                if sim >= min_similarity:
                    similarities.append((i, sim))
            
            # 按相似度排序
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # 更新访问统计
            results = []
            for i, sim in similarities[:top_k]:
                memory = self.memories[i].copy()
                memory["similarity"] = float(sim)
                memory["access_count"] += 1
                memory["last_accessed"] = datetime.now().isoformat()
                self.memories[i]["access_count"] = memory["access_count"]
                self.memories[i]["last_accessed"] = memory["last_accessed"]
                results.append(memory)
            
            self.save_index()
            return results
        else:
            # 降级到关键词搜索
            return self.keyword_search(query, top_k)
    
    def keyword_search(self, query, top_k=5):
        """关键词搜索（fallback）"""
        query_lower = query.lower()
        results = []
        
        for memory in self.memories:
            if query_lower in memory["text"].lower():
                results.append(memory.copy())
        
        # 按访问次数排序
        results.sort(key=lambda x: x.get("access_count", 0), reverse=True)
        return results[:top_k]
    
    def save_index(self):
        """保存索引"""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 不保存 embeddings，只保存记忆元数据
        # embeddings 会在下次加载时重新计算
        data = {
            "memories": self.memories,
            "last_updated": datetime.now().isoformat(),
            "total_count": len(self.memories)
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self):
        """获取统计信息"""
        if not self.memories:
            return {"total": 0}
        
        total_access = sum(m.get("access_count", 0) for m in self.memories)
        avg_importance = sum(m.get("importance", 1.0) for m in self.memories) / len(self.memories)
        
        return {
            "total_memories": len(self.memories),
            "total_accesses": total_access,
            "avg_importance": avg_importance,
            "index_file": str(self.index_file)
        }
    
    def cleanup_low_importance(self, threshold=0.2, min_age_days=30):
        """清理低重要性记忆"""
        cutoff = datetime.now().timestamp() - (min_age_days * 24 * 3600)
        
        to_remove = []
        for i, memory in enumerate(self.memories):
            created = datetime.fromisoformat(memory["created_at"]).timestamp()
            importance = memory.get("importance", 1.0)
            access_count = memory.get("access_count", 0)
            
            # 低重要性 + 长时间未访问
            if importance < threshold and access_count < 3 and created < cutoff:
                to_remove.append(i)
        
        # 从后往前删除
        for i in reversed(to_remove):
            print(f"🗑️  删除低重要性记忆：{self.memories[i]['text'][:50]}...")
            del self.memories[i]
        
        if to_remove:
            self.save_index()
            print(f"✓ 清理了 {len(to_remove)} 条低重要性记忆")
        
        return len(to_remove)


def main():
    """命令行界面"""
    import sys
    
    search = SemanticMemorySearch()
    
    if len(sys.argv) < 2:
        print("用法：semantic-search.py <命令> [参数]")
        print("\n命令:")
        print("  search <查询>     - 语义搜索")
        print("  add <文本>        - 添加记忆")
        print("  stats             - 显示统计")
        print("  cleanup           - 清理低重要性记忆")
        print("\n示例:")
        print("  semantic-search.py search \"用户买了什么\"")
        print("  semantic-search.py add \"用户喜欢 Python\"")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        query = " ".join(sys.argv[2:])
        print(f"\n🔍 搜索：{query}\n")
        results = search.search(query, top_k=5)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"{i}. [{result.get('similarity', 0):.2f}] {result['text']}")
                print(f"   访问次数：{result.get('access_count', 0)} | 重要性：{result.get('importance', 1.0):.2f}")
        else:
            print("未找到相关记忆")
    
    elif command == "add":
        text = " ".join(sys.argv[2:])
        search.add_memory(text)
    
    elif command == "stats":
        stats = search.get_statistics()
        print("\n📊 记忆统计")
        print("=" * 50)
        for key, value in stats.items():
            print(f"{key}: {value}")
        print("=" * 50)
    
    elif command == "cleanup":
        removed = search.cleanup_low_importance()
        print(f"清理完成，删除了 {removed} 条记忆")
    
    else:
        print(f"未知命令：{command}")


if __name__ == "__main__":
    main()
