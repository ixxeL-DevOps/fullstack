"""
Cluster Orchestrator Service

This service coordinates the entire cluster provisioning process,
managing the interaction between Proxmox, Talos, Vault, and GitOps components.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from ..config import Settings
from ..models.cluster import (
    ClusterCreateRequest, 
    ClusterResponse, 
    ClusterStatus, 
    ClusterListItem,
    JobInfo,
    ProvisioningStep
)
from .proxmox import ProxmoxService
from .talos import TalosService
from .vault import VaultService
from .gitops import GitOpsService

logger = logging.getLogger(__name__)


class ClusterOrchestrator:
    """Orchestrates the complete cluster provisioning workflow"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.proxmox_service = ProxmoxService(settings)
        self.talos_service = TalosService(settings)
        self.vault_service = VaultService(settings)
        self.gitops_service = GitOpsService(settings)
        
        # Job tracking
        self.active_jobs: Dict[str, JobInfo] = {}
        self.job_storage_path = Path(settings.job_storage_path)
        self.log_storage_path = Path(settings.log_storage_path)
        
        # Ensure storage directories exist
        self.job_storage_path.mkdir(parents=True, exist_ok=True)
        self.log_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing jobs from storage
        self._load_existing_jobs()
    
    def _load_existing_jobs(self):
        """Load existing job information from persistent storage"""
        try:
            for job_file in self.job_storage_path.glob("*.json"):
                with open(job_file, 'r') as f:
                    job_data = json.load(f)
                    job_info = JobInfo(**job_data)
                    self.active_jobs[job_info.job_id] = job_info
            logger.info(f"Loaded {len(self.active_jobs)} existing jobs")
        except Exception as e:
            logger.error(f"Error loading existing jobs: {str(e)}")
    
    def _save_job_info(self, job_info: JobInfo):
        """Save job information to persistent storage"""
        try:
            job_file = self.job_storage_path / f"{job_info.job_id}.json"
            with open(job_file, 'w') as f:
                json.dump(job_info.dict(), f, default=str, indent=2)
        except Exception as e:
            logger.error(f"Error saving job info: {str(e)}")
    
    async def cluster_exists(self, cluster_name: str) -> bool:
        """Check if a cluster already exists"""
        try:
            # Check if VMs exist in Proxmox
            vms_exist = await self.proxmox_service.cluster_vms_exist(cluster_name)
            
            # Check if GitOps manifests exist
            gitops_exist = await self.gitops_service.cluster_manifests_exist(cluster_name)
            
            return vms_exist or gitops_exist
        except Exception as e:
            logger.error(f"Error checking if cluster exists: {str(e)}")
            return False
    
    async def start_cluster_provisioning(self, request: ClusterCreateRequest) -> str:
        """Start the cluster provisioning process"""
        job_id = str(uuid.uuid4())
        
        job_info = JobInfo(
            job_id=job_id,
            cluster_name=request.cluster_name,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            original_request=request,
            current_step="initializing",
            progress_percentage=0
        )
        
        self.active_jobs[job_id] = job_info
        self._save_job_info(job_info)
        
        logger.info(f"Started cluster provisioning job {job_id} for cluster {request.cluster_name}")
        return job_id
    
    async def provision_cluster_background(self, job_id: str, request: ClusterCreateRequest):
        """Background task to provision a cluster"""
        job_info = self.active_jobs.get(job_id)
        if not job_info:
            logger.error(f"Job {job_id} not found")
            return
        
        try:
            await self._provision_cluster(job_id, request)
        except Exception as e:
            logger.error(f"Error in cluster provisioning job {job_id}: {str(e)}")
            job_info.status = "failed"
            job_info.current_step = f"failed: {str(e)}"
            job_info.updated_at = datetime.utcnow()
            self._save_job_info(job_info)
    
    async def _provision_cluster(self, job_id: str, request: ClusterCreateRequest):
        """Execute the cluster provisioning workflow"""
        job_info = self.active_jobs[job_id]
        cluster_name = request.cluster_name
        
        steps = [
            ("Creating VMs in Proxmox", self._step_create_vms),
            ("Generating Talos configuration", self._step_generate_talos_config),
            ("Bootstrapping Talos cluster", self._step_bootstrap_talos),
            ("Storing secrets in Vault", self._step_store_secrets),
            ("Generating GitOps manifests", self._step_generate_gitops),
            ("Verifying cluster health", self._step_verify_cluster)
        ]
        
        total_steps = len(steps)
        
        for i, (step_name, step_func) in enumerate(steps):
            try:
                # Update job status
                job_info.current_step = step_name
                job_info.progress_percentage = int((i / total_steps) * 100)
                job_info.updated_at = datetime.utcnow()
                self._save_job_info(job_info)
                
                logger.info(f"Job {job_id}: Starting step '{step_name}'")
                
                # Execute the step
                await step_func(request)
                
                logger.info(f"Job {job_id}: Completed step '{step_name}'")
                
            except Exception as e:
                logger.error(f"Job {job_id}: Failed step '{step_name}': {str(e)}")
                job_info.status = "failed"
                job_info.current_step = f"failed at: {step_name}"
                job_info.updated_at = datetime.utcnow()
                self._save_job_info(job_info)
                raise
        
        # Mark job as completed
        job_info.status = "completed"
        job_info.current_step = "cluster ready"
        job_info.progress_percentage = 100
        job_info.updated_at = datetime.utcnow()
        self._save_job_info(job_info)
        
        logger.info(f"Job {job_id}: Cluster {cluster_name} provisioning completed successfully")
    
    async def _step_create_vms(self, request: ClusterCreateRequest):
        """Step 1: Create VMs in Proxmox"""
        await self.proxmox_service.create_cluster_vms(request)
    
    async def _step_generate_talos_config(self, request: ClusterCreateRequest):
        """Step 2: Generate Talos configuration"""
        await self.talos_service.generate_cluster_config(request)
    
    async def _step_bootstrap_talos(self, request: ClusterCreateRequest):
        """Step 3: Bootstrap Talos cluster"""
        await self.talos_service.bootstrap_cluster(request)
    
    async def _step_store_secrets(self, request: ClusterCreateRequest):
        """Step 4: Store cluster secrets in Vault"""
        await self.vault_service.store_cluster_secrets(request)
    
    async def _step_generate_gitops(self, request: ClusterCreateRequest):
        """Step 5: Generate GitOps manifests"""
        if request.enable_gitops:
            await self.gitops_service.generate_cluster_manifests(request)
    
    async def _step_verify_cluster(self, request: ClusterCreateRequest):
        """Step 6: Verify cluster health"""
        await self.talos_service.verify_cluster_health(request.cluster_name)
    
    async def get_cluster_status(self, cluster_name: str) -> ClusterResponse:
        """Get detailed status of a cluster"""
        # Find job for this cluster
        job_info = None
        for job in self.active_jobs.values():
            if job.cluster_name == cluster_name:
                job_info = job
                break
        
        if not job_info:
            raise ValueError(f"Cluster '{cluster_name}' not found")
        
        # Determine cluster status
        if job_info.status == "completed":
            status = ClusterStatus.READY
        elif job_info.status == "failed":
            status = ClusterStatus.FAILED
        elif "bootstrap" in job_info.current_step.lower():
            status = ClusterStatus.BOOTSTRAPPING
        elif "gitops" in job_info.current_step.lower():
            status = ClusterStatus.CONFIGURING
        else:
            status = ClusterStatus.PROVISIONING
        
        # Build response
        response = ClusterResponse(
            cluster_name=cluster_name,
            status=status,
            created_at=job_info.created_at,
            updated_at=job_info.updated_at,
            vmid_prefix=job_info.original_request.vmid_prefix,
            control_plane_nodes=job_info.original_request.control_plane_nodes,
            worker_nodes=job_info.original_request.worker_nodes,
            network_config=job_info.original_request.network_config,
            resource_config=job_info.original_request.resource_config or {},
            job_id=job_info.job_id,
            api_server_endpoint=f"https://{job_info.original_request.network_config.vip}:6443" if status == ClusterStatus.READY else None,
            kubeconfig_available=status == ClusterStatus.READY
        )
        
        return response
    
    async def list_clusters(self) -> List[ClusterListItem]:
        """List all known clusters"""
        clusters = []
        
        for job in self.active_jobs.values():
            if job.status == "completed":
                status = ClusterStatus.READY
            elif job.status == "failed":
                status = ClusterStatus.FAILED
            else:
                status = ClusterStatus.PROVISIONING
            
            clusters.append(ClusterListItem(
                cluster_name=job.cluster_name,
                status=status,
                created_at=job.created_at,
                control_plane_nodes=job.original_request.control_plane_nodes,
                worker_nodes=job.original_request.worker_nodes,
                api_server_endpoint=f"https://{job.original_request.network_config.vip}:6443" if status == ClusterStatus.READY else None
            ))
        
        return clusters
    
    async def start_cluster_deletion(self, cluster_name: str) -> str:
        """Start the cluster deletion process"""
        job_id = str(uuid.uuid4())
        
        job_info = JobInfo(
            job_id=job_id,
            cluster_name=cluster_name,
            status="deleting",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            current_step="preparing deletion",
            progress_percentage=0
        )
        
        self.active_jobs[job_id] = job_info
        self._save_job_info(job_info)
        
        return job_id
    
    async def delete_cluster_background(self, job_id: str, cluster_name: str):
        """Background task to delete a cluster"""
        job_info = self.active_jobs.get(job_id)
        if not job_info:
            logger.error(f"Deletion job {job_id} not found")
            return
        
        try:
            await self._delete_cluster(job_id, cluster_name)
        except Exception as e:
            logger.error(f"Error in cluster deletion job {job_id}: {str(e)}")
            job_info.status = "failed"
            job_info.current_step = f"deletion failed: {str(e)}"
            job_info.updated_at = datetime.utcnow()
            self._save_job_info(job_info)
    
    async def _delete_cluster(self, job_id: str, cluster_name: str):
        """Execute the cluster deletion workflow"""
        job_info = self.active_jobs[job_id]
        
        steps = [
            ("Removing GitOps manifests", lambda: self.gitops_service.remove_cluster_manifests(cluster_name)),
            ("Deleting VMs from Proxmox", lambda: self.proxmox_service.delete_cluster_vms(cluster_name)),
            ("Cleaning up Vault secrets", lambda: self.vault_service.cleanup_cluster_secrets(cluster_name)),
            ("Removing local configurations", lambda: self._cleanup_local_files(cluster_name))
        ]
        
        total_steps = len(steps)
        
        for i, (step_name, step_func) in enumerate(steps):
            try:
                job_info.current_step = step_name
                job_info.progress_percentage = int((i / total_steps) * 100)
                job_info.updated_at = datetime.utcnow()
                self._save_job_info(job_info)
                
                logger.info(f"Deletion job {job_id}: Starting step '{step_name}'")
                await step_func()
                logger.info(f"Deletion job {job_id}: Completed step '{step_name}'")
                
            except Exception as e:
                logger.error(f"Deletion job {job_id}: Failed step '{step_name}': {str(e)}")
                # Continue with other steps even if one fails
                continue
        
        # Mark deletion as completed
        job_info.status = "deleted"
        job_info.current_step = "cluster deleted"
        job_info.progress_percentage = 100
        job_info.updated_at = datetime.utcnow()
        self._save_job_info(job_info)
        
        logger.info(f"Deletion job {job_id}: Cluster {cluster_name} deletion completed")
    
    async def _cleanup_local_files(self, cluster_name: str):
        """Clean up local configuration files"""
        # Remove cluster-specific logs
        cluster_log_dir = self.log_storage_path / cluster_name
        if cluster_log_dir.exists():
            import shutil
            shutil.rmtree(cluster_log_dir)
    
    async def get_cluster_logs(self, cluster_name: str, lines: int = 100) -> List[str]:
        """Get provisioning logs for a cluster"""
        log_file = self.log_storage_path / f"{cluster_name}.log"
        
        if not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r') as f:
                all_lines = f.readlines()
                return [line.strip() for line in all_lines[-lines:]]
        except Exception as e:
            logger.error(f"Error reading logs for cluster {cluster_name}: {str(e)}")
            return []
    
    async def get_original_request(self, cluster_name: str) -> ClusterCreateRequest:
        """Get the original provisioning request for a cluster"""
        for job in self.active_jobs.values():
            if job.cluster_name == cluster_name and job.original_request:
                return job.original_request
        
        raise ValueError(f"Original request for cluster '{cluster_name}' not found")
