
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 993a74d9e93b6496252885f04e0f1258de67c06f
helm template . --name-template wireguard-k0s --include-crds
```