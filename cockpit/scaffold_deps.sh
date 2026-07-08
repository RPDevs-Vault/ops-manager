#!/bin/bash
cd container-manager/dependencies
# Software packages list
packages=("FlareSolverr" "mega-embed-2" "t430-runner")
for pkg in "${packages[@]}"; do
    mkdir -p "$pkg"
    cat << EOR > "$pkg/README.md"
# $pkg Dependencies

## Dependent Software
- $pkg

## Build Information
Dependencies for $pkg are managed as part of the unified build fleet.

## Usage
Refer to the master [DEPENDENCIES.md](../DEPENDENCIES.md) for usage instructions.
EOR
done
