#!/usr/bin/env python3
"""
Example script showing how to use the Cluster Provisioning API

This script demonstrates how to programmatically create a new Kubernetes cluster
using the cluster provisioning service.
"""

import json
import time
import httpx
from typing import Dict, Any


def create_cluster_example():
    """Example of creating a new cluster via API"""
    
    # API endpoint
    base_url = "http://localhost:8000"
    
    # Cluster configuration
    cluster_config = {
        "cluster_name": "production",
        "vmid_prefix": 40,
        "control_plane_nodes": 3,
        "worker_nodes": 2,
        "network_config": {
            "vip": "192.168.2.160",
            "node_ips": [
                "192.168.2.161",
                "192.168.2.162", 
                "192.168.2.163",
                "192.168.2.164",
                "192.168.2.165"
            ],
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
        "enable_gitops": True,
        "applications": [
            "cert-manager",
            "external-secrets", 
            "ingress-nginx",
            "metallb",
            "longhorn"
        ]
    }
    
    print("Creating new Kubernetes cluster...")
    print(f"Cluster name: {cluster_config['cluster_name']}")
    print(f"Control plane nodes: {cluster_config['control_plane_nodes']}")
    print(f"Worker nodes: {cluster_config['worker_nodes']}")
    print(f"VIP: {cluster_config['network_config']['vip']}")
    
    with httpx.Client(timeout=30.0) as client:
        try:
            # Create cluster
            response = client.post(
                f"{base_url}/api/v1/clusters",
                json=cluster_config
            )
            response.raise_for_status()
            
            create_result = response.json()
            print(f"✓ Cluster creation started")
            print(f"  Job ID: {create_result['data']['job_id']}")
            print(f"  Status: {create_result['data']['status']}")
            
            cluster_name = cluster_config['cluster_name']
            job_id = create_result['data']['job_id']
            
            # Monitor provisioning progress
            print("\nMonitoring provisioning progress...")
            while True:
                status_response = client.get(
                    f"{base_url}/api/v1/clusters/{cluster_name}/status"
                )
                status_response.raise_for_status()
                
                status_data = status_response.json()['data']
                current_status = status_data['status']
                
                print(f"Status: {current_status}")
                if 'job_id' in status_data:
                    print(f"Progress: checking...")
                
                if current_status in ['ready', 'failed']:
                    break
                
                time.sleep(10)
            
            if current_status == 'ready':
                print("\n🎉 Cluster provisioning completed successfully!")
                print(f"API Server: {status_data.get('api_server_endpoint', 'N/A')}")
                print(f"Kubeconfig available: {status_data.get('kubeconfig_available', False)}")
                
                # Get cluster logs
                logs_response = client.get(
                    f"{base_url}/api/v1/clusters/{cluster_name}/logs?lines=20"
                )
                if logs_response.status_code == 200:
                    logs_data = logs_response.json()
                    print("\nLast 20 log lines:")
                    for log_line in logs_data['data']['logs'][-20:]:
                        print(f"  {log_line}")
                
            else:
                print(f"\n❌ Cluster provisioning failed with status: {current_status}")
                
                # Get error logs
                logs_response = client.get(
                    f"{base_url}/api/v1/clusters/{cluster_name}/logs?lines=50"
                )
                if logs_response.status_code == 200:
                    logs_data = logs_response.json()
                    print("\nError logs:")
                    for log_line in logs_data['data']['logs'][-50:]:
                        print(f"  {log_line}")
            
        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP error: {e.response.status_code}")
            try:
                error_data = e.response.json()
                print(f"Error message: {error_data.get('message', 'Unknown error')}")
            except:
                print(f"Response: {e.response.text}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")


def list_clusters_example():
    """Example of listing all clusters"""
    base_url = "http://localhost:8000"
    
    print("Listing all clusters...")
    
    with httpx.Client() as client:
        try:
            response = client.get(f"{base_url}/api/v1/clusters")
            response.raise_for_status()
            
            clusters_data = response.json()
            clusters = clusters_data['data']['clusters']
            
            if not clusters:
                print("No clusters found.")
                return
            
            print(f"\nFound {len(clusters)} cluster(s):")
            print("-" * 80)
            print(f"{'Name':<15} {'Status':<12} {'Nodes':<8} {'API Endpoint':<25} {'Created'}")
            print("-" * 80)
            
            for cluster in clusters:
                nodes = f"{cluster['control_plane_nodes']}+{cluster['worker_nodes']}"
                endpoint = cluster.get('api_server_endpoint', 'N/A')[:24]
                created = cluster['created_at'][:10]  # Just the date
                
                print(f"{cluster['cluster_name']:<15} {cluster['status']:<12} {nodes:<8} {endpoint:<25} {created}")
            
        except Exception as e:
            print(f"❌ Error listing clusters: {str(e)}")


def delete_cluster_example(cluster_name: str):
    """Example of deleting a cluster"""
    base_url = "http://localhost:8000"
    
    print(f"Deleting cluster '{cluster_name}'...")
    
    with httpx.Client() as client:
        try:
            response = client.delete(f"{base_url}/api/v1/clusters/{cluster_name}")
            response.raise_for_status()
            
            delete_result = response.json()
            print(f"✓ Cluster deletion started")
            print(f"  Job ID: {delete_result['data']['job_id']}")
            print(f"  Status: {delete_result['data']['status']}")
            
            # Monitor deletion progress
            job_id = delete_result['data']['job_id']
            print("\nMonitoring deletion progress...")
            
            while True:
                try:
                    status_response = client.get(
                        f"{base_url}/api/v1/clusters/{cluster_name}/status"
                    )
                    if status_response.status_code == 404:
                        print("✓ Cluster successfully deleted")
                        break
                    
                    status_response.raise_for_status()
                    status_data = status_response.json()['data']
                    print(f"Status: {status_data['status']}")
                    
                    if status_data['status'] == 'deleted':
                        print("✓ Cluster deletion completed")
                        break
                    
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        print("✓ Cluster successfully deleted")
                        break
                    raise
                
                time.sleep(5)
            
        except Exception as e:
            print(f"❌ Error deleting cluster: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "create":
            create_cluster_example()
        elif command == "list":
            list_clusters_example()
        elif command == "delete" and len(sys.argv) > 2:
            delete_cluster_example(sys.argv[2])
        else:
            print("Usage:")
            print("  python create_cluster_example.py create")
            print("  python create_cluster_example.py list")
            print("  python create_cluster_example.py delete <cluster_name>")
    else:
        print("Available examples:")
        print("1. Creating a cluster")
        print("2. Listing clusters")
        print("3. Deleting a cluster")
        print()
        print("Usage:")
        print("  python create_cluster_example.py create")
        print("  python create_cluster_example.py list") 
        print("  python create_cluster_example.py delete <cluster_name>")
