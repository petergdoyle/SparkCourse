#!/bin/sh

for each in $(find /usr/spark/default/bin/ -executable -type f) ; do
  name=$(basename $each)
  alternatives --install "/usr/bin/$name" "$name" "$each" 99999
done
