div align="center">

Dheeraj Gowd

AI Engineer in Progress · Building Reliable AI Systems

I build AI-powered applications around LLMs, RAG, AI agents, AI security, and backend systems.

LLMs · RAG · Agents · AI Security · Backend Engineering

</div>

About

I'm a B.Tech Computer Science student focused on becoming a production-oriented AI Engineer.

I enjoy building systems where AI is not just a chatbot, but a component of a larger engineering system involving:

LLM applications and structured generation

Retrieval-Augmented Generation (RAG)

AI agents and tool-based workflows

AI security and adversarial testing

Backend APIs and data systems

Evaluation, reliability, and guardrails

I'm interested in the engineering behind reliable AI — not just prompting models.

What I'm Building

AI ENGINEERING
│
├── LLM Applications
│   ├── Structured Outputs
│   ├── Prompt Engineering
│   └── Tool Calling
│
├── RAG Systems
│   ├── Embeddings
│   ├── Semantic Search
│   ├── Vector Databases
│   └── Retrieval Evaluation
│
├── Agentic AI
│   ├── Agent Workflows
│   ├── Tool Use
│   └── Guardrails
│
├── AI Security
│   ├── Prompt Injection
│   ├── Adversarial Testing
│   └── Defense Systems
│
└── Backend Engineering
    ├── FastAPI
    ├── PostgreSQL
    ├── APIs
    └── System Architecture

Featured Project

🛡️ Adversarial RAG SOC

Autonomous SOC Triage AI Agent & 3-Tier Hardened Defense Benchmark

An experimental security benchmark investigating prompt injection attacks against LLM-assisted SOC incident triage and evaluating a three-tier defense architecture.

The system explores:

Deterministic Detection → RAG → LLM Triage → Adversarial Attacks → Multi-Tier Defense → Independent Verification → Audit Trail

Highlights

Adversarial evaluation of LLM-assisted SOC triage

3-tier defense architecture against prompt injection and authority-spoofing attacks

Independent verification separated from untrusted alert text

Reproducible benchmark methodology

4,500+ API evaluations across benchmark runs

Focus on measurable security trade-offs rather than simple demo performance

Architecture

                    INCOMING SOC ALERT
                           │
                           ▼
                 ┌────────────────────┐
                 │ Deterministic      │
                 │ Detection / Gate   │
                 └──────────┬─────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ Threat Intelligence│
                 │ RAG Retrieval      │
                 └──────────┬─────────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │ Primary LLM        │
                 │ Triage Agent       │
                 └──────────┬─────────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                   ▼                 ▼
             Defense Tiers     Adversarial
                   │             Testing
                   └────────┬────────┘
                            ▼
                 ┌────────────────────┐
                 │ Independent        │
                 │ Verifier            │
                 └──────────┬─────────┘
                            │
                            ▼
                    FINAL SOC VERDICT

Stack: Python · FastAPI · RAG · ChromaDB · Sentence Transformers · LLMs · Adversarial Evaluation

Selected Projects

⚖️ Legal Document AI

Generative AI application focused on making complex legal documents easier to understand.

Focus: Generative AI · Document AI · LLM Applications

Repository: legal-doc

❤️ Heart Disease Prediction

Machine-learning project exploring cardiovascular risk prediction using multiple classification models and evaluation techniques.

Focus: Python · Scikit-learn · Random Forest · XGBoost · Machine Learning

Repository: heart-disease-prediction

🎬 Reel Recommendation

Recommendation-system project exploring personalized content discovery and data-driven recommendations.

Focus: Python · Recommendation Systems · Data Processing

Repository: reel-recomendation

🌐 Vnex WPC Website

Web development project focused on responsive frontend implementation and modern user experiences.

Focus: JavaScript · Frontend Development · Web Development

Repository: vnex-wpc-website

Technical Stack

AI / GenAI

Python LLMs RAG Embeddings Semantic Search

LangChain Hugging Face Vector Databases Prompt Engineering

AI Agents Structured Outputs Tool Calling AI Evaluation

Backend

FastAPI PostgreSQL SQLAlchemy Pydantic

REST APIs API Integration Backend Architecture Testing

Development

Git GitHub Linux Docker

Python JavaScript React SQL

Current Focus

BUILDING
Production-oriented AI systems

LEARNING
Agentic AI
AI Security
LLM Evaluation
Production RAG
AI Observability

EXPLORING
Reliable AI architectures
Adversarial testing
AI-powered developer tools

GOAL
Become a strong AI Engineer

Engineering Philosophy

LLMs should reason. Deterministic systems should enforce.

I care about building AI systems that are:

Reliable

Testable

Observable

Secure

Reproducible

Useful in real-world applications

How I Approach AI Systems

                    USER / SYSTEM INPUT
                            │
                            ▼
                    ┌───────────────┐
                    │   AI LAYER    │
                    │               │
                    │ LLM / Agent   │
                    │ Reasoning     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   CONTROL     │
                    │    LAYER      │
                    │               │
                    │ Validation    │
                    │ Guardrails    │
                    │ Policies      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   SYSTEM      │
                    │    LAYER      │
                    │               │
                    │ APIs / DB     │
                    │ Tools / Data  │
                    └───────┬───────┘
                            │
                            ▼
                    OBSERVABLE RESULT

The goal is to move from:

AI demo → engineered AI system

Beyond the Model

I'm especially interested in the engineering problems that appear after the model works:

Reliability
    ↓
Evaluation
    ↓
Security
    ↓
Observability
    ↓
Guardrails
    ↓
Production

Because a powerful model is only one component of a useful AI system.

GitHub

I use GitHub to document experiments, build projects, explore new AI engineering ideas, and continuously improve my software engineering skills.

My main areas of interest are:

AI Engineering · Agentic AI · RAG · AI Security · GenAI Products · Backend Systems

<div align="center">

Building AI systems, not just AI demos.

</div>
