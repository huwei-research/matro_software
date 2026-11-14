"""Generated from PDFO 2.2.0 maintained NEWUOA; see LICENSE and provenance.json.
Do not edit: run generate.py to reproduce this file.
"""

from .runtime import FArray, _div, _idiv, _sqrt, _atan, _sin, _cos, _min, _max, _huge

def _newuoa(_ctx, n, npt, x, rhobeg, rhoend, iprint, maxfun, w, f, info, ftarget):
    ibmat = 0
    id = 0
    ifv = 0
    igq = 0
    ihq = 0
    ipq = 0
    ivl = 0
    iw = 0
    ixb = 0
    ixn = 0
    ixo = 0
    ixp = 0
    izmat = 0
    min = 0
    ndim = 0
    np = 0
    nptm = 0
    print = 0.0
    _pc = 0
    while True:
        if _pc < 5:
            if _pc < 3:
                # newuoa: basic block 0
                np = int(n + 1)
                nptm = int(npt - np)
                if not (npt < n + 2 or npt > _idiv((n + 2) * np, 2)):
                    _pc = 8
                    continue
                _pc = 3
                continue
            else:
                if _pc < 4:
                    # newuoa: basic block 3
                    if not (iprint > 0):
                        _pc = 5
                        continue
                    _pc = 4
                    continue
                else:
                    # newuoa: basic block 4
                    pass
                    _pc = 5
                    continue
        else:
            if _pc < 8:
                # newuoa: basic block 5
                pass
                info = int(5)
                _pc = 24
                continue
            else:
                if _pc < 24:
                    # newuoa: basic block 8
                    ndim = int(npt + n)
                    ixb = int(1)
                    ixo = int(ixb + n)
                    ixn = int(ixo + n)
                    ixp = int(ixn + n)
                    ifv = int(ixp + n * npt)
                    igq = int(ifv + npt)
                    ihq = int(igq + n)
                    ipq = int(ihq + _idiv(n * np, 2))
                    ibmat = int(ipq + npt)
                    izmat = int(ibmat + ndim * n)
                    id = int(izmat + npt * nptm)
                    ivl = int(id + n)
                    iw = int(ivl + ndim)
                    rhoend = float(_min(rhobeg, rhoend))
                    n, npt, rhobeg, rhoend, iprint, maxfun, ndim, f, info, ftarget = _newuob(_ctx, n, npt, x, rhobeg, rhoend, iprint, maxfun, w.tail(ixb), w.tail(ixo), w.tail(ixn), w.tail(ixp), w.tail(ifv), w.tail(igq), w.tail(ihq), w.tail(ipq), w.tail(ibmat), w.tail(izmat), ndim, w.tail(id), w.tail(ivl), w.tail(iw), f, info, ftarget)
                    _pc = 24
                    continue
                else:
                    # newuoa: basic block 24
                    return n, npt, rhobeg, rhoend, iprint, maxfun, f, info, ftarget

