from src.pipe import Process,DataLoader,DataExtract
from src.model import datacolumn,logconfig,infomessages
from dataclasses import dataclass
import logging
logging.basicConfig(filename=logconfig.file.value,   
                    level=logging.DEBUG,
                    format=logconfig.formatlog.value,
                    datefmt=logconfig.dateformat.value)

@dataclass
class DataService:
    logging.info(infomessages.startservice.value)
    def dataextraction(self):
        """
        Extracción de datos fuente web y carga de datos fuentes locales
        """
        self.dataread = DataExtract()
        self.dataread.get_data()
        self.dataread.loadhist()
        if self.dataread.datahist.empty:
            self.datainit()
        self.dataread.loadmun()
        logging.info(infomessages.extracttrue.value)
    def dataprocess(self):
        """
        Procesamiento de datos cargados desde las distintas fuentes, organización,
        limpieza, filtrado y cambios en tipos de datos
        """
        pipeline = Process(datasource=self.dataread.data,
                        databefore=self.dataread.datahist,
                        datamunicipios=self.dataread.datamunicipios)
        pipeline.lastid()
        pipeline.datamean()
        pipeline.datamun()
        self.data_current = pipeline.getdatacurr
        self.data_mean = pipeline.getdatamean
        self.data_merge = pipeline.getdatamerge
        self.zones = self.data_current[datacolumn.ides.name].drop_duplicates().copy()
        logging.info(infomessages.processtrue.value)
    def datawriter(self):
        """
        Escritura de datos en las diferentes carpetas y "tablas" correspondientes
        """
        dataload = DataLoader(self.zones,datacurr=self.data_current,
                            datamean=self.data_mean,
                            datamerge=self.data_merge)
        dataload.savefinaldata()
        dataload.savecurrdata()
        logging.info(infomessages.writetrue.value)
        logging.info(infomessages.endservice.value)
    def datainit(self):
        pipeline_init = Process(datasource=self.dataread.data)
        pipeline_init.lastid()
        data_init = pipeline_init.getdatacurr
        zones_init = data_init[datacolumn.ides.name].drop_duplicates().copy()
        dataload_init = DataLoader(zones_init,datacurr=data_init)
        for init_zone in zones_init:
            dataload_init._checkzonefolder(init_zone)
        dataload_init.savecurrdata()
        self.dataread.loadhist()
        logging.debug(infomessages.initsource.value)