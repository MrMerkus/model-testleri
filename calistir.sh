#!/usr/bin/env bash
# Kullanım: calistir.sh <model-klasörü> [görev...]
# Modelin üç görevini sırayla çalıştırır; her görev kendi klasöründe, süre ve çıktı kaydıyla.
# Modeller: sonnet-5.5 opus-4.6 sonnet-4.6 gemini-3.8-flash gemini-3.1-pro space-bunny
set -u
KOK="$(cd "$(dirname "$0")" && pwd -P)"
model="$1"; shift
gorevler=("${@:-1-turkce-metin 2-mayin-tarlasi 3-hata-avi}")
gorevler=(${gorevler[@]})
SURE=1500  # görev başına en fazla 25 dakika

ISTEM='Bu klasördeki EMIR.md dosyasını oku ve oradaki görevi baştan sona kendin yap. Soru sorma, onay bekleme; belirsiz bir yer varsa makul olanı seç ve RAPOR.md içinde yaz. Yalnız bu klasörde çalış. Python için `python3`, testler için `python3 -m pytest` kullan.'

export BEYIN_INVOKED_BY=model-testi          # hafıza hook'ları bu oturumları saymaz
export PATH="$KOK/.venv/bin:$PATH"            # pytest bu sanal ortamdan gelir

calistir_bunny() {  # anonim sağlayıcı: bwrap içinde, yalnız kendi klasörüne yazabilir
  local d="$1" gizle=() k
  for k in Documents Masaüstü .ssh .claude .codex .gnupg .config; do
    [ -d "$HOME/$k" ] && gizle+=(--tmpfs "$HOME/$k")   # olmayan klasör örtülemez
  done
  timeout $SURE bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp "${gizle[@]}" \
    --bind "$HOME/.omp" "$HOME/.omp" \
    --ro-bind "$KOK/.venv" "$KOK/.venv" \
    --ro-bind "$KOK/bunny-kilit.yml" /tmp/bunny-kilit.yml \
    --bind "$d" "$d" --chdir "$d" --die-with-parent \
    omp -p --no-session --auto-approve --config /tmp/bunny-kilit.yml \
      --model openrouter/stealth/space-bunny-alpha:medium --cwd "$d" "$ISTEM"
}

for g in "${gorevler[@]}"; do
  d="$KOK/$model/$g"
  if grep -qP "^$model\t$g\t\d+\t0$" "$KOK/_sureler.tsv" 2>/dev/null; then echo "$model / $g zaten bitmiş, atlandı"; continue; fi
  if [ -e "$d/_calisma.log" ] && ! grep -qP "^$model\t$g\t" "$KOK/_sureler.tsv" 2>/dev/null; then echo "$model / $g şu an çalışıyor, atlandı"; continue; fi
  mkdir -p "$d"
  cp -n "$KOK/_gorevler/$g/"*.* "$d/"
  bas=$(date +%s)
  echo "[$(date +%T)] $model / $g başladı"
  (
    cd "$d" || exit 1
    case "$model" in
      sonnet-5.5)
        timeout $SURE claude -p "$ISTEM" --model claude-sonnet-5-5 --strict-mcp-config \
          --allowedTools "Read,Write,Edit,Glob,Grep,Bash(python3:*),Bash(ls:*),Bash(cat:*)" ;;
      opus-4.6)         timeout $SURE agy --model claude-opus-4-6-thinking --sandbox --dangerously-skip-permissions --output-format text -p="$ISTEM" ;;
      sonnet-4.6)       timeout $SURE agy --model claude-sonnet-4-6        --sandbox --dangerously-skip-permissions --output-format text -p="$ISTEM" ;;
      gemini-3.8-flash) timeout $SURE agy --model gemini-3.8-flash-high    --sandbox --dangerously-skip-permissions --output-format text -p="$ISTEM" ;;
      gemini-3.1-pro)   timeout $SURE agy --model gemini-3.1-pro-high      --sandbox --dangerously-skip-permissions --output-format text -p="$ISTEM" ;;
      space-bunny)      calistir_bunny "$d" ;;
      *) echo "bilinmeyen model: $model"; exit 1 ;;
    esac
  ) < /dev/null > "$d/_calisma.log" 2>&1
  kod=$?
  sure=$(( $(date +%s) - bas ))
  printf '%s\t%s\t%s\t%s\n' "$model" "$g" "$sure" "$kod" >> "$KOK/_sureler.tsv"
  echo "[$(date +%T)] $model / $g bitti: ${sure}s, çıkış $kod"
done
