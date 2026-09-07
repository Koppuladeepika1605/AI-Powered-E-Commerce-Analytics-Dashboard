import React, { useState } from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import { TrendingUp, Calendar, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { SalesTrendData } from '../types';

interface SalesTrendSectionProps {
  trendData: SalesTrendData | null;
  granularity: 'monthly' | 'daily';
  onGranularityChange: (gran: 'monthly' | 'daily') => void;
  isLoading: boolean;
}

export const SalesTrendSection: React.FC<SalesTrendSectionProps> = ({
  trendData,
  granularity,
  onGranularityChange,
  isLoading,
}) => {
  const [metricMode, setMetricMode] = useState<'revenue' | 'volume'>('revenue');

  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `₹${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 100000) return `₹${(val / 100000).toFixed(1)} L`;
    if (val >= 1000) return `₹${(val / 1000).toFixed(0)}k`;
    return `₹${val}`;
  };

  const chartData = trendData?.data || [];

  return (
    <div className="glass-card" style={{ marginBottom: '24px' }}>
      {/* Header Controls */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '12px',
          marginBottom: '20px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <TrendingUp size={18} color="var(--accent-primary)" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h2 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Realized Revenue Trend</h2>
              <span className="badge badge-indigo">Power BI Line Visual</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
              Sum of Realized_Revenue by Date (Historical Q2 2022 Performance)
            </p>
          </div>
        </div>

        {/* Action Toggles */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          {/* Revenue vs Volume Switch */}
          <div style={{ display: 'inline-flex', background: 'rgba(255, 255, 255, 0.04)', borderRadius: '8px', padding: '3px' }}>
            <button
              onClick={() => setMetricMode('revenue')}
              style={{
                padding: '5px 12px',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: '6px',
                background: metricMode === 'revenue' ? 'var(--accent-primary)' : 'transparent',
                color: metricMode === 'revenue' ? '#ffffff' : 'var(--text-muted)',
              }}
            >
              Revenue (INR)
            </button>
            <button
              onClick={() => setMetricMode('volume')}
              style={{
                padding: '5px 12px',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: '6px',
                background: metricMode === 'volume' ? 'var(--accent-primary)' : 'transparent',
                color: metricMode === 'volume' ? '#ffffff' : 'var(--text-muted)',
              }}
            >
              Order Volume & Qty
            </button>
          </div>

          {/* Granularity Switch */}
          <div style={{ display: 'inline-flex', background: 'rgba(255, 255, 255, 0.04)', borderRadius: '8px', padding: '3px' }}>
            <button
              onClick={() => onGranularityChange('monthly')}
              style={{
                padding: '5px 12px',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: '6px',
                background: granularity === 'monthly' ? 'rgba(99, 102, 241, 0.3)' : 'transparent',
                color: granularity === 'monthly' ? '#818cf8' : 'var(--text-muted)',
              }}
            >
              Monthly
            </button>
            <button
              onClick={() => onGranularityChange('daily')}
              style={{
                padding: '5px 12px',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: '6px',
                background: granularity === 'daily' ? 'rgba(99, 102, 241, 0.3)' : 'transparent',
                color: granularity === 'daily' ? '#818cf8' : 'var(--text-muted)',
              }}
            >
              Daily
            </button>
          </div>
        </div>
      </div>

      {/* Chart Canvas */}
      <div style={{ width: '100%', height: '320px' }}>
        {isLoading ? (
          <div className="skeleton" style={{ width: '100%', height: '100%' }} />
        ) : metricMode === 'revenue' ? (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
              <defs>
                <linearGradient id="realizedGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="grossGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
              <XAxis
                dataKey="period"
                stroke="var(--text-muted)"
                fontSize={11}
                tickLine={false}
                tickFormatter={(val) => (granularity === 'daily' && val.length > 5 ? val.slice(5) : val)}
              />
              <YAxis
                stroke="var(--text-muted)"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tickFormatter={formatCurrency}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(15, 23, 42, 0.95)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
                  fontSize: '0.82rem',
                }}
                formatter={(value: any) => [`₹${Number(value).toLocaleString('en-IN')}`, '']}
              />
              <Legend wrapperStyle={{ fontSize: '0.8rem', paddingTop: '10px' }} />
              <Area
                type="monotone"
                dataKey="gross_amount"
                name="Gross Listed Sales"
                stroke="#6366f1"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#grossGrad)"
              />
              <Area
                type="monotone"
                dataKey="realized_revenue"
                name="Realized Net Revenue"
                stroke="#10b981"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#realizedGrad)"
              />
            </AreaChart>
          </ResponsiveContainer>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
              <XAxis
                dataKey="period"
                stroke="var(--text-muted)"
                fontSize={11}
                tickLine={false}
                tickFormatter={(val) => (granularity === 'daily' && val.length > 5 ? val.slice(5) : val)}
              />
              <YAxis stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(15, 23, 42, 0.95)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
                  fontSize: '0.82rem',
                }}
              />
              <Legend wrapperStyle={{ fontSize: '0.8rem', paddingTop: '10px' }} />
              <Bar dataKey="order_count" name="Unique Orders" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              <Bar dataKey="units_sold" name="Units Sold" fill="#a855f7" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
