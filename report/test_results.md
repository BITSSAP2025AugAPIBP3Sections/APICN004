# TITO Test Results — APICN004

- LLM provider / model: `slm` / `qwen2.5:3b`
- Top-k retrieved: 6
- Vector store: ChromaDB (cosine) over sentence-transformers `sentence-transformers/all-MiniLM-L6-v2`
- Correctness column filled in by human review against the official answer key.

## Easy

| ID | Question | Answer (truncated) | Correct? | Note | Sources |
|----|----------|--------------------|----------|------|---------|
| Q-E01 | What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)? | Under the new tax regime for the financial year 2024-25 (Assessment Year 2025-26), the income tax slab rates for an individual are as follows:  - Income up to â¹ 3,00,000 (3 lakh) Nil - Income from â¹ 3,00,001 to â¹ 7,00,000 (7 lakh) 5% tax - Income from â¹ 7,00,001 to â¹ 10,00,000 (10 lakh) 10% tax - Income from … |  |  | bs2024_25.pdf p.29; bs2024_25.pdf p.33; bs2024_25(I).pdf p.29; bs2024_25.pdf p.54; bs2024_25.pdf p.32 |
| Q-E02 | What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investmen… | The maximum deduction allowed under Section 80C in a financial year is one hundred and fifty thousand rupees (150,000).  Three eligible investments under Section 80C are: 1. Investments in National Savings Certificates (NSC) 2. Investments in Public Provident Fund (PPF) 3. Investments in Life Insurance Policies  These … |  |  | Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.278; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.471; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b93… |
| Q-E03 | What is the basic exemption limit for a resident individual under 60 years of age under the old regime? | I could not find this in the provided corpus. |  |  | bs2023_24.pdf p.39; Updated-FQAs-on-Interplay&Transitions.pdf p.89; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.764; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b… |
| Q-E04 | What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25? | Under the new tax regime for the financial year 2024-25, the standard deduction available to a salaried employee is proposed to be increased from â¹50,000/- to â¹75,000/-.  This information is sourced from page 32 of the document bs2024_25.pdf. |  |  | bs2024_25.pdf p.32; bs2024_25.pdf p.54; bs2024_25.pdf p.29; bs2024_25.pdf p.33 |
| Q-E05 | What is the tax rate applicable to long-term capital gains on listed equity shares held for more than 12 month… | According to the provisions from the Income-tax Act 1961, for the financial year 2024-25, the tax rate applicable to long-term capital gains on listed equity shares held for more than 12 months is 12.5%. This is stated in the document bs2024_25.pdf, specifically on page 144. |  |  | Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.428; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.429; bs2024_25.pdf p.56; bs2024_25.pdf p.30; Income-t… |

## Medium

