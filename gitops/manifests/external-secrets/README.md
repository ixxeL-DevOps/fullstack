
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b69c8f663d61969641bae7c91eae0d546cd61245
helm template . --name-template external-secrets-k0s --include-crds
```