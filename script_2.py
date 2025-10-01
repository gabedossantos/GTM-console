# Create Next.js frontend structure for JourneyLens
frontend_structure = '''
# JourneyLens Frontend - Next.js Implementation
# AI-powered GTM console user interface

# =============================================================================
# PACKAGE.JSON DEPENDENCIES
# =============================================================================

package_json = {
  "name": "journeylens-frontend",
  "version": "1.0.0",
  "private": True,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.0.0",
    "@tailwindcss/forms": "^0.5.0",
    "autoprefixer": "^10.0.0",
    "postcss": "^8.0.0",
    "@headlessui/react": "^1.7.0",
    "@heroicons/react": "^2.0.0",
    "axios": "^1.6.0",
    "react-query": "^3.39.0",
    "recharts": "^2.8.0",
    "date-fns": "^2.30.0",
    "react-hook-form": "^7.47.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    "lucide-react": "^0.292.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}

# =============================================================================
# API CLIENT (lib/api.ts)
# =============================================================================

api_client = """
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Types
export interface Interaction {
  id: number;
  account_id: number;
  contact_id?: number;
  channel: string;
  content: string;
  timestamp: string;
}

export interface Insight {
  id: number;
  intent: string;
  sentiment: string;
  risk_score: number;
  summary: string;
  confidence: number;
  created_at: string;
}

export interface AccountDashboard {
  account_id: number;
  account_name: string;
  risk_score: number;
  recent_interactions: number;
  last_interaction: string;
  next_action: string;
}

export interface FeedbackCreate {
  insight_id: number;
  rating: boolean;
  reason_code: string;
  comments?: string;
}

export interface EvaluationMetrics {
  ai_coverage: number;
  feedback_rate: number;
  useful_rate: number;
  total_insights: number;
  avg_confidence: number;
  performance_trend: string;
}

// API functions
export const api = {
  // Dashboard endpoints
  getCsmDashboard: () => 
    apiClient.get<AccountDashboard[]>('/dashboard/csm'),
  
  getAeDashboard: () => 
    apiClient.get<AccountDashboard[]>('/dashboard/ae'),
  
  getSupportDashboard: () => 
    apiClient.get<AccountDashboard[]>('/dashboard/support'),
  
  // Account insights
  getAccountRagQuery: (accountId: number, query: string) =>
    apiClient.get(`/accounts/${accountId}/rag`, { params: { query } }),
  
  // Interactions
  createInteraction: (data: Omit<Interaction, 'id' | 'timestamp'>) =>
    apiClient.post<Insight>('/interactions/', data),
  
  // Feedback
  createFeedback: (data: FeedbackCreate) =>
    apiClient.post('/feedback/', data),
  
  // Evaluations
  getEvaluationMetrics: () =>
    apiClient.get<EvaluationMetrics>('/evaluations/metrics'),
  
  // File upload
  uploadConversations: (files: File[], accountId?: number) => {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    if (accountId) formData.append('account_id', accountId.toString());
    
    return apiClient.post('/upload/conversations', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }
};
"""

# =============================================================================
# DASHBOARD COMPONENTS
# =============================================================================

csm_dashboard = """
// components/dashboards/CsmDashboard.tsx
import React from 'react';
import { useQuery } from 'react-query';
import { api, AccountDashboard } from '../../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { AlertTriangle, TrendingUp, Clock } from 'lucide-react';

export const CsmDashboard: React.FC = () => {
  const { data: accounts, isLoading, error } = useQuery(
    'csm-dashboard',
    () => api.getCsmDashboard().then(res => res.data),
    { refetchInterval: 30000 } // Refresh every 30 seconds
  );

  if (isLoading) return <div>Loading CSM dashboard...</div>;
  if (error) return <div>Error loading dashboard</div>;

  const highRiskAccounts = accounts?.filter(acc => acc.risk_score > 0.8) || [];
  const mediumRiskAccounts = accounts?.filter(acc => acc.risk_score > 0.6 && acc.risk_score <= 0.8) || [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Accounts at Risk Today */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Accounts at Risk Today</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{highRiskAccounts.length}</div>
            <p className="text-xs text-muted-foreground">
              +{mediumRiskAccounts.length} medium risk
            </p>
            <div className="mt-4 space-y-2">
              {highRiskAccounts.slice(0, 3).map(account => (
                <div key={account.account_id} className="flex items-center justify-between">
                  <span className="text-sm font-medium">{account.account_name}</span>
                  <Badge variant="destructive">
                    {Math.round(account.risk_score * 100)}%
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Interaction Deltas */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">7-Day Interaction Delta</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">+23%</div>
            <p className="text-xs text-muted-foreground">
              vs previous week
            </p>
            <div className="mt-4">
              <div className="text-sm">
                <div className="flex justify-between">
                  <span>Support Tickets</span>
                  <span className="text-green-600">+15%</span>
                </div>
                <div className="flex justify-between">
                  <span>Check-in Calls</span>
                  <span className="text-green-600">+31%</span>
                </div>
                <div className="flex justify-between">
                  <span>Email Exchanges</span>
                  <span className="text-yellow-600">-5%</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Next Best Actions */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Next Best Actions</CardTitle>
            <Clock className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                <div>
                  <p className="text-sm font-medium">Schedule check-in call</p>
                  <p className="text-xs text-muted-foreground">Acme Corp (Risk: 92%)</p>
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                <div>
                  <p className="text-sm font-medium">Review usage metrics</p>
                  <p className="text-xs text-muted-foreground">TechFlow Inc (Risk: 75%)</p>
                </div>
              </div>
              <div className="flex items-start space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div>
                  <p className="text-sm font-medium">Send feature update</p>
                  <p className="text-xs text-muted-foreground">DataCorp (Risk: 45%)</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Account List */}
      <Card>
        <CardHeader>
          <CardTitle>Account Risk Overview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {accounts?.map(account => (
              <div key={account.account_id} className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <h3 className="font-medium">{account.account_name}</h3>
                  <p className="text-sm text-muted-foreground">
                    {account.recent_interactions} interactions • Last: {new Date(account.last_interaction).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center space-x-4">
                  <Badge 
                    variant={account.risk_score > 0.8 ? "destructive" : account.risk_score > 0.6 ? "default" : "secondary"}
                  >
                    Risk: {Math.round(account.risk_score * 100)}%
                  </Badge>
                  <button className="text-sm text-blue-600 hover:underline">
                    {account.next_action}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
"""

# =============================================================================
# ACCOUNT TIMELINE COMPONENT
# =============================================================================

account_timeline = """
// components/AccountTimeline.tsx
import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { api } from '../lib/api';
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card';
import { Badge } from './ui/Badge';
import { MessageSquare, Phone, Mail, Upload, ThumbsUp, ThumbsDown } from 'lucide-react';

interface TimelineProps {
  accountId: number;
}

export const AccountTimeline: React.FC<TimelineProps> = ({ accountId }) => {
  const [ragQuery, setRagQuery] = useState('');
  const [ragResponse, setRagResponse] = useState('');

  const handleRagQuery = async () => {
    if (!ragQuery.trim()) return;
    
    try {
      const response = await api.getAccountRagQuery(accountId, ragQuery);
      setRagResponse(response.data.answer);
    } catch (error) {
      setRagResponse('Error generating insights');
    }
  };

  const getChannelIcon = (channel: string) => {
    switch (channel) {
      case 'email': return <Mail className="h-4 w-4" />;
      case 'call': return <Phone className="h-4 w-4" />;
      case 'file_upload': return <Upload className="h-4 w-4" />;
      default: return <MessageSquare className="h-4 w-4" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600';
      case 'negative': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  // Mock timeline data - would come from API
  const timelineData = [
    {
      id: 1,
      timestamp: '2024-01-15T10:30:00Z',
      channel: 'email',
      intent: 'pricing_inquiry',
      sentiment: 'neutral',
      risk_score: 0.3,
      summary: 'Customer inquiring about enterprise pricing options and volume discounts.',
      confidence: 0.87
    },
    {
      id: 2,
      timestamp: '2024-01-14T14:15:00Z',
      channel: 'call',
      intent: 'support_request',
      sentiment: 'negative',
      risk_score: 0.7,
      summary: 'Technical issues with integration, customer expressing frustration.',
      confidence: 0.92
    },
    {
      id: 3,
      timestamp: '2024-01-12T09:00:00Z',
      channel: 'file_upload',
      intent: 'product_feedback',
      sentiment: 'positive',
      risk_score: 0.2,
      summary: 'Positive feedback on new features, suggestions for improvements.',
      confidence: 0.85
    }
  ];

  return (
    <div className="space-y-6">
      {/* RAG Query Interface */}
      <Card>
        <CardHeader>
          <CardTitle>Account Insights (AI-Powered)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex space-x-2">
              <input
                type="text"
                placeholder="Ask about this account... (e.g., 'What's the current customer intent?')"
                value={ragQuery}
                onChange={(e) => setRagQuery(e.target.value)}
                className="flex-1 px-3 py-2 border rounded-md"
                onKeyPress={(e) => e.key === 'Enter' && handleRagQuery()}
              />
              <button
                onClick={handleRagQuery}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Ask AI
              </button>
            </div>
            {ragResponse && (
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-md">
                <h4 className="font-medium text-blue-900 mb-2">AI Insights:</h4>
                <p className="text-blue-800">{ragResponse}</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Timeline */}
      <Card>
        <CardHeader>
          <CardTitle>Interaction Timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {timelineData.map((item, index) => (
              <div key={item.id} className="relative">
                {index !== timelineData.length - 1 && (
                  <div className="absolute left-4 top-8 bottom-0 w-px bg-gray-200"></div>
                )}
                
                <div className="flex space-x-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-white border-2 border-gray-300 rounded-full flex items-center justify-center">
                    {getChannelIcon(item.channel)}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-sm font-medium capitalize">{item.intent.replace('_', ' ')}</h4>
                        <p className="text-xs text-gray-500">
                          {new Date(item.timestamp).toLocaleString()} • {item.channel}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge 
                          variant={item.risk_score > 0.6 ? "destructive" : "secondary"}
                          className="text-xs"
                        >
                          Risk: {Math.round(item.risk_score * 100)}%
                        </Badge>
                        <span className={`text-xs font-medium capitalize ${getSentimentColor(item.sentiment)}`}>
                          {item.sentiment}
                        </span>
                      </div>
                    </div>
                    
                    <p className="mt-2 text-sm text-gray-700">{item.summary}</p>
                    
                    <div className="mt-3 flex items-center justify-between">
                      <span className="text-xs text-gray-500">
                        Confidence: {Math.round(item.confidence * 100)}%
                      </span>
                      
                      {/* Feedback Widget */}
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-500">Helpful?</span>
                        <button 
                          className="p-1 text-gray-400 hover:text-green-600"
                          onClick={() => api.createFeedback({
                            insight_id: item.id,
                            rating: true,
                            reason_code: 'accurate'
                          })}
                        >
                          <ThumbsUp className="h-3 w-3" />
                        </button>
                        <button 
                          className="p-1 text-gray-400 hover:text-red-600"
                          onClick={() => api.createFeedback({
                            insight_id: item.id,
                            rating: false,
                            reason_code: 'inaccurate'
                          })}
                        >
                          <ThumbsDown className="h-3 w-3" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
"""

# =============================================================================
# MAIN APP COMPONENT
# =============================================================================

main_app = """
// pages/_app.tsx
import { QueryClient, QueryClientProvider } from 'react-query';
import { useState } from 'react';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  );
}

export default MyApp;

// pages/index.tsx
import React, { useState } from 'react';
import { CsmDashboard } from '../components/dashboards/CsmDashboard';
import { AccountTimeline } from '../components/AccountTimeline';
import { EvaluationMetrics } from '../components/EvaluationMetrics';

export default function HomePage() {
  const [activeRole, setActiveRole] = useState<'csm' | 'ae' | 'support'>('csm');
  const [selectedAccount, setSelectedAccount] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">JourneyLens</h1>
              <span className="ml-2 text-sm text-gray-500">AI-Powered GTM Console</span>
            </div>
            
            <div className="flex items-center space-x-4">
              <select
                value={activeRole}
                onChange={(e) => setActiveRole(e.target.value as any)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm"
              >
                <option value="csm">Customer Success</option>
                <option value="ae">Account Executive</option>
                <option value="support">Support</option>
              </select>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Dashboard Content */}
        <div className="px-4 py-6 sm:px-0">
          {activeRole === 'csm' && <CsmDashboard />}
          {selectedAccount && <AccountTimeline accountId={selectedAccount} />}
        </div>
      </div>
    </div>
  );
}
"""

print("✅ Next.js frontend structure components:")
print("1. API client with TypeScript types")
print("2. CSM Dashboard with risk monitoring")
print("3. Account Timeline with RAG queries")
print("4. Main App with role switching")
print("5. Comprehensive component structure")

# Save individual files
files_to_create = [
    ("frontend_package.json", str(package_json)),
    ("api_client.ts", api_client),
    ("csm_dashboard.tsx", csm_dashboard),
    ("account_timeline.tsx", account_timeline),
    ("main_app.tsx", main_app)
]

for filename, content in files_to_create:
    with open(filename, "w") as f:
        f.write(content)
    print(f"   - {filename}")
'''

# Save the complete frontend structure
with open("journeylens_frontend_structure.md", "w") as f:
    f.write(frontend_structure)

print("✅ JourneyLens Next.js frontend structure saved to journeylens_frontend_structure.md")
print("\nFrontend Features:")
print("- TypeScript with full type safety")
print("- React Query for data fetching")
print("- Tailwind CSS for styling")
print("- Role-based dashboard views")
print("- Real-time RAG query interface")
print("- Interactive timeline with feedback")
print("- File upload functionality")
print("- Responsive design components")