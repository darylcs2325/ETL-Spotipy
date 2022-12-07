import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from model import TABLENAME
from cfg import DB_CONNSTR
from cfg import data

sp = data()


def extract(date, limit=50):
    """Función para la extración de datos

    Args:
        date (date): desde que fecha queremos obtener los datos hasta la
                     actualidad.
        limit (int): número de entidades para retornar.

        after (int): marca de tiempo en milisegundos, devuelve todos los
                     elementos después de esta marca.

    Returns:
        diccionario: Valores que nos entrega la API
    """
    ds = int(date.timestamp())*1000
    return sp.current_user_recently_played(limit=limit, after=ds)


def transform(raw_data):
    """Transformamos la data que extraemos

    Args:
        raw_data (dict): Valores que nos entrega la API

    Raises:
        Exception: Valores de played_at no únicos
        Exception: Valores nulos en el df

    Returns:
        dataframe: DF con los datos que nos interesa (played_at, artist,
                                                      duration, album,
                                                      popularity)
    """
    data = []
    for r in raw_data["items"]:
        data.append({
            "played_at": r["played_at"],
            "artist": r["track"]["artists"][0]["name"],
            "duration": r["track"]["duration_ms"],
            'album': r["track"]['album']['name'],
            'popularity': r["track"]["popularity"]
        })

    df = pd.DataFrame(data)

    # Asegurarnos que los valores played_at son únicos
    if not df["played_at"].is_unique:
        raise Exception("El valor de played_at no es única")

    # Vemos si hay al menos un valor nulo en el df
    if df.isnull().values.any():
        raise Exception("Un valor del df es nulo")
        
    print(df)
    return df


def load(df):
    """Función para la carga de los datos

    Args:
        df (dataframe): Dataframe obtenida de los datos transformados   
    """
    print(f"Enviando {df.shape[0]} al db")
    engine = create_engine(DB_CONNSTR)
    df.to_sql(TABLENAME, con=engine, index=False, if_exists="replace")


if __name__ == "__main__":
    date = datetime.today() - timedelta(days=1)

    # Extract
    raw_data = extract(date)
    # Transform
    df = transform(raw_data)

    # Load
    load(df)
    print("Done")
