**signalgather – AI Market Intelligence Platform**  
**Product & Technical Brief for the Development Team**  
**Version:** 1.0 – April 2026  

### 1. Main Purpose and Vision

**signalgather** is an AI-native Market Intelligence Platform designed for professional commodity traders, energy utilities, hedge funds, and analytical teams trading or managing risk in power, gas, LNG, coal, and carbon markets.

Its primary goal is to deliver a **significant informational and competitive advantage** by automatically collecting, analyzing, and transforming vast amounts of global market information into **structured, timely, and highly personalized trading insights**.

The system follows this transformation chain:  
**Raw Information → Structured Events → Market Signals → Personalized Trader Insights**

signalgather functions as an always-on, intelligent analyst team that works 24/7, understands each user’s specific trading focus, and surfaces only the highest-signal information relevant to their book and strategy.

### 2. Why We Are Building signalgather

- Commodity markets are highly volatile and news-driven. Traders and analysts spend too much time manually scanning news, reports, and data sources.
- Current solutions (Bloomberg terminals, traditional news feeds, manual monitoring) are expensive, slow to react, and lack deep personalization.
- There is strong demand for an AI-powered, agentic system that can turn information overload into actionable alpha.
- signalgather serves as the **first pilot application** built on our new Agentic Platform Framework, allowing us to validate the framework in a real revenue-generating product.
- Successful delivery will enable us to expand into other verticals and create a family of specialized agentic intelligence platforms.
   
### 3. How signalgather Will Work (User Perspective)

1. **Natural Language Setup**  
   Users describe their needs in plain text, for example:  
   “I primarily trade European gas and LNG. Focus on supply disruptions, storage levels, pipeline news, and EU regulations. I want morning briefings and instant alerts on high-impact events.”

2. **Personalized Agent Crew**  
   The system uses the framework’s dynamic configuration layer to create a tailored multi-agent crew based on the user’s profile (commodities, regions, risk style, alert preferences).

3. **Continuous Intelligence Cycle**  
   - **Discovery Layer**: Scheduler triggers regular searches via APIs, RSS feeds, structured data sources, and limited targeted scraping.  
   - **Document Intelligence Layer**: Downloaded documents are cleaned, translated if needed, and analyzed once by AI agents to extract entities, detect events, and assess market impact.  
   - **Knowledge Layer**: All structured Events and Signals are stored in PostgreSQL and pqvector.  
   - **Signal & Insight Layer**: Rule-based + agent-based engines detect market signals. Personalized Trader Crew interprets events according to the user’s profile and generates insights, alerts, and reports.

4. **Main User Interfaces**  
   - Real-time Market Signals dashboard  
   - Important Events feed  
   - Personalized Insights and trading recommendations  
   - Daily/Weekly automated briefings  
   - Search & exploration across historical data  
   - Configurable alerts delivered via web, email, or chat

The entire process is fully automated, auditable, and runs with minimal user intervention after initial setup.

### 4. Strategy for First Client & Go-to-Market

**First Client Strategy (Pilot Phase)**  
- Target 1–3 early-adopter clients (mid-sized trading houses, utilities, or boutique hedge funds active in European energy markets).  
- Offer a **paid pilot** (3–6 months) at a reduced rate with full support and customization.  
- Use the pilot to:  
  - Validate product-market fit  
  - Gather real feedback on agent quality and insight accuracy  
  - Refine prompts, event schemas, and signal logic  
  - Collect case studies and performance metrics (e.g., “X high-impact signals detected before price moved”)

**Sales & Monetization Strategy**  
- **Pricing Model**: Tiered SaaS subscription (per user or per seat) + optional usage-based component for heavy analysis.  
- **Positioning**: “Your 24/7 AI Commodity Intelligence Team” – faster, cheaper, and more personalized than hiring additional analysts or relying solely on Bloomberg.  
- **Sales Approach**:  
  - Start with warm introductions and industry networks in energy trading.  
  - Offer live demos showing real-time ingestion → event extraction → personalized insight generation.  
  - Emphasize security, data isolation (multi-tenancy), and auditability for enterprise buyers.  
  - Provide clear ROI examples: time saved, better risk management, and potential alpha generation.  
- Goal: Secure first paying client within 2–3 months after MVP deployment, then use success stories to scale sales.

### 5. How signalgather Is Implemented on the Agentic Platform Framework

signalgather is built as the **first domain-specific application** on top of our reusable **Agentic Platform Framework**.

- The Framework (`libs/agentic-core`) provides all generic infrastructure and orchestration capabilities (API, task queue, worker, scheduler, CrewAI integration, dynamic natural-language user setup, multi-tenancy, observability, deployment, etc.).
- signalgather (`apps/signalgather/`) contains **only** the domain-specific logic:
  - Trading-specific data models (Event, Signal, Document, UserProfile with commodity/region fields)
  - Custom CrewAI crews and agents (Discovery Crew, Document Intelligence Crew, Signal Engine Crew, Personalized Trader Crew)
  - Domain-specific prompt templates and validation rules
  - InsideWire-specific API routers (signals, insights, setup, reports)
  - Seeding scenarios for commodity trading use cases

This clean separation allows us to reuse the same framework for future applications with minimal effort.

### 6. Brief Technical Solution

**Architecture Style**: Modular Monolith using Monorepo structure (Core Framework + Applications)

**Technology Stack**:
- **Framework Core**: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, Redis (task queue), pqvector (vector DB), boto3 (S3-compatible storage)
- **Agent Orchestration**: CrewAI (role-based multi-agent crews) with structured Pydantic outputs
- **Services**: API Service, Agent Worker Service, Scheduler Service
- **Infrastructure**:
  - Local: Docker Compose (full parity)
  - Production: Terraform-provisioned single-node k3s on Hetzner + Helm deployment
- **Key Capabilities**:
  - Natural language user configuration (text → structured profile → dynamic crew)
  - Hybrid data discovery + one-time document analysis
  - Event Store + hybrid (rule + agent) signal detection
  - Full event replay for debugging
  - Multi-tenant isolation from day one
  - CI/CD via GitHub Actions, automatic migrations, deterministic seeding

The system is designed for small-scale production (1–3 clients) on modest hardware while being horizontally scalable when needed.