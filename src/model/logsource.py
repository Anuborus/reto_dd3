from enum import Enum,auto
from pathlib import Path
class logconfig(Enum):
    file = '.'+str(Path(str(Path(__file__).root)).joinpath('log','main.log'))
    formatlog = '%(asctime)s, %(message)s'
    dateformat = '%m/%d/%Y %I:%M:%S %p'
class infomessages(Enum):
    startservice = 'Iniciando ejecución de servicio'
    endservice = 'Finalizando ejecución de servicio'
    extracttrue = 'Datos extraídos correctamente'
    processtrue = 'Datos Procesados correctamente'
    writetrue = 'Datos Cargados correctamente'
    wstrue = 'WS Cargado Satisfactoriamente'
    ftptrue = 'FTP Cargado Satisfactoriamente'
    initsource = 'Se crea estructura inicial'
class warningmessages(Enum):
    wsfalse = 'Error WS código'
    ftpfalse = 'Error FTP:'
