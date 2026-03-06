#!/usr/bin/env python3
"""
轻量级语义搜索（使用 TF-IDF，不需要下载模型）
适合网络受限环境
"""

import json
import hashlib
import re
from datetime import datetime
from pathlib import Path
from collections import Counter
import math

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_FILE = WORKSPACE / "MEMORY.md"
MEMORY_INDEX_FILE = WORKSPACE / "memory" / "tfidf_index.json"


class TFIDFSearch:
    """TF-IDF 搜索引擎"""
    
    def __init__(self):
        self.memories = []
        self.idf = {}  # 逆文档频率
        self.index_file = MEMORY_INDEX_FILE
        self.load_index()
    
    def tokenize(self, text):
        """分词（支持中英文）"""
        # 中文按字符分词，英文按单词分词
        text = text.lower()
        
        # 提取中文字符
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        
        # 提取英文单词
        english_words = re.findall(r'\b[a-z]+\b', text)
        
        # 合并
        tokens = chinese_chars + english_words
        
        # 过滤停用词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个'}
        tokens = [t for t in tokens if t not in stopwords and len(t) > 0]
        
        return tokens
    
    def compute_tfidf(self):
        """计算 TF-IDF"""
        # 计算文档频率
        df = Counter()
        for memory in self.memories:
            tokens = set(self.tokenize(memory["text"]))
            for token in tokens:
                df[token] += 1
        
        # 计算 IDF
        n_docs = len(self.memories)
        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log((n_docs + 1) / (freq + 1)) + 1
        
        # 计算每个记忆的 TF-IDF 向量
        for memory in self.memories:
            tokens = self.tokenize(memory["text"])
            tf = Counter(tokens)
            
            # 归一化 TF
            max_freq = max(tf.values()) if tf else 1
            tf_normalized = {k: v/max_freq for k, v in tf.items()}
            
            # 计算 TF-IDF
            tfidf = {k: v * self.idf.get(k, 0) for k, v in tf_normalized.items()}
            memory["tfidf"] = tfidf
    
    def cosine_similarity(self, vec1, vec2):
        """计算余弦相似度"""
        # 获取所有术语
        all_terms = set(vec1.keys()) | set(vec2.keys())
        
        if not all_terms:
            return 0.0
        
        # 计算点积和模长
        dot_product = sum(vec1.get(t, 0) * vec2.get(t, 0) for t in all_terms)
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def load_index(self):
        """加载索引"""
        if self.index_file.exists():
            with open(self.index_file, encoding='utf-8') as f:
                data = json.load(f)
                self.memories = data.get("memories", [])
                self.idf = data.get("idf", {})
                print(f"✓ 加载了 {len(self.memories)} 条记忆索引")
        else:
            self.build_index_from_memory()
    
    def build_index_from_memory(self):
        """从 MEMORY.md 构建索引"""
        if not MEMORY_FILE.exists():
            return
        
        with open(MEMORY_FILE, encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        current_section = "General"
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            if line.startswith('## '):
                current_section = line.replace('## ', '')
                continue
            
            if line.startswith('- ') or line.startswith('* '):
                line = line[2:]
            
            if len(line) > 20:
                metadata = {"section": current_section}
                self.add_memory(line, metadata=metadata, save=False)
        
        self.compute_tfidf()
        self.save_index()
        print(f"✓ 从 MEMORY.md 构建了 {len(self.memories)} 条记忆索引")
    
    def add_memory(self, text, metadata=None, save=True):
        """添加记忆"""
        memory_id = hashlib.md5(text.encode()).hexdigest()[:8]
        
        memory = {
            "id": memory_id,
            "text": text,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None
        }
        
        # 检查是否已存在
        for i, m in enumerate(self.memories):
            if m["id"] == memory_id:
                self.memories[i] = memory
                print(f"✓ 更新记忆：{text[:50]}...")
                if save:
                    self.compute_tfidf()
                    self.save_index()
                return
        
        # 添加新记忆
        self.memories.append(memory)
        print(f"✓ 添加记忆：{text[:50]}...")
        
        if save:
            self.compute_tfidf()
            self.save_index()
    
    def search(self, query, top_k=5, min_similarity=0.1):
        """搜索"""
        if not self.memories:
            return []
        
        # 计算查询的 TF-IDF
        query_tokens = self.tokenize(query)
        query_tf = Counter(query_tokens)
        if query_tf:
            max_freq = max(query_tf.values())
            query_tf_normalized = {k: v/max_freq for k, v in query_tf.items()}
        else:
            query_tf_normalized = {}
        
        query_tfidf = {k: v * self.idf.get(k, 0) for k, v in query_tf_normalized.items()}
        
        # 计算相似度
        similarities = []
        for i, memory in enumerate(self.memories):
            if "tfidf" not in memory:
                continue
            
            sim = self.cosine_similarity(query_tfidf, memory["tfidf"])
            if sim >= min_similarity:
                similarities.append((i, sim))
        
        # 排序
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
    
    def save_index(self):
        """保存索引"""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 不保存 tfidf 向量，下次重新计算
        data = {
            "memories": self.memories,
            "idf": self.idf,
            "last_updated": datetime.now().isoformat(),
            "total_count": len(self.memories)
        }
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_statistics(self):
        """获取统计"""
        if not self.memories:
            return {"total": 0}
        
        total_access = sum(m.get("access_count", 0) for m in self.memories)
        
        return {
            "total_memories": len(self.memories),
            "total_accesses": total_access,
            "index_file": str(self.index_file),
            "search_method": "TF-IDF"
        }


def main():
    """命令行"""
    import sys
    
    search = TFIDFSearch()
    
    if len(sys.argv) < 2:
        print("用法：tfidf-search.py <命令> [参数]")
        print("\n命令:")
        print("  search <查询>     - 搜索")
        print("  add <文本>        - 添加记忆")
        print("  stats             - 显示统计")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search":
        query = " ".join(sys.argv[2:])
        print(f"\n🔍 搜索：{query}\n")
        results = search.search(query, top_k=5)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"{i}. [{result.get('similarity', 0):.2f}] {result['text']}")
                print(f"   访问：{result.get('access_count', 0)} 次")
        else:
            print("未找到相关记忆")
    
    elif command == "add":
        text = " ".join(sys.argv[2:])
        search.add_memory(text)
    
    elif command == "stats":
        stats = search.get_statistics()
        print("\n📊 统计")
        print("=" * 50)
        for key, value in stats.items():
            print(f"{key}: {value}")
        print("=" * 50)


if __name__ == "__main__":
    main()
