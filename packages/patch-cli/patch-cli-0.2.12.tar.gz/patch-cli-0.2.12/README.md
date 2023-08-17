# Patch CLI 

Patch is a zero-config backend for building data products like customer-facing analytics and external data APIs. Connect a source and deploy low latency Dataset APIs instantly. No need to pre-define models, metrics, or OLAP cubes.

Patch is an end-to-end solution for elevating analytics datasets into production. It often replaces a pipeline out of an analytical warehouse into a production database, the production database itself, a cache, and the access and API layers.   

### Features
* Run analytical queries over large datasets with low latency and without hitting the data warehouse
* Perform time series bucketing, aggregations, grouping, filtering and sorting without writing complicated SQL queries
* Leverage data from Snowflake, BigQuery, or Databricks (coming soon) in customer-facing applications
* Look up single row records with single digit millisecond response times
* Turn your dbt models into memory-backed APIs in minutes
* Query data from your application like a data micro-service  
* Automatically scale horizontally without setting up any infrastructure

### How does it work?
The best part is that you can instantly start building your application without setting up any infrastructure.

Patch replicates your tables into a distributed memory grid and exposes APIs to query the datasets. Data is kept up to date with a built-in change data capture process, and you can optionally integrate with your orchestration tool.  Since the tables are fully replicated, queries never hit the data warehouse directly.

## Getting started: CLI
Please follow our [Installation](https://docs.patch.tech/command-line-interface/installation) then [Basic Usage](https://docs.patch.tech/command-line-interface/basic-usage) recommendations on our documentation site.

## Getting help
If we're already in touch, Slack or email is the best place to reach out for help. If you're reading this and our teams haven't engaged yet, please provide your email at [patch.tech](https://www.patch.tech/) and we'll reach out as soon as possible! 

## License
> Copyright 2022 Patch Enterprises
> 
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
> 
>     http://www.apache.org/licenses/LICENSE-2.0
> 
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
