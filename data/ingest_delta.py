from deltalake import write_deltalake
import pandas as pd

df = pd.DataFrame([
    {"doc_id": "doc_1", "text": "Azure is a cloud platform by Microsoft."},
    {"doc_id": "doc_2", "text": "Delta Lake is optimized for large-scale data lakes."}
])

write_deltalake("data/delta/docs", df, mode="overwrite")