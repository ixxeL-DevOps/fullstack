"""
Proxmox Service

Handles VM creation, configuration, and management in Proxmox VE
"""

import asyncio
import logging
from typing import List, Dict, Any

from proxmoxer import ProxmoxAPI
from ..config import Settings
from ..models.cluster import ClusterCreateRequest

logger = logging.getLogger(__name__)


class ProxmoxService:
    """Service for managing Proxmox VE operations"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.proxmox = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize connection to Proxmox VE"""
        try:
            self.proxmox = ProxmoxAPI(
                self.settings.proxmox_host,
                user=self.settings.proxmox_user,
                password=self.settings.proxmox_password,
                verify_ssl=self.settings.proxmox_verify_ssl
            )
            logger.info(f"Connected to Proxmox VE at {self.settings.proxmox_host}")
        except Exception as e:
            logger.error(f"Failed to connect to Proxmox VE: {str(e)}")
            raise
    
    async def cluster_vms_exist(self, cluster_name: str) -> bool:
        """Check if VMs for a cluster already exist"""
        try:
            vms = self.proxmox.nodes(self.settings.proxmox_node).qemu.get()
            cluster_vms = [vm for vm in vms if cluster_name in vm.get('name', '')]
            return len(cluster_vms) > 0
        except Exception as e:
            logger.error(f"Error checking if cluster VMs exist: {str(e)}")
            return False
    
    async def create_cluster_vms(self, request: ClusterCreateRequest):
        """Create VMs for a new cluster"""
        cluster_name = request.cluster_name
        logger.info(f"Creating VMs for cluster {cluster_name}")
        
        # Generate VM configurations
        vm_configs = self._generate_vm_configs(request)
        
        # Create VMs
        created_vms = []
        try:
            for config in vm_configs:
                vmid = config['vmid']
                logger.info(f"Creating VM {vmid} ({config['name']})")
                
                # Create VM
                await self._create_vm(config)
                created_vms.append(vmid)
                
                # Configure network
                await self._configure_vm_network(vmid, config)
                
                # Set boot order and other settings
                await self._configure_vm_settings(vmid, config)
                
                logger.info(f"Successfully created VM {vmid}")
            
            logger.info(f"Successfully created {len(created_vms)} VMs for cluster {cluster_name}")
            
        except Exception as e:
            logger.error(f"Error creating VMs: {str(e)}")
            # Cleanup any VMs that were created
            await self._cleanup_vms(created_vms)
            raise
    
    def _generate_vm_configs(self, request: ClusterCreateRequest) -> List[Dict[str, Any]]:
        """Generate VM configurations based on cluster request"""
        configs = []
        vmid_base = request.vmid_prefix * 10
        
        # Control plane nodes
        for i in range(request.control_plane_nodes):
            vmid = vmid_base + i + 1
            ip_index = i
            
            config = {
                'vmid': vmid,
                'name': f"{request.cluster_name}-cp-{i+1}",
                'node_type': 'control-plane',
                'ip_address': request.network_config.node_ips[ip_index],
                'cpu_cores': request.resource_config.cpu_cores,
                'memory_gb': request.resource_config.memory_gb,
                'storage_gb': request.resource_config.storage_gb,
                'mac_address': self._generate_mac_address(vmid)
            }
            configs.append(config)
        
        # Worker nodes
        for i in range(request.worker_nodes):
            vmid = vmid_base + request.control_plane_nodes + i + 1
            ip_index = request.control_plane_nodes + i
            
            config = {
                'vmid': vmid,
                'name': f"{request.cluster_name}-wk-{i+1}",
                'node_type': 'worker',
                'ip_address': request.network_config.node_ips[ip_index],
                'cpu_cores': request.resource_config.cpu_cores,
                'memory_gb': request.resource_config.memory_gb,
                'storage_gb': request.resource_config.storage_gb,
                'mac_address': self._generate_mac_address(vmid)
            }
            configs.append(config)
        
        return configs
    
    def _generate_mac_address(self, vmid: int) -> str:
        """Generate a MAC address for a VM"""
        # Generate a MAC address based on VMID
        # This is a simple implementation - in production you might want
        # to use a more sophisticated approach
        mac_suffix = f"{vmid:04x}"
        return f"52:54:00:12:{mac_suffix[:2]}:{mac_suffix[2:]}"
    
    async def _create_vm(self, config: Dict[str, Any]):
        """Create a single VM in Proxmox"""
        try:
            # VM creation parameters
            vm_params = {
                'vmid': config['vmid'],
                'name': config['name'],
                'memory': config['memory_gb'] * 1024,  # Convert to MB
                'cores': config['cpu_cores'],
                'sockets': 1,
                'cpu': 'host',
                'ostype': 'l26',  # Linux 2.6+ kernel
                'boot': 'order=scsi0;ide2;net0',
                'scsihw': 'virtio-scsi-pci',
                'ide2': f"{self.settings.talos_iso_path},media=cdrom",
                'scsi0': f"{self.settings.proxmox_config.storage}:{config['storage_gb']},format=raw",
                'net0': f"virtio,bridge={self.settings.proxmox_config.bridge},macaddr={config['mac_address']}",
                'agent': 1,
                'onboot': 1
            }
            
            # Create the VM
            task = self.proxmox.nodes(self.settings.proxmox_node).qemu.create(**vm_params)
            
            # Wait for task completion
            await self._wait_for_task(task)
            
        except Exception as e:
            logger.error(f"Error creating VM {config['vmid']}: {str(e)}")
            raise
    
    async def _configure_vm_network(self, vmid: int, config: Dict[str, Any]):
        """Configure VM network settings"""
        # Network configuration is typically done via cloud-init or post-boot scripts
        # For Talos, this will be handled by the Talos configuration
        pass
    
    async def _configure_vm_settings(self, vmid: int, config: Dict[str, Any]):
        """Configure additional VM settings"""
        try:
            # Set description
            description = f"Talos {config['node_type']} node for cluster {config['name'].split('-')[0]}"
            
            self.proxmox.nodes(self.settings.proxmox_node).qemu(vmid).config.put(
                description=description
            )
            
        except Exception as e:
            logger.error(f"Error configuring VM {vmid}: {str(e)}")
            # Non-critical error, continue
    
    async def _wait_for_task(self, task_id: str, timeout: int = 300):
        """Wait for a Proxmox task to complete"""
        start_time = asyncio.get_event_loop().time()
        
        while True:
            try:
                task_status = self.proxmox.nodes(self.settings.proxmox_node).tasks(task_id).status.get()
                
                if task_status['status'] == 'stopped':
                    if task_status.get('exitstatus') == 'OK':
                        return
                    else:
                        raise Exception(f"Task failed: {task_status.get('exitstatus')}")
                
                # Check timeout
                if asyncio.get_event_loop().time() - start_time > timeout:
                    raise Exception(f"Task timeout after {timeout} seconds")
                
                # Wait before checking again
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error waiting for task {task_id}: {str(e)}")
                raise
    
    async def _cleanup_vms(self, vmids: List[int]):
        """Clean up VMs in case of error during creation"""
        for vmid in vmids:
            try:
                logger.info(f"Cleaning up VM {vmid}")
                task = self.proxmox.nodes(self.settings.proxmox_node).qemu(vmid).delete()
                await self._wait_for_task(task)
            except Exception as e:
                logger.error(f"Error cleaning up VM {vmid}: {str(e)}")
    
    async def delete_cluster_vms(self, cluster_name: str):
        """Delete all VMs for a cluster"""
        try:
            vms = self.proxmox.nodes(self.settings.proxmox_node).qemu.get()
            cluster_vms = [vm for vm in vms if cluster_name in vm.get('name', '')]
            
            for vm in cluster_vms:
                vmid = vm['vmid']
                logger.info(f"Deleting VM {vmid} ({vm.get('name')})")
                
                # Stop VM if running
                if vm.get('status') == 'running':
                    stop_task = self.proxmox.nodes(self.settings.proxmox_node).qemu(vmid).status.stop.post()
                    await self._wait_for_task(stop_task)
                
                # Delete VM
                delete_task = self.proxmox.nodes(self.settings.proxmox_node).qemu(vmid).delete()
                await self._wait_for_task(delete_task)
                
                logger.info(f"Successfully deleted VM {vmid}")
            
            logger.info(f"Successfully deleted {len(cluster_vms)} VMs for cluster {cluster_name}")
            
        except Exception as e:
            logger.error(f"Error deleting cluster VMs: {str(e)}")
            raise
