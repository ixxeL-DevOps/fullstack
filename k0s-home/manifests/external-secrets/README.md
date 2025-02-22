
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 5b786e348260eed51bf4e61dbab3cbd752d1164c
helm template . --name-template external-secrets-k0s --include-crds
```