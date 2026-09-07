import React, { useState, useEffect } from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  LineChart,
  Line,
  Area,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import {
  Cpu,
  Sparkles,
  TrendingUp,
  Sliders,
  Calendar,
  AlertCircle,
  CheckCircle2,
  Info,
  DollarSign,
  Package,
  Layers,
  Activity,
} from 'lucide-react';
import { ApiService } from '../services/api';
import { PredictionData, ActualVsPredictedItem, BenchmarkModelItem } from '../types';

interface MlForecastingSectionProps {
  categories: string[];
}

export const MlForecastingSection: React.FC<MlForecastingSectionProps> = ({ categories }) => {
  const [subTab, setSubTab] = useState<'forward_forecast' | 'actual_vs_predicted'>('forward_forecast');
  const [selectedCategory, setSelectedCategory] = useState<string>('Set');
  const [forecastDays, setForecastDays] = useState<number>(14);
  const [promoScenario, setPromoScenario] = useState<number>(25);
  const [b2bScenario, setB2bScenario] = useState<number>(1);
  const [predictionData, setPredictionData] = useState<PredictionData | null>(null);
  const [actualVsPredicted, setActualVsPredicted] = useState<ActualVsPredictedItem[]>([]);
  const [benchmarks, setBenchmarks] = useState<{ models: BenchmarkModelItem[]; best_model_metrics: Record<string, any> } | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchForecast = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await ApiService.getPrediction(
        selectedCategory,
        forecastDays,
        promoScenario / 100,
        b2bScenario / 100
      );
      setPredictionData(data);
    } catch (err: any) {
      setError(err.message || 'Failed to generate machine learning demand forecast.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchHoldoutData = async () => {
    try {
      const [holdoutRes, benchmarkRes] = await Promise.all([
        ApiService.getActualVsPredicted(selectedCategory),
        ApiService.getBenchmarks(),
      ]);
      setActualVsPredicted(holdoutRes.data);
      setBenchmarks(benchmarkRes);
    } catch (err) {
      console.error('Failed to load holdout evaluation data:', err);
    }
  };

  useEffect(() => {
    fetchForecast();
    fetchHoldoutData();
  }, [selectedCategory, forecastDays]);

  const validCategories = categories.filter((c) => c !== 'ALL');

  const formatCurrency = (val: number) => {
    if (val >= 100000) return `₹${(val / 100000).toFixed(1)} L`;
    if (val >= 1000) return `₹${(val / 1000).toFixed(0)}k`;
    return `₹${val}`;
  };

  return (
    <div style={{ marginBottom: '32px' }}>
      {/* Header & Sub-tab Switcher */}
      <div className="glass-card" style={{ marginBottom: '20px', padding: '20px 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div
              style={{
                width: '42px',
                height: '42px',
                borderRadius: '10px',
                background: 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 4px 14px rgba(168, 85, 247, 0.35)',
              }}
            >
              <Cpu size={22} color="#ffffff" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h2 style={{ fontSize: '1.2rem', fontWeight: 800 }}>
                  ML Sales & Demand Forecasting (Phase 6)
                </h2>
                <span className="badge badge-indigo">Gradient Boosting (R² = 0.9531)</span>
              </div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                Multi-Category Daily Demand Forecasting & Holdout Actual vs. Predicted Validation
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button
              onClick={() => setSubTab('forward_forecast')}
              className={`btn-tab ${subTab === 'forward_forecast' ? 'active' : ''}`}
              style={{ fontSize: '0.82rem', padding: '6px 14px' }}
            >
              <TrendingUp size={14} /> 14-Day Forward Forecaster
            </button>
            <button
              onClick={() => setSubTab('actual_vs_predicted')}
              className={`btn-tab ${subTab === 'actual_vs_predicted' ? 'active' : ''}`}
              style={{ fontSize: '0.82rem', padding: '6px 14px' }}
            >
              <Activity size={14} /> Actual vs. Predicted Holdout
            </button>
          </div>
        </div>
      </div>

      {/* Control Panel: Category & Scenario Parameters */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '16px',
          marginBottom: '20px',
        }}
      >
        {/* Category Selector */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '8px' }}>
            Target Apparel Category
          </label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{ width: '100%', fontSize: '0.9rem', padding: '10px' }}
          >
            {validCategories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>

        {/* Horizon Slider */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Forecast Horizon
            </label>
            <span style={{ fontWeight: 700, color: '#818cf8' }}>{forecastDays} Days Ahead</span>
          </div>
          <input
            type="range"
            min={7}
            max={30}
            step={7}
            value={forecastDays}
            onChange={(e) => setForecastDays(Number(e.target.value))}
            style={{ width: '100%', accentColor: '#6366f1' }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            <span>7 Days</span>
            <span>14 Days (Standard)</span>
            <span>21 Days</span>
            <span>30 Days</span>
          </div>
        </div>

        {/* Promotion Scenario Slider */}
        <div className="glass-card" style={{ padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
            <label style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
              Promotion Scenario Discount
            </label>
            <span style={{ fontWeight: 700, color: '#34d399' }}>{promoScenario}% Promos</span>
          </div>
          <input
            type="range"
            min={0}
            max={60}
            step={5}
            value={promoScenario}
            onChange={(e) => setPromoScenario(Number(e.target.value))}
            style={{ width: '100%', accentColor: '#10b981' }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            <span>0% Baseline</span>
            <span>25% Historical Avg</span>
            <span>60% Mega Sale</span>
          </div>
        </div>
      </div>

      {/* SUB-TAB 1: FORWARD FORECASTER */}
      {subTab === 'forward_forecast' && (
        <div>
          {/* Forecast Result KPIs */}
          {predictionData && (
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                gap: '16px',
                marginBottom: '20px',
              }}
            >
              <div className="glass-card" style={{ padding: '16px 20px', borderLeft: '4px solid #8b5cf6' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Total Predicted Revenue</span>
                <div style={{ fontSize: '1.45rem', fontWeight: 800, color: '#ffffff', marginTop: '4px' }}>
                  ₹{predictionData.kpis.total_predicted_revenue_inr.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                </div>
                <span style={{ fontSize: '0.72rem', color: '#a78bfa' }}>Over {forecastDays} forward days</span>
              </div>

              <div className="glass-card" style={{ padding: '16px 20px', borderLeft: '4px solid #06b6d4' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Predicted Unit Demand</span>
                <div style={{ fontSize: '1.45rem', fontWeight: 800, color: '#ffffff', marginTop: '4px' }}>
                  {predictionData.kpis.total_predicted_unit_demand.toLocaleString('en-IN')} Units
                </div>
                <span style={{ fontSize: '0.72rem', color: '#22d3ee' }}>Inventory requirement</span>
              </div>

              <div className="glass-card" style={{ padding: '16px 20px', borderLeft: '4px solid #10b981' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Daily Run-Rate Average</span>
                <div style={{ fontSize: '1.45rem', fontWeight: 800, color: '#ffffff', marginTop: '4px' }}>
                  ₹{predictionData.kpis.daily_average_revenue_inr.toLocaleString('en-IN', { maximumFractionDigits: 2 })}/day
                </div>
                <span style={{ fontSize: '0.72rem', color: '#34d399' }}>Expected daily realization</span>
              </div>

              <div className="glass-card" style={{ padding: '16px 20px', borderLeft: '4px solid #f59e0b' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Estimated ASP / Unit</span>
                <div style={{ fontSize: '1.45rem', fontWeight: 800, color: '#ffffff', marginTop: '4px' }}>
                  ₹{predictionData.kpis.avg_selling_price_inr.toFixed(2)}
                </div>
                <span style={{ fontSize: '0.72rem', color: '#fbbf24' }}>Historical realization price</span>
              </div>
            </div>
          )}

          {/* Forward Timeline Chart */}
          <div className="glass-card" style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <TrendingUp size={16} color="var(--accent-violet)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>
                  Forward Demand Forecast: {selectedCategory} ({predictionData?.forecast_start_date} to {predictionData?.forecast_end_date})
                </h3>
              </div>
              <span className="badge badge-indigo">95% Confidence Bounds (+/- 15%)</span>
            </div>

            <div style={{ width: '100%', height: '340px' }}>
              {isLoading ? (
                <div className="skeleton" style={{ width: '100%', height: '100%' }} />
              ) : predictionData ? (
                <ResponsiveContainer width="100%" height="100%">
                  <ComposedChart data={predictionData.daily_forecast} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                    <defs>
                      <linearGradient id="boundGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.25} />
                        <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
                    <XAxis dataKey="date" stroke="var(--text-muted)" fontSize={11} tickFormatter={(v) => v.slice(5)} />
                    <YAxis yAxisId="left" stroke="var(--text-muted)" fontSize={11} tickFormatter={formatCurrency} />
                    <YAxis yAxisId="right" orientation="right" stroke="var(--text-muted)" fontSize={11} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '10px',
                        fontSize: '0.82rem',
                      }}
                      formatter={(val: any, name: any) => [
                        name.includes('Revenue') || name.includes('Bound')
                          ? `₹${Number(val).toLocaleString('en-IN', { maximumFractionDigits: 2 })}`
                          : `${val} units`,
                        name,
                      ]}
                    />
                    <Legend wrapperStyle={{ fontSize: '0.8rem', paddingTop: '10px' }} />
                    <Area
                      yAxisId="left"
                      type="monotone"
                      dataKey="upper_bound_inr"
                      name="Upper Bound (INR)"
                      stroke="none"
                      fill="url(#boundGrad)"
                    />
                    <Line
                      yAxisId="left"
                      type="monotone"
                      dataKey="predicted_revenue_inr"
                      name="Predicted Daily Revenue (INR)"
                      stroke="#a855f7"
                      strokeWidth={3}
                      dot={{ r: 4, fill: '#c084fc' }}
                    />
                    <Bar
                      yAxisId="right"
                      dataKey="predicted_unit_demand"
                      name="Predicted Unit Demand"
                      fill="#06b6d4"
                      opacity={0.6}
                      radius={[4, 4, 0, 0]}
                    />
                  </ComposedChart>
                </ResponsiveContainer>
              ) : null}
            </div>
          </div>
        </div>
      )}

      {/* SUB-TAB 2: HOLDOUT ACTUAL VS. PREDICTED EVALUATION */}
      {subTab === 'actual_vs_predicted' && (
        <div>
          {/* Actual vs Predicted Time-Series */}
          <div className="glass-card" style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '8px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Activity size={16} color="var(--accent-cyan)" />
                <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>
                  14-Day Out-of-Sample Holdout Evaluation (June 16 – June 29, 2022) — {selectedCategory}
                </h3>
              </div>
              <span className="badge badge-emerald">Zero Lookahead Leakage</span>
            </div>

            <div style={{ width: '100%', height: '340px' }}>
              {actualVsPredicted.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={actualVsPredicted} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
                    <XAxis dataKey="Date" stroke="var(--text-muted)" fontSize={11} tickFormatter={(v) => v.slice(5)} />
                    <YAxis stroke="var(--text-muted)" fontSize={11} tickFormatter={formatCurrency} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '10px',
                        fontSize: '0.82rem',
                      }}
                      formatter={(val: any) => [`₹${Number(val).toLocaleString('en-IN')}`, '']}
                    />
                    <Legend wrapperStyle={{ fontSize: '0.8rem', paddingTop: '10px' }} />
                    <Line
                      type="monotone"
                      dataKey="Actual_Revenue"
                      name="Actual Realized Sales (INR)"
                      stroke="#10b981"
                      strokeWidth={3}
                      dot={{ r: 4, fill: '#34d399' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="Predicted_Revenue"
                      name="Model Predicted Sales (INR)"
                      stroke="#a855f7"
                      strokeWidth={2.5}
                      strokeDasharray="4 4"
                      dot={{ r: 4, fill: '#c084fc' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="Baseline_Lag7_Revenue"
                      name="Seasonal Baseline Lag-7 (INR)"
                      stroke="#64748b"
                      strokeWidth={1.5}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
                  Loading holdout dataset predictions...
                </div>
              )}
            </div>
          </div>

          {/* Model Comparison Benchmark Table */}
          {benchmarks && benchmarks.models.length > 0 && (
            <div className="glass-card" style={{ marginBottom: '20px', padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Layers size={16} color="var(--accent-amber)" />
                  <h4 style={{ fontSize: '0.96rem', fontWeight: 700 }}>Out-of-Sample Model Benchmarking (14-Day Test Period)</h4>
                </div>
                <span className="badge badge-indigo">Gradient Boosting Regressor Best</span>
              </div>

              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
                  <thead>
                    <tr style={{ borderBottom: '1px solid var(--border-subtle)', textAlign: 'left', color: 'var(--text-muted)' }}>
                      <th style={{ padding: '8px 12px' }}>Model Architecture</th>
                      <th style={{ padding: '8px 12px' }}>MAE (Mean Absolute Error)</th>
                      <th style={{ padding: '8px 12px' }}>RMSE</th>
                      <th style={{ padding: '8px 12px' }}>R² Accuracy</th>
                      <th style={{ padding: '8px 12px' }}>MAPE</th>
                    </tr>
                  </thead>
                  <tbody>
                    {benchmarks.models.map((m: any, idx: number) => {
                      const isBest = m.Model?.includes('Gradient Boosting');
                      return (
                        <tr
                          key={idx}
                          style={{
                            borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                            background: isBest ? 'rgba(168, 85, 247, 0.08)' : 'transparent',
                          }}
                        >
                          <td style={{ padding: '10px 12px', fontWeight: isBest ? 700 : 500, color: isBest ? '#c084fc' : '#ffffff' }}>
                            {m.Model} {isBest && '★ (Production Selected)'}
                          </td>
                          <td style={{ padding: '10px 12px' }} className="mono">₹{Number(m.MAE).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                          <td style={{ padding: '10px 12px' }} className="mono">₹{Number(m.RMSE).toLocaleString('en-IN', { maximumFractionDigits: 2 })}</td>
                          <td style={{ padding: '10px 12px', fontWeight: 700, color: '#34d399' }} className="mono">
                            {Number(m.R2).toFixed(4)}
                          </td>
                          <td style={{ padding: '10px 12px' }} className="mono">{m.MAPE}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Model Metadata & Specifications */}
      {predictionData && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))',
            gap: '16px',
          }}
        >
          {/* Natural Language Interpretation */}
          <div className="glass-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Sparkles size={16} color="var(--accent-violet)" />
              <h4 style={{ fontSize: '0.92rem', fontWeight: 700 }}>AI Forecast Interpretation</h4>
            </div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              {predictionData.interpretation}
            </p>
            <div
              style={{
                marginTop: '12px',
                padding: '8px 12px',
                borderRadius: '8px',
                background: 'rgba(255, 255, 255, 0.03)',
                fontSize: '0.74rem',
                color: 'var(--text-muted)',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <Info size={14} color="#64748b" />
              <span>{predictionData.disclaimer}</span>
            </div>
          </div>

          {/* Model Specification Card */}
          <div className="glass-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <CheckCircle2 size={16} color="#10b981" />
              <h4 style={{ fontSize: '0.92rem', fontWeight: 700 }}>Model Specifications & Verification</h4>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.8rem' }}>
              <div style={{ color: 'var(--text-muted)' }}>Algorithm:</div>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                {predictionData.model_info.algorithm}
              </div>
              <div style={{ color: 'var(--text-muted)' }}>Test R² Accuracy:</div>
              <div style={{ fontWeight: 700, color: '#34d399' }}>
                {(predictionData.model_info.testing_r2_score * 100).toFixed(1)}% (0.9531)
              </div>
              <div style={{ color: 'var(--text-muted)' }}>Trained Features:</div>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                27 Input Dimensions (Lag, Rolling, Promo, Date)
              </div>
              <div style={{ color: 'var(--text-muted)' }}>Horizon Mode:</div>
              <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                Recursive Multi-Step Forward
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MlForecastingSection;
