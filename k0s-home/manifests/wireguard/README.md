
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout acda2e8bab2d7e8de7f878f709eb12780730d358
helm template . --name-template wireguard-k0s --include-crds
```