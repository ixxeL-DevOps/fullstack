# Kubernetes Cluster Provisioning Service

A FastAPI-based service for automated provisioning of Kubernetes clusters using Talos Linux, following the genmachine pattern established in this repository.

## Features

- **Automated VM Creation**: Creates VMs in Proxmox VE with proper resource allocation
- **Talos Bootstrap**: Generates and applies Talos configurations for cluster initialization
- **Secret Management**: Stores cluster credentials and configurations in HashiCorp Vault
- **GitOps Integration**: Automatically generates ArgoCD applications and manifests
- **REST API**: Full API for cluster lifecycle management
- **Job Tracking**: Asynchronous provisioning with progress monitoring
- **Multi-cluster Support**: Manage multiple clusters with different configurations

## Quick Start

### 1. Install Dependencies

```bash
cd scripts/cluster-provisioning
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your environment configuration:

```bash
# Proxmox Configuration
PROXMOX_HOST=your-proxmox-host
PROXMOX_USER=your-username@pam
PROXMOX_PASSWORD=your-password
PROXMOX_NODE=your-proxmox-node

# Talos Configuration
TALOS_ISO_PATH=/path/to/talos.iso
TALOS_VERSION=v1.6.0

# Vault Configuration
VAULT_URL=https://your-vault-instance
VAULT_TOKEN=your-vault-token

# Git Repository
GIT_REPO_PATH=/path/to/gitops-repo
```

### 3. Start the Service

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Create a Cluster

Using the API:

```bash
curl -X POST "http://localhost:8000/api/v1/clusters" \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_name": "production",
    "vmid_prefix": 40,
    "control_plane_nodes": 3,
    "worker_nodes": 2,
    "network_config": {
      "vip": "192.168.2.160",
      "node_ips": ["192.168.2.161", "192.168.2.162", "192.168.2.163", "192.168.2.164", "192.168.2.165"]
    }
  }'
```

Using the Python example:

```bash
python examples/create_cluster_example.py create
```

Using Task:

```bash
task cluster:create CLUSTER_NAME=production VMID_PREFIX=40 CLUSTER_VIP=192.168.2.160
```

## API Documentation

### Base URL

`http://localhost:8000`

### Endpoints

#### Create Cluster
- **POST** `/api/v1/clusters`
- Creates a new Kubernetes cluster
- Returns job ID for tracking progress

#### Get Cluster Status
- **GET** `/api/v1/clusters/{cluster_name}/status`
- Returns detailed cluster status and provisioning progress

#### List Clusters
- **GET** `/api/v1/clusters`
- Returns list of all managed clusters

#### Delete Cluster
- **DELETE** `/api/v1/clusters/{cluster_name}`
- Initiates cluster deletion process

#### Get Cluster Logs
- **GET** `/api/v1/clusters/{cluster_name}/logs?lines=100`
- Returns provisioning logs for debugging

#### Retry Failed Provisioning
- **POST** `/api/v1/clusters/{cluster_name}/retry`
- Retries failed cluster provisioning

### Request Schema

```json
{
  "cluster_name": "string",
  "vmid_prefix": 40,
  "control_plane_nodes": 3,
  "worker_nodes": 2,
  "network_config": {
    "vip": "192.168.2.160",
    "node_ips": ["192.168.2.161", "192.168.2.162", "192.168.2.163"],
    "pod_cidr": "10.244.0.0/16",
    "service_cidr": "10.96.0.0/12",
    "dns_servers": ["8.8.8.8", "8.8.4.4"]
  },
  "resource_config": {
    "cpu_cores": 4,
    "memory_gb": 8,
    "storage_gb": 100
  },
  "proxmox_config": {
    "storage": "local-lvm",
    "bridge": "vmbr0"
  },
  "talos_config": {
    "version": "v1.6.0",
    "install_disk": "/dev/sda"
  },
  "enable_gitops": true,
  "applications": ["cert-manager", "external-secrets", "ingress-nginx"]
}
```

## Task Integration

The service integrates with the existing Taskfile system:

### Available Tasks

```bash
# Install dependencies
task service:install

# Start the provisioning service
task service:start

# Create a new cluster
task cluster:create CLUSTER_NAME=mytest VMID_PREFIX=50

# List all clusters
task cluster:list

# Get cluster status
task cluster:status CLUSTER_NAME=mytest

# Delete a cluster
task cluster:delete CLUSTER_NAME=mytest

# Verify cluster health
task cluster:verify CLUSTER_NAME=mytest
```

