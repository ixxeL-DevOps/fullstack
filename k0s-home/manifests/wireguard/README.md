
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0d5d5d4f4dae9ab95257dd6fdf7eacf8ebbd01b2
helm template . --name-template wireguard-k0s --include-crds
```