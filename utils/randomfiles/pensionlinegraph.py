import numpy as np
from matplotlib import pyplot as plt


def compound_interest(cash_monthly, years):
    interest = [cash_monthly]
    cash = [cash_monthly]
    balance = cash_monthly
    for i in range(12*years - 1):
        balance *= 1.005
        balance += cash_monthly
        interest.append(balance)
        cash.append(cash[-1] + cash_monthly)
    return interest, cash


def my_func(cash_monthly, years):
    x = np.linspace(0, years, years * 12)
    y1, y2 = np.array(compound_interest(cash_monthly, years))
    print(y1)
    print(type(y1))

    fig, ax = plt.subplots()
    ax.plot(x, y1)
    ax.plot(x, y2)

    ax.set_xlabel('Years')
    ax.set_ylabel('GBP (£)')

    ax.set_xlim(left=0)  # Set x-axis to start from 0
    ax.set_ylim(bottom=0)  # Set y-axis to start from 0

    ax.set_title('Pension Calculator')

    plt.show()