| ID | Question | Answer (truncated) | Correct? | Note | Sources |
|----|----------|--------------------|----------|------|---------|
| Q-M01 | A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹… | To compute the tax for the salaried individual under the new tax regime, we need to follow these steps:  1. **Calculate Gross Income**:     - Gross Annual Salary: â¹18,00,000    - EPF Contribution: â¹1,50,000    - NPS Tier-1 Contribution: â¹25,000    - Health Insurance Premium: â¹25,000    - Total Deductions: â¹1,… |  |  | bs2024_25.pdf p.32; bs2024_25.pdf p.33; bs2024_25.pdf p.36; bs2024_25.pdf p.37; bs2024_25.pdf p.9 |
| Q-M02 | I bought a residential property for ₹80,00,000 in 2018 and sold it in FY 2024-25 for ₹1,20,00,000. Compute the… | To compute the capital gains tax due, we need to follow the provisions for capital gains taxation as stated in the provided corpus. The corpus does not specify the indexation assumptions, so we will assume the indexation is done using the Cost Inflation Index (CII) as per the provisions.  ### Step 1: Determine the Cost… |  |  | bs2024_25.pdf p.30; bs2024_25.pdf p.56; bs2024_25.pdf p.58; bs2024_25.pdf p.33 |
| Q-M03 | An individual transfers ₹12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for forei… | For the financial year 2023-24, the proposed changes to Section 206C of the Income-tax Act state that the rate of TCS for foreign remittances for the purpose of education through LRS is proposed to increase from 5% to 20% for remittances in excess of â¹7 lakh. Since the individual is transferring â¹12,00,000, which i… |  |  | bs2023_24.pdf p.44; bs2023_24.pdf p.48; bs2023_24.pdf p.52; bs2023_24.pdf p.37 |
| Q-M04 | What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, includin… | Under Section 115BBH of the Income-tax Act, 2023-2024, for taxation of income from transfer of any virtual digital asset, the following provisions apply:  1. **Rate of Taxation**: The income-tax payable shall be the aggregate of the amount of income-tax calculated on the income from transfer of such virtual digital ass… |  |  | bs202223.pdf p.27; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.460; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.748; E-Book-Guidance-Note-Crypto-A… |
| Q-M05 | A taxpayer has salary income and one self-occupied house with home-loan interest of ₹2,00,000. With gross tota… | To determine which tax regime (old or new) is lower for the taxpayer, we need to calculate the tax liability under both regimes.  ### Old Tax Regime: Under the old tax regime, the tax rate structure is as follows: - 0-3 lakh rupees: Nil - 3-7 lakh rupees: 5% - 7-10 lakh rupees: 10% - 10-12 lakh rupees: 15% - 12-15 lakh… |  |  | bs2024_25.pdf p.33; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.260; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.93; Income-tax-Act-1961_2026_2026… |

## Complex

| ID | Question | Answer (truncated) | Correct? | Note | Sources |
|----|----------|--------------------|----------|------|---------|
| Q-C01 | Mr. A (resident, 45) has: (i) salary ₹24,00,000; (ii) LTCG ₹6,00,000 on listed equity sold after 23 July 2024;… | To compute the total tax under both the old and new tax regimes for Mr. A, we need to follow the tax calculation steps for each regime and then compare the results.  ### Old Tax Regime  #### Step 1: Calculate Gross Total Income - Salary: â¹24,00,000 - LTCG: â¹6,00,000 - STCG: â¹2,00,000 - Interest Income: â¹3,00,00… |  |  | bs2024_25.pdf p.32; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.86; bs2024_25.pdf p.33; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.310; Income-ta… |
| Q-C02 | A non-resident FII earned ₹50,00,000 from Indian listed securities in FY 2024-25. Explain how the FAQs on FIIs… | For a non-resident FII earning â¹50,00,000 from Indian listed securities in the assessment year (AY) 2024-25, the tax treatment would be governed by the provisions of the Income-tax Act, 2025, as per the FAQs on FIIs Exemption and transition provisions.  ### Tax Rate: Under section 210(1) of the Income-tax Act, 2025, … |  |  | FAQs-on-BIS-Exemption.pdf p.1; FAQs-on-BIS-Exemption.pdf p.2; Updated-FQAs-on-Interplay&Transitions.pdf p.91 |
| Q-C03 | Compare the treatment of 'days of stay' for determining residential status for an individual with Indian incom… | To determine the residential status for the individual with an income of â¹40,00,000, we need to apply the provisions of the Income-tax Act, 1961, as applicable to the assessment year 2026-27.  ### Residential Status for Resident Individual  For residential status, the individual must meet one of the following conditi… |  |  | Updated-FQAs-on-Interplay&Transitions.pdf p.89; Updated-FQAs-on-Interplay&Transitions.pdf p.87; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.22; Income-tax-Act-1961… |

## Full answers

<details><summary>Q-E01 — full answer (14618 ms)</summary>

Under the new tax regime for the financial year 2024-25 (Assessment Year 2025-26), the income tax slab rates for an individual are as follows:

