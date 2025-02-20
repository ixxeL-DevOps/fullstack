
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout dd11913691069b5d4ecda2a7297e577c65066376
helm template . --name-template external-secrets-k0s --include-crds
```