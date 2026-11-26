# Static figures for Lecture 3 (variogram and kriging). Needs numpy and matplotlib.
# Run from the repository root: python figures/make_L3_kriging_figures.py
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
OUT="figures/"  # run from the repository root
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.spines.top":False,"axes.spines.right":False,"savefig.dpi":200,"savefig.bbox":"tight"})
BLUE="#2457a6"; RED="#b3261e"; GREY="#5a6573"; AMB="#c47a00"
import sys
rng=np.random.default_rng(int(sys.argv[1]) if len(sys.argv)>1 else 2026)
C0,C1,A=0.2,0.9,0.3
def sph(h,c0=C0,c1=C1,a=A):
    h=np.asarray(h,float); g=np.where(h<a,c0+c1*(1.5*h/a-0.5*(h/a)**3),c0+c1); return np.where(h==0,0,g)
def cov(h): return (C0+C1)-sph(h)
# ---- simulate field at many sites
n=260; S=rng.random((n,2))
D=np.hypot(*(S[:,None,:]-S[None,:,:]).transpose(2,0,1))
K=cov(D)+np.eye(n)*1e-9  # nugget = white noise
K[np.diag_indices(n)]=C0+C1
z=5+np.linalg.cholesky(K)@rng.standard_normal(n)
# empirical variogram
iu=np.triu_indices(n,1); h=D[iu]; g=0.5*(z[iu[0]]-z[iu[1]])**2
bins=np.linspace(0,0.7,15); mid=(bins[:-1]+bins[1:])/2
gh=np.array([g[(h>=bins[k])&(h<bins[k+1])].mean() for k in range(14)]); nh=np.array([((h>=bins[k])&(h<bins[k+1])).sum() for k in range(14)])
# fit spherical by weighted LS grid search
best=None
for c0 in np.linspace(0,0.6,31):
  for c1 in np.linspace(0.2,1.6,57):
    for a in np.linspace(0.1,0.7,61):
      L=(nh*(gh-sph(mid,c0,c1,a))**2).sum()
      if best is None or L<best[0]: best=(L,c0,c1,a)
_,f0,f1,fa=best; print("fit",f0,f1,fa)
# ---- Figure 1
fig,ax=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={"width_ratios":[1,1.45],"wspace":0.35})
sc=ax[0].scatter(S[:,0],S[:,1],c=z,cmap="viridis",s=28,edgecolor="white",linewidth=.5)
ax[0].set_aspect("equal"); ax[0].set_xlim(0,1); ax[0].set_ylim(0,1); ax[0].set_title("(a) 260 measured sites",loc="left")
ax[0].set_xlabel("x"); ax[0].set_ylabel("y"); fig.colorbar(sc,ax=ax[0],shrink=.8,label="Z(s)")
i,j=np.argmin(D+np.eye(n)*9)//n,np.argmin(D+np.eye(n)*9)%n
p=ax[1]
p.scatter(mid,gh,s=12+nh/8,color=GREY,zorder=3,label="empirical semivariogram $\\hat\\gamma(h)$\n(dot size = number of pairs)")
hh=np.linspace(0,0.7,400); p.plot(hh[1:],sph(hh[1:],f0,f1,fa),color=BLUE,lw=2.5,label="fitted spherical model $\\gamma(h)$")
p.plot([0],[0],"o",color=BLUE,ms=5)
sill=f0+f1
p.axhline(sill,color=RED,ls="--",lw=1); p.axvline(fa,color=RED,ls="--",lw=1)
p.annotate("",xy=(0.012,f0),xytext=(0.012,0),arrowprops=dict(arrowstyle="<->",color=RED,lw=1.5))
p.text(0.022,f0/2,"nugget $c_0$",color=RED,va="center")
p.annotate("",xy=(0.67,sill),xytext=(0.67,f0),arrowprops=dict(arrowstyle="<->",color=RED,lw=1.2))
p.text(0.655,(sill+f0)/2,"partial sill $c_1$",color=RED,ha="right",va="center")
p.text(fa+0.015,sill-0.05,"sill $c_0+c_1$\n= total variance",color=RED,va="top")
p.text(fa+0.01,sill*1.2,"range $a$",color=RED)
p.text(0.1,0.22,"close sites:\nsimilar values,\nsmall $\\gamma$",color=GREY,fontsize=10)
p.text(fa+0.03,0.5,"beyond the range:\nsites unrelated",color=GREY,fontsize=10)
p.set_xlim(0,0.72); p.set_ylim(0,max(sill*1.3,gh.max()*1.08)); p.set_xlabel("distance between two sites, h"); p.set_ylabel("semivariance")
p.set_title("(b) Semivariogram: how fast similarity decays",loc="left"); p.legend(loc="upper center",bbox_to_anchor=(0.5,-0.16),ncol=2,frameon=False,fontsize=9.5)
fig.savefig(OUT+"L3_fig1_variogram_anatomy.png"); plt.close(fig)

