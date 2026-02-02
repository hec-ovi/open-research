# Deep Research System

A production-grade local deep research application using multi-agent orchestration with LangGraph and Ollama.

## Architecture

**Inference Engine:** Ollama (GPT OSS 20B)  
**Pattern:** Orchestrator-Workers (Star Topology)  
**Stack:**
- **Backend:** Python 3.12+ / FastAPI / LangGraph / SQLite
- **Frontend:** React / Vite / TypeScript / TailwindCSS / Framer Motion
- **Infrastructure:** Docker Compose

## Agent Grid

1. **Planner** - Decomposes queries into research plans
2. **Source Finder** - Discovers diverse sources
3. **Summarizer** - Compresses content (10:1 ratio)
4. **Reviewer** - Detects gaps and triggers iteration
5. **Writer** - Synthesizes final reports with citations

## Quick Start

```bash
# Clone and setup
git clone <repo>
cd open-research

# Copy environment template
cp .env.example .env

# Start all services
docker compose up -d

# Access
Frontend: http://localhost:5173
Backend API: http://localhost:8000
```

## Development Status

See `/agent/PLAN.md` for the execution roadmap.

## License

MIT
