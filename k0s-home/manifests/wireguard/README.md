
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f00b9a854d4a54cf435ed54ca45714dca4ca2314
helm template . --name-template wireguard-k0s --include-crds
```