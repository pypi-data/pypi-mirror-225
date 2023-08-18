import warnings, math, time, copy, random, os
from contextlib import redirect_stdout, redirect_stderr
import logging, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cluster, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.decomposition import PCA, IncrementalPCA, TruncatedSVD
from scipy import stats
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import NearestNeighbors

CLUSTERING_AGO = 'lv'
SKNETWORK = True
try:
    from sknetwork.clustering import Louvain
except ImportError:
    print('WARNING: sknetwork not installed. GMM will be used for clustering.')
    CLUSTERING_AGO = 'gm'
    SKNETWORK = False

INFERCNVPY = True
try:
    import infercnvpy as cnv
except ImportError:
    print('ERROR: infercnvpy not installed. Tumor cell identification will not be performed.')
    INFERCNVPY = False

SCANVPY = True
try:
    import scanpy as sc
except ImportError:
    print('WARNING: scanpy not installed.')
    SCANVPY = False


MIN_ABS_VALUE = 1e-8

def bimodal_fit( x ):
    
    df_param = pd.DataFrame( columns = ['value'], \
                          index = ['w0', 'm0', 'v0', 'w1', 'm1', 'v1'] )
    
    gmm = mixture.GaussianMixture(n_components = 2, random_state = 0)
    y = gmm.fit_predict(np.array(x).reshape(-1, 1))

    mns = [m[0] for m in gmm.means_]
    cvs = [cv[0,0] for cv in gmm.covariances_]

    wgs = gmm.weights_           
    if mns[0] < mns[1]:
        w0, w1 = wgs[0], wgs[1]
        m0, m1 = mns[0], mns[1]
        v0, v1 = cvs[0], cvs[1]
    else:
        w0, w1 = wgs[1], wgs[0]
        m0, m1 = mns[1], mns[0]
        v0, v1 = cvs[1], cvs[0]

    param = [w0, m0, v0, w1, m1, v1]
    df_param['value'] = param
            
    return df_param['value']
        
        
def get_normal_pdf( x, mu, var, nbins):
    
    y = np.array(x)
    mn_x = y.min()
    mx_x = y.max()
    dx = mx_x - mn_x
    mn_x -= dx/4
    mx_x += dx/4
    L = 100
    # dx = len(y)*(mx_x-mn_x)/L
    dx = (mx_x-mn_x)/nbins
    xs = np.arange(mn_x,mx_x, dx )
    pdf = (dx*len(y))*np.exp(-((xs-mu)**2)/(2*var+MIN_ABS_VALUE))/(np.sqrt(2*math.pi*var)+MIN_ABS_VALUE) + MIN_ABS_VALUE
    return pdf, xs


def get_malignancy_prob( xs, param ):
    
    w0, mu0, var0, w1, mu1, var1 = tuple(param)
    
    p0 = w0*np.exp(-((xs-mu0)**2)/(2*var0+MIN_ABS_VALUE))/(np.sqrt(2*math.pi*var0)+MIN_ABS_VALUE) + MIN_ABS_VALUE
    p1 = w1*np.exp(-((xs-mu1)**2)/(2*var1+MIN_ABS_VALUE))/(np.sqrt(2*math.pi*var1)+MIN_ABS_VALUE) + MIN_ABS_VALUE    
    pr = p1/(p0+p1)
    
    b = (xs < mu0)
    pr[b] = MIN_ABS_VALUE
    
    return pr


