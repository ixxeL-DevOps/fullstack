
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3079627df1dfadaaddc9e82c959eb961d8115f0b
helm template . --name-template wireguard-k0s --include-crds
```