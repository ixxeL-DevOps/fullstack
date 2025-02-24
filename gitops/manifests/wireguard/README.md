
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0f2448d1da3af1ce8250a5b1401394aaa28d7b4c
helm template . --name-template wireguard-k0s --include-crds
```