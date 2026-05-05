## This README provides an overview of Sprint 6 data anlysis job on google cloud. 
The pyspark job processes ATP tennis match data using Google Cloud Dataproc Serverless.



## Commands Used for Running the Job

### Define local variables in cloud shell
```
export PROJECT_ID=cs131-project-6
export REGION=us-west1
export BUCKET=cs131-team9
```


### Define which project to execute commands on during cloud shell session
```
gcloud config set project $PROJECT_ID
```


### Enable Google Cloud Services
```
gcloud services enable   storage.googleapis.com   dataproc.googleapis.com
```


### Create a Cloud Storage bucket in the us-west1 region to host project code and data
```
gsutil mb -l $REGION gs://$BUCKET/
```


### Download data onto Google Cloud Shell
### Copy data from Google Cloud Shell into bucket
Completed through UI / manually.


### Create ‘code’ folder in bucket & upload python script file onto it
Done using google cloud console interface. 

<br>

### Verify contents of ‘data’ and ‘code’ folder in the bucket
```
gsutil ls -lh gs://$BUCKET/data/
gsutil ls -lh gs://$BUCKET/code/
```

### Defines variable in cloud shell for path to python script
```
export CODE_URI=gs://$BUCKET/code/job.py
```

### Submit dataproc serverless batch using 4 executors (each with 4 cores and 4GB RAM), processing the datasets from the bucket and saving the results to the /output/ directory.
```
gcloud dataproc batches submit pyspark "$CODE_URI" \
     --region="$REGION" \
     --deps-bucket="gs://$BUCKET" \
     --properties="spark.dynamicAllocation.enabled=false,spark.executor.instances=4,spark.executor.cores=4,spark.executor.memory=4g" \
     -- \
     --matches="gs://$BUCKET/data/atp_matches.csv" \
     --qual="gs://$BUCKET/data/atp_matches_qual_chall.csv" \
     --players="gs://$BUCKET/data/atp_players.csv" \
     --rankings="gs://$BUCKET/data/atp_rankings.csv" \
     --output="gs://$BUCKET/output/"
```

### GCS Output Path
```
gs://cs131-team9/output/pa6/main_draw_BPS

gs://cs131-team9/output/pa6/qual_BPS

gs://cs131-team9/output/pa6/main_surface_dom

gs://cs131-team9/output/pa6/qual_surface_dom

gs://cs131-team9/output/pa6/upset_performance_gaps

gs://cs131-team9/output/pa6/country_win_stats

```

### Input & Output Directory Tree
```bash
cs131-team9/
├── code/
│   └── job.py
├── data/
│   ├── atp_matches.csv
│   ├── atp_matches_qual_chall.csv
│   ├── atp_players.csv
│   └── atp_rankings.csv
└── output/
    └── pa6/
        ├── main_draw_BPS/
        ├── qual_BPS/
        ├── main_surface_dom/
        ├── qual_surface_dom/
        └── upset_performance_gaps/
        └── country_win_stats
        
