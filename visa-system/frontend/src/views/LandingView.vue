<template>
  <div class="landing">
    <!-- Hero -->
    <section class="hero text-white">
      <div class="hero-pattern" aria-hidden="true" />
      <div class="container position-relative py-5">
        <div class="row align-items-center g-5">
          <div class="col-lg-6 text-lg-start text-center">
            <div class="d-inline-flex align-items-center gap-3 mb-4 justify-content-lg-start justify-content-center w-100">
              <div class="logo-mark shadow-lg" aria-hidden="true">
                <svg viewBox="0 0 64 64" width="48" height="48" role="img" aria-label="Visa Tracker logo">
                  <defs>
                    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#f7d54a" />
                      <stop offset="100%" style="stop-color:#e6b422" />
                    </linearGradient>
                  </defs>
                  <rect x="6" y="10" width="52" height="44" rx="10" fill="#0b6b3a" />
                  <path d="M18 28h28M18 36h18" stroke="url(#g1)" stroke-width="4" stroke-linecap="round" />
                  <circle cx="46" cy="38" r="8" fill="url(#g1)" opacity="0.95" />
                </svg>
              </div>
              <div class="text-start">
                <div class="brand-title">Visa Tracker SA</div>
                <div class="brand-sub text-white-50 small">Transparency for every application</div>
              </div>
            </div>
            <h1 class="display-5 fw-bold mb-3 hero-heading">
              Track your visa application with clarity — not guesswork.
            </h1>
            <p class="lead text-white-75 mb-4">
              Submit documents, follow status changes in near real-time, and get clear notifications when your case moves
              forward.
            </p>
            <div class="d-flex flex-wrap gap-3 justify-content-lg-start justify-content-center">
              <router-link to="/register" class="btn btn-warning btn-lg px-4 fw-semibold shadow-sm">
                Get started
              </router-link>
              <router-link to="/login" class="btn btn-outline-light btn-lg px-4">
                Sign in
              </router-link>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-card card border-0 shadow-lg">
              <div class="card-body p-4 p-md-5 text-start">
                <div class="d-flex align-items-center gap-2 mb-3">
                  <span class="badge rounded-pill sa-badge-green">Live status</span>
                  <span class="badge rounded-pill sa-badge-gold">Secure uploads</span>
                </div>
                <h2 class="h4 fw-bold mb-3 text-dark">How it works</h2>
                <ol class="steps text-muted mb-0">
                  <li><strong class="text-dark">Register</strong> — create your account in seconds.</li>
                  <li><strong class="text-dark">Apply &amp; upload</strong> — passport, ID, and supporting files.</li>
                  <li><strong class="text-dark">Track</strong> — pending, under review, approved, or rejected — with history.</li>
                </ol>
                <hr class="my-4" />
                <div class="d-flex align-items-center gap-3">
                  <div class="mini-logo bg-success bg-opacity-10 rounded-3 p-2" aria-hidden="true">
                    <svg width="36" height="36" viewBox="0 0 48 48">
                      <path fill="#0b6b3a" d="M24 4L6 14v14c0 11 8 18 18 20 10-2 18-9 18-20V14L24 4z" />
                      <path fill="#f7d54a" d="M24 16l-6 6h4v8h4v-8h4l-6-6z" />
                    </svg>
                  </div>
                  <div class="small text-muted">
                    Built with <strong class="text-dark">Django</strong> + <strong class="text-dark">Vue</strong> + <strong class="text-dark">SQLite</strong> — a clean stack for learning and demos.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Strip -->
    <section class="py-4 sa-strip border-bottom">
      <div class="container">
        <div class="row g-3 text-center text-md-start">
          <div class="col-md-4">
            <div class="fw-bold text-success">Green · Gold · Neutral</div>
            <div class="small text-muted">South Africa–inspired palette, kept professional.</div>
          </div>
          <div class="col-md-4">
            <div class="fw-bold text-dark">For applicants</div>
            <div class="small text-muted">Your dashboard updates as your case progresses.</div>
          </div>
          <div class="col-md-4">
            <div class="fw-bold text-dark">For administrators</div>
            <div class="small text-muted">Superuser console to review, comment, and set status.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-5">
      <div class="container">
        <h2 class="text-center fw-bold mb-5">Everything you need in one place</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card h-100 p-4 rounded-4 border bg-white shadow-sm">
              <div class="icon-wrap mb-3" aria-hidden="true">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M8 6h12M8 10h12M8 14h8M8 18h8" stroke="#0b6b3a" stroke-width="2" stroke-linecap="round"/><rect x="3" y="4" width="3" height="16" rx="1" fill="#f7d54a"/></svg>
              </div>
              <h3 class="h5 fw-bold">Apply online</h3>
              <p class="text-muted small mb-0">Structured visa application fields with instant confirmation.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card h-100 p-4 rounded-4 border bg-white shadow-sm">
              <div class="icon-wrap mb-3" aria-hidden="true">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M12 4v12a4 4 0 1 0 4-4H8a4 4 0 1 0 4 4" stroke="#0b6b3a" stroke-width="2" stroke-linecap="round"/><circle cx="8" cy="18" r="2" fill="#f7d54a"/></svg>
              </div>
              <h3 class="h5 fw-bold">Document vault</h3>
              <p class="text-muted small mb-0">Upload passport, ID, and more — visible on your application timeline.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card h-100 p-4 rounded-4 border bg-white shadow-sm">
              <div class="icon-wrap mb-3" aria-hidden="true">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M6 16v-4a6 6 0 1 1 12 0v4l2 2H4l2-2z" stroke="#0b6b3a" stroke-width="2" fill="none"/><circle cx="18" cy="5" r="3" fill="#f7d54a"/></svg>
              </div>
              <h3 class="h5 fw-bold">Smart notifications</h3>
              <p class="text-muted small mb-0">Clear messages when your status becomes under review, approved, or rejected.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-5 sa-cta text-white text-center">
      <div class="container py-4">
        <h2 class="fw-bold mb-3">Ready to stop waiting in the dark?</h2>
        <p class="mb-4 text-white-75 mx-auto" style="max-width: 520px;">
          Create an account and submit your first application in minutes.
        </p>
        <router-link to="/register" class="btn btn-warning btn-lg fw-semibold px-5 shadow">
          Start your application
        </router-link>
      </div>
    </section>

    <footer class="py-4 border-top bg-white small text-muted text-center">
      <div class="container d-flex flex-wrap justify-content-center align-items-center gap-3">
        <span class="d-inline-flex align-items-center gap-2">
          <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true"><path fill="#0b6b3a" d="M24 4L6 14v14c0 11 8 18 18 20 10-2 18-9 18-20V14L24 4z"/></svg>
          Visa Tracker SA · Demo project
        </span>
      </div>
    </footer>
  </div>
