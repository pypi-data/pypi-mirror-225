TencentCloud DLC Connector
========================


提供符合 `DB-API 2.0` 标准的库，用于连接 `DLC` 引擎，执行SQL


### 安装
```bash
pip install tencentcloud-dlc-connector
```


### 使用
``` python
import tdlc_connector

conn = tdlc_connector.connect(region="<REGION>", 
    secret_id="<SECRET_ID>", 
    secret_key="<SECRET_KEY>",
    engine="<ENGINE>",
    engine_type=constants.EngineTypes.PRESTO, 
    result_style=constants.ResultStyles.DICT)

conn.open()
cursor = conn.cursor()

count = cursor.execute("SELECT 1")

for row in cursor.fetchall():
    print(row)

```