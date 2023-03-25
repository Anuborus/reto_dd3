from enum import Enum,auto
from pathlib import Path

class datadependencies(Enum):
    URLWS = 'https://smn.conagua.gob.mx/webservices/index.php?method=1'
    URLFTP = 'ftp://ftp.conagua.gob.mx/pronosticoporciudades/DailyForecast_MX.gz'
class datapath(Enum):
    HOME = str(Path(__file__).parent.parent)
    GZFILE = str(Path(HOME).joinpath('data','data_ftp','DailyForecast_MX.gz'))
    ZONAFOLDER = str(Path(HOME).joinpath('data','data_result','zonas'))+str(Path(__file__).root)
    MUNFOLDER = str(Path(HOME).joinpath('data','data_municipios','*','data.csv'))
    MUNFILE = str(Path(__file__).root)+'municipios_mean.csv'
    CURRENTFILE = str(Path(__file__).root)+'current.csv'
    MERGEFILE = str(Path(__file__).root)+'merge.csv'

class datacolumn(Enum):
    dloc = auto()
    idmun = auto()
    ides = auto()
    idgeneral = auto()
    Cve_Ent = auto()
    Cve_Mun = auto()
    Value = auto()

class datafilter(Enum):
    columns = ['idgeneral','ides','idmun','nes','nmun','prec','tmax','tmin']

class dataresult(Enum):
    measure = {'prec':'mean','tmax':'mean','tmin':'mean'}
