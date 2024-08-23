import sys
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

def custom_transformation(df: DataFrame) -> DataFrame:
    """
    Aplica transformações customizadas ao DataFrame.
    Neste caso, remove registros com conteúdo de QR Code nulo e formata colunas.
    """
    # Filtra registros com QR Content nulo
    df = df.filter(F.col("QrContent").isNotNull())
    
    # Adiciona uma nova coluna de data formatada a partir do Timestamp
    df = df.withColumn("FormattedDate", F.date_format(F.col("Timestamp"), "yyyy-MM-dd"))
    
    # Exemplo de outras transformações: Normalização de texto
    df = df.withColumn("QrContent", F.upper(F.col("QrContent")))
    
    return df

def main():
    # Captura argumentos passados ao script
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    
    # Configuração do contexto Glue
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    
    # Leitura dos dados do catálogo Glue ou de uma fonte especificada
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="monuv_qr_database", 
        table_name="monuv_qr_table",
        transformation_ctx="datasource"
    )
    
    # Conversão para DataFrame do Spark para aplicar transformações
    df = datasource.toDF()
    
    # Aplicação das transformações customizadas
    transformed_df = custom_transformation(df)
    
    # Armazenamento dos dados transformados no S3 em formato Parquet
    transformed_df.write \
        .format("parquet") \
        .mode("overwrite") \
        .save("s3://monuv-transformed-data-bucket/transformed-data/")
    
    job.commit()

if __name__ == "__main__":
    main()