def get_cnv_threshold_bimodal( obs, ref_ind, score_key = 'cnv_score', 
                               cluster_key = 'cnv_leiden', th_max = 0, refp_min = 0.9, 
                               ucr = 0.1, plot_stat = True, suffix = '', Data = None ):
    
    th_min = -th_max
    ## obs must contain columns 'cnv_cluster', 'cnv_score'
    
    df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'mean'})
    idx_lst = list(df.index.values)
    
    ps = bimodal_fit( df['cmean'] )
    w0, m0, v0, w1, m1, v1 = tuple(ps)

    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200
    n_bins = 50

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)

    th = -1
    for k in range(len(xs0)):
        if (pdf1[k] >= pdf0[k]) & (xs0[k] > m0):
            th = xs0[k]
            break
            
    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        print('INFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
        th = m0 + np.sqrt(v0)
            
    s = obs[score_key]
    tpr = get_malignancy_prob( s, list(ps) )
    obs['tumor_score'+ suffix] = tpr
    
    # print('threshold: ', th )
    th = max(th, th_min)
    th = min(th, th_max)
    
    dec = pd.Series(['Normal']*len(s), index = obs.index)
    
    lt = th - (th - m0)*ucr # p_exc 
    ut = th + (m1 - th)*ucr #p_exc
    
    bs = (s > th)
    df['dec'] = 'Normal'
    for idx in idx_lst:
        b1 = obs[cluster_key] == idx
        if df.loc[idx, 'cmean'] > ut:            
            dec[b1] = 'Tumor'
            df.loc[idx, 'dec'] = 'Tumor'
        elif df.loc[idx, 'cmean'] < lt:
            pass
        else:
            dec[b1] = 'unclear'
            df.loc[idx, 'dec'] = 'unclear'
                
    
    # b = (obs[ref_key].isin(ref_types)) | (s <= th)
    # dec[b] = 'Normal'    
    obs['tumor_dec'+ suffix] = dec
    
    tclust = dec.copy(deep = True)
    tclust[:] = None
    cnt = 1
    for c in idx_lst:
        b = obs[cluster_key] == c
        b1 = dec == 'Tumor'
        if np.sum(b&b1) > 0:
            tclust[b&b1] = 'Tumor_c%i' % cnt
            cnt += 1        
    # obs['tumor_cluster'+ suffix] = tclust

    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        print('INFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
    
    params = {}
    params['th'] = th
    params['m0'] = m0
    params['v0'] = v0
    params['w0'] = w0
    params['m1'] = m1
    params['v1'] = v1
    params['w1'] = w1
    params['df'] = df
    
    if plot_stat:
        plot_stats( params, n_bins = 30, title = None, title_fs = 14,
                    label_fs = 12, tick_fs = 11, legend_fs = 11, 
                    legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                    figsize = (4,3), log = False, alpha = 0.8 )
        
    return obs[['tumor_dec'+ suffix, 'tumor_score'+ suffix]], params


def get_cnv_threshold_useref( obs, ref_ind, ref_ind_org, score_key = 'tumor_score', 
                              cluster_key = 'cnv_leiden', th_max = 0, refp_min = 0.9, 
                              p_exc = 0.1, ucr = 0.1, plot_stat = True, 
                              suffix = '', Data = None, verbose = False ):
    
    th_min = -th_max
    
    ## obs must contain columns 'cnv_cluster', 'cnv_score'
    start_time = time.time()
    
    # df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'median'})
    df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'mean'})
    idx_lst = list(df.index.values)
    
    ns = 0
    # while(ns == 0):
        
    b_inc = []
    df['ref_frac'] = 0
    for idx in idx_lst:
        b = obs[cluster_key] == idx
        cnt = np.sum(np.array(ref_ind)[b])
        ref_percent = cnt/np.sum(b)
        df.loc[idx, 'ref_frac'] = ref_percent
        if (ref_percent >= refp_min):
            b_inc.append(True)
        else:
            b_inc.append(False)

    df['b_inc'] = b_inc    
    b = np.array(b_inc)
    # print(df)

    ns = np.sum(b)
    # if ns == 0: refp_min *= 0.95
    if ns == 0:
        print('ERROR: no reference type clusters found.')
        obs['tumor_prob'+ suffix] = 0
        obs['tumor_dec'+ suffix] = 'NA'
        # obs['tumor_cluster'+ suffix] = ''
        return None
    elif ns == 1:
        print('WARNING: Only one reference type cluster found.')
        cmeans = np.array(df.loc[b,'cmean'])
        th2 = cmeans[0]
        b2 = df['cmean'] <= th2
    else:        
        cmeans = np.array(df.loc[b,'cmean'])
        odr = cmeans.argsort()
        m = int(round(ns*(1-p_exc)))
        if m == len(odr):
            m = m-1
        if m < 0: m = 0
        # print(' ns = %i -> m = %i' % (ns, m))
        th2 = cmeans[odr[m]]
        # th2 = cmeans.max()
        b2 = df['cmean'] <= th2
        if np.sum(b&b2) == 0:
            df2 = df.sort_values(by = 'cmean').iloc[:2]
            th2 = df2['cmean'].max()
            b2 = df['cmean'] <= th2
    
    ns = np.sum(~b)
    if ns > 0:
        cmeans = np.array(df.loc[~b,'cmean'])
        odr = cmeans.argsort()

        m = int(round(ns*(p_exc)))
        if m == len(odr):
            m = m-1
        # print(' ns = %i -> m = %i' % (ns, m))
        th3 = cmeans[odr[m]]
        b3 = df['cmean'] >= max(th3, th2) 
    else:
        th3 = df['cmean'].max()
        b3 = False

    # print(' th2 = %5.2f, th3 = %5.2f' % (th2, th3))
    
    # print(th2, th3)
    
    w0 = np.sum(b&b2)/(len(b)*p_exc)
    m0 = df.loc[b&b2,'cmean'].mean()
    if np.sum(b&b2) > 1:
        v0 = df.loc[b&b2,'cmean'].var()
    #'''
    else:
        idx = df.index.values[b&b2][0]
        bt = obs[cluster_key] == idx
        v0 = obs.loc[bt, score_key].var()
    #'''        

    for k, idx in enumerate(idx_lst):
        if df.loc[idx, 'cmean'] <= (m0 + np.sqrt(v0)):
            b[k] = True
                    
    if np.sum((~b)&b3) > 0:
        w1 = np.sum((~b)&b3)/(len(b)*p_exc)
        m1 = df.loc[(~b)&b3,'cmean'].mean()
        if np.sum((~b)&b3) > 1:
            v1 = df.loc[(~b)&b3,'cmean'].var()
        else:
            idx = df.index.values[(~b)&b3][0]
            bt = obs[cluster_key] == idx
            v1 = obs.loc[bt, score_key].var()
    else:
        w1 = 0
        m1 = np.abs(th3 - m0)*2 + m0 # m0*10
        v1 = v0

    v0, v1 = (v0*0.75 + v1*0.25), (v0*0.25 + v1*0.75)     
        
    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200
    n_bins = 20

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)

    th = -1
    for k in range(len(xs0)):
        if (pdf1[k] >= pdf0[k]) & (xs0[k] > m0):
            th = xs0[k]
            break
            
    ss_div_dm = (np.sqrt(v1)+np.sqrt(v0))/(m1-m0)
    if ss_div_dm > 1:
        if verbose: print('\nINFO: Std_sum/Mean_diff: %f > 1' % (ss_div_dm))
        if verbose: print('INFO: indicating that no tumor cells might be present in this sample.' % (ss_div_dm))
        # th = m0 + np.sqrt(v0)
        
    # print('threshold: ', th )
    th = max(th, th_min)
    th = min(th, th_max)
            
    s = obs[score_key]
    tpr = get_malignancy_prob( s, [w0, m0, v0, w1, m1, v1] )
    
    obs['tumor_prob'+ suffix] = tpr
    
    dec = pd.Series(['Normal']*len(s), index = obs.index)
    '''
    b = s >= th
    dec[b] = 'Tumor'
    dec[~b] = 'Normal'
    '''
    bs = (s > th)
    
    #'''
    lt = th - (th - m0)*ucr # p_exc 
    ut = th + (m1 - th)*ucr #p_exc
    #'''
    
    df['dec'] = 'Normal'
    if ref_ind_org is not None:
        br = np.array(ref_ind)
        for idx in idx_lst:
            b1 = obs[cluster_key] == idx
            if df.loc[idx, 'cmean'] > ut:            
                dec[b1&(~br)] = 'Tumor'
                df.loc[idx, 'dec'] = 'Tumor'
            elif df.loc[idx, 'cmean'] < lt:
                pass
            else:
                dec[b1&(~br)] = 'unclear'
                df.loc[idx, 'dec'] = 'unclear'
    else:
        for idx in idx_lst:
            b1 = obs[cluster_key] == idx
            if df.loc[idx, 'cmean'] > ut:            
                dec[b1] = 'Tumor'
                df.loc[idx, 'dec'] = 'Tumor'
            elif df.loc[idx, 'cmean'] < lt:
                pass
            else:
                dec[b1] = 'unclear'
                df.loc[idx, 'dec'] = 'unclear'
                    
    '''
    if ref_ind_org is not None:
        df_tmp = df.copy(deep = True)        
        b_inc = []
        for idx in idx_lst:
            b = obs[cluster_key] == idx
            cnt = np.sum(np.array(ref_ind_org)[b])
            ref_percent = cnt/np.sum(b)
            if (ref_percent >= refp_min):
                b_inc.append(True)
            else:
                b_inc.append(False)

        df_tmp['b_inc'] = b_inc        
        b = df_tmp['b_inc']
        normal_max = df_tmp.loc[b, 'cmean'].max()

        b = (df_tmp['b_inc'] == False) & (df_tmp['cmean'] > normal_max) \
            & ((df_tmp['dec'] == 'Normal') | (df_tmp['dec'] == 'unclear'))
        if np.sum(b) > 0:
            name_set = 'Tumor'
            df.loc[b, 'dec'] = name_set 
            for c in list(df.index.values[b]):
                b = obs[cluster_key] == c
                dec[b] = name_set
    #'''
    
    if ss_div_dm > 1:
        b = dec == 'Tumor'
        if verbose: 
            print('INFO: %i among %i were identified as tumor cells.' \
                  % (np.sum(b), len(b)))
    
    obs['tumor_dec'+ suffix] = dec

    tclust = dec.copy(deep = True)
    tclust[:] = 'Normal'
    cnt = 1
    for c in idx_lst:
        b = obs[cluster_key] == c
        b1 = dec == 'Tumor'
        if np.sum(b&b1) > 0:
            tclust[b&b1] = 'Tumor_c%i' % cnt
            cnt += 1        
    obs['tumor_cluster'+ suffix] = tclust
    
    etime = round(time.time() - start_time) 
    # print('CNVth(%i) ' % etime, end = '', flush = True)
    
    params = {}
    params['th'] = th
    params['th_lower'] = lt
    params['th_upper'] = ut
    params['m0'] = m0
    params['v0'] = v0
    params['w0'] = w0
    params['m1'] = m1
    params['v1'] = v1
    params['w1'] = w1
    params['df'] = df
    
    if plot_stat:
        plot_stats( params, n_bins = 30, title = None, title_fs = 14,
                    label_fs = 12, tick_fs = 11, legend_fs = 11, 
                    legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                    figsize = (4,3), log = False, alpha = 0.8 )
        
    return obs[['tumor_dec'+ suffix, 'tumor_prob'+ suffix]], params
    # return obs[['tumor_dec'+ suffix, 'tumor_prob'+ suffix, 'tumor_cluster'+ suffix]], params


