
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 97e711b8af8d05696a9a119ec76017f01c72fdd7
helm template . --name-template wireguard-k0s --include-crds
```