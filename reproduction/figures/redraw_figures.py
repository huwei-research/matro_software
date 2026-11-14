"""Redraw the eight main figures at their final article-page widths.

The saved samples, statistics, contour levels, selected states and view limits
are inherited without modification from v13.4. Only presentation is revised.
"""
from pathlib import Path
import gzip
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, NullLocator, LogLocator, NullFormatter, PercentFormatter, ScalarFormatter
from matplotlib import colors
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data/figure_inputs"
COLORS = {"sphere": "#B66A50", "dynamic_diagonal": "#70757C",
          "frozen_full_target": "#4F7A68", "dynamic_full": "#274C77"}
STYLES = {"sphere": (0, (4, 2)), "dynamic_diagonal": (0, (1, 1.5)),
          "frozen_full_target": (0, (5, 1.5, 1, 1.5)), "dynamic_full": "-"}
LABELS = {"sphere": "NEWUOA (full)", "dynamic_diagonal": "Diagonal metric",
          "frozen_full_target": "Fixed full target", "dynamic_full": "MATRO"}
NAMES = {"mw_07": r"Rosenbrock ($n=2$)", "mw_12": r"Powell singular ($n=4$)",
         "mw_19": r"Watson ($n=6$)", "mw_27": r"Brown–Dennis ($n=4$)"}
BUDGET = {"mw_07": 1500, "mw_12": 2500, "mw_19": 3500, "mw_27": 2500}
TRAJ_COLORS = {"matro": COLORS["dynamic_full"], "newuoa_full": COLORS["sphere"]}
METHODS = ['matro','newuoa_full','newuoa_standard','cobyqa','nelder_mead_tight','cmaes']
METHOD_LABELS = ['MATRO','NEWUOA (full)',r'NEWUOA ($2n+1$)','COBYQA','Nelder–Mead','CMA-ES']
METHOD_COLORS = ['#274C77','#B66A50','#4F7A68','#80719A','#70757C','#A78539']
METHOD_STYLES = ['-','--','-.',(0,(5,1,1,1)),':',(0,(7,2))]
TEXT_WIDTH = 210 / 25.4 - 2
WIDTH = .94 * TEXT_WIDTH
GRID_COLOR = "#E7E9EC"


def style():
    plt.style.use(HERE / "style/publication.mplstyle")
    for path in (HERE / "fonts").glob("*.otf"):
        font_manager.fontManager.addfont(path)
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Latin Modern Roman"],
        "mathtext.fontset": "cm", "axes.unicode_minus": True,
        "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "legend.fontsize": 9, "axes.linewidth": .6,
        "text.color": "#262C33", "axes.labelcolor": "#262C33",
        "axes.edgecolor": "#555C64", "xtick.color": "#444B53",
        "ytick.color": "#444B53",
        "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.major.width": .6, "ytick.major.width": .6,
        "xtick.major.size": 2.6, "ytick.major.size": 2.6,
        "axes.axisbelow": True, "savefig.dpi": 300,
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.hashsalt": "matro-v13-5-article",
    })


def save(fig, name):
    for extension in ("pdf", "svg", "png"):
        fig.savefig(HERE / f"{name}.{extension}", dpi=300)
    plt.close(fig)


