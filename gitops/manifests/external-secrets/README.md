
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 07542929e14b7ae6102b562dc8684229fc4f51c2
helm template . --name-template external-secrets-k0s --include-crds
```