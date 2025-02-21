
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 4b122ec9c58e72a15ff3c50041f25f1de1c5e507
helm template . --name-template external-secrets-k0s --include-crds
```