/**
 * Card - Atomic UI Component
 * 
 * Container component with glass effect.
 */
import type { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  headerAction?: ReactNode;
}

export function Card({ children, className = '', title, subtitle, headerAction }: CardProps) {
  return (
    <div className={`
      glass rounded-xl overflow-hidden
      ${className}
    `}>
      {(title || headerAction) && (
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-700/50">
          <div>
            {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
            {subtitle && <p className="text-sm text-slate-400">{subtitle}</p>}
          </div>
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
}
