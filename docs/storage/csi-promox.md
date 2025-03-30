# Storage

## Proxmox CSI plugin

This CSI plugin was designed to support multiple independent Proxmox clusters within a single Kubernetes cluster. It enables the use of a single storage class to deploy one or many deployments/statefulsets across different regions, leveraging region/zone anti-affinity or topology spread constraints

### Installation

#### Proxmox

Requirements for Proxmox CSI Plugin

- Proxmox must be clustered
- Proxmox CSI Plugin must have privileges in your Proxmox instance
- Kubernetes must be labelled with the correct topology
- A StoreClass referencing the CSI plugin exists

For the Proxmox CSI Plugin to work you need to cluster your Proxmox nodes.
You can cluster a single Proxmox node with itself.
Read more about Proxmox clustering [here](https://pve.proxmox.com/wiki/Cluster_Manager).

And check it with `pvecm status` :

```console
Cluster information
-------------------
Name:             Proxcorp
Config Version:   6
Transport:        knet
Secure auth:      on

Quorum information
------------------
Date:             Thu Mar 13 16:06:07 2025
Quorum provider:  corosync_votequorum
Nodes:            3
Node ID:          0x00000001
Ring ID:          1.eb
Quorate:          Yes

Votequorum information
----------------------
Expected votes:   4
Highest expected: 4
Total votes:      3
Quorum:           3
Flags:            Quorate

Membership information
----------------------
    Nodeid      Votes Name
0x00000001          1 192.168.1.251 (local)
0x00000003          1 192.168.1.249
0x00000004          1 192.168.1.248
```

Create a CSI role :

```bash
pveum role add CSI -privs "VM.Audit VM.Config.Disk Datastore.Allocate Datastore.AllocateSpace Datastore.Audit"
```

Next create a user `kubernetes-csi@pve` for the CSI plugin and grant it the above role

```bash
pveum user add kubernetes-csi@pve
pveum aclmod / -user kubernetes-csi@pve -role CSI
pveum user token add kubernetes-csi@pve csi -privsep 0
```

All VMs in the cluster must have the **SCSI Controller** set to `VirtIO SCSI single` or `VirtIO SCSI` type to be able to attach disks.

#### Kubernetes

You need to enforce label `pod-security.kubernetes.io/enforce=privileged` to your plugin namespace installation :

```bash
kubectl label ns csi-proxmox pod-security.kubernetes.io/enforce=privileged
```

**Important**: The `topology.kubernetes.io/region` and `topology.kubernetes.io/zone` labels **must** be set.
Region is the Proxmox cluster name, and zone is the Proxmox node name.
Cluster name can be human-readable and should be the same as in Cloud config.

```bash
kubecel label --overwrite nodes talos-1 topology.kubernetes.io/region=Proxcorp
kubecel label --overwrite nodes talos-1 topology.kubernetes.io/zone=genmachine
kubecel label --overwrite nodes talos-2 topology.kubernetes.io/region=Proxcorp
kubecel label --overwrite nodes talos-2 topology.kubernetes.io/zone=genmachine
kubecel label --overwrite nodes talos-3 topology.kubernetes.io/region=Proxcorp
kubecel label --overwrite nodes talos-3 topology.kubernetes.io/zone=genmachine
```

Then you need to specify your configuration in your `values.yaml` file

```yaml
createNamespace: false

node:
  nodeSelector:
    node-role.kubernetes.io/control-plane: ""
  tolerations:
    - key: node-role.kubernetes.io/control-plane
      effect: NoSchedule

nodeSelector:
  node-role.kubernetes.io/control-plane: ""
tolerations:
  - key: node-role.kubernetes.io/control-plane
    effect: NoSchedule

config:
  clusters:
    - url: https://192.168.1.248:8006/api2/json
      insecure: true
      token_id: "kubernetes-csi@pve!csi"
      token_secret: "<REDACTED>"
      region: Proxcorp

storageClass:
  - name: proxmox-data-xfs
    storage: data
    reclaimPolicy: Delete
    fstype: xfs
  - name: proxmox-data
    storage: local-lvm
    reclaimPolicy: Delete
```

### Checking

You can use following command in your proxmox node to check for volumes :

```console
root@genmachine:~# lvdisplay
  --- Logical volume ---
  LV Path                /dev/pve/vm-9999-pvc-8fc6d472-d3b6-488c-bd79-4d79a5e91d8a
  LV Name                vm-9999-pvc-8fc6d472-d3b6-488c-bd79-4d79a5e91d8a
  VG Name                pve
  LV UUID                oMCPNt-U0xh-zZQR-uaoB-twRg-0PfK-LwRTjw
  LV Write Access        read/write
  LV Creation host, time genmachine, 2025-03-13 16:43:09 +0100
  LV Pool name           data
  LV Status              available
  # open                 1
  LV Size                1.00 GiB
  Mapped size            4.78%
  Current LE             256
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:9
```

Useful commands:

```bash
cat /etc/pve/storage.cfg
lvscan
lvs
```

You can determine filesystem type :

```console
root@genmachine:~# blkid /dev/pve/vm-9999-pvc-8fc6d472-d3b6-488c-bd79-4d79a5e91d8a
/dev/pve/vm-9999-pvc-8fc6d472-d3b6-488c-bd79-4d79a5e91d8a: UUID="b5c6da9e-2bfc-4d96-9c4e-2347c0f3f633" BLOCK_SIZE="4096" TYPE="ext4"
```

Create mountpoint :

```bash
mkdir -p /mnt/lvm-volume
mount /dev/pve/vm-9999-pvc-8fc6d472-d3b6-488c-bd79-4d79a5e91d8a /mnt/lvm-volume
```

and unmount:

```bash
umount /mnt/lvm-volume
```

### Cleanup

Display volumes :

```console
root@genmachine:~# lvs
  LV                                               VG  Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  data                                             pve twi-aotz-- 794.30g             8.58   0.53
  root                                             pve -wi-ao----  96.00g
  swap                                             pve -wi-ao----   8.00g
  vm-201-disk-0                                    pve Vwi-aotz-- 150.00g data        17.63
  vm-202-disk-0                                    pve Vwi-aotz-- 150.00g data        12.19
  vm-203-disk-0                                    pve Vwi-aotz-- 150.00g data        13.02
  vm-9999-pvc-0e8fe432-4ab3-4e1e-ad21-685347c2fcd8 pve Vwi-aotz--   2.00g data        5.06
  vm-9999-pvc-1da305d3-b648-46dc-9ad7-b57176acd5ff pve Vwi-a-tz--   8.00g data        5.60
  vm-9999-pvc-2a8ec1f7-3b32-438e-8409-8a912c8f0943 pve Vwi-a-tz--   2.00g data        5.06
  vm-9999-pvc-2e1cee20-788d-4603-831f-aa6226a75cea pve Vwi-a-tz--   2.00g data        5.02
  vm-9999-pvc-4454e534-b0df-41f9-a08e-5911a0c5892a pve Vwi-aotz--  10.00g data        2.33
  vm-9999-pvc-48404b2f-71b2-4db4-a228-6eef4736fcff pve Vwi-a-tz--   8.00g data        5.30
  vm-9999-pvc-4c5e4578-764f-4cd5-a23a-6f62f5913695 pve Vwi-a-tz--   8.00g data        1.45
  vm-9999-pvc-5be83d2d-d7cc-4d39-aa82-f66d92305f41 pve Vwi-a-tz--   8.00g data        5.39
  vm-9999-pvc-5d2019bb-79eb-49a3-87a2-f2e2e7999ceb pve Vwi-a-tz--   8.00g data        8.04
  vm-9999-pvc-62368786-acf7-445d-8a6b-0a927b6d5564 pve Vwi-aotz--   8.00g data        9.80
  vm-9999-pvc-7181fd6d-57a3-42b9-964f-103843a56372 pve Vwi-a-tz--   8.00g data        3.37
  vm-9999-pvc-ed394ebe-3121-4c08-ad8b-9c30e139de4f pve Vwi-aotz--  10.00g data        2.24
```

Volume like that `Vwi-aotz--` are online and used propably by `StorageClass`.

To clean up offline volumes :

```bash
lvs -o name,attr | awk 'NR>1 && $2 !~ /o/ {print "/dev/pve/" $1}' |  xargs -n 1 lvchange -an
```

```bash
lvs -o name,attr | awk 'NR>1 && $2 !~ /o/ {print "/dev/pve/" $1}' |  xargs -n 1 lvremove
```
