
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout c6169f326a4d1f9eb32e96fdeb01600758dca047
helm template . --name-template wireguard-k0s --include-crds
```