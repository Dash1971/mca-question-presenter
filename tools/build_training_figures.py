"""Generate original, self-contained examination figures (matplotlib required)."""
from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parents[2]/'mpl-cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

OUT=Path(__file__).resolve().parents[1]/'presenter'/'web'/'assets'
plt.rcParams.update({'font.size':12,'font.family':'DejaVu Sans','svg.fonttype':'none','svg.hashsalt':'mca-oow-training'})

def save(fig,name):
    fig.savefig(OUT/name,format='svg',metadata={'Date':None},facecolor='white',bbox_inches='tight')
    # DejaVu is used for plotting metrics but is not installed on every student
    # computer. Declare common offline font fallbacks in the exported SVG.
    svg=(OUT/name).read_text()
    (OUT/name).write_text(svg.replace("font-family: 'DejaVu Sans'", "font-family: Arial, 'DejaVu Sans', sans-serif"))
    if os.environ.get('MCA_FIGURE_QA'):
        qa=Path(os.environ['MCA_FIGURE_QA'])
        qa.mkdir(parents=True,exist_ok=True)
        fig.savefig(qa/(Path(name).stem+'.png'),dpi=120,facecolor='white',bbox_inches='tight')
    plt.close(fig)

def base(title,xlabel,ylabel):
    fig,ax=plt.subplots(figsize=(8,4.8),layout='constrained')
    ax.set(title=title,xlabel=xlabel,ylabel=ylabel)
    ax.grid(color='#d6e0e5',linewidth=.6)
    ax.set_axisbelow(True)
    return fig,ax

for name,title,origin,values in [
 ('tide-rise-2.svg','Training tidal curve — rising tide','low water',[0,.05,.20,.50,.80,.95,1]),
 ('tide-fall-3.svg','Training tidal curve — falling tide','high water',[0,.10,.25,.50,.80,.95,1])]:
    change='risen' if origin=='low water' else 'fallen'
    fig,ax=base(title,f'Hours after {origin}',f'Fraction of tidal range {change}')
    ax.plot(range(7),values,'o-',color='#126d78',linewidth=2,markersize=5)
    ax.set(xlim=(-.15,6.15),ylim=(-.03,1.07),xticks=range(7))
    ax.yaxis.set_major_locator(MultipleLocator(.1))
    for x,y in enumerate(values):
        ax.annotate(f'{y:.2f}',(x,y),xytext=(0,10 if y<.9 else -20),textcoords='offset points',ha='center',fontsize=11)
    save(fig,name)

fig,ax=base('Training chartwork grid','Easting from O (nautical miles)','Northing from O (nautical miles)')
ax.set(xlim=(-.5,10),ylim=(-.5,8),aspect='equal',xticks=range(0,11,2),yticks=range(0,9,2))
ax.plot([0,8],[0,6],color='#126d78',linewidth=2)
ax.plot([8,8,0],[0,6,6],color='#6b7c86',linewidth=1,linestyle='--')
ax.scatter([0,8],[0,6],color='#18303f',s=40)
ax.annotate('O (0, 0)',(0,0),xytext=(8,10),textcoords='offset points')
ax.annotate('P (8, 6)',(8,6),xytext=(8,10),textcoords='offset points')
save(fig,'chartwork-grid.svg')

for name,x,y in [
 ('gz-paper-2.svg',[0,10,20,30,35,40,50,60,70,80],[0,.25,.5,.65,.7,.66,.48,.25,0,-.2]),
 ('gz-paper-3.svg',[0,10,20,30,40,50,60,70,80,90],[0,.3,.6,.82,.9,.82,.6,.3,0,-.22])]:
    fig,ax=base('Training curve of statical stability','Angle of heel (degrees)','Righting lever GZ (m)')
    ax.plot(x,y,'o-',color='#126d78',linewidth=2,markersize=4)
    ax.axhline(0,color='#18303f',linewidth=1)
    ax.set(xlim=(0,max(x)),ylim=(-.3,1.05),xticks=range(0,max(x)+1,10))
    ax.yaxis.set_major_locator(MultipleLocator(.1))
    if name=='gz-paper-2.svg':ax.set_xticks(sorted(set(list(range(0,81,10))+[35])))
    save(fig,name)
print('Generated five training figures.')
