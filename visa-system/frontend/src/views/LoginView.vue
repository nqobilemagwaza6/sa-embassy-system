<template>
  <div class="container py-4" style="max-width: 520px;">
    <h2 class="mb-3 text-start">Login</h2>

    <div v-if="error" class="alert alert-danger text-start">{{ error }}</div>

    <form @submit.prevent="onSubmit" class="card card-body text-start">
      <label class="form-label">Username</label>
      <input v-model.trim="username" class="form-control mb-3" autocomplete="username" required />

      <label class="form-label">Password</label>
      <input v-model="password" type="password" class="form-control mb-3" autocomplete="current-password" required />

      <button class="btn btn-success" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Login' }}
      </button>

      <div class="mt-3">
        <router-link to="/register">Create an account</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: '',
      loading: false,
      error: ''
    }
  },
  methods: {
    async onSubmit () {
      this.error = ''
      this.loading = true
      try {
        const res = await fetch('http://127.0.0.1:8000/api/auth/login/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password })
        })
        const data = await res.json()
        if (!res.ok) throw new Error((data && data.detail) || 'Login failed')
        localStorage.setItem('token', data.token)

        const meRes = await fetch('http://127.0.0.1:8000/api/auth/me/', {
          headers: { Authorization: `Token ${data.token}` }
        })
        const me = await meRes.json()
        let superuser = false
        if (meRes.ok) {
          superuser = !!me.is_superuser
          localStorage.setItem('is_superuser', superuser ? '1' : '0')
        }

        window.dispatchEvent(new Event('auth-changed'))
        this.$router.push(superuser ? '/admin' : '/dashboard')
      } catch (e) {
        this.error = e.message || 'Login failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