- Income up to â¹ 3,00,000 (3 lakh) Nil
- Income from â¹ 3,00,001 to â¹ 7,00,000 (7 lakh) 5% tax
- Income from â¹ 7,00,001 to â¹ 10,00,000 (10 lakh) 10% tax
- Income from â¹ 10,00,001 to â¹ 12,00,000 (12 lakh) 15% tax
- Income from â¹ 12,00,001 to â¹ 15,00,000 (15 lakh) 20% tax
- Income above â¹ 15,00,000 (15 lakh) 30% tax

These rates apply to the new personal income tax regime introduced in the last fiscal year, which is the financial year 2022-23. The new tax regime simplifies the tax structure and reduces tax rates for individuals with income up to â¹ 7 lakh, compared to â¹ 2.2 lakh in the financial year 2013-14.

**Sources:** bs2024_25.pdf p.29; bs2024_25.pdf p.33; bs2024_25(I).pdf p.29; bs2024_25.pdf p.54; bs2024_25.pdf p.32

</details>

<details><summary>Q-E02 — full answer (2589 ms)</summary>

The maximum deduction allowed under Section 80C in a financial year is one hundred and fifty thousand rupees (150,000).

Three eligible investments under Section 80C are:
1. Investments in National Savings Certificates (NSC)
2. Investments in Public Provident Fund (PPF)
3. Investments in Life Insurance Policies

These investments are eligible for deduction under Section 80C, which is applicable for the financial year 2026-2027. The provisions of Section 80C are subject to the provisions of Chapter VIA of the Income-tax Act, 1961.

**Sources:** Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.278; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.471; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.294; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.66; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.292; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.341

</details>

<details><summary>Q-E03 — full answer (1987 ms)</summary>

I could not find this in the provided corpus.

**Sources:** bs2023_24.pdf p.39; Updated-FQAs-on-Interplay&Transitions.pdf p.89; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.764; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.745; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.446; Updated-FQAs-on-Interplay&Transitions.pdf p.87

</details>

<details><summary>Q-E04 — full answer (3112 ms)</summary>

Under the new tax regime for the financial year 2024-25, the standard deduction available to a salaried employee is proposed to be increased from â¹50,000/- to â¹75,000/-.

This information is sourced from page 32 of the document bs2024_25.pdf.

**Sources:** bs2024_25.pdf p.32; bs2024_25.pdf p.54; bs2024_25.pdf p.29; bs2024_25.pdf p.33

</details>

<details><summary>Q-E05 — full answer (3440 ms)</summary>

According to the provisions from the Income-tax Act 1961, for the financial year 2024-25, the tax rate applicable to long-term capital gains on listed equity shares held for more than 12 months is 12.5%. This is stated in the document bs2024_25.pdf, specifically on page 144.

**Sources:** Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.428; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.429; bs2024_25.pdf p.56; bs2024_25.pdf p.30; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.430

</details>

<details><summary>Q-M01 — full answer (12919 ms)</summary>

To compute the tax for the salaried individual under the new tax regime, we need to follow these steps:

1. **Calculate Gross Income**: 
   - Gross Annual Salary: â¹18,00,000
   - EPF Contribution: â¹1,50,000
   - NPS Tier-1 Contribution: â¹25,000
   - Health Insurance Premium: â¹25,000
   - Total Deductions: â¹1,50,000 + â¹25,000 + â¹25,000 = â¹200,000
   - Gross Income: â¹18,00,000 - â¹200,000 = â¹16,00,000

2. **Calculate Taxable Income**:
   - Taxable Income = Gross Income - Standard Deduction
   - Standard Deduction: â¹75,000 (as per the provided corpus)
   - Taxable Income = â¹16,00,000 - â¹75,000 = â¹15,25,000

