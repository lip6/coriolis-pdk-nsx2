
project(
  'coriolis-pdk-ndx2',
   version:  '2025.12.01',
   meson_version: '>= 1.2.0',
)

py       = import( 'python' ).find_installation( pure:false )
py_deps  = dependency( 'python3', required: true )
pdks_dir = py.get_install_dir() / 'pdks' / 'nsx2'

python_file = ['nsx2/__init__.py']
core2chip_files = [ 'nsx2/coriolis/core2chip/__init__.py'
                  , 'nsx2/coriolis/core2chip/cmos.py'
                  , 'nsx2/coriolis/core2chip/niolib.py']

py.install_sources( files(     python_file), subdir:'pdks/nsx2' )

py.install_sources( files(  core2chip_files), subdir:'pdks/nsx2/core2chip') 
install_subdir( 'nsx2/coriolis' , install_dir:pdks_dir )
install_subdir( 'nsx2/cells' , install_dir:pdks_dir )
install_subdir( 'nsx2/target_technologies' , install_dir:pdks_dir )


