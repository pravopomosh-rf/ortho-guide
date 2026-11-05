import React from 'react';
import {useCurrentFrame, interpolate, Easing} from 'remotion';
import {C, font} from './ui';

type P = {x: number; y: number};
const L = 46; // thigh = shin
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const lp = (a: P, b: P, t: number): P => ({x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t)});
const io = (t: number) => Easing.inOut(Easing.cubic)(Math.max(0, Math.min(1, t)));

// knee by two-segment IK, knee bends forward (+dir)
const knee = (h: P, f: P, dir = 1): P => {
  const dx = f.x - h.x, dy = f.y - h.y;
  const d = Math.min(Math.hypot(dx, dy), 2 * L - 0.01);
  const a = Math.atan2(dy, dx);
  const b = Math.acos(d / (2 * L));
  const ang = a - dir * b;
  return {x: h.x + L * Math.cos(ang), y: h.y + L * Math.sin(ang)};
};

type K = {t: number; hip: P; fh: P; fo: P; tip: P};
const at = (ks: K[], t: number, liftKey: 'fh' | 'fo' | 'tip' | null = null) => {
  let i = 0;
  while (i < ks.length - 2 && t > ks[i + 1].t) i++;
  const a = ks[i], b = ks[i + 1];
  const p = io((t - a.t) / (b.t - a.t));
  const lift = (k: 'fh' | 'fo' | 'tip') => (a[k].x !== b[k].x || a[k].y !== b[k].y ? Math.sin(Math.PI * p) * 18 : 0);
  return {
    hip: lp(a.hip, b.hip, p),
    fh: {...lp(a.fh, b.fh, p), y: lerp(a.fh.y, b.fh.y, p) - lift('fh')},
    fo: {...lp(a.fo, b.fo, p), y: lerp(a.fo.y, b.fo.y, p) - lift('fo')},
    tip: {...lp(a.tip, b.tip, p), y: lerp(a.tip.y, b.tip.y, p) - lift('tip')},
  };
};

const Figure: React.FC<{hip: P; fh: P; fo: P; tip?: P; dir?: number; aid?: 'crutch' | 'walker'}> = ({hip, fh, fo, tip, dir = 1, aid}) => {
  const sh = {x: hip.x + dir * 6, y: hip.y - 58};
  const hand = aid === 'walker' && tip ? {x: tip.x - dir * 26, y: hip.y - 10} : tip ? {x: lerp(sh.x, tip.x, 0.55), y: hip.y - 4} : {x: sh.x + dir * 10, y: hip.y};
  const kh = knee(hip, fh, dir), ko = knee(hip, fo, dir);
  const leg = (k: P, f: P, c: string) => (
    <>
      <path d={`M${hip.x} ${hip.y} L${k.x} ${k.y} L${f.x} ${f.y}`} stroke={c} strokeWidth={11} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={`M${f.x - 2} ${f.y} L${f.x + dir * 14} ${f.y}`} stroke={c} strokeWidth={9} strokeLinecap="round" />
    </>
  );
  return (
    <g>
      {leg(kh, fh, C.teal)}
      {leg(ko, fo, C.dawn)}
      <path d={`M${hip.x} ${hip.y} L${sh.x} ${sh.y}`} stroke={C.teal} strokeWidth={14} strokeLinecap="round" />
      <circle cx={sh.x + dir * 4} cy={sh.y - 20} r={13} fill={C.teal} />
      {aid === 'crutch' && tip && (
        <path d={`M${hand.x} ${hand.y - 22} L${tip.x} ${tip.y} M${hand.x - 7} ${hand.y - 22} L${hand.x + 7} ${hand.y - 22}`} stroke="#7f8a96" strokeWidth={5} strokeLinecap="round" />
      )}
      {aid === 'walker' && tip && (
        <path d={`M${tip.x - dir * 30} ${hip.y - 10} L${tip.x + dir * 2} ${hip.y - 10} M${tip.x - dir * 28} ${hip.y - 10} L${tip.x - dir * 30} ${tip.y} M${tip.x} ${hip.y - 10} L${tip.x + dir * 2} ${tip.y}`} stroke="#7f8a96" strokeWidth={5} strokeLinecap="round" fill="none" />
      )}
      <path d={`M${sh.x} ${sh.y + 4} L${hand.x} ${hand.y}`} stroke={C.teal} strokeWidth={9} strokeLinecap="round" />
    </g>
  );
};

