/**
 * Header - Layout Component
 * 
 * Isolated header component with logo, system status, and heartbeat indicator.
 * Follows atomic design principles - no nested div soup.
 */
import { motion } from 'framer-motion';
import { Activity, Zap } from 'lucide-react';
import { StopButton } from './StopButton';

interface HeaderProps {
  /** Whether the SSE connection is healthy */
  isConnected?: boolean;
  /** System status text */
  systemStatus?: string;
  /** System status color */
  statusColor?: 'green' | 'amber' | 'red';
}

/**
 * HeartbeatIndicator - Shows connection health with pulsing dot
 */
function HeartbeatIndicator({ isConnected }: { isConnected: boolean }) {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800/50 border border-slate-700">
      <motion.div
        className={`w-2 h-2 rounded-full ${
          isConnected ? 'bg-emerald-400' : 'bg-red-400'
        }`}
        animate={
          isConnected
            ? {
                scale: [1, 1.2, 1],
                opacity: [1, 0.7, 1],
              }
            : {}
        }
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      <span className={`text-xs font-medium ${
        isConnected ? 'text-emerald-400' : 'text-red-400'
      }`}>
        {isConnected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
  );
}

/**
 * Logo - Brand identity component
 */
function Logo() {
  return (
    <div className="flex items-center gap-3">
      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center">
        <Activity className="w-5 h-5 text-white" />
      </div>
      <div className="flex items-center gap-2">
        <span className="font-bold text-xl text-white">Deep Research</span>
        <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
          v0.1.0
        </span>
      </div>
    </div>
  );
}

/**
 * SystemInfo - Shows backend status
 */
function SystemInfo({ status, color }: { status: string; color: string }) {
  const colorClasses = {
    green: 'text-emerald-400',
    amber: 'text-amber-400',
    red: 'text-red-400',
  };

  return (
    <div className="hidden md:flex items-center gap-2 text-sm">
      <Zap className="w-4 h-4 text-amber-400" />
      <span className="text-slate-500">Powered by</span>
      <span className={colorClasses[color as keyof typeof colorClasses] || 'text-slate-400'}>
        {status}
      </span>
    </div>
  );
}

/**
 * Header - Main navigation bar
 */
export function Header({
  isConnected = true,
  systemStatus = 'LangGraph + Ollama',
  statusColor = 'green',
}: HeaderProps) {
  return (
    <header className="border-b border-slate-800/50 bg-[#0a0a0f]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Left: Logo */}
        <Logo />

        {/* Right: System info, Heartbeat, Stop button */}
        <div className="flex items-center gap-4">
          <SystemInfo status={systemStatus} color={statusColor} />
          <HeartbeatIndicator isConnected={isConnected} />
          <StopButton />
        </div>
      </div>
    </header>
  );
}
