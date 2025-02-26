
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 4298428e7a7a8477fc296f8b416c045c771c942d
helm template . --name-template wireguard-k0s --include-crds
```