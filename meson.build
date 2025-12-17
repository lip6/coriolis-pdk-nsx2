
project(
  'coriolis-pdk-ndx2',
   version:  '2025.12.01',
   meson_version: '>= 1.2.0',
)

py       = import( 'python' ).find_installation( pure:false )
py_deps  = dependency( 'python3', required: true )
pdks_dir = py.get_install_dir() / 'pdks' / 'nsx2'

setup_files = [ 'libs.tech/coriolis/__init__.py'
              , 'libs.tech/coriolis/nsxlib2.py'
              , 'libs.tech/coriolis/techno.py'
              , 'libs.tech/coriolis/techno_symb.py'
              ]
py.install_sources( files(setup_files), subdir:'pdks/nsx2' )

install_data  ( 'libs.tech/coriolis/symbolic.graal', install_dir:pdks_dir )
install_data  ( 'libs.tech/coriolis/symbolic.dreal', install_dir:pdks_dir )
install_data  ( 'libs.tech/coriolis/sg13g2.rds'    , install_dir:pdks_dir )
install_subdir( 'libs.tech/gf180mcu'               , install_dir:pdks_dir / 'libs.tech' )
install_subdir( 'libs.tech/sg13g2'                 , install_dir:pdks_dir / 'libs.tech' )
install_subdir( 'libs.tech/sky130'                 , install_dir:pdks_dir / 'libs.tech' )
install_subdir( 'libs.ref'                         , install_dir:pdks_dir )
