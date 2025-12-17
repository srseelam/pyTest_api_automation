import pytest
import importlib
import json
import warnings
from collections import defaultdict
from py.xml import html
from common.auth_flow import get_token
from routes.products_api import ProductsAPI
from routes.users_api import UsersAPI
from routes.carts_api import CartsAPI
from utils.common_utils import mask_token

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="pytest_html"
)

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment: dev, qa, staging"
    )

@pytest.fixture(scope="session")
def env(request):
    env_name = request.config.getoption("--env")
    return importlib.import_module(f"config.{env_name}")

results = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0})

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Get scenario from marker
        scenario = "Unmarked"
        for marker in item.iter_markers():
            scenario = marker.name
            break

        results[scenario]["total"] += 1

        if report.passed:
            results[scenario]["passed"] += 1
        elif report.failed:
            results[scenario]["failed"] += 1
            
    res = getattr(item, "_response_data", {})
    report.response_code = res.get("status_code", "-")
    if report.when == "call" and report.failed:
        req = getattr(item, "_request_data", {})
        headers = req.get("headers", {})
        req["headers"] = mask_token(headers)
        body = res.get("body", "")
        try:
            parsed_body = json.loads(body)
            pretty_body = json.dumps(parsed_body, indent=2)
        except Exception:
            pretty_body = body  # non-JSON response
        report.request_data = json.dumps(req, indent=2)
        report.response_data = parsed_body

        # call.excinfo is a pytest.ExceptionInfo object
        exc_info = call.excinfo
        report.exceptionType = exc_info.type# Exception type
        report.exceptionMessage = exc_info.value       # Exception message     
       
        
def _row_color(pass_percent):
    if pass_percent >= 90:
        return "#008000"   # green
    elif pass_percent >= 80:
        return "#ffa500"   # yellow
    else:
        return "#ff0000"   # red 
    
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append("<h2>Execution Summary</h2>")
    prefix.append("""
    <style>
        table.summary-table {
            border-collapse: collapse;
            width: 70%;
        }
        table.summary-table th, table.summary-table td {
            border: 1px solid #333;
            padding: 6px;
            text-align: center;
            text-color: #ffffff;
        }
        table.summary-table th {
            background-color: #f2f2f2;
        }
    </style>
    """)
    prefix.append("""
    <table border="1" style="border-collapse:collapse; width:60%">
        <tr>
            <th>Scenario</th>
            <th>Test cases</th>
            <th>Pass</th>
            <th>Fail</th>
            <th>Pass %</th>
        </tr>
    """)

    total_tests = total_pass = total_fail = 0

    for scenario, data in results.items():
        total = data["total"]
        passed = data["passed"]
        failed = data["failed"]

        pass_pct = round((passed / total) * 100) if total else 0
        
        total_tests += total
        total_pass += passed
        total_fail += failed
        row_color = _row_color(pass_pct)
        prefix.append(f"""
        <tr style="color:white; background-color:{row_color}">
            <td>{scenario.capitalize()}</td>
            <td>{total}</td>
            <td>{passed}</td>
            <td>{failed}</td>
            <td>{pass_pct}%</td>
        </tr>
        """)
        

    # Total row
    total_pass_pct = round((total_pass / total_tests) * 100) if total_tests else 0
    total_row_color = _row_color(total_pass_pct)
    prefix.append(f"""
        <tr style="font-weight:bold;background-color:{total_row_color};color:white">
            <td>Total</td>
            <td>{total_tests}</td>
            <td>{total_pass}</td>
            <td>{total_fail}</td>
            <td>{total_pass_pct}%</td>
        </tr>
    </table>
    """)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    pytest.current_test_node = item
    yield
    pytest.current_test_node = None

def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Response Code"))
    cells.insert(3, html.th("Request"))
    cells.insert(4, html.th("Response"))
    cells.insert(5, html.th("Exception"))
    
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(getattr(report, "response_code", "-")))
    cells.insert(3, html.td(
        html.pre(getattr(report, "request_data", "-"),
                 style="max-height:200px;overflow:auto;white-space:pre-wrap")
    ))
    cells.insert(4, html.td(
        html.pre(getattr(report, "response_data", "-"),
                 style="max-height:200px;overflow:auto;white-space:pre-wrap")
    ))
    cells.insert(5, html.td(
        html.pre(f"{getattr(report, 'exceptionType', '-')}: {getattr(report, 'exceptionMessage', '-')}",
            style="max-height:200px;overflow:auto;white-space:pre-wrap")
    ))
    
     
def pytest_metadata(metadata):
    metadata.clear()
            
@pytest.fixture(scope="session")
def token(): return get_token()

@pytest.fixture()
def products_api(token): return ProductsAPI(token)

@pytest.fixture()
def users_api(token): return UsersAPI(token)

@pytest.fixture()
def carts_api(token): return CartsAPI(token)