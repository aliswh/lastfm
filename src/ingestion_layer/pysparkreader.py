from .abstract_ingestion_layer import Reader
from .config import *
import pyspark

class PySparkReader(Reader):
    def __init__(self, pysparksession, creds_path=CREDS_PATH, bucket=BUCKET_NAME):
        self.dest = pysparksession
        self.bucket = bucket
        self.dest._jsc.hadoopConfiguration().set("google.cloud.auth.service.account.json.keyfile",'./lastfm/src/ingestion_layer/'+creds_path)

    def read(self, path, dir = False):
        """ Reads from a Google Storage path and return an rdd
        """
        path = f'gs://{self.bucket}/'+path
        if dir:
            path = path+'/*'
        df = self.dest.read.option("multiline","true").json(path).cache()
        return df.rdd.map(lambda x: pyspark.sql.Row.asDict(x)).persist()
            