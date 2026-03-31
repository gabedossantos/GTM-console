import clsx from 'clsx';
import { ReactNode } from 'react';

import { useDesignVariant } from '../design/DesignContext';

interface BadgeProps {
  variant?: 'default' | 'destructive' | 'success' | 'secondary';
  className?: string;
  children?: ReactNode;
}

export function Badge({ variant = 'default', className, children }: BadgeProps) {
  const designVariant = useDesignVariant();
  const variantStyles: Record<NonNullable<BadgeProps['variant']>, string> = designVariant === 'design1'
    ? {
        default: 'bg-brand-50 text-brand-700 border border-brand-200/60',
        destructive: 'bg-rose-50 text-rose-700 border border-rose-200/60',
        success: 'bg-emerald-50 text-emerald-700 border border-emerald-200/60',
        secondary: 'bg-slate-50 text-slate-600 border border-slate-200/60',
      }
    : {
        default: 'bg-white/10 text-slate-100 border border-white/10 backdrop-blur',
        destructive: 'bg-rose-500/20 text-rose-200 border border-rose-400/30',
        success: 'bg-emerald-500/20 text-emerald-200 border border-emerald-400/30',
        secondary: 'bg-white/5 text-slate-200 border border-white/10',
      };

  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide',
        variantStyles[variant],
        className,
      )}
    >
      {children}
    </span>
  );
}