# ---- OK helpers
def ok(sites,vals,targets,c0=f0,c1=f1,a=fa):
    m=len(sites); Dm=np.hypot(*(sites[:,None]-sites[None]).transpose(2,0,1))
    G=np.ones((m+1,m+1)); G[:m,:m]=sph(Dm,c0,c1,a); G[m,m]=0
    Gi=np.linalg.inv(G); preds=[];var=[];W=[]
    for t in targets:
        b=np.ones(m+1); b[:m]=sph(np.hypot(*(sites-t).T),c0,c1,a)
        x=Gi@b; W.append(x[:m]); preds.append(x[:m]@vals); var.append(x@b)
    return np.array(preds),np.array(var),np.array(W)
# ---- Figure 2: weights IDW vs OK
s0=np.array([0.5,0.5])
P=np.array([[0.63,0.55],[0.31,0.38],[0.27,0.42],[0.32,0.32],[0.46,0.84],[0.80,0.61]])
lab=["A","B1","B2","B3","C","D"]
OFF={"A":(0.0,-0.075,"center"),"B1":(0.06,0.0,"left"),"B2":(-0.06,0.03,"right"),"B3":(0.0,-0.06,"center"),"C":(0.07,0.0,"left"),"D":(0.0,0.07,"center")}
d=np.hypot(*(P-s0).T); wi=(1/d**2)/(1/d**2).sum()
_,_,Wk=ok(P,np.zeros(len(P)),[s0],0.02,0.98,0.6); wk=Wk[0]
print(np.round(wi,3),np.round(wk,3))
fig,ax=plt.subplots(1,2,figsize=(11,5))
for k,(w,t) in enumerate([(wi,"(a) IDW ($\\beta=2$): weights depend on distance only"),(wk,"(b) Ordinary kriging: weights also see the other sites")]):
    q=ax[k]; q.set_aspect("equal"); q.set_xlim(0.1,0.95); q.set_ylim(0.2,0.97); q.set_xticks([]); q.set_yticks([])
    for sp in q.spines.values(): sp.set_visible(True); sp.set_color("#d6dce2")
    for pt in P: q.plot([s0[0],pt[0]],[s0[1],pt[1]],color="#d6dce2",lw=1,zorder=1)
    for pt,wv,l in zip(P,w,lab):
        r=0.012+0.065*np.sqrt(abs(wv)); col=BLUE if wv>=0 else RED
        q.add_patch(Circle(pt,r,facecolor=col,alpha=.25 if wv>=0 else .18,edgecolor=col,lw=1.5,ls="-" if wv>=0 else "--",zorder=2))
        q.plot(*pt,"o",color="black",ms=4,zorder=3)
        ox,oy,ha=OFF[l]; q.text(pt[0]+ox,pt[1]+oy,f"{l}  {wv:+.2f}",fontsize=10.5,zorder=4,color=col,ha=ha,va="center")
    q.plot(*s0,marker="*",color=AMB,ms=18,mec="black",zorder=5); q.text(s0[0]-0.02,s0[1]+0.05,"$s_0$ (predict here)",fontsize=10,ha="center")
    q.set_title(t,loc="left",fontsize=11)
fig.text(0.5,0.02,"Circle area is proportional to the weight. Red dashed = negative weight. Weights sum to 1 in both panels.",ha="center",color=GREY,fontsize=10)
fig.savefig(OUT+"L3_fig2_kriging_weights.png"); plt.close(fig)

# ---- Figure 3: prediction + standard error
sub=rng.choice(n,35,replace=False); Ss,zs=S[sub],z[sub]
gx=np.linspace(0,1,120); X,Y=np.meshgrid(gx,gx); T=np.c_[X.ravel(),Y.ravel()]
pr,va,_=ok(Ss,zs,T); se=np.sqrt(np.maximum(va,0))
fig,ax=plt.subplots(1,2,figsize=(11,4.6))
im=ax[0].imshow(pr.reshape(120,120),origin="lower",extent=(0,1,0,1),cmap="viridis"); fig.colorbar(im,ax=ax[0],shrink=.85,label="predicted $\\hat Z(s_0)$")
im2=ax[1].imshow(se.reshape(120,120),origin="lower",extent=(0,1,0,1),cmap="magma_r"); fig.colorbar(im2,ax=ax[1],shrink=.85,label="kriging standard error")
for q,t in zip(ax,["(a) Kriging prediction","(b) Kriging standard error: how sure we are"]):
    q.scatter(Ss[:,0],Ss[:,1],s=22,facecolor="white",edgecolor="black",lw=.8); q.set_title(t,loc="left"); q.set_xticks([]); q.set_yticks([])
ax[1].text(0.5,-0.08,"Low near sites, high in gaps and at the edges. It depends on where the sites are, not on their values.",transform=ax[1].transAxes,ha="center",va="top",fontsize=9.5,color=GREY)
fig.savefig(OUT+"L3_fig3_prediction_and_uncertainty.png"); plt.close(fig)
print(se.min(),se.max())
