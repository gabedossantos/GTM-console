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
          <header
            className={clsx(
              'border-b transition',
              designVariant === 'design1'
                ? 'border-slate-200 bg-white/90 backdrop-blur'
                : 'border-white/10 bg-white/5 backdrop-blur'
            )}
          >
            <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-4">
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
                <div className="flex items-center gap-2">
                  <span
                    className={clsx(
                      'text-xs font-semibold uppercase tracking-wide',
                      designVariant === 'design1' ? 'text-slate-500' : 'text-slate-300'
                    )}
                  >
                    Design
                  </span>
                  <div
                    className={clsx(
                      'inline-flex overflow-hidden rounded-full border text-xs font-semibold shadow-sm transition',
                      designVariant === 'design1'
                        ? 'border-slate-200 bg-white text-slate-600'
                        : 'border-white/20 bg-white/10 text-slate-200'
                    )}
                    role="group"
                    aria-label="Choose console design"
                  >
                    {(
                      [
                        { value: 'design1', label: 'Design 1' },
                        { value: 'design2', label: 'Design 2' },
                      ] as { value: DesignVariant; label: string }[]
                    ).map((option) => (
                      <button
                        key={option.value}
                        type="button"
                        onClick={() => setDesignVariant(option.value)}
                        className={clsx(
                          'px-3 py-1.5 transition-colors focus:outline-none',
                          option.value === designVariant
                            ? designVariant === 'design1'
                              ? 'bg-brand-600 text-white'
                              : 'bg-emerald-400/90 text-slate-900'
                            : designVariant === 'design1'
                            ? 'hover:bg-slate-100/60'
                            : 'text-slate-200 hover:bg-white/10'
                        )}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <label
                    className={clsx(
                      'text-xs font-semibold uppercase tracking-wide',
                      designVariant === 'design1' ? 'text-slate-500' : 'text-slate-300'
                    )}
                  >
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

          <main className="mx-auto grid max-w-7xl gap-8 px-6 py-8">
            <CsmDashboard />
            <InsightsOverview />
            {selectedAccountId && <AccountTimeline accountId={selectedAccountId} />}
          </main>
        </div>
      </DesignProvider>
    </>
  );
}
