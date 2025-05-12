# agentic-chatbot-aks with LangChain, FAISS, Redis, Delta Lake, Cosmos DB

## Features

- FastAPI backend for agentic chatbot
- FAISS with Milvus for vector search
- Redis 8.0 with vectorSet support as cache
- Delta Lake integration (Azure Data Lake Gen2)
- GPT-based RAG agent using LangChain
- Cosmos DB to store user request metadata
- Microsoft Teams bot interface with upvote/downvote feedback
- Prometheus & Grafana monitoring
- LangSmith for logging and tracing
- GitHub Actions CI/CD pipeline
- Bicep and Terraform deployment options

## Deployment Instructions

### Prerequisites

- Azure CLI
- Terraform or Bicep CLI
- kubectl
- Helm

### Bicep Deployment

```bash
az group create --name agentic-rg --location eastus
az deployment group create --resource-group agentic-rg --template-file infra/main.bicep
```

### Terraform Deployment

```bash
cd infra
terraform init
terraform apply
```

### Deploy to AKS

```bash
kubectl apply -f k8s/
helm upgrade --install agentic ./helm/
```

### Logs and Monitoring

- **LangSmith**: Configure environment variables for logging
- **Prometheus**: Default metrics exposed on `/metrics`
- **Grafana**: Use included dashboards to visualize vector usage, latency, feedback

## Evaluation

- Offline evaluation notebooks provided in `/evaluation`
- Online feedback via Teams (thumbs up/down) saved in CosmosDB and LangSmith

## CI/CD

- GitHub Actions pipeline provided in `.github/workflows/deploy.yml`