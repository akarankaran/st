import pandas as pd
import numpy as np
import numpy_financial as npf
import streamlit as st



st.set_page_config(page_title='Loan calculator' ,page_icon="📈" )


st.title('Loan calculator')

loan_amt = st.number_input('Loan Amount',value =500000)
interet_rate = st.number_input('Interest_rate (monthly)', value= 2)
tenure = st.slider('Tenure in months', 6, 48, 24)
int_type = st.radio('Type of interest rate', ['Reducing', 'Flat'])

inte = interet_rate/100
emi = (loan_amt * inte * pow(1+inte, tenure)) / (pow(1+inte, tenure) - 1)





# rate to be in percentage like ir = 2/100
# tenure in months

def red_to_flat(la, ir, te):
    flat_rate = ((((npf.pmt(ir,te,-la) * te) - la) /te) / la) 
    return flat_rate


def flat_to_red(la, ir, te):
    red_rate = npf.rate(te, ((la/te) + (la*ir)),-la, fv=0 )
    return red_rate


if int_type == 'Flat':
    st.write(f'Reducing rate is {round(flat_to_red(loan_amt, inte, tenure)*100,2)}')
else:
    st.write(f'Flat rate is {round(red_to_flat(loan_amt, inte, tenure)*100,2   )}')



if int_type == 'Flat':
    inte = flat_to_red(loan_amt, inte, tenure)
else:
    pass


def loan_table(int_type, inte, loan_amt, tenure, emi):
    loan_table = pd.DataFrame([[0,0,0,0,loan_amt]],
        columns=[
        'installment no.',
        'emi',
        'principle',
        'interest',
        'balance'
        ]
    )

    i = 0
    for i in range(tenure):
        i_ins = i+1
        i_emi = emi
        i_princ = (emi - (loan_table['balance'][i] * inte))
        i_int = (loan_table['balance'][i] * inte)
        i_bal = (loan_table['balance'][i]) - i_princ

        loan_table.loc[i+1]= [
            i_ins,
            i_emi,
            i_princ,
            i_int,
            i_bal]
        i = i + 1


    for i in loan_table[['emi', 'principle', 'interest', 'balance']]:
        loan_table[i] = loan_table[i].apply(lambda x: '{:.2f}'.format(x))
    
    loan_table['installment no.'] = loan_table['installment no.'].apply(lambda x:int(x))
    loan_table = loan_table[['emi', 'principle', 'interest', 'balance']]


    return loan_table





if st.button('calculate'):
    st.table(loan_table(int_type, inte, loan_amt, tenure, emi))
