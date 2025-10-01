import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { AlertTriangle, Clock, TrendingUp } from 'lucide-react';
import clsx from 'clsx';

import { api, type DashboardAccount } from '../../lib/api';
import { Badge } from '../ui/Badge';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { useDesignVariant } from '../design/DesignContext';

function useDashboardData() {
  return useQuery<DashboardAccount[]>({
    queryKey: ['dashboard', 'csm'],
    queryFn: async () => {
      const response = await api.getDashboard();
      return response.data;
    },
    refetchInterval: 60_000,
  });
}

export function CsmDashboard() {
  const { data: accounts = [], isLoading, isError } = useDashboardData();
  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';

  const { highRisk, mediumRisk } = useMemo(() => {
    const high = accounts.filter((account) => account.risk_score >= 0.8);
    const medium = accounts.filter((account) => account.risk_score >= 0.6 && account.risk_score < 0.8);
    return { highRisk: high, mediumRisk: medium };
  }, [accounts]);

  if (isLoading) {
    return (
      <div
        className={clsx(
          'rounded-md border border-dashed p-6 text-sm',
          isDesignTwo ? 'border-white/20 bg-white/5 text-slate-200' : 'border-slate-200 bg-slate-50 text-slate-500'
        )}
      >
        Loading dashboard…
      </div>
    );
  }

  if (isError) {
    return (
      <div
        className={clsx(
          'rounded-md border p-6 text-sm',
          isDesignTwo
            ? 'border-rose-400/30 bg-rose-500/10 text-rose-200'
            : 'border-red-200 bg-red-50 text-red-600'
        )}
      >
        Unable to load dashboard data.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex items-center justify-between">
            <CardTitle>Accounts at Risk</CardTitle>
            <AlertTriangle className="h-5 w-5 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className={clsx('text-3xl font-semibold', isDesignTwo ? 'text-rose-300' : 'text-red-600')}>
              {highRisk.length}
            </div>
            <p className={clsx('text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              +{mediumRisk.length} medium risk accounts
            </p>
            <div className="mt-4 space-y-3">
              {highRisk.slice(0, 4).map((account) => (
                <div
                  key={account.account_id}
                  className={clsx('flex items-center justify-between text-sm', isDesignTwo && 'text-slate-100')}
                >
                  <span className={clsx(isDesignTwo && 'text-slate-100')}>{account.account_name}</span>
                  <Badge variant="destructive">{Math.round(account.risk_score * 100)}%</Badge>
                </div>
              ))}
              {highRisk.length === 0 && (
                <p className={clsx('text-sm', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
                  No accounts above 80% risk right now.
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex items-center justify-between">
            <CardTitle>Engagement Momentum</CardTitle>
            <TrendingUp className="h-5 w-5 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className={clsx('text-3xl font-semibold', isDesignTwo ? 'text-emerald-300' : 'text-emerald-600')}>
              +18%
            </div>
            <p className={clsx('text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              Interactions vs. previous 7 days
            </p>
            <div className="mt-4 space-y-2 text-sm">
              <div className={clsx('flex justify-between', isDesignTwo && 'text-slate-100')}>
                <span>Support tickets</span>
                <span className={clsx(isDesignTwo ? 'text-emerald-300' : 'text-emerald-600')}>+12%</span>
              </div>
              <div className={clsx('flex justify-between', isDesignTwo && 'text-slate-100')}>
                <span>Account reviews</span>
                <span className={clsx(isDesignTwo ? 'text-emerald-300' : 'text-emerald-600')}>+24%</span>
              </div>
              <div className={clsx('flex justify-between', isDesignTwo && 'text-slate-100')}>
                <span>Email replies</span>
                <span className={clsx(isDesignTwo ? 'text-amber-300' : 'text-amber-500')}>-6%</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex items-center justify-between">
            <CardTitle>Next Best Actions</CardTitle>
            <Clock className="h-5 w-5 text-brand-500" />
          </CardHeader>
          <CardContent className={clsx('space-y-3 text-sm', isDesignTwo && 'text-slate-100')}>
            {accounts.slice(0, 4).map((account) => (
              <div
                key={account.account_id}
                className={clsx(
                  'border-b pb-3 last:border-none',
                  isDesignTwo ? 'border-white/10' : 'border-slate-100'
                )}
              >
                <p className={clsx('font-medium', isDesignTwo ? 'text-white' : 'text-slate-700')}>
                  {account.next_action}
                </p>
                <p className={clsx('text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
                  {account.account_name} · Risk {Math.round(account.risk_score * 100)}%
                </p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account Risk Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {accounts.map((account) => (
              <AccountRow key={account.account_id} account={account} />
            ))}
            {accounts.length === 0 && (
              <p
                className={clsx(
                  'rounded-md border border-dashed p-6 text-center text-sm',
                  isDesignTwo ? 'border-white/10 text-slate-300' : 'border-slate-200 text-slate-500'
                )}
              >
                Add interactions to see risk trends.
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function AccountRow({ account }: { account: DashboardAccount }) {
  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';
  return (
    <div
      className={clsx(
        'flex flex-col gap-3 rounded-lg border p-4 md:flex-row md:items-center md:justify-between',
        isDesignTwo ? 'border-white/10 bg-white/5' : 'border-slate-200'
      )}
    >
      <div>
        <p className={clsx('text-sm font-semibold', isDesignTwo ? 'text-white' : 'text-slate-700')}>
          {account.account_name}
        </p>
        <p className={clsx('text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
          {account.recent_interactions} interactions • Last touch{' '}
          {account.last_interaction ? new Date(account.last_interaction).toLocaleString() : 'N/A'}
        </p>
      </div>
      <div className="flex items-center gap-3">
        <Badge
          variant={
            account.risk_score >= 0.8
              ? 'destructive'
              : account.risk_score >= 0.6
              ? 'default'
              : 'secondary'
          }
        >
          Risk {Math.round(account.risk_score * 100)}%
        </Badge>
        <span className={clsx('text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
          {account.next_action}
        </span>
      </div>
    </div>
  );
}