def _newuob(_ctx, n, npt, x, rhobeg, rhoend, iprint, maxfun, xbase, xopt, xnew, xpt, fval, gq, hq, pq, bmat, zmat, ndim, d, vlag, w, f, info, ftarget):
    almost_infinity = 0.0
    alpha = 0.0
    beta = 0.0
    bsum = 0.0
    calfun = 0.0
    crvmin = 0.0
    dabs = 0.0
    delta = 0.0
    detrat = 0.0
    diff = 0.0
    diffa = 0.0
    diffb = 0.0
    diffc = 0.0
    distsq = 0.0
    dmax1 = 0.0
    dmin1 = 0.0
    dnorm = 0.0
    dsq = 0.0
    dsqrt = 0.0
    dstep = 0.0
    dx = 0.0
    fbeg = 0.0
    fopt = 0.0
    fsave = 0.0
    gisq = 0.0
    gqsq = 0.0
    half = 0.0
    hdiag = 0.0
    huge = 0.0
    i = 0
    idz = 0
    ih = 0
    ip = 0
    ipt = 0
    itemp = 0
    itest = 0
    j = 0
    jp = 0
    jpt = 0
    k = 0
    knew = 0
    kopt = 0
    ksave = 0
    ktemp = 0
    max0 = 0
    nf = 0
    nfm = 0
    nfmm = 0
    nfsav = 0
    nftest = 0
    nh = 0
    np = 0
    nptm = 0
    one = 0.0
    print = 0.0
    ratio = 0.0
    recip = 0.0
    reciq = 0.0
    rho = 0.0
    rhosq = 0.0
    sum = 0.0
    suma = 0.0
    sumb = 0.0
    sumz = 0.0
    temp = 0.0
    tempq = 0.0
    tenth = 0.0
    vquad = 0.0
    xipt = 0.0
    xjpt = 0.0
    xoptsq = 0.0
    zero = 0.0
    xpt = xpt.with_leading(npt)
    bmat = bmat.with_leading(ndim)
    zmat = zmat.with_leading(npt)
    _pc = 0
    while True:
        if _pc < 352:
            if _pc < 184:
                if _pc < 94:
                    if _pc < 51:
                        if _pc < 26:
                            if _pc < 17:
                                if _pc < 11:
                                    if _pc < 10:
                                        # newuob: basic block 0
                                        half = float(0.5)
                                        one = float(1.0)
                                        tenth = float(0.1)
                                        zero = float(0.0)
                                        np = int(n + 1)
                                        nh = int(_idiv(n * np, 2))
                                        nptm = int(npt - np)
                                        nftest = int(max(maxfun, 1))
                                        almost_infinity = float(_div(_huge(0.0), 2.0))
                                        j = int(1); _end9 = int(n); _step9 = int(1)
                                        _pc = 10
                                        continue
                                    else:
                                        # newuob: basic block 10
                                        if (j > _end9 if _step9 > 0 else j < _end9):
                                            _pc = 24
                                            continue
                                        _pc = 11
                                        continue
                                else:
                                    if _pc < 13:
                                        # newuob: basic block 11
                                        xbase[j] = x[j]
                                        k = int(1); _end12 = int(npt); _step12 = int(1)
                                        _pc = 13
                                        continue
                                    else:
                                        if _pc < 14:
                                            # newuob: basic block 13
                                            if (k > _end12 if _step12 > 0 else k < _end12):
                                                _pc = 17
                                                continue
                                            _pc = 14
                                            continue
                                        else:
                                            # newuob: basic block 14
                                            xpt[k, j] = zero
                                            k += _step12
                                            _pc = 13
                                            continue
                            else:
                                if _pc < 22:
                                    if _pc < 18:
                                        # newuob: basic block 17
                                        i = int(1); _end17 = int(ndim); _step17 = int(1)
                                        _pc = 18
                                        continue
                                    else:
                                        if _pc < 19:
                                            # newuob: basic block 18
                                            if (i > _end17 if _step17 > 0 else i < _end17):
                                                _pc = 22
                                                continue
                                            _pc = 19
                                            continue
                                        else:
                                            # newuob: basic block 19
                                            bmat[i, j] = zero
                                            i += _step17
                                            _pc = 18
                                            continue
                                else:
                                    if _pc < 24:
                                        # newuob: basic block 22
                                        j += _step9
                                        _pc = 10
                                        continue
                                    else:
                                        if _pc < 25:
                                            # newuob: basic block 24
                                            ih = int(1); _end24 = int(nh); _step24 = int(1)
                                            _pc = 25
                                            continue
                                        else:
                                            # newuob: basic block 25
                                            if (ih > _end24 if _step24 > 0 else ih < _end24):
                                                _pc = 29
                                                continue
                                            _pc = 26
                                            continue
                        else:
                            if _pc < 37:
                                if _pc < 31:
                                    if _pc < 29:
                                        # newuob: basic block 26
                                        hq[ih] = zero
                                        ih += _step24
                                        _pc = 25
                                        continue
                                    else:
                                        if _pc < 30:
                                            # newuob: basic block 29
                                            k = int(1); _end29 = int(npt); _step29 = int(1)
                                            _pc = 30
                                            continue
                                        else:
                                            # newuob: basic block 30
                                            if (k > _end29 if _step29 > 0 else k < _end29):
                                                _pc = 39
                                                continue
                                            _pc = 31
                                            continue
                                else:
                                    if _pc < 33:
                                        # newuob: basic block 31
                                        pq[k] = zero
                                        j = int(1); _end32 = int(nptm); _step32 = int(1)
                                        _pc = 33
                                        continue
                                    else:
                                        if _pc < 34:
                                            # newuob: basic block 33
                                            if (j > _end32 if _step32 > 0 else j < _end32):
                                                _pc = 37
                                                continue
                                            _pc = 34
                                            continue
                                        else:
                                            # newuob: basic block 34
                                            zmat[k, j] = zero
                                            j += _step32
                                            _pc = 33
                                            continue
                            else:
                                if _pc < 47:
                                    if _pc < 39:
                                        # newuob: basic block 37
                                        k += _step29
                                        _pc = 30
                                        continue
                                    else:
                                        if _pc < 43:
                                            # newuob: basic block 39
                                            rhosq = float(rhobeg * rhobeg)
                                            recip = float(_div(one, rhosq))
                                            reciq = float(_div(_sqrt(half), rhosq))
                                            nf = int(0)
                                            _pc = 43
                                            continue
                                        else:
                                            # newuob: basic block 43
                                            nfm = int(nf)
                                            nfmm = int(nf - n)
                                            nf = int(nf + 1)
                                            if not (nfm <= 2 * n):
                                                _pc = 53
                                                continue
                                            _pc = 47
                                            continue
                                else:
                                    if _pc < 48:
                                        # newuob: basic block 47
                                        if not (nfm >= 1 and nfm <= n):
                                            _pc = 50
                                            continue
                                        _pc = 48
                                        continue
                                    else:
                                        if _pc < 50:
                                            # newuob: basic block 48
                                            xpt[nf, nfm] = rhobeg
                                            _pc = 52
                                            continue
                                        else:
                                            # newuob: basic block 50
                                            if not (nfm > n):
                                                _pc = 52
                                                continue
                                            _pc = 51
                                            continue
                    else:
                        if _pc < 70:
                            if _pc < 62:
                                if _pc < 53:
                                    if _pc < 52:
                                        # newuob: basic block 51
                                        xpt[nf, nfmm] = -rhobeg
                                        _pc = 52
                                        continue
                                    else:
                                        # newuob: basic block 52
                                        _pc = 68
                                        continue
                                else:
                                    if _pc < 57:
                                        # newuob: basic block 53
                                        itemp = int(_idiv(nfmm - 1, n))
                                        jpt = int(nfm - itemp * n - n)
                                        ipt = int(jpt + itemp)
                                        if not (ipt > n):
                                            _pc = 60
                                            continue
                                        _pc = 57
                                        continue
                                    else:
                                        if _pc < 60:
                                            # newuob: basic block 57
                                            itemp = int(jpt)
                                            jpt = int(ipt - n)
                                            ipt = int(itemp)
                                            _pc = 60
                                            continue
                                        else:
                                            # newuob: basic block 60
                                            xipt = float(rhobeg)
                                            if not (fval[ipt + np] < fval[ipt + 1]):
                                                _pc = 63
                                                continue
                                            _pc = 62
                                            continue
                            else:
                                if _pc < 66:
                                    if _pc < 63:
                                        # newuob: basic block 62
                                        xipt = float(-xipt)
                                        _pc = 63
                                        continue
                                    else:
                                        if _pc < 65:
                                            # newuob: basic block 63
                                            xjpt = float(rhobeg)
                                            if not (fval[jpt + np] < fval[jpt + 1]):
                                                _pc = 66
                                                continue
                                            _pc = 65
                                            continue
                                        else:
                                            # newuob: basic block 65
                                            xjpt = float(-xjpt)
                                            _pc = 66
                                            continue
                                else:
                                    if _pc < 68:
                                        # newuob: basic block 66
                                        xpt[nf, ipt] = xipt
                                        xpt[nf, jpt] = xjpt
                                        _pc = 68
                                        continue
                                    else:
                                        if _pc < 69:
                                            # newuob: basic block 68
                                            j = int(1); _end68 = int(n); _step68 = int(1)
                                            _pc = 69
                                            continue
                                        else:
                                            # newuob: basic block 69
                                            if (j > _end68 if _step68 > 0 else j < _end68):
                                                _pc = 73
                                                continue
                                            _pc = 70
                                            continue
                        else:
                            if _pc < 84:
                                if _pc < 76:
                                    if _pc < 73:
                                        # newuob: basic block 70
                                        x[j] = xpt[nf, j] + xbase[j]
                                        j += _step68
                                        _pc = 69
                                        continue
                                    else:
                                        if _pc < 74:
                                            # newuob: basic block 73
                                            _pc = 377
                                            continue
                                        else:
                                            # newuob: basic block 74
                                            fval[nf] = f
                                            if not (nf == 1):
                                                _pc = 85
                                                continue
                                            _pc = 76
                                            continue
                                else:
                                    if _pc < 80:
                                        # newuob: basic block 76
                                        fbeg = float(f)
                                        fopt = float(f)
                                        kopt = int(1)
                                        i = int(1); _end79 = int(n); _step79 = int(1)
                                        _pc = 80
                                        continue
                                    else:
                                        if _pc < 81:
                                            # newuob: basic block 80
                                            if (i > _end79 if _step79 > 0 else i < _end79):
                                                _pc = 84
                                                continue
                                            _pc = 81
                                            continue
                                        else:
                                            # newuob: basic block 81
                                            xopt[i] = xpt[1, i]
                                            i += _step79
                                            _pc = 80
                                            continue
                            else:
                                if _pc < 89:
                                    if _pc < 85:
                                        # newuob: basic block 84
                                        _pc = 93
                                        continue
                                    else:
                                        if _pc < 86:
                                            # newuob: basic block 85
                                            if not (f < fopt):
                                                _pc = 93
                                                continue
                                            _pc = 86
                                            continue
                                        else:
                                            # newuob: basic block 86
                                            fopt = float(f)
                                            kopt = int(nf)
                                            i = int(1); _end88 = int(n); _step88 = int(1)
                                            _pc = 89
                                            continue
                                else:
                                    if _pc < 90:
                                        # newuob: basic block 89
                                        if (i > _end88 if _step88 > 0 else i < _end88):
                                            _pc = 93
                                            continue
                                        _pc = 90
                                        continue
                                    else:
                                        if _pc < 93:
                                            # newuob: basic block 90
                                            xopt[i] = xpt[nf, i]
                                            i += _step88
                                            _pc = 89
                                            continue
                                        else:
                                            # newuob: basic block 93
                                            if not (nfm <= 2 * n):
                                                _pc = 112
                                                continue
                                            _pc = 94
                                            continue
                else:
                    if _pc < 147:
                        if _pc < 117:
                            if _pc < 102:
                                if _pc < 97:
                                    if _pc < 95:
                                        # newuob: basic block 94
                                        if not (nfm >= 1 and nfm <= n):
                                            _pc = 101
                                            continue
                                        _pc = 95
                                        continue
                                    else:
                                        # newuob: basic block 95
                                        gq[nfm] = _div(f - fbeg, rhobeg)
                                        if not (npt < nf + n):
                                            _pc = 100
                                            continue
                                        _pc = 97
                                        continue
                                else:
                                    if _pc < 100:
                                        # newuob: basic block 97
                                        bmat[1, nfm] = _div(-one, rhobeg)
                                        bmat[nf, nfm] = _div(one, rhobeg)
                                        bmat[npt + nfm, nfm] = -half * rhosq
                                        _pc = 100
                                        continue
                                    else:
                                        if _pc < 101:
                                            # newuob: basic block 100
                                            _pc = 111
                                            continue
                                        else:
                                            # newuob: basic block 101
                                            if not (nfm > n):
                                                _pc = 111
                                                continue
                                            _pc = 102
                                            continue
                            else:
                                if _pc < 114:
                                    if _pc < 111:
                                        # newuob: basic block 102
                                        bmat[nf - n, nfmm] = _div(half, rhobeg)
                                        bmat[nf, nfmm] = _div(-half, rhobeg)
                                        zmat[1, nfmm] = -reciq - reciq
                                        zmat[nf - n, nfmm] = reciq
                                        zmat[nf, nfmm] = reciq
                                        ih = int(_idiv(nfmm * (nfmm + 1), 2))
                                        temp = float(_div(fbeg - f, rhobeg))
                                        hq[ih] = _div(gq[nfmm] - temp, rhobeg)
                                        gq[nfmm] = half * (gq[nfmm] + temp)
                                        _pc = 111
                                        continue
                                    else:
                                        if _pc < 112:
                                            # newuob: basic block 111
                                            _pc = 122
                                            continue
                                        else:
                                            # newuob: basic block 112
                                            ih = int(_idiv(ipt * (ipt - 1), 2) + jpt)
                                            if not (xipt < zero):
                                                _pc = 115
                                                continue
                                            _pc = 114
                                            continue
                                else:
                                    if _pc < 115:
                                        # newuob: basic block 114
                                        ipt = int(ipt + n)
                                        _pc = 115
                                        continue
                                    else:
                                        if _pc < 116:
                                            # newuob: basic block 115
                                            if not (xjpt < zero):
                                                _pc = 117
                                                continue
                                            _pc = 116
                                            continue
                                        else:
                                            # newuob: basic block 116
                                            jpt = int(jpt + n)
                                            _pc = 117
                                            continue
                        else:
                            if _pc < 137:
                                if _pc < 124:
                                    if _pc < 122:
                                        # newuob: basic block 117
                                        zmat[1, nfmm] = recip
                                        zmat[nf, nfmm] = recip
                                        zmat[ipt + 1, nfmm] = -recip
                                        zmat[jpt + 1, nfmm] = -recip
                                        hq[ih] = _div(fbeg - fval[ipt + 1] - fval[jpt + 1] + f, xipt * xjpt)
                                        _pc = 122
                                        continue
                                    else:
                                        if _pc < 123:
                                            # newuob: basic block 122
                                            if not (nf < npt):
                                                _pc = 124
                                                continue
                                            _pc = 123
                                            continue
                                        else:
                                            # newuob: basic block 123
                                            _pc = 43
                                            continue
                                else:
                                    if _pc < 132:
                                        # newuob: basic block 124
                                        rho = float(rhobeg)
                                        delta = float(rho)
                                        idz = int(1)
                                        diffa = float(zero)
                                        diffb = float(zero)
                                        itest = int(0)
                                        xoptsq = float(zero)
                                        i = int(1); _end131 = int(n); _step131 = int(1)
                                        _pc = 132
                                        continue
                                    else:
                                        if _pc < 133:
                                            # newuob: basic block 132
                                            if (i > _end131 if _step131 > 0 else i < _end131):
                                                _pc = 137
                                                continue
                                            _pc = 133
                                            continue
                                        else:
                                            # newuob: basic block 133
                                            xopt[i] = xpt[kopt, i]
                                            xoptsq = float(xoptsq + xopt[i] * xopt[i])
                                            i += _step131
                                            _pc = 132
                                            continue
                            else:
                                if _pc < 142:
                                    if _pc < 138:
                                        # newuob: basic block 137
                                        nfsav = int(nf)
                                        _pc = 138
                                        continue
                                    else:
                                        if _pc < 141:
                                            # newuob: basic block 138
                                            knew = int(0)
                                            idz, delta, rho, xoptsq, diffa, diffb, diffc, itest = _ctx.observe(locals())
                                            i = int(1); _end140 = int(n); _step140 = int(1)
                                            _pc = 141
                                            continue
                                        else:
                                            # newuob: basic block 141
                                            if (i > _end140 if _step140 > 0 else i < _end140):
                                                _pc = 147
                                                continue
                                            _pc = 142
                                            continue
                                else:
                                    if _pc < 143:
                                        # newuob: basic block 142
                                        if not (gq[i] != gq[i]):
                                            _pc = 145
                                            continue
                                        _pc = 143
                                        continue
                                    else:
                                        if _pc < 145:
                                            # newuob: basic block 143
                                            info = int(-3)
                                            _pc = 656
                                            continue
                                        else:
                                            # newuob: basic block 145
                                            i += _step140
                                            _pc = 141
                                            continue
                    else:
                        if _pc < 164:
                            if _pc < 154:
                                if _pc < 149:
                                    if _pc < 148:
                                        # newuob: basic block 147
                                        i = int(1); _end147 = int(nh); _step147 = int(1)
                                        _pc = 148
                                        continue
                                    else:
                                        # newuob: basic block 148
                                        if (i > _end147 if _step147 > 0 else i < _end147):
                                            _pc = 154
                                            continue
                                        _pc = 149
                                        continue
                                else:
                                    if _pc < 150:
                                        # newuob: basic block 149
                                        if not (hq[i] != hq[i]):
                                            _pc = 152
                                            continue
                                        _pc = 150
                                        continue
                                    else:
                                        if _pc < 152:
                                            # newuob: basic block 150
                                            info = int(-3)
                                            _pc = 656
                                            continue
                                        else:
                                            # newuob: basic block 152
                                            i += _step147
                                            _pc = 148
                                            continue
                            else:
                                if _pc < 157:
                                    if _pc < 155:
                                        # newuob: basic block 154
                                        i = int(1); _end154 = int(npt); _step154 = int(1)
                                        _pc = 155
                                        continue
                                    else:
                                        if _pc < 156:
                                            # newuob: basic block 155
                                            if (i > _end154 if _step154 > 0 else i < _end154):
                                                _pc = 161
                                                continue
                                            _pc = 156
                                            continue
                                        else:
                                            # newuob: basic block 156
                                            if not (pq[i] != pq[i]):
                                                _pc = 159
                                                continue
                                            _pc = 157
                                            continue
                                else:
                                    if _pc < 159:
                                        # newuob: basic block 157
                                        info = int(-3)
                                        _pc = 656
                                        continue
                                    else:
                                        if _pc < 161:
                                            # newuob: basic block 159
                                            i += _step154
                                            _pc = 155
                                            continue
                                        else:
                                            # newuob: basic block 161
                                            n, npt, delta, crvmin = _trsapp(_ctx, n, npt, xopt, xpt, gq, hq, pq, delta, d, w, w.tail(np), w.tail(np + n), w.tail(np + 2 * n), crvmin)
                                            dsq = float(zero)
                                            i = int(1); _end163 = int(n); _step163 = int(1)
                                            _pc = 164
                                            continue
                        else:
                            if _pc < 176:
                                if _pc < 170:
                                    if _pc < 165:
                                        # newuob: basic block 164
                                        if (i > _end163 if _step163 > 0 else i < _end163):
                                            _pc = 168
                                            continue
                                        _pc = 165
                                        continue
                                    else:
                                        if _pc < 168:
                                            # newuob: basic block 165
                                            dsq = float(dsq + d[i] * d[i])
                                            i += _step163
                                            _pc = 164
                                            continue
                                        else:
                                            # newuob: basic block 168
                                            dnorm = float(_min(delta, _sqrt(dsq)))
                                            if not (dnorm < half * rho):
                                                _pc = 181
                                                continue
                                            _pc = 170
                                            continue
                                else:
                                    if _pc < 174:
                                        # newuob: basic block 170
                                        knew = int(-1)
                                        delta = float(tenth * delta)
                                        ratio = float(-1.0)
                                        if not (delta <= 1.5 * rho):
                                            _pc = 175
                                            continue
                                        _pc = 174
                                        continue
                                    else:
                                        if _pc < 175:
                                            # newuob: basic block 174
                                            delta = float(rho)
                                            _pc = 175
                                            continue
                                        else:
                                            # newuob: basic block 175
                                            if not (nf <= nfsav + 2):
                                                _pc = 177
                                                continue
                                            _pc = 176
                                            continue
                            else:
                                if _pc < 180:
                                    if _pc < 177:
                                        # newuob: basic block 176
                                        _pc = 610
                                        continue
                                    else:
                                        if _pc < 179:
                                            # newuob: basic block 177
                                            temp = float(0.125 * crvmin * rho * rho)
                                            if not (temp <= _max(diffa, diffb, diffc)):
                                                _pc = 180
                                                continue
                                            _pc = 179
                                            continue
                                        else:
                                            # newuob: basic block 179
                                            _pc = 610
                                            continue
                                else:
                                    if _pc < 181:
                                        # newuob: basic block 180
                                        _pc = 632
                                        continue
                                    else:
                                        if _pc < 182:
                                            # newuob: basic block 181
                                            if not (dsq <= 0.001 * xoptsq):
                                                _pc = 281
                                                continue
                                            _pc = 182
                                            continue
                                        else:
                                            # newuob: basic block 182
                                            tempq = float(0.25 * xoptsq)
                                            k = int(1); _end183 = int(npt); _step183 = int(1)
                                            _pc = 184
                                            continue
            else:
                if _pc < 272:
                    if _pc < 230:
                        if _pc < 210:
                            if _pc < 195:
                                if _pc < 187:
                                    if _pc < 185:
                                        # newuob: basic block 184
                                        if (k > _end183 if _step183 > 0 else k < _end183):
                                            _pc = 210
                                            continue
                                        _pc = 185
                                        continue
                                    else:
                                        # newuob: basic block 185
                                        sum = float(zero)
                                        i = int(1); _end186 = int(n); _step186 = int(1)
                                        _pc = 187
                                        continue
                                else:
                                    if _pc < 188:
                                        # newuob: basic block 187
                                        if (i > _end186 if _step186 > 0 else i < _end186):
                                            _pc = 191
                                            continue
                                        _pc = 188
                                        continue
                                    else:
                                        if _pc < 191:
                                            # newuob: basic block 188
                                            sum = float(sum + xpt[k, i] * xopt[i])
                                            i += _step186
                                            _pc = 187
                                            continue
                                        else:
                                            # newuob: basic block 191
                                            temp = float(pq[k] * sum)
                                            sum = float(sum - half * xoptsq)
                                            w[npt + k] = sum
                                            i = int(1); _end194 = int(n); _step194 = int(1)
                                            _pc = 195
                                            continue
                            else:
                                if _pc < 203:
                                    if _pc < 196:
                                        # newuob: basic block 195
                                        if (i > _end194 if _step194 > 0 else i < _end194):
                                            _pc = 208
                                            continue
                                        _pc = 196
                                        continue
                                    else:
                                        if _pc < 202:
                                            # newuob: basic block 196
                                            gq[i] = gq[i] + temp * xpt[k, i]
                                            xpt[k, i] = xpt[k, i] - half * xopt[i]
                                            vlag[i] = bmat[k, i]
                                            w[i] = sum * xpt[k, i] + tempq * xopt[i]
                                            ip = int(npt + i)
                                            j = int(1); _end201 = int(i); _step201 = int(1)
                                            _pc = 202
                                            continue
                                        else:
                                            # newuob: basic block 202
                                            if (j > _end201 if _step201 > 0 else j < _end201):
                                                _pc = 206
                                                continue
                                            _pc = 203
                                            continue
                                else:
                                    if _pc < 206:
                                        # newuob: basic block 203
                                        bmat[ip, j] = bmat[ip, j] + vlag[i] * w[j] + w[i] * vlag[j]
                                        j += _step201
                                        _pc = 202
                                        continue
                                    else:
                                        if _pc < 208:
                                            # newuob: basic block 206
                                            i += _step194
                                            _pc = 195
                                            continue
                                        else:
                                            # newuob: basic block 208
                                            k += _step183
                                            _pc = 184
                                            continue
                        else:
                            if _pc < 220:
                                if _pc < 214:
                                    if _pc < 211:
                                        # newuob: basic block 210
                                        k = int(1); _end210 = int(nptm); _step210 = int(1)
                                        _pc = 211
                                        continue
                                    else:
                                        if _pc < 212:
                                            # newuob: basic block 211
                                            if (k > _end210 if _step210 > 0 else k < _end210):
                                                _pc = 252
                                                continue
                                            _pc = 212
                                            continue
                                        else:
                                            # newuob: basic block 212
                                            sumz = float(zero)
                                            i = int(1); _end213 = int(npt); _step213 = int(1)
                                            _pc = 214
                                            continue
                                else:
                                    if _pc < 215:
                                        # newuob: basic block 214
                                        if (i > _end213 if _step213 > 0 else i < _end213):
                                            _pc = 219
                                            continue
                                        _pc = 215
                                        continue
                                    else:
                                        if _pc < 219:
                                            # newuob: basic block 215
                                            sumz = float(sumz + zmat[i, k])
                                            w[i] = w[npt + i] * zmat[i, k]
                                            i += _step213
                                            _pc = 214
                                            continue
                                        else:
                                            # newuob: basic block 219
                                            j = int(1); _end219 = int(n); _step219 = int(1)
                                            _pc = 220
                                            continue
                            else:
                                if _pc < 224:
                                    if _pc < 221:
                                        # newuob: basic block 220
                                        if (j > _end219 if _step219 > 0 else j < _end219):
                                            _pc = 237
                                            continue
                                        _pc = 221
                                        continue
                                    else:
                                        if _pc < 223:
                                            # newuob: basic block 221
                                            sum = float(tempq * sumz * xopt[j])
                                            i = int(1); _end222 = int(npt); _step222 = int(1)
                                            _pc = 223
                                            continue
                                        else:
                                            # newuob: basic block 223
                                            if (i > _end222 if _step222 > 0 else i < _end222):
                                                _pc = 227
                                                continue
                                            _pc = 224
                                            continue
                                else:
                                    if _pc < 227:
                                        # newuob: basic block 224
                                        sum = float(sum + w[i] * xpt[i, j])
                                        i += _step222
                                        _pc = 223
                                        continue
                                    else:
                                        if _pc < 229:
                                            # newuob: basic block 227
                                            vlag[j] = sum
                                            if not (k < idz):
                                                _pc = 230
                                                continue
                                            _pc = 229
                                            continue
                                        else:
                                            # newuob: basic block 229
                                            sum = float(-sum)
                                            _pc = 230
                                            continue
                    else:
                        if _pc < 248:
                            if _pc < 238:
                                if _pc < 232:
                                    if _pc < 231:
                                        # newuob: basic block 230
                                        i = int(1); _end230 = int(npt); _step230 = int(1)
                                        _pc = 231
                                        continue
                                    else:
                                        # newuob: basic block 231
                                        if (i > _end230 if _step230 > 0 else i < _end230):
                                            _pc = 235
                                            continue
                                        _pc = 232
                                        continue
                                else:
                                    if _pc < 235:
                                        # newuob: basic block 232
                                        bmat[i, j] = bmat[i, j] + sum * zmat[i, k]
                                        i += _step230
                                        _pc = 231
                                        continue
                                    else:
                                        if _pc < 237:
                                            # newuob: basic block 235
                                            j += _step219
                                            _pc = 220
                                            continue
                                        else:
                                            # newuob: basic block 237
                                            i = int(1); _end237 = int(n); _step237 = int(1)
                                            _pc = 238
                                            continue
                            else:
                                if _pc < 243:
                                    if _pc < 239:
                                        # newuob: basic block 238
                                        if (i > _end237 if _step237 > 0 else i < _end237):
                                            _pc = 250
                                            continue
                                        _pc = 239
                                        continue
                                    else:
                                        if _pc < 242:
                                            # newuob: basic block 239
                                            ip = int(i + npt)
                                            temp = float(vlag[i])
                                            if not (k < idz):
                                                _pc = 243
                                                continue
                                            _pc = 242
                                            continue
                                        else:
                                            # newuob: basic block 242
                                            temp = float(-temp)
                                            _pc = 243
                                            continue
                                else:
                                    if _pc < 244:
                                        # newuob: basic block 243
                                        j = int(1); _end243 = int(i); _step243 = int(1)
                                        _pc = 244
                                        continue
                                    else:
                                        if _pc < 245:
                                            # newuob: basic block 244
                                            if (j > _end243 if _step243 > 0 else j < _end243):
                                                _pc = 248
                                                continue
                                            _pc = 245
                                            continue
                                        else:
                                            # newuob: basic block 245
                                            bmat[ip, j] = bmat[ip, j] + temp * vlag[j]
                                            j += _step243
                                            _pc = 244
                                            continue
                        else:
                            if _pc < 258:
                                if _pc < 254:
                                    if _pc < 250:
                                        # newuob: basic block 248
                                        i += _step237
                                        _pc = 238
                                        continue
                                    else:
                                        if _pc < 252:
                                            # newuob: basic block 250
                                            k += _step210
                                            _pc = 211
                                            continue
                                        else:
                                            # newuob: basic block 252
                                            ih = int(0)
                                            j = int(1); _end253 = int(n); _step253 = int(1)
                                            _pc = 254
                                            continue
                                else:
                                    if _pc < 255:
                                        # newuob: basic block 254
                                        if (j > _end253 if _step253 > 0 else j < _end253):
                                            _pc = 274
                                            continue
                                        _pc = 255
                                        continue
                                    else:
                                        if _pc < 257:
                                            # newuob: basic block 255
                                            w[j] = zero
                                            k = int(1); _end256 = int(npt); _step256 = int(1)
                                            _pc = 257
                                            continue
                                        else:
                                            # newuob: basic block 257
                                            if (k > _end256 if _step256 > 0 else k < _end256):
                                                _pc = 262
                                                continue
                                            _pc = 258
                                            continue
                            else:
                                if _pc < 264:
                                    if _pc < 262:
                                        # newuob: basic block 258
                                        w[j] = w[j] + pq[k] * xpt[k, j]
                                        xpt[k, j] = xpt[k, j] - half * xopt[j]
                                        k += _step256
                                        _pc = 257
                                        continue
                                    else:
                                        if _pc < 263:
                                            # newuob: basic block 262
                                            i = int(1); _end262 = int(j); _step262 = int(1)
                                            _pc = 263
                                            continue
                                        else:
                                            # newuob: basic block 263
                                            if (i > _end262 if _step262 > 0 else i < _end262):
                                                _pc = 272
                                                continue
                                            _pc = 264
                                            continue
                                else:
                                    if _pc < 266:
                                        # newuob: basic block 264
                                        ih = int(ih + 1)
                                        if not (i < j):
                                            _pc = 267
                                            continue
                                        _pc = 266
                                        continue
                                    else:
                                        if _pc < 267:
                                            # newuob: basic block 266
                                            gq[j] = gq[j] + hq[ih] * xopt[i]
                                            _pc = 267
                                            continue
                                        else:
                                            # newuob: basic block 267
                                            gq[i] = gq[i] + hq[ih] * xopt[j]
                                            hq[ih] = hq[ih] + w[i] * xopt[j] + xopt[i] * w[j]
                                            bmat[npt + i, j] = bmat[npt + j, i]
                                            i += _step262
                                            _pc = 263
                                            continue
                else:
                    if _pc < 305:
                        if _pc < 288:
                            if _pc < 281:
                                if _pc < 275:
                                    if _pc < 274:
                                        # newuob: basic block 272
                                        j += _step253
                                        _pc = 254
                                        continue
                                    else:
                                        # newuob: basic block 274
                                        j = int(1); _end274 = int(n); _step274 = int(1)
                                        _pc = 275
                                        continue
                                else:
                                    if _pc < 276:
                                        # newuob: basic block 275
                                        if (j > _end274 if _step274 > 0 else j < _end274):
                                            _pc = 280
                                            continue
                                        _pc = 276
                                        continue
                                    else:
                                        if _pc < 280:
                                            # newuob: basic block 276
                                            xbase[j] = xbase[j] + xopt[j]
                                            xopt[j] = zero
                                            j += _step274
                                            _pc = 275
                                            continue
                                        else:
                                            # newuob: basic block 280
                                            xoptsq = float(zero)
                                            _pc = 281
                                            continue
                            else:
                                if _pc < 284:
                                    if _pc < 282:
                                        # newuob: basic block 281
                                        j = int(1); _end281 = int(n); _step281 = int(1)
                                        _pc = 282
                                        continue
                                    else:
                                        if _pc < 283:
                                            # newuob: basic block 282
                                            if (j > _end281 if _step281 > 0 else j < _end281):
                                                _pc = 292
                                                continue
                                            _pc = 283
                                            continue
                                        else:
                                            # newuob: basic block 283
                                            i = int(1); _end283 = int(ndim); _step283 = int(1)
                                            _pc = 284
                                            continue
                                else:
                                    if _pc < 285:
                                        # newuob: basic block 284
                                        if (i > _end283 if _step283 > 0 else i < _end283):
                                            _pc = 290
                                            continue
                                        _pc = 285
                                        continue
                                    else:
                                        if _pc < 286:
                                            # newuob: basic block 285
                                            if not (bmat[i, j] != bmat[i, j]):
                                                _pc = 288
                                                continue
                                            _pc = 286
                                            continue
                                        else:
                                            # newuob: basic block 286
                                            info = int(-3)
                                            _pc = 656
                                            continue
                        else:
                            if _pc < 296:
                                if _pc < 293:
                                    if _pc < 290:
                                        # newuob: basic block 288
                                        i += _step283
                                        _pc = 284
                                        continue
                                    else:
                                        if _pc < 292:
                                            # newuob: basic block 290
                                            j += _step281
                                            _pc = 282
                                            continue
                                        else:
                                            # newuob: basic block 292
                                            j = int(1); _end292 = int(nptm); _step292 = int(1)
                                            _pc = 293
                                            continue
                                else:
                                    if _pc < 294:
                                        # newuob: basic block 293
                                        if (j > _end292 if _step292 > 0 else j < _end292):
                                            _pc = 303
                                            continue
                                        _pc = 294
                                        continue
                                    else:
                                        if _pc < 295:
                                            # newuob: basic block 294
                                            i = int(1); _end294 = int(npt); _step294 = int(1)
                                            _pc = 295
                                            continue
                                        else:
                                            # newuob: basic block 295
                                            if (i > _end294 if _step294 > 0 else i < _end294):
                                                _pc = 301
                                                continue
                                            _pc = 296
                                            continue
                            else:
                                if _pc < 301:
                                    if _pc < 297:
                                        # newuob: basic block 296
                                        if not (zmat[i, j] != zmat[i, j]):
                                            _pc = 299
                                            continue
                                        _pc = 297
                                        continue
                                    else:
                                        if _pc < 299:
                                            # newuob: basic block 297
                                            info = int(-3)
                                            _pc = 656
                                            continue
                                        else:
                                            # newuob: basic block 299
                                            i += _step294
                                            _pc = 295
                                            continue
                                else:
                                    if _pc < 303:
                                        # newuob: basic block 301
                                        j += _step292
                                        _pc = 293
                                        continue
                                    else:
                                        if _pc < 304:
                                            # newuob: basic block 303
                                            if not (knew > 0):
                                                _pc = 305
                                                continue
                                            _pc = 304
                                            continue
                                        else:
                                            # newuob: basic block 304
                                            n, npt, idz, ndim, knew, dstep, alpha = _biglag(_ctx, n, npt, xopt, xpt, bmat, zmat, idz, ndim, knew, dstep, d, alpha, vlag, vlag.tail(npt + 1), w, w.tail(np), w.tail(np + n))
                                            _pc = 305
                                            continue
                    else:
                        if _pc < 330:
                            if _pc < 317:
                                if _pc < 307:
                                    if _pc < 306:
                                        # newuob: basic block 305
                                        k = int(1); _end305 = int(npt); _step305 = int(1)
                                        _pc = 306
                                        continue
                                    else:
                                        # newuob: basic block 306
                                        if (k > _end305 if _step305 > 0 else k < _end305):
                                            _pc = 321
                                            continue
                                        _pc = 307
                                        continue
                                else:
                                    if _pc < 311:
                                        # newuob: basic block 307
                                        suma = float(zero)
                                        sumb = float(zero)
                                        sum = float(zero)
                                        j = int(1); _end310 = int(n); _step310 = int(1)
                                        _pc = 311
                                        continue
                                    else:
                                        if _pc < 312:
                                            # newuob: basic block 311
                                            if (j > _end310 if _step310 > 0 else j < _end310):
                                                _pc = 317
                                                continue
                                            _pc = 312
                                            continue
                                        else:
                                            # newuob: basic block 312
                                            suma = float(suma + xpt[k, j] * d[j])
                                            sumb = float(sumb + xpt[k, j] * xopt[j])
                                            sum = float(sum + bmat[k, j] * d[j])
                                            j += _step310
                                            _pc = 311
                                            continue
                            else:
                                if _pc < 324:
                                    if _pc < 321:
                                        # newuob: basic block 317
                                        w[k] = suma * (half * suma + sumb)
                                        vlag[k] = sum
                                        k += _step305
                                        _pc = 306
                                        continue
                                    else:
                                        if _pc < 323:
                                            # newuob: basic block 321
                                            beta = float(zero)
                                            k = int(1); _end322 = int(nptm); _step322 = int(1)
                                            _pc = 323
                                            continue
                                        else:
                                            # newuob: basic block 323
                                            if (k > _end322 if _step322 > 0 else k < _end322):
                                                _pc = 342
                                                continue
                                            _pc = 324
                                            continue
                                else:
                                    if _pc < 326:
                                        # newuob: basic block 324
                                        sum = float(zero)
                                        i = int(1); _end325 = int(npt); _step325 = int(1)
                                        _pc = 326
                                        continue
                                    else:
                                        if _pc < 327:
                                            # newuob: basic block 326
                                            if (i > _end325 if _step325 > 0 else i < _end325):
                                                _pc = 330
                                                continue
                                            _pc = 327
                                            continue
                                        else:
                                            # newuob: basic block 327
                                            sum = float(sum + zmat[i, k] * w[i])
                                            i += _step325
                                            _pc = 326
                                            continue
                        else:
                            if _pc < 340:
                                if _pc < 335:
                                    if _pc < 331:
                                        # newuob: basic block 330
                                        if not (k < idz):
                                            _pc = 334
                                            continue
                                        _pc = 331
                                        continue
                                    else:
                                        if _pc < 334:
                                            # newuob: basic block 331
                                            beta = float(beta + sum * sum)
                                            sum = float(-sum)
                                            _pc = 335
                                            continue
                                        else:
                                            # newuob: basic block 334
                                            beta = float(beta - sum * sum)
                                            _pc = 335
                                            continue
                                else:
                                    if _pc < 336:
                                        # newuob: basic block 335
                                        i = int(1); _end335 = int(npt); _step335 = int(1)
                                        _pc = 336
                                        continue
                                    else:
                                        if _pc < 337:
                                            # newuob: basic block 336
                                            if (i > _end335 if _step335 > 0 else i < _end335):
                                                _pc = 340
                                                continue
                                            _pc = 337
                                            continue
                                        else:
                                            # newuob: basic block 337
                                            vlag[i] = vlag[i] + sum * zmat[i, k]
                                            i += _step335
                                            _pc = 336
                                            continue
                            else:
                                if _pc < 346:
                                    if _pc < 342:
                                        # newuob: basic block 340
                                        k += _step322
                                        _pc = 323
                                        continue
                                    else:
                                        if _pc < 345:
                                            # newuob: basic block 342
                                            bsum = float(zero)
                                            dx = float(zero)
                                            j = int(1); _end344 = int(n); _step344 = int(1)
                                            _pc = 345
                                            continue
                                        else:
                                            # newuob: basic block 345
                                            if (j > _end344 if _step344 > 0 else j < _end344):
                                                _pc = 364
                                                continue
                                            _pc = 346
                                            continue
                                else:
                                    if _pc < 348:
                                        # newuob: basic block 346
                                        sum = float(zero)
                                        i = int(1); _end347 = int(npt); _step347 = int(1)
                                        _pc = 348
                                        continue
                                    else:
                                        if _pc < 349:
                                            # newuob: basic block 348
                                            if (i > _end347 if _step347 > 0 else i < _end347):
                                                _pc = 352
                                                continue
                                            _pc = 349
                                            continue
                                        else:
                                            # newuob: basic block 349
                                            sum = float(sum + w[i] * bmat[i, j])
                                            i += _step347
                                            _pc = 348
                                            continue
        else:
            if _pc < 521:
                if _pc < 436:
                    if _pc < 397:
                        if _pc < 377:
                            if _pc < 367:
                                if _pc < 356:
                                    if _pc < 355:
                                        # newuob: basic block 352
                                        bsum = float(bsum + sum * d[j])
                                        jp = int(npt + j)
                                        k = int(1); _end354 = int(n); _step354 = int(1)
                                        _pc = 355
                                        continue
                                    else:
                                        # newuob: basic block 355
                                        if (k > _end354 if _step354 > 0 else k < _end354):
                                            _pc = 359
                                            continue
                                        _pc = 356
                                        continue
                                else:
                                    if _pc < 359:
                                        # newuob: basic block 356
                                        sum = float(sum + bmat[jp, k] * d[k])
                                        k += _step354
                                        _pc = 355
                                        continue
                                    else:
                                        if _pc < 364:
                                            # newuob: basic block 359
                                            vlag[jp] = sum
                                            bsum = float(bsum + sum * d[j])
                                            dx = float(dx + d[j] * xopt[j])
                                            j += _step344
                                            _pc = 345
                                            continue
                                        else:
                                            # newuob: basic block 364
                                            beta = float(dx * dx + dsq * (xoptsq + dx + dx + half * dsq) + beta - bsum)
                                            vlag[kopt] = vlag[kopt] + one
                                            if not (knew > 0):
                                                _pc = 370
                                                continue
                                            _pc = 367
                                            continue
                            else:
                                if _pc < 371:
                                    if _pc < 369:
                                        # newuob: basic block 367
                                        temp = float(one + _div(alpha * beta, vlag[knew] * vlag[knew]))
                                        if not (abs(temp) <= 0.8):
                                            _pc = 370
                                            continue
                                        _pc = 369
                                        continue
                                    else:
                                        if _pc < 370:
                                            # newuob: basic block 369
                                            n, npt, idz, ndim, kopt, knew, beta = _bigden(_ctx, n, npt, xopt, xpt, bmat, zmat, idz, ndim, kopt, knew, d, w, vlag, beta, xnew, w.tail(ndim + 1), w.tail(6 * ndim + 1))
                                            _pc = 370
                                            continue
                                        else:
                                            # newuob: basic block 370
                                            i = int(1); _end370 = int(n); _step370 = int(1)
                                            _pc = 371
                                            continue
                                else:
                                    if _pc < 372:
                                        # newuob: basic block 371
                                        if (i > _end370 if _step370 > 0 else i < _end370):
                                            _pc = 376
                                            continue
                                        _pc = 372
                                        continue
                                    else:
                                        if _pc < 376:
                                            # newuob: basic block 372
                                            xnew[i] = xopt[i] + d[i]
                                            x[i] = xbase[i] + xnew[i]
                                            i += _step370
                                            _pc = 371
                                            continue
                                        else:
                                            # newuob: basic block 376
                                            nf = int(nf + 1)
                                            _pc = 377
                                            continue
                        else:
                            if _pc < 386:
                                if _pc < 381:
                                    if _pc < 378:
                                        # newuob: basic block 377
                                        if not (nf > nftest):
                                            _pc = 384
                                            continue
                                        _pc = 378
                                        continue
                                    else:
                                        if _pc < 380:
                                            # newuob: basic block 378
                                            nf = int(nf - 1)
                                            if not (iprint > 0):
                                                _pc = 381
                                                continue
                                            _pc = 380
                                            continue
                                        else:
                                            # newuob: basic block 380
                                            pass
                                            _pc = 381
                                            continue
                                else:
                                    if _pc < 384:
                                        # newuob: basic block 381
                                        pass
                                        info = int(3)
                                        _pc = 656
                                        continue
                                    else:
                                        if _pc < 385:
                                            # newuob: basic block 384
                                            i = int(1); _end384 = int(n); _step384 = int(1)
                                            _pc = 385
                                            continue
                                        else:
                                            # newuob: basic block 385
                                            if (i > _end384 if _step384 > 0 else i < _end384):
                                                _pc = 399
                                                continue
                                            _pc = 386
                                            continue
                            else:
                                if _pc < 391:
                                    if _pc < 387:
                                        # newuob: basic block 386
                                        if not (x[i] != x[i]):
                                            _pc = 397
                                            continue
                                        _pc = 387
                                        continue
                                    else:
                                        if _pc < 389:
                                            # newuob: basic block 387
                                            f = float(x[i])
                                            if not (nf == 1):
                                                _pc = 395
                                                continue
                                            _pc = 389
                                            continue
                                        else:
                                            # newuob: basic block 389
                                            fopt = float(f)
                                            j = int(1); _end390 = int(n); _step390 = int(1)
                                            _pc = 391
                                            continue
                                else:
                                    if _pc < 392:
                                        # newuob: basic block 391
                                        if (j > _end390 if _step390 > 0 else j < _end390):
                                            _pc = 395
                                            continue
                                        _pc = 392
                                        continue
                                    else:
                                        if _pc < 395:
                                            # newuob: basic block 392
                                            xopt[j] = zero
                                            j += _step390
                                            _pc = 391
                                            continue
                                        else:
                                            # newuob: basic block 395
                                            info = int(-1)
                                            _pc = 656
                                            continue
                    else:
                        if _pc < 416:
                            if _pc < 405:
                                if _pc < 401:
                                    if _pc < 399:
                                        # newuob: basic block 397
                                        i += _step384
                                        _pc = 385
                                        continue
                                    else:
                                        # newuob: basic block 399
                                        f = _ctx.objective(n, x)
                                        if not (f != f or f > almost_infinity):
                                            _pc = 410
                                            continue
                                        _pc = 401
                                        continue
                                else:
                                    if _pc < 402:
                                        # newuob: basic block 401
                                        if not (nf == 1):
                                            _pc = 408
                                            continue
                                        _pc = 402
                                        continue
                                    else:
                                        if _pc < 404:
                                            # newuob: basic block 402
                                            fopt = float(f)
                                            i = int(1); _end403 = int(n); _step403 = int(1)
                                            _pc = 404
                                            continue
                                        else:
                                            # newuob: basic block 404
                                            if (i > _end403 if _step403 > 0 else i < _end403):
                                                _pc = 408
                                                continue
                                            _pc = 405
                                            continue
                            else:
                                if _pc < 411:
                                    if _pc < 408:
                                        # newuob: basic block 405
                                        xopt[i] = zero
                                        i += _step403
                                        _pc = 404
                                        continue
                                    else:
                                        if _pc < 410:
                                            # newuob: basic block 408
                                            info = int(-2)
                                            _pc = 656
                                            continue
                                        else:
                                            # newuob: basic block 410
                                            if not (f <= ftarget):
                                                _pc = 413
                                                continue
                                            _pc = 411
                                            continue
                                else:
                                    if _pc < 413:
                                        # newuob: basic block 411
                                        info = int(1)
                                        _pc = 663
                                        continue
                                    else:
                                        if _pc < 414:
                                            # newuob: basic block 413
                                            if not (iprint == 3):
                                                _pc = 416
                                                continue
                                            _pc = 414
                                            continue
                                        else:
                                            # newuob: basic block 414
                                            pass
                                            pass
                                            _pc = 416
                                            continue
                        else:
                            if _pc < 424:
                                if _pc < 419:
                                    if _pc < 417:
                                        # newuob: basic block 416
                                        if not (nf <= npt):
                                            _pc = 418
                                            continue
                                        _pc = 417
                                        continue
                                    else:
                                        if _pc < 418:
                                            # newuob: basic block 417
                                            _pc = 74
                                            continue
                                        else:
                                            # newuob: basic block 418
                                            if not (knew == -1):
                                                _pc = 420
                                                continue
                                            _pc = 419
                                            continue
                                else:
                                    if _pc < 420:
                                        # newuob: basic block 419
                                        _pc = 656
                                        continue
                                    else:
                                        if _pc < 423:
                                            # newuob: basic block 420
                                            vquad = float(zero)
                                            ih = int(0)
                                            j = int(1); _end422 = int(n); _step422 = int(1)
                                            _pc = 423
                                            continue
                                        else:
                                            # newuob: basic block 423
                                            if (j > _end422 if _step422 > 0 else j < _end422):
                                                _pc = 436
                                                continue
                                            _pc = 424
                                            continue
                            else:
                                if _pc < 430:
                                    if _pc < 426:
                                        # newuob: basic block 424
                                        vquad = float(vquad + d[j] * gq[j])
                                        i = int(1); _end425 = int(j); _step425 = int(1)
                                        _pc = 426
                                        continue
                                    else:
                                        if _pc < 427:
                                            # newuob: basic block 426
                                            if (i > _end425 if _step425 > 0 else i < _end425):
                                                _pc = 434
                                                continue
                                            _pc = 427
                                            continue
                                        else:
                                            # newuob: basic block 427
                                            ih = int(ih + 1)
                                            temp = float(d[i] * xnew[j] + d[j] * xopt[i])
                                            if not (i == j):
                                                _pc = 431
                                                continue
                                            _pc = 430
                                            continue
                                else:
                                    if _pc < 431:
                                        # newuob: basic block 430
                                        temp = float(half * temp)
                                        _pc = 431
                                        continue
                                    else:
                                        if _pc < 434:
                                            # newuob: basic block 431
                                            vquad = float(vquad + temp * hq[ih])
                                            i += _step425
                                            _pc = 426
                                            continue
                                        else:
                                            # newuob: basic block 434
                                            j += _step422
                                            _pc = 423
                                            continue
                else:
                    if _pc < 480:
                        if _pc < 460:
                            if _pc < 447:
                                if _pc < 438:
                                    if _pc < 437:
                                        # newuob: basic block 436
                                        k = int(1); _end436 = int(npt); _step436 = int(1)
                                        _pc = 437
                                        continue
                                    else:
                                        # newuob: basic block 437
                                        if (k > _end436 if _step436 > 0 else k < _end436):
                                            _pc = 441
                                            continue
                                        _pc = 438
                                        continue
                                else:
                                    if _pc < 441:
                                        # newuob: basic block 438
                                        vquad = float(vquad + pq[k] * w[k])
                                        k += _step436
                                        _pc = 437
                                        continue
                                    else:
                                        if _pc < 446:
                                            # newuob: basic block 441
                                            diff = float(f - fopt - vquad)
                                            diffc = float(diffb)
                                            diffb = float(diffa)
                                            diffa = float(abs(diff))
                                            if not (dnorm > rho):
                                                _pc = 447
                                                continue
                                            _pc = 446
                                            continue
                                        else:
                                            # newuob: basic block 446
                                            nfsav = int(nf)
                                            _pc = 447
                                            continue
                            else:
                                if _pc < 453:
                                    if _pc < 449:
                                        # newuob: basic block 447
                                        fsave = float(fopt)
                                        if not (f < fopt):
                                            _pc = 457
                                            continue
                                        _pc = 449
                                        continue
                                    else:
                                        if _pc < 452:
                                            # newuob: basic block 449
                                            fopt = float(f)
                                            xoptsq = float(zero)
                                            i = int(1); _end451 = int(n); _step451 = int(1)
                                            _pc = 452
                                            continue
                                        else:
                                            # newuob: basic block 452
                                            if (i > _end451 if _step451 > 0 else i < _end451):
                                                _pc = 457
                                                continue
                                            _pc = 453
                                            continue
                                else:
                                    if _pc < 457:
                                        # newuob: basic block 453
                                        xopt[i] = xnew[i]
                                        xoptsq = float(xoptsq + xopt[i] * xopt[i])
                                        i += _step451
                                        _pc = 452
                                        continue
                                    else:
                                        if _pc < 459:
                                            # newuob: basic block 457
                                            ksave = int(knew)
                                            if not (knew > 0):
                                                _pc = 460
                                                continue
                                            _pc = 459
                                            continue
                                        else:
                                            # newuob: basic block 459
                                            _pc = 509
                                            continue
                        else:
                            if _pc < 470:
                                if _pc < 463:
                                    if _pc < 461:
                                        # newuob: basic block 460
                                        if not (not vquad < zero):
                                            _pc = 466
                                            continue
                                        _pc = 461
                                        continue
                                    else:
                                        if _pc < 462:
                                            # newuob: basic block 461
                                            if not (iprint > 0):
                                                _pc = 463
                                                continue
                                            _pc = 462
                                            continue
                                        else:
                                            # newuob: basic block 462
                                            pass
                                            _pc = 463
                                            continue
                                else:
                                    if _pc < 466:
                                        # newuob: basic block 463
                                        pass
                                        info = int(2)
                                        _pc = 656
                                        continue
                                    else:
                                        if _pc < 468:
                                            # newuob: basic block 466
                                            ratio = float(_div(f - fsave, vquad))
                                            if not (ratio <= tenth):
                                                _pc = 470
                                                continue
                                            _pc = 468
                                            continue
                                        else:
                                            # newuob: basic block 468
                                            delta = float(half * dnorm)
                                            _pc = 474
                                            continue
                            else:
                                if _pc < 474:
                                    if _pc < 471:
                                        # newuob: basic block 470
                                        if not (ratio <= 0.7):
                                            _pc = 473
                                            continue
                                        _pc = 471
                                        continue
                                    else:
                                        if _pc < 473:
                                            # newuob: basic block 471
                                            delta = float(_max(half * delta, dnorm))
                                            _pc = 474
                                            continue
                                        else:
                                            # newuob: basic block 473
                                            delta = float(_max(half * delta, dnorm + dnorm))
                                            _pc = 474
                                            continue
                                else:
                                    if _pc < 475:
                                        # newuob: basic block 474
                                        if not (delta <= 1.5 * rho):
                                            _pc = 476
                                            continue
                                        _pc = 475
                                        continue
                                    else:
                                        if _pc < 476:
                                            # newuob: basic block 475
                                            delta = float(rho)
                                            _pc = 476
                                            continue
                                        else:
                                            # newuob: basic block 476
                                            rhosq = float(_max(tenth * delta, rho) * _max(tenth * delta, rho))
                                            ktemp = int(0)
                                            detrat = float(zero)
                                            if not (f >= fsave):
                                                _pc = 482
                                                continue
                                            _pc = 480
                                            continue
                    else:
                        if _pc < 500:
                            if _pc < 487:
                                if _pc < 483:
                                    if _pc < 482:
                                        # newuob: basic block 480
                                        ktemp = int(kopt)
                                        detrat = float(one)
                                        _pc = 482
                                        continue
                                    else:
                                        # newuob: basic block 482
                                        k = int(1); _end482 = int(npt); _step482 = int(1)
                                        _pc = 483
                                        continue
                                else:
                                    if _pc < 484:
                                        # newuob: basic block 483
                                        if (k > _end482 if _step482 > 0 else k < _end482):
                                            _pc = 507
                                            continue
                                        _pc = 484
                                        continue
                                    else:
                                        if _pc < 486:
                                            # newuob: basic block 484
                                            hdiag = float(zero)
                                            j = int(1); _end485 = int(nptm); _step485 = int(1)
                                            _pc = 486
                                            continue
                                        else:
                                            # newuob: basic block 486
                                            if (j > _end485 if _step485 > 0 else j < _end485):
                                                _pc = 493
                                                continue
                                            _pc = 487
                                            continue
                            else:
                                if _pc < 493:
                                    if _pc < 489:
                                        # newuob: basic block 487
                                        temp = float(one)
                                        if not (j < idz):
                                            _pc = 490
                                            continue
                                        _pc = 489
                                        continue
                                    else:
                                        if _pc < 490:
                                            # newuob: basic block 489
                                            temp = float(-one)
                                            _pc = 490
                                            continue
                                        else:
                                            # newuob: basic block 490
                                            hdiag = float(hdiag + temp * (zmat[k, j] * zmat[k, j]))
                                            j += _step485
                                            _pc = 486
                                            continue
                                else:
                                    if _pc < 496:
                                        # newuob: basic block 493
                                        temp = float(abs(beta * hdiag + vlag[k] * vlag[k]))
                                        distsq = float(zero)
                                        j = int(1); _end495 = int(n); _step495 = int(1)
                                        _pc = 496
                                        continue
                                    else:
                                        if _pc < 497:
                                            # newuob: basic block 496
                                            if (j > _end495 if _step495 > 0 else j < _end495):
                                                _pc = 500
                                                continue
                                            _pc = 497
                                            continue
                                        else:
                                            # newuob: basic block 497
                                            distsq = float(distsq + (xpt[k, j] - xopt[j]) * (xpt[k, j] - xopt[j]))
                                            j += _step495
                                            _pc = 496
                                            continue
                        else:
                            if _pc < 508:
                                if _pc < 503:
                                    if _pc < 501:
                                        # newuob: basic block 500
                                        if not (distsq > rhosq):
                                            _pc = 502
                                            continue
                                        _pc = 501
                                        continue
                                    else:
                                        if _pc < 502:
                                            # newuob: basic block 501
                                            temp = float(temp * (_div(distsq, rhosq) * _div(distsq, rhosq) * _div(distsq, rhosq)))
                                            _pc = 502
                                            continue
                                        else:
                                            # newuob: basic block 502
                                            if not (temp > detrat and k != ktemp):
                                                _pc = 505
                                                continue
                                            _pc = 503
                                            continue
                                else:
                                    if _pc < 505:
                                        # newuob: basic block 503
                                        detrat = float(temp)
                                        knew = int(k)
                                        _pc = 505
                                        continue
                                    else:
                                        if _pc < 507:
                                            # newuob: basic block 505
                                            k += _step482
                                            _pc = 483
                                            continue
                                        else:
                                            # newuob: basic block 507
                                            if not (knew == 0):
                                                _pc = 509
                                                continue
                                            _pc = 508
                                            continue
                            else:
                                if _pc < 514:
                                    if _pc < 509:
                                        # newuob: basic block 508
                                        _pc = 610
                                        continue
                                    else:
                                        if _pc < 513:
                                            # newuob: basic block 509
                                            n, npt, idz, ndim, beta, knew = _update(_ctx, n, npt, bmat, zmat, idz, ndim, vlag, beta, knew, w)
                                            fval[knew] = f
                                            ih = int(0)
                                            i = int(1); _end512 = int(n); _step512 = int(1)
                                            _pc = 513
                                            continue
                                        else:
                                            # newuob: basic block 513
                                            if (i > _end512 if _step512 > 0 else i < _end512):
                                                _pc = 523
                                                continue
                                            _pc = 514
                                            continue
                                else:
                                    if _pc < 516:
                                        # newuob: basic block 514
                                        temp = float(pq[knew] * xpt[knew, i])
                                        j = int(1); _end515 = int(i); _step515 = int(1)
                                        _pc = 516
                                        continue
                                    else:
                                        if _pc < 517:
                                            # newuob: basic block 516
                                            if (j > _end515 if _step515 > 0 else j < _end515):
                                                _pc = 521
                                                continue
                                            _pc = 517
                                            continue
                                        else:
                                            # newuob: basic block 517
                                            ih = int(ih + 1)
                                            hq[ih] = hq[ih] + temp * xpt[knew, j]
                                            j += _step515
                                            _pc = 516
                                            continue
            else:
                if _pc < 600:
                    if _pc < 562:
                        if _pc < 539:
                            if _pc < 529:
                                if _pc < 525:
                                    if _pc < 523:
                                        # newuob: basic block 521
                                        i += _step512
                                        _pc = 513
                                        continue
                                    else:
                                        # newuob: basic block 523
                                        pq[knew] = zero
                                        j = int(1); _end524 = int(nptm); _step524 = int(1)
                                        _pc = 525
                                        continue
                                else:
                                    if _pc < 526:
                                        # newuob: basic block 525
                                        if (j > _end524 if _step524 > 0 else j < _end524):
                                            _pc = 536
                                            continue
                                        _pc = 526
                                        continue
                                    else:
                                        if _pc < 528:
                                            # newuob: basic block 526
                                            temp = float(diff * zmat[knew, j])
                                            if not (j < idz):
                                                _pc = 529
                                                continue
                                            _pc = 528
                                            continue
                                        else:
                                            # newuob: basic block 528
                                            temp = float(-temp)
                                            _pc = 529
                                            continue
                            else:
                                if _pc < 534:
                                    if _pc < 530:
                                        # newuob: basic block 529
                                        k = int(1); _end529 = int(npt); _step529 = int(1)
                                        _pc = 530
                                        continue
                                    else:
                                        if _pc < 531:
                                            # newuob: basic block 530
                                            if (k > _end529 if _step529 > 0 else k < _end529):
                                                _pc = 534
                                                continue
                                            _pc = 531
                                            continue
                                        else:
                                            # newuob: basic block 531
                                            pq[k] = pq[k] + temp * zmat[k, j]
                                            k += _step529
                                            _pc = 530
                                            continue
                                else:
                                    if _pc < 536:
                                        # newuob: basic block 534
                                        j += _step524
                                        _pc = 525
                                        continue
                                    else:
                                        if _pc < 538:
                                            # newuob: basic block 536
                                            gqsq = float(zero)
                                            i = int(1); _end537 = int(n); _step537 = int(1)
                                            _pc = 538
                                            continue
                                        else:
                                            # newuob: basic block 538
                                            if (i > _end537 if _step537 > 0 else i < _end537):
                                                _pc = 544
                                                continue
                                            _pc = 539
                                            continue
                        else:
                            if _pc < 550:
                                if _pc < 546:
                                    if _pc < 544:
                                        # newuob: basic block 539
                                        gq[i] = gq[i] + diff * bmat[knew, i]
                                        gqsq = float(gqsq + gq[i] * gq[i])
                                        xpt[knew, i] = xnew[i]
                                        i += _step537
                                        _pc = 538
                                        continue
                                    else:
                                        if _pc < 545:
                                            # newuob: basic block 544
                                            if not (ksave == 0 and delta == rho):
                                                _pc = 603
                                                continue
                                            _pc = 545
                                            continue
                                        else:
                                            # newuob: basic block 545
                                            if not (ratio > 0.01):
                                                _pc = 548
                                                continue
                                            _pc = 546
                                            continue
                                else:
                                    if _pc < 548:
                                        # newuob: basic block 546
                                        itest = int(0)
                                        _pc = 603
                                        continue
                                    else:
                                        if _pc < 549:
                                            # newuob: basic block 548
                                            k = int(1); _end548 = int(npt); _step548 = int(1)
                                            _pc = 549
                                            continue
                                        else:
                                            # newuob: basic block 549
                                            if (k > _end548 if _step548 > 0 else k < _end548):
                                                _pc = 553
                                                continue
                                            _pc = 550
                                            continue
                            else:
                                if _pc < 556:
                                    if _pc < 553:
                                        # newuob: basic block 550
                                        vlag[k] = fval[k] - fval[kopt]
                                        k += _step548
                                        _pc = 549
                                        continue
                                    else:
                                        if _pc < 555:
                                            # newuob: basic block 553
                                            gisq = float(zero)
                                            i = int(1); _end554 = int(n); _step554 = int(1)
                                            _pc = 555
                                            continue
                                        else:
                                            # newuob: basic block 555
                                            if (i > _end554 if _step554 > 0 else i < _end554):
                                                _pc = 566
                                                continue
                                            _pc = 556
                                            continue
                                else:
                                    if _pc < 558:
                                        # newuob: basic block 556
                                        sum = float(zero)
                                        k = int(1); _end557 = int(npt); _step557 = int(1)
                                        _pc = 558
                                        continue
                                    else:
                                        if _pc < 559:
                                            # newuob: basic block 558
                                            if (k > _end557 if _step557 > 0 else k < _end557):
                                                _pc = 562
                                                continue
                                            _pc = 559
                                            continue
                                        else:
                                            # newuob: basic block 559
                                            sum = float(sum + bmat[k, i] * vlag[k])
                                            k += _step557
                                            _pc = 558
                                            continue
                    else:
                        if _pc < 581:
                            if _pc < 571:
                                if _pc < 568:
                                    if _pc < 566:
                                        # newuob: basic block 562
                                        gisq = float(gisq + sum * sum)
                                        w[i] = sum
                                        i += _step554
                                        _pc = 555
                                        continue
                                    else:
                                        # newuob: basic block 566
                                        itest = int(itest + 1)
                                        if not (gqsq < 100.0 * gisq):
                                            _pc = 569
                                            continue
                                        _pc = 568
                                        continue
                                else:
                                    if _pc < 569:
                                        # newuob: basic block 568
                                        itest = int(0)
                                        _pc = 569
                                        continue
                                    else:
                                        if _pc < 570:
                                            # newuob: basic block 569
                                            if not (itest >= 3):
                                                _pc = 603
                                                continue
                                            _pc = 570
                                            continue
                                        else:
                                            # newuob: basic block 570
                                            i = int(1); _end570 = int(n); _step570 = int(1)
                                            _pc = 571
                                            continue
                            else:
                                if _pc < 576:
                                    if _pc < 572:
                                        # newuob: basic block 571
                                        if (i > _end570 if _step570 > 0 else i < _end570):
                                            _pc = 575
                                            continue
                                        _pc = 572
                                        continue
                                    else:
                                        if _pc < 575:
                                            # newuob: basic block 572
                                            gq[i] = w[i]
                                            i += _step570
                                            _pc = 571
                                            continue
                                        else:
                                            # newuob: basic block 575
                                            ih = int(1); _end575 = int(nh); _step575 = int(1)
                                            _pc = 576
                                            continue
                                else:
                                    if _pc < 577:
                                        # newuob: basic block 576
                                        if (ih > _end575 if _step575 > 0 else ih < _end575):
                                            _pc = 580
                                            continue
                                        _pc = 577
                                        continue
                                    else:
                                        if _pc < 580:
                                            # newuob: basic block 577
                                            hq[ih] = zero
                                            ih += _step575
                                            _pc = 576
                                            continue
                                        else:
                                            # newuob: basic block 580
                                            j = int(1); _end580 = int(nptm); _step580 = int(1)
                                            _pc = 581
                                            continue
                        else:
                            if _pc < 590:
                                if _pc < 585:
                                    if _pc < 582:
                                        # newuob: basic block 581
                                        if (j > _end580 if _step580 > 0 else j < _end580):
                                            _pc = 592
                                            continue
                                        _pc = 582
                                        continue
                                    else:
                                        if _pc < 584:
                                            # newuob: basic block 582
                                            w[j] = zero
                                            k = int(1); _end583 = int(npt); _step583 = int(1)
                                            _pc = 584
                                            continue
                                        else:
                                            # newuob: basic block 584
                                            if (k > _end583 if _step583 > 0 else k < _end583):
                                                _pc = 588
                                                continue
                                            _pc = 585
                                            continue
                                else:
                                    if _pc < 588:
                                        # newuob: basic block 585
                                        w[j] = w[j] + vlag[k] * zmat[k, j]
                                        k += _step583
                                        _pc = 584
                                        continue
                                    else:
                                        if _pc < 589:
                                            # newuob: basic block 588
                                            if not (j < idz):
                                                _pc = 590
                                                continue
                                            _pc = 589
                                            continue
                                        else:
                                            # newuob: basic block 589
                                            w[j] = -w[j]
                                            _pc = 590
                                            continue
                            else:
                                if _pc < 594:
                                    if _pc < 592:
                                        # newuob: basic block 590
                                        j += _step580
                                        _pc = 581
                                        continue
                                    else:
                                        if _pc < 593:
                                            # newuob: basic block 592
                                            k = int(1); _end592 = int(npt); _step592 = int(1)
                                            _pc = 593
                                            continue
                                        else:
                                            # newuob: basic block 593
                                            if (k > _end592 if _step592 > 0 else k < _end592):
                                                _pc = 602
                                                continue
                                            _pc = 594
                                            continue
                                else:
                                    if _pc < 596:
                                        # newuob: basic block 594
                                        pq[k] = zero
                                        j = int(1); _end595 = int(nptm); _step595 = int(1)
                                        _pc = 596
                                        continue
                                    else:
                                        if _pc < 597:
                                            # newuob: basic block 596
                                            if (j > _end595 if _step595 > 0 else j < _end595):
                                                _pc = 600
                                                continue
                                            _pc = 597
                                            continue
                                        else:
                                            # newuob: basic block 597
                                            pq[k] = pq[k] + zmat[k, j] * w[j]
                                            j += _step595
                                            _pc = 596
                                            continue
                else:
                    if _pc < 632:
                        if _pc < 613:
                            if _pc < 606:
                                if _pc < 603:
                                    if _pc < 602:
                                        # newuob: basic block 600
                                        k += _step592
                                        _pc = 593
                                        continue
                                    else:
                                        # newuob: basic block 602
                                        itest = int(0)
                                        _pc = 603
                                        continue
                                else:
                                    if _pc < 604:
                                        # newuob: basic block 603
                                        if not (f < fsave):
                                            _pc = 605
                                            continue
                                        _pc = 604
                                        continue
                                    else:
                                        if _pc < 605:
                                            # newuob: basic block 604
                                            kopt = int(knew)
                                            _pc = 605
                                            continue
                                        else:
                                            # newuob: basic block 605
                                            if not (f <= fsave + tenth * vquad):
                                                _pc = 607
                                                continue
                                            _pc = 606
                                            continue
                            else:
                                if _pc < 609:
                                    if _pc < 607:
                                        # newuob: basic block 606
                                        _pc = 138
                                        continue
                                    else:
                                        if _pc < 608:
                                            # newuob: basic block 607
                                            if not (ksave > 0):
                                                _pc = 609
                                                continue
                                            _pc = 608
                                            continue
                                        else:
                                            # newuob: basic block 608
                                            _pc = 138
                                            continue
                                else:
                                    if _pc < 610:
                                        # newuob: basic block 609
                                        knew = int(0)
                                        _pc = 610
                                        continue
                                    else:
                                        if _pc < 612:
                                            # newuob: basic block 610
                                            distsq = float(4.0 * delta * delta)
                                            k = int(1); _end611 = int(npt); _step611 = int(1)
                                            _pc = 612
                                            continue
                                        else:
                                            # newuob: basic block 612
                                            if (k > _end611 if _step611 > 0 else k < _end611):
                                                _pc = 624
                                                continue
                                            _pc = 613
                                            continue
                        else:
                            if _pc < 624:
                                if _pc < 619:
                                    if _pc < 615:
                                        # newuob: basic block 613
                                        sum = float(zero)
                                        j = int(1); _end614 = int(n); _step614 = int(1)
                                        _pc = 615
                                        continue
                                    else:
                                        if _pc < 616:
                                            # newuob: basic block 615
                                            if (j > _end614 if _step614 > 0 else j < _end614):
                                                _pc = 619
                                                continue
                                            _pc = 616
                                            continue
                                        else:
                                            # newuob: basic block 616
                                            sum = float(sum + (xpt[k, j] - xopt[j]) * (xpt[k, j] - xopt[j]))
                                            j += _step614
                                            _pc = 615
                                            continue
                                else:
                                    if _pc < 620:
                                        # newuob: basic block 619
                                        if not (sum > distsq):
                                            _pc = 622
                                            continue
                                        _pc = 620
                                        continue
                                    else:
                                        if _pc < 622:
                                            # newuob: basic block 620
                                            knew = int(k)
                                            distsq = float(sum)
                                            _pc = 622
                                            continue
                                        else:
                                            # newuob: basic block 622
                                            k += _step611
                                            _pc = 612
                                            continue
                            else:
                                if _pc < 629:
                                    if _pc < 625:
                                        # newuob: basic block 624
                                        if not (knew > 0):
                                            _pc = 628
                                            continue
                                        _pc = 625
                                        continue
                                    else:
                                        if _pc < 628:
                                            # newuob: basic block 625
                                            dstep = float(_max(_min(tenth * _sqrt(distsq), half * delta), rho))
                                            dsq = float(dstep * dstep)
                                            _pc = 181
                                            continue
                                        else:
                                            # newuob: basic block 628
                                            if not (ratio > zero):
                                                _pc = 630
                                                continue
                                            _pc = 629
                                            continue
                                else:
                                    if _pc < 630:
                                        # newuob: basic block 629
                                        _pc = 138
                                        continue
                                    else:
                                        if _pc < 631:
                                            # newuob: basic block 630
                                            if not (_max(delta, dnorm) > rho):
                                                _pc = 632
                                                continue
                                            _pc = 631
                                            continue
                                        else:
                                            # newuob: basic block 631
                                            _pc = 138
                                            continue
                    else:
                        if _pc < 652:
                            if _pc < 641:
                                if _pc < 636:
                                    if _pc < 633:
                                        # newuob: basic block 632
                                        if not (rho > rhoend):
                                            _pc = 653
                                            continue
                                        _pc = 633
                                        continue
                                    else:
                                        # newuob: basic block 633
                                        delta = float(half * rho)
                                        ratio = float(_div(rho, rhoend))
                                        if not (ratio <= 16.0):
                                            _pc = 638
                                            continue
                                        _pc = 636
                                        continue
                                else:
                                    if _pc < 638:
                                        # newuob: basic block 636
                                        rho = float(rhoend)
                                        _pc = 642
                                        continue
                                    else:
                                        if _pc < 639:
                                            # newuob: basic block 638
                                            if not (ratio <= 250.0):
                                                _pc = 641
                                                continue
                                            _pc = 639
                                            continue
                                        else:
                                            # newuob: basic block 639
                                            rho = float(_sqrt(ratio) * rhoend)
                                            _pc = 642
                                            continue
                            else:
                                if _pc < 645:
                                    if _pc < 642:
                                        # newuob: basic block 641
                                        rho = float(tenth * rho)
                                        _pc = 642
                                        continue
                                    else:
                                        if _pc < 644:
                                            # newuob: basic block 642
                                            delta = float(_max(delta, rho))
                                            if not (iprint >= 2):
                                                _pc = 651
                                                continue
                                            _pc = 644
                                            continue
                                        else:
                                            # newuob: basic block 644
                                            if not (iprint >= 3):
                                                _pc = 646
                                                continue
                                            _pc = 645
                                            continue
                                else:
                                    if _pc < 646:
                                        # newuob: basic block 645
                                        pass
                                        _pc = 646
                                        continue
                                    else:
                                        if _pc < 651:
                                            # newuob: basic block 646
                                            pass
                                            pass
                                            pass
                                            pass
                                            pass
                                            _pc = 651
                                            continue
                                        else:
                                            # newuob: basic block 651
                                            _pc = 137
                                            continue
                        else:
                            if _pc < 658:
                                if _pc < 655:
                                    if _pc < 653:
                                        # newuob: basic block 652
                                        _pc = 654
                                        continue
                                    else:
                                        if _pc < 654:
                                            # newuob: basic block 653
                                            info = int(0)
                                            _pc = 654
                                            continue
                                        else:
                                            # newuob: basic block 654
                                            if not (knew == -1):
                                                _pc = 656
                                                continue
                                            _pc = 655
                                            continue
                                else:
                                    if _pc < 656:
                                        # newuob: basic block 655
                                        _pc = 370
                                        continue
                                    else:
                                        if _pc < 657:
                                            # newuob: basic block 656
                                            if not (fopt <= f or f != f):
                                                _pc = 663
                                                continue
                                            _pc = 657
                                            continue
                                        else:
                                            # newuob: basic block 657
                                            i = int(1); _end657 = int(n); _step657 = int(1)
                                            _pc = 658
                                            continue
                            else:
                                if _pc < 663:
                                    if _pc < 659:
                                        # newuob: basic block 658
                                        if (i > _end657 if _step657 > 0 else i < _end657):
                                            _pc = 662
                                            continue
                                        _pc = 659
                                        continue
                                    else:
                                        if _pc < 662:
                                            # newuob: basic block 659
                                            x[i] = xbase[i] + xopt[i]
                                            i += _step657
                                            _pc = 658
                                            continue
                                        else:
                                            # newuob: basic block 662
                                            f = float(fopt)
                                            _pc = 663
                                            continue
                                else:
                                    if _pc < 664:
                                        # newuob: basic block 663
                                        if not (iprint >= 1):
                                            _pc = 667
                                            continue
                                        _pc = 664
                                        continue
                                    else:
                                        if _pc < 667:
                                            # newuob: basic block 664
                                            pass
                                            pass
                                            pass
                                            _pc = 667
                                            continue
                                        else:
                                            # newuob: basic block 667
                                            return n, npt, rhobeg, rhoend, iprint, maxfun, ndim, f, info, ftarget

