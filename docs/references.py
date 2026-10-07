"""Every reference of the paper, in citation order (Vancouver; every DOI as https://doi.org/..., checked to resolve).

METHODS: references 1-15 (cited in the text in this order). DATASETS: the original source of every dataset in the corpus,
references 16 onward, in Table 1 order (dataset name order); a dataset that repeats another's data cites that source.
ARCHIVE: the last reference. docs/render_references.py writes the list into docs/paper.md; analysis/make_outputs.py puts each
dataset's reference number into Table 1.
"""
METHODS = [
    "Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Stat Med. 2002;21(11):1539–58. https://doi.org/10.1002/sim.1186",
    "DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177–88. https://doi.org/10.1016/0197-2456(86)90046-2",
    "Viechtbauer W. Bias and efficiency of meta-analytic variance estimators in the random-effects model. J Educ Behav Stat. 2005;30(3):261–93. https://doi.org/10.3102/10769986030003261",
    "Paule RC, Mandel J. Consensus values and weighting factors. J Res Natl Bur Stand. 1982;87(5):377–85. https://doi.org/10.6028/jres.087.022",
    "Sidik K, Jonkman JN. Simple heterogeneity variance estimation for meta-analysis. J R Stat Soc Ser C Appl Stat. 2005;54(2):367–84. https://doi.org/10.1111/j.1467-9876.2005.00489.x",
    "Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw. 2010;36(3):1–48. https://doi.org/10.18637/jss.v036.i03",
    "Viechtbauer W. metafor: Meta-Analysis Package for R. R package version 5.2-1 [software]. CRAN; 2026. https://doi.org/10.32614/CRAN.package.metafor",
    "ALLMETA",
    "Morris CN. Parametric empirical Bayes inference: theory and applications. J Am Stat Assoc. 1983;78(381):47–55. https://doi.org/10.1080/01621459.1983.10477920",
    "Viechtbauer W. Confidence intervals for the amount of heterogeneity in meta-analysis. Stat Med. 2007;26(1):37–52. https://doi.org/10.1002/sim.2514",
    "Hartung J, Knapp G. A refined method for the meta-analysis of controlled clinical trials with binary outcome. Stat Med. 2001;20(24):3875–89. https://doi.org/10.1002/sim.1009",
    "Röver C, Knapp G, Friede T. Hartung-Knapp-Sidik-Jonkman approach and its modification for random-effects meta-analysis with few studies. BMC Med Res Methodol. 2015;15:99. https://doi.org/10.1186/s12874-015-0091-1",
    "Higgins JPT, Thompson SG, Spiegelhalter DJ. A re-evaluation of random-effects meta-analysis. J R Stat Soc Ser A Stat Soc. 2009;172(1):137–59. https://doi.org/10.1111/j.1467-985X.2008.00552.x",
    "Baujat B, Mahé C, Pignon JP, Hill C. A graphical method for exploring heterogeneity in meta-analyses: application to a meta-analysis of 65 trials. Stat Med. 2002;21(18):2641–52. https://doi.org/10.1002/sim.1221",
    "Viechtbauer W, White T, Noble D, Senior A, Hamilton WK. metadat: Meta-Analysis Datasets. R package version 1.6-0 [software]. CRAN; 2026. https://doi.org/10.32614/CRAN.package.metadat",
]
# allmeta: the release that contains the validated commit (to be completed; v1.2.0 predates allmeta PR #82)
ALLMETA = "Ahmad M. allmeta — open browser-only tools for evidence synthesis. Version [AUTHOR TO COMPLETE: release containing the validated commit] [software]. Zenodo; 2026. https://doi.org/[AUTHOR TO COMPLETE]"
ARCHIVE = "Ahmad M. Heterogeneity in meta-analysis in the browser: a tool validated against the R package metafor. Version 1.0.0 [software]. Zenodo; 2026. https://doi.org/[AUTHOR TO COMPLETE: DOI on release]"

