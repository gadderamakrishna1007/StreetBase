

import streamlit as st
import streamlit.components.v1 as components
import html
from textwrap import dedent
import urllib.parse

TESTIMONIALS = [
    {
        "name": "Ananya Reddy",
        "location": "Hyderabad",
        "rating": 5,
        "message": "The prediction tool delivered highly accurate estimates and made comparing prices simple.",
        # data-uri SVG placeholder (square)
        "image_url": "data:image/svg+xml;utf8," + urllib.parse.quote(
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
            '<rect width="100%" height="100%" rx="18" fill="#0ea5e9"/>'
            '<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="72" fill="white">AR</text>'
            '</svg>'
        )
    },
    {
        "name": "Rohit Sharma",
        "location": "Mumbai",
        "rating": 5,
        "message": "Clear, confident estimates that matched market quotes I saw offline.",
        "image_url": "data:image/svg+xml;utf8," + urllib.parse.quote(
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
            '<rect width="100%" height="100%" rx="18" fill="#7c3aed"/>'
            '<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="64" fill="white">RS</text>'
            '</svg>'
        )
    },
    {
        "name": "Karthik Iyer",
        "location": "Chennai",
        "rating": 3,
        "message": "Professional and precise — simplified decision making for my property search.",
        "image_url": "data:image/svg+xml;utf8," + urllib.parse.quote(
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
            '<rect width="100%" height="100%" rx="18" fill="#06b6d4"/>'
            '<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="64" fill="white">KI</text>'
            '</svg>'
        )
    },
    {
        "name": "Simran Kaur",
        "location": "New Delhi",
        "rating": 5,
        "message": "Reliable estimates and a professional experience overall.",
        "image_url": "data:image/svg+xml;utf8," + urllib.parse.quote(
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
            '<rect width="100%" height="100%" rx="18" fill="#f97316"/>'
            '<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="64" fill="white">SK</text>'
            '</svg>'
        )
    },
    {
        "name": "Vikram Singh",
        "location": "Bangalore",
        "rating": 3,
        "message": "Accurate and well-presented — helped me compare options fast.",
        "image_url": "data:image/svg+xml;utf8," + urllib.parse.quote(
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
            '<rect width="100%" height="100%" rx="18" fill="#60a5fa"/>'
            '<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="64" fill="white">VS</text>'
            '</svg>'
        )
    },
    {
        "name": "Neha Menon",
        "location": "Kochi",
        "rating": 5,
        "message": "Complete and efficient — trustworthy estimates and quick responses.",
        "image_url": "data:image/svg+xml;utf8," + urllib.parse.quote(
            '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">'
            '<rect width="100%" height="100%" rx="18" fill="#90a6fa"/>'
            '<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="64" fill="white">NM</text>'
            '</svg>'
        )
    }
]

def esc(s: str) -> str:
    # """Escape text for HTML insertion."""
    return html.escape(s or "")

def build_cards_html(testimonials):
    cards = []
    for t in testimonials:
        name = esc(t["name"])
        location = esc(t["location"])
        msg = esc(t["message"])
        rating = int(t.get("rating", 5))

        img = t.get("image_url", "")
        if img.startswith("/mnt") or img.startswith("file:/"):
            image_html = f'''
                <div class="thumb media-thumb">
                    <video src="{esc(img)}" playsinline muted loop preload="metadata"></video>
                </div>
            '''
        else:
            image_html = f'''
                <div class="thumb">
                    <img src="{esc(img)}" alt="{name}" />
                </div>
            '''
        stars = "★" * rating
        card_html = f'''
            <div class="carousel-card">
                {image_html}
                <div class="card-body">
                    <div class="card-title">{name}</div>
                    <div class="card-sub">{location} · <span class="stars">{stars}</span></div>
                    <div class="card-msg">"{msg}"</div>
                </div>
            </div>
        '''
        cards.append(card_html)
    return "\n".join(cards)

