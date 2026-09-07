import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from 'recharts';
import { Globe2, Building2, MapPin } from 'lucide-react';
import { GeographyData } from '../types';

interface GeographySectionProps {
  geoData: GeographyData | null;
  isLoading: boolean;
}

export const GeographySection: React.FC<GeographySectionProps> = ({ geoData, isLoading }) => {
  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `₹${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 100000) return `₹${(val / 100000).toFixed(1)} L`;
    return `₹${val.toLocaleString('en-IN')}`;
  };

  const topStates = geoData?.top_states.slice(0, 10) || [];
  const topCities = geoData?.top_cities.slice(0, 8) || [];

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
        gap: '20px',
        marginBottom: '24px',
      }}
    >
      {/* 1. Top States Leaderboard */}
      <div className="glass-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Globe2 size={16} color="var(--accent-cyan)" />
            <div>
              <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Revenue by State</h3>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Sum of Realized_Revenue by Ship_State</p>
            </div>
          </div>
          <span className="badge badge-cyan">Power BI State Visual</span>
        </div>

        <div style={{ width: '100%', height: '300px' }}>
          {isLoading ? (
            <div className="skeleton" style={{ width: '100%', height: '100%' }} />
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={topStates}
                layout="vertical"
                margin={{ top: 5, right: 20, left: 55, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" horizontal={false} />
                <XAxis type="number" stroke="var(--text-muted)" fontSize={11} tickFormatter={formatCurrency} />
                <YAxis dataKey="state" type="category" stroke="var(--text-secondary)" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '10px',
                    fontSize: '0.82rem',
                  }}
                  formatter={(val: any) => [`₹${Number(val).toLocaleString('en-IN')}`, 'Realized Revenue']}
                />
                <Bar dataKey="realized_revenue" fill="#06b6d4" radius={[0, 6, 6, 0]}>
                  {topStates.map((_, idx) => (
                    <Cell
                      key={`state-${idx}`}
                      fill={idx === 0 ? '#38bdf8' : idx === 1 ? '#0ea5e9' : idx === 2 ? '#0284c7' : '#0369a1'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* 2. Top Metro Cities Grid */}
      <div className="glass-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Building2 size={16} color="var(--accent-primary)" />
            <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Top Metro Cities by Demand</h3>
          </div>
          <span className="badge badge-indigo">Metro Demand</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {isLoading ? (
            Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="skeleton" style={{ height: '36px', width: '100%' }} />
            ))
          ) : topCities.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>No city data available.</p>
          ) : (
            topCities.map((city, idx) => (
              <div
                key={city.city + idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid rgba(255, 255, 255, 0.04)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div
                    style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '6px',
                      background: 'rgba(99, 102, 241, 0.15)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '0.72rem',
                      fontWeight: 700,
                      color: '#818cf8',
                    }}
                  >
                    {idx + 1}
                  </div>
                  <div>
                    <span style={{ fontWeight: 600, fontSize: '0.86rem', color: 'var(--text-primary)' }}>{city.city}</span>
                    <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginLeft: '6px' }}>
                      ({city.state})
                    </span>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontSize: '0.76rem', color: 'var(--text-secondary)' }}>
                    {city.total_orders.toLocaleString('en-IN')} Orders
                  </span>
                  <span style={{ fontWeight: 700, color: '#34d399', fontSize: '0.86rem' }}>
                    ₹{city.realized_revenue.toLocaleString('en-IN')}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