def draw_shape():
    d = DATA / "shape"
    curves = pd.read_csv(d / "shape_descent.csv.gz")
    runs = pd.read_csv(d / "runs.csv.gz")
    mapping = json.loads((d / "formal_run_map.json").read_text())
    runs = runs[runs.id.isin(mapping.values()) & runs.tau.eq(1e-9)]
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 4.95))
    fig.subplots_adjust(left=.112, right=.955, bottom=.11, top=.845,
                        wspace=.31, hspace=.49)
    order = ("dynamic_full", "sphere", "dynamic_diagonal", "frozen_full_target")
    handles = [Line2D([], [], color=COLORS[v], ls=STYLES[v], lw=1.5,
                      label=LABELS[v]) for v in order]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(.54, .995),
               ncol=2, columnspacing=2.1, handlelength=2.7, labelspacing=.55)
    plotted = {}
    for i, ((ident, name), ax) in enumerate(zip(NAMES.items(), axes.flat)):
        high = 1.05 * runs[runs.instance_id.eq(ident)].hit.max()
        tick = 100 if high > 300 else 50 if high > 150 else 25
        window = min(BUDGET[ident], int(tick * np.ceil(high / tick)))
        for v in COLORS:
            q = curves[curves.instance_id.eq(ident) & curves.variant.eq(v)]
            assert len(q) > 0
            if v in ("sphere", "dynamic_full"):
                ax.fill_between(q.nfev, q.q25, q.q75, color=COLORS[v], alpha=.085, lw=0)
            ax.plot(q.nfev, q["median"], color=COLORS[v], ls=STYLES[v],
                    lw=1.45 if v == "dynamic_full" else 1.15)
            plotted[f"{ident}:{v}"] = len(q)
        ax.set(xlim=(0, window), ylim=(1e-10, 2), yscale="log",
               xlabel="Function evaluations", ylabel="Relative objective gap")
        ax.set_title(f"({chr(97+i)})  {name}", loc="left", pad=7)
        ax.set_yticks([1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10])
        ax.yaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
        ax.axhline(1e-7, color="#A7ACB1", ls=(0, (2, 3)), lw=.8, zorder=0)
        ax.grid(axis="y", color=GRID_COLOR, lw=.45)
    for ax in axes[:, 1]:
        ax.set_ylabel("")
        ax.tick_params(labelleft=False)
    save(fig, "shape_descent")
    return plotted


def trajectory_title(case):
    config = case["function"]
    titles = {"rosenbrock": "Rosenbrock", "cubic_valley": "Cubic valley",
              "levy": "Lévy", "different_powers": "Different Powers"}
    name = titles[config["name"]]
    if config.get("coordinate_condition", 1) > 1:
        name += r" ($\kappa(A)=" + f"{config['coordinate_condition']:g}" + "$)"
    else:
        name += r" ($c=10^{" + str(int(np.log10(config["coefficient"]))) + "}$)"
    return name


def region_panel(ax, case, record, view, field):
    color = TRAJ_COLORS[record["method"]]
    gap = np.maximum(field["f"].astype(float) - case["reference"], 1e-12)
    z = np.log10(gap)
    low = np.log10(max((record["f"][0] - case["reference"]) * 1e-6, 1e-10))
    high = float(np.quantile(z, .97))
    if case["function"]["name"] == "levy":
        high = np.log10(2 * (record["f"][0] - case["reference"]))
        low = np.log10(max((record["f"][0] - case["reference"]) * 1e-4, 1e-10))
    levels = np.linspace(low, high, 10 if case["function"]["name"] == "levy" else 17)
    ax.contourf(field["x"], field["y"], z, levels=levels, cmap="Greys",
                alpha=.035, extend="both")
    ax.contour(field["x"], field["y"], z, levels=levels, colors="#A8ADB2",
               linewidths=.35, linestyles="solid", alpha=.70)
    ax.plot(*np.asarray(record["centers"]).T, color=color, lw=1.2, zorder=6)
    theta = np.linspace(0, 2*np.pi, 501)
    circle = np.array([np.cos(theta), np.sin(theta)])
    selected = record["selected_states"]
    for rank, index in enumerate(selected):
        state = record["states"][index]
        ellipse = (np.asarray(state["center"])[:, None]
                   + state["delta"] * np.asarray(state["transform"]) @ circle)
        ax.fill(*ellipse, color=color, alpha=.012, zorder=2, clip_on=True)
        ax.plot(*ellipse, color=color, lw=.7,
                alpha=.32+.36*rank/max(1, len(selected)-1), zorder=3, clip_on=True)
    ax.scatter(*case["x0"], marker="s", s=17, fc="#30363A", ec="white", lw=.5, zorder=8)
    ax.scatter(*case["optimum"], marker="*", s=45, fc="#89723F", ec="white", lw=.5, zorder=9)
    ax.set(xlim=(view["lo"][0], view["hi"][0]),
           ylim=(view["lo"][1], view["hi"][1]), aspect="equal",
           xlabel="$x_1$", ylabel="$x_2$")
    ax.xaxis.set_major_locator(MaxNLocator(3))
    ax.yaxis.set_major_locator(MaxNLocator(3))
    ax.tick_params(labelsize=7.5, pad=1.5, length=2.4)
    ax.xaxis.labelpad = 2
    ax.yaxis.labelpad = 2
    ax.set_title("MATRO" if record["method"] == "matro" else "NEWUOA (full)",
                 fontsize=8.5, pad=5)


