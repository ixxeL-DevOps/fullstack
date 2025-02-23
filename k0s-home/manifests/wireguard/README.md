
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3cfa43002e6ccf89a0cbe4d09058ba1add95cb3f
helm template . --name-template wireguard-k0s --include-crds
```