def _trsapp(_ctx, n, npt, xopt, xpt, gq, hq, pq, delta, step, d, g, hd, hs, crvmin):
    alpha = 0.0
    angle = 0.0
    angtest = 0.0
    bstep = 0.0
    cf = 0.0
    cth = 0.0
    datan = 0.0
    dcos = 0.0
    dd = 0.0
    delsq = 0.0
    dfloat = 0.0
    dg = 0.0
    dhd = 0.0
    dhs = 0.0
    dmin1 = 0.0
    ds = 0.0
    dsin = 0.0
    dsqrt = 0.0
    gg = 0.0
    ggbeg = 0.0
    ggsav = 0.0
    half = 0.0
    i = 0
    ih = 0
    isave = 0
    iterc = 0
    itermax = 0
    itersw = 0
    iu = 0
    j = 0
    k = 0
    qadd = 0.0
    qbeg = 0.0
    qmin = 0.0
    qnew = 0.0
    qred = 0.0
    qsav = 0.0
    ratio = 0.0
    reduc = 0.0
    sg = 0.0
    sgk = 0.0
    shs = 0.0
    ss = 0.0
    sth = 0.0
    temp = 0.0
    tempa = 0.0
    tempb = 0.0
    twopi = 0.0
    zero = 0.0
    xpt = xpt.with_leading(npt)
    _pc = 0
    while True:
        if _pc < 108:
            if _pc < 61:
                if _pc < 35:
                    if _pc < 16:
                        if _pc < 9:
                            if _pc < 8:
                                # trsapp: basic block 0
                                half = float(0.5)
                                zero = float(0.0)
                                twopi = float(8.0 * _atan(1.0))
                                delsq = float(delta * delta)
                                iterc = int(0)
                                itermax = int(n)
                                itersw = int(itermax)
                                i = int(1); _end7 = int(n); _step7 = int(1)
                                _pc = 8
                                continue
                            else:
                                # trsapp: basic block 8
                                if (i > _end7 if _step7 > 0 else i < _end7):
                                    _pc = 12
                                    continue
                                _pc = 9
                                continue
                        else:
                            if _pc < 12:
                                # trsapp: basic block 9
                                d[i] = xopt[i]
                                i += _step7
                                _pc = 8
                                continue
                            else:
                                if _pc < 13:
                                    # trsapp: basic block 12
                                    _pc = 167
                                    continue
                                else:
                                    # trsapp: basic block 13
                                    qred = float(zero)
                                    dd = float(zero)
                                    i = int(1); _end15 = int(n); _step15 = int(1)
                                    _pc = 16
                                    continue
                    else:
                        if _pc < 26:
                            if _pc < 17:
                                # trsapp: basic block 16
                                if (i > _end15 if _step15 > 0 else i < _end15):
                                    _pc = 24
                                    continue
                                _pc = 17
                                continue
                            else:
                                if _pc < 24:
                                    # trsapp: basic block 17
                                    step[i] = zero
                                    hs[i] = zero
                                    g[i] = gq[i] + hd[i]
                                    d[i] = -g[i]
                                    dd = float(dd + d[i] * d[i])
                                    i += _step15
                                    _pc = 16
                                    continue
                                else:
                                    # trsapp: basic block 24
                                    crvmin = float(zero)
                                    if not (dd == zero):
                                        _pc = 27
                                        continue
                                    _pc = 26
                                    continue
                        else:
                            if _pc < 27:
                                # trsapp: basic block 26
                                _pc = 166
                                continue
                            else:
                                if _pc < 31:
                                    # trsapp: basic block 27
                                    ds = float(zero)
                                    ss = float(zero)
                                    gg = float(dd)
                                    ggbeg = float(gg)
                                    _pc = 31
                                    continue
                                else:
                                    # trsapp: basic block 31
                                    iterc = int(iterc + 1)
                                    temp = float(delsq - ss)
                                    bstep = float(_div(temp, ds + _sqrt(ds * ds + dd * temp)))
                                    _pc = 167
                                    continue
                else:
                    if _pc < 46:
                        if _pc < 41:
                            if _pc < 37:
                                # trsapp: basic block 35
                                dhd = float(zero)
                                j = int(1); _end36 = int(n); _step36 = int(1)
                                _pc = 37
                                continue
                            else:
                                if _pc < 38:
                                    # trsapp: basic block 37
                                    if (j > _end36 if _step36 > 0 else j < _end36):
                                        _pc = 41
                                        continue
                                    _pc = 38
                                    continue
                                else:
                                    # trsapp: basic block 38
                                    dhd = float(dhd + d[j] * hd[j])
                                    j += _step36
                                    _pc = 37
                                    continue
                        else:
                            if _pc < 43:
                                # trsapp: basic block 41
                                alpha = float(bstep)
                                if not (dhd > zero):
                                    _pc = 48
                                    continue
                                _pc = 43
                                continue
                            else:
                                if _pc < 45:
                                    # trsapp: basic block 43
                                    temp = float(_div(dhd, dd))
                                    if not (iterc == 1):
                                        _pc = 46
                                        continue
                                    _pc = 45
                                    continue
                                else:
                                    # trsapp: basic block 45
                                    crvmin = float(temp)
                                    _pc = 46
                                    continue
                    else:
                        if _pc < 54:
                            if _pc < 48:
                                # trsapp: basic block 46
                                crvmin = float(_min(crvmin, temp))
                                alpha = float(_min(alpha, _div(gg, dhd)))
                                _pc = 48
                                continue
                            else:
                                if _pc < 53:
                                    # trsapp: basic block 48
                                    qadd = float(alpha * (gg - half * alpha * dhd))
                                    qred = float(qred + qadd)
                                    ggsav = float(gg)
                                    gg = float(zero)
                                    i = int(1); _end52 = int(n); _step52 = int(1)
                                    _pc = 53
                                    continue
                                else:
                                    # trsapp: basic block 53
                                    if (i > _end52 if _step52 > 0 else i < _end52):
                                        _pc = 59
                                        continue
                                    _pc = 54
                                    continue
                        else:
                            if _pc < 59:
                                # trsapp: basic block 54
                                step[i] = step[i] + alpha * d[i]
                                hs[i] = hs[i] + alpha * hd[i]
                                gg = float(gg + (g[i] + hs[i]) * (g[i] + hs[i]))
                                i += _step52
                                _pc = 53
                                continue
                            else:
                                if _pc < 60:
                                    # trsapp: basic block 59
                                    if not (alpha < bstep):
                                        _pc = 82
                                        continue
                                    _pc = 60
                                    continue
                                else:
                                    # trsapp: basic block 60
                                    if not (qadd <= 0.01 * qred):
                                        _pc = 62
                                        continue
                                    _pc = 61
                                    continue
            else:
                if _pc < 82:
                    if _pc < 71:
                        if _pc < 64:
                            if _pc < 62:
                                # trsapp: basic block 61
                                _pc = 166
                                continue
                            else:
                                if _pc < 63:
                                    # trsapp: basic block 62
                                    if not (gg <= 0.0001 * ggbeg):
                                        _pc = 64
                                        continue
                                    _pc = 63
                                    continue
                                else:
                                    # trsapp: basic block 63
                                    _pc = 166
                                    continue
                        else:
                            if _pc < 65:
                                # trsapp: basic block 64
                                if not (iterc == itermax):
                                    _pc = 66
                                    continue
                                _pc = 65
                                continue
                            else:
                                if _pc < 66:
                                    # trsapp: basic block 65
                                    _pc = 166
                                    continue
                                else:
                                    # trsapp: basic block 66
                                    temp = float(_div(gg, ggsav))
                                    dd = float(zero)
                                    ds = float(zero)
                                    ss = float(zero)
                                    i = int(1); _end70 = int(n); _step70 = int(1)
                                    _pc = 71
                                    continue
                    else:
                        if _pc < 79:
                            if _pc < 72:
                                # trsapp: basic block 71
                                if (i > _end70 if _step70 > 0 else i < _end70):
                                    _pc = 78
                                    continue
                                _pc = 72
                                continue
                            else:
                                if _pc < 78:
                                    # trsapp: basic block 72
                                    d[i] = temp * d[i] - g[i] - hs[i]
                                    dd = float(dd + d[i] * d[i])
                                    ds = float(ds + d[i] * step[i])
                                    ss = float(ss + step[i] * step[i])
                                    i += _step70
                                    _pc = 71
                                    continue
                                else:
                                    # trsapp: basic block 78
                                    if not (ds <= zero):
                                        _pc = 80
                                        continue
                                    _pc = 79
                                    continue
                        else:
                            if _pc < 80:
                                # trsapp: basic block 79
                                _pc = 166
                                continue
                            else:
                                if _pc < 81:
                                    # trsapp: basic block 80
                                    if not (ss < delsq):
                                        _pc = 82
                                        continue
                                    _pc = 81
                                    continue
                                else:
                                    # trsapp: basic block 81
                                    _pc = 31
                                    continue
                else:
                    if _pc < 94:
                        if _pc < 86:
                            if _pc < 84:
                                # trsapp: basic block 82
                                crvmin = float(zero)
                                itersw = int(iterc)
                                _pc = 84
                                continue
                            else:
                                if _pc < 85:
                                    # trsapp: basic block 84
                                    if not (gg <= 0.0001 * ggbeg):
                                        _pc = 86
                                        continue
                                    _pc = 85
                                    continue
                                else:
                                    # trsapp: basic block 85
                                    _pc = 166
                                    continue
                        else:
                            if _pc < 89:
                                # trsapp: basic block 86
                                sg = float(zero)
                                shs = float(zero)
                                i = int(1); _end88 = int(n); _step88 = int(1)
                                _pc = 89
                                continue
                            else:
                                if _pc < 90:
                                    # trsapp: basic block 89
                                    if (i > _end88 if _step88 > 0 else i < _end88):
                                        _pc = 94
                                        continue
                                    _pc = 90
                                    continue
                                else:
                                    # trsapp: basic block 90
                                    sg = float(sg + step[i] * g[i])
                                    shs = float(shs + step[i] * hs[i])
                                    i += _step88
                                    _pc = 89
                                    continue
                    else:
                        if _pc < 103:
                            if _pc < 97:
                                # trsapp: basic block 94
                                sgk = float(sg + shs)
                                angtest = float(_div(sgk, _sqrt(gg * delsq)))
                                if not (angtest <= -0.99):
                                    _pc = 98
                                    continue
                                _pc = 97
                                continue
                            else:
                                if _pc < 98:
                                    # trsapp: basic block 97
                                    _pc = 166
                                    continue
                                else:
                                    # trsapp: basic block 98
                                    iterc = int(iterc + 1)
                                    temp = float(_sqrt(delsq * gg - sgk * sgk))
                                    tempa = float(_div(delsq, temp))
                                    tempb = float(_div(sgk, temp))
                                    i = int(1); _end102 = int(n); _step102 = int(1)
                                    _pc = 103
                                    continue
                        else:
                            if _pc < 104:
                                # trsapp: basic block 103
                                if (i > _end102 if _step102 > 0 else i < _end102):
                                    _pc = 107
                                    continue
                                _pc = 104
                                continue
                            else:
                                if _pc < 107:
                                    # trsapp: basic block 104
                                    d[i] = tempa * (g[i] + hs[i]) - tempb * step[i]
                                    i += _step102
                                    _pc = 103
                                    continue
                                else:
                                    # trsapp: basic block 107
                                    _pc = 167
                                    continue
        else:
            if _pc < 168:
                if _pc < 142:
                    if _pc < 127:
                        if _pc < 113:
                            if _pc < 112:
                                # trsapp: basic block 108
                                dg = float(zero)
                                dhd = float(zero)
                                dhs = float(zero)
                                i = int(1); _end111 = int(n); _step111 = int(1)
                                _pc = 112
                                continue
                            else:
                                # trsapp: basic block 112
                                if (i > _end111 if _step111 > 0 else i < _end111):
                                    _pc = 118
                                    continue
                                _pc = 113
                                continue
                        else:
                            if _pc < 118:
                                # trsapp: basic block 113
                                dg = float(dg + d[i] * g[i])
                                dhd = float(dhd + hd[i] * d[i])
                                dhs = float(dhs + hd[i] * step[i])
                                i += _step111
                                _pc = 112
                                continue
                            else:
                                if _pc < 126:
                                    # trsapp: basic block 118
                                    cf = float(half * (shs - dhd))
                                    qbeg = float(sg + cf)
                                    qsav = float(qbeg)
                                    qmin = float(qbeg)
                                    isave = int(0)
                                    iu = int(49)
                                    temp = float(_div(twopi, float(iu + 1)))
                                    i = int(1); _end125 = int(iu); _step125 = int(1)
                                    _pc = 126
                                    continue
                                else:
                                    # trsapp: basic block 126
                                    if (i > _end125 if _step125 > 0 else i < _end125):
                                        _pc = 141
                                        continue
                                    _pc = 127
                                    continue
                    else:
                        if _pc < 137:
                            if _pc < 132:
                                # trsapp: basic block 127
                                angle = float(float(i) * temp)
                                cth = float(_cos(angle))
                                sth = float(_sin(angle))
                                qnew = float((sg + cf * cth) * cth + (dg + dhs * cth) * sth)
                                if not (qnew < qmin):
                                    _pc = 136
                                    continue
                                _pc = 132
                                continue
                            else:
                                if _pc < 136:
                                    # trsapp: basic block 132
                                    qmin = float(qnew)
                                    isave = int(i)
                                    tempa = float(qsav)
                                    _pc = 138
                                    continue
                                else:
                                    # trsapp: basic block 136
                                    if not (i == isave + 1):
                                        _pc = 138
                                        continue
                                    _pc = 137
                                    continue
                        else:
                            if _pc < 138:
                                # trsapp: basic block 137
                                tempb = float(qnew)
                                _pc = 138
                                continue
                            else:
                                if _pc < 141:
                                    # trsapp: basic block 138
                                    qsav = float(qnew)
                                    i += _step125
                                    _pc = 126
                                    continue
                                else:
                                    # trsapp: basic block 141
                                    if not (isave == zero):
                                        _pc = 143
                                        continue
                                    _pc = 142
                                    continue
                else:
                    if _pc < 156:
                        if _pc < 145:
                            if _pc < 143:
                                # trsapp: basic block 142
                                tempa = float(qnew)
                                _pc = 143
                                continue
                            else:
                                if _pc < 144:
                                    # trsapp: basic block 143
                                    if not (isave == iu):
                                        _pc = 145
                                        continue
                                    _pc = 144
                                    continue
                                else:
                                    # trsapp: basic block 144
                                    tempb = float(qbeg)
                                    _pc = 145
                                    continue
                        else:
                            if _pc < 147:
                                # trsapp: basic block 145
                                angle = float(zero)
                                if not (tempa != tempb):
                                    _pc = 150
                                    continue
                                _pc = 147
                                continue
                            else:
                                if _pc < 150:
                                    # trsapp: basic block 147
                                    tempa = float(tempa - qmin)
                                    tempb = float(tempb - qmin)
                                    angle = float(_div(half * (tempa - tempb), tempa + tempb))
                                    _pc = 150
                                    continue
                                else:
                                    # trsapp: basic block 150
                                    angle = float(temp * (float(isave) + angle))
                                    cth = float(_cos(angle))
                                    sth = float(_sin(angle))
                                    reduc = float(qbeg - (sg + cf * cth) * cth - (dg + dhs * cth) * sth)
                                    gg = float(zero)
                                    i = int(1); _end155 = int(n); _step155 = int(1)
                                    _pc = 156
                                    continue
                    else:
                        if _pc < 165:
                            if _pc < 157:
                                # trsapp: basic block 156
                                if (i > _end155 if _step155 > 0 else i < _end155):
                                    _pc = 162
                                    continue
                                _pc = 157
                                continue
                            else:
                                if _pc < 162:
                                    # trsapp: basic block 157
                                    step[i] = cth * step[i] + sth * d[i]
                                    hs[i] = cth * hs[i] + sth * hd[i]
                                    gg = float(gg + (g[i] + hs[i]) * (g[i] + hs[i]))
                                    i += _step155
                                    _pc = 156
                                    continue
                                else:
                                    # trsapp: basic block 162
                                    qred = float(qred + reduc)
                                    ratio = float(_div(reduc, qred))
                                    if not (iterc < itermax and ratio > 0.01):
                                        _pc = 166
                                        continue
                                    _pc = 165
                                    continue
                        else:
                            if _pc < 166:
                                # trsapp: basic block 165
                                _pc = 84
                                continue
                            else:
                                if _pc < 167:
                                    # trsapp: basic block 166
                                    return n, npt, delta, crvmin
                                else:
                                    # trsapp: basic block 167
                                    i = int(1); _end167 = int(n); _step167 = int(1)
                                    _pc = 168
                                    continue
            else:
                if _pc < 190:
                    if _pc < 177:
                        if _pc < 173:
                            if _pc < 169:
                                # trsapp: basic block 168
                                if (i > _end167 if _step167 > 0 else i < _end167):
                                    _pc = 172
                                    continue
                                _pc = 169
                                continue
                            else:
                                if _pc < 172:
                                    # trsapp: basic block 169
                                    hd[i] = zero
                                    i += _step167
                                    _pc = 168
                                    continue
                                else:
                                    # trsapp: basic block 172
                                    k = int(1); _end172 = int(npt); _step172 = int(1)
                                    _pc = 173
                                    continue
                        else:
                            if _pc < 174:
                                # trsapp: basic block 173
                                if (k > _end172 if _step172 > 0 else k < _end172):
                                    _pc = 188
                                    continue
                                _pc = 174
                                continue
                            else:
                                if _pc < 176:
                                    # trsapp: basic block 174
                                    temp = float(zero)
                                    j = int(1); _end175 = int(n); _step175 = int(1)
                                    _pc = 176
                                    continue
                                else:
                                    # trsapp: basic block 176
                                    if (j > _end175 if _step175 > 0 else j < _end175):
                                        _pc = 180
                                        continue
                                    _pc = 177
                                    continue
                    else:
                        if _pc < 183:
                            if _pc < 180:
                                # trsapp: basic block 177
                                temp = float(temp + xpt[k, j] * d[j])
                                j += _step175
                                _pc = 176
                                continue
                            else:
                                if _pc < 182:
                                    # trsapp: basic block 180
                                    temp = float(temp * pq[k])
                                    i = int(1); _end181 = int(n); _step181 = int(1)
                                    _pc = 182
                                    continue
                                else:
                                    # trsapp: basic block 182
                                    if (i > _end181 if _step181 > 0 else i < _end181):
                                        _pc = 186
                                        continue
                                    _pc = 183
                                    continue
                        else:
                            if _pc < 186:
                                # trsapp: basic block 183
                                hd[i] = hd[i] + temp * xpt[k, i]
                                i += _step181
                                _pc = 182
                                continue
                            else:
                                if _pc < 188:
                                    # trsapp: basic block 186
                                    k += _step172
                                    _pc = 173
                                    continue
                                else:
                                    # trsapp: basic block 188
                                    ih = int(0)
                                    j = int(1); _end189 = int(n); _step189 = int(1)
                                    _pc = 190
                                    continue
                else:
                    if _pc < 199:
                        if _pc < 193:
                            if _pc < 191:
                                # trsapp: basic block 190
                                if (j > _end189 if _step189 > 0 else j < _end189):
                                    _pc = 201
                                    continue
                                _pc = 191
                                continue
                            else:
                                if _pc < 192:
                                    # trsapp: basic block 191
                                    i = int(1); _end191 = int(j); _step191 = int(1)
                                    _pc = 192
                                    continue
                                else:
                                    # trsapp: basic block 192
                                    if (i > _end191 if _step191 > 0 else i < _end191):
                                        _pc = 199
                                        continue
                                    _pc = 193
                                    continue
                        else:
                            if _pc < 195:
                                # trsapp: basic block 193
                                ih = int(ih + 1)
                                if not (i < j):
                                    _pc = 196
                                    continue
                                _pc = 195
                                continue
                            else:
                                if _pc < 196:
                                    # trsapp: basic block 195
                                    hd[j] = hd[j] + hq[ih] * d[i]
                                    _pc = 196
                                    continue
                                else:
                                    # trsapp: basic block 196
                                    hd[i] = hd[i] + hq[ih] * d[j]
                                    i += _step191
                                    _pc = 192
                                    continue
                    else:
                        if _pc < 203:
                            if _pc < 201:
                                # trsapp: basic block 199
                                j += _step189
                                _pc = 190
                                continue
                            else:
                                if _pc < 202:
                                    # trsapp: basic block 201
                                    if not (iterc == 0):
                                        _pc = 203
                                        continue
                                    _pc = 202
                                    continue
                                else:
                                    # trsapp: basic block 202
                                    _pc = 13
                                    continue
                        else:
                            if _pc < 204:
                                # trsapp: basic block 203
                                if not (iterc <= itersw):
                                    _pc = 205
                                    continue
                                _pc = 204
                                continue
                            else:
                                if _pc < 205:
                                    # trsapp: basic block 204
                                    _pc = 35
                                    continue
                                else:
                                    # trsapp: basic block 205
                                    _pc = 108
                                    continue

