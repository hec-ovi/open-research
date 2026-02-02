# Deep Research System

A production-grade local deep research application using multi-agent orchestration with LangGraph and Ollama.

## Architecture

**Inference Engine:** Ollama (gpt-oss:20b) with ROCm support for AMD GPUs  
**Pattern:** Orchestrator-Workers (Star Topology)  
**Stack:**
- **Backend:** Python 3.12+ / FastAPI / LangGraph / SQLite (Ubuntu-based)
- **Frontend:** React / Vite / TypeScript / TailwindCSS / Framer Motion
- **Infrastructure:** Docker Compose

## Agent Grid

The system uses 5 specialized agents in a LangGraph workflow:

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Planner │────▶│ Finder  │────▶│Summarizer│────▶│ Reviewer │────▶│ Writer  │
└─────────┘     └─────────┘     └─────────┘     └────┬────┘     └─────────┘
                                                      │
                                               (conditional)
                                                      │
                                              ┌───────▼───────┐
                                              │ Continue/Finish │
                                              └───────┬───────┘
                                                      │
                                            ┌─────────┴──────────┐
                                            │ gaps & iter<max   │
                                            │ → Planner (loop)   │
                                            │ no gaps/max iter   │
                                            │ → Writer (finish)  │
                                            └────────────────────┘
```

| Agent | Role | Key Features |
|-------|------|--------------|
| **Planner** | Query Decomposition | Breaks complex queries into 6-8 sub-questions |
| **Source Finder** | Discovery | DuckDuckGo search, domain diversity (max 2 per domain) |
| **Summarizer** | Compression | 10:1 compression ratio, key facts extraction |
| **Reviewer** | Quality Control | Gap detection, confidence scoring, iteration triggers |
| **Writer** | Synthesis | Professional report with citations, 6 sections |

---

## 🚀 Development Stages

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 0** | ✅ Complete | Project infrastructure, Docker setup, GPU support |
| **Phase 1** | ✅ Complete | Backend core: config, adapter, state, checkpointer |
| **Phase 2** | ✅ Complete | Planner Agent - Query decomposition + LangGraph setup |
| **Phase 3** | ✅ Complete | All 5 Agents + Full Graph Assembly with conditional routing |
| **Phase 4** | 🔄 In Progress | Streaming & Interruption (SSE, stop/resume) |
| **Phase 5** | ⏳ Pending | Frontend Dashboard (Mission Control) |
| **Phase 6** | ⏳ Pending | Integration & Polish |

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- AMD GPU with ROCm drivers (for GPU acceleration)
- **For Strix Halo (Ryzen AI Max):** Ubuntu 25.04+ with kernel 6.12+
- Port 11434, 8000, 5173 available

### 🔧 GPU Configuration (Strix Halo / RDNA 3.5)

If you have an AMD Ryzen AI Max (Strix Halo) with RDNA 3.5 graphics, configure GPU access:

```bash
# Find your GPU group IDs
getent group video | cut -d: -f3   # e.g., 44
getent group render | cut -d: -f3  # e.g., 991

# Copy and edit environment
cp .env.example .env
# Edit VIDEO_GID and RENDER_GID to match your system
```

The `.env` file should contain:
```env
VIDEO_GID=44
RENDER_GID=991
HSA_OVERRIDE_GFX_VERSION=11.5.1
```

**Reference:** Configuration based on [ComfyUI Strix Halo Docker](https://github.com/hector-oviedo/comfyui-strix-docker)

### ⚠️ Important: Stop Local Ollama First!

If you have Ollama installed locally, stop it before running Docker:

```bash
# Stop local Ollama service
sudo systemctl stop ollama

# Or if running manually
pkill ollama

# Verify port is free
sudo lsof -i :11434  # Should return nothing
```

### Start the System

```bash
# Clone and setup
git clone <repo>
cd open-research

# Copy environment template
cp .env.example .env

# Start all services (Ollama auto-downloads model on first start)
docker compose up --build -d

# Monitor Ollama model download
docker logs -f deepresearch-ollama

# Check status
curl http://localhost:8000/health
```

### Access

| Service | URL | Description |
|---------|-----|-------------|
| **API Docs (Custom)** | http://localhost:8000/custom-docs | Bootstrap-styled documentation |
| **API Docs (Swagger)** | http://localhost:8000/docs | Auto-generated OpenAPI docs |
| **Backend API** | http://localhost:8000 | FastAPI endpoints |
| **Ollama** | http://localhost:11434 | Inference API |
| **Frontend** | http://localhost:5173 | React Dashboard (Phase 5) |

### Stop Everything

```bash
docker compose down

# To also remove data volumes:
docker compose down -v
```

---

## 🧪 Testing

### Health & Status

```bash
# 1. Health Check
curl http://localhost:8000/health
# Response: {"status":"healthy","version":"0.1.0","config":{"ollama_model":"gpt-oss:20b",...}}

# 2. API Status
curl http://localhost:8000/api/status
# Response: {"status":"operational","features":{"planner":"implemented",...}}

# 3. Checkpointer Stats
curl http://localhost:8000/api/checkpointer/stats
# Response: {"status":"success","stats":{"sessions":0,"checkpoints":0,...}}
```

### Individual Agent Tests

```bash
# 4. Test Planner Agent
curl -X POST http://localhost:8000/api/test/planner
# Response: {"status":"success","sub_questions_count":6,...}

# 5. Test Source Finder Agent
curl -X POST http://localhost:8000/api/test/finder
# Response: {"status":"success","sources_count":10,...}

# 6. Test Summarizer Agent
curl -X POST http://localhost:8000/api/test/summarizer
# Response: {"status":"success","key_facts_count":5,...}

# 7. Test Reviewer Agent
curl -X POST http://localhost:8000/api/test/reviewer
# Response: {"status":"success","gaps_count":3,...}

# 8. Test Writer Agent
curl -X POST http://localhost:8000/api/test/writer
# Response: {"status":"success","word_count":1200,...}

# 9. Test Full Graph (All 5 Agents)
# Note: This takes 5-10 minutes due to multiple LLM calls
curl -X POST http://localhost:8000/api/test/graph
# Response: Full research pipeline result
```

### Test Results Summary

| Endpoint | Status | Result |
|----------|--------|--------|
| `/api/test/planner` | ✅ | 6 sub-questions generated |
| `/api/test/finder` | ✅ | 10 diverse sources discovered |
| `/api/test/summarizer` | ✅ | 5 key facts, 0.95 relevance, 0.72 compression |
| `/api/test/reviewer` | ✅ | 3 gaps detected, 0.88 confidence |
| `/api/test/writer` | ✅ | 1200-word report, 6 sections, 3 citations |
| `/api/test/graph` | ✅ | Full pipeline (Planner→Finder→Summarizer→Reviewer→Writer) |

### Verify GPU is Working

```bash
# Check Ollama logs for GPU detection
docker logs deepresearch-ollama | grep "inference compute"
# Should show: library=ROCm compute=gfx1151

# Test GPU inference directly
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "gpt-oss:20b", "prompt": "Say hello GPU", "stream": false}'
```

---

## 📁 Project Structure

```
open-research/
├── docker-compose.yml          # Service orchestration
├── .env                        # Environment configuration
├── .env.example                # Configuration template
├── start.sh                    # Automation script
├── ollama/                     # Ollama service (auto-download)
│   ├── Dockerfile
│   └── entrypoint.sh
├── backend/                    # FastAPI backend (Phase 3 ✅)
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py       # HTTP endpoints (all test routes)
│   │   ├── core/
│   │   │   ├── config.py       # Pydantic Settings
│   │   │   ├── ollama_adapter.py   # VLLM singleton (Singleton pattern)
│   │   │   ├── checkpointer.py     # LangGraph persistence (SQLite)
│   │   │   └── graph.py            # LangGraph workflow (5 agents)
│   │   ├── agents/             # All 5 LangGraph agents
│   │   │   ├── prompts/        # Agent prompts as .md files
│   │   │   │   ├── planner.md      # Planner system prompt
│   │   │   │   ├── finder.md       # Source finder prompt
│   │   │   │   ├── summarizer.md   # Summarizer prompt
│   │   │   │   ├── reviewer.md     # Reviewer prompt
│   │   │   │   └── writer.md       # Writer prompt
│   │   │   ├── planner.py      # Agent 1: Query decomposition
│   │   │   ├── finder.py       # Agent 2: Source discovery
│   │   │   ├── summarizer.py   # Agent 3: Content compression
│   │   │   ├── reviewer.py     # Agent 4: Gap detection
│   │   │   └── writer.py       # Agent 5: Report synthesis
│   │   └── models/
│   │       └── state.py        # ResearchState TypedDict
│   ├── docs/
│   │   └── index.html          # Bootstrap documentation
│   ├── main.py                 # Application entry
│   └── pyproject.toml          # Dependencies (uv)
├── frontend/                   # React dashboard (Phase 5 ⏳)
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
└── agent/                      # Project tracking (not in git)
    ├── PLAN.md                 # Execution roadmap
    ├── MEMORY.md               # Technical decisions
    ├── logs.md                 # Session logs
    └── error.md                # Error tracking
