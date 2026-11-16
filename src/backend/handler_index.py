"""
文档索引处理函数 - FunctionGraph
将文档向量化并存储到 CSS
"""
import os
import json
import logging
from typing import Dict, List, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexHandler:
    """文档索引处理器"""

    def __init__(self):
        self.css_endpoint = os.environ.get('CSS_ENDPOINT', '')
        self.index_name = os.environ.get('INDEX_NAME', 'documents')

    def build_index(self, documents: List[Dict], index_name: str = '') -> Dict:
        """
        构建索引 (Flask API 版本)

        Args:
            documents: 文档列表
            index_name: 索引名称

        Returns:
            索引结果
        """
        if index_name:
            self.index_name = index_name
        return self.index_documents(documents)

    def index_documents(self, documents: List[Dict]) -> Dict:
        """
        索引文档
        
        Args:
            documents: 文档列表
            
        Returns:
            索引结果
        """
        logger.info(f"Indexing {len(documents)} documents")
        
        indexed_ids = []
        failed_ids = []
        
        for doc in documents:
            try:
                doc_id = doc.get('id')
                
                # 获取向量
                content = doc.get('content', '')
                vector = self._get_embedding(content)
                
                # 存储到 CSS
                self._store_to_css(doc, vector)
                
                indexed_ids.append(doc_id)
                
            except Exception as e:
                logger.error(f"Failed to index doc {doc.get('id')}: {e}")
                failed_ids.append(doc_id)
        
        return {
            'indexed': len(indexed_ids),
            'failed': len(failed_ids),
            'indexed_ids': indexed_ids,
            'failed_ids': failed_ids
        }
    
    def _get_embedding(self, text: str) -> List[float]:
        """
        获取文本向量
        
        Args:
            text: 输入文本
            
        Returns:
            向量数组
        """
        # TODO: 调用 ModelArts embedding API
        import numpy as np
        
        # 模拟返回向量
        embedding = np.random.randn(768).tolist()
        
        return embedding
    
    def _store_to_css(self, doc: Dict, vector: List[float]) -> None:
        """
        存储文档到 CSS
        
        Args:
            doc: 文档对象
            vector: 向量
        """
        # TODO: 使用 huaweiclients CSS SDK 存储文档
        # 示例:
        # client = CssClient(credentials, region)
        # client.cluster().create_document(index, doc)
        
        logger.info(f"Stored document {doc.get('id')} to CSS")


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
        
        documents = body.get('documents', [])
        
        if not documents:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'documents is required'})
            }
        
        # 索引文档
        handler = IndexHandler()
        result = handler.index_documents(documents)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'result': result
            })
        }
        
    except Exception as e:
        logger.error(f"Index error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


if __name__ == '__main__':
    # 本地测试
    test_event = {
        'body': json.dumps({
            'documents': [
                {
                    'id': '1',
                    'title': '营业执照办理',
                    'content': '企业营业执照办理流程...'
                },
                {
                    'id': '2',
                    'title': '税务登记',
                    'content': '税务登记办理流程...'
                }
            ]
        })
    }
    result = handler(test_event, None)
    print(result)