3. **Calculate Tax**:
   - Tax Rate Structure:
     - 0-3 lakh: Nil
     - 3-7 lakh: 5%
     - 7-10 lakh: 10%
     - 10-12 lakh: 15%
     - 12-15 lakh: 20%
     - Above 15 lakh: 30%
   - Tax Calculation:
     - Income from 0 to 3 lakh: â¹0
     - Income from 3 to 7 lakh: â¹3,00,000 * 5% = â¹15,000
     - Income from 7 to 10 lakh: â¹3,00,000 * 10% = â¹30,000
     - Income from 10 to 12 lakh: â¹2,00,000 * 15% = â¹30,000
     - Income from 12 to 15 lakh: â¹3,00,000 * 20% = â¹60,000
     - Income above 15 lakh: â¹2,00,000 * 30% = â¹60,000
   - Total Tax: â¹15,000 + â¹30,000 + â¹30,000 + â¹60,000 + â¹60,000 = â¹195,000

Therefore, the tax payable by the salaried individual under the new tax regime is â¹1,95,000.

**Sources:** bs2024_25.pdf p.32; bs2024_25.pdf p.33; bs2024_25.pdf p.36; bs2024_25.pdf p.37; bs2024_25.pdf p.9

</details>

<details><summary>Q-M02 — full answer (13951 ms)</summary>

To compute the capital gains tax due, we need to follow the provisions for capital gains taxation as stated in the provided corpus. The corpus does not specify the indexation assumptions, so we will assume the indexation is done using the Cost Inflation Index (CII) as per the provisions.

### Step 1: Determine the Cost of Purchase
The cost of purchase is â¹80,00,000 (Rs 80 lakh).

### Step 2: Determine the Cost of Sale
The cost of sale is â¹1,20,00,000 (Rs 1.2 crore).

### Step 3: Calculate Indexed Cost of Purchase
The indexed cost of purchase is calculated using the Cost Inflation Index (CII) for the year 2018. Let's assume the CII for 2018 is 100 (as it is not provided in the corpus, we will use this for calculation purposes).

Indexed Cost of Purchase = â¹80,00,000 * (CII for 2018 / 100) = â¹80,00,000 * (100 / 100) = â¹80,00,000

### Step 4: Calculate Indexed Cost of Sale
The indexed cost of sale is calculated using the Cost Inflation Index (CII) for the year 2024-25. Let's assume the CII for 2024-25 is 200 (as it is not provided in the corpus, we will use this for calculation purposes).

Indexed Cost of Sale = â¹1,20,00,000 * (CII for 2024-25 / 100) = â¹1,20,00,000 * (200 / 100) = â¹2,40,00,000

### Step 5: Calculate Capital Gains
Capital Gains = Indexed Cost of Sale - Indexed Cost of Purchase = â¹2,40,00,000 - â¹80,00,000 = â¹1,60,00,000

### Step 6: Determine the Applicable Tax Rate
According to the corpus, long-term capital gains on all financial and non-financial assets will attract a tax rate of 12.5%. Since the property is a residential property, it is classified as a non-financial asset.

### Step 7: Calculate the Tax Liability
Tax Liability = Capital Gains * Applicable Tax Rate = â¹1,60,00,000 * 12.5% = â¹1,60,00,000 * 0.125 = â¹20,00,000 (Rs 20 lakh)

### Conclusion:
The capital gains tax due on the sale of the residential property is â¹20,00,000 (Rs 20 lakh).

**Sources:** bs2024_25.pdf p.30; bs2024_25.pdf p.56; bs2024_25.pdf p.58; bs2024_25.pdf p.33

</details>

<details><summary>Q-M03 — full answer (6289 ms)</summary>

For the financial year 2023-24, the proposed changes to Section 206C of the Income-tax Act state that the rate of TCS for foreign remittances for the purpose of education through LRS is proposed to increase from 5% to 20% for remittances in excess of â¹7 lakh. Since the individual is transferring â¹12,00,000, which is in excess of â¹7 lakh, the TCS rate applicable would be 20%.