def merge_communities( communities ):
    
    cm = copy.deepcopy(communities)
    to_del = []
    for j in reversed(range(len(cm))):
        if j > 0:
            for k in range(j):
                c = list(set(cm[k]).intersection(cm[j]))
                if len(c) > 0:
                    cm[k] = list(set(cm[k]).union(cm[j]))
                    to_del.append(j)
                    break
                    
    for j in to_del:
        del cm[j]
        
    ss = []
    for j, c in enumerate(cm):
        c.sort()
        cm[j] = c
        ss.append(-len(c))
    
    ss = np.array(ss)
    odr = ss.argsort()
    
    return cm[odr[0]]


def extend_major_clusters( adj_agg_mat, seed_clusters, 
                           cluster_size, n_neighbors, alpha = 0.08, 
                           pv_cutoff = None, mode = 'max', 
                           verbose = False ):

    selected_clusters = copy.deepcopy(seed_clusters)
    maj_clusters = copy.deepcopy(seed_clusters)
    pair_clusters = list(np.zeros(len(seed_clusters)))
    metrics = list(np.zeros(len(seed_clusters)))
    thresholds = list(np.zeros(len(seed_clusters)))
    
    csz_lst = [cluster_size[n] for n in maj_clusters]
    odr = (-np.array(csz_lst)).argsort()
    maj_clusters = [maj_clusters[o] for o in odr]
    
    core_mat = adj_agg_mat[maj_clusters, :][:,maj_clusters]

    for j, n in enumerate(maj_clusters):
        cnt_n = adj_agg_mat[maj_clusters,n]                
        odr = np.array(cnt_n).argsort()
        p = maj_clusters[int(odr[-1])]
        if mode == 'max':
            met = (adj_agg_mat[p,n]/n_neighbors)
        else:
            met = (np.sum(cnt_n)/n_neighbors)
        pair_clusters[j] = p
        metrics[j] = met
        thresholds[j] = met/min(cluster_size[n], cluster_size[p])
    
    
    flag = True
    for a in range(adj_agg_mat.shape[0] - len(seed_clusters)):
        
        core_mat = adj_agg_mat[maj_clusters, :][:,maj_clusters]
        if mode == 'max':
            core_mxs = core_mat.max(axis = 1)
        else:
            core_mxs = core_mat.sum(axis = 1)
        
        core_dm = np.mean(core_mxs)
        core_ds = np.std(core_mxs)
        
        met = []
        nodes = []
        pair = []
        csz_lst = []
        for n in range(adj_agg_mat.shape[0]):

            if n not in maj_clusters:
                cnt_n = adj_agg_mat[maj_clusters,n]                
                odr = np.array(cnt_n).argsort()
                nodes.append(n)
                p = maj_clusters[int(odr[-1])]
                pair.append(p)
                csz_lst.append(cluster_size[n])
                if mode == 'max':
                    met.append(adj_agg_mat[p,n]/n_neighbors)
                else:
                    met.append(np.sum(cnt_n)/n_neighbors)
              
        cnt = 0
        med_cluster_size = 0 # np.median(csz_lst)
        for md, cn, pp, cs in zip(met, nodes, pair, csz_lst):

            if cs >= med_cluster_size:
                if alpha is not None:
                    csz = md/min(cluster_size[cn], cluster_size[pp])
                    condition = (csz >= (alpha))
                else:
                    st = np.abs(core_dm - md)/(core_ds)
                    pv = stats.t.sf(st*np.sqrt(2), df = 1)*2
                    condition = pv >= pv_cutoff
                    csz = pv

                if flag & condition:
                    maj_clusters.append(cn)
                    pair_clusters.append(pp)
                    metrics.append(md)
                    thresholds.append(csz)
                    selected_clusters = copy.deepcopy(maj_clusters)
                    cnt += 1
                    if verbose: print('A', cn, pp, '%4i' % int(md), cluster_size[cn]) 
                    
        if len(selected_clusters) == len(cluster_size): break
        
        if cnt == 0:
            flag = False
            for md, cn, pp, cs in zip(met, nodes, pair, csz_lst):

                if alpha is not None:
                    csz = md/min(cluster_size[cn], cluster_size[pp])
                    condition = (csz >= (alpha))
                else:
                    st = np.abs(core_dm - md)/(core_ds)
                    pv = stats.t.sf(st*np.sqrt(2), df = 1)*2
                    condition = pv >= pv_cutoff
                    csz = pv

                if verbose: print('B', cn, pp, '%4i' % int(md), cluster_size[cn], selected_clusters) 
                # break
                maj_clusters.append(cn)
                pair_clusters.append(pp)
                metrics.append(md)
                thresholds.append(csz)
                pass
                    
        if len(maj_clusters) >= len(cluster_size): break
        
    core_mat = adj_agg_mat[maj_clusters, :][:,maj_clusters]
    if mode == 'max':
        core_mxs = core_mat.max(axis = 1)
    else:
        core_mxs = core_mat.sum(axis = 1)
    
    return (np.array(selected_clusters), 
           np.array(maj_clusters), np.array(pair_clusters), metrics, thresholds)


