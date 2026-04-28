**`pd.read_sql.query()`**: pandas.read_sql_query(sql, con, index_col=None, coerce_float=True,
                      params=None, parse_dates=None, chunksize=None,
                      dtype=None)
1. sql: query (required)
2. con: connection object (required)
3. index_col: col if any to specify for index - type *str* or *list*
4. coerce: convert non numeric to float *if possible*
5. params: list/tuple/dictionary of parameters required by the query, if any
6. parse_dates: list/dict of columns to convert to date and time
7. chunksize: return data as chunks
8. dtype: dict specifying columns' data types manually