Additionally, the proposed changes also state that the tax exemption limit for capital gains is proposed to be capped at â¹10 crore. However, this exemption limit does not apply to the TCS rate increase for foreign remittances for education purposes. Therefore, the exemption limit of â¹10 crore does not apply to this specific scenario.

In summary, the TCS rate applicable for the transfer of â¹12,00,000 under the LRS for foreign education in the FY 2023-24 is 20%, and the exemption limit of â¹10 crore does not apply to this scenario.

**Sources:** bs2023_24.pdf p.44; bs2023_24.pdf p.48; bs2023_24.pdf p.52; bs2023_24.pdf p.37

</details>

<details><summary>Q-M04 — full answer (11007 ms)</summary>

Under Section 115BBH of the Income-tax Act, 2023-2024, for taxation of income from transfer of any virtual digital asset, the following provisions apply:

1. **Rate of Taxation**: The income-tax payable shall be the aggregate of the amount of income-tax calculated on the income from transfer of such virtual digital asset at the rate of 30 per cent, and the amount of income-tax with which the assessee would have been chargeable, had the total income of the assessee been reduced by the income referred to in clause (a).

2. **Loss Set-off**: No deduction in respect of any expenditure (other than cost of acquisition, if any) or allowance or set off of any loss shall be allowed to the assessee under any provision of this Act in computing the income referred to in clause (a) of sub-section (1). No set off of loss from transfer of the virtual digital asset computed under clause (a) of sub-section (1) shall be allowed against income computed under any provision of this Act to the assessee and such loss shall not be allowed to be carried forward to succeeding assessment years.

3. **TDS (Tax Deducted at Source) under Section 194S**: Under Section 194S, any person responsible for paying to any resident any sum by way of consideration for transfer of a virtual digital asset, shall, at the time of credit of such sum to the account of the resident or at the time of payment of such sum by any mode, whichever is earlier, deduct an amount equal to one per cent of such sum as income-tax thereon. If the consideration is wholly in kind or in exchange of another virtual digital asset, where there is no part in cash, or if the consideration is partly in cash and partly in kind but the part in cash is not sufficient to meet the liability of deduction of tax in respect of whole of such transfer, the person responsible for paying such consideration shall, before releasing the consideration, ensure that tax required to be deducted has been paid.

These provisions are applicable for the financial year 2023-2024. For the latest provisions, please refer to the latest Income-tax Act, 2026 and its related rules.

**Sources:** bs202223.pdf p.27; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.460; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.748; E-Book-Guidance-Note-Crypto-Asset-Reporting-Obligations.pdf p.188

</details>

<details><summary>Q-M05 — full answer (13997 ms)</summary>

To determine which tax regime (old or new) is lower for the taxpayer, we need to calculate the tax liability under both regimes.

### Old Tax Regime:
Under the old tax regime, the tax rate structure is as follows:
- 0-3 lakh rupees: Nil
- 3-7 lakh rupees: 5%
- 7-10 lakh rupees: 10%
- 10-12 lakh rupees: 15%
- 12-15 lakh rupees: 20%
- Above 15 lakh rupees: 30%

The taxpayer's gross total income is â¹15,00,000, which includes the home-loan interest of â¹2,00,000. The home-loan interest is not deductible under the old regime.

Tax calculation:
1. Income from salary: â¹15,00,000 - â¹2,00,000 = â¹13,00,000
2. Tax on salary: â¹13,00,000 x 20% = â¹2,60,000

Total tax under the old regime: â¹2,60,000

### New Tax Regime:
Under the new tax regime, the tax rate structure is as follows:
- 0-3 lakh rupees: Nil
- 3-7 lakh rupees: 5%
- 7-10 lakh rupees: 10%
- 10-12 lakh rupees: 15%
- 12-15 lakh rupees: 20%
- Above 15 lakh rupees: 30%

