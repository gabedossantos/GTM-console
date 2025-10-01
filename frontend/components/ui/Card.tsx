import { ReactNode } from 'react';
import clsx from 'clsx';

import { useDesignVariant } from '../design/DesignContext';

interface CardProps {
  className?: string;
  children?: ReactNode;
}

export function Card({ className, children }: CardProps) {
  const variant = useDesignVariant();
  return (
    <div
      className={clsx(
        'rounded-xl border transition-transform duration-300',
        variant === 'design1'
          ? 'border-slate-200 bg-white shadow-sm'
          : 'border-white/10 bg-white/10 text-slate-100 shadow-[0_20px_45px_rgba(52,211,153,0.18)] backdrop-blur-lg hover:-translate-y-1 hover:shadow-[0_30px_70px_rgba(16,185,129,0.25)]',
        className
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children }: CardProps) {
  const variant = useDesignVariant();
  return (
    <div
      className={clsx(
        'px-5 py-4',
        variant === 'design1' ? 'border-b border-slate-200' : 'border-b border-white/10',
        className
      )}
    >
      {children}
    </div>
  );
}

export function CardTitle({ className, children }: CardProps) {
  const variant = useDesignVariant();
  return (
    <h3
      className={clsx(
        'text-sm font-semibold',
        variant === 'design1' ? 'text-slate-700' : 'text-white',
        className
      )}
    >
      {children}
    </h3>
  );
}

export function CardContent({ className, children }: CardProps) {
  const variant = useDesignVariant();
  return (
    <div
      className={clsx(
        'px-5 py-4 text-sm',
        variant === 'design1' ? 'text-slate-600' : 'text-slate-200',
        className
      )}
    >
      {children}
    </div>
  );
}
