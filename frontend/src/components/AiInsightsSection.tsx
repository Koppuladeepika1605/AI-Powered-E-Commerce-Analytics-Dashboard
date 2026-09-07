import React, { useState, useEffect } from 'react';
import {
  Lightbulb,
  Sparkles,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  ShieldAlert,
  Zap,
  Tag,
  Cpu,
} from 'lucide-react';
import { ApiService } from '../services/api';
import { InsightsData, InsightItem } from '../types';

export const AiInsightsSection: React.FC = () => {
  const [insightsData, setInsightsData] = useState<InsightsData | null>(null);
  const [activeCategory, setActiveCategory] = useState<string>('ALL');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInsights = async () => {
      setIsLoading(true);
      try {
        const data = await ApiService.getAiInsights();
        setInsightsData(data);
      } catch (err: any) {
        setError(err.message || 'Failed to generate AI insights.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchInsights();
  }, []);

  const categories = ['ALL', 'Revenue Opportunity', 'Operations', 'Geography', 'Product Catalog'];

  const filteredInsights = insightsData?.insights.filter((item) => {
    if (activeCategory === 'ALL') return true;
    return item.category.toLowerCase() === activeCategory.toLowerCase();
  }) || [];

  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return <span className="badge badge-rose"><ShieldAlert size={12} /> High Priority</span>;
      case 'medium':
        return <span className="badge badge-amber"><AlertTriangle size={12} /> Medium Priority</span>;
      case 'positive':
        return <span className="badge badge-emerald"><CheckCircle2 size={12} /> Commercial Win</span>;
      default:
        return <span className="badge badge-indigo"><Sparkles size={12} /> Observation</span>;
    }
  };

  return (
    <div style={{ marginBottom: '32px' }}>
      {/* Executive Summary Card */}
      {insightsData && (
        <div
          className="glass-card"
          style={{
            marginBottom: '20px',
            background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.85) 0%, rgba(30, 27, 75, 0.5) 100%)',
            border: '1px solid rgba(99, 102, 241, 0.25)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div
                style={{
                  width: '38px',
                  height: '38px',
                  borderRadius: '10px',
                  background: 'var(--accent-primary-gradient)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <Lightbulb size={20} color="#ffffff" />
              </div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <h2 style={{ fontSize: '1.15rem', fontWeight: 800 }}>AI Business Intelligence & Strategy Engine</h2>
                  <span className="badge badge-indigo">
                    <Cpu size={12} /> Rules & Analytics Engine v1.0
                  </span>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  Validated analytical patterns synthesized into actionable commercial directives
                </p>
              </div>
            </div>

            {/* Commercial Health Score */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                  Catalog Health Score
                </span>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#34d399' }}>
                  {insightsData.executive_summary.health_score}/100
                </div>
              </div>
              <div
                style={{
                  width: '42px',
                  height: '42px',
                  borderRadius: '50%',
                  border: '3px solid #10b981',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '0.85rem',
                  color: '#34d399',
                }}
              >
                A
              </div>
            </div>
          </div>

          <p style={{ fontSize: '0.92rem', color: '#ffffff', fontWeight: 600, lineHeight: 1.5, marginBottom: '14px' }}>
            "{insightsData.executive_summary.headline}"
          </p>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '12px',
              padding: '12px 16px',
              borderRadius: '10px',
              background: 'rgba(0, 0, 0, 0.25)',
              border: '1px solid rgba(255, 255, 255, 0.05)',
              fontSize: '0.8rem',
            }}
          >
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Top Driver: </span>
              <strong style={{ color: '#818cf8' }}>{insightsData.executive_summary.primary_revenue_driver}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Primary Leakage: </span>
              <strong style={{ color: '#fb7185' }}>{insightsData.executive_summary.top_operational_leak}</strong>
            </div>
            <div>
              <span style={{ color: 'var(--text-muted)' }}>Focus Recommendation: </span>
              <strong style={{ color: '#34d399' }}>{insightsData.executive_summary.recommended_focus_area}</strong>
            </div>
          </div>
        </div>
      )}

      {/* Category Filter Chips */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', marginBottom: '18px', paddingBottom: '4px' }}>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`btn-tab ${activeCategory === cat ? 'active' : ''}`}
            style={{ fontSize: '0.8rem', padding: '6px 14px' }}
          >
            <Tag size={13} />
            <span>{cat === 'ALL' ? 'All Intelligence Areas' : cat}</span>
          </button>
        ))}
      </div>

      {/* Insights Cards Grid */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="skeleton" style={{ height: '120px', width: '100%', borderRadius: '16px' }} />
          ))
        ) : filteredInsights.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '30px' }}>No insights in this category.</p>
        ) : (
          filteredInsights.map((item) => (
            <div
              key={item.id}
              className="glass-card glass-card-interactive"
              style={{
                borderLeft: `4px solid ${
                  item.severity === 'high'
                    ? '#f43f5e'
                    : item.severity === 'medium'
                    ? '#f59e0b'
                    : '#10b981'
                }`,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px', marginBottom: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                    {item.title}
                  </h3>
                  <span className="badge badge-indigo" style={{ fontSize: '0.7rem' }}>
                    {item.category}
                  </span>
                </div>
                {getSeverityBadge(item.severity)}
              </div>

              <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '12px' }}>
                {item.summary}
              </p>

              {/* Impact Metric & Actionable Recommendation Banner */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '12px',
                  padding: '10px 14px',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid rgba(255, 255, 255, 0.04)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Zap size={14} color="#f59e0b" />
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    {item.impact_metric}: <strong style={{ color: '#ffffff' }}>{item.impact_value}</strong>
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: '#38bdf8' }}>
                  <ArrowRight size={14} />
                  <span style={{ fontWeight: 600 }}>{item.actionable_recommendation}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* LLM Extensibility Banner */}
      <div
        className="glass-card"
        style={{
          marginTop: '20px',
          padding: '14px 18px',
          background: 'rgba(99, 102, 241, 0.06)',
          border: '1px dashed rgba(99, 102, 241, 0.3)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '10px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Sparkles size={18} color="#818cf8" />
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <strong>Future AI/LLM Integration:</strong> This intelligence layer is designed with plug-and-play support for OpenAI / Gemini API integration to dynamically summarize live business cohorts.
          </span>
        </div>
        <span className="badge badge-indigo">LLM-Ready Interface</span>
      </div>
    </div>
  );
};
