
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout f3e770048d430dbd061a3c3eb149176724887e59
helm template . --name-template external-secrets-k0s --include-crds
```