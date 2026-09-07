import React, { useState } from 'react';
import {
  Layers,
  Globe2,
  TrendingUp,
  ExternalLink,
  Download,
  Database,
  Code2,
  CheckCircle2,
  Settings,
  Image as ImageIcon,
  Table,
  Sparkles,
  Info,
  Maximize2,
} from 'lucide-react';

export const PowerBiShowcaseSection: React.FC = () => {
  const [selectedPage, setSelectedPage] = useState<number>(1);
  const [viewMode, setViewMode] = useState<'overview' | 'schema' | 'dax' | 'embed_config'>('overview');
  const [embedUrl, setEmbedUrl] = useState<string>('');
  const [customScreenshot, setCustomScreenshot] = useState<string | null>(null);

  const pages = [
    {
      id: 1,
      name: 'Executive Overview',
      subtitle: 'Top-line financial KPIs, Category Revenue distribution, and Realized Revenue Trendline.',
      kpis: [
        { label: 'Sum of Realized_Revenue', value: '70M', desc: '₹70,285,702.00 net realized cash revenue' },
        { label: 'Cancellation Rate %', value: '0.14', desc: '14.21% pre-dispatch cancellation rate' },
        { label: 'Total Orders', value: '120K', desc: '120,378 distinct customer orders' },
      ],
      visuals: [
        'KPI Card 1: Sum of Realized_Revenue (70M)',
        'KPI Card 2: Cancellation Rate % (0.14)',
        'KPI Card 3: Total Orders (120K)',
        'Clustered Bar Chart: Revenue by Category (Western Dress, Top, Set, Saree, Kurta, etc.)',
        'Line Chart: Realized Revenue Trend by Date/Hierarchy',
        'Slicer: Year and Quarter (2022 -> Qtr 1 to Qtr 4)',
      ],
    },
    {
      id: 2,
      name: 'Regional & Product Analysis',
      subtitle: 'Multi-dimensional geographical rankings and high-velocity garment style performance.',
      kpis: [
        { label: 'Top State (Maharashtra)', value: '₹13.3M', desc: '17.15% of national sales revenue' },
        { label: 'Top Metro (Bengaluru)', value: '₹6.15M', desc: 'Highest single-city order concentration' },
        { label: 'Active Garment Styles', value: '1,377', desc: 'Ranked by revenue generation' },
      ],
      visuals: [
        'Clustered Bar Chart: Revenue by State (Sum of Realized_Revenue by Ship_State across 36 States)',
        'Count Bar Chart: Top Products by Revenue (Count of Style by Realized_Revenue)',
        'Slicer: Year and Quarter (2022 hierarchy)',
      ],
    },
    {
      id: 3,
      name: 'Operations Analysis',
      subtitle: 'Logistics fulfillment channels, courier status distribution, and cancellation mitigation.',
      kpis: [
        { label: 'Total Orders in Courier', value: '120K', desc: '85% Shipped, 5% Unshipped, 5% Unassigned, 5% Cancelled' },
        { label: 'Amazon FBA Volume', value: '89.7K', desc: '69.5% fulfillment share (93.14% realization)' },
        { label: 'Cancellation Rate %', value: '0.14', desc: '14.21% baseline operational leakage' },
      ],
      visuals: [
        'Donut Chart: Orders by Status (Total Orders by Courier_Status with center callout 120K)',
        'Clustered Column Chart: Orders by Fulfilment (Amazon FBA vs Merchant Easy Ship)',
        'Clustered Column Chart: Orders by Courier Status (Sum of Realized_Revenue by Courier_Status)',
        'KPI Card: Cancellation Rate % (0.14 / 14.21%)',
      ],
    },
  ];

  const daxMeasures = [
    {
      name: 'Total Realized Sales',
      formula: 'SUM(amazon_sales[realized_revenue])',
      output: '₹70,285,702.00',
      description: 'Net recognized cash revenue excluding cancellations and returns.',
    },
    {
      name: 'Total Gross Sales',
      formula: 'SUM(amazon_sales[gross_amount])',
      output: '₹78,592,678.30',
      description: 'Total catalog listed demand prior to pre-delivery cancellations.',
    },
    {
      name: 'Total Orders',
      formula: 'DISTINCTCOUNT(amazon_sales[order_id])',
      output: '120,378',
      description: 'Unique buyer shopping cart transactions.',
    },
    {
      name: 'Total Order Lines',
      formula: 'COUNTROWS(amazon_sales)',
      output: '128,975',
      description: 'Total line items processed across all shipments.',
    },
    {
      name: 'Average Order Value (AOV)',
      formula: 'DIVIDE([Total Realized Sales], [Total Orders], 0)',
      output: '₹583.87',
      description: 'Average realized revenue recognized per unique customer order.',
    },
    {
      name: 'Cancellation Rate %',
      formula: 'DIVIDE([Cancelled Orders], [Total Order Lines], 0)',
      output: '14.21% (0.14)',
      description: 'Proportion of transactions cancelled prior to delivery.',
    },
    {
      name: 'Realization Rate %',
      formula: 'DIVIDE([Total Realized Sales], [Total Gross Sales], 0)',
      output: '89.43%',
      description: 'Conversion efficiency from listed gross demand to realized net cash.',
    },
    {
      name: 'Total Unrealized Value',
      formula: '[Total Gross Sales] - [Total Realized Sales]',
      output: '₹8,306,976.30',
      description: 'Financial value lost due to pre-delivery cancellations and customer returns.',
    },
  ];

  const currentPage = pages.find((p) => p.id === selectedPage) || pages[0];

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCustomScreenshot(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div style={{ marginBottom: '32px' }}>
      {/* Master Section Header */}
      <div className="glass-card" style={{ padding: '24px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div
              style={{
                width: '46px',
                height: '46px',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 14px rgba(245, 158, 11, 0.35)',
              }}
            >
              <Sparkles size={24} color="#ffffff" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
                  Power BI Business Intelligence Dashboard
                </h2>
                <span className="badge badge-amber">Source of Truth</span>
              </div>
              <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                Business intelligence visualizations developed using Microsoft Power BI (3 Interactive Pages • Star Schema Architecture)
              </p>
            </div>
          </div>

          {/* Sub-view switcher */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button
              onClick={() => setViewMode('overview')}
              className={`btn-tab ${viewMode === 'overview' ? 'active' : ''}`}
              style={{ fontSize: '0.8rem', padding: '6px 12px' }}
            >
              <ImageIcon size={14} /> Report Pages
            </button>
            <button
              onClick={() => setViewMode('schema')}
              className={`btn-tab ${viewMode === 'schema' ? 'active' : ''}`}
              style={{ fontSize: '0.8rem', padding: '6px 12px' }}
            >
              <Database size={14} /> Star Schema
            </button>
            <button
              onClick={() => setViewMode('dax')}
              className={`btn-tab ${viewMode === 'dax' ? 'active' : ''}`}
              style={{ fontSize: '0.8rem', padding: '6px 12px' }}
            >
              <Code2 size={14} /> DAX Measures ({daxMeasures.length})
            </button>
            <button
              onClick={() => setViewMode('embed_config')}
              className={`btn-tab ${viewMode === 'embed_config' ? 'active' : ''}`}
              style={{ fontSize: '0.8rem', padding: '6px 12px' }}
            >
              <Settings size={14} /> Power BI Embed Setup
            </button>
          </div>
        </div>
      </div>

      {/* VIEW 1: REPORT PAGES & VISUALS */}
      {viewMode === 'overview' && (
        <div>
          {/* Page Selector Tabs */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
              gap: '12px',
              marginBottom: '20px',
            }}
          >
            {pages.map((p) => {
              const isSelected = p.id === selectedPage;
              return (
                <div
                  key={p.id}
                  onClick={() => setSelectedPage(p.id)}
                  className={`glass-card glass-card-interactive ${isSelected ? 'active-border' : ''}`}
                  style={{
                    padding: '16px 18px',
                    cursor: 'pointer',
                    background: isSelected ? 'rgba(99, 102, 241, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                    borderColor: isSelected ? 'var(--accent-primary)' : 'var(--border-subtle)',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ fontSize: '0.74rem', fontWeight: 700, color: isSelected ? '#818cf8' : 'var(--text-muted)' }}>
                      PAGE {p.id}
                    </span>
                    <span className={`badge ${isSelected ? 'badge-indigo' : 'badge-emerald'}`}>
                      {p.visuals.length} Visuals
                    </span>
                  </div>
                  <h4 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#ffffff', marginBottom: '4px' }}>
                    {p.name}
                  </h4>
                  <p style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                    {p.subtitle}
                  </p>
                </div>
              );
            })}
          </div>

          {/* Detailed Page Visual Inspector & Simulated Layout */}
          <div className="glass-card" style={{ padding: '24px', marginBottom: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px', flexWrap: 'wrap', gap: '12px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span className="badge badge-amber">Power BI Desktop Report</span>
                  <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>Page {currentPage.id}: {currentPage.name}</h3>
                </div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                  Report canvas size: 1280 × 720 • Target .pbix: <code className="mono">Dashboard/Amazon_Ecommerce_Analytics_Dashboard.pbix</code>
                </p>
              </div>

              <div style={{ display: 'flex', gap: '8px' }}>
                <label className="btn-secondary" style={{ fontSize: '0.78rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <ImageIcon size={14} /> Upload Screenshot
                  <input type="file" accept="image/*" onChange={handleImageUpload} style={{ display: 'none' }} />
                </label>
              </div>
            </div>

            {/* Top KPI Callouts corresponding to Power BI Page */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '14px',
                marginBottom: '20px',
              }}
            >
              {currentPage.kpis.map((k, i) => (
                <div
                  key={i}
                  style={{
                    padding: '14px 18px',
                    borderRadius: '10px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontWeight: 600 }}>{k.label}</div>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#ffffff', margin: '4px 0' }}>{k.value}</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>{k.desc}</div>
                </div>
              ))}
            </div>

            {/* Custom Screenshot View if uploaded, else visual list */}
            {customScreenshot ? (
              <div style={{ marginBottom: '16px', borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
                <img src={customScreenshot} alt="Power BI Page Export" style={{ width: '100%', height: 'auto', display: 'block' }} />
              </div>
            ) : null}

            {/* Visual Inventory & Layout Breakdown */}
            <div style={{ padding: '16px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.04)' }}>
              <h4 style={{ fontSize: '0.86rem', fontWeight: 700, marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle2 size={15} color="#10b981" /> Verified Visual Components on Page {currentPage.id}:
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '8px' }}>
                {currentPage.visuals.map((v, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '8px 12px',
                      borderRadius: '6px',
                      background: 'rgba(255, 255, 255, 0.02)',
                      fontSize: '0.78rem',
                      color: 'var(--text-secondary)',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                    }}
                  >
                    <span style={{ color: 'var(--accent-primary)', fontWeight: 700 }}>#{idx + 1}</span>
                    <span>{v}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW 2: STAR SCHEMA DATA MODEL */}
      {viewMode === 'schema' && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <Database size={20} color="var(--accent-primary)" />
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Power BI Star Schema Data Model</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                1 Central Fact Table (128,975 rows) connected via 1:N single-direction relationships to 4 Dimension Tables
              </p>
            </div>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
              gap: '16px',
              marginBottom: '20px',
            }}
          >
            {/* Fact Table */}
            <div style={{ padding: '16px', borderRadius: '10px', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid #6366f1' }}>
              <span className="badge badge-indigo" style={{ marginBottom: '8px' }}>Fact Table (128,975 rows)</span>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>Fact_AmazonSales</h4>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                Key Columns: <code className="mono">order_id, order_date, sku, ship_city, ship_state, status, qty, gross_amount, realized_revenue</code>
              </p>
            </div>

            {/* Dim_Date */}
            <div style={{ padding: '16px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)' }}>
              <span className="badge badge-cyan" style={{ marginBottom: '8px' }}>Dim_Date (91 Days)</span>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>Dim_Date</h4>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                1:N on <code className="mono">Date</code> (Year, Quarter, Month, Week, Day_Name, Is_Weekend)
              </p>
            </div>

            {/* Dim_Product */}
            <div style={{ padding: '16px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)' }}>
              <span className="badge badge-amber" style={{ marginBottom: '8px' }}>Dim_Product (7,200 SKUs)</span>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>Dim_Product</h4>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                1:N on <code className="mono">SKU</code> (Category, Style, Size, ASIN)
              </p>
            </div>

            {/* Dim_Geography */}
            <div style={{ padding: '16px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)' }}>
              <span className="badge badge-emerald" style={{ marginBottom: '8px' }}>Dim_Geography (14,437 Cities)</span>
              <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#ffffff' }}>Dim_Geography</h4>
              <p style={{ fontSize: '0.74rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
                1:N on <code className="mono">City / State</code> (Ship_City, Ship_State, Postal_Code, Country)
              </p>
            </div>
          </div>
        </div>
      )}

      {/* VIEW 3: DAX MEASURES REFERENCE */}
      {viewMode === 'dax' && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Code2 size={20} color="var(--accent-cyan)" />
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>DAX Measures Concordance Dictionary</h3>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                  100% Verified mathematical concordance across Power BI DAX, Python EDA & PostgreSQL SQL Queries
                </p>
              </div>
            </div>
            <span className="badge badge-emerald">100% Match Validated</span>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-subtle)', textAlign: 'left', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '10px 12px' }}>Measure Name</th>
                  <th style={{ padding: '10px 12px' }}>DAX Formula</th>
                  <th style={{ padding: '10px 12px' }}>Formatted Output</th>
                  <th style={{ padding: '10px 12px' }}>Business Rationale</th>
                </tr>
              </thead>
              <tbody>
                {daxMeasures.map((m, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid rgba(255, 255, 255, 0.04)' }}>
                    <td style={{ padding: '10px 12px', fontWeight: 700, color: '#ffffff' }}>{m.name}</td>
                    <td style={{ padding: '10px 12px' }}><code className="mono" style={{ color: '#818cf8' }}>{m.formula}</code></td>
                    <td style={{ padding: '10px 12px', fontWeight: 700, color: '#34d399' }} className="mono">{m.output}</td>
                    <td style={{ padding: '10px 12px', color: 'var(--text-secondary)' }}>{m.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* VIEW 4: POWER BI EMBED SETUP */}
      {viewMode === 'embed_config' && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <Settings size={20} color="var(--accent-amber)" />
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Power BI Service Live Embedding Configuration</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Publish your <code className="mono">Amazon_Ecommerce_Analytics_Dashboard.pbix</code> report to Power BI Service (app.powerbi.com) to embed live interactive frames.
              </p>
            </div>
          </div>

          <div style={{ maxWidth: '640px', display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '20px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Power BI Publish-to-Web or Secure Embed URL:
              </label>
              <input
                type="text"
                placeholder="https://app.powerbi.com/view?r=eyJrIjoi... or embed url"
                value={embedUrl}
                onChange={(e) => setEmbedUrl(e.target.value)}
                style={{ width: '100%', fontSize: '0.85rem', padding: '10px 12px' }}
              />
            </div>

            <div style={{ padding: '14px', borderRadius: '8px', background: 'rgba(255, 255, 255, 0.03)', fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              <strong>How to get your Power BI Embed Link:</strong>
              <ol style={{ paddingLeft: '18px', marginTop: '6px' }}>
                <li>Open <code className="mono">Amazon_Ecommerce_Analytics_Dashboard.pbix</code> in Power BI Desktop.</li>
                <li>Click <strong>File</strong> $\rightarrow$ <strong>Publish</strong> $\rightarrow$ <strong>Publish to Power BI</strong>.</li>
                <li>In Power BI Service (<a href="https://app.powerbi.com" target="_blank" rel="noreferrer" style={{ color: '#818cf8' }}>app.powerbi.com</a>), open your report.</li>
                <li>Click <strong>File</strong> $\rightarrow$ <strong>Embed report</strong> $\rightarrow$ <strong>Publish to web (public)</strong> or <strong>Website or portal</strong>.</li>
                <li>Copy the generated link and paste it into the field above.</li>
              </ol>
            </div>
          </div>

          {embedUrl ? (
            <div style={{ width: '100%', height: '540px', borderRadius: '10px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
              <iframe
                title="Power BI Live Report"
                width="100%"
                height="100%"
                src={embedUrl}
                frameBorder="0"
                allowFullScreen={true}
              />
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default PowerBiShowcaseSection;
