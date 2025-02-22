
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9918638c31ca62614f40736ee0cc9f3b4ad135e3
helm template . --name-template wireguard-k0s --include-crds
```