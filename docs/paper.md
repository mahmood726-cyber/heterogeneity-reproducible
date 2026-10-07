# Heterogeneity in meta-analysis in the browser: a tool validated against the R package metafor

**Mahmood Ahmad**¹ [AUTHOR TO COMPLETE: ORCID, corresponding-author e-mail]

¹ [AUTHOR TO COMPLETE: affiliation]

## Abstract

**Background:** Between-study heterogeneity shapes every random-effects meta-analysis, but its estimators, intervals and diagnostics are usually computed in R or Stata. We built a browser tool needing no installation and validated it against R.

**Methods:** The allmeta heterogeneity app estimates the between-study variance τ² by eight methods and reports Q, I², Q-profile confidence intervals, the pooled estimate with normal and Hartung–Knapp intervals, the prediction interval, leave-one-out results and a Baujat plot. We compared it with the R package metafor on every model without moderators fitted in the examples of the dataset package metadat: 88 meta-analyses from 49 datasets (4 to 160 studies), each with all eight estimators.

**Results:** All 131,781 checks passed: every number agreed with metafor within 10⁻⁹, and the same 28 analyses were refused.

**Conclusions:** The app reproduces metafor's heterogeneity analyses in a browser.

**Keywords:** meta-analysis; heterogeneity; between-study variance; prediction interval; Hartung–Knapp; metafor; software validation; reproducibility

## Introduction

Random-effects meta-analysis needs an estimate of the between-study variance τ², usually reported with Q and I² [1]. Many estimators exist [2–5]; the R package metafor implements them, with intervals and diagnostics [6,7]. We describe the allmeta heterogeneity app, one of a collection of offline browser tools for evidence synthesis [8], validated against metafor.

## Methods

### Implementation

