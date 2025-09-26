from django.shortcuts import render
from django.http import HttpResponse
from calculator.common import get_dividends_from_date
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.


def index_views(request):
    dividends = get_dividends_from_date("2025-01-01", datetime.now(), "O")
    
    results = []
    if request.method == "POST":

        # ticker별로 그룹화
        ticker_map = {}
        for i, item in enumerate(dividends):
            ownership = request.POST.get(f"ownership_{i}")
            if not ownership:
                continue
            total = float(item["cash_amount"]) * int(ownership)
            total = round(total, 2)
            year_month = item["declaration_date"][:7] if "declaration_date" in item else ""
            ticker = item["ticker"]
            if ticker not in ticker_map:
                ticker_map[ticker] = []
            ticker_map[ticker].append({
                "year_month": year_month,
                "ticker": ticker,
                "cash_amount": item["cash_amount"],
                "ownership": ownership,
                "total": total,
            })
        # 결과 리스트에 rowspan 추가
        for ticker, items in ticker_map.items():
            rowspan = len(items)
            for idx, row in enumerate(items):
                row_copy = row.copy()
                if idx == 0:
                    row_copy["rowspan"] = rowspan
                results.append(row_copy)
        
        request.session['results'] = results

        return redirect('index:index_views')
        
    results = request.session.pop('results', []) if 'results' in request.session else []

    return render(request, "index.html", {"dividends": dividends, "results": results})