def render_testimonials(height=380, autoplay_interval=3000):
    cards_html = build_cards_html(TESTIMONIALS)
    template = dedent("""
    <style>
    :root{
        --bg: #f8fafc;
        --card-bg: #ffffff;
        --muted: #6b7280;
        --accent: #0f172a;
        --shadow: 0 20px 40px rgba(12, 18, 30, 0.08);
    }
    .carousel-root{
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        width: 100%;
        display:flex;
        justify-content:center;
        padding: 18px 8px;
        box-sizing: border-box;
        background: transparent;
    }

    .carousel-viewport{
        width: min(1200px, 96%); /* NEW → wider panel */
        position: relative;
        overflow: visible;
    }


    .carousel-track{
        display:flex;
        gap: 20px;
        padding: 24px 84px; /* allow peek */
        box-sizing: border-box;
        align-items: center;
        scroll-behavior: smooth;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }

    /* Hide scrollbar but allow dragging */
    .carousel-track::-webkit-scrollbar { height: 8px; }
    .carousel-track::-webkit-scrollbar-thumb {
        background: rgba(12,18,30,0.08);
        border-radius:999px;
    }

    .carousel-card{
        flex: 0 0 360px;
        min-width: 360px;
        background: var(--card-bg);
        border-radius: 16px;
        box-shadow: var(--shadow);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform-origin: center;
        transition: transform 420ms cubic-bezier(.2,.9,.27,1), box-shadow 280ms ease, opacity 280ms ease;
        height: 230px; /* NEW → compact height */
    }


    /* Thumb (square image at top) */
    .thumb{
        width: 100%;
        height: 130px; /* NEW → compact thumbnail */
        display:flex;
        align-items:center;
        justify-content:center;
        overflow:hidden;
    }

    .thumb img, .thumb video{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display:block;
    }
    .media-thumb {
        background: #eef2ff;
    }
    .card-body{
        padding: 12px 16px 16px 16px; /* NEW */
        display:flex;
        flex-direction:column;
        gap:6px; /* NEW */
    }


    .card-title{
        font-size: 16px;
        font-weight: 700;
        color: var(--accent);
    }
    .card-sub{
        font-size: 13px;
        color: var(--muted);
    }
    .card-msg{
        margin-top: 4px; /* NEW */
        font-size: 13.5px; /* NEW */
        color: #0f172a;
        line-height:1.35; /* NEW */
    }


    /* Center emphasis: scale the centered card and slightly dim others */
    .carousel-track .carousel-card {
        opacity: 0.85;
        transform: scale(0.98);
    }
    .carousel-track .carousel-card.center {
        opacity: 1;
        transform: scale(1.03);
        box-shadow: 0 30px 60px rgba(12,18,30,0.12);
    }

    /* Arrows */
    .nav-btn {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 56px;
        height: 56px;
        border-radius: 14px;
        background: rgba(255,255,255,0.9);
        display:flex;
        align-items:center;
        justify-content:center;
        box-shadow: 0 10px 30px rgba(12,18,30,0.06);
        cursor:pointer;
        transition: transform 140ms ease, opacity 140ms ease;
        z-index: 40;
    }
    .nav-btn:hover { transform: translateY(-50%) scale(1.03); }
    .nav-left { left: 10px; }
    .nav-right { right: 10px; }

    .nav-btn svg { width: 20px; height: 20px; color: var(--accent); }

    /* Responsive */
    @media (max-width: 880px){
        .carousel-track { padding: 12px 28px; gap: 12px; }
        .carousel-card { flex: 0 0 80%; min-width: 80%; }
        .nav-btn { display:none; }
    }
    </style>

    <div class="carousel-root">
      <div class="carousel-viewport" role="region" aria-label="Testimonials carousel">
        <div class="nav-btn nav-left" id="navLeft" title="Previous">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </div>

        <div id="track" class="carousel-track" tabindex="0" aria-live="polite">
            {CARDS}
        </div>

        <div class="nav-btn nav-right" id="navRight" title="Next">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </div>
      </div>
    </div>

    <script>
    (function(){
      const track = document.getElementById('track');
      const left = document.getElementById('navLeft');
      const right = document.getElementById('navRight');

      // Convert HTMLCollection to array for convenience
      function cardsArray(){ return Array.from(track.querySelectorAll('.carousel-card')); }

      // Scroll amount equals card width + gap (approx)
      function scrollAmount(){
        const first = track.querySelector('.carousel-card');
        if(!first) return 360;
        const style = window.getComputedStyle(first);
        // fallback gap measured as difference
        const gap = 20;
        return Math.round(first.offsetWidth + gap);
      }

      // center tracking logic
      function updateCenterClass(){
        const cards = cardsArray();
        const trackRect = track.getBoundingClientRect();
        const centerX = trackRect.left + trackRect.width / 2;
        let closest = null;
        let minDist = Infinity;
        cards.forEach(c => {
          const r = c.getBoundingClientRect();
          const cx = r.left + r.width/2;
          const d = Math.abs(cx - centerX);
          if(d < minDist){ minDist = d; closest = c; }
        });
        cards.forEach(c => c.classList.remove('center'));
        if(closest) closest.classList.add('center');
      }

      // snap to nearest card on scroll end
      let isScrolling;
      track.addEventListener('scroll', () => {
        window.clearTimeout(isScrolling);
        updateCenterClass();
        isScrolling = setTimeout(() => {
          const card = track.querySelector('.carousel-card.center');
          if(card){
            const cardRect = card.getBoundingClientRect();
            const trackRect = track.getBoundingClientRect();
            const offset = (cardRect.left + cardRect.width/2) - (trackRect.left + trackRect.width/2);
            // scroll by the offset to center it
            track.scrollBy({ left: offset, behavior: 'smooth' });
          }
        }, 120);
      });

      // navigation
      left.addEventListener('click', () => {
        track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
      });
      right.addEventListener('click', () => {
        track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
      });

      // keyboard
      track.addEventListener('keydown', (e) => {
        if(e.key === 'ArrowLeft'){ track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' }); }
        if(e.key === 'ArrowRight'){ track.scrollBy({ left: scrollAmount(), behavior: 'smooth' }); }
      });

      // touch swipe (lightweight)
      let touchStartX = 0;
      track.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, {passive:true});
      track.addEventListener('touchend', (e) => {
        const dx = (e.changedTouches[0].clientX - touchStartX);
        if(Math.abs(dx) > 40){
          if(dx < 0) track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
          else track.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
        }
      }, {passive:true});

      // autoplay controls
      let autoplayInterval = {INTERVAL_MS};
      let autoplayTimer = null;
      function startAutoplay(){
        stopAutoplay();
        autoplayTimer = setInterval(() => {
          // scroll to next card
          track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
        }, autoplayInterval);
      }
      function stopAutoplay(){
        if(autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; }
      }

      // pause on hover & focus
      track.addEventListener('mouseenter', stopAutoplay);
      track.addEventListener('mouseleave', startAutoplay);
      track.addEventListener('focusin', stopAutoplay);
      track.addEventListener('focusout', startAutoplay);

      // init
      updateCenterClass();
      // small delay to ensure layout computed
      setTimeout(() => { updateCenterClass(); startAutoplay(); }, 350);

      // ensure center class updates on resize
      window.addEventListener('resize', () => { updateCenterClass(); });
    })();
    </script>
    """)

    html_output = template.replace("{CARDS}", cards_html).replace("{INTERVAL_MS}", str(autoplay_interval))

    components.html(html_output, height=height, scrolling=True)

# if __name__ == "__main__":
#     # st.set_page_config(page_title="Testimonials", layout="centered")
#     # st.markdown("## Testimonials")
#     st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
#     st.markdown("<div style='height:420px'></div>", unsafe_allow_html=True)

#     render_testimonials(height=420, autoplay_interval=3000)

#     st.caption("Auto-play pauses on hover/focus. Replace the local file path in the testimonials list if you want a hosted image.")
