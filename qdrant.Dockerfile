FROM qdrant/qdrant:latest

# Cloud Run benötigt Port 8080
ENV QDRANT__SERVICE__HTTP_PORT=8080
ENV QDRANT__SERVICE__GRPC_PORT=6334

# Expose ports
EXPOSE 8080 6334

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
