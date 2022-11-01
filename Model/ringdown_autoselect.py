# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:13:18 2022

@author: denho
"""
import numpy as np
import scipy.signal as scs
import pwlf

def zerocrossings(array) -> np.ndarray:
    """
    When a one-dimensional array is given returns the indeces of zero-crossings.

    Parameters
    ----------
    array : list,ndarray
        One-dimensional array.

    Returns
    -------
    ndarray
        Array containing indeces of zero-crossings.

    """
    return np.where(np.diff(np.sign(array)))[0] 
 

def autoselect(x,
            y,
            n_segments_max=5,
            convergence_tresh = 2/3,
            edge_inclusion = 10,
            slope_scan = 5,
            err_cutoff = 10,
            dy_cutoff0 = 1,
            dy_cutoff1 = 10,
            minslope = 0,
            min_dy = 5,
            min_dx = .1):
    """
    Function for autofitting a ringdown measurement. The method is not perfect, 
    but in most instances performs pretty well.

    Parameters
    ----------
    x : array
        [s] Time data.
    y : array
        [dB] Amplitude data.
    n_segments_max : int, optional
        Maximum number of line segments for piecewise linear fit. Larger 
        numbers may lead to long fitting times. The default is 5.
    convergence_tresh : float, optional
        Relative convergence value for piecewise linear fit. Must be between 0 
        and 1. Larger values may lead to longer fitting times The default is 
        2/3.
    edge_inclusion : int, optional
        Extra number of data points added into initial sub-segment of data. The 
        default is 10.
    slope_scan : float, optional
        [dB] Slope detection value. Must be larger than 0. The default is 5 dB.
    err_cutoff : float, optional
        [dB] Filtering of bad data. Must be larger than 0. The default is 10 
        dB.
    dy_cutoff0 : float, optional
        [dB] Truncation for ringdown data selection at upper end. The default 
        is 1 dB.
    dy_cutoff1 : float, optional
        [dB] Truncation for ringdown data selection at lower end. The default 
        is 5 dB.
    minslope : float, optional
        [dB/s] Minimum acceptable slope for ringdown data. The default is 0 
        dB/s.
    min_dy : float, optional
        [dB] Minimum y-length of ringdown data. The default is 5 dB.
    min_dx : float, optional
        [s] Minimum x-length of ringdown data. The default is .1 s.

    Returns
    -------
    i_selected : array
        Indices for identified ringdown.

    """

    ''' Select subset of data '''
    i_crossings = zerocrossings(y - np.max(y) + slope_scan)
    d_kernel = [1/2,0, -1/2]
    dy = np.convolve(y,d_kernel,'same')
    if len(i_crossings) == 1:
        # Use all data
        i0 = 0
        i1 = len(x)
    else:
        # Use subset. Select best qualified
        best_obj = 0
        best_bounds = []
        for i0_sel in range(-1,len(i_crossings)): #while (y[i0] - y[i0+1] > 20) or (y[i0+1] > y[i0]):
            if i0_sel == -1:
                i0 = 0
            else:
                i0 = i_crossings[i0_sel]
                
            if i0_sel == len(i_crossings)-1:
                i1 = len(x) - 1
            else:
                i1 = i_crossings[i0_sel+1]
            
            y_sub = y[i0:i1]
            y1 = y_sub.min()
            y2 = y_sub.max()   
            slope_counter = np.mean(dy[i0:i1] < 0)
            obj = (y2-y1)*slope_counter#/err
            if obj > best_obj:
                best_obj = obj
                best_bounds = [i0,i1]
                
         
        if len(best_bounds):
            i0,i1 = best_bounds
            
        i0 -= edge_inclusion
        if i0 < 0:
            i0 = 0
        i1 += edge_inclusion
        if i1 > len(x):
            i1 = len(x)
    
    x_sub = x[i0:i1]
    y_sub = y[i0:i1]
    
    ''' Loop over number of segments and choose an apropriate fit '''
    SSR = []
    pwlf_models = []
    best_results = 0
    for i_loop,n_segments in enumerate(range(1,n_segments_max+1)):
        #print("Fitting for {:g} segments.".format(n_segments))
        # initialize piecewise linear fit with your x and y data
        my_pwlf = pwlf.PiecewiseLinFit(x_sub, y_sub)
        pwlf_models.append(my_pwlf)
        
        # fit the data for four line segments
        # res = my_pwlf.fitfast(8,pop=3)
        res = my_pwlf.fit(n_segments)
        
        # predict for the determined points
        y_hat = my_pwlf.predict(x_sub)
        
        SSR.append(np.sum((y_hat - y_sub)**2))
        
        
        # Determine if done
        best_results = i_loop
        if i_loop > 0:
            if SSR[-1]/SSR[-2] > convergence_tresh:
                best_results = i_loop - 1
                break
        # if i_loop > 2:
        #     if SSR[-2]/SSR[-1] < (SSR[-3]/SSR[-2])/1.5:
        #         break
        
    my_pwlf = pwlf_models[best_results]
    
    ''' Select data points '''
    slopes = my_pwlf.calc_slopes()
    breaks = my_pwlf.fit_breaks
    
    # Select segment based on length and slope
    i_sel = -1
    last_obj = np.inf
    for i in range(len(slopes)):
        slope = slopes[i]
        if slope > -minslope:
            continue
        x_seg_0i = breaks[i]
        x_seg_0f = breaks[i+1]
        if (x_seg_0f - x_seg_0i) < min_dx:
            continue
        
        i_seg_0i = int(zerocrossings(x_sub-x_seg_0i)) + 1
        i_seg_0f = int(zerocrossings(x_sub-x_seg_0f))
        
        dy = y_sub[i_seg_0f] - y_sub[i_seg_0i]
        if abs(dy) < min_dy:
            continue
        # print('dy',dy,'i',i)
        
        x_hat = x_sub[i_seg_0i:i_seg_0f]
        y_hat = my_pwlf.predict(x_hat)
        e_hat = y_hat - y_sub[i_seg_0i:i_seg_0f]
        MSE = np.sum(e_hat**2)/len(e_hat)
        
        obj = MSE#abs(slope)#/t_segment
        
        if obj < last_obj:
            # print('dy',dy,'i',i)
            last_obj = obj
            i_sel = i            
    
    x_seg_0i = breaks[i_sel]
    x_seg_0f = breaks[i_sel+1]
    i_seg_0i = int(zerocrossings(x_sub-x_seg_0i)) + 1
    i_seg_0f = int(zerocrossings(x_sub-x_seg_0f))
    
    # Compare selected points to fit and remove bad data
    x_hat = x_sub[i_seg_0i:i_seg_0f]
    y_hat = my_pwlf.predict(x_hat)
    e_hat = y_hat - y_sub[i_seg_0i:i_seg_0f]
    
    i_selected_0 = i_seg_0i + np.where(np.abs(e_hat) < err_cutoff)[0]
    
    
    # Cutoff ends to remove possible bad data
    n_scan = len(i_selected_0)
        
    temp = zerocrossings(y_sub[i_selected_0[0]:i_selected_0[0]+n_scan] - y_sub[i_selected_0[0]] + dy_cutoff0)
    if len(temp):
        i_seg0_cutoff = i_selected_0[0] + temp[-1] + 1
    else:
        i_seg0_cutoff = i_selected_0[0]
        
    temp = zerocrossings(y_sub[i_selected_0[-1]-n_scan:i_selected_0[-1]] - y_sub[i_selected_0[-1]] - dy_cutoff1)
    if len(temp):
        i_seg1_cutoff = (i_selected_0[-1]-n_scan) + temp[0]
    else:
        i_seg1_cutoff = i_selected_0[-1]-n_scan
    
    i_selected = i0 + np.array(range(i_seg0_cutoff,i_seg1_cutoff+1))
    
    return i_selected