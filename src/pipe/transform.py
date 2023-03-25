import pandas as pd
from dataclasses import dataclass
from src.model import datacolumn,datafilter,dataresult
@dataclass
class Process:
    """
    Procesa la información para manejo y visualización de manera adecuada
    """
    datasource:pd.DataFrame
    databefore:pd.DataFrame = None
    datamunicipios:pd.DataFrame = None
    def lastid(self):
        """
        Extrae la información mas reciente de la fuente inicial (Web),
        realiza formateo de identificadores y modelamiento de datos
        """
        self.dataprocess = self.datasource.copy()
        self.dataprocess[datacolumn.dloc.name] = pd.to_datetime(self.dataprocess[datacolumn.dloc.name])
        self.dataprocess[datacolumn.idmun.name] = self.dataprocess[datacolumn.idmun.name].apply(lambda x: '{:0>3d}'.format(x))
        self.dataprocess[datacolumn.ides.name] = self.dataprocess[datacolumn.ides.name].apply(lambda x: '{:0>2d}'.format(x))
        self.dataprocess = self.dataprocess.astype({datacolumn.ides.name:str,datacolumn.idmun.name:str})
        self.dataprocess[datacolumn.idgeneral.name] = self.dataprocess[datacolumn.ides.name]+self.dataprocess[datacolumn.idmun.name]
        self.dataprocess = self.dataprocess.sort_values([datacolumn.idgeneral.name, datacolumn.dloc.name]).copy()
        self.dataprocess = self.dataprocess.groupby(datacolumn.idgeneral.name).tail(1)
        self.dataprocess.reset_index(inplace=True,drop=True)
        self.dataprocess = self.dataprocess[datafilter.columns.value]
    def datamean(self):
        """
        Cálculo de promedios entre los datos de las dos últimas horas
        """
        self.databefore[datacolumn.idgeneral.name] = self.databefore[datacolumn.idgeneral.name].apply(lambda x: '{:0>5d}'.format(x))
        self.databefore[datacolumn.idmun.name] = self.databefore[datacolumn.idmun.name].apply(lambda x: '{:0>3d}'.format(x))
        self.databefore[datacolumn.ides.name] = self.databefore[datacolumn.ides.name].apply(lambda x: '{:0>2d}'.format(x))
        self.databefore = self.databefore.astype({datacolumn.ides.name:str,datacolumn.idmun.name:str})
        self.datamunmean = pd.concat([self.databefore,self.dataprocess],ignore_index=True)
        self.datamunmean = self.datamunmean.groupby([datacolumn.idgeneral.name,datacolumn.ides.name,datacolumn.idmun.name],as_index=False).agg(dataresult.measure.value)
    def datamun(self):
        """
        Combinación de datos entre los promedios y data_municipios más reciente
        """
        self.datamunicipios[datacolumn.Cve_Ent.name] = self.datamunicipios[datacolumn.Cve_Ent.name].apply(lambda x: '{:0>2d}'.format(x))
        self.datamunicipios[datacolumn.Cve_Mun.name] = self.datamunicipios[datacolumn.Cve_Mun.name].apply(lambda x: '{:0>3d}'.format(x))
        self.datamunicipios = self.datamunicipios.astype({datacolumn.Cve_Ent.name:str,datacolumn.Cve_Mun.name:str})
        self.datamunicipios[datacolumn.idgeneral.name] = self.datamunicipios[datacolumn.Cve_Ent.name]+self.datamunicipios[datacolumn.Cve_Mun.name]
        self.datamunicipios = self.datamunicipios[[datacolumn.idgeneral.name,datacolumn.Value.name]]
        self.datamerge = self.datamunmean.merge(self.datamunicipios,on=datacolumn.idgeneral.name,how='left')
    @property
    def getdatacurr(self) -> pd.DataFrame:
        return self.dataprocess.copy()
    @property
    def getdatamean(self) -> pd.DataFrame:
        return self.datamunmean.copy()
    @property
    def getdatamerge(self) -> pd.DataFrame:
        return self.datamerge.copy()