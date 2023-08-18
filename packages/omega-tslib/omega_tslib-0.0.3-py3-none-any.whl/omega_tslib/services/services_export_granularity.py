import pandas as pd

from datetime import datetime


class exportFile:
        
    def __init__(self, df: pd.DataFrame, df_frequency: pd.DataFrame, date_column):
        # chama o df inicial, com todas as medições do cliente
        self.df = df
        
        # chama o df de frequências
        self.df_frequency = df_frequency

        # chama a coluna de datas do dataframe
        self.date_column = date_column

        # cria as listas de granularidade
        self.lista_colunas = []
        self.lista_colunas_second = []
        self.lista_colunas_third = []
        self.lista_colunas_fourth = []


    # Método para criar o dataframe final
    def create_dataframe(self, lista, tupla, nome):
        df_final_cd = pd.DataFrame(data=lista).T
        df_final_cd.index = tupla[2]
        df_final_cd = df_final_cd.dropna(how='all')

        df_frequency_copy = self.df_frequency.drop('check', axis=1).copy()
        nome_colunas = df_frequency_copy.columns
        novos_nome_colunas = [item + suffix for item in nome_colunas for suffix in ('_du', '_fds')]
        df_final_cd.columns = novos_nome_colunas
        
        return df_final_cd.to_csv(f'{nome}.csv', sep=';')


    # Método para criar a previsão para a granularidade padrão
    def create_15_minutes(self, coluna, dataframe=None):
            
        if dataframe == None:
            dataframe = self.df
        
        lista_pontos_du = []
        lista_pontos_fds = []
        lista_tempo = []

        for tempo in range(0, 60, 15):
            tempo = str(tempo).zfill(2)

            # seta o index de acordo com date_column
            df_reset_index = dataframe.set_index(self.date_column)

            # cria uma coluna de acordo com o nome dos dias
            days = list(df_reset_index.index.day_name())
            df_reset_index['day'] = days
            
            # # reindexando e colocando um filtro para que pegue somente as linhas com as horas correspondentes
            df_reset_index = df_reset_index[df_reset_index.index.strftime('%H:%M:%S').str.endswith(f':{tempo}:00')]

            # filtra por por dia da semana
            df_reset_index_filtered_du = df_reset_index[(df_reset_index['day'] != 'Saturday') & (df_reset_index['day'] != 'Sunday')]
            df_reset_index_filtered_fds = df_reset_index[(df_reset_index['day'] == 'Saturday') | (df_reset_index['day'] == 'Sunday')]

            # faz a média somente para as HORAS correspondentes
            ponto = sum(df_reset_index_filtered_du[coluna])/(len(df_reset_index_filtered_du[coluna]))
            ponto_fds = sum(df_reset_index_filtered_fds[coluna])/(len(df_reset_index_filtered_fds[coluna]))

            # coloca valores nas listas
            lista_pontos_du.append(round(ponto, 2))
            lista_pontos_fds.append(round(ponto_fds, 2))
            lista_tempo.append(f'{tempo}')

        return (lista_pontos_du, lista_pontos_fds, lista_tempo)


    # Método para criar a previsão para a granularidade padrão
    def create_hour(self, coluna, dataframe=None):
            
        if dataframe == None:
            dataframe = self.df
        
        lista_pontos_du = []
        lista_pontos_fds = []
        lista_tempo = []

        for tempo in range(0, 24):
            tempo = str(tempo).zfill(2)

            # seta o index de acordo com date_column
            df_reset_index = dataframe.set_index(self.date_column)

            # cria uma coluna de acordo com o nome dos dias
            days = list(df_reset_index.index.day_name())
            df_reset_index['day'] = days
            
            # # reindexando e colocando um filtro para que pegue somente as linhas com as horas correspondentes
            df_reset_index = df_reset_index[df_reset_index.index.strftime('%H:%M:%S').str.endswith(f'{tempo}:00:00')]

            # filtra por por dia da semana
            df_reset_index_filtered_du = df_reset_index[(df_reset_index['day'] != 'Saturday') & (df_reset_index['day'] != 'Sunday')]
            df_reset_index_filtered_fds = df_reset_index[(df_reset_index['day'] == 'Saturday') | (df_reset_index['day'] == 'Sunday')]

            # faz a média somente para as HORAS correspondentes
            ponto = sum(df_reset_index_filtered_du[coluna])/(len(df_reset_index_filtered_du[coluna]))
            ponto_fds = sum(df_reset_index_filtered_fds[coluna])/(len(df_reset_index_filtered_fds[coluna]))

            # coloca valores nas listas
            lista_pontos_du.append(round(ponto, 2))
            lista_pontos_fds.append(round(ponto_fds, 2))
            lista_tempo.append(f'{tempo}:00:00')

        return (lista_pontos_du, lista_pontos_fds, lista_tempo)


    # Método para criar a segunda granularidade
    def create_day(self, coluna, dataframe=None):
            
        if dataframe == None:
            dataframe = self.df
        
        lista_pontos_du = []
        lista_pontos_fds = []
        lista_tempo = []

        for tempo in range(1, 31):
            tempo = str(tempo).zfill(2)
            df_reset_index = dataframe
            df_reset_index = df_reset_index.set_index(self.date_column)

            # reindexando e colocando um filtro para que pegue somente as linhas com as horas correspondentes
            df_reset_index = df_reset_index.resample('D').sum(numeric_only=True)
            df_reset_index = df_reset_index[df_reset_index.index.strftime('%Y-%m-%d').str.endswith(f'-{tempo}')]

            # cria uma coluna de acordo com o nome dos dias
            days = list(df_reset_index.index.day_name())
            df_reset_index['day'] = days
            
            df_daily_filtered_du = df_reset_index[(df_reset_index['day'] != 'Saturday') & (df_reset_index['day'] != 'Sunday')]
            df_daily_filtered_fds = df_reset_index[(df_reset_index['day'] == 'Saturday') | (df_reset_index['day'] == 'Sunday')]
            
            # cálculo dos valores médios para cada ponto
            ponto = df_daily_filtered_du[coluna].mean()
            ponto_fds =df_daily_filtered_fds[coluna].mean()

            lista_pontos_du.append(round(ponto, 2))
            lista_pontos_fds.append(round(ponto_fds, 2))
            lista_tempo.append(f'{tempo}')
                    
        return (lista_pontos_du, lista_pontos_fds, lista_tempo)


    # Método para criar a terceira granularidade
    def create_month(self, coluna, dataframe=None):
            
            if dataframe == None:
                dataframe = self.df
            
            lista_pontos_du = []
            lista_pontos_fds = []
            lista_tempo = []

            for tempo in range(1, 13):
                tempo = str(tempo).zfill(2)
                df_reset_index = dataframe
                df_reset_index = df_reset_index.set_index(self.date_column)
                
                
                # reindexando e colocando um filtro para que pegue somente as linhas com as horas correspondentes
                df_reset_index = df_reset_index.resample('MS').sum(numeric_only=True)
                df_reset_index = df_reset_index[df_reset_index.index.strftime('%Y-%m').str.endswith(f'-{tempo}')]
                
                # cálculo dos valores médios para cada ponto
                ponto = df_reset_index[coluna].mean()
                ponto_fds =df_reset_index[coluna].mean()

                lista_pontos_du.append(round(ponto, 2))
                lista_pontos_fds.append(round(ponto_fds, 2))
                lista_tempo.append(f'{tempo}')

            return (lista_pontos_du, lista_pontos_fds, lista_tempo)


    # Método para criar a quarta granularidade
    def create_year(self, coluna, dataframe=None):
            
        if dataframe == None:
            dataframe = self.df
        
        lista_pontos_du = []
        lista_pontos_fds = []
        lista_tempo = []

        for tempo in range(2019, datetime.now().year+1):
            tempo = str(tempo).zfill(2)
            df_reset_index = dataframe
            df_reset_index = df_reset_index.set_index(self.date_column)
            
            
            # reindexando e colocando um filtro para que pegue somente as linhas com as horas correspondentes
            df_reset_index = df_reset_index.resample('MS').sum(numeric_only=True)
            df_reset_index = df_reset_index[df_reset_index.index.strftime('%Y').str.endswith(f'{tempo}')]
            
            # cálculo dos valores médios para cada ponto
            ponto = df_reset_index[coluna].mean()
            ponto_fds =df_reset_index[coluna].mean()

            lista_pontos_du.append(round(ponto, 2))
            lista_pontos_fds.append(round(ponto_fds, 2))
            lista_tempo.append(f'{tempo}')
                    
        return (lista_pontos_du, lista_pontos_fds, lista_tempo)

    