def descent_panel(ax, case, records):
    maxend = max(record["end"] for record in records)
    end = int(np.ceil(1.07 * maxend))
    tau = 1e-7
    ax.axhline(tau, color="#B6BDC2", lw=.8, ls=(0, (2, 3)), zorder=0)
    for record in records:
        gap = np.maximum((np.asarray(record["best"])-case["reference"])
                         / (record["f"][0]-case["reference"]), 1e-12)
        method = record["method"]
        color = TRAJ_COLORS[method]
        ax.step(np.arange(1, len(gap)+1), gap, where="post", color=color,
                lw=1.2, ls="-" if method == "matro" else (0, (3, 2)))
        hit = record["summary"]["first_hits"]["1e-07"]
        if hit:
            ax.scatter(hit, tau, marker="o" if method == "matro" else "s",
                       s=17, fc=color if method == "matro" else "white",
                       ec=color, lw=.8, zorder=8)
            ax.annotate(str(hit), (hit, tau), xytext=(3, 6),
                        textcoords="offset points", fontsize=8, color=color)
    ax.set(xlim=(0, end), yscale="log", ylim=(1e-10, 2),
           xlabel="Function evaluations", ylabel="Relative gap")
    ax.set_yticks([1, 1e-5, 1e-10])
    ax.yaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_locator(MaxNLocator(4, integer=True))
    ax.tick_params(labelsize=7.5, pad=2)
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)
    ax.xaxis.labelpad = 3
    ax.yaxis.labelpad = 2
    ax.grid(axis="y", color=GRID_COLOR, lw=.45)


