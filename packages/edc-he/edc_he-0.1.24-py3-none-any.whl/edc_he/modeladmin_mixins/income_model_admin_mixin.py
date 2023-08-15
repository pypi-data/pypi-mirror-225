from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple


def get_income_fieldsets_tuple() -> list[tuple]:
    fieldsets = []
    sources = [
        ("wages", "Wages / Salary"),
        ("selling", "Selling, trading or hawking"),
        ("rental_income", "Rental income"),
        ("pension", "Pension, etc."),
        ("ngo_assistance", "NGO assistance"),
        ("interest", "Interest and dividends"),
        ("internal_remit", "Money transfers (domestic)"),
        ("external_remit", "Remittances (from outside the country)"),
        ("more_sources", "Other sources of income"),
    ]
    for fld, label in sources:
        fields = [
            fld,
            f"{fld}_value_known",
            f"{fld}_value",
        ]
        if fld == "external_remit":
            fields.extend(["external_remit_currency", "external_remit_currency_other"])
        if fld == "more_sources":
            fields.insert(1, "more_sources_other")

        fieldsets.append(
            (
                label,
                {
                    "description": format_html(
                        "Estimate the total amount of income from this source "
                        "for the <b>household</b> over the time period indicated"
                    ),
                    "fields": tuple(fields),
                },
            )
        )
    return fieldsets


class HealthEconomicsIncomeModelAdminMixin:
    form = None

    additional_instructions = format_html(
        "<H5><B><font color='orange'>Interviewer to read</font></B></H5>"
        "<P>We want to learn about the household and we use these questions "
        "to get an understanding of wealth and opportunities in the community.</P>"
        "<p>Now, I will ask about <b>income for the household</b> from paid work or "
        "other sources.</p><p>I know it may be difficult to calculate those figures, "
        "but please do try to give amounts as accurately as possible. Remember "
        "that <b>all information will be kept strictly confidential</b>. This "
        "information is important to assess overall health and well-being of "
        "people in your household, compared to other similar households.</p><p>"
        "I am now going to read you a list of possible sources of income. "
        "Thinking over the last 12 months, can you tell me what the average "
        "earnings of the household have been per week or per month or per year? "
        "Please tell me whichever time period that is easier for you.</p>"
    )
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        *get_income_fieldsets_tuple(),
        (
            "Dependents, financial status",
            {
                "fields": (
                    "external_dependents",
                    "income_enough",
                    "financial_status",
                    "financial_status_compare",
                )
            },
        ),
        (
            "Debt / Loans",
            {
                "description": format_html(
                    "<H5><B><font color='orange'>Interviewer to read</font></B></H5>"
                    "<p>Now, I will ask about the total current debt/loans for the household. "
                    "I know it may be difficult to calculate this, but please do try to "
                    "give amounts as accurately as possible. Remember that all information "
                    "will be kept strictly confidential. <B>It is not possible to offer "
                    "any help for your debts through this project</B>, but this information "
                    "will contribute to research and is important to assess the overall "
                    "health and well-being of people in your household, compared to other "
                    "similar households.</p>"
                ),
                "fields": (
                    "household_debt",
                    "household_debt_value",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "wages": admin.VERTICAL,
        "wages_value_known": admin.VERTICAL,
        "selling": admin.VERTICAL,
        "selling_value_known": admin.VERTICAL,
        "rental_income": admin.VERTICAL,
        "rental_income_value_known": admin.VERTICAL,
        "pension": admin.VERTICAL,
        "pension_value_known": admin.VERTICAL,
        "ngo_assistance": admin.VERTICAL,
        "ngo_assistance_value_known": admin.VERTICAL,
        "interest": admin.VERTICAL,
        "interest_value_known": admin.VERTICAL,
        "internal_remit": admin.VERTICAL,
        "internal_remit_value_known": admin.VERTICAL,
        "external_remit": admin.VERTICAL,
        "external_remit_value_known": admin.VERTICAL,
        "external_remit_currency": admin.VERTICAL,
        "more_sources": admin.VERTICAL,
        "more_sources_value_known": admin.VERTICAL,
        "income_enough": admin.VERTICAL,
        "financial_status": admin.VERTICAL,
        "financial_status_compare": admin.VERTICAL,
        "household_debt": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }
