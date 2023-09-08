import pandas as pd
import polars as pl
import functools
import numpy as np


df = pl.DataFrame({'a': [1, 2.5, None, 10], 'b': ['t1', 't2', 't3', 't4'], 'c': ['t2.12', '2', '5,', '1']})

print(df)

df = df.with_columns(pl.concat_str((pl.col('a').cast(str) + '---' + pl.col('b'))))

print(df)

df = df.with_columns(pl.when(functools.reduce(lambda x, y: x | y, [pl.col('b').str.contains('2|3'), pl.col('b').str.contains('2')])).
                     then(pl.lit(True).alias('a')).
                     otherwise(pl.lit(False).alias('a')))

print(df)

print(pd.DataFrame(pd.Series([0.1, np.nan])).replace({np.nan:None}).to_dict(orient='records'))

df = df.with_columns(pl.when(pl.col('b') > '2').then(pl.lit("Nice").alias('new_k')).fill_null(0))
print(df)

df = df.with_columns(pl.col('c').str.contains(r'\d[. ,]\d').alias('test'))

print(df)

df = pl.DataFrame({'a': [1, 2.5, None, 10, 6], 'b': ['t1aaat2t2kkkkkt4', 't2kkkkkt4', 't3yyyyyyt1', 't4t5', 't5']})
regexp = r'(t\d).*?(t\d)'

df = df.with_columns(pl.col('b').str.extract(regexp).alias('extracted'))
print(df)

df = pl.extract_groups(df['b']).alias('extracted')
print(df)


# rows = rows.with_columns(pl.col(source_fld).str.extract_groups(r'(\d+)\s*[-:]\s*(\d+)').alias('tmp_range'))
#             rows = rows.with_columns(pl.when(pl.col('tmp_range').struct[0].is_not_null() &
#                                              pl.col('tmp_range').struct[1].is_not_null() & global_condition)
#                                      .then(self.agg_func(pl.col('tmp_range').struct[0].cast(int),
#                                                          pl.col('tmp_range').struct[1].cast(int)).alias(self.sel_fld))
#                                      .when(pl.col(source_fld).str.extract(r'(\d+)').is_not_null() & global_condition)
#                                      .then(pl.col(source_fld).str.extract(r'(\d+)').cast(int).alias(self.sel_fld))
#                                      .otherwise(pl.col(self.sel_fld)))