DATASETS = {
    "dat.aloe2013": "Aloe AM, Thompson CG. The synthesis of partial effect sizes. J Soc Soc Work Res. 2013;4(4):390–405. https://doi.org/10.5243/jsswr.2013.24",
    "dat.axfors2021": "Axfors C, Schmitt A, Janiaud P, van 't Hooft J, Moher D, Goodman S, et al. Hydroxychloroquine and chloroquine for survival in COVID-19: an international collaborative meta-analysis of randomized trials [preprint]. OSF Preprints; 2021. https://doi.org/10.17605/OSF.IO/QESV4",
    "dat.bangertdrowns2004": "Bangert-Drowns RL, Hurley MM, Wilkinson B. The effects of school-based writing-to-learn interventions on academic achievement: a meta-analysis. Rev Educ Res. 2004;74(1):29–58. https://doi.org/10.3102/00346543074001029",
    "dat.bartos2023": "Bartoš F, Sarafoglou A, Godmann HR, Sahrani A, Leunk DK, Gui PY, et al. Fair coins tend to land on the same side they started: evidence from 350,757 flips [preprint]. arXiv:2310.04153; 2023. https://doi.org/10.48550/arXiv.2310.04153",
    "dat.baskerville2012": "Baskerville NB, Liddy C, Hogg W. Systematic review and meta-analysis of practice facilitation within primary care settings. Ann Fam Med. 2012;10(1):63–74. https://doi.org/10.1370/afm.1312",
    "dat.bauer2002": "Bauer HW, Rahlfs VW, Lauener PA, Bleßmann GSS. Prevention of recurrent urinary tract infections with immuno-active E. coli fractions: a meta-analysis of five placebo-controlled double-blind studies. Int J Antimicrob Agents. 2002;19(6):451–6. https://doi.org/10.1016/s0924-8579(02)00106-1",
    "dat.bcg": "Colditz GA, Brewer TF, Berkey CS, Wilson ME, Burdick E, Fineberg HV, et al. Efficacy of BCG vaccine in the prevention of tuberculosis: meta-analysis of the published literature. JAMA. 1994;271(9):698–702. https://doi.org/10.1001/jama.1994.03510330076038",
    "dat.begg1989": "Begg CB, Pilote L. A model for incorporating historical controls into a meta-analysis. Biometrics. 1991;47(3):899–906. https://doi.org/10.2307/2532647",
    "dat.bonett2010": "Bonett DG. Varying coefficient meta-analytic methods for alpha reliability. Psychol Methods. 2010;15(4):368–85. https://doi.org/10.1037/a0020142",
    "dat.bourassa1996": "Bourassa DC, McManus IC, Bryden MP. Handedness and eye-dominance: a meta-analysis of their relationship. Laterality. 1996;1(1):5–34. https://doi.org/10.1080/713754206",
    "dat.chiarito2020": "Chiarito M, Sanz-Sánchez J, Cannata F, Cao D, Sturla M, Panico C, et al. Monotherapy with a P2Y12 inhibitor or aspirin for secondary prevention in patients with established atherosclerosis: a systematic review and meta-analysis. Lancet. 2020;395(10235):1487–95. https://doi.org/10.1016/s0140-6736(20)30315-9",
    "dat.cohen1981": "Cohen PA. Student ratings of instruction and student achievement: a meta-analysis of multisection validity studies. Rev Educ Res. 1981;51(3):281–309. https://doi.org/10.3102/00346543051003281",
    "dat.crede2010": "Credé M, Roch SG, Kieszczynka UM. Class attendance in college: a meta-analytic review of the relationship of class attendance with grades and student characteristics. Rev Educ Res. 2010;80(2):272–95. https://doi.org/10.3102/0034654310362998",
    "dat.crisafulli2020": "Crisafulli S, Sultana J, Fontana A, Salvo F, Messina S, Trifirò G. Global epidemiology of Duchenne muscular dystrophy: an updated systematic review and meta-analysis. Orphanet J Rare Dis. 2020;15:141. https://doi.org/10.1186/s13023-020-01430-8",
    "dat.curtis1998": "Curtis PS, Wang X. A meta-analysis of elevated CO2 effects on woody plant mass, form, and physiology. Oecologia. 1998;113(3):299–313. https://doi.org/10.1007/s004420050381",
    "dat.dagostino1998": "D'Agostino RB Sr, Weintraub M, Russell HK, Stepanians M, D'Agostino RB Jr, Cantilena LR Jr, et al. The effectiveness of antihistamines in reducing the severity of runny nose and sneezing: a meta-analysis. Clin Pharmacol Ther. 1998;64(6):579–96. https://doi.org/10.1016/S0009-9236(98)90049-2",
    "dat.damico2009": "D'Amico R, Pifferi S, Torri V, Brazzi L, Parmelli E, Liberati A. Antibiotic prophylaxis to reduce respiratory tract infections and mortality in adults receiving intensive care. Cochrane Database Syst Rev. 2009;(4):CD000022. https://doi.org/10.1002/14651858.CD000022.pub3",
    "dat.debruin2009": "de Bruin M, Viechtbauer W, Hospers HJ, Schaalma HP, Kok G. Standard care quality determines treatment outcomes in control groups of HAART-adherence intervention studies: implications for the interpretation and comparison of intervention effects. Health Psychol. 2009;28(6):668–74. https://doi.org/10.1037/a0015989",
    "dat.demir2022": "Demir E, Öz S, Aral N, Gürsoy F. A reliability generalization meta-analysis of the Mother-to-Infant Bonding Scale. Psychol Rep. 2024;127(1):447–64. https://doi.org/10.1177/00332941221114413",
    "dat.dorn2007": "Dorn SD, Kaptchuk TJ, Park JB, Nguyen LT, Canenguez K, Nam BH, et al. A meta-analysis of the placebo response in complementary and alternative medicine trials of irritable bowel syndrome. Neurogastroenterol Motil. 2007;19(8):630–7. https://doi.org/10.1111/j.1365-2982.2007.00937.x",
    "dat.frank2008": "Frank B, Rigas SH, Bermejo JL, Wiestler M, Wagner K, Hemminki K, et al. The CASP8 -652 6N del promoter polymorphism and breast cancer risk: a multicenter study. Breast Cancer Res Treat. 2008;111(1):139–44. https://doi.org/10.1007/s10549-007-9752-z",
    "dat.gibson2002": "Gibson PG, Powell H, Wilson A, Abramson MJ, Haywood P, Bauman A, et al. Self-management education and regular practitioner review for adults with asthma. Cochrane Database Syst Rev. 2002;(3):CD001117. https://doi.org/10.1002/14651858.CD001117",
    "dat.hackshaw1998": "Hackshaw AK, Law MR, Wald NJ. The accumulated evidence on lung cancer and environmental tobacco smoke. BMJ. 1997;315(7114):980–8. https://doi.org/10.1136/bmj.315.7114.980",
    "dat.hannum2020": "Hannum ME, Ramirez VA, Lipson SJ, Herriman RD, Toskala AK, Lin C, et al. Objective sensory testing methods reveal a higher prevalence of olfactory loss in COVID-19-positive patients compared to subjective methods: a systematic review and meta-analysis. Chem Senses. 2020;45(9):865–74. https://doi.org/10.1093/chemse/bjaa064",
    "dat.hart1999": "Hart RG, Benavente O, McBride R, Pearce LA. Antithrombotic therapy to prevent stroke in patients with atrial fibrillation: a meta-analysis. Ann Intern Med. 1999;131(7):492–501. https://doi.org/10.7326/0003-4819-131-7-199910050-00003",
    "dat.hine1989": "Hine LK, Laird N, Hewitt P, Chalmers TC. Meta-analytic evidence against prophylactic use of lidocaine in acute myocardial infarction. Arch Intern Med. 1989;149(12):2694–8. https://doi.org/10.1001/archinte.1989.00390120056011",
    "dat.kearon1998": "Kearon C, Julian JA, Math M, Newman TE, Ginsberg JS. Noninvasive diagnosis of deep venous thrombosis. Ann Intern Med. 1998;128(8):663–77. https://doi.org/10.7326/0003-4819-128-8-199804150-00011",
    "dat.knapp2017": "Knapp F, Viechtbauer W, Leonhart R, Nitschke K, Kaller CP. Planning performance in schizophrenia patients: a meta-analysis of the influence of task difficulty and clinical and sociodemographic variables. Psychol Med. 2017;47(11):2002–16. https://doi.org/10.1017/S0033291717000459",
    "dat.konstantopoulos2011": "Konstantopoulos S. Fixed effects and variance components estimation in three-level meta-analysis. Res Synth Methods. 2011;2(1):61–76. https://doi.org/10.1002/jrsm.35",
    "dat.landenberger2005": "Landenberger NA, Lipsey MW. The positive effects of cognitive-behavioral programs for offenders: a meta-analysis of factors associated with effective treatment. J Exp Criminol. 2005;1(4):451–76. https://doi.org/10.1007/s11292-005-3541-7",
    "dat.laopaiboon2015": "Laopaiboon M, Panpanich R, Swa Mya K. Azithromycin for acute lower respiratory tract infections. Cochrane Database Syst Rev. 2015;(3):CD001954. https://doi.org/10.1002/14651858.CD001954.pub4",
    "dat.lee2004": "Lee A, Done ML. Stimulation of the wrist acupuncture point P6 for preventing postoperative nausea and vomiting. Cochrane Database Syst Rev. 2004;(3):CD003281. https://doi.org/10.1002/14651858.CD003281.pub2",
    "dat.lehmann2018": "Lehmann GK, Elliot AJ, Calin-Jageman RJ. Meta-analysis of the effect of red on perceived attractiveness. Evol Psychol. 2018;16(4):1474704918802412. https://doi.org/10.1177/1474704918802412",
    "dat.li2007": "Li J, Zhang Q, Zhang M, Egger M. Intravenous magnesium for acute myocardial infarction. Cochrane Database Syst Rev. 2007;(2):CD002755. https://doi.org/10.1002/14651858.CD002755.pub2",
    "dat.linde2005": "Linde K, Berner M, Egger M, Mulrow C. St John's wort for depression: meta-analysis of randomised controlled trials. Br J Psychiatry. 2005;186(2):99–107. https://doi.org/10.1192/bjp.186.2.99",
    "dat.mcdaniel1994": "McDaniel MA, Whetzel DL, Schmidt FL, Maurer SD. The validity of employment interviews: a comprehensive review and meta-analysis. J Appl Psychol. 1994;79(4):599–616. https://doi.org/10.1037/0021-9010.79.4.599",
    "dat.michael2013": "Michael RB, Newman EJ, Vuorre M, Cumming G, Garry M. On the (non)persuasive power of a brain image. Psychon Bull Rev. 2013;20(4):720–5. https://doi.org/10.3758/s13423-013-0391-6",
    "dat.molloy2014": "Molloy GJ, O'Carroll RE, Ferguson E. Conscientiousness and medication adherence: a meta-analysis. Ann Behav Med. 2014;47(1):92–101. https://doi.org/10.1007/s12160-013-9524-4",
    "dat.nielweise2007": "Niel-Weise BS, Stijnen T, van den Broek PJ. Anti-infective-treated central venous catheters: a systematic review of randomized controlled trials. Intensive Care Med. 2007;33(12):2058–68. https://doi.org/10.1007/s00134-007-0897-3",
    "dat.nielweise2008": "Niel-Weise BS, Stijnen T, van den Broek PJ. Anti-infective-treated central venous catheters for total parenteral nutrition or chemotherapy: a systematic review. J Hosp Infect. 2008;69(2):114–23. https://doi.org/10.1016/j.jhin.2008.02.020",
    "dat.nissen2007": "Nissen SE, Wolski K. Effect of rosiglitazone on the risk of myocardial infarction and death from cardiovascular causes. N Engl J Med. 2007;356(24):2457–71. https://doi.org/10.1056/NEJMoa072761",
    "dat.normand1999": "Normand SLT. Meta-analysis: formulating, evaluating, combining, and reporting. Stat Med. 1999;18(3):321–59. https://doi.org/10.1002/(SICI)1097-0258(19990215)18:3<321::AID-SIM28>3.0.CO;2-P",
    "dat.pignon2000": "Pignon JP, Bourhis J, Domenge C, Designé L. Chemotherapy added to locoregional treatment for head and neck squamous-cell carcinoma: three meta-analyses of updated individual data. Lancet. 2000;355(9208):949–55. https://doi.org/10.1016/S0140-6736(00)90011-4",
    "dat.pritz1997": "Zhou XH, Brizendine EJ, Pritz MB. Methods for combining rates from several studies. Stat Med. 1999;18(5):557–66. https://doi.org/10.1002/(SICI)1097-0258(19990315)18:5<557::AID-SIM53>3.0.CO;2-F",
    "dat.raudenbush1985": "Raudenbush SW. Magnitude of teacher expectancy effects on pupil IQ as a function of the credibility of expectancy induction: a synthesis of findings from 18 experiments. J Educ Psychol. 1984;76(1):85–97. https://doi.org/10.1037/0022-0663.76.1.85",
    "dat.riley2003": "Riley RD, Sutton AJ, Abrams KR, Lambert PC. Sensitivity analyses allowed more appropriate and reliable meta-analysis conclusions for multiple outcomes when missing data was present. J Clin Epidemiol. 2004;57(9):911–24. https://doi.org/10.1016/j.jclinepi.2004.01.018",
    "dat.vanhowe1999": "Van Howe RS. Circumcision and HIV infection: review of the literature and meta-analysis. Int J STD AIDS. 1999;10(1):8–16. https://doi.org/10.1258/0956462991913015",
    "dat.viechtbauer2021": "Viechtbauer W. Model checking in meta-analysis. In: Schmid CH, Stijnen T, White IR, editors. Handbook of meta-analysis. Boca Raton (FL): CRC Press; 2021. p. 219–54. https://doi.org/10.1201/9781315119403",
}
# datasets that share a source with another (cite once): dat.colditz1994 = dat.bcg; dat.hine1989 data are also in Normand 1999
SAME_AS = {"dat.colditz1994": "dat.bcg"}


def numbering(datasets):
    """Reference number of each dataset (in the given order); a dataset in SAME_AS cites the other's number."""
    num, n = {}, len(METHODS) + 1
    for d in datasets:
        if d in SAME_AS:
            continue
        num[d] = n
        n += 1
    for d, other in SAME_AS.items():
        if d in datasets:
            num[d] = num[other]
    return num, n
