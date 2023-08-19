#!/usr/bin/env bash
for version in $(tissuumaps-schema versions); do
    mkdir -p _site/${version}
    for model in $(tissuumaps-schema models --version ${version}); do
        tissuumaps-schema generate --version ${version} ${model} > _site/${version}/${model,,}.json
    done
    generate-schema-doc --expand-buttons --no-link-to-reused-ref --deprecated-from-description _site/${version} _site/${version}
done
