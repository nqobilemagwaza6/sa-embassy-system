<template>
  <div class="container mt-5">
    <h2>Apply for a Visa</h2>
    <form @submit.prevent="submitApplication">
      <input v-model="full_name" placeholder="Full Name" class="form-control mb-2" />
      <input v-model="passport_number" placeholder="Passport Number" class="form-control mb-2" />
      <input v-model="nationality" placeholder="Nationality" class="form-control mb-2" />
      <input v-model="destination_country" placeholder="Destination Country" class="form-control mb-2" />
      <input v-model="travel_date" type="date" class="form-control mb-2" />
      <input type="file" @change="handleFileUpload" class="form-control mb-2" />
      <button type="submit" class="btn btn-success">Submit Application</button>
    </form>

    <h3 class="mt-4">Your Applications</h3>
    <ul class="list-group">
      <li v-for="app in applications" :key="app.id" class="list-group-item">
        {{ app.full_name }} - <span :class="statusClass(app.status)">{{ app.status }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data () {
    return {
      full_name: '',
      passport_number: '',
      nationality: '',
      destination_country: '',
      travel_date: '',
      file: null,
      applications: []
    }
  },
  methods: {
    fetchApplications () {
      fetch('http://127.0.0.1:8000/api/applications/')
        .then(res => res.json())
        .then(data => {
          this.applications = data
        })
    },
    handleFileUpload (e) {
      this.file = e.target.files[0]
    },
    submitApplication () {
      const formData = new FormData()
      formData.append('full_name', this.full_name)
      formData.append('passport_number', this.passport_number)
      formData.append('nationality', this.nationality)
      formData.append('destination_country', this.destination_country)
      formData.append('travel_date', this.travel_date)
      // Application is created first; documents are uploaded separately

      fetch('http://127.0.0.1:8000/api/applications/', {
        method: 'POST',
        body: JSON.stringify({
          full_name: this.full_name,
          passport_number: this.passport_number,
          nationality: this.nationality,
          destination_country: this.destination_country,
          travel_date: this.travel_date
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(res => res.json())
        .then(data => {
          this.applications.push(data)
          this.full_name = ''
          this.passport_number = ''
          this.nationality = ''
          this.destination_country = ''
          this.travel_date = ''
          this.file = null
        })
    },
    statusClass (status) {
      if (status === 'APPROVED') return 'text-success'
      if (status === 'REJECTED') return 'text-danger'
      if (status === 'UNDER_REVIEW') return 'text-warning'
      return ''
    }
  },
  mounted () {
    this.fetchApplications()
  }
}
</script>
