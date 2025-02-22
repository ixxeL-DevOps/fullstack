
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 2b7e039307c6fcb85e8062e951be0e6bb5968dff
helm template . --name-template wireguard-k0s --include-crds
```