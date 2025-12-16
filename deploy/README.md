# Backend Deployment Guide

## 🚀 Run locally with Docker
```bash
docker build -t rag-backend -f deploy/Dockerfile .
docker run -p 8000:8000 rag-backend