def draw_trajectories():
    data = DATA / "trajectories"
    ids = json.loads((data / "index.json").read_text())
    loaded = []
    for ident in ids:
        with gzip.open(data / (ident + ".json.gz"), "rt", encoding="utf8") as handle:
            record = json.load(handle)
        field = dict(np.load(data / (ident + "_field.npz")))
        loaded.append((record, field))
    assert len(loaded) == 4
    fig = plt.figure(figsize=(WIDTH, 6.55))
    outer = fig.add_gridspec(2, 2, left=.10, right=.985, bottom=.105,
                             top=.91, wspace=.27, hspace=.55)
    selected = {}
    for i, (data, field) in enumerate(loaded):
        grid = outer[i//2, i%2].subgridspec(2, 2, height_ratios=[3, 1.12],
                                          hspace=.47, wspace=.32)
        for j, record in enumerate(data["records"]):
            ax = fig.add_subplot(grid[0, j])
            region_panel(ax, data["case"], record, data["view"], field)
            if j:
                ax.set_ylabel("")
                ax.tick_params(labelleft=False)
            selected[f"{data['case']['id']}:{record['method']}"] = record["selected_states"]
        descent_panel(fig.add_subplot(grid[1, :]), data["case"], data["records"])
        pos = outer[i//2, i%2].get_position(fig)
        fig.text((pos.x0+pos.x1)/2, pos.y1+.033,
                 f"({chr(97+i)}) " + trajectory_title(data["case"]),
                 ha="center", fontsize=9.5)
    symbols = [Line2D([], [], color=TRAJ_COLORS["matro"], lw=1.4, label="MATRO"),
               Line2D([], [], color=TRAJ_COLORS["newuoa_full"], lw=1.4,
                      ls="--", label="NEWUOA (full)"),
               Line2D([], [], marker="s", ls="", ms=4, color="#30363A", label="Start"),
               Line2D([], [], marker="*", ls="", ms=6, color="#89723F", label="Minimizer")]
    fig.legend(handles=symbols, loc="lower center", bbox_to_anchor=(.54, .018),
               ncol=4, fontsize=8.5, columnspacing=1.6, handlelength=2.3)
    save(fig, "four_trajectories")
    for data, field in loaded:
        fig = plt.figure(figsize=(WIDTH, 4.6))
        grid = fig.add_gridspec(2, 2, left=.105, right=.985, bottom=.17,
                               top=.86, height_ratios=[3, 1.12],
                               hspace=.47, wspace=.32)
        for j, record in enumerate(data["records"]):
            ax = fig.add_subplot(grid[0, j])
            region_panel(ax, data["case"], record, data["view"], field)
            if j:
                ax.set_ylabel("")
                ax.tick_params(labelleft=False)
        descent_panel(fig.add_subplot(grid[1, :]), data["case"], data["records"])
        fig.text(.545, .95, trajectory_title(data["case"]), ha="center", fontsize=10.5)
        fig.legend(handles=symbols, loc="lower center", bbox_to_anchor=(.54, .015),
                   ncol=4, fontsize=8.5, columnspacing=1.6, handlelength=2.3)
        save(fig, "trajectory_" + data["case"]["function"]["name"])
    return selected


def method_legend(fig):
    handles = [Line2D([], [], label=label, color=color, ls=line,
                      lw=1.5 if i == 0 else 1.05)
               for i,(label,color,line) in enumerate(zip(METHOD_LABELS,METHOD_COLORS,METHOD_STYLES))]
    fig.legend(handles=handles, ncol=3, loc='upper center',
               bbox_to_anchor=(.53,.995), frameon=False, fontsize=8.5,
               handlelength=2.7, columnspacing=1.4, labelspacing=.6)


def draw_profiles():
    report = {}
    for kind in ['data','performance']:
        fig, axes = plt.subplots(2,2,figsize=(WIDTH,4.95))
        fig.subplots_adjust(left=.115,right=.955,bottom=.11,top=.855,
                            wspace=.31,hspace=.40)
        method_legend(fig)
        for ax,exponent in zip(axes.flat,[3,5,7,9]):
            table=pd.read_csv(DATA/f'profiles_1e-{exponent}.csv.gz')
            assert set(table.denominator)=={2940}
            for i,method in enumerate(METHODS):
                q=table[(table.profile==kind)&(table.method==method)].sort_values('x')
                assert np.all(np.diff(q.solved_fraction)>=-1e-12)
                ax.step(q.x,q.solved_fraction,where='post',color=METHOD_COLORS[i],
                        ls=METHOD_STYLES[i],lw=1.5 if i==0 else 1.05,zorder=10 if i==0 else 2)
                report[f'{kind}:{exponent}:{method}']=len(q)
            ax.set_title(rf'$\tau=10^{{-{exponent}}}$',pad=6)
            ax.set_ylim(0,1)
            ax.set_yticks([0,.25,.5,.75,1])
            ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
            ax.set_ylabel('Fraction of problems solved')
            if kind=='performance':
                ax.set_xscale('log',base=2);ax.set_xlim(1,128)
                ax.set_xticks([1,2,4,8,16,32,64,128])
                ax.xaxis.set_major_formatter(ScalarFormatter())
                ax.set_xlabel('Evaluations / fastest solver')
                ax.tick_params(axis='x',labelsize=7.7)
            else:
                ax.set_xscale('symlog',linthresh=1);ax.set_xlim(0,500)
                ax.set_xticks([0,1,5,20,100,500])
                ax.xaxis.set_major_formatter(ScalarFormatter())
                ax.set_xlabel(r'Evaluations / $(n+1)$')
            ax.grid(axis='y',color=GRID_COLOR,lw=.45)
        for ax in axes[:, 1]:
            ax.set_ylabel('')
            ax.tick_params(labelleft=False)
        save(fig,f'{kind}_profiles')
    return report


def draw_nine():
    examples=['cutest_palmer8c_n8','cutest_brownbs_n2','cutest_nondquar_n12',
              'mw_07','mw_43','cutest_watson_n12','cutest_yfitu_n3',
              'cutest_kirby2ls_n5','cutest_himmelbf_n4']
    curves=pd.read_csv(DATA/'nine_descent.csv.gz')
    instances=pd.read_csv(DATA/'nine_instances.csv.gz').set_index('instance_id')
    fig,axes=plt.subplots(3,3,figsize=(TEXT_WIDTH,5.65))
    fig.subplots_adjust(left=.105,right=.987,bottom=.08,top=.875,
                        wspace=.25,hspace=.38)
    method_legend(fig)
    report={}
    for j,(ax,ident) in enumerate(zip(axes.flat,examples)):
        frame=curves[curves.instance_id.eq(ident)]
        for i,method in enumerate(METHODS):
            q=frame[frame.method.eq(method)]
            if i<2:
                ax.fill_between(q.nfev,np.maximum(q.q25_gap,1e-10),
                                np.maximum(q.q75_gap,1e-10),step='post',
                                color=METHOD_COLORS[i],alpha=.085,lw=0)
            ax.step(q.nfev,np.maximum(q.median_gap,1e-10),where='post',
                    color=METHOD_COLORS[i],ls=METHOD_STYLES[i],
                    lw=1.5 if i==0 else 1.0,zorder=10 if i==0 else 2)
            report[f'{ident}:{method}']=len(q)
        row=instances.loc[ident];name=str(row['name']).upper().replace('_',' ')
        if ident=='mw_07':name='Rosenbrock'
        if ident=='mw_43':name='Cube'
        if ident=='cutest_watson_n12':name='Watson'
        ax.set_title(f'({chr(97+j)}) {name}'+rf', $n={int(row["n"])}$',
                     loc='left',pad=6,fontsize=8.5)
        ax.set_xscale('log');ax.set_yscale('log')
        ax.set_xlim(1,frame.nfev.max());ax.set_ylim(1e-10,1.8)
        ax.set_yticks([1,1e-3,1e-6,1e-9])
        ax.xaxis.set_major_locator(LogLocator(base=10,numticks=5))
        ax.xaxis.set_minor_locator(LogLocator(base=10,subs=[2,5]))
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.yaxis.set_minor_locator(NullLocator())
        ax.grid(axis='y',color=GRID_COLOR,lw=.45)
        ax.tick_params(direction='out',pad=2,labelsize=8)
        if j%3==0:ax.set_ylabel('Relative objective gap',fontsize=8.5)
        else:ax.tick_params(labelleft=False)
        if j>=6:ax.set_xlabel('Objective evaluations',fontsize=8.5)
    save(fig,'descent_nine')
    return report


def draw_conditioning():
    table=pd.read_csv(DATA/'conditioning_summary.csv')
    report={}
    for success in (True,False):
        fig,axes=plt.subplots(2,2,figsize=(WIDTH,4.95))
        fig.subplots_adjust(left=.118,right=.955,bottom=.11,top=.86,
                            wspace=.32,hspace=.46)
        handles=[Line2D([],[],color=COLORS[v],ls=STYLES[v],lw=1.5,
                        label=LABELS[v]) for v in ('dynamic_full','sphere')]
        fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.54,.975),
                   ncol=2,columnspacing=2.5,handlelength=2.7)
        for i,((ident,name),ax) in enumerate(zip(NAMES.items(),axes.flat)):
            for v in ('sphere','dynamic_full'):
                q=table[table.instance_id.eq(ident)&table.variant.eq(v)].sort_values('kappa')
                y=q.success if success else q.mean_queries
                lo=q.success_low if success else q.queries_low
                hi=q.success_high if success else q.queries_high
                ax.fill_between(q.kappa,lo,hi,color=COLORS[v],alpha=.085,lw=0)
                ax.plot(q.kappa,y,color=COLORS[v],ls=STYLES[v],lw=1.35,
                        marker='s' if v=='sphere' else 'o',ms=2.8,
                        mfc='white' if v=='sphere' else COLORS[v],mew=.7,clip_on=False)
                report[f'{ident}:{v}']=len(q)
            ax.set(xscale='log',xlim=(.85,1.18e5),xlabel=r'Coordinate condition number $\kappa(A)$')
            ax.xaxis.label.set_size(8.5)
            ax.set_xticks([1,10,100,1000,10000,100000])
            ax.xaxis.set_minor_locator(LogLocator(base=10,subs=(2,5),numticks=30))
            ax.xaxis.set_minor_formatter(NullFormatter())
            ax.grid(axis='y',color=GRID_COLOR,lw=.45)
            ax.set_title(f'({chr(97+i)})  {name}',loc='left',pad=7,fontsize=9)
            if success:
                ax.set(ylim=(-.025,1.055),ylabel='Success rate')
                ax.set_yticks([0,.25,.5,.75,1])
                ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0))
            else:
                ax.set(ylim=(0,BUDGET[ident]*1.07),ylabel='Mean evaluations to target')
                ax.yaxis.label.set_size(8.5)
                ax.set_yticks(np.arange(0,BUDGET[ident]+1,500))
                ax.yaxis.set_major_formatter(lambda x,pos:f'{int(x):,}')
                ax.axhline(BUDGET[ident],color='#969B9F',lw=.8,ls=(0,(2,3)),zorder=0)
        for ax in axes[:, 1]:
            ax.set_ylabel('')
            if success: ax.tick_params(labelleft=False)
        save(fig,'anisotropy_success' if success else 'anisotropy_budget_linear')
    return report


