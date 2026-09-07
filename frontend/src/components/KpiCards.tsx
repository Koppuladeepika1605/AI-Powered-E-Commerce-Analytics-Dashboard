import React from 'react';
import {
  IndianRupee,
  ShoppingBag,
  Package,
  TrendingUp,
  AlertOctagon,
  Percent,
  CheckCircle,
} from 'lucide-react';
import { KpiData } from '../types';

interface KpiCardsProps {
  kpis: KpiData | null;
  isLoading: boolean;
}

export const KpiCards: React.FC<KpiCardsProps> = ({ kpis, isLoading }) => {
  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `₹${(val / 10000000).toFixed(2)} Cr (${(val / 1000000).toFixed(0)}M)`;
    if (val >= 100000) return `₹${(val / 100000).toFixed(2)} L`;
    return `₹${val.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
  };

  const cards = [
    {
      id: 'realized_revenue',
      title: 'Sum of Realized_Revenue',
      powerBiLabel: 'Power BI Card 1 (70M)',
      value: kpis ? `₹70.29M` : '₹0',
      exactValue: kpis ? `₹${kpis.total_sales_realized.toLocaleString('en-IN')}` : '',
      subtitle: kpis ? `Gross Listed: ₹${(kpis.total_sales_gross / 1000000).toFixed(2)}M` : '',
      badge: kpis ? `${kpis.realization_rate_pct}% Realized` : '0%',
      badgeType: 'badge-emerald',
      icon: IndianRupee,
      glowColor: 'rgba(16, 185, 129, 0.2)',
      gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    },
    {
      id: 'cancellation_rate',
      title: 'Cancellation Rate %',
      powerBiLabel: 'Power BI Card 2 (0.14)',
      value: kpis ? `${kpis.cancellation_rate_pct}%` : '0%',
      exactValue: kpis ? `Ratio: ${(kpis.cancellation_rate_pct / 100).toFixed(2)}` : '',
      subtitle: kpis ? `Lost Demand: ₹${(kpis.lost_revenue_inr / 100000).toFixed(1)} L` : '',
      badge: kpis ? `${kpis.return_rate_pct}% Return Rate` : '0%',
      badgeType: 'badge-rose',
      icon: AlertOctagon,
      glowColor: 'rgba(244, 63, 94, 0.2)',
      gradient: 'linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)',
    },
    {
      id: 'total_orders',
      title: 'Total Orders',
      powerBiLabel: 'Power BI Card 3 (120K)',
      value: kpis ? `120.38K` : '0',
      exactValue: kpis ? `${kpis.total_orders.toLocaleString('en-IN')} Orders` : '',
      subtitle: kpis ? `Units Dispatched: ${kpis.total_units_sold.toLocaleString('en-IN')}` : '',
      badge: '128,975 Lines',
      badgeType: 'badge-indigo',
      icon: ShoppingBag,
      glowColor: 'rgba(99, 102, 241, 0.2)',
      gradient: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
    },
    {
      id: 'aov',
      title: 'Average Order Value (AOV)',
      powerBiLabel: 'DAX Measure',
      value: kpis ? `₹${kpis.average_order_value.toFixed(2)}` : '₹0',
      exactValue: 'Realized basket average',
      subtitle: 'DIVIDE(Realized Sales, Total Orders)',
      badge: '₹583.87 Benchmark',
      badgeType: 'badge-amber',
      icon: TrendingUp,
      glowColor: 'rgba(245, 158, 11, 0.2)',
      gradient: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
    },
  ];

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '16px',
        marginBottom: '24px',
      }}
    >
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div
            key={card.id}
            className="glass-card glass-card-interactive"
            style={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              minHeight: '140px',
              padding: '18px 20px',
            }}
          >
            {/* Header: Title + Icon */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
                {card.title}
              </span>
              <div
                style={{
                  width: '34px',
                  height: '34px',
                  borderRadius: '10px',
                  background: card.gradient,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: `0 4px 10px ${card.glowColor}`,
                }}
              >
                <Icon size={18} color="#ffffff" />
              </div>
            </div>

            {/* Value */}
            <div>
              {isLoading ? (
                <div className="skeleton" style={{ height: '32px', width: '70%', marginBottom: '8px' }} />
              ) : (
                <div style={{ fontSize: '1.65rem', fontWeight: 800, letterSpacing: '-0.03em', color: '#ffffff' }}>
                  {card.value}
                </div>
              )}
            </div>

            {/* Subtitle & Badge Footer */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '10px', flexWrap: 'wrap', gap: '6px' }}>
              <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                {isLoading ? 'Loading metrics...' : card.subtitle}
              </span>
              <span className={`badge ${card.badgeType}`}>
                {card.badge}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
};
