# Semantic Search Solution

> Semantic search implementation on Huawei Cloud with vector search and RAG support

<!-- 章节 1: 标题与徽章 [CRITICAL] -->
[![License](https://img.shields.io/badge/License-MIT%20No%20Attribution-blue.svg)](LICENSE)
[![Huawei Cloud](https://img.shields.io/badge/Huawei%20Cloud-Search-red.svg)](https://www.huaweicloud.com/)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](#)

---

## 1. Introduction [CRITICAL]

This practice provides a semantic search solution on Huawei Cloud, supporting traditional keyword search (BM25), vector-based semantic search, and Retrieval Augmented Generation (RAG). It serves as a reference architecture for enterprise knowledge bases and intelligent Q&A systems.

### Core Capabilities

- Vector semantic search
- Full-text search
- RAG retrieval augmentation
- Conversational search
- Fine-tuned model integration

---

## 2. Table of Contents

- [1. Introduction](#1-introduction-critical)
- [2. Table of Contents](#2-table-of-contents)
- [3. Architecture](#3-architecture)
- [4. Key Features](#4-key-features)
- [5. Cloud Services](#5-cloud-services)
- [6. Prerequisites](#6-prerequisites-critical)
- [7. Quick Start](#7-quick-start-critical)
- [8. Step-by-Step Deployment](#8-step-by-step-deployment)
- [9. Usage](#9-usage--verification-critical)
- [10. Cleanup](#10-cleanup-resources)
- [11. Details](#11-details)
- [12. License](#12-license-critical)
- [13. Contact](#13-contact-critical)

---

## 3. Architecture

```
                                    ┌─────────────────┐
                                    │   User/Browser  │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │     APIG        │
                                    │  (API Gateway) │
                                    └────────┬────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  CCE (Container)│
                                    │  (Backend)     │
                                    └────────┬────────┘
                                             │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
                    ▼                          ▼                          ▼
           ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
           │   CSS           │    │   ModelArts     │    │   PanGu/MaaS   │
           │ (Vector Search)│    │ (Embedding)    │    │   (LLM)        │
           └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

| Component | Huawei Cloud Service | Description |
|-----------|-------------------|-------------|
| API Gateway | APIG | RESTful API |
| Backend | CCE | Containerized deployment |
| Vector Search | CSS | Full-text & vector search |
| Embedding Model | ModelArts | Text vectorization |
| LLM | PanGu/MaaS | Generative AI |

---

## 4. Key Features

- **High Performance**: Millisecond-level vector search response
- **Low Cost**: Pay-as-you-go, auto-scaling containers
- **Easy Scaling**: CCE elastic scaling
- **Secure**: IAM access control, data encryption

---

## 5. Cloud Services

| Service | Usage |
|---------|-------|
| APIG | API Gateway |
| CCE | Backend compute (containerized) |
| CSS | Vector & full-text search |
| ModelArts | Embedding model deployment |
| PanGu/MaaS | Large language model |

---

## 6. Prerequisites [CRITICAL]

- Huawei Cloud account (with billing enabled)
- IAM user with permissions:
  - CSS FullAccess
  - CCE FullAccess
  - APIG FullAccess
  - IAM FullAccess
- Docker and kubectl installed locally

---

## 7. Quick Start [CRITICAL]

### One-Click Deployment

```bash
# Clone repository
git clone <repository-url>
cd huaweicloud/semantic-search-with-amazon-opensearch

# Enter infra directory
cd infra

# Initialize
terraform init

# Plan
terraform plan

# Deploy
terraform apply
```

### Build Container Image

```bash
# Enter backend directory
cd ../src/backend

# Build image
docker build -t semantic-search-backend:latest .

# Push to SWR (optional)
docker tag semantic-search-backend:latest swr.cn-north-4.myhuaweicloud.com/your-namespace/semantic-search-backend:latest
docker push swr.cn-north-4.myhuweiicloud.com/your-namespace/semantic-search-backend:latest
```

---

## 8. Step-by-Step Deployment

### Step 1: Configure Credentials

```bash
# Set environment variables
export HW_ACCESS_KEY="your-access-key"
export HW_SECRET_KEY="your-secret-key"
export HW_REGION="cn-north-4"
```

### Step 2: Configure Variables

```bash
# Copy example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit configuration
vi terraform.tfvars
```

### Step 3: Initialize and Deploy

```bash
terraform init
terraform plan
terraform apply
```

### Step 4: Get CCE Cluster Credentials

```bash
# Get cluster endpoint
terraform output cce_endpoint

# Configure kubectl
kubectl config set-cluster cce --server=https://<cce_endpoint>
kubectl config set-credentials cce-user --token=<cce_token>
kubectl config set-context cce --cluster=cce --user=cce-user
kubectl config use-context cce
```

---

## 9. Usage / Verification [CRITICAL]

### Search Example

```bash
curl -X POST https://{apig-url}/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how to apply for business license",
    "top_k": 5
  }'
```

### RAG Chat

```bash
curl -X POST https://{apig-url}/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "what documents needed for company legal representative change"
  }'
```

### Health Check

```bash
curl http://<cce-service-ip>/health
```

---

## 10. Cleanup Resources

```bash
cd infra
terraform destroy
```

---

## 11. Details

### Search Flow

1. User initiates search request
2. APIG receives request
3. CCE container calls embedding model to vectorize query
4. Vector similarity search in CSS
5. Return search results

### RAG Flow

1. User asks question
2. Retrieve relevant document chunks
3. Use chunks as context for LLM
4. Generate answer

### Containerization Benefits

- **Serverless Experience**: No server management, on-demand scaling
- **Fast Deployment**: Image-based delivery, one-click deploy
- **Resource Isolation**: Each service in separate container
- **Easy Operations**: Standardized logging and monitoring

---

## 12. License [CRITICAL]

This project is licensed under MIT No Attribution.

See [LICENSE](LICENSE) for details.

---

## 13. Contact [CRITICAL]

**Maintainer**: Shangdongd

For issues, please submit a GitHub Issue.

---

*Last updated: 2026-09-14*
