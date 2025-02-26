
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout b9af47a1d9996406a62a9304406b6748d9cc5005
helm template . --name-template external-secrets-k0s --include-crds
```