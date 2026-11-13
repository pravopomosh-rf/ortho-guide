// «После операции: тревожные признаки» — ролик для пациентов в формате «клинический случай» (9:16).
import React from 'react';
import {AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame, interpolate} from 'remotion';
import {Bg, FontCSS, Header, Headline, Card, Counter, Bar, Subtitle, Slot, Note, C, BODY, HEAD, MONO, ease, Word, clamp01} from './kit';
import {Vertebra} from './Vertebra';
import {Person, Icon} from './Figures';
import {Phone101} from './UrgentArt';
import timing from './timing_postop_ar.json';

type T = {id: string; dur: number; audio?: string; text: string; head: string; acc: string[]; label: string; sacc?: string[]}[];
const TT = timing as T;
const FPS = 30, PAD = 0.5;
export const totalPostop_ar = () => TT.reduce((s, x) => s + Math.round((x.dur + PAD) * FPS), 0);
const BRAND = 'جراحة العظام · للمرضى';

// words timed proportionally to characters across the audio
const wordsOf = (text: string, d: number): Word[] => {
  const ws = text.split(' ');
  const tot = ws.reduce((s, w) => s + w.length + 1, 0);
  let acc = 0;
  return ws.map((w) => { const t = Math.round(6 + (acc / tot) * (d - 10)); acc += w.length + 1; return {w, t}; });
};
const fr = (d: number, p: number) => Math.round(d * p);

