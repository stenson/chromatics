from coldtype import *
from coldtype.pens.translationpen import TranslationPen, polarCoord
from math import radians

src = DefconFont("src/chromatics.ufo")

def Glyphs(ufo, glyphNames):
    return DATPenSet([DATPen().glyph(ufo[gn]) for gn in glyphNames]).distribute()

DATPenSet.Glyphs = Glyphs

@renderable(bg=1, watch=[src.path])
def test(r):
    #A = StyledString("AR", Style(font, 1000, t=10)).pen().align(r).removeOverlap()
    #A = DATPen().glyph(src["A"]).align(r)
    A = DATPenSet.Glyphs(src, ["R","A","I"]).pen()
    A_comp = DATPenSet()
    knock = A.copy().grow(10).project(-45, 5).f(1)#.s(0)
    A_comp += A.copy().castshadow(-45, 100).difference(knock).f(Gradient.Vertical(r, ("hr",0.5,0.35), ("hr",0.5,0.35)))
    A_comp += A.f(Gradient.Horizontal(r, ("hr", 0.65, 0.5), ("hr", 0.65, 0.5)))
    return A_comp