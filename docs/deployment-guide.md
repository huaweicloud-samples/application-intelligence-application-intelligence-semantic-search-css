# 部署指南

## 1. 前置条件

### 1.1 账号要求
- 华为云账号（已实名认证）
- IAM 用户或委托权限

### 1.2 权限要求
创建 IAM 委托或用户，需具备以下权限：
- CSS FullAccess
- FunctionGraph FullAccess
- APIG FullAccess
- VPC FullAccess
- ELB FullAccess
- CES FullAccess（可选，监控）

### 1.3 环境准备
```bash
# 安装 Terraform
# 参考: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

# 安装华为云 Terraform Provider
terraform init
```

## 2. 配置步骤

### 2.1 配置凭据
```bash
# 方式一：环境变量
export HW_ACCESS_KEY="your-access-key"
export HW_SECRET_KEY="your-secret-key"
export HW_REGION="cn-north-4"

# 方式二：配置文件
# 在 infra 目录下创建 terraform.tfvars
```

### 2.2 复制配置模板
```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
```

### 2.3 编辑配置
编辑 `terraform.tfvars`，配置以下参数：
```hcl
project_name = "semantic-search"
apig_instance_name = "semantic-search-apig"
css_cluster_name = "semantic-search-css"
function_package_name = "semantic-search-pkg"
```

## 3. 部署步骤

### 3.1 初始化
```bash
terraform init
```

### 3.2 规划预览
```bash
terraform plan
```
确认将要创建的资源：
- VPC 及子网
- 安全组
- CSS 集群
- APIG 实例及 API 分组
- FunctionGraph 函数

### 3.3 执行部署
```bash
terraform apply
```
输入 `yes` 确认部署。

### 3.4 验证部署
```bash
# 查看输出
terraform output

# 测试 API
curl -X GET "https://${apig_endpoint}/health"
```

## 4. 索引构建

### 4.1 准备文档
将待搜索的文档整理为 JSON 格式：
```json
[
  {"id": "1", "content": "企业营业执照办理流程...", "title": "营业执照"},
  {"id": "2", "content": "税务申报时间规定...", "title": "税务申报"}
]
```

### 4.2 调用索引 API
```bash
curl -X POST "https://${apig_endpoint}/index" \
  -H "Content-Type: application/json" \
  -d @documents.json
```

## 5. 搜索测试

### 5.1 关键词搜索
```bash
curl -X POST "https://${apig_endpoint}/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "如何办理营业执照",
    "top_k": 5,
    "search_type": "keyword"
  }'
```

### 5.2 向量搜索
```bash
curl -X POST "https://${apig_endpoint}/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "我想注册一个公司需要什么材料",
    "top_k": 5,
    "search_type": "vector"
  }'
```

### 5.3 混合搜索
```bash
curl -X POST "https://${apig_endpoint}/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "公司法人变更流程",
    "top_k": 5,
    "search_type": "hybrid"
  }'
```

### 5.4 RAG 对话
```bash
curl -X POST "https://${apig_endpoint}/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "新公司注册需要准备哪些材料？"
  }'
```

## 6. 清理资源

### 6.1 销毁资源
```bash
terraform destroy
```
输入 `yes` 确认销毁。

### 6.2 手动检查
登录华为云控制台，确认以下资源已释放：
- CSS 集群
- APIG 实例
- FunctionGraph 函数
- VPC/安全组

## 7. 故障排查

### 7.1 部署失败
- 检查凭据是否正确
- 检查区域资源配额
- 查看 Terraform 日志

### 7.2 API 调用失败
- 检查 APIG 是否部署完成
- 验证 FunctionGraph 函数日志
- 检查 CSS 集群状态

### 7.3 向量搜索无结果
- 确认文档已索引
- 检查 embedding 模型是否正常
