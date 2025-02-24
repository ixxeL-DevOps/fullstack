
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 8cd56ab071636756b353d9e4f79b33795bd4de12
helm template . --name-template wireguard-k0s --include-crds
```