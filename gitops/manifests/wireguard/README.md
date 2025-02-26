
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 2e0a1407147b19a6a49c08fd4dc95a5aca3093fe
helm template . --name-template wireguard-k0s --include-crds
```