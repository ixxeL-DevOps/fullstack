#!/usr/bin/env python3
"""
Kubernetes Cluster Provisioning Service

This FastAPI service automates the creation of new Kubernetes clusters
following the genmachine pattern, including:
- Proxmox VM provisioning
- Talos cluster bootstrap
- Vault secret storage
- GitOps manifest generation
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .models.cluster import ClusterCreateRequest, ClusterResponse, ClusterStatus
from .models.responses import StandardResponse, StatusResponse
from .services.cluster_orchestrator import ClusterOrchestrator
from .utils.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global cluster orchestrator
cluster_orchestrator: ClusterOrchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI application"""
    global cluster_orchestrator
    
    settings = get_settings()
    cluster_orchestrator = ClusterOrchestrator(settings)
    
    logger.info("Cluster Provisioning Service started")
    yield
    
    logger.info("Cluster Provisioning Service shutting down")


# Create FastAPI application
app = FastAPI(
    title="Kubernetes Cluster Provisioning Service",
    description="Automated provisioning of Kubernetes clusters using Talos Linux and GitOps",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_orchestrator() -> ClusterOrchestrator:
    """Dependency to get the cluster orchestrator"""
    if cluster_orchestrator is None:
        raise HTTPException(status_code=503, detail="Service not ready")
    return cluster_orchestrator


@app.get("/", response_model=StandardResponse)
async def root():
    """Root endpoint with service information"""
    return StandardResponse(
        success=True,
        message="Kubernetes Cluster Provisioning Service",
        data={
            "version": "1.0.0",
            "status": "healthy"
        }
    )


@app.get("/health", response_model=StatusResponse)
async def health_check():
    """Health check endpoint"""
    return StatusResponse(
        status="healthy",
        timestamp="",  # Will be set by the model
        details={
            "service": "cluster-provisioning",
            "version": "1.0.0"
        }
    )


@app.post("/api/v1/clusters", response_model=StandardResponse)
async def create_cluster(
    request: ClusterCreateRequest,
    background_tasks: BackgroundTasks,
    orchestrator: ClusterOrchestrator = Depends(get_orchestrator)
):
    """
    Create a new Kubernetes cluster
    
    This endpoint initiates the cluster provisioning process:
    1. Validates the request
    2. Starts background provisioning task
    3. Returns immediately with provisioning job ID
    """
    try:
        # Validate cluster name doesn't already exist
        if await orchestrator.cluster_exists(request.cluster_name):
            raise HTTPException(
                status_code=409,
                detail=f"Cluster '{request.cluster_name}' already exists"
            )
        
        # Start provisioning process in background
        job_id = await orchestrator.start_cluster_provisioning(request)
        
        # Add background task to monitor provisioning
        background_tasks.add_task(
            orchestrator.provision_cluster_background,
            job_id,
            request
        )
        
        return StandardResponse(
            success=True,
            message=f"Cluster provisioning started for '{request.cluster_name}'",
            data={
                "cluster_name": request.cluster_name,
                "job_id": job_id,
                "status": "provisioning"
            }
        )
        
    except Exception as e:
        logger.error(f"Error creating cluster {request.cluster_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/clusters/{cluster_name}/status", response_model=StandardResponse)
async def get_cluster_status(
    cluster_name: str,
    orchestrator: ClusterOrchestrator = Depends(get_orchestrator)
):
    """Get the status of a cluster provisioning job or existing cluster"""
    try:
        status = await orchestrator.get_cluster_status(cluster_name)
        return StandardResponse(
            success=True,
            message=f"Status for cluster '{cluster_name}'",
            data=status.dict()
        )
        
    except Exception as e:
        logger.error(f"Error getting status for cluster {cluster_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/clusters", response_model=StandardResponse)
async def list_clusters(
    orchestrator: ClusterOrchestrator = Depends(get_orchestrator)
):
    """List all known clusters and their statuses"""
    try:
        clusters = await orchestrator.list_clusters()
        return StandardResponse(
            success=True,
            message="List of all clusters",
            data={"clusters": clusters}
        )
        
    except Exception as e:
        logger.error(f"Error listing clusters: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/clusters/{cluster_name}", response_model=StandardResponse)
async def delete_cluster(
    cluster_name: str,
    background_tasks: BackgroundTasks,
    orchestrator: ClusterOrchestrator = Depends(get_orchestrator)
):
    """
    Delete a cluster and cleanup all resources
    
    This endpoint initiates the cluster deletion process:
    1. Validates the cluster exists
    2. Starts background deletion task
    3. Returns immediately with deletion job ID
    """
    try:
        if not await orchestrator.cluster_exists(cluster_name):
            raise HTTPException(
                status_code=404,
                detail=f"Cluster '{cluster_name}' not found"
            )
        
        # Start deletion process in background
        job_id = await orchestrator.start_cluster_deletion(cluster_name)
        
        # Add background task to perform deletion
        background_tasks.add_task(
            orchestrator.delete_cluster_background,
            job_id,
            cluster_name
        )
        
        return StandardResponse(
            success=True,
            message=f"Cluster deletion started for '{cluster_name}'",
            data={
                "cluster_name": cluster_name,
                "job_id": job_id,
                "status": "deleting"
            }
        )
        
    except Exception as e:
        logger.error(f"Error deleting cluster {cluster_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/clusters/{cluster_name}/logs", response_model=StandardResponse)
async def get_cluster_logs(
    cluster_name: str,
    lines: int = 100,
    orchestrator: ClusterOrchestrator = Depends(get_orchestrator)
):
    """Get provisioning logs for a cluster"""
    try:
        logs = await orchestrator.get_cluster_logs(cluster_name, lines)
        return StandardResponse(
            success=True,
            message=f"Logs for cluster '{cluster_name}'",
            data={"logs": logs}
        )
        
    except Exception as e:
        logger.error(f"Error getting logs for cluster {cluster_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/v1/clusters/{cluster_name}/retry", response_model=StandardResponse)
async def retry_cluster_provisioning(
    cluster_name: str,
    background_tasks: BackgroundTasks,
    orchestrator: ClusterOrchestrator = Depends(get_orchestrator)
):
    """Retry failed cluster provisioning"""
    try:
        status = await orchestrator.get_cluster_status(cluster_name)
        
        if status.status != ClusterStatus.FAILED:
            raise HTTPException(
                status_code=400,
                detail=f"Cluster '{cluster_name}' is not in failed state"
            )
        
        # Get original request from job history
        original_request = await orchestrator.get_original_request(cluster_name)
        
        # Start new provisioning process
        job_id = await orchestrator.start_cluster_provisioning(original_request)
        
        background_tasks.add_task(
            orchestrator.provision_cluster_background,
            job_id,
            original_request
        )
        
        return StandardResponse(
            success=True,
            message=f"Cluster provisioning retry started for '{cluster_name}'",
            data={
                "cluster_name": cluster_name,
                "job_id": job_id,
                "status": "provisioning"
            }
        )
        
    except Exception as e:
        logger.error(f"Error retrying cluster {cluster_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
