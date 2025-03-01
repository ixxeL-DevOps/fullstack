
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 111c9a9a4217fc43aa0b9fd054c1152d3e4df430
helm template . --name-template external-secrets-k0s --include-crds
```