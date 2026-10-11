"""Documentary evidence freeze. Reads existing results; never imports/runs scientific executors."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import csv
import hashlib
import json
import shutil
import subprocess
import zipfile
import numpy as np
import pandas as pd

BASE = Path('/Users/fede/Documents/Codex/2026-10-08/files-pasted-by-the-user-diagn')
REPO = BASE/'work/tb-global-refit-phase1'
OUT = BASE/'outputs/TB_SEIT_EVIDENCE_FREEZE_2026-10-10'
P1 = BASE/'outputs/TB_SEIT_global_refit_phase1_2026-10-08'
P2 = BASE/'outputs/TB_SEIT_rolling_ordinary_phase2_2026-10-08'
A3 = BASE/'outputs/TB_SEIT_PHASE3_CONFORMITY_AUDIT_2026-10-10'
P3 = A3/'existing_phase3_evidence'
A2 = BASE/'outputs/PHASE2_ZIP_VERIFICATION_2026-10-10'
COMMIT = 'b3ad21bb059eb5357742693a4d5072107dc0df63'
CHECKS = []
SOURCES = {}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return json.loads(Path(p).read_text())
def table(p): return pd.read_csv(p, float_precision='round_trip')
def dump(p, obj): Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
def check(name, value, detail=None):
    CHECKS.append(dict(check=name, status='PASS' if bool(value) else 'FAIL', detail=detail))
    if not value: raise RuntimeError('Evidence freeze discrepancy: '+name)
def eq(a,b): return bool(np.allclose(a,b,rtol=2e-12,atol=1e-8))
def git(path, *args):
    return subprocess.check_output(['git','-C',str(path),*args], text=True)
def metrics(obs,pred):
    e=np.asarray(pred)-np.asarray(obs)
    return [float(np.sqrt(np.mean(e*e))), float(np.mean(abs(e))), float(np.mean(e))]
def files(root): return sorted(p for p in Path(root).rglob('*') if p.is_file())
def inventory(root): return {str(p.relative_to(root)):sha(p) for p in files(root)}
def check_manifest(root):
    manifest=load(root/'artifact_manifest.json')
    return all(sha(root/p)==h for p,h in manifest.items()) and set(manifest)==set(inventory(root))-{'artifact_manifest.json'}
def copy_file(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    assert sha(src)==sha(dest)
    SOURCES[str(dest.relative_to(OUT))]={'source_absolute_path':str(src),'sha256':sha(src),'bytes':src.stat().st_size}
def copy_tree(src, dest):
    for p in files(src): copy_file(p, dest/p.relative_to(src))
def write_csv(path, rows):
    pd.DataFrame(rows).to_csv(path,index=False,float_format='%.17g')

def validate_sources():
    for name,root in [('phase1',P1),('phase2',P2),('phase2_verification',A2),('phase3_conformity',A3)]:
        check(name+'_complete_existing_manifest',check_manifest(root))
    check('phase3_existing_25_files_match_audit_hashes',inventory(P3)==load(A3/'source_sha256_at_audit.json'))
    for name,source in [('phase1',P1),('phase2',P2),('phase3',P3)]:
        folder={'phase1':'observation_operator_refit_phase1_2026-10-08','phase2':'observation_operator_rolling_origin_phase2_2026-10-08','phase3':'observation_operator_phase3_identifiability_2026-10-08'}[name]
        audit=REPO/'audits'/folder
        check(name+'_delivered_bytes_match_worktree',all(sha(audit/p.relative_to(source))==sha(p) for p in files(source)))
    zip2=BASE/'outputs/TB_SEIT_rolling_ordinary_phase2_2026-10-08.zip'
    check('phase2_original_ZIP_hash',sha(zip2)=='90ac75b21112be90ac4f9eba8658ef5203334535371b35011b519c167215818b')
    with zipfile.ZipFile(zip2) as z:
        check('phase2_original_ZIP_CRC',z.testzip() is None)
    check('phase3_adopted_protocol_hash',sha(P3/'PROTOCOL_DECISION.md')=='58d4bed36871f9c63cd93e4c199d5c9890f006ccaf96ede85362480dee91469b')
    check('phase1_prior_verification_pass',load(P1/'verification.json')['status']=='PASS')
    a2=load(A2/'verification_report.json')
    check('43_phase2_prior_checks_pass',a2['status']=='PASS' and len(a2['checks'])==43 and all(c['status']=='PASS' for c in a2['checks']))
    a3=table(A3/'conformity_checks.csv')
    check('49_phase3_prior_checks_pass',len(a3)==49 and a3.status.eq('PASS').all())
    check('phase3_accepted_limited_verdict',load(A3/'SUMMARY.json')['verdict']=='PHASE3_PASS_WITH_DOCUMENTED_LIMITATIONS')
    tracked=load(P3/'tracked_before_sha256.json')
    check('239_tracked_hashes_unchanged',len(tracked)==239 and all(sha(REPO/p)==h for p,h in tracked.items()))
    check('repository_exact_commit',git(REPO,'rev-parse','HEAD').strip()==COMMIT)
    check('Git_only_preserved_untracked_audits',git(REPO,'status','--porcelain=v1')=='?? audits/\n')
    return tracked

def validate_results():
    r1=P1/'tb_global_refit_phase1/results_global_primary'
    params=table(r1/'global_refit_parameters.csv').set_index('model')
    m1=table(r1/'global_refit_metrics.csv')
    report1=load(r1/'phase1_report.json')
    check('phase1_two_independent_successful_primary_fits',len(params)==2 and all(r['success'] for r in report1['parameters']) and all(r['seed']==20260815 for r in report1['parameters']))
    prediction1={m:table(r1/(m+'_predictions.csv')) for m in ['fractional','integer']}
    for model,df in prediction1.items():
        check('phase1_'+model+'_264_months_correct_splits',len(df)==264 and df.date.nunique()==264 and df.groupby('split').size().to_dict()=={'calibration':240,'validation_open_loop':24} and df.date.iloc[0]=='2001-01-01' and df.date.iloc[-1]=='2022-12-01')
        for split,sub in df.groupby('split'):
            row=m1[(m1.model==model)&(m1.split==split)].iloc[0]
            check('phase1_'+model+'_'+split+'_saved_metrics',len(sub)==row.n and eq(metrics(sub.observed,sub.predicted),row[['rmse','mae','bias']].to_numpy(float)) and eq(sub.residual,sub.predicted-sub.observed))
    check('phase1_S1_contract_static',all(s in (P1/'tb_global_refit_phase1/run_global_refit.py').read_text() for s in ['solver.y[:, 1]','0.5 * sigma * h * (e[:-1] + e[1:])','reshape(n_months, steps).sum(axis=1)']))
    pred=table(P2/'rolling_origin_predictions.csv')
    models={'fractional','integer','persistence','seasonal_naive_12','SARIMA'}
    check('phase2_780_predictions_exact_five_models',len(pred)==780 and set(pred.model)==models and pred.groupby('model').size().eq(156).all())
    check('phase2_common_support_13x12',not pred.duplicated(['model','origin','horizon']).any() and pred.groupby(['origin','horizon']).model.nunique().eq(5).all() and pred.origin.nunique()==13 and set(pred.horizon)==set(range(1,13)) and pred.origin.min()=='2020-12-01' and pred.origin.max()=='2021-12-01')
    dates=pd.to_datetime(pred.origin)
    expected=pd.PeriodIndex(dates,freq='M')+pred.horizon.to_numpy(int)
    check('phase2_targets_match_origin_plus_horizon',np.array_equal(expected.to_timestamp().strftime('%Y-%m-%d'),pred.target_date))
    check('phase2_finite_shared_observations',np.isfinite(pred[['observed','predicted','residual']]).all().all() and pred.groupby(['origin','horizon'])['observed'].nunique().eq(1).all() and eq(pred.residual,pred.predicted-pred.observed))
    check('phase2_SEIT_S1_operator_only',pred[pred.model.isin(['fractional','integer'])].observation_operator.eq('ordinary_composite_trapezoid').all())
    fits=table(P2/'fit_states.csv')
    check('phase2_26_successful_fits_single_seed',len(fits)==26 and fits.success.all() and fits.seed.eq(20260815).all())
    for model in ['fractional','integer']:
        first=fits[(fits.model==model)&(fits.origin=='2020-12-01')].iloc[0]
        check('phase2_first_origin_'+model+'_same_global_parameters',eq(first[['beta','sigma','gamma','d','alpha']].to_numpy(float),params.loc[model,['beta','sigma','gamma','d','alpha']].to_numpy(float)))
    hist=table(REPO/'outputs/forecasting/rolling_origin_predictions.csv')
    base=pred[~pred.model.isin(['fractional','integer'])].sort_values(['model','origin','horizon'])
    oldbase=hist[~hist.model.isin(['fractional','integer'])].sort_values(['model','origin','horizon'])
    check('phase2_468_baselines_preserved_exactly',len(base)==len(oldbase)==468 and np.array_equal(base.predicted.to_numpy(),oldbase.predicted.to_numpy()) and np.array_equal(base[['model','origin','horizon','target_date','observed']].to_numpy(),oldbase[['model','origin','horizon','target_date','observed']].to_numpy()))
    met=table(P2/'metrics_by_horizon.csv').rename(columns={'RMSE':'rmse','MAE':'mae'})
    check('phase2_60_metric_rows',len(met)==60)
    for row in met.itertuples():
        sub=pred[(pred.model==row.model)&(pred.horizon==row.horizon)]
        assert len(sub)==13 and eq(metrics(sub.observed,sub.predicted),[row.rmse,row.mae,row.bias])
    check('phase2_all_RMSE_MAE_bias_reconstructed',True)
    skill=table(P2/'skill_by_horizon.csv')
    for row in skill.itertuples():
        own=met[(met.model==row.model)&(met.horizon==row.horizon)].iloc[0][row.metric.lower()]
        ref=met[(met.model==row.baseline)&(met.horizon==row.horizon)].iloc[0][row.metric.lower()]
        assert eq([row.error_model,row.error_baseline,row.skill],[own,ref,1-own/ref])
    check('phase2_168_skills_exact_formula',len(skill)==168)
    summaries=table(P2/'horizon_summary.csv')
    for row in summaries.itertuples():
        sub=skill[(skill.model==row.model)&(skill.baseline==row.baseline)&(skill.metric==row.metric)].sort_values('horizon')
        positive=sub[sub.skill>0].horizon.to_list()
        relaxed=max(positive,default=0)
        strict=0
        for h in range(1,13):
            if h not in positive: break
            strict=h
        assert (row.H_relax,row.H_strict)==(relaxed,strict)
    check('phase2_14_Hrelax_Hstrict_exact_definitions',len(summaries)==14)
    fskill=skill[skill.model=='fractional']
    for baseline,positive in [('integer',list(range(1,13))),('persistence',[]),('SARIMA',[]),('seasonal_naive_12',list(range(1,6)))]:
        check('fractional_skill_signs_'+baseline,all(fskill[(fskill.baseline==baseline)&(fskill.metric==metric)&(fskill.skill>0)].horizon.to_list()==positive for metric in ['RMSE','MAE']))
    check('phase2_fractional_negative_bias_all_horizons',met[met.model=='fractional'].bias.lt(0).all())
    check('phase2_alpha_lower_boundary_all_origins',fits[fits.model=='fractional'].alpha.between(.5,.51).all())
    final2=load(P2/'final_verification.json')
    check('phase2_prior_leakage_resolution_and_skill_gates',final2['training_hashes_initial_states_constants_verified'] and final2['all_numeric_gates_pass'] and final2['all_skill_signs_and_horizon_summaries_stable_across_steps'])
    pool=table(P3/'solution_pool.csv')
    primary=pool[pool.solution_id=='primary_20260815'].iloc[0]
    check('phase3_primary_exact_global_reuse',np.array_equal(primary[['beta','sigma','gamma','d','alpha']].to_numpy(float),params.loc['fractional',['beta','sigma','gamma','d','alpha']].to_numpy(float)))
    check('phase3_complete_47_pool_no_selection',len(pool)==47 and pool.source.value_counts().to_dict()=={'reoptimized_profile':42,'diagnostic_multiseed':4,'reused_phase1_primary':1})
    alpha=table(P3/'alpha_profile_comparison.csv')
    fixed=table(P3/'alpha_fixed_section.csv')
    profiles=table(P3/'profile_objective.csv')
    check('phase3_21_fixed_and_21_reoptimized_alpha',len(alpha)==len(fixed)==21 and profiles.profile_parameter.eq('alpha').sum()==21 and np.array_equal(alpha.alpha,fixed.alpha) and alpha.alpha.min()==.5 and alpha.alpha.max()==1.)
    check('phase3_fixed_others_constant',all(fixed[k].eq(primary[k]).all() for k in ['beta','sigma','gamma','d']))
    limit=float(primary.calibration_rmse)*1.01
    admitted=pool.calibration_rmse.le(limit)
    check('phase3_exact_1pct_membership_32',admitted.sum()==32 and np.array_equal(admitted,pool.admissible_1pct))
    check('phase3_membership_unchanged_fine_step',np.array_equal(admitted,pool.admissible_1pct_hquarter_primary_reference))
    r0=pool.beta*pool.sigma/((pool.sigma+1/888)*(pool.gamma+1/888+pool.d))
    check('phase3_mu_and_R0_identity_existing_table',eq(r0,pool.R0_reference))
    env=table(P3/'R0_practical_envelopes.csv').set_index('set')
    near=env.loc['NEAR_EQUIVALENT_1_PCT']
    check('phase3_envelope_finite_admitted_set',near.n==32 and eq([near.minimum,near.maximum],[pool[admitted].R0_reference.min(),pool[admitted].R0_reference.max()]) and near.n_below_1==32 and near.n_above_1==0)
    stable=table(P3/'dfe_stability.csv')
    check('phase3_DFE_32_stable_autonomous_scope',stable[stable.admissible_1pct].classification.eq('ASYMPTOTICALLY_STABLE_AUTONOMOUS_REFERENCE').all() and stable.theory_scope.eq('AUTONOMOUS_CONSTANT_N_REFERENCE_ONLY').all())
    check('phase3_full_pool_44_stable_3_unstable',stable.classification.str.startswith('ASYMPTOTICALLY_STABLE').sum()==44 and stable.classification.str.startswith('UNSTABLE').sum()==3)
    old=table(REPO/'results_canonical/03_R0_stability/table_R0_stability_summary.csv').iloc[0]
    check('historical_25_unstable_reference_confirmed',old.n_solutions==25 and old.DFE_unstable==25 and old.DFE_stable==0 and eq([old.R0_min,old.R0_max],[1.154172396476935,1.1892187917630623]))
    oldh=table(P2/'historical_horizon_comparison.csv')
    check('seasonal_horizon_replacement_7_to_5',all((oldh[(oldh.model=='fractional')&(oldh.baseline=='seasonal_naive_12')][k]==v).all() for k,v in [('H_relax_ordinary',5),('H_strict_ordinary',5),('H_relax_historical',7),('H_strict_historical',7)]))
    return dict(params=params,m1=m1,pred1=prediction1,pred=pred,met=met,skill=skill,summaries=summaries,pool=pool,alpha=alpha,env=env,old=old,threshold=limit,primary=primary)

def create_figures(data):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
    target=OUT/'figures'; target.mkdir()
    definitions=[]
    def save(fig,name,title,sources,scope):
        fig.tight_layout()
        fig.savefig(target/(name+'.png'))
        fig.savefig(target/(name+'.pdf'),metadata={'Title':title,'Subject':'Existing frozen tables; no new scientific experiment'})
        plt.close(fig)
        definitions.append(dict(figure_id=name,title=title,files=[str((target/(name+ext)).relative_to(OUT)) for ext in ['.png','.pdf']],source_tables=sources,scope=scope))
    fig,ax=plt.subplots(figsize=(9,4))
    df=data['pred1']['fractional']; dates=pd.to_datetime(df.date)
    ax.plot(dates,df.observed,color='black',lw=1,label='Observado')
    for model,col in [('fractional','#087e8b'),('integer','#bd5139')]: ax.plot(dates,data['pred1'][model].predicted,color=col,lw=1.2,label=model)
    ax.axvline(pd.Timestamp('2021-01-01'),ls='--',color='gray'); ax.set(ylabel='Incidencia mensual S1',title='Fase 1: ajuste global y validación open-loop de origen único'); ax.legend(ncol=3)
    save(fig,'F1_global_open_loop','Global S1 and single-origin validation',['phase1/tb_global_refit_phase1/results_global_primary/fractional_predictions.csv','phase1/tb_global_refit_phase1/results_global_primary/integer_predictions.csv'],'One 24-month validation origin; descriptive, not baseline superiority')
    fig,ax=plt.subplots(figsize=(8,4.3))
    for model,sub in data['met'].groupby('model'): ax.plot(sub.horizon,sub.rmse,marker='o',ms=3,label=model)
    ax.set(xlabel='Horizonte (meses)',ylabel='RMSE (casos/mes)',title='Fase 2: 13 predicciones por horizonte y modelo',xticks=range(1,13)); ax.legend(fontsize=8,ncol=2)
    save(fig,'F2_rolling_RMSE','Rolling-origin RMSE',['phase2/metrics_by_horizon.csv'],'13 origins × 12 horizons; no cross-horizon pooling')
    fig,axes=plt.subplots(1,2,figsize=(10,4),sharex=True)
    for ax,metric in zip(axes,['RMSE','MAE']):
        sub=data['skill'][(data['skill'].model=='fractional')&(data['skill'].metric==metric)]
        for baseline,rows in sub.groupby('baseline'): ax.plot(rows.horizon,rows.skill,marker='o',ms=3,label=baseline)
        ax.axhline(0,color='black',lw=.7); ax.set(title=metric,xlabel='Horizonte (meses)',ylabel='Skill = 1 − error / referencia',xticks=[1,3,5,7,9,12])
    axes[1].legend(fontsize=8); fig.suptitle('Fase 2: fractional frente a cuatro comparadores')
    save(fig,'F3_fractional_skill','Fractional RMSE and MAE skill',['phase2/skill_by_horizon.csv','phase2/horizon_summary.csv'],'Integer advantage; persistence/SARIMA negative at all horizons; seasonal positive only 1–5')
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    a=data['alpha']
    for ax in axes:
        ax.plot(a.alpha,a.fixed_section_rmse,'o-',ms=3,label='Otros parámetros fijos')
        ax.plot(a.alpha,a.de_profile_rmse,'s-',ms=3,label='Reoptimizado (DE)')
        ax.axhline(data['threshold'],ls='--',color='gray',label='RMSE primario × 1.01'); ax.set(xlabel='α',ylabel='RMSE de calibración')
    axes[0].set_title('21 puntos completos'); axes[1].set(xlim=(.499,.555),ylim=(615,655),title='Detalle de la frontera inferior'); axes[0].legend(fontsize=8)
    fig.suptitle('Fase 3: sección fija y perfil reoptimizado, sin inferencia de unicidad')
    save(fig,'F4_alpha_profiles','Alpha fixed and reoptimized profiles',['phase3/alpha_profile_comparison.csv','phase3/alpha_fixed_section.csv','phase3/profile_objective.csv'],'Finite grid; connecting lines only guide the eye; no continuous confidence interval')
    fig,ax=plt.subplots(figsize=(8,4))
    pool=data['pool'].sort_values('R0_reference').reset_index(drop=True)
    for flag,label,col in [(True,'Región RMSE ≤ primario × 1.01 (32)','#087e8b'),(False,'Resto diagnóstico (15)','#a0a0a0')]:
        subset=pool[pool.admissible_1pct==flag]; ax.scatter(subset.R0_reference,subset.index,c=col,s=23,label=label)
    ax.axvline(1,color='black',ls='--',label='R₀ = 1'); ax.set(xlabel='R₀ de referencia autónoma (μ = 1/888)',ylabel='Soluciones ordenadas por R₀',title='Fase 3: las 47 soluciones conservadas'); ax.legend(fontsize=8)
    save(fig,'F5_R0_explored_pool','Reference R0 finite explored pool',['phase3/solution_pool.csv','phase3/R0_practical_envelopes.csv','phase3/dfe_stability.csv'],'Envelope is descriptive; stable classification only autonomous reference; no eradication claim')
    dump(OUT/'FIGURE_TRACEABILITY.json',definitions)
    return definitions

def claims(data):
    p1='phase1/tb_global_refit_phase1/results_global_primary/'
    proto1=['phase1/tb_global_refit_phase1/README.md','phase1/package_provenance.json']
    proto2=['phase2/PROTOCOL_DECISION.md']
    proto3=['phase3/PROTOCOL_DECISION.md','decisions/AUTHOR_FREEZE_DECISION.md']
    out=[]
    def add(cid,status,text,tables,selector,calc,protocols,figures,limit,old_ids=None):
        out.append(dict(claim_id=cid,status=status,scientific_statement=text,tables=json.dumps(tables),row_selector=selector,calculation_sources=json.dumps(calc),protocols=json.dumps(protocols),figures=json.dumps(figures),scope_and_limitation=limit,historical_claim_ids=','.join(old_ids or [])))
    c1=['phase1/tb_global_refit_phase1/run_global_refit.py']
    c2=['phase2/run_rolling_ordinary.py','verification/freeze_evidence_20261010.py']
    c3=['phase3/run_phase3.py','verification/phase3_conformity/audit_phase3_conformity_20261010.py']
    add('S1','ACCEPTED','Observable SEIT: integral ordinaria mensual de σE sobre E corregida, por trapecios; C no realimenta la dinámica.',[p1+'phase1_report.json','verification/phase3_conformity/conformity_checks.csv'],'S1_ordinary_corrected_E_quadrature; observable_C_no_feedback_and_T_derivative',c1+['repository_snapshot/src/tb_seit/model.py'],proto1+proto2+proto3,[],'Contrato implementado y controles existentes, sin cambiar ecuaciones SEIT.')
    add('G1','ACCEPTED_DESCRIPTIVE','Fase 1: modelos independientes, semilla 20260815; train 2001–2020, validación open-loop 2021–2022.',[p1+'global_refit_parameters.csv',p1+'phase1_report.json',p1+'global_refit_metrics.csv'],'2 modelos; calibration n=240; validation_open_loop n=24',c1,proto1,['F1_global_open_loop'],'Un origen con 24 meses; no prueba inferencial ni competencia con baselines.')
    add('G2','ACCEPTED_DESCRIPTIVE','RMSE open-loop S1: fractional 1216.541986, integer 1759.542092; ventaja relativa fractional ≈30.8603%.',[p1+'global_refit_metrics.csv','reconciled_tables/phase1_comparison.csv'],'split=validation_open_loop',c1+['verification/freeze_evidence_20261010.py'],proto1,['F1_global_open_loop'],'Menor error descriptivo frente a integer; independiente del benchmark rolling-origin.')
    add('G3','ACCEPTED_DESCRIPTIVE','RMSE fractional open-loop histórico 1117.960028 sustituido por 1216.541986 bajo S1; mayor en ≈8.8180%.',['phase1/scientific_comparison.csv','reconciled_tables/phase1_comparison.csv'],'original_frozen_parameters vs ordinary_global_refit; fractional validation',c1,proto1,['F1_global_open_loop'],'Cambio conjuntamente de observable y parámetros: no atribución causal exclusiva a S1.')
    add('G4','ACCEPTED_WITH_NUMERICAL_LIMIT','Integer α=1: equivalencia teórica entre operadores; RMSE histórico 1759.538401 y S1 1759.542092 son numéricamente próximos.',['phase1/scientific_comparison.csv','phase1/preflight.json'],'integer validation; absolute difference 0.00369134047',c1,proto1,[],'No son floats idénticos: cuadratura ordinaria y discretización histórica distintas.')
    add('T1','ACCEPTED','Fase 2: 780 predicciones, 156 pares comunes por modelo, 13 orígenes, 12 horizontes y 26 ajustes SEIT exitosos.',['phase2/rolling_origin_predictions.csv','phase2/common_support.csv','phase2/fit_states.csv'],'5 modelos; origin 2020-12..2021-12; horizon 1..12',c2,proto2,['F2_rolling_RMSE'],'Baseline reutilizado exactamente; no nuevos ajustes en el cierre.')
    add('T2','ACCEPTED_DESCRIPTIVE','Fractional tiene menor RMSE y MAE que integer en los 12 horizontes.',['phase2/metrics_by_horizon.csv','phase2/skill_by_horizon.csv'],'model=fractional; baseline=integer; metric RMSE/MAE; skill>0 h=1..12',c2,proto2,['F2_rolling_RMSE','F3_fractional_skill'],'Comparación dentro de la familia; no superioridad estadística ni general.', ['C01'])
    add('T3','ACCEPTED_DESCRIPTIVE','Fractional no supera persistence: skill RMSE y MAE negativo en los 12 horizontes.',['phase2/skill_by_horizon.csv'],'model=fractional; baseline=persistence',c2,proto2,['F3_fractional_skill'],'Error observado; sin test de significación.', ['C02','C05'])
    add('T4','ACCEPTED_DESCRIPTIVE','Fractional no supera SARIMA: skill RMSE y MAE negativo en los 12 horizontes.',['phase2/skill_by_horizon.csv','phase2/baseline_reuse_verification.json'],'model=fractional; baseline=SARIMA',c2+['repository_snapshot/scripts/run_rolling_origin_forecast.py','repository_snapshot/scripts/select_sarima_order.py'],proto2+['repository_snapshot/docs/SARIMA_BASELINE_CONTRACT.md'],['F3_fractional_skill'],'No coeficientes SARIMA por origen archivados; procedencia código/datos/orden y predicciones sí verificada.', ['C03','C05'])
    add('T5','ACCEPTED_DESCRIPTIVE','Fractional supera seasonal naive solo h=1..5; H_relax=H_strict=5 para RMSE y MAE.',['phase2/skill_by_horizon.csv','phase2/horizon_summary.csv','phase2/historical_horizon_comparison.csv'],'fractional vs seasonal_naive_12; positivo 1..5, negativo 6..12',c2,proto2,['F3_fractional_skill'],'Sustituye h=7 histórico; no horizonte universal de predictibilidad.', ['C04'])
    add('T6','ACCEPTED','H_relax es el último h con skill>0; H_strict es el tramo positivo continuo desde h=1; cero si no existe.',['phase2/horizon_summary.csv','reconciled_tables/fractional_vs_four_comparators.csv'],'H=12 integer; H=5 seasonal; H=0 persistence/SARIMA; ambas métricas',c2,proto2,['F3_fractional_skill'],'Definiciones congeladas; signos preservados en controles de paso.')
    add('T7','ACCEPTED_DESCRIPTIVE','Bias fractional negativo en todos los horizontes rolling-origin.',['phase2/metrics_by_horizon.csv'],'model=fractional; bias=mean(predicted−observed)<0',c2,proto2,[],'Subpredicción observada en este soporte; no extrapolación causal ni universal.')
    add('T8','ACCEPTED_WITH_LIMITATION','α fractional está próximo a .50 en los 13 orígenes; global α=.502203.',['phase2/fit_states.csv',p1+'global_refit_parameters.csv'],'fractional α .500021.. .503773; cotas .50..1.00',c1+c2,proto1+proto2,[],'Frontera de búsqueda condiciona interpretación; no ampliar ni inferir memoria.', ['C06'])
    add('I1','ACCEPTED_DIAGNOSTIC','Perfil de α en 21 puntos .50..1: sección con otros parámetros fijos y reoptimización de cuatro parámetros separadas.',['phase3/alpha_fixed_section.csv','phase3/alpha_profile_comparison.csv','phase3/profile_objective.csv'],'21 α; raw fixed_section_rmse vs de_profile_rmse',c3,proto3,['F4_alpha_profiles'],'DE aproximado, curvas conectan puntos; no mínimo global/único ni intervalo continuo.')
    add('I2','ACCEPTED_DIAGNOSTIC','Pool de 47: primaria reutilizada, cuatro semillas diagnósticas y 42 perfiles; primaria no sustituida por menor coste.',['phase3/solution_pool.csv','phase3/multiseed_functionals.csv'],'sources 1+4+42; seeds 20260815 primary/profiles, 20260816..19 diagnostics',c3,proto3,['F5_R0_explored_pool'],'Conjunto correlacionado de soluciones; no muestra probabilística ni selección favorable.')
    add('I3','ACCEPTED_DIAGNOSTIC','Región explorada del 1%: RMSE ≤625.5119390086228, referencia primaria 619.3187514936859; 32 soluciones.',['phase3/solution_pool.csv','phase3/R0_practical_envelopes.csv'],'admissible_1pct=True; coste primario ×1.01',c3,proto3,['F4_alpha_profiles','F5_R0_explored_pool'],'No usar el menor coste del pool como nueva referencia; membresía estable h=.25.')
    add('I4','ACCEPTED_WITH_LIMITATION','En la rejilla reoptimizada, α admisible .50.. .52 y .55 excluido; no unicidad demostrada.',['phase3/alpha_profile_comparison.csv','phase3/parameter_dispersion.csv'],'reoptimized alpha admissible at sampled points',c3,proto3,['F4_alpha_profiles'],'No IC, no identificación precisa interior, no traslado de antiguas dispersiones.', ['C06','C09'])
    add('R1','ACCEPTED_REFERENCE_FUNCTIONAL','R₀ primario=0.35776750381879896 con μ=1/888 y Nref=S*=Λ/μ.',['phase3/solution_pool.csv','phase3/execution_provenance.json'],'solution_id=primary_20260815; R0=βσ/[(σ+μ)(γ+μ+d)]',c3,proto3,['F5_R0_explored_pool'],'Funcional de referencia del modelo; no estimación epidemiológica externa.')
    add('R2','ACCEPTED_DESCRIPTIVE_ENVELOPE','R₀ en 32 soluciones admisibles: .3416572022567021–.587925772372874, todas inferiores a uno.',['phase3/R0_practical_envelopes.csv','phase3/solution_pool.csv'],'NEAR_EQUIVALENT_1_PCT; n=32',c3,proto3,['F5_R0_explored_pool'],'No intervalo de confianza ni cota exhaustiva de todas las soluciones posibles.', ['C07'])
    add('R3','ACCEPTED_DIAGNOSTIC','Pool completo: R₀ .341657–1.661998; 44 por debajo de uno y tres por encima.',['phase3/R0_practical_envelopes.csv','phase3/solution_pool.csv'],'FULL_DIAGNOSTIC_POOL; n=47',c3,proto3,['F5_R0_explored_pool'],'Las tres soluciones R0>1 se conservan; quedan fuera por RMSE, no por su signo.')
    add('D1','ACCEPTED_AUTONOMOUS_ONLY','DFE estable en las 32 soluciones admisibles bajo referencia autónoma; pool completo 44 estables y tres inestables.',['phase3/dfe_stability.csv','phase3/dfe_eigenvalues.csv','verification/phase3_conformity/SCIENTIFIC_CONFORMITY_REPORT.md'],'admissible_1pct; J(q=1); cuatro estados; ∂Tdot/∂I=γ',c3+['phase3/test_phase3.py'],proto3,['F5_R0_explored_pool'],'Matignon común α, matriz constante: R₀<1 implica autovalores negativos. No estabilidad global.', ['C08'])
    add('D2','NOT_ESTABLISHED','No está demostrada estabilidad para el sistema con N(t) variable.',['phase3/dfe_frozen_time_diagnostics.csv','verification/phase3_conformity/SCIENTIFIC_CONFORMITY_REPORT.md'],'nonautonomous_stability_proof=False en todos los registros',c3,proto3,[],'Matignon congelado punto a punto no demuestra estabilidad no autónoma.')
    add('D3','NOT_SUPPORTED','No se demuestra desaparición de tuberculosis en Brasil.',['phase3/dfe_stability.csv','phase3/dfe_frozen_time_diagnostics.csv'],'Referencia autónoma distinta del sistema N(t) y de una predicción poblacional',c3,proto3,[],'Prohibida interpretación epidemiológica de erradicación a partir de esta clasificación.')
    add('Q1','ACCEPTED_WITH_ARCHIVE_LIMITATION','Controles h=1,.5,.25 pasados; máximo cambio mensual Fase 3 ≈.119134%; signs Skill y miembros del 1% conservados.',['phase2/origin_numerical_checks.csv','phase2/skill_discretization_check.csv','phase3/numerical_resolution_checks.csv','phase3/numerical_checkpoint.jsonl'], '26 controles Fase2; 115 Fase3; todos pasan',c2+c3,proto2+proto3,[],'Comprobación empírica, no cota de error continuo; estados finos Fase3 no archivados íntegros.')
    add('Q2','ACCEPTED','Calibración usa solo datos al origen; población/inicialización de entrenamiento; validación no selecciona soluciones.',['phase2/leakage_checks.csv','phase2/fit_states.csv','phase3/initial_states_and_leakage.csv'], '26 leakage rows; 47 global solutions train hash común',c1+c2+c3,proto1+proto2+proto3,[],'Expanding-window incluye meses 2021 ya observados en orígenes posteriores; no confundir con validación global fija.')
    add('Q3','ACCEPTED_DOCUMENTARY_LIMIT','Protocolo disponible precede ejecución Fase3 según sesión local, pero se redactó tras conocer Fases1/2; adopción del autor retrospectiva.',['verification/phase3_conformity/audit_evidence.json','verification/phase3_conformity/chronology_fragments.jsonl'],'write protocol 2026-10-08T19:36:16.660Z; launch 19:40:16.626Z', ['verification/phase3_conformity/audit_phase3_conformity_20261010.py'],proto3,[],'Sin sellado temporal independiente ni equivalencia con protocolo desaparecido; búsqueda cerrada.')
    add('Q4','NOT_TESTED','No se realizaron pruebas de significación ni se estableció superioridad estadística.',['phase2/phase2_report.json','phase2/final_verification.json'],'statistical_inference_performed=False',c2,proto2,[],'Forecasts dependientes entre orígenes/horizontes; inferencia no autorizada.', ['C11'])
    add('Q5','NOT_ESTABLISHED','No se atribuye toda la inversión histórica de R₀/DFE exclusivamente a S1.',['reconciled_tables/historical_vs_corrected.csv','phase1/scientific_comparison.csv'],'Cambian observable, vector estimado y conjunto explorado',c1+c3,proto1+proto3,[],'Ablación existente a parámetros fijos no identifica la causa de toda la inversión mecanística.')
    add('Q6','OUT_OF_SCOPE_UNVERIFIED','La reducción histórica de control óptimo ~48% sigue sin verificar y no forma parte de la evidencia congelada.',['historical_reference/PROJECT_CANON.md','historical_reference/results_canonical/07_claim_support/claim_support_table.csv'],'historical C10', ['repository_snapshot/src/tb_seit/model.py'], ['historical_reference/PROJECT_CANON.md'],[],'No nuevo modelo ni implementación de control óptimo.', ['C10'])
    return out

def main():
    if OUT.exists(): raise RuntimeError('Refusing to overwrite existing freeze')
    tracked=validate_sources()
    before_sources={str(p):sha(p) for root in [P1,P2,A2,A3] for p in files(root)}
    controls=[REPO,Path('/Users/fede/repos/tb-fractional-seit-brazil'),Path('/Users/fede/repos/tb-seit-claim-audit'),BASE/'work/tb-observation-ablation']
    git_before={str(r):dict(head=git(r,'rev-parse','HEAD').strip(),branch=git(r,'branch','--show-current').strip(),status=git(r,'status','--porcelain=v1')) for r in controls}
    data=validate_results()
    OUT.mkdir()
    copy_tree(P1,OUT/'phase1'); copy_tree(P2,OUT/'phase2'); copy_tree(P3,OUT/'phase3')
    copy_tree(A2,OUT/'verification/phase2_zip')
    copy_tree(A3,OUT/'verification/phase3_conformity')
    for rel in tracked:
        if rel.startswith(('src/','scripts/','tests/','data/','docs/')) or rel=='pyproject.toml': copy_file(REPO/rel,OUT/'repository_snapshot'/rel)
    for rel in tracked:
        if rel.startswith(('results_canonical/','outputs/')) or rel in ['PROJECT_CANON.md','IDENTIFIABILITY_AUDIT_REPORT.md','R0_STABILITY_ANALYSIS_NOTE.md','FORECASTING_EVALUATION_REPORT.md']:
            copy_file(REPO/rel,OUT/'historical_reference'/rel)
    for directory in ['decisions','reconciled_tables','verification']: (OUT/directory).mkdir(exist_ok=True)
    copy_file(Path(__file__),OUT/'verification'/Path(__file__).name)
    dump(OUT/'verification/tracked_239_sha256.json',tracked)
    (OUT/'decisions/AUTHOR_FREEZE_DECISION.md').write_text('''# Decisión del autor — 10 de octubre de 2026\n\nFuente: instrucción humana en este chat. Registro documental del encargo actual; no sustituye ni modifica protocolos históricos.\n\nSe acepta `PHASE3_PASS_WITH_DOCUMENTED_LIMITATIONS` tras las 49 comprobaciones. Se autoriza reconciliación y congelación de Fases 1, 2 y 3 exclusivamente con evidencia existente. No se autorizan nuevos experimentos, cambios de modelos, parámetros o criterios ni redacción editorial.\n\nSe conservan S1, 21 puntos de α fijo/reoptimizado, 32 soluciones bajo 1% de RMSE, R₀ primario .357768 y envolvente .341657–.587926, DFE estable únicamente en referencia autónoma. La envolvente no es IC y los perfiles no demuestran unicidad. No se atribuye toda la diferencia histórica exclusivamente al operador ni se infiere desaparición de TB o estabilidad con N(t).\n\n`ORIGINAL_PROTOCOL_UNAVAILABLE`: búsqueda cerrada. `PROTOCOL_DECISION.md` de Fase 3 se conserva con SHA-256 58d4bed36871f9c63cd93e4c199d5c9890f006ccaf96ede85362480dee91469b como protocolo efectivamente ejecutado; no equivalencia con el desaparecido ni preespecificación general.\n\nEl siguiente gate es `EVIDENCE_FREEZE`. Manuscrito, integración PR #3, compilación, envío y decisión de revista no se ejecutan en este encargo.\n''')
    comp=table(P1/'scientific_comparison.csv')
    comp.to_csv(OUT/'reconciled_tables/phase1_comparison.csv',index=False,float_format='%.17g')
    comparisons=data['skill'][data['skill'].model=='fractional'].copy()
    comparisons.to_csv(OUT/'reconciled_tables/fractional_vs_four_comparators.csv',index=False,float_format='%.17g')
    changes=[
        dict(aspect='Global fractional alpha',historical='0.9640110362133341',corrected='0.5022029993981696',disposition='REPLACED_S1',scope='Boundary-limited estimate; no biological memory proof'),
        dict(aspect='Global fractional validation RMSE',historical='1117.9600278486839',corrected='1216.5419862064475',disposition='REPLACED_S1',scope='Single-origin 24 months; no baseline superiority'),
        dict(aspect='Global integer validation RMSE',historical='1759.5384005453041',corrected='1759.542091885776',disposition='REPLACED_NUMERIC_S1',scope='Theoretical alpha=1 equivalence; small quadrature difference retained'),
        dict(aspect='Fractional seasonal naive H_relax/H_strict RMSE/MAE',historical='7/7',corrected='5/5',disposition='REPLACED_S1',scope='Specific comparator and evaluated support'),
        dict(aspect='Fractional vs integer',historical='Lower RMSE/MAE at all 12 horizons',corrected='Lower RMSE/MAE at all 12 horizons',disposition='CONCLUSION_RETAINED_VALUES_REPLACED',scope='Descriptive within-model-family'),
        dict(aspect='Fractional vs persistence/SARIMA',historical='Negative skill all 12 horizons',corrected='Negative skill all 12 horizons',disposition='CONCLUSION_RETAINED_VALUES_REPLACED',scope='No significance tests; SARIMA coefficients per origin absent'),
        dict(aspect='R0 1pct explored envelope',historical='1.154172396476935–1.1892187917630623; n=25',corrected='0.3416572022567021–0.587925772372874; n=32',disposition='HISTORICAL_OBSOLETE',scope='Distinct explored sets; descriptive envelope not CI'),
        dict(aspect='DFE 1pct explored set',historical='0 stable, 25 unstable',corrected='32 stable, 0 unstable',disposition='HISTORICAL_OBSOLETE',scope='Corrected autonomous reference only; no claim for N(t)'),
        dict(aspect='R0 full diagnostic pool',historical='n=33, min=.639310940867302 max=1.6148758715364961',corrected='n=47, min=.3416572022567021 max=1.6619977217037603',disposition='REPLACED_DIAGNOSTIC',scope='Do not conflate full pool with 1% set'),
        dict(aspect='Identifiability/dispersion claims',historical='Previous operator and parameters',corrected='21 alpha points, fixed/reoptimized separated; finite explored diagnostics',disposition='REASSESS_OLD_NUMERIC_SPREADS',scope='No unique interior alpha; no transfer of historical parameter spread factors'),
        dict(aspect='Figures/tables in manuscript and PR #3',historical='Old observable evidence',corrected='New frozen figures/tables supplied in this bundle',disposition='OLD_CONTENT_OUTDATED_NOT_EDITED',scope='No manuscript/PR modifications or compilation')]
    write_csv(OUT/'reconciled_tables/historical_vs_corrected.csv',changes)
    figures=create_figures(data)
    rows=claims(data); write_csv(OUT/'CLAIM_EVIDENCE_MATRIX.csv',rows)
    registry=[]
    with (REPO/'results_canonical/07_claim_support/claim_support_table.csv').open() as handle:
        parsed=list(csv.reader(handle))
    header=parsed[0]
    overflow=[r[0] for r in parsed[1:] if len(r)>len(header)]
    check('historical_C09_C11_unquoted_notes_commas_documented',overflow==['C09','C11'] and all(len(r)>=len(header) for r in parsed[1:]))
    # Original C09/C11 have unquoted commas in final notes. First six fields are
    # unchanged; join the extra trailing fields for the new disposition registry.
    for raw in parsed[1:]:
        r=dict(zip(header,raw[:6]+[','.join(raw[6:])]))
        ids=[c['claim_id'] for c in rows if r['claim_id'] in c['historical_claim_ids'].split(',')]
        status='REPLACED_OBSOLETE' if r['claim_id'] in ['C04','C07','C08'] else ('HISTORICAL_WORDING_NOT_TRANSFERABLE' if r['claim_id'] in ['C06','C09'] else 'RECONCILED_WITH_NEW_EVIDENCE')
        registry.append(dict(historical_claim_id=r['claim_id'],historical_statement=r['candidate_claim'],historical_status=r['status'],freeze_disposition=status,current_claim_ids=','.join(ids),historical_table=r['supporting_artifact'],original_not_modified=True))
    write_csv(OUT/'HISTORICAL_CLAIM_DISPOSITION.csv',registry)
    figure_ids={r['figure_id'] for r in figures}
    for r in rows:
        for col in ['tables','calculation_sources','protocols']:
            assert all((OUT/p).is_file() for p in json.loads(r[col]))
        assert set(json.loads(r['figures']))<=figure_ids
    check('all_29_claims_have_existing_table_calculation_protocol_links',len(rows)==29 and all(json.loads(r['tables']) and json.loads(r['calculation_sources']) and json.loads(r['protocols']) for r in rows))
    check('all_11_historical_claims_have_current_disposition',len(registry)==11 and all(r['current_claim_ids'] for r in registry))
    check('all_five_figures_derive_only_from_frozen_tables',len(figures)==5 and all((OUT/p).is_file() for r in figures for p in r['source_tables']))
    check('all_copied_sources_identical',all(sha(OUT/p)==entry['sha256'] for p,entry in SOURCES.items()))
    check('all_input_evidence_preserved',all(sha(p)==h for p,h in before_sources.items()))
    check('239_repository_tracked_files_preserved_after_freeze',all(sha(REPO/p)==h for p,h in tracked.items()))
    git_after={str(r):dict(head=git(r,'rev-parse','HEAD').strip(),branch=git(r,'branch','--show-current').strip(),status=git(r,'status','--porcelain=v1')) for r in controls}
    check('all_four_control_worktrees_HEAD_branch_status_preserved',git_after==git_before)
    dump(OUT/'verification/git_integrity.json',dict(before=git_before,after=git_after,tracked_files=239,tracked_hashes_preserved=True,untracked_audits_preserved=True))
    dump(OUT/'SOURCE_PROVENANCE.json',SOURCES)
    write_csv(OUT/'verification/freeze_checks.csv',CHECKS)
    summary=dict(verdict='EVIDENCE_FREEZE_PASS',freeze_timestamp_utc=datetime.now(timezone.utc).isoformat(),source_commit=COMMIT,branch=git_after[str(REPO)]['branch'],checks=len(CHECKS),all_checks_pass=True,claims=len(rows),figures=5,phase2_predictions=780,phase2_pairs_per_model=156,phase2_fits=26,phase3_pool=47,phase3_admissible=32,phase3_alpha_grid=21,primary_R0=float(data['primary'].R0_reference),R0_envelope=[float(data['env'].loc['NEAR_EQUIVALENT_1_PCT','minimum']),float(data['env'].loc['NEAR_EQUIVALENT_1_PCT','maximum'])],primary_rmse=float(data['primary'].calibration_rmse),admissible_threshold=data['threshold'],new_optimizations=0,new_solver_simulations=0,new_scientific_experiments=0,method='Integrity checks, static inspection, arithmetic from existing tables, documentary reconciliation and plots only',original_protocol_status='ORIGINAL_PROTOCOL_UNAVAILABLE_SEARCH_CLOSED',phase3_protocol_sha256=sha(P3/'PROTOCOL_DECISION.md'),editorial_actions_executed=False,canonical_results_modified=False,commit_push_merge=False,limitations_retained=True)
    dump(OUT/'FREEZE_SUMMARY.json',summary)
    write_report(data,summary)
    make_verifier()
    manifest=inventory(OUT)
    dump(OUT/'artifact_manifest.json',manifest)
    assert check_manifest(OUT)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

def write_report(data,summary):
    p1val=data['m1'].set_index(['model','split'])
    advantage=100*(1-p1val.loc[('fractional','validation_open_loop'),'rmse']/p1val.loc[('integer','validation_open_loop'),'rmse'])
    (OUT/'EVIDENCE_FREEZE_REPORT.md').write_text(f'''# Reconciliación y congelación de evidencia — 10 de octubre de 2026

**Dictamen: `EVIDENCE_FREEZE_PASS`.** Las Fases 1, 2 y 3 quedan congeladas documentalmente en este paquete con las limitaciones aceptadas por el autor. Pasan {summary['checks']} controles de cierre y se conservan los informes previos de 43 comprobaciones de Fase 2 y 49 de Fase 3. La auditoría verifica hashes actuales y reconstruye métricas de tablas existentes; no vuelve a ejecutar esas simulaciones ni optimizaciones.

## Qué se congela

| Eje | Evidencia vigente | Alcance |
|---|---|---|
| Observación SEIT | Integral mensual ordinaria S1 de σE; trapecios sobre E corregida | No se usa el acumulador Caputo C para incidencia |
| Fase 1 global | Fractional e integer independientes, seed 20260815, train 2001–2020 | Validación open-loop 2021–2022, un origen |
| Fase 2 temporal | 780 predicciones; 156 pares por modelo; 26 ajustes SEIT | 13 orígenes 2020-12…2021-12, h=1…12 |
| Fase 3 práctica | 21 α fijos/reoptimizados; 47 soluciones; 32 bajo 1% | Diagnósticos aproximados y conjunto finito |
| R₀ y DFE | Primario .3577675038; envolvente .3416572023–.5879257724; 32 estables | Referencia autónoma; no prueba para N(t) variable |

Los bytes originales de cada fase están en `phase1/`, `phase2/` y `phase3/`. Sus propios informes reflejan los estados de revisión de sus fechas de creación y permanecen intactos. La aceptación y la congelación actual constan en este informe y en `decisions/AUTHOR_FREEZE_DECISION.md`; no se reescribe la historia para que los informes antiguos parezcan ya aceptados.

## Fase 1: validación y sustitución

| Modelo S1 | RMSE train | MAE train | Bias train | RMSE open-loop | MAE open-loop | Bias open-loop |
|---|---:|---:|---:|---:|---:|---:|
| Fractional | 619.318751 | 484.062478 | +49.456919 | 1216.541986 | 1035.207104 | −983.953702 |
| Integer | 776.040852 | 616.145573 | +171.226633 | 1759.542092 | 1588.652631 | −1588.652631 |

Las 264 predicciones de cada modelo reproducen los cuatro registros de métricas, con 240 meses de calibración y 24 de validación. La ventaja relativa de RMSE fractional frente a integer es {advantage:.6f}% en este origen. Este resultado sigue válido como descripción open-loop; no establece superioridad frente a baselines ni significación estadística.

Se sustituye el RMSE fractional histórico 1117.960028 por 1216.541986. α primario pasa de .964011 a .502203; la estimación corregida se reutiliza sin seleccionarla entre semillas diagnósticas. A α=1 los operadores son teóricamente equivalentes, pero sus discretizaciones no producen floats idénticos: RMSE integer histórico 1759.538401 y S1 1759.542092, diferencia 0.00369134. Se conserva y documenta esa pequeña diferencia. `phase1/scientific_comparison.csv` separa ablación a parámetros fijos de reajuste global; no se mezclan para atribuir causalmente todo cambio mecanístico al operador.

## Fase 2: predicciones y cuatro comparadores

Se congelan **exactamente** `phase2/rolling_origin_predictions.csv` (780 filas), `metrics_by_horizon.csv` (60), `skill_by_horizon.csv` (168) y `horizon_summary.csv` (14). No se agrupan horizontes para fabricar una métrica global. Las 468 predicciones de persistence, seasonal naive y SARIMA se conservan exactamente; las 312 SEIT pertenecen solo a S1.

| Referencia de fractional | Skill RMSE/MAE positivo | H_relax | H_strict |
|---|---|---:|---:|
| Integer | h=1…12 | 12 | 12 |
| Persistence | Ninguno | 0 | 0 |
| Seasonal naive 12 | h=1…5 | 5 | 5 |
| SARIMA | Ninguno | 0 | 0 |

Skill=1−error_modelo/error_referencia. H_relax es el último horizonte con skill positivo y H_strict el tramo positivo desde h=1, o cero. La comparación con seasonal naive sustituye **7 por 5**; el resto conserva su conclusión descriptiva con valores nuevos. Fractional tiene bias negativo en todos los horizontes. Los 13 α fraccionarios están próximos a la cota inferior .50.

Leakage: cada rolling origin utiliza solamente datos hasta ese origen; las ventanas posteriores incorporan los meses 2021 ya observados. No son los mismos 240 meses fijos del ajuste global. Constantes, población extrapolada e inicialización se construyen dentro de cada entrenamiento. Los objetivos futuros no entran al ajuste. Los 26 vectores y controles permanecen guardados. El ZIP verificado originalmente mantiene SHA-256 `90ac75b21112be90ac4f9eba8658ef5203334535371b35011b519c167215818b`.

Limitación SARIMA: especificación congelada (0,1,2)(1,1,1,12), procedencia de código/datos y predicciones acreditadas; faltan los coeficientes de cada ajuste histórico. No se hace refit para completar el archivo. Las comparaciones son descriptivas, sin pruebas de significación que ignoren la dependencia entre errores.

## Fase 3: identificabilidad, R₀ y DFE

La sección de α con β/σ/γ/d fijos y el perfil reoptimizado usan 21 puntos idénticos; sus columnas crudas se preservan por separado. `feasible_cost_upper_bound` es una columna auxiliar y no reemplaza costes ni soluciones. El pool incluye primaria, cuatro semillas diagnósticas y 42 perfiles; se conservan todos, incluso los tres con R₀>1. El menor coste explorado no reemplaza la primaria.

El umbral principal es **619.3187514936859 ×1.01 =625.5119390086228**, aplicado al RMSE de calibración. Da 32 soluciones y coincide la membresía con los controles h=.25. Los α reoptimizados admisibles muestreados están entre .50 y .52; .55 queda fuera. No se identifica una frontera continua entre esos puntos, unicidad, un mínimo global ni un mecanismo biológico de memoria.

Con μ=1/888, R₀=βσ/[(σ+μ)(γ+μ+d)] en la referencia Nref=S*=Λ/μ. Primario **.35776750381879896**. En las 32 soluciones exploradas admisibles, **.3416572022567021–.587925772372874**. El pool diagnóstico completo tiene 47, con R₀ .341657–1.661998 (44<1, 3>1). La envolvente no es IC ni rango exhaustivo de todas las soluciones matemáticamente admisibles.

El jacobiano epidemiológico de cuatro estados incluye ∂Tdot/∂I=γ; C no realimenta y se excluye del criterio. En referencia autónoma, el bloque E/I tiene traza negativa y determinante (σ+μ)(γ+μ+d)(1−R₀). Si R₀<1 todos sus autovalores y los dos −μ son negativos: cumplen Matignon para orden común 0<α≤1. Las 32 soluciones admisibles son estables; el pool completo presenta 44 estables y tres inestables. Se conserva la demostración y la comprobación de los 188 autovalores en el informe de conformidad de Fase 3, sin recalcular un nuevo experimento.

Con N(t) exógeno el jacobiano cambia. Los espectros congelados punto a punto son diagnósticos, no una prueba no autónoma. **No se demuestra desaparición de tuberculosis en Brasil, estabilidad global ni estabilidad del sistema con N(t) variable.** Para un espectro fijo disminuir α reduce el umbral angular de Matignon; no lo hace más exigente.

El conjunto histórico de 25 soluciones con R₀ 1.154172–1.189219 y DFE inestable se marca **obsoleto para S1**, conservando sus tablas intactas en `historical_reference/`. La inversión de clasificación dentro de dos conjuntos explorados distintos no se atribuye exclusivamente al observable: también cambian los parámetros y el diseño del pool.

## Claims, figuras y retirada documental

`CLAIM_EVIDENCE_MATRIX.csv` vincula {summary['claims']} afirmaciones/limitaciones con tablas y selección de filas, código de cálculo, protocolo y figuras cuando corresponde. Incluye estados NOT_ESTABLISHED/NOT_TESTED/NOT_SUPPORTED para evitar convertir una falta de evidencia en un resultado positivo. `HISTORICAL_CLAIM_DISPOSITION.csv` reconcilia los 11 claims históricos: C04 (h=7), C07 (R₀>1) y C08 (DFE inestable) quedan sustituidos; wording de estabilidad de α y factores de dispersión antiguos no se trasladan. El control óptimo ~48% continúa fuera de alcance y sin verificar.

El CSV histórico de claims tiene dos comas sin entrecomillar en la nota final de C09 y una en C11. Se conserva intacto y, solo para el nuevo registro de disposición, se unen sus campos sobrantes de notas; los seis primeros campos permanecen sin cambio. Es una limitación de formato histórica, sin efecto en las cifras científicas o la clasificación de este gate.

Se generan cinco figuras documentales a partir de las tablas guardadas, PNG y PDF: ajuste/open-loop, RMSE rolling, skill frente a cuatro comparadores, α fijo/perfilado y pool R₀. `FIGURE_TRACEABILITY.json` fija los insumos y el alcance de cada una. No son figuras insertadas en el manuscrito ni una redacción editorial. Las figuras históricas permanecen en la sección marcada como referencia obsoleta y no se deben reutilizar para S1.

## Protocolo y cronología

Se conserva `PROTOCOL_DECISION.md` SHA-256 **58d4bed36871f9c63cd93e4c199d5c9890f006ccaf96ede85362480dee91469b**. Registro local: creación de sus bytes exactos 2026-10-08 19:36:16.660 UTC, ejecución 19:40:16.626 UTC. Es anterior al cálculo de Fase 3, pero posterior a los resultados conocidos de Fases 1/2; adopción humana documental del 10 de octubre. No existe sellado temporal independiente de esa cronología.

`ORIGINAL_PROTOCOL_UNAVAILABLE`: decisión cerrada, sin nueva búsqueda, equivalencia ni autorización atribuida al documento desaparecido. Se conservan los 21 puntos y cuatro semillas diagnósticas como diseño ejecutado y aceptado, sin volver a ejecutar para producir resultados más favorables.

## Integridad, reproducibilidad y límites del sellado

239 hashes tracked, HEAD/rama/status de cuatro worktrees y todos los archivos fuente auditados se preservan. Git científico termina con `?? audits/`; esos archivos se conservan. No hubo commit, push, merge, cambios canónicos, manuscrito, PR ni compilación. La copia de código/datos/protocolos y el entorno guardado permiten inspección y reproducción futura, pero este gate no autoriza repetir experimentos.

Los controles de resolución existentes comparan h=1,.5,.25; su máxima diferencia mensual de Fase 3 es aproximadamente .119134%, inferior al 1%. Son controles empíricos, no una cota formal de error continuo. Fase 3 no conserva todos los estados crudos de las mallas finas: se guardan 115 controles, 114 checkpoints y código/insumos. El cierre no realiza simulaciones para completar ese archivo. Se conserva expresamente esta limitación, junto a la ausencia de un manifiesto integral de Fase 3 sellado antes de esta auditoría.

`SOURCE_PROVENANCE.json` registra procedencia y SHA-256 de cada copia. `artifact_manifest.json` cubre todos los archivos del paquete salvo a sí mismo; se entrega un hash externo del manifiesto y del ZIP. Es congelación por integridad criptográfica local a la fecha actual, no un sello prospectivo o certificado temporal externo. Cualquier cambio requiere una versión nueva y un manifiesto nuevo, sin sobrescribir esta.

Comprobación portátil de solo lectura: `python verification/verify_frozen_bundle.py RUTA_PAQUETE`. Verifica manifiesto, lista completa, predicciones/soporte y estados, sin importar solvers u optimizadores. El generador conservado `verification/freeze_evidence_20261010.py` documenta las comprobaciones aritméticas detalladas y rechaza sobrescribir una congelación existente.

## Estado de cierre

El gate de evidencia queda satisfecho con las limitaciones documentadas. Forecasting y referencia mecanística siguen separados. Queda preparada la evidencia para una instrucción posterior de reconciliación editorial; este encargo no modifica Abstract, Results, Discussion, PR #3, compilación, envío ni selección de revista. El paso del gate no constituye permiso para merge, publicación ni envío.

**Dictamen final: `EVIDENCE_FREEZE_PASS`.**
''')
    (OUT/'README.md').write_text('''# Evidencia TB/SEIT Brasil — S1 — congelación 2026-10-10

Estado vigente: `EVIDENCE_FREEZE_PASS`; leer `EVIDENCE_FREEZE_REPORT.md` y `FREEZE_SUMMARY.json`.

- `phase1/`, `phase2/`, `phase3/`: copias byte idénticas de la evidencia corregida.
- `CLAIM_EVIDENCE_MATRIX.csv`: afirmaciones vigentes, no demostradas y límites; insumos de cálculo y protocolo.
- `HISTORICAL_CLAIM_DISPOSITION.csv`, `reconciled_tables/`: sustituciones y comparaciones.
- `figures/`, `FIGURE_TRACEABILITY.json`: visualizaciones documentales de tablas existentes.
- `historical_reference/`: EVIDENCIA HISTÓRICA del otro operador, conservada para comparación; **no usar como evidencia vigente S1**. Sus informes y sellos históricos no prevalecen sobre el presente registro de sustituciones.
- `repository_snapshot/`: insumos y código base del commit b3ad21b; el acumulador histórico sigue en el código base, pero los ejecutores corregidos en phase1/2/3 usan la cuadratura S1.
- `verification/`: controles previos, cierre actual, cronología y verificador portátil.
- `SOURCE_PROVENANCE.json`, `artifact_manifest.json`: procedencia y SHA-256.

Los informes/protocolos anteriores están preservados, incluidos sus estados de revisión a fecha de ejecución. La aceptación presente está en `decisions/AUTHOR_FREEZE_DECISION.md`. La búsqueda del protocolo perdido permanece cerrada.

Solo verificar: `python verification/verify_frozen_bundle.py RUTA_PAQUETE`. No ejecutar los runners científicos por este gate. No hay permiso de nuevas optimizaciones, simulaciones, editorial, merge ni envío. Las líneas de las curvas de α solo conectan los 21 puntos y no son un intervalo continuo.
''')

def make_verifier():
    (OUT/'verification/verify_frozen_bundle.py').write_text('''"""Portable read-only freeze verifier. Standard library only; no scientific execution."""
from pathlib import Path
import csv
import hashlib
import json
import sys

root=Path(sys.argv[1]).resolve()
manifest=json.loads((root/'artifact_manifest.json').read_text())
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==set(manifest)|{'artifact_manifest.json'}, 'Incomplete or extra files'
for name,digest in manifest.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest, 'Hash discrepancy: '+name
rows=list(csv.DictReader((root/'phase2/rolling_origin_predictions.csv').open()))
assert len(rows)==780
models={'fractional','integer','persistence','seasonal_naive_12','SARIMA'}
assert {r['model'] for r in rows}==models
support={model:{(r['origin'],r['target_date'],r['horizon']) for r in rows if r['model']==model} for model in models}
assert all(len(s)==156 for s in support.values())
assert all(s==next(iter(support.values())) for s in support.values())
checks=list(csv.DictReader((root/'verification/freeze_checks.csv').open()))
assert all(r['status']=='PASS' for r in checks)
summary=json.loads((root/'FREEZE_SUMMARY.json').read_text())
assert len(checks)==summary['checks'] and summary['verdict']=='EVIDENCE_FREEZE_PASS'
claims=list(csv.DictReader((root/'CLAIM_EVIDENCE_MATRIX.csv').open()))
assert len(claims)==summary['claims']
for r in claims:
    for column in ['tables','calculation_sources','protocols']:
        assert all((root/p).is_file() for p in json.loads(r[column]))
assert summary['new_optimizations']==summary['new_solver_simulations']==summary['new_scientific_experiments']==0
print(json.dumps({'status':'PASS','payload_files':len(manifest),'predictions':780,'pairs_per_model':156,'claims':len(claims),'freeze_checks':len(checks),'scientific_executions':0},indent=2))
''')

if __name__=='__main__': main()
