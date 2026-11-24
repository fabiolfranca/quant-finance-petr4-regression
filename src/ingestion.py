from pathlib import Path
import pandas as pd
import yfinance as yf

def padrao_yf_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza colunas, indice de data e timezone de um DataFrame do yfinance."""
    if df.empty:
        return pd.DataFrame()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()
    date_col = "Date" if "Date" in df.columns else df.columns[0]
    df["Date"] = pd.to_datetime(df[date_col]).dt.tz_localize(None)
    if date_col != "Date":
        df = df.drop(columns=[date_col])

    return df.sort_values("Date").reset_index(drop=True)

def fetch_petr4_incremental(
    ticker: str = "PETR4.SA",
    initial_start: str = "2018-01-01",
    output_path: str = "data/01_bronze/petr4_raw.parquet",
    overlap_days: int = 2,
) -> pd.DataFrame:
  """Atualiza a camada Bronze de forma incremental.

  Na primeira execução, baixa desde `initial_start`. Nas seguintes, busca
  apenas a partir de (última data salva - `overlap_days`) para absorver
  ajustes recentes e evitar duplicidades.
  """
  path = Path(output_path)
  path.parent.mkdir(parents=True, exist_ok=True)
  asset = yf.Ticker(ticker)

  if path.exists():
    df_existing = pd.read_parquet(path)
    df_existing["Date"] = pd.to_datetime(df_existing["Date"])
    last_date = df_existing["Date"].max()

    start_date = (last_date - pd.Timedelta(days=overlap_days)).strftime(
        "%Y-%m-%d"
    )
    print(
        f"Base existente até {last_date.date()}. Buscando atualizações a partir"
        f" de {start_date}..."
    )

    df_new_raw = asset.history(start=start_date, auto_adjust=True)
    df_new = padrao_yf_dataframe(df_new_raw)

    if df_new.empty:
      print("Nenhum pregão novo retornado. Base Bronze mantida.")
      return df_existing.sort_values("Date").reset_index(drop=True)

    df_final = pd.concat([df_existing, df_new], ignore_index=True)
  else:
    print(
        f"Base Bronze não encontrada. Executando carga inicial desde"
        f" {initial_start}..."
    )
    df_init_raw = asset.history(start=initial_start, auto_adjust=True)
    df_final = padrao_yf_dataframe(df_init_raw)

    if df_final.empty:
      raise ValueError(f"Nenhum dado retornado para {ticker}.")

  # Garante unicidade por data (mantém o dado mais recente em caso de ajuste)
  df_final = (
      df_final.drop_duplicates(subset=["Date"], keep="last")
      .sort_values("Date")
      .reset_index(drop=True)
  )

  df_final.to_parquet(path, index=False)
  print(
      f"Camada Bronze atualizada! Total de linhas: {len(df_final)} | Última"
      f" data: {df_final['Date'].max().date()}"
  )
  return df_final


if __name__ == "__main__":
  df_bronze = fetch_petr4_incremental()
  print(df_bronze.tail())