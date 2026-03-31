import Head from 'next/head';
import type { ChangeEvent } from 'react';
import { useEffect, useMemo, useState } from 'react';
import clsx from 'clsx';
import { useQuery } from '@tanstack/react-query';

import { AccountTimeline } from '../components/AccountTimeline';
import { CsmDashboard } from '../components/dashboards/CsmDashboard';
import { InsightsOverview } from '../components/InsightsOverview';
import { DesignProvider, type DesignVariant } from '../components/design/DesignContext';
import { api, type Account } from '../lib/api';

export default function HomePage() {
  const { data: accounts = [], isLoading } = useQuery<Account[]>({
    queryKey: ['accounts'],
    queryFn: async () => {
      const response = await api.getAccounts();
      return response.data;
    },
  });

  const demoAccountId = useMemo(() => accounts[0]?.id ?? null, [accounts]);
  const [selectedAccountId, setSelectedAccountId] = useState<number | null>(null);
  const [designVariant, setDesignVariant] = useState<DesignVariant>('design1');

  useEffect(() => {
    if (!selectedAccountId && demoAccountId) {
      setSelectedAccountId(demoAccountId);
    }
  }, [demoAccountId, selectedAccountId]);

  return (
    <>
      <Head>
        <title>JourneyLens · GTM Console</title>
  <meta name="description" content="Customer intelligence console bringing insights to your team" />
      </Head>

      <DesignProvider variant={designVariant}>
        <div
          data-design={designVariant}
          className={clsx(
            'min-h-screen transition-colors duration-300',
            designVariant === 'design1'
              ? 'bg-slate-50 text-slate-900'
              : 'bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-slate-100'
          )}
        >
          <header className="border-b border-slate-200 bg-white/90 backdrop-blur transition">
            <div className="mx-auto flex max-w-[1600px] flex-wrap items-center justify-between gap-4 px-4 py-4 md:px-6 lg:px-8">
              <div>
                <h1
                  className={clsx(
                    'text-xl font-semibold',
                    designVariant === 'design1' ? 'text-slate-900' : 'text-white'
                  )}
                >
                  JourneyLens
                </h1>
                <p
                  className={clsx(
                    'text-sm',
                    designVariant === 'design1' ? 'text-slate-500' : 'text-slate-300'
                  )}
                >
                  Customer Intelligence Console
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-4">
                <div className="flex items-center gap-3">
                  <label className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Account Focus
                  </label>
                  <select
                    className={clsx(
                      'rounded-md border px-3 py-2 text-sm shadow-sm focus:border-brand-500 focus:outline-none',
                      designVariant === 'design1'
                        ? 'border-slate-200 bg-white text-slate-800'
                        : 'border-white/20 bg-white/10 text-slate-100 placeholder:text-slate-400'
                    )}
                    value={selectedAccountId ?? ''}
                    onChange={(event: ChangeEvent<HTMLSelectElement>) => setSelectedAccountId(Number(event.target.value))}
                  >
                    <option value="" disabled>
                      {isLoading ? 'Loading accounts…' : 'Select account'}
                    </option>
                    {accounts.map((account) => (
                      <option key={account.id} value={account.id}>
                        {account.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          </header>

          <main className="mx-auto max-w-[1600px] px-4 py-8 md:px-6 lg:px-8">
            <div className="flex flex-col lg:flex-row gap-8 items-start animate-fade-in">
              {/* Main content column */}
              <div className="flex-1 w-full space-y-8 min-w-0">
                <CsmDashboard />
                <InsightsOverview />
              </div>

              {/* Right Sidebar - Sticky */}
              <div className="w-full lg:w-[380px] xl:w-[450px] shrink-0 lg:sticky lg:top-8 animate-slide-up">
                {selectedAccountId ? (
                  <AccountTimeline accountId={selectedAccountId} />
                ) : (
                  <div className="flex h-[400px] items-center justify-center rounded-2xl border border-dashed border-slate-200 bg-white/50 p-8 text-center text-sm text-slate-500 shadow-sm backdrop-blur-sm transition-all hover:bg-white/80">
                    <p>Select an account to view its timeline and ask the Co-Pilot.</p>
                  </div>
                )}
              </div>
            </div>
          </main>
        </div>
      </DesignProvider>
    </>
  );
}
