### 新增百度的关键词汇总

位置 : baidu.kw_tools.py

1. KeywordSummary
2. KeywordAggregator

### Langchain相关工具的封装

1. eg1-生成prompt

### Mysql工具的使用

```python
from db import MysqlDB

MyDB = MysqlDB(keys=["promotion_id"], uri="")
# logger.debug(df.columns)  # df的列? 为什么没有过滤好?
MyDB.update(df, table_name)
```
