from langchain_ray.api.imports import *
from langchain_ray.driver.ingress_driver import *


class TNetData(BaseModel):
    data_path: str = Field(
        title="The PDF path.",
        description="It can be a single file, list of files, directory or list of directories.",
        example="/home/hamza/dev/HF/langchain_ray/resumes_5",
    )
    ems_folder: str = Field(
        title="The folder to write the embeddings to.",
        description="It must be a directory.",
        regex=".*\/$",
        example="/media/hamza/data2/faiss_data/saved_ems/",
    )
    tenant_id: str = Field(
        title="The tenant id.",
        description="It must be a string.",
        example="ten_123",
        default="ten_123",
    )


class ResumesData(TNetData):
    cats_folder: str = Field(
        title="The folder to write the categories to.",
        description="It must be a directory.",
        regex=".*\/$",
        example="/media/hamza/data2/faiss_data/saved_cats/",
    )
    do_ner: bool = Field(
        title="Whether to do NER or not.",
        description="It must be a boolean.",
        default=False,
    )


class ResumeData(ResumesData):
    data_path: str = Field(
        title="The PDF path.",
        description="It must be a pdf file. Not a directory.",
        regex=".*\.pdf",
        example="/home/hamza/dev/HF/langchain_ray/resumes_5/0bedb223-262c-4388-9756-093dd7905428.pdf",
    )


app = FastAPI()