The app is a static JavaScript page (https://mahmood726-cyber.github.io/allmeta/heterogeneity/). It takes one row per study: label, estimate and standard error.

**Estimation.** τ² by Paule–Mandel (default), restricted maximum likelihood (REML), maximum likelihood, empirical Bayes [9], Sidik–Jonkman, Hedges, Hunter–Schmidt or DerSimonian–Laird [2–5]; DerSimonian–Laird needs 10 or more studies, otherwise the app uses Paule–Mandel and says so.

**Outputs.** Q and its p-value; I² from Q [1]; Q-profile 95% confidence intervals for τ² and I² [10]; the pooled estimate with a normal 95% interval and a Hartung–Knapp–Sidik–Jonkman interval (t, k − 1 df, scaling factor floored at 1) [11,12]; the 95% prediction interval [13]; leave-one-out results; a Baujat plot [14]; and export.

### Operation

A user (Figure 1):

1. pastes the studies or loads an example;
2. chooses the τ² estimator;
3. reads the summary statistics;
4. inspects the Baujat plot and leave-one-out table;
5. sees DerSimonian–Laird refused for fewer than 10 studies;
6. exports the results.

### Validation

We validated allmeta (commit 7cb5975). The corpus is every model without moderators fitted in the help-page examples of metadat 1.6-0 [15], with the data each model used: 88 meta-analyses from 49 datasets [16–63] (2,241 study rows; 4 to 160 studies; 23 effect measures; dat.colditz1994 repeats dat.bcg). The two pages that exceeded our time limit fit only multilevel models.

The app itself ran each meta-analysis in a headless browser with all eight estimators (704 analyses); metafor 5.2-1 [7] analysed the same data with tight convergence controls.

A check is one reported number compared with metafor's: per meta-analysis, 9 (studies read, Q, df, p-value, I², and the limits of both Q-profile intervals); per estimator, 1 refusal check and, if offered, 9 (τ², estimate, standard error, and the limits of the normal, Hartung–Knapp and prediction intervals) plus 7 per study (leave-one-out estimate, interval limits, I² and τ²; Baujat coordinates). Agreement required identical refusals and differences within 10⁻⁹: relative for estimates, intervals, τ² and Q; absolute for I² and p-values.

This validation found faults in earlier versions, all corrected (allmeta PR #82): an imprecise t quantile in the Hartung–Knapp and prediction intervals; REML and maximum-likelihood τ² converged only to an absolute 10⁻¹²; a Baujat influence axis that did not follow its definition; and four wrong variances and a wrong year in the built-in BCG dataset.

One command (`python reproduce.py`) runs everything in a Docker image (R 4.6.0, Node 24.15.0); continuous integration repeats it on Linux, Windows, macOS and Docker.

## Results

**Agreement.** All 131,781 checks passed (Table 2, Figure 3). The app and metafor treated the same 28 analyses as refused (DerSimonian–Laird with fewer than 10 studies) and agreed on the other 676: every difference was below 5 × 10⁻¹⁰, and below 10⁻¹⁰ for estimates and intervals (Table 1). All 120,720 displayed numbers matched the computed values.

With metafor's default convergence settings, τ² moved by up to 10⁻⁴ (Table 4).

**Worked example.** The BCG vaccine trials (13 studies [22]) gave Q = 152.2 (12 df), I² 92.1% (95% CI 81.9% to 97.7%) and τ² from 0.228 (Hunter–Schmidt) to 0.346 (Sidik–Jonkman). With REML, the risk ratio was 0.49 (Hartung–Knapp 95% CI 0.33 to 0.73; prediction interval 0.14 to 1.76), and Hart and Sutherland's trial was the most influential (Figure 2).

**Reproducibility.** Every number was reproduced on all four platforms.

## Discussion

Limitations:

1. there are no moderators or multilevel models;
2. input is one estimate and standard error per study;
3. I² is computed from Q whichever τ² estimator is chosen;
4. the corpus consists of published teaching examples.

## Conclusions

A browser tool can reproduce standard heterogeneity analyses on published datasets.

## Data availability

**Underlying data:** built from the examples of the R package metadat 1.6-0 [15]; original sources in Table 1.

**Extended data:** app, code, corpus, expected values, figures and screenshots: Zenodo, [AUTHOR TO COMPLETE: DOI on release] [64]. Licence: MIT.

## Software availability

- **Source code available from:** https://github.com/mahmood726-cyber/allmeta (`heterogeneity/`, `shared/ma-core.js`, `shared/heterogeneity-ci.js`); validated version: commit 7cb5975429531791d1879e80cf5c05f765e82c21
- **Archived source code at time of publication:** Zenodo. Heterogeneity in meta-analysis in the browser: a tool validated against the R package metafor (v1.0.0). [AUTHOR TO COMPLETE: DOI] [64]
- **Licence:** MIT
- **Reproduction:** one click via GitHub Codespaces, a fork's "Run workflow" button, or `python reproduce.py`; verified runs: https://mahmood726-cyber.github.io/heterogeneity-reproducible/

## Competing interests

The author develops allmeta. [AUTHOR TO CONFIRM: no other competing interests.]

## Grant information

[AUTHOR TO COMPLETE]

## Acknowledgements

[AUTHOR TO COMPLETE.] Claude (Anthropic), an AI assistant, helped write the software, the analysis code and the draft of this manuscript. The author checked all code, results and text.

## References

1. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Stat Med. 2002;21(11):1539–58. https://doi.org/10.1002/sim.1186
2. DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177–88. https://doi.org/10.1016/0197-2456(86)90046-2
3. Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. J Educ Behav Stat. 2005;30(3):261–93. https://doi.org/10.3102/10769986030003261
4. Paule RC, Mandel J. Consensus values and weighting factors. J Res Natl Bur Stand. 1982;87(5):377–85. https://doi.org/10.6028/jres.087.022
5. Sidik K, Jonkman JN. Simple heterogeneity variance estimation for meta-analysis. J R Stat Soc Ser C Appl Stat. 2005;54(2):367–84. https://doi.org/10.1111/j.1467-9876.2005.00489.x
6. Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw. 2010;36(3):1–48. https://doi.org/10.18637/jss.v036.i03
7. Viechtbauer W. metafor: Meta-Analysis Package for R. R package version 5.2-1 [software]. CRAN; 2026. https://doi.org/10.32614/CRAN.package.metafor
8. Ahmad M. allmeta — open browser-only tools for evidence synthesis. Version [AUTHOR TO COMPLETE: release containing the validated commit] [software]. Zenodo; 2026. https://doi.org/[AUTHOR TO COMPLETE]
9. Morris CN. Parametric empirical Bayes inference: theory and applications. J Am Stat Assoc. 1983;78(381):47–55. https://doi.org/10.1080/01621459.1983.10477920
10. Viechtbauer W. Confidence intervals for the amount of heterogeneity in meta-analysis. Stat Med. 2007;26(1):37–52. https://doi.org/10.1002/sim.2514
11. Hartung J, Knapp G. A refined method for the meta-analysis of controlled clinical trials with binary outcome. Stat Med. 2001;20(24):3875–89. https://doi.org/10.1002/sim.1009
12. Röver C, Knapp G, Friede T. Hartung-Knapp-Sidik-Jonkman approach and its modification for random-effects meta-analysis with few studies. BMC Med Res Methodol. 2015;15:99. https://doi.org/10.1186/s12874-015-0091-1
13. Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A Stat Soc. 2009;172(1):137–59. https://doi.org/10.1111/j.1467-985X.2008.00552.x
14. Baujat B, Mahé C, Pignon JP, Hill C. A graphical method for exploring heterogeneity in meta-analyses: application to a meta-analysis of 65 trials. Stat Med. 2002;21(18):2641–52. https://doi.org/10.1002/sim.1221
15. Viechtbauer W, White T, Noble D, Senior A, Hamilton WK. metadat: Meta-Analysis Datasets. R package version 1.6-0 [software]. CRAN; 2026. https://doi.org/10.32614/CRAN.package.metadat
16. Aloe AM, Thompson CG. The synthesis of partial effect sizes. J Soc Soc Work Res. 2013;4(4):390–405. https://doi.org/10.5243/jsswr.2013.24
17. Axfors C, Schmitt A, Janiaud P, van 't Hooft J, Moher D, Goodman S, et al. Hydroxychloroquine and chloroquine for survival in COVID-19: an international collaborative meta-analysis of randomized trials [preprint]. OSF Preprints; 2021. https://doi.org/10.17605/OSF.IO/QESV4
18. Bangert-Drowns RL, Hurley MM, Wilkinson B. The effects of school-based writing-to-learn interventions on academic achievement: a meta-analysis. Rev Educ Res. 2004;74(1):29–58. https://doi.org/10.3102/00346543074001029
19. Bartoš F, Sarafoglou A, Godmann HR, Sahrani A, Leunk DK, Gui PY, et al. Fair coins tend to land on the same side they started: evidence from 350,757 flips [preprint]. arXiv:2310.04153; 2023. https://doi.org/10.48550/arXiv.2310.04153
20. Baskerville NB, Liddy C, Hogg W. Systematic review and meta-analysis of practice facilitation within primary care settings. Ann Fam Med. 2012;10(1):63–74. https://doi.org/10.1370/afm.1312
21. Bauer HW, Rahlfs VW, Lauener PA, Bleßmann GSS. Prevention of recurrent urinary tract infections with immuno-active E. coli fractions: a meta-analysis of five placebo-controlled double-blind studies. Int J Antimicrob Agents. 2002;19(6):451–6. https://doi.org/10.1016/s0924-8579(02)00106-1
22. Colditz GA, Brewer TF, Berkey CS, Wilson ME, Burdick E, Fineberg HV, et al. Efficacy of BCG vaccine in the prevention of tuberculosis: meta-analysis of the published literature. JAMA. 1994;271(9):698–702. https://doi.org/10.1001/jama.1994.03510330076038
23. Begg CB, Pilote L. A model for incorporating historical controls into a meta-analysis. Biometrics. 1991;47(3):899–906. https://doi.org/10.2307/2532647
24. Bonett DG. Varying coefficient meta-analytic methods for alpha reliability. Psychol Methods. 2010;15(4):368–85. https://doi.org/10.1037/a0020142
25. Bourassa DC, McManus IC, Bryden MP. Handedness and eye-dominance: a meta-analysis of their relationship. Laterality. 1996;1(1):5–34. https://doi.org/10.1080/713754206
26. Chiarito M, Sanz-Sánchez J, Cannata F, Cao D, Sturla M, Panico C, et al. Monotherapy with a P2Y12 inhibitor or aspirin for secondary prevention in patients with established atherosclerosis: a systematic review and meta-analysis. Lancet. 2020;395(10235):1487–95. https://doi.org/10.1016/s0140-6736(20)30315-9
27. Cohen PA. Student ratings of instruction and student achievement: a meta-analysis of multisection validity studies. Rev Educ Res. 1981;51(3):281–309. https://doi.org/10.3102/00346543051003281
28. Credé M, Roch SG, Kieszczynka UM. Class attendance in college: a meta-analytic review of the relationship of class attendance with grades and student characteristics. Rev Educ Res. 2010;80(2):272–95. https://doi.org/10.3102/0034654310362998
29. Crisafulli S, Sultana J, Fontana A, Salvo F, Messina S, Trifirò G. Global epidemiology of Duchenne muscular dystrophy: an updated systematic review and meta-analysis. Orphanet J Rare Dis. 2020;15:141. https://doi.org/10.1186/s13023-020-01430-8
30. Curtis PS, Wang X. A meta-analysis of elevated CO2 effects on woody plant mass, form, and physiology. Oecologia. 1998;113(3):299–313. https://doi.org/10.1007/s004420050381
31. D'Agostino RB Sr, Weintraub M, Russell HK, Stepanians M, D'Agostino RB Jr, Cantilena LR Jr, et al. The effectiveness of antihistamines in reducing the severity of runny nose and sneezing: a meta-analysis. Clin Pharmacol Ther. 1998;64(6):579–96. https://doi.org/10.1016/S0009-9236(98)90049-2
32. D'Amico R, Pifferi S, Torri V, Brazzi L, Parmelli E, Liberati A. Antibiotic prophylaxis to reduce respiratory tract infections and mortality in adults receiving intensive care. Cochrane Database Syst Rev. 2009;(4):CD000022. https://doi.org/10.1002/14651858.CD000022.pub3
33. de Bruin M, Viechtbauer W, Hospers HJ, Schaalma HP, Kok G. Standard care quality determines treatment outcomes in control groups of HAART-adherence intervention studies: implications for the interpretation and comparison of intervention effects. Health Psychol. 2009;28(6):668–74. https://doi.org/10.1037/a0015989
34. Demir E, Öz S, Aral N, Gürsoy F. A reliability generalization meta-analysis of the Mother-to-Infant Bonding Scale. Psychol Rep. 2024;127(1):447–64. https://doi.org/10.1177/00332941221114413
35. Dorn SD, Kaptchuk TJ, Park JB, Nguyen LT, Canenguez K, Nam BH, et al. A meta-analysis of the placebo response in complementary and alternative medicine trials of irritable bowel syndrome. Neurogastroenterol Motil. 2007;19(8):630–7. https://doi.org/10.1111/j.1365-2982.2007.00937.x
36. Frank B, Rigas SH, Bermejo JL, Wiestler M, Wagner K, Hemminki K, et al. The CASP8 -652 6N del promoter polymorphism and breast cancer risk: a multicenter study. Breast Cancer Res Treat. 2008;111(1):139–44. https://doi.org/10.1007/s10549-007-9752-z
37. Gibson PG, Powell H, Wilson A, Abramson MJ, Haywood P, Bauman A, et al. Self-management education and regular practitioner review for adults with asthma. Cochrane Database Syst Rev. 2002;(3):CD001117. https://doi.org/10.1002/14651858.CD001117
38. Hackshaw AK, Law MR, Wald NJ. The accumulated evidence on lung cancer and environmental tobacco smoke. BMJ. 1997;315(7114):980–8. https://doi.org/10.1136/bmj.315.7114.980
39. Hannum ME, Ramirez VA, Lipson SJ, Herriman RD, Toskala AK, Lin C, et al. Objective sensory testing methods reveal a higher prevalence of olfactory loss in COVID-19-positive patients compared to subjective methods: a systematic review and meta-analysis. Chem Senses. 2020;45(9):865–74. https://doi.org/10.1093/chemse/bjaa064
40. Hart RG, Benavente O, McBride R, Pearce LA. Antithrombotic therapy to prevent stroke in patients with atrial fibrillation: a meta-analysis. Ann Intern Med. 1999;131(7):492–501. https://doi.org/10.7326/0003-4819-131-7-199910050-00003
41. Hine LK, Laird N, Hewitt P, Chalmers TC. Meta-analytic evidence against prophylactic use of lidocaine in acute myocardial infarction. Arch Intern Med. 1989;149(12):2694–8. https://doi.org/10.1001/archinte.1989.00390120056011
42. Kearon C, Julian JA, Math M, Newman TE, Ginsberg JS. Noninvasive diagnosis of deep venous thrombosis. Ann Intern Med. 1998;128(8):663–77. https://doi.org/10.7326/0003-4819-128-8-199804150-00011
43. Knapp F, Viechtbauer W, Leonhart R, Nitschke K, Kaller CP. Planning performance in schizophrenia patients: a meta-analysis of the influence of task difficulty and clinical and sociodemographic variables. Psychol Med. 2017;47(11):2002–16. https://doi.org/10.1017/S0033291717000459
44. Konstantopoulos S. Fixed effects and variance components estimation in three-level meta-analysis. Res Synth Methods. 2011;2(1):61–76. https://doi.org/10.1002/jrsm.35
45. Landenberger NA, Lipsey MW. The positive effects of cognitive-behavioral programs for offenders: a meta-analysis of factors associated with effective treatment. J Exp Criminol. 2005;1(4):451–76. https://doi.org/10.1007/s11292-005-3541-7
46. Laopaiboon M, Panpanich R, Swa Mya K. Azithromycin for acute lower respiratory tract infections. Cochrane Database Syst Rev. 2015;(3):CD001954. https://doi.org/10.1002/14651858.CD001954.pub4
47. Lee A, Done ML. Stimulation of the wrist acupuncture point P6 for preventing postoperative nausea and vomiting. Cochrane Database Syst Rev. 2004;(3):CD003281. https://doi.org/10.1002/14651858.CD003281.pub2
48. Lehmann GK, Elliot AJ, Calin-Jageman RJ. Meta-analysis of the effect of red on perceived attractiveness. Evol Psychol. 2018;16(4):1474704918802412. https://doi.org/10.1177/1474704918802412
49. Li J, Zhang Q, Zhang M, Egger M. Intravenous magnesium for acute myocardial infarction. Cochrane Database Syst Rev. 2007;(2):CD002755. https://doi.org/10.1002/14651858.CD002755.pub2
50. Linde K, Berner M, Egger M, Mulrow C. St John's wort for depression: meta-analysis of randomised controlled trials. Br J Psychiatry. 2005;186(2):99–107. https://doi.org/10.1192/bjp.186.2.99
51. McDaniel MA, Whetzel DL, Schmidt FL, Maurer SD. The validity of employment interviews: a comprehensive review and meta-analysis. J Appl Psychol. 1994;79(4):599–616. https://doi.org/10.1037/0021-9010.79.4.599
52. Michael RB, Newman EJ, Vuorre M, Cumming G, Garry M. On the (non)persuasive power of a brain image. Psychon Bull Rev. 2013;20(4):720–5. https://doi.org/10.3758/s13423-013-0391-6
53. Molloy GJ, O'Carroll RE, Ferguson E. Conscientiousness and medication adherence: a meta-analysis. Ann Behav Med. 2014;47(1):92–101. https://doi.org/10.1007/s12160-013-9524-4
54. Niel-Weise BS, Stijnen T, van den Broek PJ. Anti-infective-treated central venous catheters: a systematic review of randomized controlled trials. Intensive Care Med. 2007;33(12):2058–68. https://doi.org/10.1007/s00134-007-0897-3
55. Niel-Weise BS, Stijnen T, van den Broek PJ. Anti-infective-treated central venous catheters for total parenteral nutrition or chemotherapy: a systematic review. J Hosp Infect. 2008;69(2):114–23. https://doi.org/10.1016/j.jhin.2008.02.020
56. Nissen SE, Wolski K. Effect of rosiglitazone on the risk of myocardial infarction and death from cardiovascular causes. N Engl J Med. 2007;356(24):2457–71. https://doi.org/10.1056/NEJMoa072761
57. Normand SLT. Meta-analysis: formulating, evaluating, combining, and reporting. Stat Med. 1999;18(3):321–59. https://doi.org/10.1002/(SICI)1097-0258(19990215)18:3<321::AID-SIM28>3.0.CO;2-P
58. Pignon JP, Bourhis J, Domenge C, Designé L. Chemotherapy added to locoregional treatment for head and neck squamous-cell carcinoma: three meta-analyses of updated individual data. Lancet. 2000;355(9208):949–55. https://doi.org/10.1016/S0140-6736(00)90011-4
59. Zhou XH, Brizendine EJ, Pritz MB. Methods for combining rates from several studies. Stat Med. 1999;18(5):557–66. https://doi.org/10.1002/(SICI)1097-0258(19990315)18:5<557::AID-SIM53>3.0.CO;2-F
60. Raudenbush SW. Magnitude of teacher expectancy effects on pupil IQ as a function of the credibility of expectancy induction: a synthesis of findings from 18 experiments. J Educ Psychol. 1984;76(1):85–97. https://doi.org/10.1037/0022-0663.76.1.85
61. Riley RD, Sutton AJ, Abrams KR, Lambert PC. Sensitivity analyses allowed more appropriate and reliable meta-analysis conclusions for multiple outcomes when missing data was present. J Clin Epidemiol. 2004;57(9):911–24. https://doi.org/10.1016/j.jclinepi.2004.01.018
62. Van Howe RS. Circumcision and HIV infection: review of the literature and meta-analysis. Int J STD AIDS. 1999;10(1):8–16. https://doi.org/10.1258/0956462991913015
63. Viechtbauer W. Model checking in meta-analysis. In: Schmid CH, Stijnen T, White IR, editors. Handbook of meta-analysis. Boca Raton (FL): CRC Press; 2021. p. 219–54. https://doi.org/10.1201/9781315119403
64. Ahmad M. Heterogeneity in meta-analysis in the browser: a tool validated against the R package metafor. Version 1.0.0 [software]. Zenodo; 2026. https://doi.org/[AUTHOR TO COMPLETE: DOI on release]

## Figure and table legends

**Figure 1.** Using the app, step by step (BCG vaccine trials, log risk ratios; Google Chrome, light theme; high-resolution captures cropped to the relevant panels).
(1) Data entry, one row per study.
(2) The τ² estimator (REML).
(3) Summary: Q, I² and the τ² intervals, τ² by three estimators and the τ² used, the pooled estimate with normal and Hartung–Knapp intervals, and the prediction interval.
(4) Baujat plot (A) and leave-one-out table (B).
(5) DerSimonian–Laird requested for the app's 8-study example: the note (A) and the Paule–Mandel results shown (B).
(6) Export of results (A) and of the plot and session, with a check in R in the browser (B).
Panels 4–6 are labelled composites of regions of one page; panels 1–3 are single crops.

**Figure 2.** Worked example, BCG vaccine: (A) risk ratio with Hartung–Knapp 95% confidence interval and prediction interval for each τ² estimator; (B) Baujat plot (REML). The app (blue) is drawn over metafor.

**Figure 3.** App versus metafor: largest difference in each meta-analysis for every reported quantity, over all eight estimators.

**Table 1.** Agreement with metafor by dataset: original source, meta-analyses, effect measures, number of studies, and largest relative and absolute difference.

**Table 2.** Largest difference from metafor for each reported quantity, with its tolerance and number of checks.

**Table 3.** (Extended data) Every meta-analysis and estimator, with its largest difference.

**Table 4.** τ² from metafor with its default convergence settings versus tight settings, by estimator.
