
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 752534e76fa5a31176821668d8bcf65f1c28fb36
helm template . --name-template wireguard-k0s --include-crds
```