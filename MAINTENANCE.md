# 🛠️ Guia de Manutenção — Pega Carlos!

Documento de referência para manter e evoluir o jogo. Tudo vive em um único
arquivo (`index.html`), sem build, sem dependências, sem framework.

- **Repositório:** https://github.com/marcelueda/pega-carlos
- **Jogo no ar:** https://marcelueda.github.io/pega-carlos/ (GitHub Pages, branch `master`)

---

## 📁 Estrutura de arquivos

| Arquivo | Vai pro GitHub? | Descrição |
|---|---|---|
| `index.html` | ✅ | O jogo inteiro (HTML + CSS + JS num arquivo só) |
| `carlos_face.png` | ✅ | Rosto do Carlos recortado em círculo (256×256, usado no jogo) |
| `emerson_face.png` | ✅ | Rosto do Emerson recortado em círculo (256×256, usado no jogo) |
| `README.md` | ✅ | Apresentação do projeto |
| `MAINTENANCE.md` | ✅ | Este guia |
| `tools/generate_faces.py` | ✅ | Script que gera os `*_face.png` a partir das fotos originais |
| `carlos.png` / `emerson.jpeg` | ❌ (no `.gitignore`) | Fotos originais — só existem localmente, não são necessárias para rodar |
| `.claude/` | ❌ | Config local de preview (ignorado) |

> O jogo **só carrega** `carlos_face.png` e `emerson_face.png`. As fotos originais
> servem apenas para regenerar os recortes (ver seção "Trocar os rostos").

---

## 🧩 Como o código está organizado (dentro de `index.html`)

O `<script>` está dividido em blocos comentados, nesta ordem:

1. **Setup do canvas** — `cv`, `ctx`, `resize()`, `DPR`.
2. **`save` / `persist()`** — progresso salvo em `localStorage` (chave `pegaCarlos.v1`):
   moedas, fantasias compradas, fantasia equipada, mudo, recorde.
3. **`COSTUMES`** — objeto com todas as fantasias (nome, preço, cores, acessórios).
4. **`FACE` + `drawFace()`** — carrega as fotos reais e desenha o rosto recortado
   em círculo na cabeça. `drawDizzyStars()` = estrelinhas de tontura.
5. **`Audio`** — módulo de som: efeitos gerados via **Web Audio API** (`tone`, `noise`)
   e a voz do grito via **SpeechSynthesis** (`Audio.speak`).
6. **Câmera** — `cam`, `w2s()` (mundo→tela), `updateCamera()` (segue o Carlos).
7. **Estado do jogo** — `player`, `participants`, `game`, `particles`, `floatTexts`.
8. **`spawnParticipants(n)`** — cria de 6 a 12 Emersons com comportamentos variados.
9. **Input** — joystick virtual (`joyZone`), botões `sprint`/`scream`, teclado (WASD/setas/espaço).
10. **Ações** — `doScream()`, `transformMonster()`.
11. **Efeitos** — `spawnBurst()`, `floatText()`, `showCombo()`, `showScream()`, `narrate()`.
12. **`update(dt)`** — lógica do quadro: movimento, IA dos Emersons, colisões, timer.
13. **`capture(p)`** — captura um Emerson: pontos, combo, moedas, dispara transformação.
14. **Render** — `drawField()`, `drawFence()`, `drawLights()`, `drawEmerson()`,
    `drawHead()` (rosto desenhado, usado como *fallback*), `drawCarlos()`.
15. **HUD** — `syncHud()`.
16. **Loop principal** — `loop()` com `requestAnimationFrame` e delta-time.
17. **Telas e fluxo** — `showScreen()`, `startGame()`, `endGame()`.
18. **Loja** — `buildShop()`, `drawCostumePreview()`.

---

## 🎚️ Ajustes rápidos (onde mexer)

| Quero mudar... | Onde | Valor atual |
|---|---|---|
| Tempo da partida | `startGame()` → `game={ time:60, ...}` | 60 s |
| Nº de participantes | `startGame()` → `const n = 6 + ...` | 6 a 12 |
| Velocidade do Carlos | objeto `player` → `speed` | 300 (370 no monstro) |
| Frase do grito | const `SCREAM_LINE` | "Corre mais, está correndo pouco, vaiii!!" |
| Dificuldade (sobe a cada captura) | `capture()` → `game.difficulty = 1 + ...` | +5% por captura |
| Cooldown do grito | `doScream()` → `game.screamCooldown = 6` | 6 s |
| Preços/cores das fantasias | objeto `COSTUMES` | — |
| Velocidades por tipo (fast/juke/clumsy) | `spawnParticipants()` → `baseSpeed` | 180–255 |

---

## 🖼️ Trocar os rostos (Carlos ou Emerson)

Os rostos são recortes circulares das fotos. Para gerar de novo (ou trocar a foto):

1. Coloque a foto nova na pasta (ex.: `carlos.png` ou `emerson.jpeg`).
2. Ajuste as coordenadas de recorte em `tools/generate_faces.py` (formato
   `(esquerda, topo, direita, base)` em pixels da foto original).
3. Rode:
   ```powershell
   python tools/generate_faces.py
   ```
   Isso regenera `carlos_face.png` / `emerson_face.png`.
4. Commit + push (ver abaixo) para publicar.

> Dica: para achar as coordenadas, abra a foto e veja onde fica o rosto.
> O recorte deve ser ~quadrado, do topo do cabelo até o queixo.

Se as imagens não carregarem, o jogo usa automaticamente o **rosto desenhado**
(`drawHead()`) como fallback — então o jogo nunca quebra.

---

## 🚀 Publicar uma atualização

Depois de editar qualquer coisa:

```powershell
cd C:\temp\jogo
git add -A
git commit -m "descreva a mudança aqui"
git push
```

O GitHub Pages reconstrói sozinho em ~1 minuto. O link continua o mesmo:
**https://marcelueda.github.io/pega-carlos/**

Verificar se o build terminou:
```powershell
& "C:\Program Files\GitHub CLI\gh.exe" api repos/marcelueda/pega-carlos/pages/builds/latest --jq .status
```
(`built` = no ar; `building` = aguarde)

---

## 🧪 Rodar e testar localmente

Abrir via servidor local (recomendado — `file://` pode bloquear as imagens):

```powershell
cd C:\temp\jogo
node -e "const h=require('http'),f=require('fs'),p=require('path');h.createServer((q,s)=>{let x=p.join(process.cwd(),q.url==='/'?'index.html':decodeURIComponent(q.url.slice(1)));f.readFile(x,(e,d)=>{s.writeHead(e?404:200);s.end(d||'404')})}).listen(8000,()=>console.log('http://localhost:8000'))"
```

Acesse `http://localhost:8000`. No celular (mesma rede Wi-Fi): `http://SEU-IP:8000`.

---

## ⚠️ Observações técnicas

- **Áudio/voz no mobile:** só toca após o 1º toque na tela (política dos navegadores).
  O jogo chama `Audio.init()` no primeiro toque — já tratado.
- **Voz do grito:** usa a voz pt-BR do sistema; se o aparelho não tiver, usa a padrão.
- **60 FPS:** o loop usa delta-time e cap de `dt` (0,05 s) para não "teleportar" após travadas.
- **Performance:** tudo é desenhado em Canvas 2D; nada de DOM por entidade. Escala com `DPR` (cap em 2).
- **Sem analytics, sem backend, sem cookies.** Progresso fica só no `localStorage` do aparelho.