@serve.deployment(
    autoscaling_config=dict(
        min_replicas=1, max_replicas=1, target_num_ongoing_requests_per_replica=1
    ),
    ray_actor_options=dict(num_cpus=2, num_gpus=0.2),
    health_check_period_s=10,
    health_check_timeout_s=30,
)
@serve.ingress(app)
class TNetIngress(Ingress):
    def __init__(
        self,
        model_name="HamzaFarhan/PDFSegs",
        block_size=50,
        num_cpus=4,
        num_gpus=0.2,
        redis_host="127.0.0.1",
        redis_port=6379,
        verbose=True,
    ):
        msg.info(f"TNetIngress RAY RESOURCES: {ray.available_resources()}", spaced=True)
        self.ray_chain_args = dict(
            block_size=block_size, num_cpus=num_cpus, num_gpus=num_gpus, verbose=verbose
        )
        self.verbose = verbose
        device = default_device()
        self.ems_model = SentenceTransformer(model_name, device=device)
        self.cats_model = SetFitModel.from_pretrained("HamzaFarhan/PDFSegs").to(device)
        self.e_ner = load_edu_model(device=device)
        self.j_ner = load_job_model(device=device)
        super().__init__(
            redis_host=redis_host,
            redis_port=redis_port,
        )

    def res_chain(self, resumes_data):
        msg.info(f"res_chain RAY RESOURCES: {ray.available_resources()}", spaced=True)
        chains = []
        output_vars = []

        docs_chain = pdf_to_docs_chain(
            input_variables=["data_path"], output_variables=["docs"], verbose=self.verbose
        )
        chains.append(docs_chain)
        output_vars.append(["docs"])
        # tnet_chain = add_str_to_docs_chain(
        #     input_variables=output_vars[-1],
        #     output_variables=["tnet_docs"],
        #     verbose=self.verbose,
        # )
        # chains.append(tnet_chain)
        # output_vars.append(["tnet_docs"])
        cats_chain = add_cats_to_docs_chain(
            cats_model=self.cats_model,
            input_variables=output_vars[-1],
            output_variables=["cat_docs"],
            verbose=self.verbose,
        )
        cats_chain = ray_chain(cats_chain, **self.ray_chain_args)
        chains.append(cats_chain)
        output_vars.append(["cat_docs"])
        if resumes_data.get("do_ner", False):
            ner_chain = add_ners_to_docs_chain(
                e_ner=self.e_ner,
                j_ner=self.j_ner,
                input_variables=output_vars[-1],
                output_variables=["ner_docs"],
                verbose=self.verbose,
            )
            ner_chain = ray_chain(ner_chain, **self.ray_chain_args)
            chains.append(ner_chain)
            output_vars.append(["ner_docs"])

        json_chain = docs_to_json_chain(
            json_folder=resumes_data["cats_folder"],
            input_variables=output_vars[-1],
            output_variables=["json_docs"],
            verbose=self.verbose,
        )
        chains.append(json_chain)
        output_vars.append(["json_docs"])
        ems_chain = add_ems_to_docs_chain(
            self.ems_model,
            input_variables=output_vars[-1],
            output_variables=["ems_docs"],
            verbose=self.verbose,
        )
        ems_chain = ray_chain(ems_chain, **self.ray_chain_args)
        chains.append(ems_chain)
        output_vars.append(["ems_docs"])
        json_chain2 = docs_to_json_chain(
            json_folder=resumes_data["ems_folder"],
            input_variables=output_vars[-1],
            output_variables=["final_docs"],
            verbose=self.verbose,
        )
        chains.append(json_chain2)
        return SequentialChain(
            chains=chains,
            input_variables=["data_path"],
            output_variables=["final_docs"],
            verbose=self.verbose,
        )

    def jobs_chain(self, jobs_data):
        chain1 = pdf_to_docs_chain(
            input_variables=["data_path"], output_variables=["docs"], verbose=self.verbose
        )
        chain2 = add_ems_to_docs_chain(
            self.ems_model,
            input_variables=["docs"],
            output_variables=["ems_docs"],
            verbose=self.verbose,
        )
        chain2 = ray_chain(chain2, **self.ray_chain_args)
        chain3 = docs_to_json_chain(
            jobs_data["ems_folder"],
            with_content=False,
            input_variables=["ems_docs"],
            output_variables=["final_docs"],
            verbose=self.verbose,
        )
        return SequentialChain(
            chains=[chain1, chain2, chain3],
            input_variables=["data_path"],
            output_variables=["final_docs"],
            verbose=self.verbose,
        )

    @app.post("/batchembedding/resumes")
    async def resumes(self, resumes_data: ResumesData, background_tasks: BackgroundTasks):
        # try:
        #     chain = self.res_chain(resumes_data)
        # except Exception as e:
        #     msg.fail("Failed to create Resumes Chain.", spaced=True)
        #     raise Exception(e)
        msg.info("********* CALLING ACTION *********", spaced=True)
        data_dict = dict(chain_data=resumes_data.dict())
        res = self.bulk_action(
            data=data_dict, background_tasks=background_tasks, chain_creator=self.res_chain
        )
        # torch.cuda.empty_cache()
        msg.good(f"RETURNING RESULTS = {res}", spaced=True)
        return JSONResponse(content=res)

    @app.post("/batchembedding/resume")
    async def resume(self, resumes_data: ResumeData):
        t1 = time()
        try:
            chain = self.res_chain(resumes_data.dict())
        except Exception as e:
            msg.fail("Failed to create Resumes Chain.", spaced=True)
            raise Exception(e)
        try:
            chain(dict(data_path=resumes_data.data_path), return_only_outputs=True)
        except Exception as e:
            msg.fail("Failed to run Resumes Chain.", spaced=True)
            raise Exception(e)
        t2 = time()
        time_taken = t2 - t1
        msg.good(f"Time taken: {time_taken:.2f} seconds.", spaced=True)
        res = dict(
            data_path=resumes_data.data_path,
            cats_folder=resumes_data.cats_folder,
            ems_folder=resumes_data.ems_folder,
            time_taken=time_taken,
        )
        torch.cuda.empty_cache()
        msg.good(f"RETURNING RESULTS = {res}", spaced=True)
        return JSONResponse(content=res)

    @app.post("/batchembedding/jobs")
    async def jobs(self, jobs_data: TNetData):
        t1 = time()
        try:
            chain = self.jobs_chain(jobs_data.dict())
        except Exception as e:
            msg.fail("Failed to create Jobs Chain.", spaced=True)
            raise Exception(e)
        try:
            chain(dict(data_path=jobs_data.data_path), return_only_outputs=True)
        except Exception as e:
            msg.fail("Failed to run Jobs Chain.", spaced=True)
            raise Exception(e)
        t2 = time()
        time_taken = t2 - t1
        msg.good(f"Time taken: {time_taken:.2f} seconds.", spaced=True)
        res = dict(
            data_path=jobs_data.data_path,
            ems_folder=jobs_data.ems_folder,
            time_taken=time_taken,
        )
        torch.cuda.empty_cache()
        msg.good(f"RETURNING RESULTS = {res}", spaced=True)
        return JSONResponse(content=res)
