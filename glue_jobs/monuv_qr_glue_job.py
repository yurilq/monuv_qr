import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Importa a função custom_transformation do script glue_job_script.py
from glue_job_script import custom_transformation

# Inicialização do contexto do Glue e do job
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leitura dos dados do catálogo do Glue ou de outra fonte
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="monuv_qr_database", 
    table_name="monuv_qr_table",
    transformation_ctx="datasource"
)

# Conversão para DataFrame do Spark
df = datasource.toDF()

# Aplicação das transformações personalizadas
transformed_df = custom_transformation(df)

# Armazenamento dos dados transformados no S3 em formato Parquet
transformed_df.write \
    .format("parquet") \
    .mode("overwrite") \
    .save("s3://monuv-transformed-data-bucket/transformed-data/")

# Finalização do job
job.commit()
