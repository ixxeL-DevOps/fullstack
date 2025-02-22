
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 494d1b0a1b92ec4b81539097af4f53405e34f3d7
helm template . --name-template wireguard-k0s --include-crds
```