The taxpayer's gross total income is â¹15,00,000, which includes the home-loan interest of â¹2,00,000. The home-loan interest is deductible under the new regime.

Tax calculation:
1. Income from salary: â¹15,00,000 - â¹2,00,000 = â¹13,00,000
2. Tax on salary: â¹13,00,000 x 15% = â¹1,95,000

Total tax under the new regime: â¹1,95,000

### Comparison:
- Old regime tax: â¹2,60,000
- New regime tax: â¹1,95,000

The taxpayer's tax liability is lower under the new tax regime, which is â¹1,95,000 compared to â¹2,60,000 under the old regime.

### Conclusion:
The taxpayer is in a lower tax bracket under the new tax regime, which is â¹1,95,000. This is due to the home-loan interest deduction under the new regime, which reduces the taxable income. Therefore, the taxpayer would have a lower tax liability under the new tax regime.

**Sources:** bs2024_25.pdf p.33; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.260; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.93; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.740; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.92; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.601

</details>

<details><summary>Q-C01 — full answer (32860 ms)</summary>

To compute the total tax under both the old and new tax regimes for Mr. A, we need to follow the tax calculation steps for each regime and then compare the results.

### Old Tax Regime

#### Step 1: Calculate Gross Total Income
- Salary: â¹24,00,000
- LTCG: â¹6,00,000
- STCG: â¹2,00,000
- Interest Income: â¹3,00,000
- PPF Investment: â¹2,00,000
- Medical Insurance: â¹75,000

Gross Total Income = â¹24,00,000 + â¹6,00,000 + â¹2,00,000 + â¹3,00,000 + â¹2,00,000 + â¹75,000 = â¹37,75,000

#### Step 2: Calculate Deductions
- Standard Deduction: â¹50,000 (as per old regime)
- Medical Insurance: â¹75,000

Total Deductions = â¹50,000 + â¹75,000 = â¹1,25,000

#### Step 3: Calculate Taxable Income
Taxable Income = â¹37,75,000 - â¹1,25,000 = â¹36,50,000

#### Step 4: Calculate Tax
- 0-3 lakh: Nil
- 3-7 lakh: 5% of â¹36,50,000 - â¹3,00,000 = â¹1,82,500
- 7-10 lakh: 10% of â¹36,50,000 - â¹3,00,000 = â¹2,65,000
- 10-12 lakh: 15% of â¹36,50,000 - â¹3,00,000 = â¹3,97,500
- 12-15 lakh: 20% of â¹36,50,000 - â¹3,00,000 = â¹5,30,000
- Above 15 lakh: 30% of â¹36,50,000 - â¹3,00,000 = â¹9,05,000

Total Tax = â¹1,82,500 + â¹2,65,000 + â¹3,97,500 + â¹5,30,000 + â¹9,05,000 = â¹22,70,000

#### Step 5: Calculate Surcharge and Cess
- Surcharge: 1% of â¹22,70,000 = â¹22,700
- Education Cess: 4% of â¹22,70,000 = â¹8,980

Total Tax (Old Regime) = â¹22,70,000 + â¹22,700 + â¹8,980 = â¹23,81,680

### New Tax Regime

#### Step 1: Calculate Gross Total Income
- Salary: â¹24,00,000
- LTCG: â¹6,00,000
- STCG: â¹2,00,000
- Interest Income: â¹3,00,000
- PPF Investment: â¹2,00,000
- Medical Insurance: â¹75,000

Gross Total Income = â¹24,00,000 + â¹6,00,000 + â¹2,00,000 + â¹3,00,000 + â¹2,00,000 + â¹75,000 = â¹37,75,000

#### Step 2: Calculate Deductions
- Standard Deduction: â¹75,000 (as per new regime)
- Medical Insurance: â¹75,000

Total Deductions = â¹75,000 + â¹75,000 = â¹1,50,000

