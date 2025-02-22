
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8a945825fe57e6d13924ff5c8df0eed9b4f8fe5c
helm template . --name-template wireguard-k0s --include-crds
```