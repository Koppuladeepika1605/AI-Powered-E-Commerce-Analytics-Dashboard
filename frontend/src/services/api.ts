// ==============================================================================
// AI-POWERED E-COMMERCE ANALYTICS DASHBOARD — API CLIENT SERVICE
// ==============================================================================

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
  ActualVsPredictedItem,
  BenchmarkModelItem,
  FulfilmentItem,
  SalesChannelItem,
  PredictionData,
  InsightsData,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

function buildQueryString(filters?: Partial<FilterState>, extraParams?: Record<string, any>): string {
  const params = new URLSearchParams();

  if (filters) {
    if (filters.startDate) params.append('start_date', filters.startDate);
    if (filters.endDate) params.append('end_date', filters.endDate);
    if (filters.category && filters.category !== 'ALL') params.append('category', filters.category);
    if (filters.state && filters.state !== 'ALL') params.append('state', filters.state);
    if (filters.status && filters.status !== 'ALL') params.append('status', filters.status);
    if (filters.fulfilment && filters.fulfilment !== 'ALL') params.append('fulfilment', filters.fulfilment);
    if (filters.salesChannel && filters.salesChannel !== 'ALL') params.append('sales_channel', filters.salesChannel);
  }

  if (extraParams) {
    Object.entries(extraParams).forEach(([key, val]) => {
      if (val !== undefined && val !== null) {
        params.append(key, String(val));
      }
    });
  }

  const qs = params.toString();
  return qs ? `?${qs}` : '';
}

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {}),
      },
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`API Error [${res.status} ${res.statusText}]: ${errorText}`);
    }

    return await res.json();
  } catch (err: any) {
    console.error(`Fetch failed for ${url}:`, err);
    throw err;
  }
}

export const ApiService = {
  getFilterOptions: async (): Promise<FilterOptions> => {
    return fetchJson<FilterOptions>('/api/filter-options');
  },

  getKpis: async (filters: FilterState): Promise<KpiData> => {
    return fetchJson<KpiData>(`/api/kpis${buildQueryString(filters)}`);
  },

  getSalesTrend: async (filters: FilterState, granularity: 'monthly' | 'daily' = 'monthly'): Promise<SalesTrendData> => {
    return fetchJson<SalesTrendData>(`/api/sales-trend${buildQueryString(filters, { granularity })}`);
  },

  getCategories: async (filters: FilterState): Promise<{ data: CategoryItem[] }> => {
    return fetchJson<{ data: CategoryItem[] }>(`/api/categories${buildQueryString(filters)}`);
  },

  getTopProducts: async (filters: FilterState, limit: number = 10): Promise<TopProductsData> => {
    return fetchJson<TopProductsData>(`/api/top-products${buildQueryString(filters, { limit })}`);
  },

  getGeography: async (filters: FilterState, stateLimit: number = 15, cityLimit: number = 15): Promise<GeographyData> => {
    return fetchJson<GeographyData>(`/api/geography${buildQueryString(filters, { state_limit: stateLimit, city_limit: cityLimit })}`);
  },

  getOrderStatus: async (filters: FilterState): Promise<{ data: OrderStatusItem[] }> => {
    return fetchJson<{ data: OrderStatusItem[] }>(`/api/order-status${buildQueryString(filters)}`);
  },

  getFulfilment: async (filters: FilterState): Promise<{ data: FulfilmentItem[] }> => {
    return fetchJson<{ data: FulfilmentItem[] }>(`/api/fulfilment${buildQueryString(filters)}`);
  },

  getSalesChannel: async (filters: FilterState): Promise<{ data: SalesChannelItem[] }> => {
    return fetchJson<{ data: SalesChannelItem[] }>(`/api/sales-channel${buildQueryString(filters)}`);
  },

  getPrediction: async (
    category: string = 'Set',
    forecastDays: number = 14,
    promotionRatio?: number,
    b2bRatio?: number
  ): Promise<PredictionData> => {
    return fetchJson<PredictionData>('/api/predictions', {
      method: 'POST',
      body: JSON.stringify({
        category,
        forecast_days: forecastDays,
        promotion_ratio: promotionRatio,
        b2b_ratio: b2bRatio,
      }),
    });
  },

  getCourierStatus: async (filters: FilterState): Promise<{ data: CourierStatusItem[] }> => {
    return fetchJson<{ data: CourierStatusItem[] }>(`/api/courier-status${buildQueryString(filters)}`);
  },

  getActualVsPredicted: async (category?: string): Promise<{ total_records: number; data: ActualVsPredictedItem[] }> => {
    const qs = category && category !== 'ALL' ? `?category=${encodeURIComponent(category)}` : '';
    return fetchJson<{ total_records: number; data: ActualVsPredictedItem[] }>(`/api/predictions/actual-vs-predicted${qs}`);
  },

  getBenchmarks: async (): Promise<{ models: BenchmarkModelItem[]; best_model_metrics: Record<string, any> }> => {
    return fetchJson<{ models: BenchmarkModelItem[]; best_model_metrics: Record<string, any> }>('/api/predictions/benchmarks');
  },

  getAiInsights: async (): Promise<InsightsData> => {
    return fetchJson<InsightsData>('/api/insights');
  },

  checkHealth: async (): Promise<{ status: string }> => {
    return fetchJson<{ status: string }>('/health');
  },
};