const CheckRow: React.FC<{y: number; at: number; icon: string; text: string}> = ({y, at, icon, text}) => {
  const f = useCurrentFrame();
  return <Card x={64} y={y} w={952} at={at}>
    <div style={{display: 'flex', alignItems: 'center', gap: 26}}>
      <Icon k={icon} s={70} />
      <div style={{flex: 1, fontFamily: BODY, fontWeight: 700, fontSize: 34, color: C.ink, lineHeight: 1.25}}>{text}</div>
      <div style={{opacity: ease(f, at + 14, at + 22), transform: `scale(${0.6 + 0.4 * ease(f, at + 14, at + 22)})`}}><Icon k="check" s={60} /></div>
    </div>
  </Card>;
};
const Tier: React.FC<{y: number; at: number; title: string; color: string; bg: string; items: [string, string][]; h: number}> = ({y, at, title, color, bg, items, h}) => {
  const f = useCurrentFrame();
  return <Card x={64} y={y} w={952} h={h} at={at} style={{border: `4px solid ${color}`, background: bg}}>
    <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 36, color, marginBottom: 14}}>{title}</div>
    <div style={{display: 'flex', flexWrap: 'wrap', gap: '10px 18px'}}>
      {items.map(([k, t], i) => <div key={i} style={{display: 'flex', alignItems: 'center', gap: 10, opacity: ease(f, at + 8 + i * 6, at + 16 + i * 6)}}>
        <Icon k={k} s={42} c={color} /><span style={{fontFamily: BODY, fontWeight: 700, fontSize: 26, color: C.ink}}>{t}</span></div>)}
    </div>
  </Card>;
};
// ---- Тревожные признаки: сцены P01–P10 ----
const RED = C.blood, ORG = '#B45309', BLU = C.navy;
const Band: React.FC<{y: number; at: number; color: string; bg: string; title: string; sub: string}> = ({y, at, color, bg, title, sub}) => {
  const f = useCurrentFrame(); const p = ease(f, at, at + 14);
  return <div style={{position: 'absolute', left: 64, top: y, width: 952, height: 200, borderRadius: 28, background: bg, border: `4px solid ${color}`, overflow: 'hidden', opacity: p, transform: `translateX(${(1 - p) * -40}px)`}}>
    <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${100 * p}%`, background: color, opacity: 0.08}} />
    <div style={{position: 'absolute', insetInlineStart: 34, top: 34, fontFamily: HEAD, fontWeight: 800, fontSize: 48, color}}>{title}</div>
    <div style={{position: 'absolute', insetInlineStart: 34, top: 112, fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.ink}}>{sub}</div>
  </div>;
};
const List: React.FC<{y: number; d: number; items: [string, string][]; color: string; start?: number; step?: number}> = ({y, d, items, color, start = 0.05, step = 0.14}) => {
  const f = useCurrentFrame();
  return <>{items.map(([k, t], i) => <div key={i} style={{position: 'absolute', left: 64, width: 952, top: y + i * 118, display: 'flex', alignItems: 'center', gap: 22, background: '#fff', borderRadius: 22, padding: '18px 24px', boxSizing: 'border-box', borderLeft: `10px solid ${color}`, opacity: ease(f, fr(d, start + i * step), fr(d, start + i * step) + 10)}}>
    <Icon k={k} s={54} c={color} /><span style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.ink, lineHeight: 1.2}}>{t}</span></div>)}</>;
};
const Stamp: React.FC<{y: number; at: number; color: string; bg: string; text: string}> = ({y, at, color, bg, text}) =>
  <Card x={64} y={y} w={952} at={at} style={{background: bg, border: `4px solid ${color}`, textAlign: 'center'}}>
    <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 46, color}}>{text}</div>
  </Card>;

const S01: React.FC<{d: number}> = ({d}) => <>
  <Band y={480} at={fr(d, 0.45)} color={RED} bg="#FDECEC" title="101" sub="اتصلوا فورًا" />
  <Band y={710} at={fr(d, 0.58)} color={ORG} bg="#FFF7ED" title="قسم الطوارئ" sub="فورًا" />
  <Band y={940} at={fr(d, 0.72)} color={BLU} bg="#fff" title="في اليوم نفسه" sub="إلى الطبيب أو القسم" />
</>;
const S02: React.FC<{d: number}> = ({d}) => <>
  <List y={480} d={d} color={RED} items={[['lungs', 'ضيق نفس مفاجئ'], ['heart', 'ألم في الصدر'], ['drop', 'سعال مع دم'], ['faint', 'فقدان الوعي · تشنّجات · ارتباك مفاجئ'], ['wound', 'نزيف من الجرح لا يتوقف بالضغط']]} step={0.13} />
  <Stamp y={1110} at={fr(d, 0.82)} color={RED} bg="#FDECEC" text="اتصلوا بـ 101 فورًا" />
  <Phone101 y={1230} at={fr(d, 0.84)} s={0.72} />
</>;
const S03: React.FC<{d: number}> = ({d}) => <>
  <List y={480} d={d} color={RED} items={[['leg', 'القدم أو الساق فجأة باردة أو شاحبة أو مزرقّة'], ['leg', 'خاصةً مع ألم شديد أو خدر أو ضعف']]} step={0.12} />
  <Card x={64} y={760} w={952} at={fr(d, 0.45)} label="بعد عملية في الرقبة" style={{borderLeft: `10px solid ${RED}`}}>
    <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.ink, lineHeight: 1.3}}>تورّم الرقبة يزداد بسرعة · صعوبة التنفّس · لا يمكن بلع الريق</div>
  </Card>
  <Stamp y={1040} at={fr(d, 0.85)} color={RED} bg="#FDECEC" text="اتصلوا بـ 101 فورًا" />
</>;
const S04: React.FC<{d: number}> = ({d}) => <>
  <Card x={64} y={470} w={952} at={4} label="بعد عملية في العمود الفقري" style={{borderLeft: `10px solid ${ORG}`}}>
    <div style={{fontFamily: BODY, fontWeight: 600, fontSize: 26, color: C.mute}}>جديد أو يزداد بسرعة:</div>
  </Card>
  <List y={640} d={d} color={ORG} items={[['leg', 'ضعف أو خدر في الذراع أو الساق'], ['bladder', 'خدر: الأعضاء التناسلية، بين الساقين، حول فتحة الشرج'], ['bladder', 'لا يمكن التبوّل · فقدان السيطرة على المثانة أو الأمعاء']]} start={0.08} step={0.15} />
  <Stamp y={1030} at={fr(d, 0.62)} color={ORG} bg="#FFF7ED" text="فورًا إلى الطوارئ" />
  <div style={{position: 'absolute', left: 64, top: 1200, opacity: ease(f0(), fr(d, 0.8), fr(d, 0.88))}}><Note color={RED} bg="#FDECEC" size={28}>إذا لم تستطيعوا الوصول بأمان: 101</Note></div>
</>;
const S05: React.FC<{d: number}> = ({d}) => <>
  <List y={480} d={d} color={ORG} items={[['calf', 'ألم أو تورّم أو احمرار أو سخونة في الربلة أو الفخذ، خاصةً في جانب واحد'], ['leg', 'ألم شديد لا يزول بالمسكّنات · الساق في وضع غير معتاد']]} step={0.12} />
  <Stamp y={760} at={fr(d, 0.3)} color={ORG} bg="#FFF7ED" text="فورًا إلى الطوارئ" />
  <Card x={64} y={950} w={952} at={fr(d, 0.5)} label="بعد عملية مفصل الورك" style={{border: `4px solid ${RED}`, background: '#FDECEC'}}>
    <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.ink, lineHeight: 1.3}}>الساق أقصر أو ملتوية · ألم شديد مفاجئ · لا يمكن الدوس</div>
    <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: RED, marginTop: 12}}>لا تمشوا ولا تُرجعوا المفصل بأنفسكم ← 101</div>
  </Card>
</>;
const S06: React.FC<{d: number}> = ({d}) => {
  const f = useCurrentFrame();
  return <>
    <Card x={64} y={480} w={952} at={4} style={{display: 'flex'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 30}}>
        <Icon k="therm" s={120} c={BLU} />
        <div><div style={{direction: 'ltr', display: 'inline-block'}}><Counter from={36} to={38} a={fr(d, 0.05)} b={fr(d, 0.3)} size={110} suffix=" °C" /></div>
          <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.mute}}>حرارة 38 درجة مئوية أو أكثر · حمى مستمرة أو متكررة · قشعريرة</div></div>
      </div>
    </Card>
    <Stamp y={820} at={fr(d, 0.45)} color={BLU} bg="#fff" text="في اليوم نفسه: القسم أو الطبيب" />
    <Card x={64} y={1020} w={952} at={fr(d, 0.75)} style={{border: `4px solid ${ORG}`}}>
      <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.ink}}>إذا ساءت الحالة: اطلبوا المساعدة مهما كان الرقم</div>
    </Card>
  </>;
};
const S07: React.FC<{d: number}> = ({d}) => <>
  <List y={480} d={d} color={BLU} items={[['wound', 'احمرار وسخونة وتورّم وألم تزداد'], ['drop', 'صديد أو إفرازات غير معتادة'], ['wound', 'الضماد يبتلّ باستمرار'], ['wound', 'رائحة كريهة · حوافّ الجرح تتباعد']]} step={0.15} />
  <Stamp y={1000} at={fr(d, 0.78)} color={BLU} bg="#fff" text="فحص في اليوم نفسه" />
</>;
const S08: React.FC<{d: number}> = ({d}) => <>
  <Card x={64} y={480} w={952} at={4} label="معتاد في الأيام الأولى" style={{borderLeft: `10px solid ${C.green}`}}>
    <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 32, color: C.ink, lineHeight: 1.35}}>ألم معتدل · تورّم خفيف · كدمة حول الجرح</div>
    <div style={{fontFamily: BODY, fontWeight: 600, fontSize: 28, color: C.mute, marginTop: 10}}>تخفّ تدريجيًا</div>
  </Card>
  <Card x={64} y={800} w={952} at={fr(d, 0.6)} style={{background: C.tealL}}>
    <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 32, color: C.teal}}>إذا لم تكونوا متأكدين: اتصلوا بالقسم</div>
  </Card>
</>;
const S09: React.FC<{d: number}> = ({d}) => <>
  <CheckRow y={480} at={fr(d, 0.02)} icon="wound" text="لا تنزعوا الضماد ولا تغيّروه بأنفسكم، ما لم تُعطَوا تعليمات أخرى" />
  <CheckRow y={700} at={fr(d, 0.3)} icon="pills" text="ضد الجلطات: أقراص أو حقن بدقة حسب رسالة الخروج · لا توقفوها بأنفسكم" />
  <Card x={64} y={920} w={952} at={fr(d, 0.6)} label="الجوارب الضاغطة" style={{border: `4px solid ${ORG}`}}>
    <div style={{fontFamily: BODY, fontWeight: 700, fontSize: 30, color: C.ink}}>ألم، ضغط شديد، فقاعات، تغيّر لون الجلد ← انزعوها واتصلوا بالطاقم فورًا</div>
  </Card>
</>;
const S10: React.FC<{d: number}> = () => (
  <Card x={64} y={760} w={952} at={4} style={{borderTop: `8px solid ${C.teal}`, textAlign: 'center'}}>
    <div style={{fontFamily: HEAD, fontWeight: 800, fontSize: 44, color: C.ink, marginBottom: 18}}>هذه توصيات عامة</div>
    <div style={{fontFamily: BODY, fontWeight: 600, fontSize: 32, color: C.mute, lineHeight: 1.35}}>تعليمات طبيبكم والفريق الطبي الخاصة بكم لها الأولوية</div>
  </Card>
);
const f0 = () => useCurrentFrame();

const SC: Record<string, React.FC<{d: number}>> = {P01: S01, P02: S02, P03: S03, P04: S04, P05: S05, P06: S06, P07: S07, P08: S08, P09: S09, P10: S10};

export const Postop_ar: React.FC<{withAudio?: boolean}> = ({withAudio = true}) => {
  let at = 0;
  return (
    <AbsoluteFill style={{direction: 'rtl'}}>
      <FontCSS /><Bg />
      {TT.map((x, i) => {
        const d = Math.round((x.dur + PAD) * FPS), from = at; at += d;
        const Comp = SC[x.id];
        return <Sequence key={x.id} from={from} durationInFrames={d + (i < TT.length - 1 ? 10 : 0)}>
          <Fade d={d} last={i === TT.length - 1}>
            <Header brand={BRAND} n={i + 1} total={TT.length} label={x.label} />
            <Headline text={x.head} acc={x.acc} at={0} />
            <Comp d={d} />
            <Subtitle words={wordsOf(x.text, Math.round(x.dur * FPS))} acc={x.sacc || x.acc} />
          </Fade>
          {withAudio && x.audio && <Sequence from={4}><Audio src={staticFile(`aud/${x.audio}`)} /></Sequence>}
        </Sequence>;
      })}
    </AbsoluteFill>
  );
};

const Fade: React.FC<{d: number; last?: boolean; children: React.ReactNode}> = ({d, last, children}) => {
  const f = useCurrentFrame();
  const i = ease(f, 0, 10), o = last ? 1 : 1 - ease(f, d - 2, d + 10);
  const v = Math.min(i, o);
  return <AbsoluteFill style={{opacity: v, filter: `blur(${(1 - v) * 8}px)`}}>{children}</AbsoluteFill>;
};
