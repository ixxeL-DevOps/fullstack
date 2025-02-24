
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5666317410fe994f588e58bfbe07e1f8f6317424
helm template . --name-template wireguard-k0s --include-crds
```