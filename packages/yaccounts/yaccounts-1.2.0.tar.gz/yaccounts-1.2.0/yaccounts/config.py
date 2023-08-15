CODES_STUDENT_WAGES = (
    5510,  # Contracts: Student teaching assist salary
    5599,  # Contracts: Student Asst Salary (Reclass)
    5572,  # Contracts: Stdnt Research Assist Sal-FICA
    5570,  # Contracts: Student Research Assist Salary
    5610,  # Time Cards: Student Wages-Teaching Assist
    5672,  # Time Cards: Stdnt Wages Rsrch Assist-FICA
    5600,  # Time Cards: Student Wages
    5602,  # Time Cards: Student Wages-FICA
    5670,  # Time Cards: Student Wages-Research Assist
    5699,  # Time Cards: Student Wages (Reclass)
    5720,  # Non-Student Wages: Category 1 no Benefit
    5750,  # Non-Student Wages: Category 2 Part Benefit
    8905,  # Sponsored Research: Research Participant Stipends
    5812,  # Payroll Incentives (Cell Phone Personal Use)
    5950,  # Student Contract Benefits
    5960,  # Student Time Card Benefits
    5970,  # Non Student Benefits
    5999,  # Benefits (reclass)
)

CODES_STUDENT_TUITION = (
    6300,  # Scholarships
    6303,  # Graduate Tuition
    6304,  # Graduate Cash Award
    6309,  # Scholarships (reclass)
    6319,  # Student Aid (reclass)
    6390,  # Other Student Aid
)

CODES_FACULTY_SPRING_SUMMER = (
    5920,  # Faculty Supplemental Benefits
    5260,  # Faculty Sal-Spr/Sum-Benefits
    5220,  # Faculty Sal-Spr/Sum No Ben
    5240,  # Faculty Sal-Supp (Overload)
)

CODES_TRAVEL_FACULTY = (
    6190,  # Employee Development/Training
    6400,  # Insurance Expense
    6494,  # Other Medical
    7000,  # Domestic-Business Travel
    7010,  # Domestic-Recruiting Travel
    7020,  # Domestic-Prof Developmt Travel
    7050,  # Foreign-Business Travel
    7060,  # Foreign-Recruiting Travel
    7070,  # Foreign-Prof Developmt Travel
)

CODES_TRAVEL_STUDENT = (
    7030,  # Domestic-Student Travel
    7080,  # Foreign-Student Travel
)

CODES_TRAVEL = CODES_TRAVEL_FACULTY + CODES_TRAVEL_STUDENT

CODES_SUPPLIES = (
    2200,  # Accrued Liabilities - Faculty computers?
    5980,  # Other Payroll Benefits
    6000,  # Software Acquisitions/Support
    6005,  # Software / Media Licenses
    6100,  # Supplies
    6109,  # Supplies (reclass)
    6110,  # Supplies-BYU Store
    6120,  # Printing and Copying
    6125,  # Research Publications Costs
    6130,  # Postage and Mailing
    6140,  # Telecommunications
    6160,  # Advertising and Promotion
    6180,  # Hosting, Food, Entertainment
    6185,  # Guest Tickets
    6192,  # Employee Memberships, Dues
    6200,  # Contract Service-Off Campus
    6210,  # Contract Services-Campus
    6220,  # Rental Expense - Intra Campus
    6250,  # Non-capital equipment
    6255,  # Non-Cap Access Equipment
    6270,  # Equipment Maintenance
    6403,  # Other Academic Payments
    6405,  # Prizes
    6600,  # Access Equipment
    6610,  # Access Lab Equipment
    6480,  # Legal Fees
    6490,  # Other Expense
    6499,  # Other Expense (reclass)
    8940,  # Conference Hosting (R-project)
)

CODES_CAPITAL = (
    1625,  # Capital Equipment
    1725,  # AccDepre-Capital Equipment
    8930,  # Research Capital Equipment
    9126,  # AM Retirement-Assets
    9127,  # AM Retirement-Accum Depr
    9136,  # AM Transfer-Assets
    9137,  # AM Tansfer-Accum Depr
)

CODES_OVERHEAD = (
    8990,  # Facilities & Admin Recovery
    8991,  # Waived Facilities & Admin Cost
    8993,  # Subcontract Facilities & Admin
)

CODES_INTEREST = (
    4711,  # Interest Alloc-Claim on Cash
    4719,  # Non-Invest-Intrst Inc(reclass)
)

# Income only applies to non-budgeted accounts
CODES_INCOME = (
    3500,  # Beginning Net Assets
    4755,  # Distributed Royalty Income
    4891,  # Endowment Payout (UFS only)
    8920,  # Subawards w/ F&A
    8925,  # Subawards w/out F&A
    9250,  # Transfer Into Net Assets
    9260,  # Transfer Out of Net Assets
)

# Non-budgeted accounts, don't normally use BUDGET lines and they
# can be removed, except for these codes
CODES_NON_BUDGETED_BUDGET_CODES = (10,)

# These codes aren't used by anything and can be removed from the data
CODES_IGNORED = (
    1010,  # Claim on Cash
    1235,  # Sponsored Programs Receivable
    2000,  # Accounts Payable
    2210,  # Accrued Payroll-Biweekly
    3500,  # Beginning Net Assets
    4200,  # Gift Revenue-Cash
    4220,  # Grants & Contract Revenue
)

COL_NAME_AMOUNT = "JRNL Monetary Amount -no scrn aggregation"

COLOR_STUDENT_WAGES = "rosybrown"
COLOR_STUDENT_BENEFITS = "moccasin"
COLOR_STUDENT_TUITION = "moccasin"
COLOR_FACULTY = "lightskyblue"
COLOR_TRAVEL = "plum"
COLOR_SUPPLIES = "khaki"
COLOR_CAPITAL = "khaki"
COLOR_OVERHEAD = "silver"
COLOR_TOTAL_EXPENSES = "tomato"
COLOR_TOTAL_INCOME = "limegreen"


def all_expense_codes():
    return (
        CODES_STUDENT_WAGES
        + CODES_STUDENT_TUITION
        + CODES_FACULTY_SPRING_SUMMER
        + CODES_TRAVEL
        + CODES_SUPPLIES
        + CODES_OVERHEAD
        + CODES_CAPITAL
    )


def student_aid_expense_codes():
    return CODES_STUDENT_WAGES + CODES_STUDENT_TUITION + CODES_TRAVEL_STUDENT


def all_handled_codes():
    return all_expense_codes() + CODES_INTEREST + CODES_IGNORED + CODES_INCOME
