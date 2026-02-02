/**
 * ResearchInput - Feature Component
 * 
 * Input form for starting new research with integrated action buttons.
 * ChatGPT-style interface with buttons inside the input.
 */
import { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Search, Sparkles, Play, Square } from 'lucide-react';
import { useResearch } from '../hooks/useResearch';
import { useAgentStream } from '../hooks/useAgentStream';
import { useResearchStore } from '../stores/researchStore';

export function ResearchInput() {
  const [query, setQuery] = useState('');
  const { startResearch, isLoading } = useResearch();
  const { connect, disconnect } = useAgentStream();
  const { status, sessionId } = useResearchStore();
  const isRunning = status === 'running';

  const handleSubmit = useCallback(async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim() || isLoading || isRunning) return;

    const newSessionId = await startResearch(query);
    if (newSessionId) {
      connect(newSessionId);
    }
  }, [query, isLoading, isRunning, startResearch, connect]);

  const { stopResearch } = useResearch();

  const handleStop = useCallback(async () => {
    if (sessionId) {
      await stopResearch(sessionId);
      disconnect();
    }
  }, [sessionId, stopResearch, disconnect]);

  // Keyboard shortcut: Ctrl+Enter to submit
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (!isRunning && query.trim()) {
          handleSubmit();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleSubmit, isRunning, query]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-3xl mx-auto"
    >
      <div className="text-center mb-8">
        <motion.div
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 mb-4"
        >
          <Sparkles className="w-4 h-4 text-blue-400" />
          <span className="text-sm text-blue-300">AI-Powered Research</span>
        </motion.div>
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gradient-text">Deep Research</span> System
        </h1>
        <p className="text-slate-400 text-lg max-w-xl mx-auto">
          Enter any topic and let our multi-agent system research it for you.
          Planner → Finder → Summarizer → Reviewer → Writer.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="relative">
        <div className="relative flex items-center">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 z-10" />
          
          <input
            type="text"
            placeholder="What would you like to research?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isRunning}
            className="w-full pl-12 pr-14 py-4 bg-slate-800/50 border border-slate-700 rounded-xl
                       text-white placeholder-slate-500 text-lg
                       focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500
                       transition-all duration-200
                       disabled:opacity-70 disabled:cursor-not-allowed"
          />
          
          {/* Action button inside input */}
          <div className="absolute right-2 top-1/2 -translate-y-1/2">
            {isRunning ? (
              <button
                type="button"
                onClick={handleStop}
                className="p-2.5 rounded-lg bg-amber-500/20 text-amber-400 hover:bg-amber-500/30
                           border border-amber-500/30 transition-colors"
                title="Stop research"
              >
                <Square className="w-5 h-5 fill-current" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!query.trim() || isLoading}
                className="p-2.5 rounded-lg bg-blue-500 text-white hover:bg-blue-600
                           disabled:opacity-50 disabled:cursor-not-allowed
                           transition-colors"
                title="Start research"
              >
                {isLoading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  >
                    <Search className="w-5 h-5" />
                  </motion.div>
                ) : (
                  <Play className="w-5 h-5 fill-current" />
                )}
              </button>
            )}
          </div>
        </div>
      </form>

      {sessionId && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 text-center text-sm text-slate-500"
        >
          Session: <code className="bg-slate-800 px-2 py-1 rounded">{sessionId}</code>
        </motion.div>
      )}
    </motion.div>
  );
}
