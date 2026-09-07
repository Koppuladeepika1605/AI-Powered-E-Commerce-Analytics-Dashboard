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
import { Truck, CheckCircle2, AlertTriangle, ShieldCheck, ShoppingBag, PieChart as PieIcon, BarChart3, AlertOctagon } from 'lucide-react';
import { CourierStatusItem, OrderStatusItem, FulfilmentItem, SalesChannelItem } from '../types';

interface OperationsSectionProps {
  courierStatuses: CourierStatusItem[];
  orderStatuses: OrderStatusItem[];
  fulfilments: FulfilmentItem[];
  salesChannels: SalesChannelItem[];
  cancellationRate?: number;
  isLoading: boolean;
}

const COURIER_COLORS: Record<string, string> = {
  Shipped: '#06b6d4',
  Unassigned: '#6366f1',
  Unshipped: '#f59e0b',
  Cancelled: '#f43f5e',
};

const DEFAULT_COLORS = ['#06b6d4', '#6366f1', '#f59e0b', '#f43f5e', '#10b981'];

export const OperationsSection: React.FC<OperationsSectionProps> = ({
  courierStatuses,
  orderStatuses,
  fulfilments,
  salesChannels,
  cancellationRate = 14.21,
  isLoading,
}) => {
  const formatCurrency = (val: number) => {
    if (val >= 10000000) return `₹${(val / 10000000).toFixed(2)} Cr`;
    if (val >= 1000000) return `₹${(val / 1000000).toFixed(1)}M`;
    if (val >= 100000) return `₹${(val / 100000).toFixed(1)} L`;
    if (val >= 1000) return `₹${(val / 1000).toFixed(0)}k`;
    return `₹${val}`;
  };

  // 1. Donut Data: Orders by Courier Status
  const donutData = (courierStatuses.length > 0 ? courierStatuses : [
    { courier_status: 'Shipped', order_count: 109487, share_pct: 84.89, total_quantity: 109896, realized_revenue: 69670972 },
    { courier_status: 'Unassigned', order_count: 6872, share_pct: 5.33, total_quantity: 0, realized_revenue: 0 },
    { courier_status: 'Unshipped', order_count: 6681, share_pct: 5.18, total_quantity: 6753, realized_revenue: 614730 },
    { courier_status: 'Cancelled', order_count: 5935, share_pct: 4.60, total_quantity: 0, realized_revenue: 0 },
  ]).map((item) => ({
    name: item.courier_status,
    value: item.order_count,
    share: item.share_pct,
    rev: item.realized_revenue,
  }));

  // 2. Column Data: Orders by Fulfilment
  const fulfilmentChartData = (fulfilments.length > 0 ? fulfilments : [
    { fulfilment: 'Amazon', order_lines: 89683, volume_share_pct: 69.5, realized_revenue: 65463870, realization_rate_pct: 93.14 },
    { fulfilment: 'Merchant', order_lines: 39292, volume_share_pct: 30.5, realized_revenue: 4821832, realization_rate_pct: 81.14 },
  ]).map((f) => ({
    name: f.fulfilment,
    orders: f.order_lines,
    revenue: f.realized_revenue,
    realization: f.realization_rate_pct,
  }));

  // 3. Column Data: Orders by Courier Status (Revenue)
  const courierRevenueData = (courierStatuses.length > 0 ? courierStatuses : [
    { courier_status: 'Shipped', realized_revenue: 69670972 },
    { courier_status: 'Unshipped', realized_revenue: 614730 },
    { courier_status: 'Cancelled', realized_revenue: 0 },
    { courier_status: 'Unassigned', realized_revenue: 0 },
  ]).map((item) => ({
    courier_status: item.courier_status,
    realized_revenue: item.realized_revenue,
  }));

  return (
    <div>
      {/* Top 2 Power BI Visuals Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
          gap: '20px',
          marginBottom: '20px',
        }}
      >
        {/* Visual 1: Orders by Status (Donut Chart) */}
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <PieIcon size={16} color="var(--accent-cyan)" />
              <div>
                <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Orders by Status</h3>
                <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Total Orders by Courier_Status</p>
              </div>
            </div>
            <span className="badge badge-cyan">Power BI Donut Visual</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
            <div style={{ width: '220px', height: '220px', margin: '0 auto', position: 'relative' }}>
              {isLoading ? (
                <div className="skeleton" style={{ width: '100%', height: '100%', borderRadius: '50%' }} />
              ) : (
                <>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={donutData}
                        innerRadius={65}
                        outerRadius={95}
                        paddingAngle={3}
                        dataKey="value"
                      >
                        {donutData.map((entry) => (
                          <Cell
                            key={`cell-${entry.name}`}
                            fill={COURIER_COLORS[entry.name] || '#6366f1'}
                          />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'rgba(15, 23, 42, 0.95)',
                          border: '1px solid var(--border-subtle)',
                          borderRadius: '10px',
                          fontSize: '0.8rem',
                        }}
                        formatter={(val: any, name: any) => [
                          `${Number(val).toLocaleString('en-IN')} Orders (${((Number(val) / 128975) * 100).toFixed(1)}%)`,
                          name,
                        ]}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                  {/* Center Total Callout matching Power BI (120K) */}
                  <div
                    style={{
                      position: 'absolute',
                      top: '50%',
                      left: '50%',
                      transform: 'translate(-50%, -50%)',
                      textAlign: 'center',
                      pointerEvents: 'none',
                    }}
                  >
                    <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#ffffff' }}>120K</div>
                    <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Orders</div>
                  </div>
                </>
              )}
            </div>

            {/* Courier Status Breakdown Table */}
            <div style={{ flex: 1, minWidth: '200px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {donutData.map((st) => (
                <div
                  key={st.name}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontSize: '0.82rem',
                    padding: '6px 10px',
                    borderRadius: '8px',
                    background: 'rgba(255, 255, 255, 0.02)',
                    border: '1px solid rgba(255, 255, 255, 0.04)',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div
                      style={{
                        width: '10px',
                        height: '10px',
                        borderRadius: '3px',
                        background: COURIER_COLORS[st.name] || '#6366f1',
                      }}
                    />
                    <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{st.name}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span className="mono" style={{ color: 'var(--text-secondary)' }}>
                      {st.value.toLocaleString('en-IN')}
                    </span>
                    <span className="badge badge-indigo" style={{ fontSize: '0.68rem', padding: '1px 6px' }}>
                      {st.share}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Visual 2: Orders by Fulfilment (Clustered Column Chart) */}
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <BarChart3 size={16} color="var(--accent-primary)" />
              <div>
                <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Orders by Fulfilment</h3>
                <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Total Orders by Fulfilment (Amazon vs Merchant)</p>
              </div>
            </div>
            <span className="badge badge-indigo">Power BI Column Visual</span>
          </div>

          <div style={{ width: '100%', height: '240px' }}>
            {isLoading ? (
              <div className="skeleton" style={{ width: '100%', height: '100%' }} />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={fulfilmentChartData}
                  margin={{ top: 10, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" vertical={false} />
                  <XAxis dataKey="name" stroke="var(--text-secondary)" fontSize={12} tickLine={false} />
                  <YAxis
                    stroke="var(--text-muted)"
                    fontSize={11}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(v) => `${(v / 1000).toFixed(0)}K`}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(15, 23, 42, 0.95)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '10px',
                      fontSize: '0.82rem',
                    }}
                    formatter={(val: any) => [`${Number(val).toLocaleString('en-IN')} Orders`, 'Total Orders']}
                  />
                  <Bar dataKey="orders" name="Total Orders" fill="#0284c7" radius={[6, 6, 0, 0]}>
                    <Cell fill="#0284c7" />
                    <Cell fill="#38bdf8" />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>

      {/* Bottom 2 Power BI Visuals Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))',
          gap: '20px',
          marginBottom: '24px',
        }}
      >
        {/* Visual 3: Orders by Courier Status (Revenue Column Chart) */}
        <div className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Truck size={16} color="var(--accent-emerald)" />
              <div>
                <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Orders by Courier Status</h3>
                <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Sum of Realized_Revenue by Courier_Status</p>
              </div>
            </div>
            <span className="badge badge-emerald">Power BI Column Visual</span>
          </div>

          <div style={{ width: '100%', height: '240px' }}>
            {isLoading ? (
              <div className="skeleton" style={{ width: '100%', height: '100%' }} />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={courierRevenueData}
                  margin={{ top: 10, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" vertical={false} />
                  <XAxis dataKey="courier_status" stroke="var(--text-secondary)" fontSize={12} tickLine={false} />
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
                      fontSize: '0.82rem',
                    }}
                    formatter={(val: any) => [`₹${Number(val).toLocaleString('en-IN')}`, 'Realized Revenue']}
                  />
                  <Bar dataKey="realized_revenue" name="Realized Revenue" fill="#0284c7" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Visual 4: Cancellation Rate % KPI & Fulfilment Channel Realization */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <AlertOctagon size={16} color="var(--accent-rose)" />
                <div>
                  <h3 style={{ fontSize: '0.98rem', fontWeight: 700 }}>Cancellation Rate %</h3>
                  <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Power BI Card Visual (0.14)</p>
                </div>
              </div>
              <span className="badge badge-rose">14.21% Metric</span>
            </div>

            <div style={{ padding: '16px', borderRadius: '12px', background: 'rgba(244, 63, 94, 0.08)', border: '1px solid rgba(244, 63, 94, 0.2)', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px' }}>
                <span style={{ fontSize: '2.2rem', fontWeight: 800, color: '#fb7185' }}>0.14</span>
                <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>(14.21% cancelled transactions)</span>
              </div>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                Formula: <code className="mono">DIVIDE([Cancelled Orders], [Total Order Lines], 0)</code>
              </p>
            </div>
          </div>

          {/* Fulfillment Comparison Card */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div style={{ padding: '12px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '4px' }}>Amazon FBA Channel</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#34d399' }}>93.14% Realized</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: '2px' }}>12.79% Cancellation Rate</div>
            </div>

            <div style={{ padding: '12px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.03)', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '4px' }}>Merchant Easy Ship</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fbbf24' }}>81.14% Realized</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: '2px' }}>17.47% Cancellation Rate</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OperationsSection;
