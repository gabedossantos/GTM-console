import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import clsx from 'clsx';

import { api, type EvaluationMetrics, type Insight } from '../lib/api';
import { Badge } from './ui/Badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { useDesignVariant } from './design/DesignContext';

export function InsightsOverview() {
  const { data: insights = [], isLoading: isLoadingInsights } = useQuery<Insight[]>({
    queryKey: ['insights', 'recent'],
    queryFn: async () => {
      const response = await api.getRecentInsights(6);
      return response.data;
    },
  });

  const { data: metrics, isLoading: isLoadingMetrics } = useQuery<EvaluationMetrics>({
  queryKey: ['metrics', 'insights'],
    queryFn: async () => {
      const response = await api.getEvaluationMetrics();
      return response.data;
    },
  });

  const chartData = useMemo(() => {
    return insights.map((insight: Insight) => ({
      name: `#${insight.id}`,
      risk: Math.round(insight.risk_score * 100),
      confidence: Math.round(insight.confidence * 100),
    }));
  }, [insights]);

  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Recent Insights</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {isLoadingInsights && (
            <p className={clsx('text-sm', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              Loading insights…
            </p>
          )}
          {!isLoadingInsights && insights.length === 0 && (
            <p className={clsx('text-sm', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              No insights yet.
            </p>
          )}
          {!isLoadingInsights &&
            insights.map((insight: Insight) => (
              <div
                key={insight.id}
                className={clsx(
                  'rounded-lg border p-4',
                  isDesignTwo ? 'border-white/10 bg-white/5 text-slate-200' : 'border-slate-200'
                )}
              >
                <div
                  className={clsx(
                    'flex flex-wrap items-center gap-2 text-xs',
                    isDesignTwo ? 'text-slate-300' : 'text-slate-500'
                  )}
                >
                  <Badge variant="secondary" className="capitalize">
                    {insight.intent.replace('_', ' ')}
                  </Badge>
                  <Badge variant={insight.sentiment === 'negative' ? 'destructive' : 'success'}>
                    {insight.sentiment}
                  </Badge>
                  <span>Risk {Math.round(insight.risk_score * 100)}%</span>
                  <span>Confidence {Math.round(insight.confidence * 100)}%</span>
                </div>
                <p className={clsx('mt-2 text-sm', isDesignTwo ? 'text-slate-200' : 'text-slate-600')}>
                  {insight.summary}
                </p>
                {insight.keywords && (
                  <p className={clsx('mt-1 text-xs', isDesignTwo ? 'text-slate-400' : 'text-slate-400')}>
                    Keywords: {insight.keywords}
                  </p>
                )}
              </div>
            ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Program Metrics</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {isLoadingMetrics && (
            <p className={clsx('text-sm', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              Gathering metrics…
            </p>
          )}
          {metrics && (
            <div className="grid grid-cols-2 gap-4 text-center text-sm">
              <Metric value={`${('coverage' in metrics ? metrics.coverage : metrics.ai_coverage) ?? 0}%`} label="Coverage" />
              <Metric value={`${metrics.feedback_rate}%`} label="Feedback Rate" />
              <Metric value={`${metrics.useful_rate}%`} label="Useful Insights" />
              <Metric value={metrics.performance_trend} label="Performance" />
            </div>
          )}

          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="2 2" vertical={false} />
                <XAxis dataKey="name" fontSize={12} tickMargin={8} />
                <YAxis domain={[0, 100]} fontSize={12} tickFormatter={(value) => `${value}%`} />
                <Tooltip formatter={(value: number) => `${value}%`} labelFormatter={(label) => `Insight ${label}`} />
                <Bar dataKey="risk" fill="#ef4444" radius={[6, 6, 0, 0]} name="Risk" />
                <Bar dataKey="confidence" fill="#2563eb" radius={[6, 6, 0, 0]} name="Confidence" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Metric({ value, label }: { value: string; label: string }) {
  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';
  return (
    <div
      className={clsx(
        'rounded-lg border p-4',
        isDesignTwo ? 'border-white/10 bg-white/5' : 'border-slate-200 bg-slate-50'
      )}
    >
      <p className={clsx('text-lg font-semibold', isDesignTwo ? 'text-white' : 'text-slate-700')}>{value}</p>
      <p className={clsx('text-xs uppercase tracking-wide', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
        {label}
      </p>
    </div>
  );
}
