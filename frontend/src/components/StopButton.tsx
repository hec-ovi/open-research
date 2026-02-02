/**
 * StopButton - Feature Component
 * 
 * Button to stop running research.
 */
import { motion } from 'framer-motion';
import { Square } from 'lucide-react';
import { Button } from './ui/Button';
import { useResearch } from '../hooks/useResearch';
import { useResearchStore } from '../stores/researchStore';

export function StopButton() {
  const { stopResearch } = useResearch();
  const { status, sessionId } = useResearchStore();

  const handleStop = async () => {
    if (sessionId) {
      await stopResearch(sessionId);
    }
  };

  if (status !== 'running') return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    >
      <Button
        variant="danger"
        onClick={handleStop}
        className="animate-pulse-glow"
      >
        <Square className="w-4 h-4 mr-2 fill-current" />
        Stop Research
      </Button>
    </motion.div>
  );
}
