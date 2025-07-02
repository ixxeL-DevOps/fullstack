"""Pydantic models for cluster management"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class ClusterStatus(str, Enum):
    """Cluster status enumeration"""
    PENDING = "pending"
    PROVISIONING = "provisioning"
    BOOTSTRAPPING = "bootstrapping"
    CONFIGURING = "configuring"
    READY = "ready"
    FAILED = "failed"
    DELETING = "deleting"
    DELETED = "deleted"


class NetworkConfig(BaseModel):
    """Network configuration for cluster"""
    vip: str = Field(..., description="Virtual IP for control plane HA")
    node_ips: List[str] = Field(..., description="IP addresses for cluster nodes")
    pod_cidr: str = Field(default="10.244.0.0/16", description="Pod CIDR range")
    service_cidr: str = Field(default="10.96.0.0/12", description="Service CIDR range")
    dns_servers: Optional[List[str]] = Field(default=["8.8.8.8", "8.8.4.4"], description="DNS servers")
    
    @validator('node_ips')
    def validate_node_ips(cls, v):
        if len(v) < 1:
            raise ValueError('At least one node IP is required')
        return v


class ResourceConfig(BaseModel):
    """Resource configuration for VMs"""
    cpu_cores: int = Field(default=4, ge=2, le=32, description="CPU cores per VM")
    memory_gb: int = Field(default=8, ge=4, le=64, description="Memory per VM in GB")
    storage_gb: int = Field(default=100, ge=50, le=1000, description="Storage per VM in GB")


class ProxmoxConfig(BaseModel):
    """Proxmox-specific configuration"""
    node: Optional[str] = Field(default=None, description="Proxmox node name")
    storage: str = Field(default="local-lvm", description="Storage pool name")
    bridge: str = Field(default="vmbr0", description="Network bridge")
    
    
class TalosConfig(BaseModel):
    """Talos-specific configuration"""
    version: str = Field(default="v1.6.0", description="Talos version")
    install_disk: str = Field(default="/dev/sda", description="Installation disk")
    registry_mirrors: Optional[Dict[str, Any]] = Field(default=None, description="Container registry mirrors")


class ClusterCreateRequest(BaseModel):
    """Request model for creating a new cluster"""
    cluster_name: str = Field(..., min_length=3, max_length=32, description="Cluster name")
    vmid_prefix: int = Field(..., ge=10, le=999, description="VMID prefix for VMs")
    control_plane_nodes: int = Field(default=3, ge=1, le=7, description="Number of control plane nodes")
    worker_nodes: int = Field(default=2, ge=0, le=20, description="Number of worker nodes")
    
    network_config: NetworkConfig
    resource_config: Optional[ResourceConfig] = Field(default_factory=ResourceConfig)
    proxmox_config: Optional[ProxmoxConfig] = Field(default_factory=ProxmoxConfig)
    talos_config: Optional[TalosConfig] = Field(default_factory=TalosConfig)
    
    # GitOps configuration
    enable_gitops: bool = Field(default=True, description="Enable GitOps manifest generation")
    applications: Optional[List[str]] = Field(default=None, description="Applications to deploy")
    
    @validator('cluster_name')
    def validate_cluster_name(cls, v):
        import re
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Cluster name must contain only lowercase letters, numbers, and hyphens')
        return v
    
    @validator('applications')
    def validate_applications(cls, v):
        if v is None:
            return ["cert-manager", "external-secrets", "ingress-nginx", "metallb"]
        return v


class ProvisioningStep(BaseModel):
    """Individual provisioning step"""
    name: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    logs: Optional[List[str]] = Field(default_factory=list)


class ClusterResponse(BaseModel):
    """Response model for cluster information"""
    cluster_name: str
    status: ClusterStatus
    created_at: datetime
    updated_at: datetime
    
    # Configuration
    vmid_prefix: int
    control_plane_nodes: int
    worker_nodes: int
    network_config: NetworkConfig
    resource_config: ResourceConfig
    
    # Status information
    job_id: Optional[str] = None
    provisioning_steps: Optional[List[ProvisioningStep]] = Field(default_factory=list)
    error_message: Optional[str] = None
    
    # Kubernetes information
    kubeconfig_available: bool = False
    api_server_endpoint: Optional[str] = None
    
    # GitOps information
    git_branch: Optional[str] = None
    argocd_applications: Optional[List[str]] = Field(default_factory=list)


class ClusterListItem(BaseModel):
    """Simplified cluster information for listing"""
    cluster_name: str
    status: ClusterStatus
    created_at: datetime
    control_plane_nodes: int
    worker_nodes: int
    api_server_endpoint: Optional[str] = None


class ClusterStatusResponse(BaseModel):
    """Detailed status response for a cluster"""
    cluster: ClusterResponse
    nodes: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    pods: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    services: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class JobInfo(BaseModel):
    """Information about a provisioning job"""
    job_id: str
    cluster_name: str
    status: str
    created_at: datetime
    updated_at: datetime
    original_request: Optional[ClusterCreateRequest] = None
    current_step: Optional[str] = None
    progress_percentage: Optional[int] = None
    estimated_completion: Optional[datetime] = None
