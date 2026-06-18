
import sys
import os
import socket
from   pathlib import Path
from   coriolis.designflow.task     import ShellEnv
from   coriolis.designflow.yosys    import Yosys
from   coriolis.designflow.tasyagle import TasYagle
from   coriolis.designflow.klayout  import Klayout
from   coriolis.designflow.lvx      import Lvx
from   coriolis.designflow.x2y      import x2y
from   coriolis.designflow.iverilog import Iverilog
from   coriolis.helpers.io          import ErrorMessage
from   coriolis.technos.common.dft  import DftStdCells

__all__ = [ 'setup', 'setup_techno' ]


packageDir = Path( __file__ ).parent


def setup ():
    global packageDir

    ShellEnv().export()
    cellsDir = packageDir / 'libs.ref' / 'nsxlib2'
    liberty  = cellsDir / 'nsxlib2.lib'

    from coriolis         import Cfg 
    from coriolis         import Viewer
    from coriolis         import CRL 
    from coriolis.helpers import overlay, l, u, n
    from .                import techno, nsxlib2

    techno.setup( packageDir )
    nsxlib2.setup( cellsDir )
    
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
    stdCellLibVlog = cellsDir / 'stdcell.v'
    Iverilog.setStdCellLib( stdCellLibVlog )


def setup_techno ( techno ):
    global packageDir

    supportedTechnos = [ "sky130", "sg13g2", "gf180mcu" ]
    if techno not in supportedTechnos:
        raise ErrorMessage( 1, [ f'nsx2.setup_techno(): Unsupported target technology "{techno}".'
                               ,  'Available technologies are "sky130", "sg13g2" and "gf180mcu".'
                               ] )

    # Setup technology
    targetDir                = packageDir / 'libs.tech' / techno
    ShellEnv.RDS_TECHNO_NAME = (targetDir / 'RDS'   / f'{techno}.rds').as_posix()
    ngspiceTech              =  targetDir / 'spice' / f'{techno}_models'
    klayoutTechno            = techno
    if techno == "sky130": klayoutTechno = "sky130A"
    lypFile                  = targetDir / 'klayout'/ f'{klayoutTechno}.lyp'

    shellEnv = ShellEnv( f'Alliance Environment for "{techno}"' )
    shellEnv[ 'MBK_CATA_LIB' ] =  targetDir / 'spice' /'spimodel.cfg'
    Klayout.setLypFile( lypFile )
    TasYagle.flags            = TasYagle.Transistor
    TasYagle.SpiceType        = 'hspice'
    TasYagle.MBK_CATA_LIB     = (ngspiceTech).as_posix() + ':.'
    Lvx.MBK_CATA_LIB          = TasYagle.MBK_CATA_LIB
    x2y.MBK_CATA_LIB          = TasYagle.MBK_CATA_LIB
    TasYagle.MBK_SPI_MODEL    = targetDir / 'spice' /'spimodel.cfg'
    ShellEnv.MBK_SPI_MODEL    = targetDir / 'spice' /'spimodel.cfg'
    TasYagle.Temperature      = 25.0
    TasYagle.VddName          = 'vdd'
    TasYagle.VssName          = 'vss'
    TasYagle.ClockName        = 'clk'
    TasYagle.VddSupply        = 1.8 

    if techno == "sky130":
        TasYagle.SpiceTrModel = [ 'lod.spice', 
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
        TasYagle.SpiceTrModel = [ 'typical.lib', 'design.ngspice', 'sm141064.ngspice' ]
        TasYagle.VddSupply    = 5.0
    elif techno == "sg13g2":
        TasYagle.SpiceTrModel = [ 'mos_tt.lib' ]
        TasYagle.OSDIdlls     = [ ngspiceTech / 'psp103_nqs.osdi' ]

    return techno


def getDftStdCells():
    dft = DftStdCells()

    # -------- FF supported --------
    dft.dff_names = [
        "sff1_x4",
        "sff1r_x4",
    ]

    # -------- Mapping FF → Scan FF --------
    dft.ff_to_scanff = {
    }

    # -------- Fallback cells (used when no scan FF is available in the library) --------
    dft.mux_name = "mx2_x2"
    dft.buf_name = "buf_x2"

    # -------- Functional FF pin mapping --------
    dft.ff_pins = {
        "d": "i",
        "q": "q",
    }

    # -------- Scan control pins (used for both native and generated scan FFs) --------
    dft.scan_pins = {
        "si": "SI",
        "se": "SE",
    }

    # -------- Mux pin mapping --------
    dft.mux_pins = {
        "i0": "i0",
        "i1": "i1",
        "sel": "cmd",
        "out": "q",
    }
    dft.scan_pins = {
        "d":  "i",  
        "si": "i1",   # scan input
        "se": "cmd",  # scan enable
        "q":  "q",   
    }
    # -------- Buffer pin mapping --------
    dft.buf_pins = {
        "i": "i",
        "z": "q",
    }

    # -------- Placement orientations --------
    dft.mux_orientation = "ID"
    dft.ff_orientation  = "ID"

    return dft