#### Step 3: Calculate Taxable Income
Taxable Income = â¹37,75,000 - â¹1,50,000 = â¹36,25,000

#### Step 4: Calculate Tax
- 0-3 lakh: Nil
- 3-7 lakh: 5% of â¹36,25,000 - â¹3,00,000 = â¹1,75,000
- 7-10 lakh: 10% of â¹36,25,000 - â¹3,00,000 = â¹2,65,000
- 10-12 lakh: 15% of â¹36,25,000 - â¹3,00,000 = â¹3,93,750
- 12-15 lakh: 20% of â¹36,25,000 - â¹3,00,000 = â¹5,25,000
- Above 15 lakh: 30% of â¹36,25,000 - â¹3,00,000 = â¹9,07,500

Total Tax = â¹1,75,000 + â¹2,65,000 + â¹3,93,750 + â¹5,25,000 + â¹9,07,500 = â¹22,66,250

#### Step 5: Calculate Surcharge and Cess
- Surcharge: 1% of â¹22,66,250 = â¹22,662.50
- Education Cess: 4% of â¹22,66,250 = â¹8,985

Total Tax (New Regime) = â¹22,66,250 + â¹22,662.50 + â¹8,985 = â¹23,77,897.50

### Recommendation
Comparing the total tax under both regimes:
- Old Regime: â¹23,81,680
- New Regime: â¹23,77,897.50

The new tax regime results in a lower total tax of â¹23,77,897.50 compared to the old regime of â¹23,81,680. Therefore, Mr. A should opt for the new tax regime.

### Summary
- **Old Regime Total Tax:** â¹23,81,680
- **New Regime Total Tax:** â¹23,77,897.50

Mr. A should choose the new tax regime for better tax savings.

**Sources:** bs2024_25.pdf p.32; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.86; bs2024_25.pdf p.33; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.310; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.464; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.848

</details>

<details><summary>Q-C02 — full answer (11991 ms)</summary>

For a non-resident FII earning â¹50,00,000 from Indian listed securities in the assessment year (AY) 2024-25, the tax treatment would be governed by the provisions of the Income-tax Act, 2025, as per the FAQs on FIIs Exemption and transition provisions.

### Tax Rate:
Under section 210(1) of the Income-tax Act, 2025, income in respect of securities is taxable at 20%. Therefore, the income of â¹50,00,000 would be taxed at 20%, resulting in a tax liability of:
\[ \text{Tax Liability} = â¹50,00,000 \times 20\% = â¹10,00,000 \]

### Documentation Needed:
To claim the benefit of the exemption under the proposed ordinance, the FII would need to provide the following documentation:

1. **Proof of FII Status**: The FII must provide a valid notification from the Central Government specifying them as a Foreign Institutional Investor (FII). This notification was issued on 22.01.2014, as mentioned in the FAQs.

2. **Details of Securities**: The FII must provide details of the securities held and the income earned from these securities. This includes the names of the securities, the number of units or shares, and the period for which the securities were held.

3. **Proof of Investment**: The FII should provide proof of investment, such as investment certificates or transaction records, to substantiate the investment in Indian listed securities.

4. **Proof of Non-Resident Status**: The FII must provide proof of their non-resident status, such as a valid passport, residence certificate, or any other document issued by the relevant government authority that confirms their non-resident status.

5. **Proof of Compliance with Taxation Provisions**: The FII should provide any other necessary documentation as required by the tax authorities to ensure compliance with the tax provisions applicable to FIIs.

### Conclusion:
The income of â¹50,00,000 earned by the non-resident FII from Indian listed securities in the AY 2024-25 would be taxed at 20% under section 210(1) of the Income-tax Act, 2025. The FII must provide the required documentation to claim the exemption under the proposed ordinance.

**Sources:** FAQs-on-BIS-Exemption.pdf p.1; FAQs-on-BIS-Exemption.pdf p.2; Updated-FQAs-on-Interplay&Transitions.pdf p.91

