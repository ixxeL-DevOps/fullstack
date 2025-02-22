
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout adf832a808cd4fa60ee075588b611ffe36189842
helm template . --name-template external-secrets-k0s --include-crds
```