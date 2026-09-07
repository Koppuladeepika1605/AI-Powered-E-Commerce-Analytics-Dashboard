import React, { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { FilterBar } from './components/FilterBar';
import { KpiCards } from './components/KpiCards';
import { SalesTrendSection } from './components/SalesTrendSection';
import { CategorySection } from './components/CategorySection';
import { TopProductsSection } from './components/TopProductsSection';
import { GeographySection } from './components/GeographySection';
import { OperationsSection } from './components/OperationsSection';
import { MlForecastingSection } from './components/MlForecastingSection';
import { PowerBiShowcaseSection } from './components/PowerBiShowcaseSection';
import { AiInsightsSection } from './components/AiInsightsSection';
import { ApiService } from './services/api';
import {
  FilterState,
  FilterOptions,
  KpiData,
  SalesTrendData,
  CategoryItem,
  TopProductsData,
  GeographyData,
  OrderStatusItem,
  CourierStatusItem,
  FulfilmentItem,
  SalesChannelItem,
} from './types';
import { AlertCircle, RefreshCw, CheckCircle, Database, Cpu, Code2, Sparkles } from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [dbStatus, setDbStatus] = useState<'online' | 'error' | 'checking'>('checking');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Global Filter State
  const [filters, setFilters] = useState<FilterState>({
    startDate: '',
    endDate: '',
    category: 'ALL',
    state: 'ALL',
    status: 'ALL',
    fulfilment: 'ALL',
    salesChannel: 'ALL',
  });

  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);

  // Dashboard Data Stores
  const [kpis, setKpis] = useState<KpiData | null>(null);
  const [trendData, setTrendData] = useState<SalesTrendData | null>(null);
  const [trendGranularity, setTrendGranularity] = useState<'monthly' | 'daily'>('monthly');
  const [categories, setCategories] = useState<CategoryItem[]>([]);
  const [productsData, setProductsData] = useState<TopProductsData | null>(null);
  const [geoData, setGeoData] = useState<GeographyData | null>(null);
  const [orderStatuses, setOrderStatuses] = useState<OrderStatusItem[]>([]);
  const [courierStatuses, setCourierStatuses] = useState<CourierStatusItem[]>([]);
  const [fulfilments, setFulfilments] = useState<FulfilmentItem[]>([]);
  const [salesChannels, setSalesChannels] = useState<SalesChannelItem[]>([]);

  // Fetch Filter Dropdown Options on mount
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const opts = await ApiService.getFilterOptions();
        setFilterOptions(opts);
      } catch (err) {
        console.error('Failed to load filter options:', err);
      }
    };
    fetchOptions();
  }, []);

  // Fetch Dashboard Analytics Data
  const loadDashboardData = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      // Parallel API Fetching
      const [
        kpiRes,
        trendRes,
        catRes,
        prodRes,
        geoRes,
        statusRes,
        courierRes,
        fulfilRes,
        channelRes,
        healthRes,
      ] = await Promise.all([
        ApiService.getKpis(filters),
        ApiService.getSalesTrend(filters, trendGranularity),
        ApiService.getCategories(filters),
        ApiService.getTopProducts(filters, 10),
        ApiService.getGeography(filters, 15, 15),
        ApiService.getOrderStatus(filters),
        ApiService.getCourierStatus(filters),
        ApiService.getFulfilment(filters),
        ApiService.getSalesChannel(filters),
        ApiService.checkHealth(),
      ]);

      setKpis(kpiRes);
      setTrendData(trendRes);
      setCategories(catRes.data);
      setProductsData(prodRes);
      setGeoData(geoRes);
      setOrderStatuses(statusRes.data);
      setCourierStatuses(courierRes.data);
      setFulfilments(fulfilRes.data);
      setSalesChannels(channelRes.data);
      setDbStatus(healthRes.status === 'healthy' ? 'online' : 'error');
    } catch (err: any) {
      console.error('Error fetching dashboard analytics:', err);
      setErrorMessage(err.message || 'Failed to connect to Analytics API.');
      setDbStatus('error');
    } finally {
      setIsLoading(false);
    }
  }, [filters, trendGranularity]);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleResetFilters = () => {
    setFilters({
      startDate: '',
      endDate: '',
      category: 'ALL',
      state: 'ALL',
      status: 'ALL',
      fulfilment: 'ALL',
      salesChannel: 'ALL',
    });
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Ambient Decorative Lighting */}
      <div className="ambient-glow-1" />
      <div className="ambient-glow-2" />

      {/* Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onRefresh={loadDashboardData}
        isLoading={isLoading}
        dbStatus={dbStatus}
      />

      {/* Main Content Area */}
      <main style={{ flex: 1, maxWidth: '1440px', width: '100%', margin: '0 auto', padding: '24px' }}>
        {/* Error Alert Banner */}
        {errorMessage && (
          <div
            className="glass-card"
            style={{
              marginBottom: '20px',
              borderLeft: '4px solid #f43f5e',
              background: 'rgba(244, 63, 94, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '14px 20px',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <AlertCircle size={20} color="#fb7185" />
              <div>
                <strong style={{ color: '#fb7185' }}>Backend Connection Notice:</strong>
                <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
                  {errorMessage} Ensure FastAPI backend server is running on port 8000 (`uvicorn backend.main:app`).
                </p>
              </div>
            </div>
            <button onClick={loadDashboardData} className="btn-secondary" style={{ fontSize: '0.78rem' }}>
              Retry
            </button>
          </div>
        )}

        {/* Global Filter Bar (Available on Overview, Regional/Product & Operations tabs) */}
        {activeTab !== 'ml' && activeTab !== 'powerbi' && activeTab !== 'insights' && (
          <FilterBar
            filters={filters}
            filterOptions={filterOptions}
            onFilterChange={handleFilterChange}
            onResetFilters={handleResetFilters}
          />
        )}

        {/* TAB 1: EXECUTIVE OVERVIEW (Power BI Page 1) */}
        {activeTab === 'overview' && (
          <div>
            <KpiCards kpis={kpis} isLoading={isLoading} />
            <CategorySection categories={categories} isLoading={isLoading} />
            <SalesTrendSection
              trendData={trendData}
              granularity={trendGranularity}
              onGranularityChange={setTrendGranularity}
              isLoading={isLoading}
            />
          </div>
        )}

        {/* TAB 2: REGIONAL & PRODUCT ANALYSIS (Power BI Page 2) */}
        {activeTab === 'regional_product' && (
          <div>
            <KpiCards kpis={kpis} isLoading={isLoading} />
            <GeographySection geoData={geoData} isLoading={isLoading} />
            <TopProductsSection productsData={productsData} isLoading={isLoading} />
          </div>
        )}

        {/* TAB 3: OPERATIONS ANALYSIS (Power BI Page 3) */}
        {activeTab === 'operations' && (
          <div>
            <OperationsSection
              courierStatuses={courierStatuses}
              orderStatuses={orderStatuses}
              fulfilments={fulfilments}
              salesChannels={salesChannels}
              cancellationRate={kpis?.cancellation_rate_pct}
              isLoading={isLoading}
            />
          </div>
        )}

        {/* TAB 4: ML DEMAND FORECASTING & VALIDATION (Phase 6) */}
        {activeTab === 'ml' && (
          <MlForecastingSection
            categories={filterOptions?.categories || ['Set', 'Kurta', 'Western Dress', 'Top', 'Saree']}
          />
        )}

        {/* TAB 5: POWER BI DEDICATED SHOWCASE & ARCHITECTURE */}
        {activeTab === 'powerbi' && <PowerBiShowcaseSection />}

        {/* TAB 6: AI BUSINESS INSIGHTS */}
        {activeTab === 'insights' && <AiInsightsSection />}
      </main>

      {/* Footer */}
      <footer
        style={{
          borderTop: '1px solid var(--border-subtle)',
          background: 'rgba(9, 13, 22, 0.95)',
          padding: '24px',
          marginTop: 'auto',
          zIndex: 10,
        }}
      >
        <div
          style={{
            maxWidth: '1440px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '16px',
            fontSize: '0.8rem',
            color: 'var(--text-muted)',
          }}
        >
          <div>
            <strong>AI-Powered E-Commerce Analytics Dashboard</strong> • Power BI Concordance Architecture
          </div>
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Database size={13} color="#6366f1" /> Star Schema & SQL Engine
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Sparkles size={13} color="#f59e0b" /> Microsoft Power BI Source of Truth
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Cpu size={13} color="#a855f7" /> Scikit-Learn Forecaster
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Code2 size={13} color="#06b6d4" /> FastAPI + React TypeScript
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
