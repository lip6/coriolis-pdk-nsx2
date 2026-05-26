
   packageName="coriolis-pdk-nsx2"
  venvVersion="2.5.5"
 venvSnapshot="venv-al9-${venvVersion}.tar.gz"
      version="2025.12.31"
    obsCI_CNT="10"
     obsB_CNT="1"

 rpmSources=""
 rpmSources="${rpmSources} packaging/coriolis-pdk-nsx2.spec"
 rpmSources="${rpmSources} packaging/coriolis-pdk-nsx2-rpmlintrc"
 rpmSources="${rpmSources} packaging/patchvenv.sh"
 rpmSources="${rpmSources} ${venvSnapshot}"
 rpmSources="${rpmSources} coriolis-pdk-nsx2-${version}.tar.gz"

 debSources=""
 debSources="${debSources} packaging/coriolis-pdk-nsx2.dsc"
 debSources="${debSources} packaging/coriolis-pdk-nsx2-deblintrc"
 debSources="${debSources} packaging/debian.changelog"
 debSources="${debSources} packaging/debian.control"
 debSources="${debSources} packaging/debian.copyright"
 debSources="${debSources} packaging/debian.rules"


 echo "Running uploadOBSs.sh"

 source ./packaging/uploadUtils.sh

     doVEnv="false"
   doCommit="false"

 parseArguments $*
 simpleBuildArchive
 runDoVEnv
 copyFiles
 buildObs
 buildLocalRpm