</details>

<details><summary>Q-C03 — full answer (16054 ms)</summary>

To determine the residential status for the individual with an income of â¹40,00,000, we need to apply the provisions of the Income-tax Act, 1961, as applicable to the assessment year 2026-27.

### Residential Status for Resident Individual

For residential status, the individual must meet one of the following conditions:
1. Stay in India for 182 days or more in the relevant tax year.
2. Stay in India for 60 days or more in the relevant tax year coupled with 365 days or more in the preceding four years.

Given the individual's income is â¹40,00,000, which exceeds the threshold of â¹12,00,000 for the previous year, the individual is considered a resident individual under the provisions of the Income-tax Act, 1961.

The individual visited India for 130 days across two visits in the year. Let's evaluate the residential status:

- **Stay in India for 182 days or more in the relevant tax year:** The individual did not meet this condition as they stayed for 130 days.
- **Stay in India for 60 days or more in the relevant tax year coupled with 365 days or more in the preceding four years:** The individual stayed for 130 days in the relevant tax year and must also have stayed for 365 days or more in the preceding four years. Since the individual's income is â¹40,00,000, they are considered a resident individual.

### Residential Status for Not Onerously Resident (NOR) Individual

For residential status, the individual must meet one of the following conditions:
1. Stay in India for 182 days or more in the relevant tax year.
2. Stay in India for 60 days or more in the relevant tax year coupled with 365 days or more in the preceding four years.
3. Special relaxation for individuals who have been non-resident in India in nine out of the ten previous years preceding that year, or have during the seven previous years preceding that year been in India for a period of, or periods amounting in all to, seven hundred and twenty-nine days or less.

Given the individual's income is â¹40,00,000, they are not considered a resident individual as their income exceeds â¹12,00,000 for the previous year. Therefore, the individual is considered a Not Onerously Resident (NOR) individual.

### Tax Consequence for Not Onerously Resident (NOR) Individual

For a NOR individual, the income is taxed at the rate applicable to non-residents. The tax rate for non-residents is 30% (without surcharge or cess).

Given the income of â¹40,00,000, the tax liability would be:
\[ \text{Tax Liability} = â¹40,00,000 \times 0.30 = â¹12,00,000 \]

### Summary

- **Resident Individual:** The individual is considered a resident individual as their income exceeds â¹12,00,000 for the previous year.
- **Not Onerously Resident (NOR) Individual:** The individual is considered a NOR individual and is taxed at the rate applicable to non-residents, which is 30% (without surcharge or cess).

Thus, the tax consequence for the NOR individual is â¹12,00,000.

**Sources:** Updated-FQAs-on-Interplay&Transitions.pdf p.89; Updated-FQAs-on-Interplay&Transitions.pdf p.87; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.22; Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf p.688

</details>

## VIVO demo integration notes

| Demo file | Question ID | Transcript captured? | Answer audible? | Follow-up handled? | Note |
|-----------|-------------|----------------------|-----------------|--------------------|------|
| demo/vivo_1.mp3 | Q-E01 | Yes | Yes | n/a | Single-turn spoken Q and A |
| demo/vivo_2.mp3 | Q-E02 | Yes | Yes | n/a | Single-turn spoken Q and A |
| demo/vivo_3.mp3 | Q-E05 | Yes | Yes | n/a | Single-turn spoken Q and A |
| demo/vivo_4.mp3 | Q-M01 | Yes | Yes | n/a | Single-turn spoken Q and A |
| demo/vivo_5.mp3 | Q-M04 | Yes | Yes | n/a | Single-turn spoken Q and A |
| demo/vivo_6.mp3 | Q-C01 | Yes | Yes | n/a | Single-turn spoken Q and A |
| demo/vivo_7.mp3 | Q-C03 | Yes | Yes | Yes | Multi-turn: Q-C03 then a follow-up on ROR tax liability |
