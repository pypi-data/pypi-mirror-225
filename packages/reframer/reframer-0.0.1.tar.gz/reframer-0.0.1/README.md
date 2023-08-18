# <a href="https://reframe.is/"><img src="https://d3g1vr8yw3euzd.cloudfront.net/nnext-ultra-wide-tingle.png" alt="Aigent"></a>

## About


Aigent is an experiomental agent framework powered by GPT-4 that operates on dataframes.
Powered by the remarkable GPT-4, this program ingeniously links together thoughts from
Large Language Models (LLMs) to autonomously accomplish your desired objectives.
As a groundbreaking example of GPT-4 operating entirely independently, Auto-GPT pushes
the frontiers of AI's potential to new and awe-inspiring heights.

<a href="https://twitter.com/intent/follow?screen_name=nnextai"><img src="https://img.shields.io/badge/Follow-nnextai-blue.svg?style=flat&logo=twitter"></a>

[Installation](#installation) |  [Quick Start](#quick-start) | [Documentation](#documentation)

## Installation

By far the easiest way to install the Aigent server is to use docker.

```sql
wget https://raw.githubusercontent.com/nnextai/aigent/main/docker-compose.yaml
docker-compose up -d
```

https://discord.gg/KkFzHRTF5K

### Install aigent client
```shell
pip install aigent
```

## Aigent strives to be

* 🥽 Transparent - through logging, and metrics that create visibility into the inner operations.
* 🤸🏾 Flexible - AI Agents and tools are independent of each other, allowing you to create workflows easily.
* 🧩 Composable. Aigents are simply executable python functions and classes with a well defined interface. You can easily construct sophisticated agents from basic building blocks. These building blocks can be obtained from our ecosystem or you can develop custom ones that are specific to your organization.
* 🛹 Incrementally adoptable - By using existing technologies such as Docker, Kubernetes and Celery Aigent enables you to seamlessly adopt it with your organization. From simple ZeroShot agents to sophisticated multi-step AI agents each component can be integrated into your existing workflows.
* 🔨 Reusable - once a tool is running, it can be utilized by various agents, thereby reducing operational overhead, increasing throughput and making tools easy to reason about.
* 🏎️ Fast by taking advantage of data parallelism and prompt sequencing in a manner increases efficiency and reduces the overall number of expensive API calls made to LLM endpoints.
* 🏟️ Rich ecosystem that enables your to pick and choose which tools and agents to deploy. Through contributions from open source developers, we are making great progress to develop a robust ecosystem of tools so that you always have a tool for the job.

# Features
* 🌐 Internet access for searches and information gathering
* 📥 Long-term and short-term memory management 
* 🧠 GPT-4 & Anthropic instances for text generation 
* 🔗 Access to popular websites and platforms 
* 🗃️ File storage and summarization with GPT-3.5 
* 🔌 Extensibility with Plugins

## Documentation

More documentation is available here [https://reframe.is/aigent/docs](https://reframe.is/aigent/docs).: