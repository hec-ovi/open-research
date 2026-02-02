/**
 * Research Store - Zustand state management
 * 
 * Central store for research session state.
 * Follows atomic design: small, focused state slices.
 */
import { create } from 'zustand';
import type { ResearchState, TraceEvent, AgentStatus } from '../types';
import { AGENTS } from '../types';

interface ResearchStore extends ResearchState {
  // Actions
  setQuery: (query: string) => void;
  startResearch: (sessionId: string) => void;
  stopResearch: () => void;
  completeResearch: () => void;
  setError: (error: string) => void;
  reset: () => void;
  
  // Agent status
  agentStatus: AgentStatus[];
  setAgentRunning: (agentName: string) => void;
  setAgentCompleted: (agentName: string) => void;
  resetAgentStatus: () => void;
  
  // Trace events
  events: TraceEvent[];
  addEvent: (event: TraceEvent) => void;
  clearEvents: () => void;
  
  // Progress
  progress: number;
  setProgress: (progress: number) => void;
}

const initialState: ResearchState = {
  query: '',
  plan: [],
  sources: [],
  findings: [],
  gaps: null,
  finalReport: null,
  iteration: 0,
  status: 'idle',
  error: null,
  sessionId: null,
};

export const useResearchStore = create<ResearchStore>((set, get) => ({
  ...initialState,
  agentStatus: AGENTS.map(a => ({ ...a })),
  events: [],
  progress: 0,

  setQuery: (query) => set({ query }),
  
  startResearch: (sessionId) => set({
    ...initialState,
    sessionId,
    status: 'running',
    query: get().query,
  }),
  
  stopResearch: () => set({
    status: 'stopped',
  }),
  
  completeResearch: () => set({
    status: 'completed',
    progress: 100,
  }),
  
  setError: (error) => set({
    status: 'error',
    error,
  }),
  
  reset: () => set({
    ...initialState,
    agentStatus: AGENTS.map(a => ({ ...a, status: 'idle' as const })),
    events: [],
    progress: 0,
  }),

  setAgentRunning: (agentName) => set((state) => ({
    agentStatus: state.agentStatus.map(a => 
      a.name === agentName ? { ...a, status: 'running' as const } : 
      a.status === 'running' ? { ...a, status: 'completed' as const } : a
    ),
  })),
  
  setAgentCompleted: (agentName) => set((state) => ({
    agentStatus: state.agentStatus.map(a => 
      a.name === agentName ? { ...a, status: 'completed' as const } : a
    ),
  })),
  
  resetAgentStatus: () => set({
    agentStatus: AGENTS.map(a => ({ ...a, status: 'idle' as const })),
  }),

  addEvent: (event) => set((state) => ({
    events: [...state.events, event],
  })),
  
  clearEvents: () => set({ events: [] }),

  setProgress: (progress) => set({ progress: Math.min(100, Math.max(0, progress)) }),
}));
