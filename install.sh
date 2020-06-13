# /usr/bin/env bash
# script for purescript-python installation

if [ ! -x "$(command -v pip)" ]
then
    echo "pip not found"
    exit 1
fi

[ ! -x "$(command -v pspy)" ] && pip install -U purescripto -y --no-cache

td="`mktemp -d`"

if [ ! -x "$td" ]
then
    echo "cannot create temp directory!"    
    exit 1
fi

cd $td
mkdir pspy_executable
pspy-gen-setup > setup.py
pspy-gen-init > pspy_executable/__init__.py
pspy-get-binary pspy_executable

if [ -x "$(command -v pspy-blueprint-check)" ]
then
    pip uninstall pspy-executable -y
fi

python setup.py install

cd ~
echo "removing temp dir"
rm -rf $td