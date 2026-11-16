"""
Semantic Search Backend - Flask API Server
替换 FunctionGraph，支持容器化部署
"""
import os
import json
import logging
from flask import Flask, request, jsonify
from handler_search import SearchHandler
from handler_chat import ChatHandler
from handler_index import IndexHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化处理器
search_handler = SearchHandler()
chat_handler = ChatHandler()
index_handler = IndexHandler()


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'semantic-search-backend'
    })


@app.route('/search', methods=['POST'])
def search():
    """
    搜索 API - 替代原 FunctionGraph search 函数
    """
    try:
        data = request.get_json() or {}

        query = data.get('query', '')
        search_type = data.get('search_type', 'hybrid')
        top_k = data.get('top_k', 5)

        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400

        if search_type == 'keyword':
            results = search_handler.keyword_search(query, top_k)
        elif search_type == 'vector':
            results = search_handler.vector_search(query, top_k)
        else:  # hybrid
            results = search_handler.hybrid_search(query, top_k)

        return jsonify({
            'success': True,
            'data': results,
            'query': query,
            'search_type': search_type
        })

    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/chat', methods=['POST'])
def chat():
    """
    对话 API - 替代原 FunctionGraph rag 函数
    """
    try:
        data = request.get_json() or {}

        question = data.get('question', '')
        use_rag = data.get('use_rag', True)
        context = data.get('context', '')

        if not question:
            return jsonify({
                'success': False,
                'error': 'question is required'
            }), 400

        answer = chat_handler.chat(question, use_rag, context)

        return jsonify({
            'success': True,
            'answer': answer,
            'question': question
        })

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/index', methods=['POST'])
def index():
    """
    索引构建 API - 替代原 FunctionGraph index 函数
    """
    try:
        data = request.get_json() or {}

        documents = data.get('documents', [])
        index_name = data.get('index_name', 'documents')

        if not documents:
            return jsonify({
                'success': False,
                'error': 'documents is required'
            }), 400

        result = index_handler.build_index(documents, index_name)

        return jsonify({
            'success': True,
            'result': result,
            'indexed_count': len(documents)
        })

    except Exception as e:
        logger.error(f"Index error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/', methods=['GET'])
def root():
    """根路径"""
    return jsonify({
        'service': 'semantic-search-backend',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'search': '/search',
            'chat': '/chat',
            'index': '/index'
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Semantic Search Backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
