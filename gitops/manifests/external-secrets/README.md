
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout fcb737fc1d9988888e0e264ecf1df00b10562736
helm template . --name-template external-secrets-k0s --include-crds
```