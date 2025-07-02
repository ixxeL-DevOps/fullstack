"""Configuration settings for the cluster provisioning service"""

import os
from functools import lru_cache
from typing import Optional, List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Proxmox configuration
    proxmox_host: str = Field(..., description="Proxmox VE hostname/IP")
    proxmox_user: str = Field(..., description="Proxmox username")
    proxmox_password: str = Field(..., description="Proxmox password")
    proxmox_node: str = Field(..., description="Proxmox node name")
    proxmox_verify_ssl: bool = Field(default=False, description="Verify SSL for Proxmox")
    
    # Talos configuration
    talos_iso_path: str = Field(..., description="Path to Talos ISO file")
    talos_version: str = Field(default="v1.6.0", description="Talos version")
    
    # Vault configuration
    vault_url: str = Field(..., description="Vault server URL")
    vault_token: Optional[str] = Field(default=None, description="Vault token")
    vault_role_id: Optional[str] = Field(default=None, description="Vault AppRole role ID")
    vault_secret_id: Optional[str] = Field(default=None, description="Vault AppRole secret ID")
    vault_mount_point: str = Field(default="admin", description="Vault mount point")
    
    # Git configuration
    git_repo_path: str = Field(..., description="Path to GitOps repository")
    git_branch_prefix: str = Field(default="feature/cluster-", description="Git branch prefix for new clusters")
    git_commit_author_name: str = Field(default="Cluster Provisioning Service", description="Git commit author name")
    git_commit_author_email: str = Field(default="cluster-provisioning@example.com", description="Git commit author email")
    
    # Cluster defaults
    default_vmid_prefix: int = Field(default=50, description="Default VMID prefix for new clusters")
    default_cpu_cores: int = Field(default=4, description="Default CPU cores per VM")
    default_memory_gb: int = Field(default=8, description="Default memory per VM in GB")
    default_storage_gb: int = Field(default=100, description="Default storage per VM in GB")
    default_control_plane_nodes: int = Field(default=3, description="Default number of control plane nodes")
    default_worker_nodes: int = Field(default=2, description="Default number of worker nodes")
    
    # Network defaults
    default_pod_cidr: str = Field(default="10.244.0.0/16", description="Default pod CIDR")
    default_service_cidr: str = Field(default="10.96.0.0/12", description="Default service CIDR")
    
    # Storage configuration
    job_storage_path: str = Field(default="/tmp/cluster-jobs", description="Path to store job information")
    log_storage_path: str = Field(default="/tmp/cluster-logs", description="Path to store cluster logs")
    
    # Task execution
    task_timeout: int = Field(default=3600, description="Task timeout in seconds")
    max_concurrent_jobs: int = Field(default=3, description="Maximum concurrent provisioning jobs")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=8001, description="Metrics server port")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Environment-specific settings
def get_development_settings() -> Settings:
    """Get development-specific settings"""
    settings = get_settings()
    settings.debug = True
    settings.proxmox_verify_ssl = False
    return settings


def get_production_settings() -> Settings:
    """Get production-specific settings"""
    settings = get_settings()
    settings.debug = False
    settings.proxmox_verify_ssl = True
    return settings
