import axios, { type InternalAxiosRequestConfig } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const AUTH_TOKEN = process.env.NEXT_PUBLIC_DEMO_TOKEN || 'demo-token';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${AUTH_TOKEN}`,
  },
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (typeof window !== 'undefined') {
    const storedToken = window.localStorage.getItem('journeylensToken');
    if (storedToken) {
      config.headers.Authorization = `Bearer ${storedToken}`;
    }
  }
  return config;
});

export interface Account {
  id: number;
  name: string;
  industry?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Insight {
  id: number;
  interaction_id: number;
  intent: string;
  sentiment: string;
  risk_score: number;
  confidence: number;
  summary: string;
  keywords?: string;
  created_at: string;
  updated_at: string;
}

export interface Interaction {
  id: number;
  account_id: number;
  contact_id?: number;
  channel: string;
  content: string;
  summary?: string;
  timestamp: string;
  created_at: string;
  updated_at: string;
  source_file?: string;
  insight?: Insight;
}

export interface AccountWithInsights extends Account {
  interactions: Interaction[];
}

export interface DashboardAccount {
  account_id: number;
  account_name: string;
  risk_score: number;
  recent_interactions: number;
  last_interaction?: string;
  next_action: string;
}

export interface EvaluationMetrics {
  ai_coverage: number;
  feedback_rate: number;
  useful_rate: number;
  total_insights: number;
  avg_confidence: number;
  performance_trend: string;
}

export interface RagResponse {
  account_id: number;
  query: string;
  answer: string;
  supporting_insights: Insight[];
  timestamp: string;
}

export interface FeedbackPayload {
  insight_id: number;
  rating: boolean;
  reason_code: string;
  comments?: string;
}

export interface CreateInteractionPayload {
  account_id: number;
  contact_id?: number;
  channel: string;
  content: string;
  timestamp?: string;
}

export const api = {
  getHealth: () => apiClient.get('/health'),
  getAccounts: () => apiClient.get<Account[]>('/accounts'),
  getAccount: (accountId: number) => apiClient.get<AccountWithInsights>(`/accounts/${accountId}`),
  getDashboard: () => apiClient.get<DashboardAccount[]>('/dashboard/csm'),
  getRecentInsights: (limit = 6) => apiClient.get<Insight[]>(`/insights/recent`, { params: { limit } }),
  createInteraction: (payload: CreateInteractionPayload) => apiClient.post('/interactions', payload),
  getRagResponse: (accountId: number, query: string) =>
    apiClient.get<RagResponse>(`/accounts/${accountId}/rag`, { params: { query } }),
  submitFeedback: (payload: FeedbackPayload) => apiClient.post('/feedback', payload),
  getEvaluationMetrics: () => apiClient.get<EvaluationMetrics>('/evaluations/metrics'),
};
