from src.service import DataService
import time

def main():
    servicio = DataService()
    servicio.dataextraction()
    servicio.dataprocess()
    servicio.datawriter()

if __name__=='__main__':
    while True:
        main()
        time.sleep(3600)