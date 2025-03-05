# k0s Cluster Installation Guide (Single Node)

This document details the installation and configuration of a **single-node k0s cluster** for my home lab environment. It is based on the provided `k0sctl.yaml` file and explains the technical choices made. Additionally, a **Taskfile** is used to simplify cluster management tasks.

## 🏗️ Cluster Overview

The cluster is a **single-node Kubernetes cluster** running on a small home server. It uses **k0s**, a lightweight Kubernetes distribution, and stores its state in **Kine** instead of etcd.

### 🔹 Key Features:

- **Data Storage**: `kine` (instead of etcd, more lightweight for a home lab)
- **CNI (Networking)**: `kube-router`
- **SSH Management**: Connection via user `fred`
- **Disabled Components**: `autopilot`, `helm`, `windows-node`, `konnectivity-server` for optimization
- **Security**: Certain unsafe `sysctls` are allowed for advanced routing (`net.ipv4.ip_forward`, `net.ipv4.conf.all.src_valid_mark`), particularly for **WireGuard VPN** integration.
- **Environment Management**: Uses **Devbox** to handle binaries like `k0sctl`, `kubectl`, `task`, and other necessary CLI tools.

## 🛠️ Installation

### 📌 Prerequisites

Before installing the cluster, ensure you have:

- A server with a compatible Linux distribution (Ubuntu/Debian recommended)
- SSH access with a key (`~/.ssh/id_rsa`)
- **Devbox installed** to manage required tools:
  ```sh
  curl -fsSL https://get.jetify.com/devbox | bash
  ```
- **Set up the environment** using Devbox:
  ```sh
  devbox add k0sctl kubectl go-task
  ```
- **Launch your devbox shell**:
  ```sh
  devbox shell
  ```

### 🚀 Deploying the Cluster

1. **Check your k0sctl file**

   file should be in `infra/k0s/fullstack.yaml`

2. **Verify the configuration and start the installation**

   ```sh
   task apply-config
   ```

   This ensures everything is ready before actual deployment ans ask for applying changes.

3. **Verify that the cluster is active**
   ```sh
   task kubeconf
   kubectl get nodes
   ```

## ⚙️ Technical Configuration Details

### 1️⃣ Networking Configuration

- **CNI Used**: `kube-router`
- **Hairpin Mode Enabled**: Allows pods to communicate via their own IP address.
- **iptables Mode for kube-proxy**: Ensures better compatibility with existing networking setups.

### 2️⃣ Security & Sysctls

Certain advanced `sysctls` are enabled to enhance routing management, particularly for **WireGuard VPN tunnels**:

```yaml
--allowed-unsafe-sysctls=net.ipv4.ip_forward,net.ipv4.conf.all.src_valid_mark
```

- `net.ipv4.ip_forward`: Enables packet forwarding, required for VPN and overlay networks.
- `net.ipv4.conf.all.src_valid_mark`: Ensures proper routing of encrypted WireGuard packets.

### 3️⃣ Disabled Components

Some unnecessary components for a home lab are disabled to reduce resource usage and improve stability:

- **Autopilot** (automatic updates management, not needed here)
- **Helm** (not required since charts can be managed separately)
- **Windows-node** (no Windows support required)
- **Konnectivity-server** (used for complex networks, unnecessary here)

### 4️⃣ Data Storage

- The Kubernetes state storage is managed by **Kine**, a lightweight alternative to `etcd`, using SQLite or a remote database.
- This reduces resource consumption and avoids the complexity of running an etcd cluster on a single node.

## 🔄 Cluster Management

### 🏗️ Check the controller

```sh
ssh fred@192.168.1.190 "sudo systemctl status k0scontroller.service"
```

### 🚀 Access the Cluster

```sh
export KUBECONFIG=$(task kubeconf)
kubectl get nodes
```

## 🔧 Upgrading k0s

To upgrade k0s to the latest stable version:

```sh
task upgrade-cluster
```

## 🔄 Backing Up the Cluster

To create a backup of the cluster:

```sh
task backup
```
