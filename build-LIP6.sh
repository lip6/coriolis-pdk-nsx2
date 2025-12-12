#!/bin/sh

    rootDir="${HOME}/coriolis-2.x"
   buildDir="${rootDir}/release/nsx2"
 installDir="${rootDir}/release/install"
 rm -rf ${buildDir}
 rm -rf ${installDir}/lib64/python3.9/site-packages/pdks/nsx2
 meson setup --prefix ${installDir} ${buildDir}
 meson install -C ${buildDir}
