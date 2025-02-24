
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1f67cc80c7d252638fa7628fe8a00064dcee712a
helm template . --name-template wireguard-k0s --include-crds
```