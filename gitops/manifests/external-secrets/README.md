
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 536749f0ea41eda42bc47cb8278891385f640f77
helm template . --name-template external-secrets-k0s --include-crds
```