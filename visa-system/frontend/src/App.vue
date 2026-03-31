<template>
  <nav class="navbar navbar-expand-lg navbar-dark sa-navbar">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/dashboard">Visa Tracker</router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div id="nav" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/dashboard">My Dashboard</router-link>
          </li>
          <li v-if="isSuperuser" class="nav-item">
            <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
          </li>
        </ul>

        <div class="d-flex gap-2">
          <router-link v-if="!hasToken" class="btn btn-outline-light btn-sm" to="/login">Login</router-link>
          <router-link v-if="!hasToken" class="btn btn-warning btn-sm" to="/register">Register</router-link>
          <button v-if="hasToken" class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>

  <main class="bg-light" style="min-height: calc(100vh - 56px);">
    <router-view/>
  </main>
</template>

<script>
export default {
  computed: {
    hasToken () {
      return !!localStorage.getItem('token')
    },
    isSuperuser () {
      return localStorage.getItem('is_superuser') === '1'
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('token')
      localStorage.removeItem('is_superuser')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.sa-navbar {
  background: #0b6b3a; /* SA-inspired green */
}
</style>