def _biglag(_ctx, n, npt, xopt, xpt, bmat, zmat, idz, ndim, knew, delta, d, alpha, hcol, gc, gd, s, w):
    angle = 0.0
    cf1 = 0.0
    cf2 = 0.0
    cf3 = 0.0
    cf4 = 0.0
    cf5 = 0.0
    cth = 0.0
    dabs = 0.0
    datan = 0.0
    dcos = 0.0
    dd = 0.0
    delsq = 0.0
    denom = 0.0
    dfloat = 0.0
    dhd = 0.0
    dsin = 0.0
    dsqrt = 0.0
    gg = 0.0
    half = 0.0
    i = 0
    isave = 0
    iterc = 0
    iu = 0
    j = 0
    k = 0
    nptm = 0
    one = 0.0
    scale = 0.0
    sp = 0.0
    ss = 0.0
    step = 0.0
    sth = 0.0
    sum = 0.0
    tau = 0.0
    taubeg = 0.0
    taumax = 0.0
    tauold = 0.0
    temp = 0.0
    tempa = 0.0
    tempb = 0.0
    twopi = 0.0
    zero = 0.0
    xpt = xpt.with_leading(npt)
    bmat = bmat.with_leading(ndim)
    zmat = zmat.with_leading(npt)
    _pc = 0
    while True:
        if _pc < 91:
            if _pc < 44:
                if _pc < 19:
                    if _pc < 13:
                        if _pc < 9:
                            if _pc < 8:
                                # biglag: basic block 0
                                half = float(0.5)
                                one = float(1.0)
                                zero = float(0.0)
                                twopi = float(8.0 * _atan(one))
                                delsq = float(delta * delta)
                                nptm = int(npt - n - 1)
                                iterc = int(0)
                                k = int(1); _end7 = int(npt); _step7 = int(1)
                                _pc = 8
                                continue
                            else:
                                # biglag: basic block 8
                                if (k > _end7 if _step7 > 0 else k < _end7):
                                    _pc = 12
                                    continue
                                _pc = 9
                                continue
                        else:
                            if _pc < 12:
                                # biglag: basic block 9
                                hcol[k] = zero
                                k += _step7
                                _pc = 8
                                continue
                            else:
                                # biglag: basic block 12
                                j = int(1); _end12 = int(nptm); _step12 = int(1)
                                _pc = 13
                                continue
                    else:
                        if _pc < 16:
                            if _pc < 14:
                                # biglag: basic block 13
                                if (j > _end12 if _step12 > 0 else j < _end12):
                                    _pc = 24
                                    continue
                                _pc = 14
                                continue
                            else:
                                # biglag: basic block 14
                                temp = float(zmat[knew, j])
                                if not (j < idz):
                                    _pc = 17
                                    continue
                                _pc = 16
                                continue
                        else:
                            if _pc < 17:
                                # biglag: basic block 16
                                temp = float(-temp)
                                _pc = 17
                                continue
                            else:
                                if _pc < 18:
                                    # biglag: basic block 17
                                    k = int(1); _end17 = int(npt); _step17 = int(1)
                                    _pc = 18
                                    continue
                                else:
                                    # biglag: basic block 18
                                    if (k > _end17 if _step17 > 0 else k < _end17):
                                        _pc = 22
                                        continue
                                    _pc = 19
                                    continue
                else:
                    if _pc < 34:
                        if _pc < 24:
                            if _pc < 22:
                                # biglag: basic block 19
                                hcol[k] = hcol[k] + temp * zmat[k, j]
                                k += _step17
                                _pc = 18
                                continue
                            else:
                                # biglag: basic block 22
                                j += _step12
                                _pc = 13
                                continue
                        else:
                            if _pc < 27:
                                # biglag: basic block 24
                                alpha = float(hcol[knew])
                                dd = float(zero)
                                i = int(1); _end26 = int(n); _step26 = int(1)
                                _pc = 27
                                continue
                            else:
                                if _pc < 28:
                                    # biglag: basic block 27
                                    if (i > _end26 if _step26 > 0 else i < _end26):
                                        _pc = 34
                                        continue
                                    _pc = 28
                                    continue
                                else:
                                    # biglag: basic block 28
                                    d[i] = xpt[knew, i] - xopt[i]
                                    gc[i] = bmat[knew, i]
                                    gd[i] = zero
                                    dd = float(dd + d[i] * d[i])
                                    i += _step26
                                    _pc = 27
                                    continue
                    else:
                        if _pc < 36:
                            if _pc < 35:
                                # biglag: basic block 34
                                k = int(1); _end34 = int(npt); _step34 = int(1)
                                _pc = 35
                                continue
                            else:
                                # biglag: basic block 35
                                if (k > _end34 if _step34 > 0 else k < _end34):
                                    _pc = 54
                                    continue
                                _pc = 36
                                continue
                        else:
                            if _pc < 39:
                                # biglag: basic block 36
                                temp = float(zero)
                                sum = float(zero)
                                j = int(1); _end38 = int(n); _step38 = int(1)
                                _pc = 39
                                continue
                            else:
                                if _pc < 40:
                                    # biglag: basic block 39
                                    if (j > _end38 if _step38 > 0 else j < _end38):
                                        _pc = 44
                                        continue
                                    _pc = 40
                                    continue
                                else:
                                    # biglag: basic block 40
                                    temp = float(temp + xpt[k, j] * xopt[j])
                                    sum = float(sum + xpt[k, j] * d[j])
                                    j += _step38
                                    _pc = 39
                                    continue
            else:
                if _pc < 67:
                    if _pc < 54:
                        if _pc < 48:
                            if _pc < 47:
                                # biglag: basic block 44
                                temp = float(hcol[k] * temp)
                                sum = float(hcol[k] * sum)
                                i = int(1); _end46 = int(n); _step46 = int(1)
                                _pc = 47
                                continue
                            else:
                                # biglag: basic block 47
                                if (i > _end46 if _step46 > 0 else i < _end46):
                                    _pc = 52
                                    continue
                                _pc = 48
                                continue
                        else:
                            if _pc < 52:
                                # biglag: basic block 48
                                gc[i] = gc[i] + temp * xpt[k, i]
                                gd[i] = gd[i] + sum * xpt[k, i]
                                i += _step46
                                _pc = 47
                                continue
                            else:
                                # biglag: basic block 52
                                k += _step34
                                _pc = 35
                                continue
                    else:
                        if _pc < 59:
                            if _pc < 58:
                                # biglag: basic block 54
                                gg = float(zero)
                                sp = float(zero)
                                dhd = float(zero)
                                i = int(1); _end57 = int(n); _step57 = int(1)
                                _pc = 58
                                continue
                            else:
                                # biglag: basic block 58
                                if (i > _end57 if _step57 > 0 else i < _end57):
                                    _pc = 64
                                    continue
                                _pc = 59
                                continue
                        else:
                            if _pc < 64:
                                # biglag: basic block 59
                                gg = float(gg + gc[i] * gc[i])
                                sp = float(sp + d[i] * gc[i])
                                dhd = float(dhd + d[i] * gd[i])
                                i += _step57
                                _pc = 58
                                continue
                            else:
                                if _pc < 66:
                                    # biglag: basic block 64
                                    scale = float(_div(delta, _sqrt(dd)))
                                    if not (sp * dhd < zero):
                                        _pc = 67
                                        continue
                                    _pc = 66
                                    continue
                                else:
                                    # biglag: basic block 66
                                    scale = float(-scale)
                                    _pc = 67
                                    continue
                else:
                    if _pc < 74:
                        if _pc < 70:
                            if _pc < 69:
                                # biglag: basic block 67
                                temp = float(zero)
                                if not (sp * sp > 0.99 * dd * gg):
                                    _pc = 70
                                    continue
                                _pc = 69
                                continue
                            else:
                                # biglag: basic block 69
                                temp = float(one)
                                _pc = 70
                                continue
                        else:
                            if _pc < 72:
                                # biglag: basic block 70
                                tau = float(scale * (abs(sp) + half * scale * abs(dhd)))
                                if not (gg * delsq < 0.01 * tau * tau):
                                    _pc = 73
                                    continue
                                _pc = 72
                                continue
                            else:
                                if _pc < 73:
                                    # biglag: basic block 72
                                    temp = float(one)
                                    _pc = 73
                                    continue
                                else:
                                    # biglag: basic block 73
                                    i = int(1); _end73 = int(n); _step73 = int(1)
                                    _pc = 74
                                    continue
                    else:
                        if _pc < 80:
                            if _pc < 75:
                                # biglag: basic block 74
                                if (i > _end73 if _step73 > 0 else i < _end73):
                                    _pc = 80
                                    continue
                                _pc = 75
                                continue
                            else:
                                # biglag: basic block 75
                                d[i] = scale * d[i]
                                gd[i] = scale * gd[i]
                                s[i] = gc[i] + temp * gd[i]
                                i += _step73
                                _pc = 74
                                continue
                        else:
                            if _pc < 85:
                                # biglag: basic block 80
                                iterc = int(iterc + 1)
                                dd = float(zero)
                                sp = float(zero)
                                ss = float(zero)
                                i = int(1); _end84 = int(n); _step84 = int(1)
                                _pc = 85
                                continue
                            else:
                                if _pc < 86:
                                    # biglag: basic block 85
                                    if (i > _end84 if _step84 > 0 else i < _end84):
                                        _pc = 91
                                        continue
                                    _pc = 86
                                    continue
                                else:
                                    # biglag: basic block 86
                                    dd = float(dd + d[i] * d[i])
                                    sp = float(sp + d[i] * s[i])
                                    ss = float(ss + s[i] * s[i])
                                    i += _step84
                                    _pc = 85
                                    continue
        else:
            if _pc < 141:
                if _pc < 106:
                    if _pc < 97:
                        if _pc < 94:
                            if _pc < 93:
                                # biglag: basic block 91
                                temp = float(dd * ss - sp * sp)
                                if not (temp <= 1e-08 * dd * ss):
                                    _pc = 94
                                    continue
                                _pc = 93
                                continue
                            else:
                                # biglag: basic block 93
                                _pc = 179
                                continue
                        else:
                            if _pc < 96:
                                # biglag: basic block 94
                                denom = float(_sqrt(temp))
                                i = int(1); _end95 = int(n); _step95 = int(1)
                                _pc = 96
                                continue
                            else:
                                # biglag: basic block 96
                                if (i > _end95 if _step95 > 0 else i < _end95):
                                    _pc = 101
                                    continue
                                _pc = 97
                                continue
                    else:
                        if _pc < 102:
                            if _pc < 101:
                                # biglag: basic block 97
                                s[i] = _div(dd * s[i] - sp * d[i], denom)
                                w[i] = zero
                                i += _step95
                                _pc = 96
                                continue
                            else:
                                # biglag: basic block 101
                                k = int(1); _end101 = int(npt); _step101 = int(1)
                                _pc = 102
                                continue
                        else:
                            if _pc < 103:
                                # biglag: basic block 102
                                if (k > _end101 if _step101 > 0 else k < _end101):
                                    _pc = 117
                                    continue
                                _pc = 103
                                continue
                            else:
                                if _pc < 105:
                                    # biglag: basic block 103
                                    sum = float(zero)
                                    j = int(1); _end104 = int(n); _step104 = int(1)
                                    _pc = 105
                                    continue
                                else:
                                    # biglag: basic block 105
                                    if (j > _end104 if _step104 > 0 else j < _end104):
                                        _pc = 109
                                        continue
                                    _pc = 106
                                    continue
                else:
                    if _pc < 117:
                        if _pc < 111:
                            if _pc < 109:
                                # biglag: basic block 106
                                sum = float(sum + xpt[k, j] * s[j])
                                j += _step104
                                _pc = 105
                                continue
                            else:
                                # biglag: basic block 109
                                sum = float(hcol[k] * sum)
                                i = int(1); _end110 = int(n); _step110 = int(1)
                                _pc = 111
                                continue
                        else:
                            if _pc < 112:
                                # biglag: basic block 111
                                if (i > _end110 if _step110 > 0 else i < _end110):
                                    _pc = 115
                                    continue
                                _pc = 112
                                continue
                            else:
                                if _pc < 115:
                                    # biglag: basic block 112
                                    w[i] = w[i] + sum * xpt[k, i]
                                    i += _step110
                                    _pc = 111
                                    continue
                                else:
                                    # biglag: basic block 115
                                    k += _step101
                                    _pc = 102
                                    continue
                    else:
                        if _pc < 124:
                            if _pc < 123:
                                # biglag: basic block 117
                                cf1 = float(zero)
                                cf2 = float(zero)
                                cf3 = float(zero)
                                cf4 = float(zero)
                                cf5 = float(zero)
                                i = int(1); _end122 = int(n); _step122 = int(1)
                                _pc = 123
                                continue
                            else:
                                # biglag: basic block 123
                                if (i > _end122 if _step122 > 0 else i < _end122):
                                    _pc = 131
                                    continue
                                _pc = 124
                                continue
                        else:
                            if _pc < 131:
                                # biglag: basic block 124
                                cf1 = float(cf1 + s[i] * w[i])
                                cf2 = float(cf2 + d[i] * gc[i])
                                cf3 = float(cf3 + s[i] * gc[i])
                                cf4 = float(cf4 + d[i] * gd[i])
                                cf5 = float(cf5 + s[i] * gd[i])
                                i += _step122
                                _pc = 123
                                continue
                            else:
                                if _pc < 140:
                                    # biglag: basic block 131
                                    cf1 = float(half * cf1)
                                    cf4 = float(half * cf4 - cf1)
                                    taubeg = float(cf1 + cf2 + cf4)
                                    taumax = float(taubeg)
                                    tauold = float(taubeg)
                                    isave = int(0)
                                    iu = int(49)
                                    temp = float(_div(twopi, float(iu + 1)))
                                    i = int(1); _end139 = int(iu); _step139 = int(1)
                                    _pc = 140
                                    continue
                                else:
                                    # biglag: basic block 140
                                    if (i > _end139 if _step139 > 0 else i < _end139):
                                        _pc = 155
                                        continue
                                    _pc = 141
                                    continue
            else:
                if _pc < 159:
                    if _pc < 152:
                        if _pc < 150:
                            if _pc < 146:
                                # biglag: basic block 141
                                angle = float(float(i) * temp)
                                cth = float(_cos(angle))
                                sth = float(_sin(angle))
                                tau = float(cf1 + (cf2 + cf4 * cth) * cth + (cf3 + cf5 * cth) * sth)
                                if not (abs(tau) > abs(taumax)):
                                    _pc = 150
                                    continue
                                _pc = 146
                                continue
                            else:
                                # biglag: basic block 146
                                taumax = float(tau)
                                isave = int(i)
                                tempa = float(tauold)
                                _pc = 152
                                continue
                        else:
                            if _pc < 151:
                                # biglag: basic block 150
                                if not (i == isave + 1):
                                    _pc = 152
                                    continue
                                _pc = 151
                                continue
                            else:
                                # biglag: basic block 151
                                tempb = float(tau)
                                _pc = 152
                                continue
                    else:
                        if _pc < 156:
                            if _pc < 155:
                                # biglag: basic block 152
                                tauold = float(tau)
                                i += _step139
                                _pc = 140
                                continue
                            else:
                                # biglag: basic block 155
                                if not (isave == 0):
                                    _pc = 157
                                    continue
                                _pc = 156
                                continue
                        else:
                            if _pc < 157:
                                # biglag: basic block 156
                                tempa = float(tau)
                                _pc = 157
                                continue
                            else:
                                if _pc < 158:
                                    # biglag: basic block 157
                                    if not (isave == iu):
                                        _pc = 159
                                        continue
                                    _pc = 158
                                    continue
                                else:
                                    # biglag: basic block 158
                                    tempb = float(taubeg)
                                    _pc = 159
                                    continue
                else:
                    if _pc < 175:
                        if _pc < 164:
                            if _pc < 161:
                                # biglag: basic block 159
                                step = float(zero)
                                if not (tempa != tempb):
                                    _pc = 164
                                    continue
                                _pc = 161
                                continue
                            else:
                                # biglag: basic block 161
                                tempa = float(tempa - taumax)
                                tempb = float(tempb - taumax)
                                step = float(_div(half * (tempa - tempb), tempa + tempb))
                                _pc = 164
                                continue
                        else:
                            if _pc < 169:
                                # biglag: basic block 164
                                angle = float(temp * (float(isave) + step))
                                cth = float(_cos(angle))
                                sth = float(_sin(angle))
                                tau = float(cf1 + (cf2 + cf4 * cth) * cth + (cf3 + cf5 * cth) * sth)
                                i = int(1); _end168 = int(n); _step168 = int(1)
                                _pc = 169
                                continue
                            else:
                                if _pc < 170:
                                    # biglag: basic block 169
                                    if (i > _end168 if _step168 > 0 else i < _end168):
                                        _pc = 175
                                        continue
                                    _pc = 170
                                    continue
                                else:
                                    # biglag: basic block 170
                                    d[i] = cth * d[i] + sth * s[i]
                                    gd[i] = cth * gd[i] + sth * w[i]
                                    s[i] = gc[i] + gd[i]
                                    i += _step168
                                    _pc = 169
                                    continue
                    else:
                        if _pc < 177:
                            if _pc < 176:
                                # biglag: basic block 175
                                if not (abs(tau) <= 1.1 * abs(taubeg)):
                                    _pc = 177
                                    continue
                                _pc = 176
                                continue
                            else:
                                # biglag: basic block 176
                                _pc = 179
                                continue
                        else:
                            if _pc < 178:
                                # biglag: basic block 177
                                if not (iterc < n):
                                    _pc = 179
                                    continue
                                _pc = 178
                                continue
                            else:
                                if _pc < 179:
                                    # biglag: basic block 178
                                    _pc = 80
                                    continue
                                else:
                                    # biglag: basic block 179
                                    return n, npt, idz, ndim, knew, delta, alpha

