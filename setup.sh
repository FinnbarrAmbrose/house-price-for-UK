#!/usr/bin/env bash
set -e

echo "→ creating output dirs"
mkdir -p outputs/datasets/collection outputs/models

echo "→ using pre-generated CSV & model"
ls outputs/datasets/collection/*.csv || echo "‼️ no CSV!"
ls outputs/models/*.pkl             || echo "‼️ no model!"

echo "✅ setup OK"
