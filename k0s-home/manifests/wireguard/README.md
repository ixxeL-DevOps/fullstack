
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b2e19984aa62be646a2a74cdc7be9f74611f5610
helm template . --name-template wireguard-k0s --include-crds
```