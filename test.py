from coldtype import *
from coldtype.pens.translationpen import TranslationPen
import defcon

img_path = Path("media/brrrrr.png").resolve()
src_path = Path("src/chromatics.ufo").resolve()
try:
    src = defcon.Font(str(src_path))
except:
    src = defcon.Font()
    src.insertGlyph(DATPen().oval(Rect(500, 500)).to_glyph(), "A")

#src.images[img_path.name] = img_path.read_bytes()
#img = defcon.Image(imageDict=dict(fileName=img_path.name))
#src["A"].image = img
#src.save(str(src_path))

def project(frontAngle, frontWidth):
    d = frontWidth
    lightAngle = frontAngle
    lightZAngle = 45; # how "straight-on" the light is (?)
    lightAngleRad = lightAngle * math.pi/180 - math.pi/2;
    lightZAngleRad = lightZAngle * math.pi/180;
    xTranslate = math.tan(lightZAngleRad) * d * math.cos(lightAngleRad);
    yTranslate = math.tan(lightZAngleRad) * d * math.sin(lightAngleRad);
    return (xTranslate, yTranslate)

def castshadow(self, angle=-45, width=100, ro=1):
    out = DATPen()
    tp = TranslationPen(out, frontAngle=angle, frontWidth=width)
    self.replay(tp)
    out.record(self.copy().translate(*project(-angle, width)))
    if ro:
        out.removeOverlap()
    self.value = out.value
    return self

DATPen.castshadow = castshadow

@renderable()
def test(r):
    A = DATPen().glyph(src["A"]).removeOverlap()
    A_comp = DATPenSet()
    A_comp += A.copy().castshadow().f("hr", 0.5, 0.5)#.s(0).sw(3)
    A_comp += A.copy().castshadow(width=20).f(1)
    #A_comp += A.copy().outline(10).f(1)
    A_comp += A.f("hr", 0.5, 0.5)
    return A_comp.align(r)