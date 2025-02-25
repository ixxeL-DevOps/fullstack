
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 9638b9110ec25130da1ecf09bf3c9e486049e709
helm template . --name-template wireguard-k0s --include-crds
```