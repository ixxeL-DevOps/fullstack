
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout eafdf86d686833ef01fea63360fc7cfa19fd52a2
helm template . --name-template external-secrets-k0s --include-crds
```