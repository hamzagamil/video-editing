# Director's notes

**Thesis (his words):** «ميسي مش بيجري أسرع من المدافع.. ميسي عايش في المستقبل».

**Angle:** a myth explained as engineering — Messi's football brain as a notebook of measurements, plans
and predictions. The image system follows: warm graph paper, graphite construction lines, a solid orange
10-dot for Messi, hollow ink dots for defenders, dashed sky lines for anything predicted.

**Length decision:** the recording is calm and slow (≈ 2 words/s). After removing every retake, lean-out
and pause > 0.20 s the speech is 216.3 s; nothing that carries a claim was dropped. Final 3:43 with the
closing verse. Pages ≈ one per 10 s, broken up by the presenter so his face returns every 4–14 s.

**Energy arc (1–5)**
```
hook  map  title scan calc future plan | secret chain 0.3s program feint thesis lag illusion trap TOUCH | equation music history sleep GENIUS founder cta verse
 3     3    4     4    4    4      4   |   4     3     3     3      4     5     4     4      4    5   |    4       3      3      3     5      4     4    5
```
Peak: G12 «تتش» (photo flash + impact + crowd). Release: the quiet G15 «بتنام في رجله», then the payoff
«ميسي دي عبقرية» on his face, then the verse.

**Hook:** face at frame 0, push 1.00 → 1.12 in 0.7 s, first caption at 0.04 s, cut to the first page on
«لاعب» (1.57 s): the player appears as the orange dot before he «looks one way and passes the other».
Alternatives considered: cutting on «بيبص» (3.3 s — too late) or opening on the title (no face, rejected).

**Earned stillness:** one held beat after «يقطع الكورة» (the heartbeat stops,
then «لكن في تتش»); 0.4 s before «ميسي مش لعيب كورة». The payoff holds one close crop (1.15) for 9 s.

**Mute test:** every page names its idea in one headline (بيبص في حتة / بيرسم خريطة / هندسة الماتريكس /
الماسح الضوئي / شايف المستقبل / خطة هندسية / الآلة المكسورة / تتش سريع / معادلة هندسية / العازف الوحيد);
presenter sections carry 1–4-word captions with one highlighted word.

**What changed from the pre-plan (because the audio wins):** no «ترمش» → the blink moment is gone; no
«تحديث» / «البوم» → the lag reads as two progress bars and the impact lands on «تتش»; «ضد مين؟» was not
said → the CTA card uses his words «فيديو جيم … NPCs» + «اكتب في الكومنتات»; the 80 % and the 0.3–0.4 s
stats became cards over the presenter so his face stays on screen; «مؤسس هندسة الماتريكس» (his ad-lib)
became a callback of the title page.

**Revision after the first render (the speaker's note: «في حاجات بكون بميل علشان اقرا الاسكريبت»):**
every presenter frame was checked for leans (face tracking on the proxy, then 15 fps strips). Seven leans
were on screen. 17 silent slivers (≤ 0.4 s, < −40 dB) left between two trimmed pauses were the frames where
he leans to the script; they are now dropped automatically (`SLIVER_MAX/SLIVER_DB`), which also removed
three one-frame black flashes the renderer produced after those tiny clips. Leans after the last word are
trimmed by hand (`TRIM`, incl. the 0.5 s hold after «سر مرعب»); leans that overlap a syllable get a held
clean frame for 0.23–0.30 s (`FREEZE`, video only); the two leans back into frame after G6 and G14 are
covered by holding those pages 0.5 s / 0.3 s longer; «عشان يفترسه» (a 0.5 s lean mid-word) is covered by a
new cut-away page (`gp-pounce`). Speech 216.3 → 212.0 s.
