
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 78f58040b07c500bb70f513024f71bbd8e6a828e
helm template . --name-template external-secrets-k0s --include-crds
```