def initially_detect_major_clusters( adj_agg_mat, 
                           cluster_size, n_neighbors, alpha = 0.08, 
                           pv_cutoff = None, mode = 'max', 
                           verbose = False ):

    cluster_lst = list(np.arange(len(cluster_size)))
    
    selected_clusters = []
    for c in cluster_lst:
        seed_clusters = [c]
        selected, maj, pairs, mets, threshs = \
            extend_major_clusters( adj_agg_mat, seed_clusters, 
                           cluster_size, n_neighbors, alpha = 0.08, 
                           pv_cutoff = None, mode = 'max', 
                           verbose = False )
        
        if len(selected) > len(selected_clusters):
            selected_clusters = copy.deepcopy(selected)
            
    return selected_clusters


import warnings

def run_icnv(adata, ref_key, ref_types, gtf_file, cluster_key = 'cnv_leiden', 
             resolution = 2, N_pca = 15, n_neighbors = 10, umap = True, 
             pca = True, n_cores = 4, verbose = False ):
    
    pca_umap = umap
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    
        ## Normalize and log-transform
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)

        sc.pp.highly_variable_genes(adata, n_top_genes = 2000) # , flavor = 'seurat_v3')

        # 출력을 숨기기 위해 /dev/null로 리디렉션
        log_level = logging.getLogger().getEffectiveLevel()
        logging.basicConfig(level=logging.ERROR)

        # 출력을 숨기기 위해 /dev/null로 리디렉션
        null_file = open(os.devnull, 'w')
        save_stdout = sys.stdout
        save_stderr = sys.stderr
        sys.stdout = null_file
        sys.stderr = null_file

        # with open(os.devnull, 'w') as fnull:
        #     with redirect_stdout(fnull), redirect_stderr(fnull):
        cnv.io.genomic_position_from_gtf(gtf_file, adata, gtf_gene_id='gene_name', 
                                         adata_gene_id=None, inplace=True)
        cnv.tl.infercnv(adata, reference_key = ref_key, reference_cat=ref_types, 
                        window_size=100, n_jobs = n_cores)
                
        #'''
        # 출력을 복원
        sys.stdout = save_stdout
        sys.stderr = save_stderr
        null_file.close()

        logging.getLogger().setLevel(log_level)
        # logging.getLogger().setLevel(logging.NOTSET)    
        #''' 

        if pca:
            if verbose: print('PCA .. ', end = '')
            cnv.tl.pca(adata, n_comps = N_pca) 
        
        if umap:
            if verbose: print('Finding neighbors .. ', end = '')
            cnv.pp.neighbors(adata, key_added = 'cnv_neighbors', n_neighbors=n_neighbors, n_pcs=N_pca)
            if verbose: print('Clustering .. ', end = '')
            cnv.tl.leiden(adata, neighbors_key='cnv_neighbors', key_added=cluster_key, resolution = resolution)
            if verbose: print('UMAP .. ', end = '')
            cnv.tl.umap(adata)
            
            if verbose: print('Scoring .. ', end = '')
            cnv.tl.cnv_score(adata, groupby = cluster_key, key_added = 'cnv_score')
            
        if verbose: print('done.')

    return adata



from sklearn.decomposition import PCA
from sklearn import cluster, mixture
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import kneighbors_graph
from sklearn.neighbors import NearestNeighbors

CLUSTERING_AGO = 'lv'
SKNETWORK = True
try:
    from sknetwork.clustering import Louvain
except ImportError:
    print('WARNING: sknetwork not installed. GMM will be used for clustering.')
    CLUSTERING_AGO = 'km'
    SKNETWORK = False

    
def clustering_alg(X_pca, clust_algo = 'lv', N_clusters = 25, resolution = 1, N_neighbors = 10, 
                   mode='connectivity', n_cores = 4):
                   # mode='distance', n_cores = 4):
    
    adj = None
    if clust_algo[:2] == 'gm':
        gmm = mixture.GaussianMixture(n_components = int(N_clusters), random_state = 0)
        cluster_label = gmm.fit_predict(np.array(X_pca))
        return cluster_label, gmm, adj
    elif clust_algo[:2] == 'km':
        km = cluster.KMeans(n_clusters = int(N_clusters), random_state = 0)
        km.fit(X_pca)
        cluster_label = km.labels_
        return cluster_label, km, adj
    else:
        adj = kneighbors_graph(X_pca, int(N_neighbors), mode=mode, include_self=True, 
                               n_jobs = n_cores)
        louvain = Louvain(resolution = resolution, random_state = 0)
        if hasattr(louvain, 'fit_predict'):
            cluster_label = louvain.fit_predict(adj)        
        else:
            cluster_label = louvain.fit_transform(adj)        
        return cluster_label, louvain, adj
    '''
    elif clust_algo[:2] == 'ld':
        leiden = LeidenClustering()
        leiden.fit(X)
        cluster_label = leiden.labels_
        return cluster_label, km
    '''

    
