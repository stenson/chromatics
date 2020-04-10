from coldtype import *
from coldtype.pens.translationpen import TranslationPen, polarCoord
from math import radians
from random import randint

src = DefconFont("src/chromatics.ufo")

def Glyphs(ufo, glyphNames):
    return DATPenSet([DATPen().glyph(ufo.layers["public.default"][gn]) for gn in glyphNames]).distribute()

DATPenSet.Glyphs = Glyphs

angle = randint(-60, -30)
angle = -45

def harrild1(r, letter):
    g = DATPen().glyph(src[letter]).removeOverlap()
    gs = DATPen().glyph(src.layers["shadow"][letter])

    g_comp = DATPenSet()
    knock = g.copy().grow(10).project(angle, 5).f(1)#.s(0)
    main_shadow = g.copy().grow(5).castshadow(angle, 100).difference(knock).f(Gradient.Horizontal(r, ("hr0.8-0.9",0.65,0.5), ("hr0.9-1.3",0.65,0.5)))
    g_comp += main_shadow
    g_comp += g.f(Gradient.Vertical(r, ("hr0.6-0.8", 0.75, 0.75), ("hr0.3-0.5", 0.75, 0.75)))
    #g_comp += g.f("hr",0.5,0.5,0.1)
    gse = gs.explode()
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
    gse.pmap(extrude)
    g_comp += gse.f(Gradient.Horizontal(r, ("hr0.6-0.9", 0.5, 0.35), ("hr0.5-0.8", 0.65, 0.25)))
    return g_comp

@renderable(bg=1, watch=[src.path])
def test(r):
    #g = DATPenSet.Glyphs(src, ["R"]).track(10).pen()
    glyphs = DATPenSet([
        harrild1(r, "R"),
        harrild1(r, "S"),
    ]).distribute().track(10).align(r)
    return glyphs