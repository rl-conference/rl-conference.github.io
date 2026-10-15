#!/bin/sh
set -eu

cd "$(dirname "$0")"
../tailwindcss --output build.css