def get_neighbors(adj, n_neighbors):
    
    rows = adj.tocoo().row
    cols = adj.tocoo().col
    data = adj.data    
    
    N = int(np.max(rows) + 1)
    neighbors = np.full([N, n_neighbors], -1)
    distances = np.full([N, n_neighbors], -1)
    cnts = np.zeros(N, dtype = int)
    
    for r, c, d in zip(rows, cols, data):
        neighbors[r, cnts[r]] = c
        distances[r, cnts[r]] = d
        cnts[r] += 1
        
    for i in range(N):
        odr = distances[i,:].argsort()
        distances[i,:] = distances[i,odr]
        neighbors[i,:] = neighbors[i,odr]
        
    return neighbors, distances
    

def set_cluster_for_others_v01( ilst, labels, neighbors, distances ):
    
    label_lst = list(set(labels))
    label_lst.sort()
    label_array = np.array(labels)
    iary = np.array(ilst)
    label_all = np.full(neighbors.shape[0], -1)
    
    for c in label_lst:
        b = label_array == c
        lst = list(iary[b])
        lst_ext = copy.deepcopy(lst)
        for i in lst:
            lst_ext = lst_ext + list(neighbors[i,:])
        lst_ext = list(set(lst_ext))
        label_all[lst_ext] = c
        
    return label_all

def set_cluster_for_others( ilst, labels, neighbors, distances ):
    
    label_lst = list(set(labels))
    label_lst.sort()
    label_array = np.array(labels)
    iary = np.array(ilst)
    label_all = np.full(neighbors.shape[0], -1)
    label_all[ilst] = labels
    
    b1 = label_all < 0
    nn = np.sum(b1)
    
    for j in range(neighbors.shape[1]):
        for k in range(len(label_all)):
            nlst = list(neighbors[b1,j])
            label_sel = label_all[nlst]
            label_all[b1] = label_sel

            b1 = label_all < 0
            # print(np.sum(b1))
            if (np.sum(b1) == 0) | (nn == np.sum(b1)):
                break
            else:
                nn = np.sum(b1)

        b1 = label_all < 0
        # print(np.sum(b1), 'AA')
        if (np.sum(b1) == 0):
            break
        
    return label_all


def clustering_subsample( X_vec, neighbors = None, distances = None, 
                          clust_algo = 'lv', N_clusters = 25, resolution = 1, N_neighbors = 10, 
                          mode='connectivity', n_cores = 4, Ns = 10000, Rs = 0.95 ):

    method = clust_algo
    Ns = int(min(Ns, X_vec.shape[0]*Rs))

    adj = None
    if (neighbors is None) | (distances is None):
        start = time.time()
        adj = kneighbors_graph(X_vec, int(N_neighbors), mode = 'distance', # 'connectivity', 
                           include_self=False, n_jobs = 4)
        neighbors, distances = get_neighbors(adj, N_neighbors)
        lapsed = time.time() - start
        # print(lapsed, len(list(set(list(labels)))))
    
    lst_full = list(np.arange(X_vec.shape[0]))
    lst_sel = random.sample(lst_full, k= Ns)

    Xs = X_vec[lst_sel,:]

    start = time.time()
    labels, obj, adj_tmp = clustering_alg(Xs, clust_algo = method, N_clusters = N_clusters, 
                                          resolution = resolution, N_neighbors = N_neighbors, 
                                          mode='connectivity', n_cores = 4)

    lapsed = time.time() - start
    # print(lapsed, len(list(set(list(labels)))))

    label_all = set_cluster_for_others( lst_sel, labels, neighbors, distances )

    return label_all, obj, adj



def get_cluster_stat( obs, ref_ind, cluster_key = 'cnv_cluster', 
                      score_key = 'tumor_score', refp_min = 0.9):
    
    # df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'median'})
    df = obs.groupby([cluster_key])[score_key].agg(**{'cmean':'mean'})
    idx_lst = list(df.index.values)
    
    ns = 0
    # while(ns == 0):
        
    b_inc = []
    df['ref_frac'] = 0
    for idx in idx_lst:
        b = obs[cluster_key] == idx
        # cts = obs.loc[b, ref_key]
        '''
        ct_vc = cts.value_counts()
        cnt = 0
        for ct in list(ct_vc.index.values):
            if ct in ref_types:
                cnt += ct_vc[ct]
        '''
        cnt = np.sum(np.array(ref_ind)[b])
        ref_percent = cnt/np.sum(b)
        df.loc[idx, 'ref_frac'] = ref_percent
        if (ref_percent >= refp_min):
            b_inc.append(True)
        else:
            b_inc.append(False)

    df['b_inc'] = b_inc
    b = np.array(b_inc)
    # print(df)
    return df


def find_num_clusters( N, Clustering_resolution = 1 ):
    return int(max(((N*(Clustering_resolution**2))**(1/6))*5, 10))

def merge_small_clusters( adj_agg_mat, cluster_size, alpha, min_cluster_size = 100 ):
    
    b = np.array(cluster_size) < min_cluster_size
    if np.sum(b) == 0:
        return None
    else:
        dct = {}
        clst = list(np.arange(len(cluster_size))[b])
        for c in clst:
            met = adj_agg_mat[:,c]
            odr = met.argsort()
            md = met[odr[-1]]
            csz = md/cluster_size[c]
            if csz >= (alpha):
                dct[c] = odr[-1]
            
        return dct    

'''
    df_res, summary, cobj, X_pca = identify_tumor_cells(X_cnv, ref_ind, pca = pca, clust = None, 
                           use_cnv_score = False, Clustering_algo = clustering_algo, 
                           Clustering_resolution = clustering_resolution, N_clusters = 30,
                           gmm_N_comp = 20, th_max = tumor_dec_th_max, refp_min = 0.9, p_exc = 0.1, 
                           dec_margin = tumor_dec_margin, n_neighbors = 10, cmd_cutoff = cmd_cutoff, 
                           gcm = gcm, plot_stat = False, use_ref = use_ref_only, N_cells_max_for_clustering = 10000,
                           connectivity_thresh = connectivity_threshold, net_search_mode = net_search_mode,
                           suffix = '', Data = None, n_cores = n_cores, verbose = verbose, use_umap = use_umap)
                           
    df = scoda_icnv_addon( adata_t, gtf_file, 
                           ref_types = ref_types, 
                           ref_key = "celltype_major", 
                           use_ref_only = False, 
                           clustering_algo = 'lv', clustering_resolution = 1, 
                           n_cores = n_cores_to_use, 
                           connectivity_threshold = 0.1, verbose = False, 
                           use_umap = False, tumor_dec_th_max = 5, tumor_dec_margin = 0.01, 
                           net_search_mode = 'max', cmd_cutoff = 0.03, gcm = 0.3 )
                           
'''
    
