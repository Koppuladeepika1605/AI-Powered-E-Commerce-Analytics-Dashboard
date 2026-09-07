import React from 'react';
import {
  Sparkles,
  RefreshCw,
  Layers,
  TrendingUp,
  Globe2,
  Cpu,
  Lightbulb,
  CheckCircle2,
  AlertCircle,
} from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onRefresh: () => void;
  isLoading: boolean;
  dbStatus: 'online' | 'error' | 'checking';
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  onRefresh,
  isLoading,
  dbStatus,
}) => {
  const tabs = [
    { id: 'overview', label: '1. Executive Overview', icon: Layers, badge: 'PBI Page 1' },
    { id: 'regional_product', label: '2. Regional & Product Analysis', icon: Globe2, badge: 'PBI Page 2' },
    { id: 'operations', label: '3. Operations Analysis', icon: TrendingUp, badge: 'PBI Page 3' },
    { id: 'ml', label: 'ML Demand Forecasting', icon: Cpu, badge: 'Phase 6' },
    { id: 'powerbi', label: 'Power BI Showcase & Architecture', icon: Sparkles, badge: 'Source of Truth' },
    { id: 'insights', label: 'AI Business Insights', icon: Lightbulb, badge: 'Live' },
  ];

  return (
    <header style={{ borderBottom: '1px solid var(--border-subtle)', background: 'rgba(9, 13, 22, 0.85)', backdropFilter: 'blur(20px)', position: 'sticky', top: 0, zIndex: 50 }}>
      <div style={{ maxWidth: '1440px', margin: '0 auto', padding: '16px 24px' }}>
        {/* Top Branding Row */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div
              style={{
                width: '42px',
                height: '42px',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #6366f1 0%, #06b6d4 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(99, 102, 241, 0.35)',
              }}
            >
              <Sparkles size={22} color="#ffffff" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <h1 style={{ fontSize: '1.35rem', fontWeight: 800, letterSpacing: '-0.03em' }} className="gradient-text">
                  AI-Powered E-Commerce Analytics
                </h1>
                <span className="badge badge-indigo">
                  <Cpu size={12} /> Enterprise Edition
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                128,975 Verified Transactions • PostgreSQL Analytics • Scikit-Learn ML Forecaster
              </p>
            </div>
          </div>

          {/* Right Action Tools */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {/* Live Database Badge */}
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--border-subtle)',
                fontSize: '0.78rem',
              }}
            >
              {dbStatus === 'online' ? (
                <>
                  <CheckCircle2 size={14} color="#10b981" />
                  <span style={{ color: '#34d399', fontWeight: 600 }}>API & SQL Engine Online</span>
                </>
              ) : dbStatus === 'error' ? (
                <>
                  <AlertCircle size={14} color="#f43f5e" />
                  <span style={{ color: '#fb7185', fontWeight: 600 }}>API Disconnected</span>
                </>
              ) : (
                <>
                  <RefreshCw size={14} className="spin" color="#6366f1" />
                  <span style={{ color: 'var(--text-muted)' }}>Connecting...</span>
                </>
              )}
            </div>

            {/* Refresh Button */}
            <button
              onClick={onRefresh}
              disabled={isLoading}
              className="btn-secondary"
              title="Refresh Dashboard Data"
              style={{ padding: '8px 14px', fontSize: '0.82rem' }}
            >
              <RefreshCw size={14} style={{ animation: isLoading ? 'spin 1s linear infinite' : 'none' }} />
              <span>{isLoading ? 'Updating...' : 'Refresh'}</span>
            </button>
          </div>
        </div>

        {/* Tab Navigation Row */}
        <nav style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`btn-tab ${isActive ? 'active' : ''}`}
                style={{ whiteSpace: 'nowrap' }}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
                {tab.badge && (
                  <span
                    style={{
                      fontSize: '0.68rem',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      background: isActive ? 'rgba(99, 102, 241, 0.3)' : 'rgba(255, 255, 255, 0.08)',
                      color: isActive ? '#a5b4fc' : 'var(--text-muted)',
                      fontWeight: 700,
                    }}
                  >
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      <style>{`
        @keyframes spin {
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </header>
  );
};
