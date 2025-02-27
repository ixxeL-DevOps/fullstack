
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 3750e0add4d5269631c3345cbc68240313a248cd
helm template . --name-template external-secrets-k0s --include-crds
```