
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 1aa84525bc19d624c052362e09182f1081d7d38f
helm template . --name-template wireguard-k0s --include-crds
```