#!/bin/bash
REPOS=(
  "IamRPDev/dotfiles"
  "IamRPDev/llmdata-core"
  "IamRPDev/hugo_main.iamrpdev.github.io"
  "IamRPDev/mkdocs_wiki.iamrpdev.github.io"
  "IamRPDev/iamrpdev.github.io"
  "IamRPDev/llm-project"
  "IamRPDev/llm-thinktank"
  "IamRPDev/cinn-agent-monitor"
  "IamRPDev/cyan-resonance"
)

LICENSE_TEXT="MIT License

Copyright (c) 2026 IamRPDev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."

CONTENT=$(echo "$LICENSE_TEXT" | base64 -w 0)

for repo in "${REPOS[@]}"; do
  echo "Adding LICENSE to $repo..."
  gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "/repos/$repo/contents/LICENSE" \
    -f message="chore: add MIT License placeholder" \
    -f content="$CONTENT" || echo "Failed or already exists for $repo"
done
