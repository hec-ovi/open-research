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
  completeResearch: (finalReport?: ResearchState['finalReport']) => void;
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
    agentStatus: AGENTS.map(a => ({ ...a, status: 'idle' as const })),
  }),
  
  stopResearch: () => set({
    status: 'stopped',
  }),
  
  completeResearch: (finalReport?: ResearchState['finalReport']) => set((state) => ({
    status: 'completed',
    progress: 100,
    finalReport: finalReport || state.finalReport,
  })),
  
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

  setAgentRunning: (agentName) => set((state) => {
    // Mark the target agent as running, and any currently running agent as completed
    const updatedAgents = state.agentStatus.map(a => {
      if (a.name === agentName) {
        return { ...a, status: 'running' as const };
      }
      if (a.status === 'running') {
        return { ...a, status: 'completed' as const };
      }
      return a;
    });
    return { agentStatus: updatedAgents };
  }),
  
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
