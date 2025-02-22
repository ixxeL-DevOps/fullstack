
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 51ba7b4de836dafcd9eabfd4047a05dd3c4578ac
helm template . --name-template wireguard-k0s --include-crds
```