/** Animated stairs: climbs up (healthy first), then walks down (crutch + operated first). */
export const StairClimb: React.FC<{upFrom: number; upTo: number; downFrom: number; downTo: number; w?: number; h?: number}> = ({upFrom, upTo, downFrom, downTo, w = 520, h = 340}) => {
  const f = useCurrentFrame();
  const W = 90, H = 44, X0 = 40, B = 320, N = 4;
  const foot = (k: number, off = 0): P => ({x: X0 + k * W + W / 2 + off, y: B - k * H});
  const stand = (k: number, off = 0): P => ({x: X0 + k * W + W / 2 - 4 + off, y: B - k * H - 2 * L * 0.97});
  const ksUp: K[] = [];
  for (let k = 0; k < N - 1; k++) {
    const t0 = k / (N - 1), dt = 1 / (N - 1);
    ksUp.push({t: t0, hip: stand(k), fh: foot(k, 6), fo: foot(k, -8), tip: foot(k, -22)});
    ksUp.push({t: t0 + dt * 0.35, hip: stand(k, 12), fh: foot(k + 1, 0), fo: foot(k, -8), tip: foot(k, -22)});
    ksUp.push({t: t0 + dt * 0.7, hip: stand(k + 1, -10), fh: foot(k + 1, 0), fo: foot(k, -8), tip: foot(k, -22)});
  }
  ksUp.push({t: 1, hip: stand(N - 1), fh: foot(N - 1, 6), fo: foot(N - 1, -8), tip: foot(N - 1, -22)});
  // down: facing left
  const ksDn: K[] = [];
  for (let k = N - 1; k > 0; k--) {
    const t0 = (N - 1 - k) / (N - 1), dt = 1 / (N - 1);
    ksDn.push({t: t0, hip: stand(k, 4), fh: foot(k, 8), fo: foot(k, -6), tip: foot(k, -24)});
    ksDn.push({t: t0 + dt * 0.3, hip: stand(k, 0), fh: foot(k, 8), fo: foot(k, -6), tip: foot(k - 1, 20)});
    ksDn.push({t: t0 + dt * 0.65, hip: stand(k - 1, 30), fh: foot(k, 8), fo: foot(k - 1, 6), tip: foot(k - 1, 20)});
  }
  ksDn.push({t: 1, hip: stand(0, 4), fh: foot(0, 8), fo: foot(0, -6), tip: foot(0, -24)});
  const goingDown = f >= downFrom;
  const t = goingDown ? (f - downFrom) / (downTo - downFrom) : (f - upFrom) / (upTo - upFrom);
  const s = at(goingDown ? ksDn : ksUp, Math.max(0, Math.min(1, t)));
  let path = `M0 ${B}`;
  for (let k = 0; k < N; k++) path += ` L${X0 + k * W} ${B - k * H} L${X0 + (k + 1) * W} ${B - k * H}`;
  path += ` L${w} ${B - (N - 1) * H}`;
  const label = goingDown ? 'Вниз: костыль → оперированная' : 'Вверх: сначала здоровая';
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <path d={`M${X0 + W / 2} ${B - 100} L${X0 + (N - 0.5) * W} ${B - (N - 1) * H - 100}`} stroke={C.mute} strokeWidth={5} strokeLinecap="round" />
      <path d={path} stroke={C.ink} strokeWidth={5} fill="none" />
      <Figure hip={s.hip} fh={s.fh} fo={s.fo} tip={s.tip} dir={goingDown ? -1 : 1} aid="crutch" />
      <text x={12} y={28} fontFamily={font} fontWeight={800} fontSize={20} fill={goingDown ? '#b8661c' : C.teal}>{label}</text>
    </svg>
  );
};

/** Walking with a walker on flat ground: walker → operated leg → healthy leg, looped. */
export const WalkerWalk: React.FC<{from?: number; cycle?: number; w?: number; h?: number}> = ({from = 0, cycle = 45, w = 420, h = 230}) => {
  const f = Math.max(0, useCurrentFrame() - from);
  const S = 34, G = h - 14;
  const n = Math.floor(f / cycle), p = (f % cycle) / cycle;
  const base = 70 + (n % 6) * S;
  const fade = n % 6 === 5 ? 1 - p : 1;
  const ks: K[] = [
    {t: 0, hip: {x: base, y: G - 2 * L * 0.97}, fh: {x: base + 4, y: G}, fo: {x: base - 6, y: G}, tip: {x: base + 64, y: G}},
    {t: 0.3, hip: {x: base + 6, y: G - 2 * L * 0.96}, fh: {x: base + 4, y: G}, fo: {x: base - 6, y: G}, tip: {x: base + 64 + S, y: G}},
    {t: 0.62, hip: {x: base + 20, y: G - 2 * L * 0.96}, fh: {x: base + 4, y: G}, fo: {x: base - 6 + S, y: G}, tip: {x: base + 64 + S, y: G}},
    {t: 1, hip: {x: base + S, y: G - 2 * L * 0.97}, fh: {x: base + 4 + S, y: G}, fo: {x: base - 6 + S, y: G}, tip: {x: base + 64 + S, y: G}},
  ];
  const s = at(ks, p);
  const step = p < 0.3 ? 'ходунки' : p < 0.62 ? 'оперированная нога' : 'здоровая нога';
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`}>
      <path d={`M10 ${G + 4} L${w - 10} ${G + 4}`} stroke={C.mute} strokeWidth={4} strokeLinecap="round" />
      <g opacity={fade}><Figure hip={s.hip} fh={s.fh} fo={s.fo} tip={s.tip} aid="walker" /></g>
      <text x={w - 12} y={26} textAnchor="end" fontFamily={font} fontWeight={800} fontSize={19} fill={p >= 0.3 && p < 0.62 ? '#b8661c' : C.teal}>{step}</text>
    </svg>
  );
};

/** Slow camera push for static scenes. */
export const usePush = (d: number, amt = 0.04) => {
  const f = useCurrentFrame();
  return 1 + amt * interpolate(f, [0, d], [0, 1], {extrapolateRight: 'clamp'});
};
