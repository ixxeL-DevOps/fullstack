
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout a0718e95e53cd0699aa0628fbd1f7fda2575117b
helm template . --name-template wireguard-k0s --include-crds
```