### Manual Cluster Creation Steps

If you prefer to run individual steps manually:

```bash
# 1. Validate parameters
task cluster:validate CLUSTER_NAME=mytest

# 2. Create VMs in Proxmox
task cluster:provision-vms CLUSTER_NAME=mytest VMID_PREFIX=50

# 3. Bootstrap Talos cluster
task cluster:bootstrap-talos CLUSTER_NAME=mytest

# 4. Store secrets in Vault
task cluster:store-secrets CLUSTER_NAME=mytest

# 5. Generate GitOps manifests
task cluster:generate-gitops CLUSTER_NAME=mytest

# 6. Verify cluster health
task cluster:verify CLUSTER_NAME=mytest
```

## Architecture

### Provisioning Workflow

1. **VM Creation**: Creates VMs in Proxmox with Talos ISO
2. **Configuration Generation**: Generates Talos machine configs
3. **Cluster Bootstrap**: Applies configs and bootstraps etcd
4. **Secret Storage**: Stores talosconfig and kubeconfig in Vault
5. **GitOps Generation**: Creates ArgoCD applications and manifests
6. **Health Verification**: Verifies cluster is ready and healthy

### Service Components

- **ClusterOrchestrator**: Main coordination service
- **ProxmoxService**: VM management and provisioning
- **TalosService**: Talos configuration and bootstrap
- **VaultService**: Secret storage and retrieval
- **GitOpsService**: Manifest generation and Git operations

### Job Management

- Asynchronous background processing
- Persistent job state storage
- Progress tracking and monitoring
- Error handling and retry capabilities
- Detailed logging for debugging

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROXMOX_HOST` | Proxmox VE hostname/IP | Required |
| `PROXMOX_USER` | Proxmox username | Required |
| `PROXMOX_PASSWORD` | Proxmox password | Required |
| `PROXMOX_NODE` | Proxmox node name | Required |
| `TALOS_ISO_PATH` | Path to Talos ISO file | Required |
| `VAULT_URL` | Vault server URL | Required |
| `VAULT_TOKEN` | Vault authentication token | Required |
| `GIT_REPO_PATH` | GitOps repository path | Required |
| `HOST` | Service host | `0.0.0.0` |
| `PORT` | Service port | `8000` |
| `DEBUG` | Enable debug mode | `false` |

### Networking Requirements

- Access to Proxmox VE API
- Access to HashiCorp Vault API
- Network connectivity to cluster VMs for Talos operations
- Git repository access for GitOps manifest commits

## Troubleshooting

### Common Issues

**VM Creation Fails**
- Check Proxmox credentials and connectivity
- Verify Talos ISO path exists and is accessible
- Ensure sufficient resources on Proxmox node

**Talos Bootstrap Fails**
- Verify VM network connectivity
- Check if VMs booted successfully from Talos ISO
- Validate IP addresses are accessible

**GitOps Generation Fails**
- Check Git repository permissions
- Verify Git repository path is correct
- Ensure genmachine template exists

### Debug Mode

Enable debug mode for detailed logging:

```bash
DEBUG=true python -m uvicorn app.main:app --reload
```

### Log Files

Cluster provisioning logs are stored in:
- Job information: `/tmp/cluster-jobs/{job_id}.json`
- Cluster logs: `/tmp/cluster-logs/{cluster_name}.log`

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Adding New Features

1. Extend the appropriate service class
2. Update the ClusterOrchestrator workflow
3. Add new API endpoints if needed
4. Update documentation and examples

### Contributing

1. Create a feature branch
2. Implement changes with tests
3. Update documentation
4. Submit a pull request

## Examples

See the `examples/` directory for:
- `create_cluster_example.py`: Complete API usage examples
- Configuration templates
- Testing scripts

## Security Considerations

- Store sensitive credentials in Vault, not environment files
- Use TLS for API communication in production
- Implement proper authentication and authorization
- Regular security updates for dependencies
- Network segmentation for cluster nodes

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `http://localhost:8000/docs`
3. Check cluster logs for detailed error information
4. Consult the main repository documentation
