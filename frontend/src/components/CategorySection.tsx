import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import { Tag, PieChart as PieIcon, Award } from 'lucide-react';
import { CategoryItem } from '../types';

interface CategorySectionProps {
  categories: CategoryItem[];
  isLoading: boolean;
}

const CATEGORY_COLORS = [
  '#6366f1',
  '#06b6d4',
  '#10b981',
  '#f59e0b',
  '#ec4899',
  '#8b5cf6',
  '#14b8a6',
  '#f97316',
  '#64748b',
  '#a855f7',
];

export const CategorySection: React.FC<CategorySectionProps> = ({ categories, isLoading }) => {
  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `₹${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 100000) return `₹${(val / 100000).toFixed(1)} L`;
    if (val >= 1000) return `₹${(val / 1000).toFixed(0)}k`;
    return `₹${val}`;
  };

  const pieData = categories.slice(0, 6).map((c) => ({
    name: c.category,
    value: c.realized_revenue,
    share: c.revenue_share_pct,
  }));

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
        gap: '20px',
        marginBottom: '24px',
      }}
    >
      {/* 1. Category Revenue Bar Breakdown */}
      <div className="glass-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Tag size={16} color="var(--accent-primary)" />
            <div>
              <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Revenue by Category</h3>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Sum of Realized_Revenue by Category</p>
            </div>
          </div>
          <span className="badge badge-indigo">Power BI Bar Visual</span>
        </div>

        <div style={{ width: '100%', height: '280px' }}>
          {isLoading ? (
            <div className="skeleton" style={{ width: '100%', height: '100%' }} />
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={categories}
                layout="vertical"
                margin={{ top: 5, right: 20, left: 40, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" horizontal={false} />
                <XAxis type="number" stroke="var(--text-muted)" fontSize={11} tickFormatter={formatCurrency} />
                <YAxis dataKey="category" type="category" stroke="var(--text-secondary)" fontSize={12} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '10px',
                    fontSize: '0.82rem',
                  }}
                  formatter={(val: any, name: any) => [
                    name === 'realized_revenue' ? `₹${Number(val).toLocaleString('en-IN')}` : val,
                    name === 'realized_revenue' ? 'Realized Revenue' : name,
                  ]}
                />
                <Bar dataKey="realized_revenue" name="Realized Revenue" fill="#6366f1" radius={[0, 6, 6, 0]}>
                  {categories.map((_, idx) => (
                    <Cell key={`cell-${idx}`} fill={CATEGORY_COLORS[idx % CATEGORY_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* 2. Category Share Doughnut & Realization Table */}
      <div className="glass-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PieIcon size={16} color="var(--accent-cyan)" />
            <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Revenue Share Distribution</h3>
          </div>
          <span className="badge badge-cyan">Top 6 Share</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ width: '200px', height: '200px', margin: '0 auto' }}>
            {isLoading ? (
              <div className="skeleton" style={{ width: '100%', height: '100%', borderRadius: '50%' }} />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    innerRadius={55}
                    outerRadius={85}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {pieData.map((_, index) => (
                      <Cell key={`slice-${index}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(15, 23, 42, 0.95)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '10px',
                      fontSize: '0.8rem',
                    }}
                    formatter={(val: any) => [`₹${Number(val).toLocaleString('en-IN')}`, 'Revenue']}
                  />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>

          {/* Quick Realization Summary Legend */}
          <div style={{ flex: 1, minWidth: '200px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {categories.slice(0, 5).map((cat, i) => (
              <div
                key={cat.category}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontSize: '0.82rem',
                  padding: '4px 8px',
                  borderRadius: '6px',
                  background: 'rgba(255, 255, 255, 0.02)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div
                    style={{
                      width: '10px',
                      height: '10px',
                      borderRadius: '3px',
                      background: CATEGORY_COLORS[i % CATEGORY_COLORS.length],
                    }}
                  />
                  <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{cat.category}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ color: 'var(--text-muted)' }}>{cat.revenue_share_pct}%</span>
                  <span className="badge badge-emerald" style={{ fontSize: '0.7rem', padding: '1px 6px' }}>
                    {cat.realization_rate_pct}% Real.
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
