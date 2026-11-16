"""
搜索处理函数 - FunctionGraph
支持关键词搜索、向量搜索、混合搜索
"""
import os
import json
import logging
from typing import Dict, List, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchHandler:
    """搜索处理器"""
    
    def __init__(self):
        self.css_endpoint = os.environ.get('CSS_ENDPOINT', '')
        self.modelarts_endpoint = os.environ.get('MODELARTS_ENDPOINT', '')
        self.index_name = os.environ.get('INDEX_NAME', 'documents')
        
    def keyword_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        关键词搜索 (BM25)
        
        Args:
            query: 搜索关键词
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        logger.info(f"Keyword search: {query}")
        
        # TODO: 调用 CSS 进行 BM25 搜索
        # 实际实现需要连接 CSS 集群
        
        return [
            {
                "id": "1",
                "title": "营业执照办理指南",
                "content": "企业营业执照办理流程...",
                "score": 0.95
            }
        ]
    
    def vector_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        向量语义搜索
        
        Args:
            query: 搜索文本
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        logger.info(f"Vector search: {query}")
        
        # 1. 获取查询向量
        query_vector = self._get_embedding(query)
        
        # 2. 在 CSS 中进行向量搜索
        results = self._css_vector_search(query_vector, top_k)
        
        return results
    
    def hybrid_search(self, query: str, top_k: int = 5, 
                     keyword_weight: float = 0.3, 
                     vector_weight: float = 0.7) -> List[Dict]:
        """
        混合搜索 (BM25 + 向量)
        
        Args:
            query: 搜索文本
            top_k: 返回结果数量
            keyword_weight: 关键词权重
            vector_weight: 向量权重
            
        Returns:
            搜索结果列表
        """
        logger.info(f"Hybrid search: {query}")
        
        # 并行执行两种搜索
        keyword_results = self.keyword_search(query, top_k * 2)
        vector_results = self.vector_search(query, top_k * 2)
        
        # 合并结果
        merged = self._merge_results(
            keyword_results, 
            vector_results,
            keyword_weight,
            vector_weight
        )
        
        return merged[:top_k]
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        获取文本向量 - 调用 ModelArts embedding 服务
        
        Args:
            text: 输入文本
            
        Returns:
            向量数组
        """
        # TODO: 调用 ModelArts embedding API
        # 示例: POST {modelarts_endpoint}/v1/{project_id}/embeddings
        
        import numpy as np
        
        # 模拟返回向量 (实际需要调用 ModelArts)
        embedding = np.random.randn(768).tolist()
        
        return embedding
    
    def _css_vector_search(self, query_vector: List[float], 
                           top_k: int) -> List[Dict]:
        """
        CSS 向量搜索
        
        Args:
            query_vector: 查询向量
            top_k: 返回数量
            
        Returns:
            搜索结果
        """
        # TODO: 连接 CSS 集群执行 kNN 搜索
        # 使用 huaweiclients CSS SDK
        
        return [
            {
                "id": "2",
                "title": "公司注册流程",
                "content": "新公司注册所需材料和流程...",
                "score": 0.88
            }
        ]
    
    def _merge_results(self, 
                       keyword_results: List[Dict],
                       vector_results: List[Dict],
                       keyword_weight: float,
                       vector_weight: float) -> List[Dict]:
        """
        合并搜索结果
        
        Args:
            keyword_results: 关键词搜索结果
            vector_results: 向量搜索结果
            keyword_weight: 关键词权重
            vector_weight: 向量权重
            
        Returns:
            合并后的结果
        """
        # 构建结果映射
        result_map = {}
        
        for r in keyword_results:
            rid = r['id']
            r['keyword_score'] = r.pop('score', 0)
            r['final_score'] = r['keyword_score'] * keyword_weight
            result_map[rid] = r
        
        for r in vector_results:
            rid = r['id']
            r['vector_score'] = r.pop('score', 0)
            if rid in result_map:
                result_map[rid]['vector_score'] = r['vector_score']
                result_map[rid]['final_score'] += r['vector_score'] * vector_weight
            else:
                r['final_score'] = r['vector_score'] * vector_weight
                result_map[rid] = r
        
        # 按分数排序
        sorted_results = sorted(
            result_map.values(), 
            key=lambda x: x['final_score'], 
            reverse=True
        )
        
        return sorted_results


def handler(event, context):
    """
    FunctionGraph 入口函数
    
    Args:
        event: 请求事件
        context: 上下文
        
    Returns:
        API 响应
    """
    try:
        # 解析请求
        body = json.loads(event.get('body', '{}'))
        
        query = body.get('query', '')
        search_type = body.get('search_type', 'hybrid')
        top_k = body.get('top_k', 5)
        
        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'query is required'})
            }
        
        # 执行搜索
        handler = SearchHandler()
        
        if search_type == 'keyword':
            results = handler.keyword_search(query, top_k)
        elif search_type == 'vector':
            results = handler.vector_search(query, top_k)
        else:  # hybrid
            results = handler.hybrid_search(query, top_k)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'data': results,
                'query': query,
                'search_type': search_type
            })
        }
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


if __name__ == '__main__':
    # 本地测试
    test_event = {
        'body': json.dumps({
            'query': '如何注册公司',
            'search_type': 'hybrid',
            'top_k': 5
        })
    }
    result = handler(test_event, None)
    print(result)
