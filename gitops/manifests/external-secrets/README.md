
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b1606439e29d3ed1011bfbcfcad183f592acf46a
helm template . --name-template external-secrets-k0s --include-crds
```