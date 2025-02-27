
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f3fd84f80d8445975f03f76cc715198f46133330
helm template . --name-template external-secrets-k0s --include-crds
```