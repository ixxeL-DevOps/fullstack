
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3c8da769bc803361ec234968ae6cc9b8f74664f4
helm template . --name-template wireguard-k0s --include-crds
```