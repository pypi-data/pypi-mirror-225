from calendar import monthrange

from NEMO.decorators import accounting_or_user_office_or_manager_required
from NEMO.typing import QuerySetType
from NEMO.utilities import extract_optional_beginning_and_end_dates, get_month_timeframe, month_list
from NEMO.views.pagination import SortedPaginator
from NEMO.views.usage import get_managed_projects
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from NEMO_billing.models import CoreFacility
from NEMO_billing.prepayments.models import Fund, ProjectPrepaymentDetail


@login_required
def usage_project_prepayments(request):
    start_date, end_date = get_month_timeframe()
    projects = get_managed_projects(request.user)
    prepaid_projects = ProjectPrepaymentDetail.objects.filter(project__in=[project for project in projects if project.active])
    add_fund_info_to_prepaid_projects(request, prepaid_projects, start_date, end_date)
    return render(request, "prepayments/prepaid_project_status_table.html", {"page": prepaid_projects})


@accounting_or_user_office_or_manager_required
@require_http_methods(["GET", "POST"])
def prepaid_project_status(request):
    # Default is year to date
    start_date, end_date = get_month_timeframe()
    start_date = start_date.replace(month=1)
    if request.POST.get("start") and request.POST.get("end"):
        submitted_start_date, submitted_end_date = extract_optional_beginning_and_end_dates(
            request.POST, date_only=True
        )
        if not submitted_start_date > submitted_end_date:
            start_date = start_date.replace(year=submitted_start_date.year, month=submitted_start_date.month)
            end_date = end_date.replace(
                year=submitted_end_date.year,
                month=submitted_end_date.month,
                day=monthrange(submitted_end_date.year, submitted_end_date.month)[1],
            )
    page = SortedPaginator(ProjectPrepaymentDetail.objects.all(), request, order_by="project").get_current_page()
    add_fund_info_to_prepaid_projects(request, page.object_list, start_date, end_date)
    dictionary = {
        "start": start_date,
        "end": end_date,
        "month_list": month_list(),
        "page": page,
        "core_facilities_exist": CoreFacility.objects.exists(),
    }
    return render(request, "prepayments/prepaid_project_status.html", dictionary)


def add_fund_info_to_prepaid_projects(request, prepaid_projects: QuerySetType[ProjectPrepaymentDetail], start_date, end_date):
    for prepaid_project in prepaid_projects:
        try:
            prepaid_project: ProjectPrepaymentDetail = prepaid_project
            charges, charges_amount, funds = prepaid_project.get_prepayment_info(start_in_month=start_date, until=end_date)
            bulk_funds = Fund.objects.in_bulk(funds)
            prepaid_project.total_funds = sum(fund.amount for fund in bulk_funds.values())
            prepaid_project.total_funds_left = sum(
                balance for fund_id, balance in funds.items() if bulk_funds[fund_id].is_active(end_date)
            )
            prepaid_project.charges_amount = sum(charge.amount for charge in charges)
            prepaid_project.taxes_amount = (
                prepaid_project.charges_amount * prepaid_project.configuration.tax_amount()
                if not prepaid_project.project.projectbillingdetails.no_tax
                else 0
            )
            prepaid_project.total_charges_amount = prepaid_project.charges_amount + prepaid_project.taxes_amount
            prepaid_project.charges = charges
            prepaid_project.charges.reverse()
        except Exception as e:
            messages.error(request, str(e), extra_tags="data-trigger=manual")
