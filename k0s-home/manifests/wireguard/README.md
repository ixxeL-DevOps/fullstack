
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout ff7bf77ffcac31ff8bc24cbf847434f5cdb263f8
helm template . --name-template wireguard-k0s --include-crds
```