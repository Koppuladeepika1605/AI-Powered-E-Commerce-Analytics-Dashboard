import React, { useState } from 'react';
import { Package, Award, Sparkles, TrendingUp, Search } from 'lucide-react';
import { TopProductsData, TopProductItem } from '../types';

interface TopProductsSectionProps {
  productsData: TopProductsData | null;
  isLoading: boolean;
}

export const TopProductsSection: React.FC<TopProductsSectionProps> = ({ productsData, isLoading }) => {
  const [viewMode, setViewMode] = useState<'styles' | 'skus'>('styles');
  const [searchQuery, setSearchQuery] = useState('');

  const items: TopProductItem[] =
    viewMode === 'styles' ? productsData?.top_styles || [] : productsData?.top_skus || [];

  const filteredItems = items.filter((item) => {
    const key = (item.style || item.sku || '').toLowerCase();
    const cat = item.category.toLowerCase();
    const q = searchQuery.toLowerCase();
    return key.includes(q) || cat.includes(q);
  });

  return (
    <div className="glass-card" style={{ marginBottom: '24px' }}>
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '14px',
          marginBottom: '16px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'rgba(245, 158, 11, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Award size={18} color="var(--accent-amber)" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Top Products by Revenue</h3>
              <span className="badge badge-amber">Power BI Product Visual</span>
            </div>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
              Count of Style & SKUs by Realized_Revenue and Order Velocity
            </p>
          </div>
        </div>

        {/* Mode Switch & Search */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <div style={{ position: 'relative' }}>
            <Search size={14} style={{ position: 'absolute', left: '10px', top: '9px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search style / SKU..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ paddingLeft: '30px', width: '180px' }}
            />
          </div>

          <div style={{ display: 'inline-flex', background: 'rgba(255, 255, 255, 0.04)', borderRadius: '8px', padding: '3px' }}>
            <button
              onClick={() => setViewMode('styles')}
              style={{
                padding: '5px 12px',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: '6px',
                background: viewMode === 'styles' ? 'var(--accent-primary)' : 'transparent',
                color: viewMode === 'styles' ? '#ffffff' : 'var(--text-muted)',
              }}
            >
              Top Styles (Revenue)
            </button>
            <button
              onClick={() => setViewMode('skus')}
              style={{
                padding: '5px 12px',
                fontSize: '0.78rem',
                fontWeight: 600,
                borderRadius: '6px',
                background: viewMode === 'skus' ? 'var(--accent-primary)' : 'transparent',
                color: viewMode === 'skus' ? '#ffffff' : 'var(--text-muted)',
              }}
            >
              Top SKUs (Volume)
            </button>
          </div>
        </div>
      </div>

      {/* Table Content */}
      <div style={{ overflowX: 'auto' }}>
        <table className="custom-table">
          <thead>
            <tr>
              <th style={{ width: '60px' }}>Rank</th>
              <th>{viewMode === 'styles' ? 'Garment Style' : 'Product SKU'}</th>
              <th>Category</th>
              <th style={{ textAlign: 'right' }}>Total Orders</th>
              <th style={{ textAlign: 'right' }}>Units Sold</th>
              <th style={{ textAlign: 'right' }}>Realized Revenue</th>
              <th style={{ textAlign: 'right' }}>Realization Rate</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <tr key={i}>
                  <td colSpan={7}>
                    <div className="skeleton" style={{ height: '28px', width: '100%' }} />
                  </td>
                </tr>
              ))
            ) : filteredItems.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
                  No matching products found.
                </td>
              </tr>
            ) : (
              filteredItems.map((p, idx) => (
                <tr key={p.style || p.sku || idx}>
                  <td>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '24px',
                        height: '24px',
                        borderRadius: '6px',
                        fontWeight: 700,
                        fontSize: '0.75rem',
                        background:
                          idx === 0
                            ? 'rgba(245, 158, 11, 0.2)'
                            : idx === 1
                            ? 'rgba(148, 163, 184, 0.2)'
                            : idx === 2
                            ? 'rgba(217, 119, 6, 0.2)'
                            : 'rgba(255, 255, 255, 0.04)',
                        color:
                          idx === 0
                            ? '#fbbf24'
                            : idx === 1
                            ? '#cbd5e1'
                            : idx === 2
                            ? '#f59e0b'
                            : 'var(--text-muted)',
                      }}
                    >
                      #{idx + 1}
                    </span>
                  </td>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }} className="mono">
                    {p.style || p.sku}
                  </td>
                  <td>
                    <span className="badge badge-indigo">{p.category}</span>
                  </td>
                  <td style={{ textAlign: 'right' }} className="mono">
                    {p.total_orders.toLocaleString('en-IN')}
                  </td>
                  <td style={{ textAlign: 'right' }} className="mono">
                    {p.total_quantity.toLocaleString('en-IN')}
                  </td>
                  <td style={{ textAlign: 'right', fontWeight: 700, color: '#34d399' }} className="mono">
                    ₹{p.realized_revenue.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <span className="badge badge-emerald">{p.realization_rate_pct}%</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