def identify_tumor_cells(X_cnv, ref_ind, pca = False, use_cnv_score = False, clust = None, 
                         Clustering_algo = 'lv', Clustering_resolution = 1, N_clusters = 30,
                         # cluster_key = 'cnv_leiden', score_key = 'tumor_score', 
                         gmm_N_comp = 20, th_max = 5, refp_min = 0.9, p_exc = 0.1, 
                         dec_margin = 0.05, n_neighbors = 10, cmd_cutoff = 0.03, N_loops = 1,
                         gcm = 0.3, plot_stat = False, use_ref = False, N_cells_max_for_clustering = 10000,
                         n_cores = 4, connectivity_thresh = 0.1, net_search_mode = 'max', 
                         suffix = '', Data = None, verbose = False, use_umap = False):
    
    N_clusters = find_num_clusters( X_cnv.shape[0], Clustering_resolution )
    if verbose: 
        if Clustering_algo != 'lv':
            print('Clustering using %s with N_clusters = %i. ' % (Clustering_algo.upper(), N_clusters))
    
    ## Remove all zero X_cnv
    X_cnv_mean = np.array(X_cnv.sum(axis = 1))
    b = X_cnv_mean == 0
    if np.sum(b) > 0:
        # print(np.sum(b))
        odr = np.array(X_cnv_mean).argsort()
        o_min = odr[int(np.sum(b))]
        x_cnv = X_cnv[o_min,:]
        idxs = np.arange(X_cnv.shape[0])[list(b)]
        for i in idxs:
            X_cnv[i,:] = x_cnv
            
    ref_addon = None
    score_key = 'tumor_score' + suffix
    cluster_key = 'cnv_cluster' 
    
    ##########
    ## PCA ###
    start_time = time.time()
    start_time_a = start_time
    if verbose: 
        print('Running iCNV addon .. ', end = '', flush = True)
    
    if isinstance(X_cnv, pd.DataFrame):
        df = pd.DataFrame(index = X_cnv.index.values)
    else:
        df = pd.DataFrame()
        X_cnv = pd.DataFrame(X_cnv)
    
    N_components_pca = 15
    pca_obj = TruncatedSVD(n_components = int(N_components_pca), random_state = 0) # , algorithm = 'arpack')
    
    if not pca: 
        X_pca = pca_obj.fit_transform(X_cnv)
        if use_umap:
            umap_obj = umap.UMAP(random_state=0)
            X_vec = umap_obj.fit_transform(X_pca)
        else: 
            X_vec = copy.deepcopy(X_pca)
        
        etime = round(time.time() - start_time) 
        if verbose: print('P(%i) .. ' % etime, end = '', flush = True)
        start_time = time.time()           
    else: 
        X_pca = np.array(X_cnv.copy(deep = True)) #.copy(deep = True)
        if use_umap:
            umap_obj = umap.UMAP(random_state=0)
            X_vec = umap_obj.fit_transform(X_pca)
        else: 
            X_vec = copy.deepcopy(X_pca)

    ## Get neighbor lst and dst
    start = time.time()
    adj = kneighbors_graph(X_vec, int(n_neighbors), mode = 'distance', # 'connectivity', 
                       include_self=False, n_jobs = 4)
    neighbors, distances = get_neighbors(adj, n_neighbors)
    lapsed = time.time() - start
    
    if ref_ind is not None:
        X_vec_sel = X_vec[~ref_ind, :]            
        adj_sel = kneighbors_graph(X_vec_sel, int(n_neighbors), mode = 'distance', # 'connectivity', 
                           include_self=False, n_jobs = 4)
        neighbors_sel, distances_sel = get_neighbors(adj_sel, n_neighbors)
        N_cs = find_num_clusters( np.sum(~ref_ind), Clustering_resolution )
        
        X_vec_ref = X_vec[ref_ind, :]
        adj_ref = kneighbors_graph(X_vec_ref, int(n_neighbors), mode = 'distance', # 'connectivity', 
                           include_self=False, n_jobs = 4)
        neighbors_ref, distances_ref = get_neighbors(adj_ref, n_neighbors)
        N_cr = find_num_clusters( np.sum(ref_ind), Clustering_resolution )
        
    etime = round(time.time() - start_time) 
    if verbose: print('A(%i) .. ' % (etime), end = '', flush = True)
    start_time = time.time()
    
    ################
    ## Clustering ##
    for crun in range(N_loops):

        # start_time = time.time()
        if ref_ind is None: 
            y_clust, cobj, adj_t = clustering_subsample( X_vec, neighbors, distances, 
                                                       clust_algo = Clustering_algo, N_clusters = N_clusters, 
                                                       resolution = Clustering_resolution, N_neighbors = n_neighbors, 
                                                       mode='connectivity', n_cores = n_cores, 
                                                       Ns = N_cells_max_for_clustering, Rs = 0.95 )        
            N_clusters = int(np.max(y_clust) + 1)
        else:            
            y_clust_sel, cobj, adj_s = clustering_subsample( X_vec_sel, neighbors_sel, distances_sel, 
                                                           clust_algo = Clustering_algo, N_clusters = N_cs, 
                                                           resolution = Clustering_resolution, N_neighbors = n_neighbors, 
                                                           mode = 'connectivity', n_cores = n_cores, 
                                                           Ns = N_cells_max_for_clustering, Rs = 0.95 )

            y_clust_ref, cobj, adj_r = clustering_subsample( X_vec_ref, neighbors_ref, distances_ref, 
                                                           clust_algo = Clustering_algo, N_clusters = N_cr, 
                                                           resolution = Clustering_resolution, N_neighbors = n_neighbors, 
                                                           mode = 'connectivity', n_cores = n_cores, 
                                                           Ns = N_cells_max_for_clustering, Rs = 0.95 )

            y_clust = np.zeros(X_vec.shape[0], dtype = int)
            y_clust[ref_ind] = y_clust_ref
            y_clust[~ref_ind] = y_clust_sel + (1 + np.max(y_clust_ref))         
            N_clusters = N_cs + N_cr

        # etime = round(time.time() - start_time) 
        # print('C(%i, Nc:%i) .. ' % (etime, N_clusters), end = '', flush = True)
        # start_time = time.time()

        ## Compute Cluster size, Aggregated Adj.Mat and Merge Small clusters 
        cnv_clust_lst = list(set(y_clust))

        for kk in range(len(cnv_clust_lst)):

            cnv_clust_lst = list(set(y_clust))
            cnv_clust_lst.sort()

            cluster_size = [] 
            for c in cnv_clust_lst:
                b = y_clust == c
                cluster_size.append(np.sum(b))

            ## Generate agg_adj_mat
            if (ref_ind is None) & (Clustering_algo == 'lv'):
                adj_agg = cobj.aggregate_
                adj_agg_mat = np.array(adj_agg.todense().astype(int)) 
            else:
                rows = adj.tocoo().row
                cols = adj.tocoo().col
                vals = adj.data

                adj_agg_mat = np.zeros([len(cnv_clust_lst), len(cnv_clust_lst)], dtype = int)
                for r, c, v in zip(rows, cols, vals):
                    adj_agg_mat[y_clust[r],y_clust[c]] += 1

                adj_agg_mat = adj_agg_mat - np.diag(np.diag(adj_agg_mat))
                adj_agg_mat = adj_agg_mat + adj_agg_mat.transpose()

            if np.min(cluster_size) >= 100:
                break
            else:
                ## Merge small clusters to a closest one
                cc_dct = merge_small_clusters( adj_agg_mat, cluster_size, 
                                               alpha = connectivity_thresh, min_cluster_size = 100 )
                if cc_dct is not None:
                    for ck in cc_dct.keys():
                        b = y_clust == ck
                        y_clust[b] = cc_dct[ck]

                    ## Re-numbering
                    cnv_clust_lst = list(set(y_clust))
                    cnv_clust_lst.sort()
                    y_clust_new = np.zeros(X_vec.shape[0], dtype = int)
                    for j, c in enumerate(cnv_clust_lst):
                        b = y_clust == c
                        y_clust_new[b] = j
                    y_clust = y_clust_new
                else:
                    break


        ## Find seed clusters
        cluster_sel = None

        if ref_ind is None: 
            cluster_sel = initially_detect_major_clusters( adj_agg_mat, 
                               cluster_size, n_neighbors, alpha = connectivity_thresh, 
                               pv_cutoff = None, mode = net_search_mode, 
                               verbose = verbose )
        else:
            b = ref_ind
            b_inc = []
            for idx in cnv_clust_lst:
                b = y_clust == idx
                bt = b & ref_ind
                cnt = np.sum(bt)

                if (cnt >= refp_min*np.sum(b)):
                    b_inc.append(True)
                else:
                    b_inc.append(False)

            if np.sum(b_inc) > 0:
                cluster_sel = list(np.array(cnv_clust_lst)[b_inc]) 
            else:
                print('ERROR: No reference cell types found.')
                return 

        seed_clusters = copy.deepcopy(cluster_sel)
        cluster_sel, cluster_odr, pair_cluster, strength_odr, threshold_odr = \
                extend_major_clusters(adj_agg_mat, cluster_sel, cluster_size, 
                                      n_neighbors = n_neighbors, 
                                      alpha = connectivity_thresh, pv_cutoff = None, 
                                      mode = net_search_mode, verbose = verbose )

        b = y_clust == cluster_sel[0]
        if len(cluster_sel) > 1:
            for c in cluster_sel[1:]:
                b = b | (y_clust == c)
        ref_ind2 = b

        if crun == 0:
            ref_ind_all = [ref_ind2]
        else:
            ref_ind_all.append(ref_ind2)
    ## End For    
    
    ref_ind_all = np.array(ref_ind_all)
    if N_loops == 0:
        ref_ind2 = ref_ind_all[0,:]
    else:
        ref_ind2 = ref_ind_all.sum(axis = 0) > (N_loops/2)

    etime = round(time.time() - start_time) 
    if verbose: 
        if ref_ind is None: 
            print('CNS(%i) N_ref: %i .. ' % \
                  (etime, np.sum(ref_ind2)), end = '')
        else:
            print('CNS(%i) N_ref: %i -> %i .. ' % \
                  (etime, np.sum(ref_ind), np.sum(ref_ind2)), end = '')
    #'''
    df[cluster_key] = y_clust
    
    start_time = time.time()

    ## Find cluster score
    abs_X_cnv = np.sqrt(X_cnv**2)
    '''
    Nn = int(X_cnv.shape[1]*0.85)
    abs_X_cnv = np.sort((abs_X_cnv), axis = 1)[:,Nn:]
    print('abs_X_cnv shape: ', abs_X_cnv.shape)
    '''
    y_conf = (abs_X_cnv.mean(axis = 1))*100
        
    cluster_scores = []
    for c in cnv_clust_lst:
        b = y_clust == c
        cluster_scores.append(y_conf[b].mean())
           
    X_vec_sel = X_vec[ref_ind2,:]
    
    if X_vec_sel.shape[0] > N_cells_max_for_clustering:
        idxs = list(np.arange(X_vec_sel.shape[0]))
        idxs = random.sample(idxs, k = N_cells_max_for_clustering)
        X_vec_sel = X_vec_sel[idxs,:]
        
    gmm_N_comp = find_num_clusters( np.sum(ref_ind2), Clustering_resolution )
    
    gmm = mixture.GaussianMixture(n_components = int(gmm_N_comp), random_state = 0)
    gmm.fit(X_vec_sel)
    y_conf_gmm = -gmm.score_samples(X_vec)
    #'''

    MIN_VAL = 1e-10
    df['tumor_score'] = np.log((y_conf)*(1/(1+np.exp(-y_conf_gmm*gcm))) + MIN_VAL) 
    # df['tumor_score'] = ((y_conf)*(1/(1+np.exp(-y_conf_gmm*gcm))) + MIN_VAL) 
    df['y_conf'] = y_conf
    df['y_conf_gmm'] = y_conf_gmm
    df['tumor_prob'] = (1/(1+np.exp(-y_conf_gmm*gcm)))
    df['tumor_dec'] = 'Normal'
    b = df[score_key] > 0
    df.loc[b, 'tumor_dec'] = 'Tumor'
    if N_loops == 0:
        df['ref_ind_score'] = ref_ind_all[0,:]
    else:
        df['ref_ind_score'] = ref_ind_all.mean(axis = 0)

    etime = round(time.time() - start_time) 
    if verbose: print('G(%i) .. ' % etime, end = '', flush = True)
    start_time = time.time()
    
    #'''
    dft, td_params = get_cnv_threshold_useref( df, ref_ind2, ref_ind,
                                       score_key = score_key, cluster_key = cluster_key,
                                       th_max = th_max, refp_min = refp_min, p_exc = p_exc, 
                                       ucr = dec_margin, plot_stat = plot_stat, 
                                       suffix = suffix, Data = Data )
    #'''
    
    summary = {}
    summary['tumor_dec_params'] = td_params
    summary['adj_mat'] = adj
    summary['agg_adj_mat'] = adj_agg_mat
    summary['connectivity_threshold'] = connectivity_thresh
    
    # df_res = get_cluster_stat( df, ref_ind2, cluster_key = 'cnv_cluster', 
    #                            score_key = 'tumor_score', refp_min = 0.9)
    td_params['df'].rename(columns = {'dec': 'tumor_dec'}, inplace = True)
    df_res = td_params['df'].copy(deep = True)
    
    df_res['cluster_size'] = cluster_size
    df_res['cluster_score'] = cluster_scores
    df_res['seed'] = False
    for c in seed_clusters:
        df_res.loc[c, 'seed'] = True
    df_res['selected'] = False
    df_res.loc[cluster_sel, 'selected'] = True
    df_res['selection_order'] = -1
    df_res['paired_cluster'] = -1
    df_res['edge_wgt'] = -1
    df_res['threshold'] = -1
    for j, (c, p, v, u) in enumerate(zip(cluster_odr, pair_cluster, strength_odr, threshold_odr)): 
        df_res.loc[c, 'selection_order'] = j
        df_res.loc[c, 'paired_cluster'] = p
        df_res.loc[c, 'edge_wgt'] = v
        df_res.loc[c, 'threshold'] = u
    df_res.drop(columns = 'b_inc', inplace = True)
    summary['cnv_cluster_info'] = df_res    
    
    etime = round(time.time() - start_time_a) 
    if verbose: print('done (%i) ' % etime) 
    
    return df, summary, cobj, X_pca


