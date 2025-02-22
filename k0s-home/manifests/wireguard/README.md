
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 57e0e1a2db9dc391d5fbbfd707eb455a4e3239a9
helm template . --name-template wireguard-k0s --include-crds
```