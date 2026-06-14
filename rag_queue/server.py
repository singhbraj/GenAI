from fastapi import FastAPI, Query
from .client.rq_client import queue
from .workers.worker import process_query


app = FastAPI()

@app.get('/')
def root():
    return {"status": "Server is up and running"}

@app.post('/chat')
def chat(
        query: str = Query(..., dewscription="The chat query of the user ")
):
    
    job = queue.enqueue(process_query, query)

    return {"status": "queued", "job_id": job.id}

@app.get('/job-status')
def gert_result(
        job_id: str = Query(..., description="Job ID")
):
    
    job = queue.fetch_job(job_id = job_id)
    result = job.return_value()
    return {"result": result}