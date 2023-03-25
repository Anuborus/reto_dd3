from dataclasses import dataclass
import pandas as pd
from datetime import datetime
import os
from src.model import datapath,datacolumn
from pathlib import Path
@dataclass
class DataLoader:
    """
    Permite crear los directorios donde posteriormente se almacenaran los datos
    """
    zones:pd.Series
    datacurr:pd.DataFrame
    datamean:pd.DataFrame = None
    datamerge:pd.DataFrame = None
    @staticmethod
    def _checkzonefolder(zone:str):
        """
        Comprueba si el directorio del número zona existe, 
        en caso de que no exista lo crea
        """
        zonepath = datapath.ZONAFOLDER.value+zone
        if not os.path.exists(zonepath):
            os.mkdir(zonepath)
    @staticmethod
    def _makeprocessfolder(zone:str):
        """
        Crea la carpeta según la fecha y hora de procesamiento, 
        donde se almacenaran los datos
        """
        processdatetime = datetime.now()
        processfolder = str(Path(__file__).root)+processdatetime.strftime("%Y%m%dT%H")
        processpath = datapath.ZONAFOLDER.value+zone+processfolder
        if not os.path.exists(processpath):
            os.mkdir(processpath)
        return processpath
    def savefinaldata(self):
        """
        Guarda los datos de promedios por municipio (Punto 2) y
        los datos cruzados contra la data_municipios (Punto 3)
        """
        for zone in self.zones:
            self._checkzonefolder(zone)
            pathzone = self._makeprocessfolder(zone)
            datazonemean = self.datamean[self.datamean[datacolumn.ides.name]==zone].copy()
            datazonemean.to_csv(pathzone+datapath.MUNFILE.value,index=False)
            datazonemerge = self.datamerge[self.datamerge[datacolumn.ides.name]==zone].copy()
            datazonemerge.to_csv(pathzone+datapath.MERGEFILE.value,index=False)
    def savecurrdata(self):
        """
        Guarda los datos más recientes (Punto 4)
        """
        for zone in self.zones:
            pathzonecurr = datapath.ZONAFOLDER.value+zone
            datazonecurr = self.datacurr[self.datacurr[datacolumn.ides.name]==zone].copy()
            datazonecurr.to_csv(pathzonecurr+datapath.CURRENTFILE.value,index=False)

        
        

