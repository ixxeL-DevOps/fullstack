
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b4ddc251f555ed3a0dcd17c2e6f6ade267f1d805
helm template . --name-template wireguard-k0s --include-crds
```