def draw_coverage():
    field=np.load(DATA/'coverage_field.npz')
    fig=plt.figure(figsize=(TEXT_WIDTH,2.55))
    axes=[fig.add_axes(p) for p in ([.08,.38,.405,.51],[.57,.38,.405,.51])]
    cmap=colors.LinearSegmentedColormap.from_list('absolute_error',
          ['#FAFAF7','#DEE5E7','#A6BAC5','#637E94','#2E465F'])
    norm=colors.PowerNorm(.5,vmin=0,vmax=.4)
    x,y=np.meshgrid(field['x'],field['y']);w=field['metric_eigenvalues']
    extent=[field['x'].min(),field['x'].max(),field['y'].min(),field['y'].max()]
    for i,ax in enumerate(axes):
        inside=x*x+y*y<=1 if i==0 else w[0]*x*x+w[1]*y*y<=1
        ax.imshow(field['error'],extent=extent,origin='lower',norm=norm,cmap=cmap,
                   alpha=np.where(inside,1.,.06),interpolation='nearest',rasterized=True)
        curve=field['circle'] if i==0 else field['ellipse']
        ax.plot(*curve.T,color='#49515B',lw=.75,alpha=.9,zorder=4)
        ax.scatter(*field['samples'].T,s=18,fc='white',ec='#343C46',lw=.75,zorder=6)
        ax.scatter([0],[0],marker='+',s=40,lw=1,color='#343C46',zorder=7)
        ax.set(xlim=(-2.4,2.4),ylim=(-1.2,1.2),xlabel=r'$u_1$')
        ax.set_aspect('equal');ax.set_xticks([-2,-1,0,1,2]);ax.set_yticks([-1,0,1])
        ax.tick_params(length=2.6,pad=2,labelsize=8)
        ax.set_title('(a)  Sphere' if i==0 else '(b)  MATRO',loc='left',pad=6)
        if i==0:ax.set_ylabel(r'$u_2$',labelpad=4)
        else:ax.tick_params(labelleft=False)
    cax=fig.add_axes([.24,.175,.57,.032])
    cb=fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap=cmap),cax=cax,
                   orientation='horizontal',extend='max',ticks=[0,.025,.1,.2,.4])
    cb.ax.set_xticklabels(['0','0.025','0.1','0.2','0.4'])
    cb.ax.tick_params(length=2,pad=2,labelsize=8)
    cb.outline.set_linewidth(.5)
    cb.set_label(r'Absolute prediction error  $|f(x_k+s)-m_k(s)|$',labelpad=3,fontsize=9)
    save(fig,'interpolation_coverage')
    return dict(grid_shape=list(field['error'].shape),square_root_color_scale=True,
                saturation=.4)


if __name__ == "__main__":
    manifest = json.loads((DATA / "manifest.json").read_text())
    for entry in manifest["files"]:
        path = HERE.parent / entry["destination"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    style()
    report = dict(figure_width_inches=WIDTH, text_width_inches=TEXT_WIDTH,
                  paper_width_points=TEXT_WIDTH*72,
                  optimizer_evaluations=0, objective_evaluations=0,
                  source_files_checked=len(manifest["files"]),
                  shape_plotted_rows=draw_shape(),
                  unchanged_trajectory_state_indices=draw_trajectories(),
                  profile_rows=draw_profiles(),nine_curve_rows=draw_nine(),
                  conditioning_rows=draw_conditioning(),coverage=draw_coverage())
    try:
        import psutil
        info=psutil.Process().memory_info()
        report['peak_working_set_bytes']=getattr(info,'peak_wset',info.rss)
        assert report['peak_working_set_bytes']<manifest['plot_peak_working_set_budget_bytes']
    except ImportError:
        pass
    (HERE / "redraw_checks.json").write_text(json.dumps(report, indent=2), encoding="utf8")
    print(json.dumps({k:v for k,v in report.items() if isinstance(v, (int, float))}))
