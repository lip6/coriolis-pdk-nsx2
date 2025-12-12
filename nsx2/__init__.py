
import sys
import os
import socket
from   pathlib import Path
from   coriolis.designflow.task   import ShellEnv
from   coriolis.designflow.yosys      import Yosys
from coriolis.designflow.tasyagle import TasYagle
from coriolis.designflow.klayout  import Klayout
from coriolis.designflow.cougar   import Cougar
from coriolis.designflow.lvx      import Lvx
from coriolis.designflow.x2y      import x2y
from coriolis.designflow.iverilog import Iverilog
__all__ = [ 'setup','setup_techno' ]


TechDir          =  Path( __file__ ).parent

def setup (  ):
    ShellEnv().export()
    coriolisTechDir = TechDir / 'coriolis'
    sys.path.append( coriolisTechDir.as_posix() )

    cellsTop  = TechDir / 'cells' 
    liberty   = coriolisTechDir /'nsxlib2_techno'/ 'nsxlib2.lib'

    from coriolis          import Cfg 
    from coriolis          import Viewer
    from coriolis          import CRL 
    from coriolis.helpers   import overlay, l, u, n
    from nsxlib2_techno import techno, nsxlib2

    techno.setup( coriolisTechDir )
    nsxlib2.setup( cellsTop )
    
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.misc.catchCore              = False
        cfg.misc.info                   = False
        cfg.misc.paranoid               = False
        cfg.misc.bug                    = False
        cfg.misc.logMode                = True
        cfg.misc.verboseLevel1          = True
        cfg.misc.verboseLevel2          = True
        cfg.misc.minTraceLevel          = 1900
        cfg.misc.maxTraceLevel          = 3000
        cfg.katana.eventsLimit          = 1000000
        cfg.katana.termSatReservedLocal = 6 
        cfg.katana.termSatThreshold     = 9
        af  = CRL.AllianceFramework.get()
        Viewer.Graphics.setStyle( 'Alliance.Classic [black]' )
        env = af.getEnvironment()
        #for clk id and scale ???
        env.setCLOCK( '^sys_clk$|^ck|^jtag_tck$' )
        env.setSCALE_X( 100 )


    Yosys.setLiberty( liberty )
    stdCellLibVlog = TechDir / 'cells' /'verilog'/ 'stdcell.v'
    Iverilog.setStdCellLib( stdCellLibVlog )



    path = None
    AllianceDir =Path( __file__ ).parents[4]
    for pathVar in [ 'PATH', 'path' ]:
        if pathVar in os.environ:
            path = os.environ[ pathVar ]
            os.environ[ pathVar ] = path + ':' + (AllianceDir / 'bin').as_posix()
            break

def setup_techno(techno):
    supported_techno = {"sky130", "sg13g2", "gf180mcu"}

    if techno not in supported_techno:
        raise ValueError(
            f"Invalid technology '{techno}'. Allowed values are: sky130, sg13g2, gf180."
        )

    #  setup technology
    ShellEnv.RDS_TECHNO_NAME   = (TechDir / 'target_technologies' / f'{techno}' / 'RDS' / f'{techno}.rds').as_posix()
    ngspiceTech    = TechDir / 'target_technologies' / f'{techno}' / 'spice' / f'{techno}_models'
    if  techno == "sky130":
        techno_for_klayout = "sky130A"
    else :
        techno_for_klayout = techno

    lypFile        =  TechDir / 'target_technologies' / f'{techno}' / 'klayout'/f'{techno_for_klayout}.lyp'
    shellEnv = ShellEnv( f'{techno} Alliance Environment' )
    shellEnv[ 'MBK_CATA_LIB' ] =  TechDir / 'target_technologies' / f'{techno}' / 'spice' /'spimodel.cfg'
    shellEnv.export()
    Klayout.setLypFile( lypFile )
    TasYagle.flags         = TasYagle.Transistor
    TasYagle.SpiceType     = 'hspice'
    TasYagle.MBK_CATA_LIB  = (ngspiceTech).as_posix() + ':'+ '.'
    Lvx.MBK_CATA_LIB  = TasYagle.MBK_CATA_LIB
    x2y.MBK_CATA_LIB  = TasYagle.MBK_CATA_LIB
    TasYagle.MBK_SPI_MODEL =  TechDir / 'target_technologies' / f'{techno}' / 'spice' /'spimodel.cfg'
    Cougar.MBK_SPI_MODEL   =  TechDir / 'target_technologies' / f'{techno}' / 'spice' /'spimodel.cfg'
    TasYagle.Temperature   = 25.0
    TasYagle.VddSupply     = 1.8 
    TasYagle.VddName       = 'vdd'
    TasYagle.VssName       = 'vss'
    TasYagle.ClockName     = 'clk'

    if techno == "sky130":
        TasYagle.SpiceTrModel  = [ 'lod.spice', 
                                   'sky130_fd_pr__nfet_01v8__mismatch.corner.spice',
                                   'sky130_fd_pr__nfet_01v8__tt.corner.spice',
                                   'sky130_fd_pr__nfet_01v8__tt.pm3.spice',
                                   'sky130_fd_pr__pfet_01v8_hvt__mismatch.corner.spice',
                                   'sky130_fd_pr__pfet_01v8_hvt__tt.corner.spice',
                                   'sky130_fd_pr__pfet_01v8_hvt__tt.pm3.spice',
                                   'sky130_fd_pr__pfet_01v8__mismatch.corner.spice',
                                   'sky130_fd_pr__pfet_01v8__tt.corner.spice',
                                   'sky130_fd_pr__pfet_01v8__tt.pm3.spice']

    elif techno == "gf180mcu":
        TasYagle.SpiceTrModel  = ['typical.lib','design.ngspice','sm141064.ngspice']


    elif techno == "sg13g2":
        TasYagle.SpiceTrModel  = [ 'mos_tt.lib' ]
        TasYagle.OSDIdll       = ngspiceTech / 'psp103_nqs.osdi'

    return techno