```

### Backend Architecture

**Design Patterns Used:**
- **Singleton:** `VLLMAdapter`, `ResearchGraph`, all Agent instances
- **Adapter:** Ollama adapter hides LLM complexity
- **Factory:** Graph compilation, state creation
- **Capsule:** Each agent is isolated with single responsibility

**Key Files:**
- `app/core/ollama_adapter.py` - VLLM singleton with retry logic
- `app/core/graph.py` - Complete 5-agent LangGraph workflow
- `app/core/checkpointer.py` - SQLite persistence for state
- `app/agents/*.py` - Individual agent implementations
- `app/agents/prompts/*.md` - Externalized system prompts

---

## Alternative: Using the Launch Script

```bash
# Make executable and run
chmod +x start.sh
./start.sh up        # Start everything
./start.sh status    # Check status
./start.sh logs      # View logs
./start.sh down      # Stop everything
```

---

## Troubleshooting

### Port 11434 Already in Use

**Error:** `failed to bind host port 0.0.0.0:11434/tcp: address already in use`

**Solution:** Stop local Ollama:
```bash
sudo systemctl stop ollama
# or
pkill ollama
```

### ROCm GPU Not Detected

**Error:** Ollama runs on CPU instead of GPU (`library=cpu`)

**Solution for Standard AMD GPUs:**
```bash
# Verify GPU is visible
rocm-smi

# Check render group ID
cat /etc/group | grep render

# Edit .env with your group IDs
VIDEO_GID=44
RENDER_GID=991
```

**Solution for Strix Halo (RDNA 3.5 / gfx1151):**
The docker-compose.yml already includes required settings:
- `privileged: true` - Required for GPU access
- `HSA_OVERRIDE_GFX_VERSION=11.5.1` - Strix Halo architecture
- `ipc: host` and `seccomp:unconfined` - Shared memory

Verify GPU detection:
```bash
docker logs deepresearch-ollama | grep "inference compute"
# Should show: library=ROCm compute=gfx1151
```

### Model Auto-Download

The Ollama container now **auto-downloads** the model on first start. To monitor:
```bash
docker logs -f deepresearch-ollama
# Wait for: "✓ Model is ready to use!"
```

Or check if model is ready:
```bash
curl http://localhost:11434/api/tags | grep gpt-oss
```

---

## Development Status

**Current Phase:** Phase 4 - Streaming & Interruption (SSE) 🔄

**Latest Updates:**
- ✅ Phase 0: Infrastructure, Docker, GPU support (Strix Halo)
- ✅ Phase 1: Backend core (config, adapter, state, checkpointer)
- ✅ Phase 2: Planner Agent + LangGraph setup
- ✅ Phase 3: All 5 Agents + Full Graph Assembly
  - Planner: Query decomposition
  - Finder: DuckDuckGo search, domain diversity
  - Summarizer: 10:1 compression, key facts
  - Reviewer: Gap detection, iteration triggers
  - Writer: Report synthesis with citations
- ✅ Full Graph: Complete pipeline with conditional routing
- ✅ All Libraries Up-to-Date (verified Feb 2026)
- 🔄 Phase 4 Next: Streaming & Interruption (SSE endpoints)

See `/agent/PLAN.md` for detailed execution roadmap.

## License

MIT
