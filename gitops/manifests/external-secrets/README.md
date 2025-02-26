
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout d5c3b42e34fc2b1a8bedace8cabf8e86e9fdd399
helm template . --name-template external-secrets-k0s --include-crds
```