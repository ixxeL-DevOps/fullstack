
# Manifest Hydration

To hydrate the manifests in this repository, run the following commands:

```shell

git clone https://github.com/ixxeL-DevOps/fullstack.git
# cd into the cloned directory
git checkout 13d241ab82d627ebf99b720a22ef28fc6557bf5f
helm template . --name-template wireguard-k0s --include-crds
```