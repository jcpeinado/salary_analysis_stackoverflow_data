import json
from pathlib import Path
p=Path('notebooks/peinado_1012953314_assignment1.ipynb')
n=json.loads(p.read_text(encoding='utf-8'))
def get(i): return ''.join(n['cells'][i]['source'])
def put(i,s): n['cells'][i]['source']=s.splitlines(True)
put(4,get(4)+'''

### Study Population and Sample Selection Criteria
The intended study concerns workforce participation. Two researcher-defined sample selection
criteria operationalize the analytical scope and engineering judgment: exclude respondents
explicitly classified as retired, and exclude recorded ages greater than 80 years. Age 80
remains eligible. The upper age limit defines the research population; it does not establish
that older respondents are erroneous or statistical outliers. These eligibility decisions
precede all descriptive and inferential analyses and are distinct from satisfaction-scale
cleaning and the separate salary-IQR sensitivity analyses.

Inspection of the supplied CSV identifies four `Employment` categories: `Employed`,
`Independent contractor, freelancer, or self-employed`, `Student`, and `Not employed`.
There is no retired category in that field. Two rows instead have `DevType = Retired`,
although both also have `Employment = Employed`. We prioritize the explicit retired
classification for exclusion, without guessing which conflicting field is correct.
`EmploymentAddl` contains semicolon-delimited activities, including `Transitioning to
retirement (gradually reducing work hours)`; transition is not completed retirement and
is not itself grounds for exclusion. Exact, case-normalized retired tokens are checked
across all three fields, rather than matching the substring "retir".

Excluding retirement does **not** establish that everyone remaining is employed. The
employment categories and supplementary paid-work responses support a self-reported
employment indicator, but students and those marked not employed remain under these two
specified criteria. We report these categories and the indicator as an audit, without imposing
an additional employed-only filter. Findings therefore concern the selected salary-reporting
survey respondents, not a verified population of actively employed workers. Employment timing,
conflicting classifications, and the original cleaning history cannot be independently verified.

Missing ages are retained for analyses that do not require age because they do not establish
an age above 80; they are excluded from the age plot. Thus the age ceiling is verified only
for respondents with recorded ages. The sample-flow table reports each criterion separately,
their overlap, sequential removals, and the final sample without double-counting.
''')
s=get(5).replace('survey = pd.read_csv(data_path)','source_survey = pd.read_csv(data_path)\nsurvey = source_survey.copy()').replace("required = ['Age',", "required = ['Employment', 'EmploymentAddl', 'Age',")
pos=s.index('schema =')
s=s[:pos]+'''# Eligibility selection precedes every descriptive statistic, plot and test.
def has_exact_token(series, label):
    return series.fillna('').astype(str).str.split(';').map(
        lambda tokens: label.casefold() in {t.strip().casefold() for t in tokens})

retired_by_field = pd.DataFrame({column: has_exact_token(source_survey[column], 'Retired')
                               for column in ['Employment', 'EmploymentAddl', 'DevType']})
retired_mask = retired_by_field.any(axis=1)
over_80_mask = source_survey.Age.gt(80)
selection_mask = ~(retired_mask | over_80_mask)
survey = source_survey.loc[selection_mask].copy()
selected_frame_hash = pd.util.hash_pandas_object(survey, index=True).to_numpy().copy()
original_n = len(source_survey)
retired_n = int(retired_mask.sum())
over_80_n = int(over_80_mask.sum())
overlap_n = int((retired_mask & over_80_mask).sum())
age_excluded_after_retirement = int((~retired_mask & over_80_mask).sum())
selection_flow = pd.DataFrame({
    'Stage': ['Original supplied sample', 'Exclude retired', 'Exclude age >80 after retirement',
              'Final analysis sample'],
    'Excluded at stage': [0, retired_n, age_excluded_after_retirement, 0],
    'Remaining': [original_n, original_n-retired_n, len(survey), len(survey)]
})
display(retired_by_field.sum().rename('Explicit retired classifications').to_frame())
display(source_survey.Employment.value_counts(dropna=False).rename('Original employment categories').to_frame())
display(source_survey.EmploymentAddl.dropna().str.split(';').explode().str.strip()
        .value_counts().rename('Supplementary activity tokens (multiple per respondent)').to_frame())
display(selection_flow)
employment_audit = survey.Employment.value_counts(dropna=False).rename('Selected respondents').to_frame()
display(employment_audit)
reported_employment = survey.Employment.isin(['Employed', 'Independent contractor, freelancer, or self-employed'])
reported_paid_activity = survey.EmploymentAddl.fillna('').str.split(';').map(
    lambda tokens: any(t.strip().startswith('Engaged in paid work (') for t in tokens))
employment_indicator_n = int((reported_employment | reported_paid_activity).sum())
narrative(f'**Sample selection.** Original n={original_n:,}; retired exclusions={retired_n:,}; '
          f'age >80 exclusions in the original sample={over_80_n:,}; overlap={overlap_n:,}; '
          f'additional age exclusions after retirement={age_excluded_after_retirement:,}; '
          f'final n={len(survey):,}. The selected sample retains '
          f'{int(survey.Age.eq(80).sum()):,} respondents aged exactly 80 and '
          f'{int(survey.Age.isna().sum()):,} with missing age. '
          f'{employment_indicator_n:,} report employment/self-employment or supplementary paid work; '
          f'{len(survey)-employment_indicator_n:,} lack that affirmative indicator. '
          'This indicator is descriptive, not an additional eligibility restriction or external verification.')

''' +s[pos:]
s=s.replace('**Results.** The source has','**Results.** The selected analysis sample has')
put(5,s)
s=get(6).replace('Keep the source DataFrame unchanged and select only the variables','Keep the source DataFrame unchanged; apply the population criteria above, then select only the variables').replace('retain every nonmissing numeric value','retain every eligible nonmissing numeric value').replace('Do not let age or satisfaction issues exclude otherwise usable salary records in Q2 or Q3.','The retirement and age-ceiling criteria apply to every analysis, including Q2 and Q3.\nOther age diagnostics and satisfaction validity rules do not trigger additional salary exclusions.')
put(6,s)
put(10,get(10).replace('All positive finite\nsalaries','All positive finite\nsalaries within the selected population'))
put(14,get(14).replace('no age-based or satisfaction-based removal is carried into Q2 or Q3.','the retirement and age-ceiling criteria apply throughout Q2 and Q3, while satisfaction\ncleaning and the remaining age diagnostic flags do not cause additional salary removals.'))
put(32,get(32).replace('Retain all positive finite salaries','Within the selected population, retain all positive finite salaries'))
put(45,get(45).replace('- **Confounding:**','- **Population selection:** retirement and age >80 exclusions define analytical scope, not\n  data errors or outliers. Missing age and inconsistent employment classifications limit\n  verification; retained respondents are not necessarily actively employed.\n- **Confounding:**'))
s=get(48).replace('hash_pandas_object(survey, index=True).to_numpy(), original_frame_hash','hash_pandas_object(source_survey, index=True).to_numpy(), original_frame_hash')
s+='''
np.testing.assert_array_equal(pd.util.hash_pandas_object(survey, index=True).to_numpy(), selected_frame_hash)
assert len(survey) == original_n-retired_n-over_80_n+overlap_n
assert not survey.Age.gt(80).any()
assert not retired_by_field.loc[survey.index].any(axis=None)
assert source_survey.index[source_survey.Age.eq(80) & ~retired_mask].isin(survey.index).all()
assert source_survey.index[source_survey.Age.isna() & ~retired_mask].isin(survey.index).all()
for analysis_frame in [satisfaction_data, title_salary_data, age_salary_data, q2_data, q3_data]:
    assert analysis_frame.index.isin(survey.index).all()
assert not pd.Series([79, 80, 81, np.nan]).gt(80).iloc[1]
assert pd.Series([79, 80, 81, np.nan]).gt(80).tolist() == [False, False, True, False]
assert has_exact_token(pd.Series(['Retired', 'Employed; Retired',
    'Transitioning to retirement (gradually reducing work hours)', None]), 'Retired').tolist() == [True, True, False, False]
print('PASS: selection counts, overlap, age-80 boundary, missing-age policy, retirement tokens, all analysis subsets.')
'''
put(48,s)
put(49,get(49).replace('for the Future PDF Report','for the Written Report').replace('no report or dashboard is generated.','the accompanying written report must use this executed version.'))
put(50,get(50).replace('**Dataset and preparation.**', '''**Study Population and Sample Selection Criteria.** Original sample: {original_n:,}.
Excluded as retired: {retired_n:,}; aged >80: {over_80_n:,}; overlap: {overlap_n:,}.
Final sample: {len(survey):,}. These are researcher-defined scope decisions based on
engineering judgment, not cleaning or outlier removal. Age 80 remains eligible.
Missing ages are retained outside the age plot. Explicit retirement is recorded in DevType,
with conflicting Employment classifications. Excluding retirement does not establish an
employed-only population; students and respondents marked not employed remain.

**Dataset and preparation.**'''))
put(51,get(51)+'''

**Sample-selection revision (October 14, 2026).** At the researcher's request, explicit retired
classifications and ages greater than 80 are excluded before all analyses. Employment and
supplementary activity categories were inspected, including the inconsistent retired records.
The original CSV is unchanged. All statistics, bootstrap replications, intervals and figures
are recalculated from the selected sample; the revised written report supersedes earlier
reports and dashboard outputs for this population. The execution outputs and final integrity
checks document this revision. Colab execution remains unverified.
''')
for c in n['cells']:
    if c['cell_type']=='code': c['outputs']=[]; c['execution_count']=None
p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('Updated notebook')
