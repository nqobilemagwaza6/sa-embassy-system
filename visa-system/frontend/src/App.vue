<template>
  <nav class="navbar navbar-expand-lg navbar-dark sa-navbar shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold d-flex align-items-center gap-2" :to="brandTo">
        <span class="nav-logo" aria-hidden="true">
          <svg viewBox="0 0 32 32" width="28" height="28">
            <rect x="3" y="5" width="26" height="22" rx="5" fill="#f7d54a" />
            <rect x="5" y="7" width="22" height="18" rx="3" fill="#0b6b3a" />
            <path d="M10 16h12M10 20h8" stroke="#f7d54a" stroke-width="2" stroke-linecap="round" />
          </svg>
        </span>
        Visa Tracker SA
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="nav" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li v-if="!hasToken" class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li v-if="hasToken && !isSuperuser" class="nav-item">
            <router-link class="nav-link" to="/dashboard">My Dashboard</router-link>
          </li>
          <li v-if="hasToken && isSuperuser" class="nav-item">
            <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
          </li>
        </ul>

        <div class="d-flex gap-2 flex-wrap align-items-center">
          <template v-if="!hasToken">
            <router-link class="btn btn-outline-light btn-sm" to="/login">Login</router-link>
            <router-link class="btn btn-warning btn-sm fw-semibold" to="/register">Register</router-link>
          </template>
          <button v-else class="btn btn-outline-light btn-sm" type="button" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>

  <main :class="mainClass">
    <router-view/>
  </main>
</template>

<script>
export default {
  data () {
    return {
      hasToken: !!localStorage.getItem('token'),
      isSuperuser: localStorage.getItem('is_superuser') === '1'
    }
  },
  computed: {
    brandTo () {
      if (!this.hasToken) return '/'
      return this.isSuperuser ? '/admin' : '/dashboard'
    },
    mainClass () {
      const isLanding = this.$route && this.$route.name === 'landing'
      return isLanding ? 'main-landing' : 'bg-light main-app'
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('token')
      localStorage.removeItem('is_superuser')
      window.dispatchEvent(new Event('auth-changed'))
      this.$router.push('/')
    }
  },
  mounted () {
    this._onAuthChanged = () => {
      this.hasToken = !!localStorage.getItem('token')
      this.isSuperuser = localStorage.getItem('is_superuser') === '1'
    }
    window.addEventListener('auth-changed', this._onAuthChanged)
  },
  beforeUnmount () {
    window.removeEventListener('auth-changed', this._onAuthChanged)
  }
}
</script>

<style>
#app {
  font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.sa-navbar {
  background: linear-gradient(90deg, #064a28, #0b6b3a 55%, #0a5a32);
}

.nav-logo {
  display: inline-flex;
  align-items: center;
}

.main-app {
  min-height: calc(100vh - 56px);
}

.main-landing {
  min-height: calc(100vh - 56px);
}
</style>
