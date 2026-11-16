"""
RAG 对话处理函数 - CCE 容器版本
基于检索增强的对话生成
"""
import os
import json
import logging
from typing import Dict, List, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatHandler:
    """对话处理器"""

    def __init__(self):
        self.maas_endpoint = os.environ.get('MAAS_ENDPOINT', 'maas.cn-north-4.myhuaweicloud.com')
        self.model_id = os.environ.get('MODEL_ID', 'pangu-7b')
        self.system_prompt = os.environ.get('SYSTEM_PROMPT',
            '你是一个专业的企业服务助手，请根据提供的上下文回答用户问题。')

    def chat(self, question: str, use_rag: bool = True, context: str = '') -> str:
        """
        对话生成 (Flask API 版本)

        Args:
            question: 用户问题
            use_rag: 是否使用 RAG 检索
            context: 外部传入的上下文（可选）

        Returns:
            生成的回答
        """
        logger.info(f"Chat question: {question}, use_rag: {use_rag}")

        # 如果使用 RAG，先检索相关文档
        if use_rag:
            context_docs = self._retrieve_context(question, 3)
            prompt = self._build_prompt(question, context_docs)
        elif context:
            # 使用外部传入的上下文
            prompt = self._build_prompt_from_text(question, context)
        else:
            # 无上下文，直接问答
            prompt = self._build_prompt_from_text(question, '')

        # 调用大模型生成
        answer = self._call_llm(prompt)

        return answer

    def _build_prompt(self, question: str, context: List[Dict]) -> str:
        """
        构建 RAG prompt

        Args:
            question: 用户问题
            context: 检索到的上下文文档列表

        Returns:
            完整 prompt
        """
        # 构建上下文文本
        context_text = "\n\n".join([
            f"参考文档 {i+1}:\n标题: {item.get('title', '')}\n内容: {item.get('content', '')}"
            for i, item in enumerate(context)
        ])

        prompt = f"""{self.system_prompt}

参考上下文:
{context_text}

用户问题: {question}

请根据参考上下文回答用户问题。如果上下文中没有相关信息，请说明无法从提供的内容中找到答案。

回答:"""

        return prompt

    def _build_prompt_from_text(self, question: str, context: str) -> str:
        """
        构建简单 prompt

        Args:
            question: 用户问题
            context: 上下文文本

        Returns:
            完整 prompt
        """
        if context:
            prompt = f"""{self.system_prompt}

参考上下文:
{context}

用户问题: {question}

回答:"""
        else:
            prompt = f"""{self.system_prompt}

用户问题: {question}

回答:"""

        return prompt

    def _call_llm(self, prompt: str) -> str:
        """
        调用大模型服务 (盘古/MaaS)

        Args:
            prompt: 完整 prompt

        Returns:
            模型生成的回答
        """
        # TODO: 调用 MaaS API
        # 示例: POST {maas_endpoint}/v1/{project_id}/chat/completions

        logger.info("Calling LLM...")

        # 模拟返回
        answer = "根据企业服务相关文档，您需要准备以下材料：\n\n1. 公司章程\n2. 法人身份证明\n3. 注册地址证明\n4. 股东会决议\n\n建议您咨询当地工商局获取最新要求。"

        return answer

    def _retrieve_context(self, question: str, top_k: int = 3) -> List[Dict]:
        """
        检索相关上下文

        Args:
            question: 用户问题
            top_k: 检索数量

        Returns:
            检索到的文档
        """
        # 调用搜索函数获取相关文档
        from handler_search import SearchHandler

        search_handler = SearchHandler()
        results = search_handler.hybrid_search(question, top_k)

        return results
