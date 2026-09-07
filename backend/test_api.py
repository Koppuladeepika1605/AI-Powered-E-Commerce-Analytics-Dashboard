import sys
import json

# Ensure UTF-8 output on all platforms
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_endpoint(name: str, method: str, url: str, payload: dict = None, expected_status: int = 200):
    print(f"\n[TESTING] {name} -> {method} {url}...")
    if method.upper() == "GET":
        res = client.get(url)
    elif method.upper() == "POST":
        res = client.post(url, json=payload or {})
    else:
        raise ValueError(f"Unsupported method: {method}")

    assert res.status_code == expected_status, f"Expected {expected_status}, got {res.status_code}: {res.text}"
    data = res.json()
    print(f"  [PASS] Status: {res.status_code}")
    return data


def run_all_tests():
    print("=" * 80)
    print("      FASTAPI BACKEND ENDPOINT VALIDATION & INTEGRATION TEST SUITE")
    print("=" * 80)

    # 1. Health & Root
    health = test_endpoint("Health Check", "GET", "/health")
    assert health["status"] == "healthy"

    # 2. Filter Options
    filter_opts = test_endpoint("Filter Options", "GET", "/api/filter-options")
    assert "categories" in filter_opts and len(filter_opts["categories"]) > 5
    assert "states" in filter_opts and len(filter_opts["states"]) > 10
    print(f"  -> Categories available: {len(filter_opts['categories'])}, States: {len(filter_opts['states'])}")

    # 3. Overall KPIs
    kpis = test_endpoint("Executive KPIs", "GET", "/api/kpis")
    assert kpis["total_orders"] > 100000, f"Expected >100k orders, got {kpis['total_orders']}"
    assert kpis["total_sales_realized"] > 70000000, f"Expected >70M INR realized, got {kpis['total_sales_realized']}"
    print(f"  -> Realized Revenue: INR {kpis['total_sales_realized']:,.2f}")
    print(f"  -> Total Unique Orders: {kpis['total_orders']:,}")
    print(f"  -> AOV: INR {kpis['average_order_value']:,.2f}")
    print(f"  -> Cancellation Rate: {kpis['cancellation_rate_pct']:.2f}%")

    # 4. Filtered KPIs
    filtered_kpis = test_endpoint("Filtered KPIs (Category=Set)", "GET", "/api/kpis?category=Set")
    assert filtered_kpis["total_sales_realized"] < kpis["total_sales_realized"]
    print(f"  -> 'Set' Category Realized Revenue: INR {filtered_kpis['total_sales_realized']:,.2f}")

    # 5. Sales Trends (Monthly & Daily)
    monthly_trend = test_endpoint("Sales Trend (Monthly)", "GET", "/api/sales-trend?granularity=monthly")
    assert len(monthly_trend["data"]) >= 3
    print(f"  -> Monthly periods count: {len(monthly_trend['data'])}")

    daily_trend = test_endpoint("Sales Trend (Daily)", "GET", "/api/sales-trend?granularity=daily")
    assert len(daily_trend["data"]) > 60
    print(f"  -> Daily periods count: {len(daily_trend['data'])}")

    # 6. Categories
    categories = test_endpoint("Category Breakdown", "GET", "/api/categories")
    assert len(categories["data"]) >= 8
    top_cat = categories["data"][0]
    print(f"  -> Top Category: {top_cat['category']} (INR {top_cat['realized_revenue']:,.2f}, Share: {top_cat['revenue_share_pct']}%)")

    # 7. Top Products
    top_products = test_endpoint("Top Products", "GET", "/api/top-products?limit=10")
    assert len(top_products["top_styles"]) == 10
    assert len(top_products["top_skus"]) == 10
    print(f"  -> Top Style: {top_products['top_styles'][0]['style']} (INR {top_products['top_styles'][0]['realized_revenue']:,.2f})")

    # 8. Geography
    geo = test_endpoint("Geographic Insights", "GET", "/api/geography?state_limit=15&city_limit=15")
    assert len(geo["top_states"]) > 0
    assert len(geo["top_cities"]) > 0
    print(f"  -> Top State: {geo['top_states'][0]['state']} (INR {geo['top_states'][0]['realized_revenue']:,.2f})")
    print(f"  -> Top City: {geo['top_cities'][0]['city']} (INR {geo['top_cities'][0]['realized_revenue']:,.2f})")

    # 9. Order Status
    order_status = test_endpoint("Order Status Distribution", "GET", "/api/order-status")
    assert len(order_status["data"]) > 0
    print(f"  -> Primary Status: {order_status['data'][0]['status']} ({order_status['data'][0]['order_count']:,} orders)")

    # 10. Courier Status Distribution (Power BI Page 3 Visual)
    courier_status = test_endpoint("Courier Status Distribution", "GET", "/api/courier-status")
    assert len(courier_status["data"]) >= 4
    assert courier_status["data"][0]["courier_status"] == "Shipped"
    print(f"  -> Primary Courier Status: {courier_status['data'][0]['courier_status']} ({courier_status['data'][0]['order_count']:,} orders, INR {courier_status['data'][0]['realized_revenue']:,.2f})")

    # 11. Fulfilment
    fulfilment = test_endpoint("Fulfilment Performance", "GET", "/api/fulfilment")
    assert len(fulfilment["data"]) >= 2
    print(f"  -> Fulfilment Methods: {[f['fulfilment'] for f in fulfilment['data']]}")

    # 12. Sales Channels
    channels = test_endpoint("Sales Channels", "GET", "/api/sales-channel")
    assert len(channels["data"]) >= 1
    print(f"  -> Sales Channel: {channels['data'][0]['sales_channel']}")

    # 13. ML Predictions (POST & GET)
    pred_post = test_endpoint(
        "ML Forecast (POST)",
        "POST",
        "/api/predictions",
        payload={"category": "Set", "forecast_days": 14, "promotion_ratio": 0.25},
    )
    assert pred_post["status"] == "success"
    assert len(pred_post["daily_forecast"]) == 14
    assert pred_post["kpis"]["total_predicted_revenue_inr"] > 0
    print(f"  -> 14-Day Predicted Revenue for 'Set': INR {pred_post['kpis']['total_predicted_revenue_inr']:,.2f}")
    print(f"  -> Total Predicted Demand: {pred_post['kpis']['total_predicted_unit_demand']:,} units")
    print(f"  -> Model Algorithm: {pred_post['model_info']['algorithm']}")

    pred_get = test_endpoint("ML Forecast (GET)", "GET", "/api/predictions?category=Kurta&forecast_days=7")
    assert pred_get["status"] == "success"
    assert len(pred_get["daily_forecast"]) == 7
    print(f"  -> 7-Day Predicted Revenue for 'Kurta': INR {pred_get['kpis']['total_predicted_revenue_inr']:,.2f}")

    # 14. ML Holdout Predictions & Benchmarks
    holdout = test_endpoint("ML Holdout Actual vs Predicted", "GET", "/api/predictions/actual-vs-predicted?category=Set")
    assert holdout["total_records"] > 0
    print(f"  -> Holdout Test Records for 'Set': {holdout['total_records']}")

    benchmarks = test_endpoint("ML Benchmark Models", "GET", "/api/predictions/benchmarks")
    assert len(benchmarks["models"]) >= 4
    print(f"  -> Benchmark Models Count: {len(benchmarks['models'])}")

    # 15. AI Business Insights
    insights = test_endpoint("AI Business Insights", "GET", "/api/insights")
    assert len(insights["insights"]) >= 5
    assert insights["executive_summary"]["health_score"] > 0
    print(f"  -> Executive Headline: {insights['executive_summary']['headline']}")
    print(f"  -> Generated Insights Count: {len(insights['insights'])}")

    print("\n" + "=" * 80)
    print("  >>> ALL 15 BACKEND API & POWER BI INTEGRATION TESTS PASSED WITH 100% SUCCESS <<<")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    run_all_tests()