def _bigden(_ctx, n, npt, xopt, xpt, bmat, zmat, idz, ndim, kopt, knew, d, w, vlag, beta, s, wvec, prod):
    alpha = 0.0
    angle = 0.0
    dabs = 0.0
    datan = 0.0
    dcos = 0.0
    dd = 0.0
    denmax = 0.0
    denold = 0.0
    densav = 0.0
    dfloat = 0.0
    diff = 0.0
    dmax1 = 0.0
    ds = 0.0
    dsin = 0.0
    dsqrt = 0.0
    dstemp = 0.0
    dtest = 0.0
    half = 0.0
    i = 0
    ip = 0
    isave = 0
    iterc = 0
    iu = 0
    j = 0
    jc = 0
    k = 0
    ksav = 0
    nptm = 0
    nw = 0
    one = 0.0
    quart = 0.0
    ss = 0.0
    ssden = 0.0
    sstemp = 0.0
    step = 0.0
    sum = 0.0
    sumold = 0.0
    tau = 0.0
    temp = 0.0
    tempa = 0.0
    tempb = 0.0
    tempc = 0.0
    two = 0.0
    twopi = 0.0
    xoptd = 0.0
    xopts = 0.0
    xoptsq = 0.0
    zero = 0.0
    xpt = xpt.with_leading(npt)
    bmat = bmat.with_leading(ndim)
    zmat = zmat.with_leading(npt)
    wvec = wvec.with_leading(ndim)
    prod = prod.with_leading(ndim)
    den = FArray.zeros(9)
    denex = FArray.zeros(9)
    par = FArray.zeros(9)
    _pc = 0
    while True:
        if _pc < 170:
            if _pc < 97:
                if _pc < 44:
                    if _pc < 19:
                        if _pc < 13:
                            if _pc < 9:
                                if _pc < 8:
                                    # bigden: basic block 0
                                    half = float(0.5)
                                    one = float(1.0)
                                    quart = float(0.25)
                                    two = float(2.0)
                                    zero = float(0.0)
                                    twopi = float(8.0 * _atan(one))
                                    nptm = int(npt - n - 1)
                                    k = int(1); _end7 = int(npt); _step7 = int(1)
                                    _pc = 8
                                    continue
                                else:
                                    # bigden: basic block 8
                                    if (k > _end7 if _step7 > 0 else k < _end7):
                                        _pc = 12
                                        continue
                                    _pc = 9
                                    continue
                            else:
                                if _pc < 12:
                                    # bigden: basic block 9
                                    w[n + k] = zero
                                    k += _step7
                                    _pc = 8
                                    continue
                                else:
                                    # bigden: basic block 12
                                    j = int(1); _end12 = int(nptm); _step12 = int(1)
                                    _pc = 13
                                    continue
                        else:
                            if _pc < 16:
                                if _pc < 14:
                                    # bigden: basic block 13
                                    if (j > _end12 if _step12 > 0 else j < _end12):
                                        _pc = 24
                                        continue
                                    _pc = 14
                                    continue
                                else:
                                    # bigden: basic block 14
                                    temp = float(zmat[knew, j])
                                    if not (j < idz):
                                        _pc = 17
                                        continue
                                    _pc = 16
                                    continue
                            else:
                                if _pc < 17:
                                    # bigden: basic block 16
                                    temp = float(-temp)
                                    _pc = 17
                                    continue
                                else:
                                    if _pc < 18:
                                        # bigden: basic block 17
                                        k = int(1); _end17 = int(npt); _step17 = int(1)
                                        _pc = 18
                                        continue
                                    else:
                                        # bigden: basic block 18
                                        if (k > _end17 if _step17 > 0 else k < _end17):
                                            _pc = 22
                                            continue
                                        _pc = 19
                                        continue
                    else:
                        if _pc < 31:
                            if _pc < 24:
                                if _pc < 22:
                                    # bigden: basic block 19
                                    w[n + k] = w[n + k] + temp * zmat[k, j]
                                    k += _step17
                                    _pc = 18
                                    continue
                                else:
                                    # bigden: basic block 22
                                    j += _step12
                                    _pc = 13
                                    continue
                            else:
                                if _pc < 30:
                                    # bigden: basic block 24
                                    alpha = float(w[n + knew])
                                    dd = float(zero)
                                    ds = float(zero)
                                    ss = float(zero)
                                    xoptsq = float(zero)
                                    i = int(1); _end29 = int(n); _step29 = int(1)
                                    _pc = 30
                                    continue
                                else:
                                    # bigden: basic block 30
                                    if (i > _end29 if _step29 > 0 else i < _end29):
                                        _pc = 38
                                        continue
                                    _pc = 31
                                    continue
                        else:
                            if _pc < 39:
                                if _pc < 38:
                                    # bigden: basic block 31
                                    dd = float(dd + d[i] * d[i])
                                    s[i] = xpt[knew, i] - xopt[i]
                                    ds = float(ds + d[i] * s[i])
                                    ss = float(ss + s[i] * s[i])
                                    xoptsq = float(xoptsq + xopt[i] * xopt[i])
                                    i += _step29
                                    _pc = 30
                                    continue
                                else:
                                    # bigden: basic block 38
                                    if not (not ds * ds <= 0.99 * dd * ss):
                                        _pc = 65
                                        continue
                                    _pc = 39
                                    continue
                            else:
                                if _pc < 42:
                                    # bigden: basic block 39
                                    ksav = int(knew)
                                    dtest = float(_div(ds * ds, ss))
                                    k = int(1); _end41 = int(npt); _step41 = int(1)
                                    _pc = 42
                                    continue
                                else:
                                    if _pc < 43:
                                        # bigden: basic block 42
                                        if (k > _end41 if _step41 > 0 else k < _end41):
                                            _pc = 60
                                            continue
                                        _pc = 43
                                        continue
                                    else:
                                        # bigden: basic block 43
                                        if not (k != kopt):
                                            _pc = 58
                                            continue
                                        _pc = 44
                                        continue
                else:
                    if _pc < 65:
                        if _pc < 54:
                            if _pc < 48:
                                if _pc < 47:
                                    # bigden: basic block 44
                                    dstemp = float(zero)
                                    sstemp = float(zero)
                                    i = int(1); _end46 = int(n); _step46 = int(1)
                                    _pc = 47
                                    continue
                                else:
                                    # bigden: basic block 47
                                    if (i > _end46 if _step46 > 0 else i < _end46):
                                        _pc = 53
                                        continue
                                    _pc = 48
                                    continue
                            else:
                                if _pc < 53:
                                    # bigden: basic block 48
                                    diff = float(xpt[k, i] - xopt[i])
                                    dstemp = float(dstemp + d[i] * diff)
                                    sstemp = float(sstemp + diff * diff)
                                    i += _step46
                                    _pc = 47
                                    continue
                                else:
                                    # bigden: basic block 53
                                    if not (not _div(dstemp * dstemp, sstemp) >= dtest):
                                        _pc = 58
                                        continue
                                    _pc = 54
                                    continue
                        else:
                            if _pc < 60:
                                if _pc < 58:
                                    # bigden: basic block 54
                                    ksav = int(k)
                                    dtest = float(_div(dstemp * dstemp, sstemp))
                                    ds = float(dstemp)
                                    ss = float(sstemp)
                                    _pc = 58
                                    continue
                                else:
                                    # bigden: basic block 58
                                    k += _step41
                                    _pc = 42
                                    continue
                            else:
                                if _pc < 61:
                                    # bigden: basic block 60
                                    i = int(1); _end60 = int(n); _step60 = int(1)
                                    _pc = 61
                                    continue
                                else:
                                    if _pc < 62:
                                        # bigden: basic block 61
                                        if (i > _end60 if _step60 > 0 else i < _end60):
                                            _pc = 65
                                            continue
                                        _pc = 62
                                        continue
                                    else:
                                        # bigden: basic block 62
                                        s[i] = xpt[ksav, i] - xopt[i]
                                        i += _step60
                                        _pc = 61
                                        continue
                    else:
                        if _pc < 87:
                            if _pc < 73:
                                if _pc < 68:
                                    # bigden: basic block 65
                                    ssden = float(dd * ss - ds * ds)
                                    iterc = int(0)
                                    densav = float(zero)
                                    _pc = 68
                                    continue
                                else:
                                    # bigden: basic block 68
                                    iterc = int(iterc + 1)
                                    temp = float(_div(one, _sqrt(ssden)))
                                    xoptd = float(zero)
                                    xopts = float(zero)
                                    i = int(1); _end72 = int(n); _step72 = int(1)
                                    _pc = 73
                                    continue
                            else:
                                if _pc < 74:
                                    # bigden: basic block 73
                                    if (i > _end72 if _step72 > 0 else i < _end72):
                                        _pc = 79
                                        continue
                                    _pc = 74
                                    continue
                                else:
                                    if _pc < 79:
                                        # bigden: basic block 74
                                        s[i] = temp * (dd * s[i] - ds * d[i])
                                        xoptd = float(xoptd + xopt[i] * d[i])
                                        xopts = float(xopts + xopt[i] * s[i])
                                        i += _step72
                                        _pc = 73
                                        continue
                                    else:
                                        # bigden: basic block 79
                                        tempa = float(half * xoptd * xoptd)
                                        tempb = float(half * xopts * xopts)
                                        den[1] = dd * (xoptsq + half * dd) + tempa + tempb
                                        den[2] = two * xoptd * dd
                                        den[3] = two * xopts * dd
                                        den[4] = tempa - tempb
                                        den[5] = xoptd * xopts
                                        i = int(6); _end86 = int(9); _step86 = int(1)
                                        _pc = 87
                                        continue
                        else:
                            if _pc < 91:
                                if _pc < 88:
                                    # bigden: basic block 87
                                    if (i > _end86 if _step86 > 0 else i < _end86):
                                        _pc = 91
                                        continue
                                    _pc = 88
                                    continue
                                else:
                                    # bigden: basic block 88
                                    den[i] = zero
                                    i += _step86
                                    _pc = 87
                                    continue
                            else:
                                if _pc < 92:
                                    # bigden: basic block 91
                                    k = int(1); _end91 = int(npt); _step91 = int(1)
                                    _pc = 92
                                    continue
                                else:
                                    if _pc < 93:
                                        # bigden: basic block 92
                                        if (k > _end91 if _step91 > 0 else k < _end91):
                                            _pc = 110
                                            continue
                                        _pc = 93
                                        continue
                                    else:
                                        # bigden: basic block 93
                                        tempa = float(zero)
                                        tempb = float(zero)
                                        tempc = float(zero)
                                        i = int(1); _end96 = int(n); _step96 = int(1)
                                        _pc = 97
                                        continue
            else:
                if _pc < 138:
                    if _pc < 124:
                        if _pc < 111:
                            if _pc < 103:
                                if _pc < 98:
                                    # bigden: basic block 97
                                    if (i > _end96 if _step96 > 0 else i < _end96):
                                        _pc = 103
                                        continue
                                    _pc = 98
                                    continue
                                else:
                                    # bigden: basic block 98
                                    tempa = float(tempa + xpt[k, i] * d[i])
                                    tempb = float(tempb + xpt[k, i] * s[i])
                                    tempc = float(tempc + xpt[k, i] * xopt[i])
                                    i += _step96
                                    _pc = 97
                                    continue
                            else:
                                if _pc < 110:
                                    # bigden: basic block 103
                                    wvec[k, 1] = quart * (tempa * tempa + tempb * tempb)
                                    wvec[k, 2] = tempa * tempc
                                    wvec[k, 3] = tempb * tempc
                                    wvec[k, 4] = quart * (tempa * tempa - tempb * tempb)
                                    wvec[k, 5] = half * tempa * tempb
                                    k += _step91
                                    _pc = 92
                                    continue
                                else:
                                    # bigden: basic block 110
                                    i = int(1); _end110 = int(n); _step110 = int(1)
                                    _pc = 111
                                    continue
                        else:
                            if _pc < 120:
                                if _pc < 112:
                                    # bigden: basic block 111
                                    if (i > _end110 if _step110 > 0 else i < _end110):
                                        _pc = 120
                                        continue
                                    _pc = 112
                                    continue
                                else:
                                    # bigden: basic block 112
                                    ip = int(i + npt)
                                    wvec[ip, 1] = zero
                                    wvec[ip, 2] = d[i]
                                    wvec[ip, 3] = s[i]
                                    wvec[ip, 4] = zero
                                    wvec[ip, 5] = zero
                                    i += _step110
                                    _pc = 111
                                    continue
                            else:
                                if _pc < 121:
                                    # bigden: basic block 120
                                    jc = int(1); _end120 = int(5); _step120 = int(1)
                                    _pc = 121
                                    continue
                                else:
                                    if _pc < 122:
                                        # bigden: basic block 121
                                        if (jc > _end120 if _step120 > 0 else jc < _end120):
                                            _pc = 172
                                            continue
                                        _pc = 122
                                        continue
                                    else:
                                        # bigden: basic block 122
                                        nw = int(npt)
                                        if not (jc == 2 or jc == 3):
                                            _pc = 125
                                            continue
                                        _pc = 124
                                        continue
                    else:
                        if _pc < 130:
                            if _pc < 126:
                                if _pc < 125:
                                    # bigden: basic block 124
                                    nw = int(ndim)
                                    _pc = 125
                                    continue
                                else:
                                    # bigden: basic block 125
                                    k = int(1); _end125 = int(npt); _step125 = int(1)
                                    _pc = 126
                                    continue
                            else:
                                if _pc < 127:
                                    # bigden: basic block 126
                                    if (k > _end125 if _step125 > 0 else k < _end125):
                                        _pc = 130
                                        continue
                                    _pc = 127
                                    continue
                                else:
                                    # bigden: basic block 127
                                    prod[k, jc] = zero
                                    k += _step125
                                    _pc = 126
                                    continue
                        else:
                            if _pc < 132:
                                if _pc < 131:
                                    # bigden: basic block 130
                                    j = int(1); _end130 = int(nptm); _step130 = int(1)
                                    _pc = 131
                                    continue
                                else:
                                    # bigden: basic block 131
                                    if (j > _end130 if _step130 > 0 else j < _end130):
                                        _pc = 147
                                        continue
                                    _pc = 132
                                    continue
                            else:
                                if _pc < 134:
                                    # bigden: basic block 132
                                    sum = float(zero)
                                    k = int(1); _end133 = int(npt); _step133 = int(1)
                                    _pc = 134
                                    continue
                                else:
                                    if _pc < 135:
                                        # bigden: basic block 134
                                        if (k > _end133 if _step133 > 0 else k < _end133):
                                            _pc = 138
                                            continue
                                        _pc = 135
                                        continue
                                    else:
                                        # bigden: basic block 135
                                        sum = float(sum + zmat[k, j] * wvec[k, jc])
                                        k += _step133
                                        _pc = 134
                                        continue
                else:
                    if _pc < 150:
                        if _pc < 142:
                            if _pc < 140:
                                if _pc < 139:
                                    # bigden: basic block 138
                                    if not (j < idz):
                                        _pc = 140
                                        continue
                                    _pc = 139
                                    continue
                                else:
                                    # bigden: basic block 139
                                    sum = float(-sum)
                                    _pc = 140
                                    continue
                            else:
                                if _pc < 141:
                                    # bigden: basic block 140
                                    k = int(1); _end140 = int(npt); _step140 = int(1)
                                    _pc = 141
                                    continue
                                else:
                                    # bigden: basic block 141
                                    if (k > _end140 if _step140 > 0 else k < _end140):
                                        _pc = 145
                                        continue
                                    _pc = 142
                                    continue
                        else:
                            if _pc < 147:
                                if _pc < 145:
                                    # bigden: basic block 142
                                    prod[k, jc] = prod[k, jc] + sum * zmat[k, j]
                                    k += _step140
                                    _pc = 141
                                    continue
                                else:
                                    # bigden: basic block 145
                                    j += _step130
                                    _pc = 131
                                    continue
                            else:
                                if _pc < 148:
                                    # bigden: basic block 147
                                    if not (nw == ndim):
                                        _pc = 159
                                        continue
                                    _pc = 148
                                    continue
                                else:
                                    if _pc < 149:
                                        # bigden: basic block 148
                                        k = int(1); _end148 = int(npt); _step148 = int(1)
                                        _pc = 149
                                        continue
                                    else:
                                        # bigden: basic block 149
                                        if (k > _end148 if _step148 > 0 else k < _end148):
                                            _pc = 159
                                            continue
                                        _pc = 150
                                        continue
                    else:
                        if _pc < 160:
                            if _pc < 153:
                                if _pc < 152:
                                    # bigden: basic block 150
                                    sum = float(zero)
                                    j = int(1); _end151 = int(n); _step151 = int(1)
                                    _pc = 152
                                    continue
                                else:
                                    # bigden: basic block 152
                                    if (j > _end151 if _step151 > 0 else j < _end151):
                                        _pc = 156
                                        continue
                                    _pc = 153
                                    continue
                            else:
                                if _pc < 156:
                                    # bigden: basic block 153
                                    sum = float(sum + bmat[k, j] * wvec[npt + j, jc])
                                    j += _step151
                                    _pc = 152
                                    continue
                                else:
                                    if _pc < 159:
                                        # bigden: basic block 156
                                        prod[k, jc] = prod[k, jc] + sum
                                        k += _step148
                                        _pc = 149
                                        continue
                                    else:
                                        # bigden: basic block 159
                                        j = int(1); _end159 = int(n); _step159 = int(1)
                                        _pc = 160
                                        continue
                        else:
                            if _pc < 163:
                                if _pc < 161:
                                    # bigden: basic block 160
                                    if (j > _end159 if _step159 > 0 else j < _end159):
                                        _pc = 170
                                        continue
                                    _pc = 161
                                    continue
                                else:
                                    # bigden: basic block 161
                                    sum = float(zero)
                                    i = int(1); _end162 = int(nw); _step162 = int(1)
                                    _pc = 163
                                    continue
                            else:
                                if _pc < 164:
                                    # bigden: basic block 163
                                    if (i > _end162 if _step162 > 0 else i < _end162):
                                        _pc = 167
                                        continue
                                    _pc = 164
                                    continue
                                else:
                                    if _pc < 167:
                                        # bigden: basic block 164
                                        sum = float(sum + bmat[i, j] * wvec[i, jc])
                                        i += _step162
                                        _pc = 163
                                        continue
                                    else:
                                        # bigden: basic block 167
                                        prod[npt + j, jc] = sum
                                        j += _step159
                                        _pc = 160
                                        continue
        else:
            if _pc < 288:
                if _pc < 251:
                    if _pc < 205:
                        if _pc < 176:
                            if _pc < 173:
                                if _pc < 172:
                                    # bigden: basic block 170
                                    jc += _step120
                                    _pc = 121
                                    continue
                                else:
                                    # bigden: basic block 172
                                    k = int(1); _end172 = int(ndim); _step172 = int(1)
                                    _pc = 173
                                    continue
                            else:
                                if _pc < 174:
                                    # bigden: basic block 173
                                    if (k > _end172 if _step172 > 0 else k < _end172):
                                        _pc = 202
                                        continue
                                    _pc = 174
                                    continue
                                else:
                                    # bigden: basic block 174
                                    sum = float(zero)
                                    i = int(1); _end175 = int(5); _step175 = int(1)
                                    _pc = 176
                                    continue
                        else:
                            if _pc < 181:
                                if _pc < 177:
                                    # bigden: basic block 176
                                    if (i > _end175 if _step175 > 0 else i < _end175):
                                        _pc = 181
                                        continue
                                    _pc = 177
                                    continue
                                else:
                                    # bigden: basic block 177
                                    par[i] = half * prod[k, i] * wvec[k, i]
                                    sum = float(sum + par[i])
                                    i += _step175
                                    _pc = 176
                                    continue
                            else:
                                if _pc < 202:
                                    # bigden: basic block 181
                                    den[1] = den[1] - par[1] - sum
                                    tempa = float(prod[k, 1] * wvec[k, 2] + prod[k, 2] * wvec[k, 1])
                                    tempb = float(prod[k, 2] * wvec[k, 4] + prod[k, 4] * wvec[k, 2])
                                    tempc = float(prod[k, 3] * wvec[k, 5] + prod[k, 5] * wvec[k, 3])
                                    den[2] = den[2] - tempa - half * (tempb + tempc)
                                    den[6] = den[6] - half * (tempb - tempc)
                                    tempa = float(prod[k, 1] * wvec[k, 3] + prod[k, 3] * wvec[k, 1])
                                    tempb = float(prod[k, 2] * wvec[k, 5] + prod[k, 5] * wvec[k, 2])
                                    tempc = float(prod[k, 3] * wvec[k, 4] + prod[k, 4] * wvec[k, 3])
                                    den[3] = den[3] - tempa - half * (tempb - tempc)
                                    den[7] = den[7] - half * (tempb + tempc)
                                    tempa = float(prod[k, 1] * wvec[k, 4] + prod[k, 4] * wvec[k, 1])
                                    den[4] = den[4] - tempa - par[2] + par[3]
                                    tempa = float(prod[k, 1] * wvec[k, 5] + prod[k, 5] * wvec[k, 1])
                                    tempb = float(prod[k, 2] * wvec[k, 3] + prod[k, 3] * wvec[k, 2])
                                    den[5] = den[5] - tempa - half * tempb
                                    den[8] = den[8] - par[4] + par[5]
                                    tempa = float(prod[k, 4] * wvec[k, 5] + prod[k, 5] * wvec[k, 4])
                                    den[9] = den[9] - half * tempa
                                    k += _step172
                                    _pc = 173
                                    continue
                                else:
                                    if _pc < 204:
                                        # bigden: basic block 202
                                        sum = float(zero)
                                        i = int(1); _end203 = int(5); _step203 = int(1)
                                        _pc = 204
                                        continue
                                    else:
                                        # bigden: basic block 204
                                        if (i > _end203 if _step203 > 0 else i < _end203):
                                            _pc = 209
                                            continue
                                        _pc = 205
                                        continue
                    else:
                        if _pc < 239:
                            if _pc < 234:
                                if _pc < 209:
                                    # bigden: basic block 205
                                    par[i] = half * (prod[knew, i] * prod[knew, i])
                                    sum = float(sum + par[i])
                                    i += _step203
                                    _pc = 204
                                    continue
                                else:
                                    # bigden: basic block 209
                                    denex[1] = alpha * den[1] + par[1] + sum
                                    tempa = float(two * prod[knew, 1] * prod[knew, 2])
                                    tempb = float(prod[knew, 2] * prod[knew, 4])
                                    tempc = float(prod[knew, 3] * prod[knew, 5])
                                    denex[2] = alpha * den[2] + tempa + tempb + tempc
                                    denex[6] = alpha * den[6] + tempb - tempc
                                    tempa = float(two * prod[knew, 1] * prod[knew, 3])
                                    tempb = float(prod[knew, 2] * prod[knew, 5])
                                    tempc = float(prod[knew, 3] * prod[knew, 4])
                                    denex[3] = alpha * den[3] + tempa + tempb - tempc
                                    denex[7] = alpha * den[7] + tempb + tempc
                                    tempa = float(two * prod[knew, 1] * prod[knew, 4])
                                    denex[4] = alpha * den[4] + tempa + par[2] - par[3]
                                    tempa = float(two * prod[knew, 1] * prod[knew, 5])
                                    denex[5] = alpha * den[5] + tempa + prod[knew, 2] * prod[knew, 3]
                                    denex[8] = alpha * den[8] + par[4] - par[5]
                                    denex[9] = alpha * den[9] + prod[knew, 4] * prod[knew, 5]
                                    sum = float(denex[1] + denex[2] + denex[4] + denex[6] + denex[8])
                                    denold = float(sum)
                                    denmax = float(sum)
                                    isave = int(0)
                                    iu = int(49)
                                    temp = float(_div(twopi, float(iu + 1)))
                                    par[1] = one
                                    i = int(1); _end233 = int(iu); _step233 = int(1)
                                    _pc = 234
                                    continue
                            else:
                                if _pc < 235:
                                    # bigden: basic block 234
                                    if (i > _end233 if _step233 > 0 else i < _end233):
                                        _pc = 260
                                        continue
                                    _pc = 235
                                    continue
                                else:
                                    # bigden: basic block 235
                                    angle = float(float(i) * temp)
                                    par[2] = _cos(angle)
                                    par[3] = _sin(angle)
                                    j = int(4); _end238 = int(8); _step238 = int(2)
                                    _pc = 239
                                    continue
                        else:
                            if _pc < 244:
                                if _pc < 240:
                                    # bigden: basic block 239
                                    if (j > _end238 if _step238 > 0 else j < _end238):
                                        _pc = 244
                                        continue
                                    _pc = 240
                                    continue
                                else:
                                    # bigden: basic block 240
                                    par[j] = par[2] * par[j - 2] - par[3] * par[j - 1]
                                    par[j + 1] = par[2] * par[j - 1] + par[3] * par[j - 2]
                                    j += _step238
                                    _pc = 239
                                    continue
                            else:
                                if _pc < 247:
                                    # bigden: basic block 244
                                    sumold = float(sum)
                                    sum = float(zero)
                                    j = int(1); _end246 = int(9); _step246 = int(1)
                                    _pc = 247
                                    continue
                                else:
                                    if _pc < 248:
                                        # bigden: basic block 247
                                        if (j > _end246 if _step246 > 0 else j < _end246):
                                            _pc = 251
                                            continue
                                        _pc = 248
                                        continue
                                    else:
                                        # bigden: basic block 248
                                        sum = float(sum + denex[j] * par[j])
                                        j += _step246
                                        _pc = 247
                                        continue
                else:
                    if _pc < 264:
                        if _pc < 258:
                            if _pc < 256:
                                if _pc < 252:
                                    # bigden: basic block 251
                                    if not (abs(sum) > abs(denmax)):
                                        _pc = 256
                                        continue
                                    _pc = 252
                                    continue
                                else:
                                    # bigden: basic block 252
                                    denmax = float(sum)
                                    isave = int(i)
                                    tempa = float(sumold)
                                    _pc = 258
                                    continue
                            else:
                                if _pc < 257:
                                    # bigden: basic block 256
                                    if not (i == isave + 1):
                                        _pc = 258
                                        continue
                                    _pc = 257
                                    continue
                                else:
                                    # bigden: basic block 257
                                    tempb = float(sum)
                                    _pc = 258
                                    continue
                        else:
                            if _pc < 261:
                                if _pc < 260:
                                    # bigden: basic block 258
                                    i += _step233
                                    _pc = 234
                                    continue
                                else:
                                    # bigden: basic block 260
                                    if not (isave == 0):
                                        _pc = 262
                                        continue
                                    _pc = 261
                                    continue
                            else:
                                if _pc < 262:
                                    # bigden: basic block 261
                                    tempa = float(sum)
                                    _pc = 262
                                    continue
                                else:
                                    if _pc < 263:
                                        # bigden: basic block 262
                                        if not (isave == iu):
                                            _pc = 264
                                            continue
                                        _pc = 263
                                        continue
                                    else:
                                        # bigden: basic block 263
                                        tempb = float(denold)
                                        _pc = 264
                                        continue
                    else:
                        if _pc < 278:
                            if _pc < 269:
                                if _pc < 266:
                                    # bigden: basic block 264
                                    step = float(zero)
                                    if not (tempa != tempb):
                                        _pc = 269
                                        continue
                                    _pc = 266
                                    continue
                                else:
                                    # bigden: basic block 266
                                    tempa = float(tempa - denmax)
                                    tempb = float(tempb - denmax)
                                    step = float(_div(half * (tempa - tempb), tempa + tempb))
                                    _pc = 269
                                    continue
                            else:
                                if _pc < 273:
                                    # bigden: basic block 269
                                    angle = float(temp * (float(isave) + step))
                                    par[2] = _cos(angle)
                                    par[3] = _sin(angle)
                                    j = int(4); _end272 = int(8); _step272 = int(2)
                                    _pc = 273
                                    continue
                                else:
                                    if _pc < 274:
                                        # bigden: basic block 273
                                        if (j > _end272 if _step272 > 0 else j < _end272):
                                            _pc = 278
                                            continue
                                        _pc = 274
                                        continue
                                    else:
                                        # bigden: basic block 274
                                        par[j] = par[2] * par[j - 2] - par[3] * par[j - 1]
                                        par[j + 1] = par[2] * par[j - 1] + par[3] * par[j - 2]
                                        j += _step272
                                        _pc = 273
                                        continue
                        else:
                            if _pc < 282:
                                if _pc < 281:
                                    # bigden: basic block 278
                                    beta = float(zero)
                                    denmax = float(zero)
                                    j = int(1); _end280 = int(9); _step280 = int(1)
                                    _pc = 281
                                    continue
                                else:
                                    # bigden: basic block 281
                                    if (j > _end280 if _step280 > 0 else j < _end280):
                                        _pc = 286
                                        continue
                                    _pc = 282
                                    continue
                            else:
                                if _pc < 286:
                                    # bigden: basic block 282
                                    beta = float(beta + den[j] * par[j])
                                    denmax = float(denmax + denex[j] * par[j])
                                    j += _step280
                                    _pc = 281
                                    continue
                                else:
                                    if _pc < 287:
                                        # bigden: basic block 286
                                        k = int(1); _end286 = int(ndim); _step286 = int(1)
                                        _pc = 287
                                        continue
                                    else:
                                        # bigden: basic block 287
                                        if (k > _end286 if _step286 > 0 else k < _end286):
                                            _pc = 296
                                            continue
                                        _pc = 288
                                        continue
            else:
                if _pc < 324:
                    if _pc < 311:
                        if _pc < 296:
                            if _pc < 291:
                                if _pc < 290:
                                    # bigden: basic block 288
                                    vlag[k] = zero
                                    j = int(1); _end289 = int(5); _step289 = int(1)
                                    _pc = 290
                                    continue
                                else:
                                    # bigden: basic block 290
                                    if (j > _end289 if _step289 > 0 else j < _end289):
                                        _pc = 294
                                        continue
                                    _pc = 291
                                    continue
                            else:
                                if _pc < 294:
                                    # bigden: basic block 291
                                    vlag[k] = vlag[k] + prod[k, j] * par[j]
                                    j += _step289
                                    _pc = 290
                                    continue
                                else:
                                    # bigden: basic block 294
                                    k += _step286
                                    _pc = 287
                                    continue
                        else:
                            if _pc < 302:
                                if _pc < 301:
                                    # bigden: basic block 296
                                    tau = float(vlag[knew])
                                    dd = float(zero)
                                    tempa = float(zero)
                                    tempb = float(zero)
                                    i = int(1); _end300 = int(n); _step300 = int(1)
                                    _pc = 301
                                    continue
                                else:
                                    # bigden: basic block 301
                                    if (i > _end300 if _step300 > 0 else i < _end300):
                                        _pc = 309
                                        continue
                                    _pc = 302
                                    continue
                            else:
                                if _pc < 309:
                                    # bigden: basic block 302
                                    d[i] = par[2] * d[i] + par[3] * s[i]
                                    w[i] = xopt[i] + d[i]
                                    dd = float(dd + d[i] * d[i])
                                    tempa = float(tempa + d[i] * w[i])
                                    tempb = float(tempb + w[i] * w[i])
                                    i += _step300
                                    _pc = 301
                                    continue
                                else:
                                    if _pc < 310:
                                        # bigden: basic block 309
                                        if not (iterc >= n):
                                            _pc = 311
                                            continue
                                        _pc = 310
                                        continue
                                    else:
                                        # bigden: basic block 310
                                        _pc = 349
                                        continue
                    else:
                        if _pc < 315:
                            if _pc < 313:
                                if _pc < 312:
                                    # bigden: basic block 311
                                    if not (iterc > 1):
                                        _pc = 313
                                        continue
                                    _pc = 312
                                    continue
                                else:
                                    # bigden: basic block 312
                                    densav = float(_max(densav, denold))
                                    _pc = 313
                                    continue
                            else:
                                if _pc < 314:
                                    # bigden: basic block 313
                                    if not (abs(denmax) <= 1.1 * abs(densav)):
                                        _pc = 315
                                        continue
                                    _pc = 314
                                    continue
                                else:
                                    # bigden: basic block 314
                                    _pc = 349
                                    continue
                        else:
                            if _pc < 318:
                                if _pc < 317:
                                    # bigden: basic block 315
                                    densav = float(denmax)
                                    i = int(1); _end316 = int(n); _step316 = int(1)
                                    _pc = 317
                                    continue
                                else:
                                    # bigden: basic block 317
                                    if (i > _end316 if _step316 > 0 else i < _end316):
                                        _pc = 322
                                        continue
                                    _pc = 318
                                    continue
                            else:
                                if _pc < 322:
                                    # bigden: basic block 318
                                    temp = float(tempa * xopt[i] + tempb * d[i] - vlag[npt + i])
                                    s[i] = tau * bmat[knew, i] + alpha * temp
                                    i += _step316
                                    _pc = 317
                                    continue
                                else:
                                    if _pc < 323:
                                        # bigden: basic block 322
                                        k = int(1); _end322 = int(npt); _step322 = int(1)
                                        _pc = 323
                                        continue
                                    else:
                                        # bigden: basic block 323
                                        if (k > _end322 if _step322 > 0 else k < _end322):
                                            _pc = 338
                                            continue
                                        _pc = 324
                                        continue
                else:
                    if _pc < 342:
                        if _pc < 332:
                            if _pc < 327:
                                if _pc < 326:
                                    # bigden: basic block 324
                                    sum = float(zero)
                                    j = int(1); _end325 = int(n); _step325 = int(1)
                                    _pc = 326
                                    continue
                                else:
                                    # bigden: basic block 326
                                    if (j > _end325 if _step325 > 0 else j < _end325):
                                        _pc = 330
                                        continue
                                    _pc = 327
                                    continue
                            else:
                                if _pc < 330:
                                    # bigden: basic block 327
                                    sum = float(sum + xpt[k, j] * w[j])
                                    j += _step325
                                    _pc = 326
                                    continue
                                else:
                                    # bigden: basic block 330
                                    temp = float((tau * w[n + k] - alpha * vlag[k]) * sum)
                                    i = int(1); _end331 = int(n); _step331 = int(1)
                                    _pc = 332
                                    continue
                        else:
                            if _pc < 336:
                                if _pc < 333:
                                    # bigden: basic block 332
                                    if (i > _end331 if _step331 > 0 else i < _end331):
                                        _pc = 336
                                        continue
                                    _pc = 333
                                    continue
                                else:
                                    # bigden: basic block 333
                                    s[i] = s[i] + temp * xpt[k, i]
                                    i += _step331
                                    _pc = 332
                                    continue
                            else:
                                if _pc < 338:
                                    # bigden: basic block 336
                                    k += _step322
                                    _pc = 323
                                    continue
                                else:
                                    if _pc < 341:
                                        # bigden: basic block 338
                                        ss = float(zero)
                                        ds = float(zero)
                                        i = int(1); _end340 = int(n); _step340 = int(1)
                                        _pc = 341
                                        continue
                                    else:
                                        # bigden: basic block 341
                                        if (i > _end340 if _step340 > 0 else i < _end340):
                                            _pc = 346
                                            continue
                                        _pc = 342
                                        continue
                    else:
                        if _pc < 351:
                            if _pc < 348:
                                if _pc < 346:
                                    # bigden: basic block 342
                                    ss = float(ss + s[i] * s[i])
                                    ds = float(ds + d[i] * s[i])
                                    i += _step340
                                    _pc = 341
                                    continue
                                else:
                                    # bigden: basic block 346
                                    ssden = float(dd * ss - ds * ds)
                                    if not (ssden >= 1e-08 * dd * ss):
                                        _pc = 349
                                        continue
                                    _pc = 348
                                    continue
                            else:
                                if _pc < 349:
                                    # bigden: basic block 348
                                    _pc = 68
                                    continue
                                else:
                                    if _pc < 350:
                                        # bigden: basic block 349
                                        k = int(1); _end349 = int(ndim); _step349 = int(1)
                                        _pc = 350
                                        continue
                                    else:
                                        # bigden: basic block 350
                                        if (k > _end349 if _step349 > 0 else k < _end349):
                                            _pc = 359
                                            continue
                                        _pc = 351
                                        continue
                        else:
                            if _pc < 354:
                                if _pc < 353:
                                    # bigden: basic block 351
                                    w[k] = zero
                                    j = int(1); _end352 = int(5); _step352 = int(1)
                                    _pc = 353
                                    continue
                                else:
                                    # bigden: basic block 353
                                    if (j > _end352 if _step352 > 0 else j < _end352):
                                        _pc = 357
                                        continue
                                    _pc = 354
                                    continue
                            else:
                                if _pc < 357:
                                    # bigden: basic block 354
                                    w[k] = w[k] + wvec[k, j] * par[j]
                                    j += _step352
                                    _pc = 353
                                    continue
                                else:
                                    if _pc < 359:
                                        # bigden: basic block 357
                                        k += _step349
                                        _pc = 350
                                        continue
                                    else:
                                        # bigden: basic block 359
                                        vlag[kopt] = vlag[kopt] + one
                                        return n, npt, idz, ndim, kopt, knew, beta

