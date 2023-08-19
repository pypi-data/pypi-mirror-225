import pandas as pd
import pkg_resources

abs_file_path = pkg_resources.resource_filename("cpilib", "data/hicp_labels.parquet")
coicop_labels = pd.read_parquet(abs_file_path)
