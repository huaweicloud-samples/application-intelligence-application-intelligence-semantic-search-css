# 语义搜索解决方案

> 基于华为云的语义搜索实现，支持向量检索与 RAG

<!-- 章节 1: 标题与徽章 [CRITICAL] -->
[![License](https://img.shields.io/badge/License-MIT%20No%20Attribution-blue.svg)](LICENSE)
[![Huawei Cloud](https://img.shields.io/badge/Huawei%20Cloud-Search-red.svg)](https://www.huaweicloud.com/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](#)

---

## 1. 简介 / Overview [CRITICAL]

**中文**：本实践提供基于华为云的语义搜索解决方案，支持从传统关键字搜索（BM25）到向量语义搜索，再到检索增强生成（RAG）的完整能力。可作为企业知识库、智能问答系统的参考架构。

**English**: This solution provides semantic search capabilities on Huawei Cloud, supporting traditional keyword search (BM25), vector-based semantic search, and Retrieval Augmented Generation (RAG). It serves as a reference architecture for enterprise knowledge bases and intelligent Q&A systems.

### 核心能力

- 向量语义搜索
- 全文检索
- RAG 检索增强
- 对话式搜索
- 模型微调集成

---

## 2. 目录

- [1. 简介](#1-简介--overview-critical)
- [2. 目录](#2-目录)
- [3. 架构图](#3-架构图)
- [4. 方案亮点](#4-方案亮点)
- [5. 涉及云服务](#5-涉及云服务)
- [6. 前置条件](#6-前置条件-critical)
- [7. 快速开始](#7-快速开始-critical)
- [8. 分步部署](#8-分步部署)
- [9. 使用方法 / 验证](#9-使用方法--验证-critical)
- [10. 清理资源](#10-清理资源)
- [11. 详细说明](#11-详细说明)
- [12. 许可证](#12-许可证-critical)
- [13. 联系方式](#13-联系方式-critical)

---

## 3. 架构图

```
                                    ┌─────────────────┐
                                    │   用户/浏览器    │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │     APIG        │
                                    │   (API 网关)    │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  CCE (容器集群) │
                                    │   (后端服务)    │
                                    └────────┬────────┘
                                             │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
           ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
           │   CSS           │    │   ModelArts     │    │   盘古/MaaS    │
           │  (向量搜索)     │    │   (嵌入模型)   │    │   (大模型)      │
           └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 技术架构

| 组件 | 华为云服务 | 说明 |
|------|-----------|------|
| API 网关 | APIG | RESTful 接口 |
| 后端服务 | CCE | 容器化部署 |
| 向量搜索 | CSS | 全文与向量检索 |
| 嵌入模型 | ModelArts | 文本向量化 |
| 大语言模型 | 盘古/MaaS | 生成式 AI |

---

## 4. 方案亮点

- **高性能**: 向量检索毫秒级响应
- **弹性伸缩**: 容器自动伸缩，按需使用
- **易扩展**: CCE 弹性伸缩
- **安全可靠**: IAM 权限控制，数据加密

---

## 5. 涉及云服务

| 服务 | 用途 |
|------|------|
| APIG | API 网关 |
| CCE | 后端计算（容器化） |
| CSS | 向量与全文搜索 |
| ModelArts | 嵌入模型部署 |
| 盘古/MaaS | 大语言模型 |

---

## 6. 前置条件 [CRITICAL]

- 华为云账号（已实名认证）
- IAM 用户具备以下权限：
  - CSS FullAccess
  - CCE FullAccess
  - APIG FullAccess
  - IAM FullAccess
- 本地安装 Docker 和 kubectl

---

## 7. 快速开始 [CRITICAL]

### 分阶段部署

由于 CCE 集群创建后需要配置 kubectl，本方案采用两阶段部署：

**阶段 1: Terraform 部署基础设施**

```bash
# 克隆仓库
git clone <repository-url>
cd huaweicloud/semantic-search-with-amazon-opensearch

# 进入 infra 目录
cd infra

# 初始化
terraform init

# 复制配置
cp terraform.tfvars.example terraform.tfvars
# 编辑 terraform.tfvars 填入 backend_host (初始可设为任意 IP，后续更新)

# 规划
terraform plan

# 部署 (创建 VPC/CSS/CCE/APIG)
terraform apply
```

**阶段 2: 部署容器应用**

```bash
# 1. 构建镜像
cd ../src/backend
docker build -t semantic-search-backend:latest .

# 2. 推送到 SWR (必须)
docker tag semantic-search-backend:latest swr.cn-north-4.myhuaweicloud.com/your-namespace/semantic-search-backend:latest
docker push swr.cn-north-4.myhuaweicloud.com/your-namespace/semantic-search-backend:latest

# 3. 配置 kubectl
terraform output cce_endpoint  # 获取集群地址
terraform output cce_cluster_ca_cert  # 获取 CA 证书

# 4. 部署 Kubernetes 资源
cd ../../infra
kubectl apply -f k8s-deployment.yaml
```

---

## 8. 分步部署

### 步骤 1: 配置凭据

```bash
# 设置环境变量
export HW_ACCESS_KEY="your-access-key"
export HW_SECRET_KEY="your-secret-key"
export HW_REGION="cn-north-4"
```

### 步骤 2: 配置变量

```bash
# 复制示例配置
cp terraform.tfvars.example terraform.tfvars

# 编辑配置
vi terraform.tfvars
```

### 步骤 3: 初始化与部署

```bash
terraform init
terraform plan
terraform apply
```

### 步骤 4: 获取 CCE 集群凭证

```bash
# 获取集群凭证
terraform output cce_endpoint

# 配置 kubectl
kubectl config set-cluster cce --server=https://<cce_endpoint>
kubectl config set-credentials cce-user --token=<cce_token>
kubectl config set-context cce --cluster=cce --user=cce-user
kubectl config use-context cce
```

---

## 9. 使用方法 / 验证 [CRITICAL]

### 搜索示例

```bash
curl -X POST https://{apig-url}/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "如何申请营业执照",
    "top_k": 5
  }'
```

### RAG 对话

```bash
curl -X POST https://{apig-url}/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "公司变更法人需要什么材料"
  }'
```

### 健康检查

```bash
curl http://<cce-service-ip>/health
```

---

## 10. 清理资源

```bash
cd infra
terraform destroy
```

---

## 11. 详细说明

### 搜索流程

1. 用户发起搜索请求
2. APIG 接收请求
3. CCE 容器调用嵌入模型将查询向量化
4. 向量查询在 CSS 中进行相似度检索
5. 返回检索结果

### RAG 流程

1. 用户提问
2. 检索相关文档片段
3. 将片段作为上下文调用大模型
4. 生成回答

### 容器化优势

- **无服务器体验**: 无需管理服务器，按需伸缩
- **快速部署**: 镜像化交付，一键部署
- **资源隔离**: 每个服务独立容器
- **易于运维**: 日志、监控标准化

---

## 12. 许可证 [CRITICAL]

本项目基于 MIT No Attribution 许可证。

See [LICENSE](LICENSE) for details.

---

## 13. 联系方式 [CRITICAL]

**维护者**: Shangdongd

如有问题，请在 GitHub 提交 Issue。

---

*最后更新: 2026-09-14*
