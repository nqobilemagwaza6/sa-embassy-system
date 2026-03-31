<template>
  <div class="container mt-5">
    <h2>Visa Applications</h2>

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Name</th>
          <th>Passport</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="app in applications" :key="app.id">
          <td>{{ app.full_name }}</td>
          <td>{{ app.passport_number }}</td>
          <td>{{ app.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      applications: []
    }
  },
  mounted () {
    fetch('http://127.0.0.1:8000/api/applications/')
      .then(res => res.json())
      .then(data => {
        this.applications = data
      })
  }
}
</script>
