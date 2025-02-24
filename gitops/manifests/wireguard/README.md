
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f82f5c08de6fa316571c72fcc5e099555af4cdcc
helm template . --name-template wireguard-k0s --include-crds
```