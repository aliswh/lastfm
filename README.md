# LastFM user data analysis via PySpark
Use LastFM (non-commercial use) APIs to get information about user features and listening sessions.
> This project has been developed for "Architectures For Big Data" course at UniMi in A.Y. 2021/22.

## Architecture

The architecture solution includes the design of 4 different Points of View/Layers:

PoV | Layer | Implementation
--- | --- | ---
Systems | Ingestion Layer | LastFM APIs (via PyLast)
Infrastructure | Data Lake and Storage Layer | Google Cloud Storage
Developer | Batch Computing Layer | PySpark
Cost/Business | Presentation Layer | Google Colab

## Requirements 
The following Python libraries are required:

* requests
* pylast
* pyspark
* google-cloud-storage



