# TRIRIGA AI Data Query Tool

The TRIRIGA database is a perfect represntation of a graph database. With a very simple setup, one can set up a database and set up a retrieval augmented generation (RAG) process for data queries. The goal of this repository is to demonstrate how that's possible without using any third party external services. All of this code can be executed in an private network without any internet access.

This solution is powered by Next.js 14, Python FastAPI, Llama.cpp and [Kùzu](https://kuzudb.com/). Kùzu is a fast, embeddable graph database that has been developed by some smart folks at my alma mater.

Looking for a more detailed overview of the problem and solution? Check out my [blog post](https://www.karbasi.dev/blog/querying-tririga-data-with-ai) on this project.

# System Requirements

I used my local workstation with a 10GB RTX 3080, R9 7900X and 64GB DDR5 memory. The model does use a lot of resources and you can play around with different models from HuggingFace.

# Installation

Install the frontend dependencies:
```
npm install
```

Next, build and install Llama.cpp for python with specific hardware acceleration support. For example, I use Windows and CUDA, therefore I used the following command:
```
$env:CMAKE_ARGS = "-DLLAMA_CUBLAS=on"
pip install llama-cpp-python
```

Please see the [repository readme](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#installation-with-specific-hardware-acceleration-blas-cuda-metal-etc_) for a comprehensive list of commands.

Finally, run the following to install the backend dependencies:
```
pip install -r requirements.txt
```

# Data Setup

I've set up a test database in the subfolder `location_data`. It is generated using the sample data in `test_data`.

The commands to generate a new schema and load data from CSVs are located in the file `data_setup.py`.

If you want to use your own data for tests, I recommend building TRIRIGA queries with similar headings as the CSV files and replacing the files. Feel free to use the ID field if it's globally unique on your properties. If there are issues with the value not being unique, then stick with the Spec ID.

I used space as a foundational piece for queries. This can be expanded to other functional modules (e.g. Corrective maintenance, preventive maintenance, capital projects, RE leases, occupancy, etc).

# Running Local Instance

Run the following two commands from the main directory to start the backend and frontend:

```
npm run dev
uvicorn main:app --reload
```

This app is NOT optimized for production. I highly recommend protecting the API and database behind authentication to avoid unauthorized access.