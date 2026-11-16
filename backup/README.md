# Резервная копия сайта ortho-guide
- Полная копия (все ветки, вся история): D:\Downloadsinsta_channel\ortho-guide_backup\ortho-guide_full_2026-11-16.bundle.part00–06 (+ SHA256SUMS, КАК_ВОССТАНОВИТЬ_САЙТ.txt); папка синхронизируется с Google Диском.
- refs_<дата>.txt — состояние всех веток на момент копии. Еженедельная добавка строится от ПОСЛЕДНЕГО refs_*.txt:
  git clone --mirror https://github.com/pravopomosh-rf/ortho-guide m.git; cd m.git
  git bundle create ortho-guide_inc_<дата>.bundle --branches --tags --not $(cut -d' ' -f1 ../refs_<прошлая>.txt)
  (если «empty bundle» — изменений нет). Затем новый refs_<дата>.txt сюда, bundle → D:\...\ortho-guide_backup\weekly\ (части ≤350 МБ, SendUserFile → device_commit_files по одному файлу).
- Раз в ~2 месяца или когда добавок > 10: сделать новую полную копию, старую полную и добавки — в Корзину.
