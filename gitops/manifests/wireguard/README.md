
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 030db9af20a8fdf946983f27af9e8dbf2361074d
helm template . --name-template wireguard-k0s --include-crds
```