import type { ChangeEvent, KeyboardEvent, FC } from 'react';
import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Loader2, Mail, MessageSquare, Phone, Reply, ThumbsDown, ThumbsUp } from 'lucide-react';
import clsx from 'clsx';

import { api, type AccountWithInsights, type FeedbackPayload, type Interaction } from '../lib/api';
import { Badge } from './ui/Badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { useDesignVariant } from './design/DesignContext';

interface AccountTimelineProps {
  accountId: number;
}

export function AccountTimeline({ accountId }: AccountTimelineProps) {
  const queryClient = useQueryClient();
  const [query, setQuery] = useState('');
  const [ragAnswer, setRagAnswer] = useState<string>('');
  const [ragIsLoading, setRagIsLoading] = useState(false);
  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';

  const { data, isLoading, isError } = useQuery<AccountWithInsights>({
    queryKey: ['account', accountId],
    queryFn: async () => {
      const response = await api.getAccount(accountId);
      return response.data;
    },
    enabled: Boolean(accountId),
  });

  const feedbackMutation = useMutation({
    mutationFn: (payload: FeedbackPayload) => api.submitFeedback(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dashboard', 'csm'] });
    },
  });

  const handleRagQuery = async () => {
    if (!query.trim()) return;
    try {
      setRagIsLoading(true);
      const response = await api.getRagResponse(accountId, query.trim());
      setRagAnswer(response.data.answer);
    } catch (error) {
  setRagAnswer('Unable to generate insight for this account.');
    } finally {
      setRagIsLoading(false);
    }
  };

  if (isLoading) {
    return <CardPlaceholder text="Loading account timeline…" />;
  }

  if (isError || !data) {
    return <CardPlaceholder text="Unable to load account data." tone="error" />;
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Ask the Account Co-Pilot</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col gap-2 md:flex-row">
            <input
              className={clsx(
                'flex-1 rounded-md border px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-brand-500/60',
                isDesignTwo
                  ? 'border-white/10 bg-white/10 text-slate-100 placeholder:text-slate-400'
                  : 'border-slate-200 bg-white text-slate-800 focus:border-brand-500'
              )}
              placeholder="What is the current customer intent?"
              value={query}
              onChange={(event: ChangeEvent<HTMLInputElement>) => setQuery(event.target.value)}
              onKeyDown={(event: KeyboardEvent<HTMLInputElement>) => event.key === 'Enter' && handleRagQuery()}
            />
            <button
              className={clsx(
                'inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium shadow-sm transition',
                isDesignTwo
                  ? 'bg-emerald-400 text-slate-900 hover:bg-emerald-300'
                  : 'bg-brand-600 text-white hover:bg-brand-500'
              )}
              onClick={handleRagQuery}
              type="button"
            >
              {ragIsLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Ask'}
            </button>
          </div>
          {ragAnswer && (
            <div
              className={clsx(
                'rounded-md border p-4 text-sm',
                isDesignTwo
                  ? 'border-emerald-400/40 bg-emerald-400/10 text-emerald-200'
                  : 'border-brand-100 bg-brand-50 text-brand-800'
              )}
            >
              <p className="whitespace-pre-line">{ragAnswer}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Interaction Timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {data.interactions.map((interaction: Interaction) => (
              <TimelineItem
                key={interaction.id}
                interaction={interaction}
                onFeedback={(rating: boolean) =>
                  feedbackMutation.mutate({
                    insight_id: interaction.insight?.id ?? 0,
                    rating,
                    reason_code: rating ? 'accurate' : 'inaccurate',
                  })
                }
              />
            ))}
            {data.interactions.length === 0 && (
              <p className={clsx('text-sm', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
                No interactions recorded yet.
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function CardPlaceholder({ text, tone = 'default' }: { text: string; tone?: 'default' | 'error' }) {
  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';
  const toneClasses =
    tone === 'error'
      ? isDesignTwo
        ? 'border-rose-400/40 bg-rose-500/10 text-rose-200'
        : 'border-red-200 bg-red-50 text-red-600'
      : isDesignTwo
      ? 'border-white/10 bg-white/5 text-slate-300'
      : 'border-slate-200 bg-slate-50 text-slate-500';

  return (
    <Card className={`border border-dashed ${toneClasses}`}>
      <CardContent>{text}</CardContent>
    </Card>
  );
}

interface TimelineItemProps {
  interaction: Interaction;
  onFeedback: (rating: boolean) => void;
}

const TimelineItem: FC<TimelineItemProps> = ({ interaction, onFeedback }: TimelineItemProps) => {
  const Icon = getIcon(interaction.channel);
  const insight = interaction.insight;
  const designVariant = useDesignVariant();
  const isDesignTwo = designVariant === 'design2';

  return (
    <div
      className={clsx(
        'relative border-l pl-6',
        isDesignTwo ? 'border-white/10' : 'border-slate-200'
      )}
    >
      <span
        className={clsx(
          'absolute -left-3 flex h-6 w-6 items-center justify-center rounded-full border',
          isDesignTwo ? 'border-white/20 bg-white/10' : 'border-slate-200 bg-white'
        )}
      >
        <Icon className={clsx('h-4 w-4', isDesignTwo ? 'text-emerald-200' : 'text-slate-500')} />
      </span>
      <div className="space-y-2">
        <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <div>
            <p className={clsx('text-sm font-semibold capitalize', isDesignTwo ? 'text-white' : 'text-slate-700')}>
              {interaction.channel}
            </p>
            <p className={clsx('text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              {new Date(interaction.timestamp).toLocaleString()}
            </p>
          </div>
          {insight && (
            <div className={clsx('flex items-center gap-2 text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              <Badge variant="secondary" className="capitalize">
                {insight.intent.replace('_', ' ')}
              </Badge>
              <Badge variant={insight.sentiment === 'negative' ? 'destructive' : 'success'}>
                {insight.sentiment}
              </Badge>
              <Badge variant={insight.risk_score > 0.6 ? 'destructive' : 'secondary'}>
                Risk {Math.round(insight.risk_score * 100)}%
              </Badge>
            </div>
          )}
        </div>
        <p className={clsx('text-sm whitespace-pre-line', isDesignTwo ? 'text-slate-100' : 'text-slate-600')}>
          {interaction.content}
        </p>
        {insight && (
          <div
            className={clsx(
              'rounded-md border p-3',
              isDesignTwo ? 'border-white/10 bg-white/5' : 'border-slate-200 bg-slate-50'
            )}
          >
            <p className={clsx('text-sm font-medium', isDesignTwo ? 'text-white' : 'text-slate-700')}>Summary</p>
            <p className={clsx('mt-1 text-sm', isDesignTwo ? 'text-slate-200' : 'text-slate-600')}>
              {insight.summary}
            </p>
            <div className={clsx('mt-3 flex items-center gap-3 text-xs', isDesignTwo ? 'text-slate-300' : 'text-slate-500')}>
              <span>Was this helpful?</span>
              <button
                type="button"
                onClick={() => onFeedback(true)}
                className={clsx(
                  'inline-flex items-center gap-1 rounded-md border px-2 py-1 transition',
                  isDesignTwo
                    ? 'border-emerald-400/40 text-emerald-200 hover:bg-emerald-400/10'
                    : 'border-slate-200 text-emerald-600 hover:border-emerald-200 hover:bg-emerald-50'
                )}
              >
                <ThumbsUp className="h-3 w-3" /> Helpful
              </button>
              <button
                type="button"
                onClick={() => onFeedback(false)}
                className={clsx(
                  'inline-flex items-center gap-1 rounded-md border px-2 py-1 transition',
                  isDesignTwo
                    ? 'border-rose-400/40 text-rose-200 hover:bg-rose-400/10'
                    : 'border-slate-200 text-red-600 hover:border-red-200 hover:bg-red-50'
                )}
              >
                <ThumbsDown className="h-3 w-3" /> Needs work
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

function getIcon(channel: string) {
  switch (channel) {
    case 'email':
      return Mail;
    case 'call':
      return Phone;
    case 'chat':
      return MessageSquare;
    default:
      return Reply;
  }
}