</template>

<script>
export default { name: 'LandingView' }
</script>

<style scoped>
.landing { background: #f6f8fb; }
.hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #064a28 0%, #0b6b3a 45%, #0d5430 100%);
}
.hero-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.12;
  background-image:
    radial-gradient(circle at 20% 30%, #fff 1px, transparent 1px),
    radial-gradient(circle at 80% 70%, #f7d54a 1px, transparent 1px);
  background-size: 48px 48px, 64px 64px;
}
.hero-heading { letter-spacing: -0.02em; }
.text-white-75 { color: rgba(255, 255, 255, 0.82) !important; }
.logo-mark {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 10px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.brand-title { font-weight: 800; font-size: 1.15rem; letter-spacing: 0.02em; }
.hero-card { border-radius: 1.25rem; }
.sa-badge-green { background: #0b6b3a; color: #fff; }
.sa-badge-gold { background: #f7d54a; color: #1a1a1a; }
.steps li { margin-bottom: 0.65rem; }
.steps {
  padding-left: 1.1rem;
}
.sa-strip { background: #fff; }
.feature-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(11, 107, 58, 0.12) !important;
}
.icon-wrap { font-size: 1.75rem; }
.sa-cta {
  background: linear-gradient(90deg, #0b6b3a, #0a5c32 50%, #084422);
}
</style>
