// ==============================================================================
// AI-POWERED E-COMMERCE ANALYTICS DASHBOARD — FRONTEND TYPES
// ==============================================================================

export interface FilterState {
  startDate: string;
  endDate: string;
  category: string;
  state: string;
  status: string;
  fulfilment: string;
  salesChannel: string;
}

export interface FilterOptions {
  categories: string[];
  states: string[];
  statuses: string[];
  fulfilment_types: string[];
  sales_channels: string[];
  date_range: {
    min_date: string;
    max_date: string;
  };
}

export interface KpiData {
  total_sales_gross: number;
  total_sales_realized: number;
  total_orders: number;
  total_units_sold: number;
  average_order_value: number;
  cancellation_rate_pct: number;
  return_rate_pct: number;
  realization_rate_pct: number;
  lost_revenue_inr: number;
  b2b_sales_pct: number;
  promo_usage_pct: number;
}

export interface SalesTrendItem {
  period: string;
  order_count: number;
  units_sold: number;
  gross_amount: number;
  realized_revenue: number;
  growth_pct?: number | null;
}

export interface SalesTrendData {
  granularity: 'monthly' | 'daily';
  data: SalesTrendItem[];
}

export interface CategoryItem {
  category: string;
  total_transactions: number;
  total_quantity: number;
  gross_amount: number;
  realized_revenue: number;
  revenue_share_pct: number;
  realization_rate_pct: number;
  cancellation_rate_pct: number;
}

export interface TopProductItem {
  style?: string;
  sku?: string;
  category: string;
  total_orders: number;
  total_quantity: number;
  gross_amount: number;
  realized_revenue: number;
  realization_rate_pct: number;
}

export interface TopProductsData {
  top_styles: TopProductItem[];
  top_skus: TopProductItem[];
}

export interface StateSalesItem {
  state: string;
  total_orders: number;
  total_quantity: number;
  realized_revenue: number;
  revenue_share_pct: number;
  cancellation_rate_pct: number;
}

export interface CitySalesItem {
  city: string;
  state: string;
  total_orders: number;
  realized_revenue: number;
}

export interface GeographyData {
  top_states: StateSalesItem[];
  top_cities: CitySalesItem[];
}

export interface OrderStatusItem {
  status: string;
  order_count: number;
  share_pct: number;
  total_quantity: number;
  realized_revenue: number;
}

export interface CourierStatusItem {
  courier_status: string;
  order_count: number;
  share_pct: number;
  total_quantity: number;
  realized_revenue: number;
}

export interface ActualVsPredictedItem {
  Date: string;
  Category: string;
  Actual_Revenue: number;
  Predicted_Revenue: number;
  Baseline_Lag7_Revenue: number;
  Prediction_Error: number;
}

export interface BenchmarkModelItem {
  Model?: string;
  MAE?: number;
  RMSE?: number;
  R2?: number;
  MAPE?: string | number;
  [key: string]: any;
}

export interface PowerBiEmbedConfig {
  embedUrl: string;
  reportId: string;
  groupId?: string;
  accessToken?: string;
  activePage: number;
}

export interface FulfilmentItem {
  fulfilment: string;
  fulfilled_by: string;
  order_lines: number;
  volume_share_pct: number;
  total_quantity: number;
  gross_amount: number;
  realized_revenue: number;
  realization_rate_pct: number;
  cancellation_rate_pct: number;
}

export interface SalesChannelItem {
  sales_channel: string;
  total_records: number;
  channel_share_pct: number;
  total_units: number;
  gross_amount: number;
  realized_revenue: number;
  realization_rate_pct: number;
}

export interface DailyForecastItem {
  date: string;
  day_of_week: string;
  is_weekend: boolean;
  predicted_revenue_inr: number;
  predicted_unit_demand: number;
  lower_bound_inr: number;
  upper_bound_inr: number;
}

export interface ForecastKpis {
  total_predicted_revenue_inr: number;
  total_predicted_unit_demand: number;
  daily_average_revenue_inr: number;
  avg_selling_price_inr: number;
}

export interface ModelInfo {
  model_name: string;
  algorithm: string;
  target_metric: string;
  feature_count: number;
  features_used: string[];
  training_r2_score: number;
  testing_r2_score: number;
  testing_mae_inr: number;
}

export interface HistoricalPoint {
  date: string;
  actual_revenue: number;
  actual_units: number;
}

export interface PredictionData {
  status: string;
  category: string;
  forecast_horizon_days: number;
  forecast_start_date: string;
  forecast_end_date: string;
  kpis: ForecastKpis;
  daily_forecast: DailyForecastItem[];
  recent_history: HistoricalPoint[];
  model_info: ModelInfo;
  interpretation: string;
  disclaimer: string;
}

export interface InsightItem {
  id: string;
  category: string;
  title: string;
  severity: 'high' | 'medium' | 'low' | 'positive';
  summary: string;
  impact_metric: string;
  impact_value: string;
  actionable_recommendation: string;
  supporting_data?: Record<string, any>;
}

export interface ExecutiveSummary {
  headline: string;
  health_score: number;
  primary_revenue_driver: string;
  top_operational_leak: string;
  recommended_focus_area: string;
}

export interface InsightsData {
  executive_summary: ExecutiveSummary;
  insights: InsightItem[];
  generated_at: string;
  engine_version: string;
}