def _update(_ctx, n, npt, bmat, zmat, idz, ndim, vlag, beta, knew, w):
    alpha = 0.0
    dabs = 0.0
    denom = 0.0
    dsqrt = 0.0
    i = 0
    iflag = 0
    j = 0
    ja = 0
    jb = 0
    jl = 0
    jp = 0
    nptm = 0
    one = 0.0
    scala = 0.0
    scalb = 0.0
    tau = 0.0
    tausq = 0.0
    temp = 0.0
    tempa = 0.0
    tempb = 0.0
    zero = 0.0
    bmat = bmat.with_leading(ndim)
    zmat = zmat.with_leading(npt)
    _pc = 0
    while True:
        if _pc < 52:
            if _pc < 26:
                if _pc < 14:
                    if _pc < 7:
                        if _pc < 5:
                            # update: basic block 0
                            one = float(1.0)
                            zero = float(0.0)
                            nptm = int(npt - n - 1)
                            jl = int(1)
                            j = int(2); _end4 = int(nptm); _step4 = int(1)
                            _pc = 5
                            continue
                        else:
                            if _pc < 6:
                                # update: basic block 5
                                if (j > _end4 if _step4 > 0 else j < _end4):
                                    _pc = 23
                                    continue
                                _pc = 6
                                continue
                            else:
                                # update: basic block 6
                                if not (j == idz):
                                    _pc = 9
                                    continue
                                _pc = 7
                                continue
                    else:
                        if _pc < 9:
                            # update: basic block 7
                            jl = int(idz)
                            _pc = 21
                            continue
                        else:
                            if _pc < 10:
                                # update: basic block 9
                                if not (zmat[knew, j] != zero):
                                    _pc = 21
                                    continue
                                _pc = 10
                                continue
                            else:
                                # update: basic block 10
                                temp = float(_sqrt(zmat[knew, jl] * zmat[knew, jl] + zmat[knew, j] * zmat[knew, j]))
                                tempa = float(_div(zmat[knew, jl], temp))
                                tempb = float(_div(zmat[knew, j], temp))
                                i = int(1); _end13 = int(npt); _step13 = int(1)
                                _pc = 14
                                continue
                else:
                    if _pc < 21:
                        if _pc < 15:
                            # update: basic block 14
                            if (i > _end13 if _step13 > 0 else i < _end13):
                                _pc = 20
                                continue
                            _pc = 15
                            continue
                        else:
                            if _pc < 20:
                                # update: basic block 15
                                temp = float(tempa * zmat[i, jl] + tempb * zmat[i, j])
                                zmat[i, j] = tempa * zmat[i, j] - tempb * zmat[i, jl]
                                zmat[i, jl] = temp
                                i += _step13
                                _pc = 14
                                continue
                            else:
                                # update: basic block 20
                                zmat[knew, j] = zero
                                _pc = 21
                                continue
                    else:
                        if _pc < 23:
                            # update: basic block 21
                            j += _step4
                            _pc = 5
                            continue
                        else:
                            if _pc < 25:
                                # update: basic block 23
                                tempa = float(zmat[knew, 1])
                                if not (idz >= 2):
                                    _pc = 26
                                    continue
                                _pc = 25
                                continue
                            else:
                                # update: basic block 25
                                tempa = float(-tempa)
                                _pc = 26
                                continue
            else:
                if _pc < 33:
                    if _pc < 29:
                        if _pc < 27:
                            # update: basic block 26
                            if not (jl > 1):
                                _pc = 28
                                continue
                            _pc = 27
                            continue
                        else:
                            if _pc < 28:
                                # update: basic block 27
                                tempb = float(zmat[knew, jl])
                                _pc = 28
                                continue
                            else:
                                # update: basic block 28
                                i = int(1); _end28 = int(npt); _step28 = int(1)
                                _pc = 29
                                continue
                    else:
                        if _pc < 30:
                            # update: basic block 29
                            if (i > _end28 if _step28 > 0 else i < _end28):
                                _pc = 35
                                continue
                            _pc = 30
                            continue
                        else:
                            if _pc < 32:
                                # update: basic block 30
                                w[i] = tempa * zmat[i, 1]
                                if not (jl > 1):
                                    _pc = 33
                                    continue
                                _pc = 32
                                continue
                            else:
                                # update: basic block 32
                                w[i] = w[i] + tempb * zmat[i, jl]
                                _pc = 33
                                continue
                else:
                    if _pc < 46:
                        if _pc < 35:
                            # update: basic block 33
                            i += _step28
                            _pc = 29
                            continue
                        else:
                            if _pc < 42:
                                # update: basic block 35
                                alpha = float(w[knew])
                                tau = float(vlag[knew])
                                tausq = float(tau * tau)
                                denom = float(alpha * beta + tausq)
                                vlag[knew] = vlag[knew] - one
                                iflag = int(0)
                                if not (jl == 1):
                                    _pc = 55
                                    continue
                                _pc = 42
                                continue
                            else:
                                # update: basic block 42
                                temp = float(_sqrt(abs(denom)))
                                tempb = float(_div(tempa, temp))
                                tempa = float(_div(tau, temp))
                                i = int(1); _end45 = int(npt); _step45 = int(1)
                                _pc = 46
                                continue
                    else:
                        if _pc < 50:
                            if _pc < 47:
                                # update: basic block 46
                                if (i > _end45 if _step45 > 0 else i < _end45):
                                    _pc = 50
                                    continue
                                _pc = 47
                                continue
                            else:
                                # update: basic block 47
                                zmat[i, 1] = tempa * zmat[i, 1] - tempb * vlag[i]
                                i += _step45
                                _pc = 46
                                continue
                        else:
                            if _pc < 51:
                                # update: basic block 50
                                if not (idz == 1 and temp < zero):
                                    _pc = 52
                                    continue
                                _pc = 51
                                continue
                            else:
                                # update: basic block 51
                                idz = int(2)
                                _pc = 52
                                continue
        else:
            if _pc < 76:
                if _pc < 66:
                    if _pc < 55:
                        if _pc < 53:
                            # update: basic block 52
                            if not (idz >= 2 and temp >= zero):
                                _pc = 54
                                continue
                            _pc = 53
                            continue
                        else:
                            if _pc < 54:
                                # update: basic block 53
                                iflag = int(1)
                                _pc = 54
                                continue
                            else:
                                # update: basic block 54
                                _pc = 76
                                continue
                    else:
                        if _pc < 57:
                            # update: basic block 55
                            ja = int(1)
                            if not (beta >= zero):
                                _pc = 58
                                continue
                            _pc = 57
                            continue
                        else:
                            if _pc < 58:
                                # update: basic block 57
                                ja = int(jl)
                                _pc = 58
                                continue
                            else:
                                # update: basic block 58
                                jb = int(jl + 1 - ja)
                                temp = float(_div(zmat[knew, jb], denom))
                                tempa = float(temp * beta)
                                tempb = float(temp * tau)
                                temp = float(zmat[knew, ja])
                                scala = float(_div(one, _sqrt(abs(beta) * temp * temp + tausq)))
                                scalb = float(scala * _sqrt(abs(denom)))
                                i = int(1); _end65 = int(npt); _step65 = int(1)
                                _pc = 66
                                continue
                else:
                    if _pc < 72:
                        if _pc < 67:
                            # update: basic block 66
                            if (i > _end65 if _step65 > 0 else i < _end65):
                                _pc = 71
                                continue
                            _pc = 67
                            continue
                        else:
                            if _pc < 71:
                                # update: basic block 67
                                zmat[i, ja] = scala * (tau * zmat[i, ja] - temp * vlag[i])
                                zmat[i, jb] = scalb * (zmat[i, jb] - tempa * w[i] - tempb * vlag[i])
                                i += _step65
                                _pc = 66
                                continue
                            else:
                                # update: basic block 71
                                if not (denom <= zero):
                                    _pc = 76
                                    continue
                                _pc = 72
                                continue
                    else:
                        if _pc < 74:
                            if _pc < 73:
                                # update: basic block 72
                                if not (beta < zero):
                                    _pc = 74
                                    continue
                                _pc = 73
                                continue
                            else:
                                # update: basic block 73
                                idz = int(idz + 1)
                                _pc = 74
                                continue
                        else:
                            if _pc < 75:
                                # update: basic block 74
                                if not (beta >= zero):
                                    _pc = 76
                                    continue
                                _pc = 75
                                continue
                            else:
                                # update: basic block 75
                                iflag = int(1)
                                _pc = 76
                                continue
            else:
                if _pc < 87:
                    if _pc < 80:
                        if _pc < 77:
                            # update: basic block 76
                            if not (iflag == 1):
                                _pc = 85
                                continue
                            _pc = 77
                            continue
                        else:
                            if _pc < 79:
                                # update: basic block 77
                                idz = int(idz - 1)
                                i = int(1); _end78 = int(npt); _step78 = int(1)
                                _pc = 79
                                continue
                            else:
                                # update: basic block 79
                                if (i > _end78 if _step78 > 0 else i < _end78):
                                    _pc = 85
                                    continue
                                _pc = 80
                                continue
                    else:
                        if _pc < 85:
                            # update: basic block 80
                            temp = float(zmat[i, 1])
                            zmat[i, 1] = zmat[i, idz]
                            zmat[i, idz] = temp
                            i += _step78
                            _pc = 79
                            continue
                        else:
                            if _pc < 86:
                                # update: basic block 85
                                j = int(1); _end85 = int(n); _step85 = int(1)
                                _pc = 86
                                continue
                            else:
                                # update: basic block 86
                                if (j > _end85 if _step85 > 0 else j < _end85):
                                    _pc = 100
                                    continue
                                _pc = 87
                                continue
                else:
                    if _pc < 95:
                        if _pc < 92:
                            # update: basic block 87
                            jp = int(npt + j)
                            w[jp] = bmat[knew, j]
                            tempa = float(_div(alpha * vlag[jp] - tau * w[jp], denom))
                            tempb = float(_div(-beta * w[jp] - tau * vlag[jp], denom))
                            i = int(1); _end91 = int(jp); _step91 = int(1)
                            _pc = 92
                            continue
                        else:
                            if _pc < 93:
                                # update: basic block 92
                                if (i > _end91 if _step91 > 0 else i < _end91):
                                    _pc = 98
                                    continue
                                _pc = 93
                                continue
                            else:
                                # update: basic block 93
                                bmat[i, j] = bmat[i, j] + tempa * vlag[i] + tempb * w[i]
                                if not (i > npt):
                                    _pc = 96
                                    continue
                                _pc = 95
                                continue
                    else:
                        if _pc < 98:
                            if _pc < 96:
                                # update: basic block 95
                                bmat[jp, i - npt] = bmat[i, j]
                                _pc = 96
                                continue
                            else:
                                # update: basic block 96
                                i += _step91
                                _pc = 92
                                continue
                        else:
                            if _pc < 100:
                                # update: basic block 98
                                j += _step85
                                _pc = 86
                                continue
                            else:
                                # update: basic block 100
                                return n, npt, idz, ndim, beta, knew
