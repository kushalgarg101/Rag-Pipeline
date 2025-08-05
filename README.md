# End to End RAG Pipeline

- Rag project where data is ingested from local directory(can be any others tools like S3 bucket or Database stored).
- Using Prefect made a Pipeline which includes from data ingestion to preprocessing to loading these into vector database.
- Exposed endpoints using Fastapi and containerized it with docker.
- Attached a database to the app so that all reponses and user inputs will be stored.

  ![Pipeline](https://github.com/kushalgarg101/Rag-Pipeline/blob/master/prefect_rag.png)
