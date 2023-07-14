from dvc import api
import pandas as pd
from io import StringIO
import sys
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.INFO,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)

logger=logging.getLogger(__name__)

logging.info('Cargando data')

# Leer archivos .dvc de manera string
movie_data_path = api.read("dataset/movies.csv",
                           remote='dataset-track')
opening_data_path = api.read("dataset/opening_gross.csv",
                           remote='dataset-track')
finantials_data_path = api.read("dataset/finantials.csv",
                           remote='dataset-track')

#convertir en dataFrames
fin_data=pd.read_csv(StringIO(finantials_data_path))
movie_data=pd.read_csv(StringIO(movie_data_path))
opening_data=pd.read_csv(StringIO(opening_data_path))

num_col_mask=(movie_data.dtypes == float) \
    | (movie_data.dtypes == int)

num_cols=[col for col in num_col_mask.index if num_col_mask[col]]
movie_data=movie_data[num_cols+['movie_title']]

fin_data= fin_data[['movie_title',
                    'production_budget',
                    'worldwide_gross']]

fin_movie_data=pd.merge(fin_data,
                        movie_data,
                        on="movie_title",
                        how="left")

full_movie_data=pd.merge(opening_data,
                         fin_movie_data,
                         on="movie_title",
                         how="left")

full_movie_data=full_movie_data.drop(['gross',"movie_title"],
                                      axis=1)

full_movie_data.to_csv("dataset/full_data.csv",
                       index=False)

#Punto para romper el script:bandera para mirar el
#funcionamiento hasta ese punto
#breakpoint()

logger.info("Data cargada y lista ...")