def plot_td_stats( params, n_bins = 30, title = None, title_fs = 14,
                   label_fs = 12, tick_fs = 11, legend_fs = 11, 
                   legend_loc = 'upper left', bbox_to_anchor = (1, 1),
                   figsize = (4,3), log = True, alpha = 0.8 ):
    
    th = params['th']
    m0 = params['m0']
    v0 = params['v0']
    w0 = params['w0']
    m1 = params['m1']
    v1 = params['v1']
    w1 = params['w1']
    df = params['df']
        
    mxv = df['cmean'].max()
    mnv = df['cmean'].min()
    Dv = mxv - mnv
    dv = Dv/200

    x = np.arange(mnv,mxv,dv)
    pdf0, xs0 = get_normal_pdf( x, m0, v0, 100)
    pdf1, xs1 = get_normal_pdf( x, m1, v1, 100)
    
    pr = pdf1/(pdf1 + pdf0) # get_malignancy_prob( xs0, [w0, m0, v0, w1, m1, v1] )
    bx = (xs0 >= m0) & ((xs1 <= m1))

    nn = len(df['cmean'])
    pdf0 = pdf0*(w0*nn*(200/n_bins)/pdf0.sum())
    pdf1 = pdf1*(w1*nn*(200/n_bins)/(pdf1.sum())) 

    max_pdf = max(pdf0.max(), pdf1.max())
    
    plt.figure(figsize = figsize)
    ax = plt.gca()
    
    counts, bins = np.histogram(df['cmean'], bins = n_bins)
    # max_cnt = np.max(counts)

    legend_labels = []
    
    max_cnt = 0
    b = df['tumor_dec'] == 'Normal'
    if np.sum(b) > 0:
        legend_labels.append('Normal')
        counts, bins_t, bar_t = plt.hist(df.loc[b, 'cmean'], bins = bins, alpha = alpha)
        max_cnt = max(max_cnt, np.max(counts))
    b = df['tumor_dec'] == 'Tumor'
    if np.sum(b) > 0:
        legend_labels.append('Tumor')
        counts, bins_t, bar_t = plt.hist(df.loc[b, 'cmean'], bins = bins, alpha = alpha)
        max_cnt = max(max_cnt, np.max(counts))
    b = df['tumor_dec'] == 'unclear'
    if np.sum(b) > 0:
        legend_labels.append('unclear')
        counts, bins_t, bar_t = plt.hist(df.loc[b, 'cmean'], bins = bins, alpha = alpha)
        max_cnt = max(max_cnt, np.max(counts))
    
    sf = 0.9*max_cnt/max_pdf
    plt.plot(xs0, pdf0*sf)
    plt.plot(xs1, pdf1*sf)
    plt.plot([th, th], [0, max_cnt]) # max(pdf0.max()*sf, pdf1.max()*sf)])
    plt.plot(xs0[bx], pr[bx]*max_cnt)

    if title is not None: plt.title(title, fontsize = title_fs)
    plt.xlabel('CNV_score', fontsize = label_fs)
    plt.ylabel('Number of clusters', fontsize = label_fs)
    plt.legend(['Normal distr.', 'Tumor distr.', 'Threshold', 'Tumor Prob.'], #, 'Score hist.'], 
               loc = legend_loc, bbox_to_anchor = bbox_to_anchor, fontsize = legend_fs)
    if log: plt.yscale('log')
    ax.tick_params(axis='x', labelsize=tick_fs)
    ax.tick_params(axis='y', labelsize=tick_fs)
    plt.grid()
    plt.show()
        
    return 
    