from coldtype import *
from coldtype.pens.datpen import DPR
from functools import partial

src = DefconFont("src/chromatics.ufo")

angle = -45

def harrild_shadow(r, g, gs=None):
    g_comp = DATPenSet()
    knock = g.copy().grow(10).project(angle, 5).f(1)#.s(0)
    main_shadow = g.copy()
    #main_shadow.grow(5)
    main_shadow.castshadow(angle, 100)
    #main_shadow.difference(knock)
    #main_shadow.difference(g)
    main_shadow.f(Gradient.Horizontal(r, ("hr0.8-0.9",0.65,0.5), ("hr0.9-1.3",0.65,0.5)))
    g_comp += main_shadow
    g_comp += g.f(Gradient.Vertical(r, ("hr0.6-0.8", 0.75, 0.75), ("hr0.3-0.5", 0.75, 0.75)))
    #g_comp += g.f("hr",0.5,0.5,0.1)
    
    def extrude(idx, p):
        if len(p.value) == 2:
            unprojected = p.copy().points()
            projected = p.copy().project(angle, 200).points()
            dp = DATPen()
            dp.line([unprojected[0][0], projected[0][0]])
            dp.outline(4).intersection(main_shadow)
            p.value = dp.value
        else:
            unprojected = p.copy().points()
            projected = p.copy().project(angle, 200).points()
            dp = DATPen()
            dp.moveTo(unprojected[0][2])
            dp.lineTo(projected[0][2])
            dp.lineTo(projected[0][1])
            dp.lineTo(unprojected[0][1])
            dp.closePath()
            #print(dp.value)
            dp.reverse().intersection(main_shadow)
            p.value = dp.value
    if False:
        gse = gs.explode()
        gse.pmap(extrude)
        g_comp += gse.f(Gradient.Horizontal(r, ("hr0.6-0.9", 0.5, 0.35), ("hr0.5-0.8", 0.65, 0.25)))
    return g_comp

def harrild1(r, letter):
    g = DATPen().glyph(src[letter]).explode().f("random")[3]
    gs = DATPen().glyph(src.layers["shadow"][letter])
    return harrild_shadow(r, g, gs)

#@renderable(bg=1, watch=[src.path])
def test(r):
    #g = DATPenSet.Glyphs(src, ["R"]).track(10).pen()
    glyphs = DATPenSet([
        harrild1(r, "T"),
        harrild1(r, "R"),
    ]).distribute().track(10).align(r)
    return glyphs

BLKW = 146
BLKH = 192
STMW = 62
VSRW = 62
VSRH = 192
CSBH = 38

def show_body(glyph, dps):
    return [
        DATPenSet([DPR(glyph.body).f("hr", 0.75, 0.8, 0.1).s(0, 0.1).sw(5), dps.copy().f("hr", 0.5, 0.5, 0.2).s(0, 0.3).sw(1)]).translate(-200, 0),
        dps.pen().removeOverlap().translate(200, 0).f(0.2)
    ]

french_no_9 = partial(glyph, postfn=show_body)

@french_no_9("A", width=300)
def _A():
    r = _A.body
    return DATPenSet([
        DPR(r.t(BLKW-20, "mnx").take(BLKH, "mny")),
        DPR(r.t(BLKW, "mxx").take(BLKH, "mny")),
        DPR(r.t(CSBH, "mdy").t(138, "mdx")).translate(0, -50),
        DATPen().glyph(src["A.legs"]).align(r, y="mxy")
    ])

@french_no_9("H", width=320)
def _H():
    r = _H.body
    return DATPenSet([
        DPR(r.t(STMW, "mnx").offset(BLKW/2-STMW/2, 0)),
        DPR(r.t(STMW, "mxx").offset(-(BLKW/2-STMW/2), 0)),
        DPR(r.t(BLKW, "mnx").t(BLKH, "mxy")),
        DPR(r.t(BLKW, "mxx").t(BLKH, "mxy")),
        DPR(r.t(BLKW, "mnx").t(BLKH, "mny")),
        DPR(r.t(BLKW, "mxx").t(BLKH, "mny")),
        DPR(r.t(CSBH, "mdy").inset(STMW, 0)),
    ])

@french_no_9("I", width=BLKW)
def _I():
    r = _I.body
    return DATPenSet([
        DPR(r.t(STMW, "mdx")),
        DPR(r.t(BLKW, "mdx").t(BLKH, "mxy")),
        DPR(r.t(BLKW, "mdx").t(BLKH, "mny"))
    ])

@french_no_9("T", width=250)
def _T():
    r = _T.body
    t_top = DATPen().glyph(src["T.top"]).align(r, x="mnx", y="mxy")
    return DATPenSet([
        DPR(r.t(STMW, "mdx")),
        DPR(r.t(BLKW, "mdx").t(BLKH, "mny")),
        t_top,
        t_top.copy().align(r, x="mxx", y="mxy").scale(-1, 1).reverse(),
    ])

@french_no_9("R", width=290)
def _R():
    r = _R.body
    return DATPenSet([
        DPR(r.t(STMW, "mnx")).translate(BLKW/2-STMW/2, 0),
        DPR(r.t(BLKW, "mnx").t(BLKH, "mny")),
        DPR(r.t(BLKW/2, "mnx").t(BLKH, "mxy")),
        DATPen().glyph(src["R.lobe"]).align(r, x="mxx", y="mxy").translate(-55, 0),
        DATPen().glyph(src["R.leg"]).align(r, x="mxx", y="mny"),
    ])

@french_no_9("S", width=190)
def _S():
    r = _S.body
    return DATPenSet([
        DPR(r.t(50, "mxx").t(300, "mxy").offset(-8, 0)),
        DPR(r.t(50, "mnx").t(350, "mny")),
        DATPen().glyph(src["S.curve"]).align(r)
    ])

@renderable()
def shadow_test(r):
    return harrild_shadow(r, _H.func().pen().s(None).removeOverlap()).align(r)