/**
 * Header - Layout Component
 * 
 * Isolated header component with logo and heartbeat indicator.
 * Follows atomic design principles - no nested div soup.
 */
import { motion } from 'framer-motion';
import { Activity, Settings } from 'lucide-react';

interface HeaderProps {
  /** Whether the SSE connection is healthy */
  isConnected?: boolean;
  /** Callback when settings is clicked */
  onSettingsClick?: () => void;
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
      <div>
        <span className="font-bold text-xl text-white">Deep Research</span>
        <p className="text-xs text-slate-500">Multi-Agent AI Research System</p>
      </div>
    </div>
  );
}

/**
 * Header - Main navigation bar
 */
export function Header({
  isConnected = true,
  onSettingsClick,
}: HeaderProps) {
  return (
    <header className="border-b border-slate-800/50 bg-[#0a0a0f]/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Left: Logo */}
        <Logo />

        {/* Right: Heartbeat, Settings */}
        <div className="flex items-center gap-4">
          <HeartbeatIndicator isConnected={isConnected} />
          {onSettingsClick && (
            <button
              onClick={onSettingsClick}
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
