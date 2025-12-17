
  venvVersion="2.5.5"
 venvSnapshot="venv-al9-${venvVersion}.tar.gz"
      version="2025.12.31"
       obsDir="../coriolis-obs/home:jpc-lip6/coriolis-pdk-nsx2"

 printHelp () {
   echo ""
   echo "  Usage: uploadOBSs.sh [--sources] [--venv] [--commit] [--all]"
   echo ""
   echo "  Options:"
   echo "    [--sources] : Build an archive from the HEAD of the current branch."
   echo "    [--venv]    : Copy the venv snapshot from coriolis-eda OBS local checkout."
   echo "                    <./coriolis-obs/home:jpc-lip6/coriolis-eda/${venvSnapshot}>"
   echo "    [--commit]  : Push the files (commit) on the remote builder repository."
   echo "                  This will effectively triggers the rebuild of the packages."
   echo "                  OBS local repository is hardwired to:"
   echo "                      \"${obsDir}\""
   echo "    [--all]     : Perform all actions at once."
   echo ""

 }

 if [ $# -eq 0 ]; then printHelp; fi

    githash=`git log -1 --pretty=format:%h`
  doSources="false"
     doDocs="false"
     doVEnv="false"
   doCommit="false"
 badAgument=""
 while [ $# -gt 0 ]; do
   case $1 in
     --sources) doSources="true";;
     --commit)  doCommit="true";;
     --all)     doSources="true"
                doDocs="true"
                doVEnv="true"
                doCommit="true";;
     *)         badArgument="$1";;
   esac
   shift
 done
 if [ ! -z "${badArgument}" ]; then
   echo "[ERROR] uploadOBS.sh: Unknown argument \"${badArgument}\"."
   exit 1
 fi

 echo "Running uploadOBSs.sh"
 echo "* Using HEAD githash as release: ${githash}."
 if [ "${doSources}" = "true" ]; then
   echo "* Making source file archive from Git HEAD ..."
   ./packaging/git-archive-all.sh -v --prefix coriolis-pdk-nsx2-${version}/ \
                                     --format tar.gz \
                                     coriolis-pdk-nsx2-${version}.tar.gz
 fi

 if [ "${doVenv}" = "true" ]; then
   if [ -f "${obsDir}/${venvSnapshot}" ]; then
     echo "* Venv snaphot already copied."
   else
     referenceVenvSnapshot="../coriolis-eda/${venvSnapshot}"
     if [ ! -f "${referenceVenvSnapshot}" ]; then
       echo "[ERROR] Venv snapshot reference not found in <${referenceVenvSnapshot}>."
       echo "        You must checkout the coriolis-eda project *or*, if it is already there,"
       echo "        actually make the snapshot from it."
       exit 1
     fi
     cp ${referenceVenvSnapshot} .
   fi
 fi

 echo "* Update files in OBS project directory."
 echo "  OBS package directory: \"${obsDir}\"."
 for distribFile in packaging/coriolis-pdk-nsx2.spec      \
                    packaging/coriolis-pdk-nsx2-rpmlintrc \
                    packaging/patchvenv.sh                \
                    ${venvSnapshot}                       \
                    coriolis-pdk-nsx2-${version}.tar.gz   \
                    packaging/coriolis-pdk-nsx2.dsc       \
                    packaging/coriolis-pdk-nsx2-rpmlintrc \
                    packaging/debian.changelog            \
                    packaging/debian.control              \
                    packaging/debian.copyright            \
                    packaging/debian.rules                \
                    ; do
   if [ ! -f "${distribFile}" ]; then continue; fi
   if [[ "${distribFile}" == packaging* ]]; then
     echo "  - copy ${distribFile}."
     cp ${distribFile} ${obsDir}
   else
     echo "  - move ${distribFile}."
     mv ${distribFile} ${obsDir}
   fi
 done
 
 sed -i "s,^Release: *1,Release:        <CI_CNT>.<B_CNT>.${githash}," ${obsDir}/coriolis-pdk-nsx2.spec
 if [ "${doCommit}" = "true" ]; then
   pushd ${obsDir}
   osc add *
   osc commit
   popd
 fi

