
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout c72c59e8b67e5133bc3f94f5195e5510db498db7
helm template . --name-template wireguard-k0s --include-crds
```