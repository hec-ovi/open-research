/**
 * TraceLog - Feature Component
 * 
 * Displays real-time event log from the research process.
 */
import { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useResearchStore } from '../stores/researchStore';
import { 
  Play, 
  Search, 
  FileText, 
  CheckCircle, 
  PenTool, 
  AlertCircle,
  XCircle,
  Heart
} from 'lucide-react';
import type { TraceEvent } from '../types';

const eventIcons: Record<string, React.ElementType> = {
  research_started: Play,
  planner_complete: Search,
  finder_complete: FileText,
  summarizer_complete: FileText,
  reviewer_complete: CheckCircle,
  research_completed: PenTool,
  research_error: AlertCircle,
  research_stopped: XCircle,
  heartbeat: Heart,
  connected: Play,
};

const eventColors: Record<string, string> = {
  research_started: 'text-blue-400',
  planner_complete: 'text-blue-400',
  finder_complete: 'text-emerald-400',
  summarizer_complete: 'text-amber-400',
  reviewer_complete: 'text-violet-400',
  research_completed: 'text-pink-400',
  research_error: 'text-red-400',
  research_stopped: 'text-amber-400',
  heartbeat: 'text-slate-500',
  connected: 'text-emerald-400',
};

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { 
    hour12: false, 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  });
}

function EventItem({ event, index }: { event: TraceEvent; index: number }) {
  const Icon = eventIcons[event.type] || Play;
  const colorClass = eventColors[event.type] || 'text-slate-400';
  
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0 }}
      transition={{ delay: index * 0.05 }}
      className="flex items-start gap-3 py-2 px-3 rounded-lg hover:bg-slate-800/50 transition-colors"
    >
      <div className={`mt-0.5 ${colorClass}`}>
        <Icon className="w-4 h-4" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 font-mono">
            {formatTime(event.timestamp)}
          </span>
          <span className={`text-sm font-medium ${colorClass}`}>
            {event.type.replace(/_/g, ' ')}
          </span>
        </div>
        {event.details && Object.keys(event.details).length > 0 && (
          <p className="text-xs text-slate-500 mt-0.5 truncate">
            {JSON.stringify(event.details)}
          </p>
        )}
        {event.error && (
          <p className="text-xs text-red-400 mt-0.5">{event.error}</p>
        )}
      </div>
    </motion.div>
  );
}

export function TraceLog() {
  const { events, status } = useResearchStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  if (status === 'idle' && events.length === 0) {
    return null;
  }

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider">
          Event Log
        </h3>
        <span className="text-xs text-slate-500">{events.length} events</span>
      </div>
      
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto min-h-[200px] max-h-[400px] space-y-1 pr-2"
      >
        <AnimatePresence mode="popLayout">
          {events.length === 0 ? (
            <div className="text-center py-8 text-slate-500">
              Waiting for events...
            </div>
          ) : (
            events.map((event, index) => (
              <EventItem key={`${event.timestamp}-${index}`} event={event} index={index} />
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
