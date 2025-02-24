
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout fe3433911eb128ddbac30c8a8efc35bef9a12bf1
helm template . --name-template wireguard-k0s --include-crds
```