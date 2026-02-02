/**
 * AgentStatus - Feature Component
 * 
 * Visualizes the 5 agents with their current status.
 */
import { motion } from 'framer-motion';
import { useResearchStore } from '../stores/researchStore';
import { Brain, Search, FileText, CheckCircle, PenTool } from 'lucide-react';

const agentIcons = {
  Planner: Brain,
  Finder: Search,
  Summarizer: FileText,
  Reviewer: CheckCircle,
  Writer: PenTool,
};

export function AgentStatus() {
  const { agentStatus } = useResearchStore();

  return (
    <div className="w-full">
      <h3 className="text-sm font-medium text-slate-400 mb-4 uppercase tracking-wider">
        Agent Pipeline
      </h3>
      <div className="flex flex-col gap-3">
        {agentStatus.map((agent, index) => {
          const Icon = agentIcons[agent.name as keyof typeof agentIcons];
          const isActive = agent.status === 'running';
          const isCompleted = agent.status === 'completed';
          
          return (
            <motion.div
              key={agent.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`
                relative flex items-center gap-4 p-4 rounded-xl
                border transition-all duration-300
                ${isActive 
                  ? 'bg-slate-800/80 border-slate-600' 
                  : isCompleted
                    ? 'bg-slate-800/40 border-slate-700/50'
                    : 'bg-slate-800/20 border-slate-800'
                }
              `}
            >
              {/* Status indicator */}
              <div className="relative">
                <div
                  className={`
                    w-10 h-10 rounded-xl flex items-center justify-center
                    transition-all duration-300
                    ${isActive ? 'animate-pulse' : ''}
                  `}
                  style={{ 
                    backgroundColor: isActive || isCompleted 
                      ? `${agent.color}20` 
                      : 'rgba(30, 41, 59, 0.5)',
                    border: `1px solid ${isActive || isCompleted ? agent.color : 'transparent'}`,
                  }}
                >
                  <Icon 
                    className="w-5 h-5 transition-colors duration-300"
                    style={{ color: isActive || isCompleted ? agent.color : '#64748b' }}
                  />
                </div>
                
                {/* Connection line */}
                {index < agentStatus.length - 1 && (
                  <div 
                    className={`
                      absolute left-1/2 top-full w-0.5 h-3 -translate-x-1/2 mt-1
                      transition-colors duration-500
                    `}
                    style={{ 
                      backgroundColor: isCompleted ? agent.color : '#1e293b'
                    }}
                  />
                )}
              </div>

              {/* Agent info */}
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className={`
                    font-medium transition-colors duration-300
                    ${isActive || isCompleted ? 'text-white' : 'text-slate-400'}
                  `}>
                    {agent.name}
                  </span>
                  {isActive && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 animate-pulse">
                      Running
                    </span>
                  )}
                  {isCompleted && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400">
                      Done
                    </span>
                  )}
                </div>
                <p className="text-sm text-slate-500">{agent.description}</p>
              </div>

              {/* Progress bar for active agent */}
              {isActive && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-slate-700 rounded-b-xl overflow-hidden">
                  <motion.div
                    className="h-full"
                    style={{ backgroundColor: agent.color }}
                    initial={{ width: '0%' }}
                    animate={{ width: ['0%', '100%', '0%'] }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                  />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
