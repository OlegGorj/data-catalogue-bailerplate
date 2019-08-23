
# Data models for data catalog

Deploy structures:


```
TARGET_PRJ=<your target project>

# init config with target project
gcloud init

bq mk --dataset ${TARGET_PRJ}:data_catalog
bq mk --table ${TARGET_PRJ}:data_catalog.data_catalog  ./data_catalog.data_catalog.json
bq mk --table ${TARGET_PRJ}:data_catalog.data_providers  ./data_catalog.data_providers.json

```


Backup data catalog structures:


```
bq show --schema data_catalog.data_catalog > data_catalog.data_catalog.json
bq show --schema data_catalog.data_providers > data_catalog.data_providers.json

```
