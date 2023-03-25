import requests
import gzip
import pandas as pd
import logging
import urllib.request
from dataclasses import dataclass
from glob import glob
from src.model import datapath,datadependencies,infomessages,warningmessages

logger = logging.getLogger(__name__)
@dataclass
class DataExtract:
    """
    Definición de extracción de datos necesarios para la ejecución del proceso
    """
    data:pd.DataFrame = None
    datahist:pd.DataFrame = None
    datamunicipios:pd.DataFrame = None
    def loadws(self):
        """
        Define extracción de datos desde el webservice
        """
        response = requests.get(datadependencies.URLWS.value)
        dataws = response.content
        try:
            dataunzip = gzip.decompress(dataws)
            dataunzip = dataunzip.decode()
            dataunzip = pd.read_json(dataunzip,compression='gzip')
            logger.info(infomessages.wstrue.value)
        except Exception as err:
            logger.warning(warningmessages.wsfalse.value+' {response.status_code}: {err}')
            self.data = pd.DataFrame()
        else:
            self.data = dataunzip.copy()
    def loadftp(self):
        """
        Define extracción de datos desde el servicio FTP
        """
        urllib.request.urlretrieve(datadependencies.URLFTP.value, datapath.GZFILE.value)
        try:
            dataftp = pd.read_json(datapath.GZFILE.value,compression='gzip')
            logger.info(infomessages.ftptrue.value)
        except Exception as err:
            logger.error(warningmessages.ftpfalse.value+f' {err}')
            self.data = None
        else:
            self.data = dataftp.copy()
    def get_data(self):
        """
        Extracción de datos según la fuente disponible
        """
        self.loadws()
        if self.data.empty:
            self.loadftp()
    def loadhist(self):
        """
        Carga de datos del procesamiento anterior
        """
        pathdatahist = datapath.ZONAFOLDER.value
        pathfiles = [glob(pathzone+datapath.CURRENTFILE.value)[0] for pathzone in glob(pathdatahist+'*') if glob(pathzone+datapath.CURRENTFILE.value)]
        if pathfiles:
            datafiles = [pd.read_csv(file,header=0) for file in pathfiles if file]
            databefore = pd.concat(datafiles,ignore_index=True)
            self.datahist = databefore.copy()
        else:
            self.datahist = pd.DataFrame()
    def loadmun(self):
        """
        Carga de datos más recientes de la fuente data_municipios
        """
        pathdatamun = datapath.MUNFOLDER.value
        pathlastdata = glob(pathdatamun)[-1]
        datamunlast = pd.read_csv(pathlastdata,header=0)
        self.datamunicipios = datamunlast.copy()