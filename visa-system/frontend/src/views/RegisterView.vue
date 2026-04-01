<template>
  <div class="container py-4" style="max-width: 520px;">
    <h2 class="mb-3 text-start">Register</h2>

    <div v-if="error" class="alert alert-danger text-start">{{ error }}</div>

    <form @submit.prevent="onSubmit" class="card card-body text-start">
      <label class="form-label">Username</label>
      <input v-model.trim="username" class="form-control mb-3" autocomplete="username" required />

      <label class="form-label">Email (optional)</label>
      <input v-model.trim="email" type="email" class="form-control mb-3" autocomplete="email" />

      <label class="form-label">Password</label>
      <input v-model="password" type="password" class="form-control mb-3" autocomplete="new-password" required />

      <button class="btn btn-success" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create account' }}
      </button>

      <div class="mt-3">
        <router-link to="/login">Already have an account?</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      email: '',
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
        const res = await fetch('http://127.0.0.1:8000/api/auth/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, email: this.email, password: this.password })
        })
        const data = await res.json()
        if (!res.ok) throw new Error((data && data.detail) || JSON.stringify(data) || 'Registration failed')
        localStorage.setItem('token', data.token)
        localStorage.setItem('is_superuser', '0')
        window.dispatchEvent(new Event('auth-changed'))
        this.$router.push('/dashboard')
      } catch (e) {
        this.error = e.message || 'Registration failed'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
