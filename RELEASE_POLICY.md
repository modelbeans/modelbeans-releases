# Public release policy

The public destination for ModelBeans and RuntimeShare distribution is:

https://github.com/modelbeans/modelbeans-releases/releases

## Contents

This repository may contain user-facing documentation, release notes, reviewed SDK usage examples, compatibility manifests and license notices. Installers and runtime/developer archives are attached as GitHub Release assets, not committed as binary blobs in Git history.

Product implementation source, internal design/review documents, development history, credentials, user data and model caches are outside this repository's scope. Creating this channel does not authorize publishing any particular binary, SDK source package or model weights.

## Version records

- ModelBeans releases use `vX.Y.Z`; preview candidates may use `vX.Y.Z-rc.N` and are marked Pre-release.
- If RuntimeShare is released independently, use namespaced tags such as `runtimeshare-vX.Y.Z` to avoid version collisions.
- A release records supported platforms, included components and their versions, artifact hashes, relevant licensing, installation instructions and known limitations.
- A distribution-repository tag identifies the release documentation and manifest. It is not the implementation source revision; build provenance must be recorded separately.
- Published version tags and asset contents must not silently change. Corrections require a new version and explanatory release notes; unsafe releases can be withdrawn with an explanation.

## Verification

Only tested capabilities may be advertised. A successful build or mock test does not certify a hardware backend. A checksum verifies bytes, not publisher identity; signing status must be stated accurately.

For models, local hardware requirements and licenses apply independently. API compatibility refers to the documented and tested subset, not every feature of an upstream provider.

No automated publishing workflow is configured by this repository initialization.
