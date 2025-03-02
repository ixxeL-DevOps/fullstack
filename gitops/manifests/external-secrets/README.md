
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 0c8efc47855636199d238894b082916d359aa56a
helm template . --name-template external-secrets-k0s --include-crds
```