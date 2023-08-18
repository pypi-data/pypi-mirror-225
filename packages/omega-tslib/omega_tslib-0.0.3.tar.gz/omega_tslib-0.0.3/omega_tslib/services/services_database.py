import os
from omegaanalytics import omega_cloud

def get_medicao_scde(SnowflakeSession: omega_cloud.Snowflake):
   # definições das querys de entrada
    query = f"""
    with a as(
        select * from energy_prod.smf.ccee_medicao
    ),
    b as (
        select distinct descricao, cod_ccee from energy_prod.d_hub.d_medidor
    )
    select 
        to_timestamp(a.timestamp) as timestamp,
        b.descricao as nm_ponto, 
        a.nm_ponto_cod, 
        a.subtipo, a.status, 
        to_number(a.geracao_ativa, 20, 6) geracao_ativa, 
        a.geracao_reativa, 
        to_number(a.consumo_ativo, 20, 6)  consumo_ativo,
        a.consumo_reativo, 
        a.datetime_upload
    from 
        a
    inner join 
        b
    on 
        a.nm_ponto_cod = b.cod_ccee
    where 
        timestamp >= dateadd(day, -120, current_date())
    order by
        timestamp;
    """

    return SnowflakeSession.query(query)

def get_medicao_contratos(SnowflakeSession: omega_cloud.Snowflake):
   # definições das querys de entrada
    query = f"""
    select 
        ID, AMBIENTE,
        TO_CHAR(TO_DATE(data), 'YYYY-MM-DD') DATA, 
        VENDEDOR, COMPRADOR, SUBMERCADO, TIPO_FONTE, 
        CAST(REPLACE(MW_MED, ',', '') AS FLOAT) MW_MED, 
        FLEX_INFERIOR, FLEX_SUPERIOR, SAZO_INFERIOR, 
        SAZO_SUPERIOR, 
        CAST(REPLACE(MW_MED_SAZO, ',', '') AS FLOAT) MW_MED_SAZO, 
        FLEX_EXERCIDA, SAZO_EXERCIDA, 
        CAST(REPLACE(MW_MED_FINAL, ',', '') AS FLOAT) MW_MED_FINAL, 
        CAST(REPLACE(MW_HORA_FINAL, ',', '') AS FLOAT) MW_HORA_FINAL, 
        TIPO_PRECO, PRECO_NOMINAL, INDICE_REAJUSTE, 
        VALOR_INDICE_REAJUSTE,
        to_timestamp(DATA_BASE_REAJUSTE) DATA_BASE_REAJUSTE,
        MES_REAJUSTE, DATA_REAJUSTE, PRECO_REAJUSTADO,
        AJUSTE_PRECO, ECONOMIA, VALOR_NF,
        TO_TIMESTAMP(DATETIME_CRIACAO) DATETIME_CRIACAO,
        CLASSIFICACAO,
        to_timestamp(DATA_PRIMEIRO_REAJUSTE) DATA_PRIMEIRO_REAJUSTE,
        to_timestamp(UPDATE_TIMESTAMP) UPDATE_TIMESTAMP    
    from 
        COMERCIALIZACAO_PROD.FORECAST.F_CONTRATOS_FORECAST;
    """

    return SnowflakeSession.query(query)


def get_medicao_carteira(SnowflakeSession: omega_cloud.Snowflake, ano: int):
   # definições das querys de entrada
    query = f"""
    with medidores as (
        select carga, max(TRY_CAST(COD_CARGA AS INT)) AS COD_CARGA 
        from comercializacao_prod.mercado_livre.d_medidores
        group by carga
    )
    ,
    infomercado as (
        select ano_mes, hora, sigla, cod_carga, consumo_livre_ajustado_mwh, consumo_total_ajustado from COMERCIALIZACAO_DEV.MIDDLE_PRECO.F_INFOMERCADO_HORARIO
    )
    ,
    c1 as (
        select to_timestamp(i.ano_mes || ' ' || i.hora || ':00:00') as data_hora, m.cod_carga, i.sigla, i.consumo_livre_ajustado_mwh, i.consumo_total_ajustado 
        from infomercado as i
        join medidores m
        on i.cod_carga = m.cod_carga
    )

    select * from c1 where year(data_hora) = {ano} order by data_hora desc
    ;
    """

    return SnowflakeSession.query(query)
