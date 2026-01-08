#!/bin/bash
set -e

echo "Building Lambda package..."

rm -rf .build lambda_package.zip

poetry export -f requirements.txt --output requirements.txt --without-hashes

mkdir -p .build
pip install -r requirements.txt -t .build --platform manylinux2014_x86_64 --only-binary=:all:

cp -r src .build/
cp config.yaml .build/

cd .build
zip -r ../lambda_package.zip . -x "*.pyc" -x "*__pycache__*"
cd ..

rm -rf .build requirements.txt

echo "Lambda package created: lambda_package.zip"
