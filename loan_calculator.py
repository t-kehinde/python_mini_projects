# #########################################################################
# LOAN CALCULATOR
# tags: [command line arguments]
#
# This program is designed to calculate the loan parameters for an annuity
# differentiated loan using the principal, periods, interest, payments and
# repayment type as parameters
# #########################################################################


import math
import sys
import argparse


def compute_differentiated_payment(P, n, i, m):
    """ Compute the differentiated payment for a loan. given
    the loan principal(P), number of periods(n), and interest rate(i). """
    i = i / (12 * 100)
    # monthly differentiated payment
    Dm = round((P / n) + i * (P - (P * (m - 1)) / n), 2)
    return Dm


def compute_loan_principal(A, n, i):
    """ Compute the loan principal for a loan. given the
    annuity payment, number of periods, and interest rate. """
    i = i / (12 * 100)            # i is the nominal interest rate
    P = round(A / ((i * (1 + i)**n) / ((1 + i)**n - 1)), 2)
    return P


def compute_annuity(P, n, i):
    """ Compute the annuity payment for a loan. given the loan
    principal, number of periods, and interest rate. """
    i = i / (12 * 100)
    A = round(P * ((i * (1 + i)**n) / ((1 + i)**n - 1)), 2)
    return A


def compute_number_of_payments(P, A, i):
    """ Compute the number of payments for a loan. given the loan
    principal, annuity payment, and interest rate. """
    i = i / (12 * 100)
    n = math.ceil(math.log((A / (A - i * P)), (1 + i)))

    # convert to years and months - if the number of years is
    # computed from the months is not an integer, get the
    # remaining number of months
    years = math.floor(n/12)
    months = n % 12
    return (years, months)


def loan_payment_calculator():
    """ Calculate the loan payment for a loan. given the loan
    principal, number of periods, and interest rate. """
    # Get the variables from the command line arguments
    loan_principal = args.principal
    number_of_periods = args.periods
    loan_interest = args.interest
    annuity_payments = args.payment
    # Validate the input
    try:
        if len(sys.argv) < 4:     # negative numbers are not allowed
            raise ValueError("Incorrect parameters")
    except ValueError:
        print("Incorrect parameters")
        sys.exit(1)
    # case for annuity payment amount
    if args.type == "annuity":
        if annuity_payments is None:
            annuity = compute_annuity(
                loan_principal, number_of_periods, loan_interest)
            print(f"Your annuity payment = {math.ceil(annuity)}!")

            overpayment = (math.ceil(annuity) * number_of_periods) - \
                math.ceil(loan_principal)
            print(f"Overpayment = {overpayment}")

        elif annuity_payments is not None and number_of_periods is None:
            # compute number of payments
            number_of_payments = compute_number_of_payments(
                loan_principal, annuity_payments, loan_interest)
            period_years, period_months = number_of_payments
            print(f"It will take {period_years} years{'and'  if period_months else ''} {period_months if period_months else ''}"
                  f"{'month' if period_months == 1 else 'months' if period_months > 1 else ''}to repay this loan!")
            # Compute the overpayment
            overpayment = math.ceil(
                annuity_payments * number_of_payments[0] * 12 + annuity_payments * number_of_payments[1] - math.ceil(loan_principal))
            print(f"Overpayment = {overpayment}")

        else:
            # Compute loan principal for both repayment types
            loan_principal = compute_loan_principal(
                annuity_payments, number_of_periods, loan_interest)
            print(f"Your loan principal = {math.floor(loan_principal)}!")
            # compute the overpayment
            overpayment = annuity_payments * number_of_periods - loan_principal
            print(f"Overpayment = {math.floor(overpayment)}")

    elif args.type == 'diff':
        sum_differentiated_payments = 0
        for month in range(1, number_of_periods + 1):
            differentiated_payments = compute_differentiated_payment(
                loan_principal, number_of_periods, loan_interest, month)
            sum_differentiated_payments += math.ceil(differentiated_payments)
            print(
                f"Month {month}: Payment is {math.ceil(differentiated_payments)}")
        print(
            f"Overpayment = {math.ceil(sum_differentiated_payments) - loan_principal}")


if __name__ == "__main__":
    # Prompt user for parameters to calculate
    parser = argparse.ArgumentParser(
        description=''' Calculate the loan payment for a loan.''')

    # Add the positional arguments to the parser
    parser.add_argument('--type', type=str,
                        help='type of repayment you want to analyze; annuity or diff ( Required )')

    parser.add_argument('--principal', type=int, required=False,
                        help='loan principal(Required). This can be computed if the interest, annuity payment, and principal are provided')
    parser.add_argument('--payment', type=float, required=False,
                        help='monthly payment amount. For the differentiated payment, this is different each month. Hence the number of months to repay the loan and the principal can not be calculated.')
    parser.add_argument('--interest', type=float,
                        help='interest rate without the percent symbol ( Required )')
    parser.add_argument('--periods', type=int, required=False,
                        help='number of months to repay the loan. This can be computed if the interest, annuity payment, and principal are provided')

    # Parse the arguments
    args = parser.parse_args()
    # Check that differentiated payment is not used with annuity payment
    try:
        if args.type == "diff" and args.payment is not None:
            raise TypeError("Incorrect parameters")
    except TypeError:
        print("Incorrect parameters")
        sys.exit(1)
    # Check for negative values in the parameters
    try:
        args_dict = vars(args)      # convert arguments to dictionary

        # remove strings and non-integer and non-float from the dictionary
        clean_args_dict = {k: v for k, v in args_dict.items(
        ) if v is not None and isinstance(v, int) or isinstance(v, float)}
        if any(v < 0 for v in clean_args_dict.values()):
            raise ValueError("Incorrect parameters")
    except ValueError:
        print("Incorrect parameters")
        sys.exit(1)
    # check for the required parameters - principal, interest
    try:
        if args.interest is None:
            raise ValueError("Incorrect parameters")
    except ValueError:
        print("Incorrect parameters")
        sys.exit(1)
    # Check that there are more than 3 arguments
    try:
        args_dict = vars(args)      # convert arguments to a dictionary
        if len(args_dict) < 1:
            print(len(args_dict))
            raise TypeError("Incorrect parameters")
    except TypeError:
        print("Incorrect parameters")
        sys.exit(1)

    loan_payment_calculator()
    input("\nPress Enter to exit...")
    exit()
