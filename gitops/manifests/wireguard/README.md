
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3654ede901407cdc8bb8cea1e596a1d88205db62
helm template . --name-template wireguard-k0s --include-crds
```