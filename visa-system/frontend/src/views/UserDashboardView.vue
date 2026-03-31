<template>
  <div class="container py-4">
    <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
      <h2 class="mb-0 text-start">My Visa Applications</h2>
      <button class="btn btn-outline-secondary" @click="loadAll" :disabled="loading">
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="error" class="alert alert-danger text-start">{{ error }}</div>

    <div class="row g-3">
      <div class="col-lg-5">
        <div class="card">
          <div class="card-header text-start fw-bold">Apply for a Visa</div>
          <div class="card-body text-start">
            <form @submit.prevent="submitApplication">
              <label class="form-label">Full name</label>
              <input v-model.trim="form.full_name" class="form-control mb-2" required />

              <label class="form-label">Passport number</label>
              <input v-model.trim="form.passport_number" class="form-control mb-2" required />

              <label class="form-label">Nationality</label>
              <input v-model.trim="form.nationality" class="form-control mb-2" required />

              <label class="form-label">Destination country</label>
              <input v-model.trim="form.destination_country" class="form-control mb-2" required />

              <label class="form-label">Travel date</label>
              <input v-model="form.travel_date" type="date" class="form-control mb-3" required />

              <button class="btn btn-success" :disabled="saving">
                {{ saving ? 'Submitting...' : 'Submit application' }}
              </button>
            </form>
          </div>
        </div>

        <div class="card mt-3">
          <div class="card-header text-start fw-bold">Notifications</div>
          <div class="card-body text-start">
            <div v-if="notifications.length === 0" class="text-muted">No notifications yet.</div>
            <div v-for="n in notifications" :key="n.id" class="border rounded p-2 mb-2">
              <div class="small text-muted">{{ formatDate(n.created_at) }}</div>
              <div :class="n.is_read ? 'text-muted' : ''">{{ n.message }}</div>
              <button v-if="!n.is_read" class="btn btn-sm btn-outline-secondary mt-2" @click="markRead(n.id)">
                Mark read
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-7">
        <div class="card">
          <div class="card-header text-start fw-bold">Applications</div>
          <div class="card-body">
            <div v-if="applications.length === 0" class="text-start text-muted">
              You have no applications yet. Submit one on the left.
            </div>

            <div v-for="app in applications" :key="app.id" class="border rounded p-3 mb-3 text-start">
              <div class="d-flex flex-wrap align-items-center justify-content-between gap-2">
                <div class="fw-bold">{{ app.full_name }}</div>
                <span class="badge" :class="statusBadge(app.status)">{{ humanStatus(app.status) }}</span>
              </div>

              <div class="mt-2 small text-muted">
                Passport: {{ app.passport_number }} • Destination: {{ app.destination_country }} • Travel: {{ app.travel_date }}
              </div>

              <div v-if="app.admin_comment" class="mt-2 alert alert-warning mb-2">
                <div class="fw-bold">Admin comment</div>
                <div>{{ app.admin_comment }}</div>
              </div>

              <details class="mt-2">
                <summary class="fw-bold">Upload documents</summary>
                <div class="mt-2">
                  <div class="small text-muted mb-1">Uploaded documents</div>
                  <div v-if="!app.documents || app.documents.length === 0" class="text-muted">
                    No documents uploaded yet.
                  </div>
                  <ul v-else class="mb-2">
                    <li v-for="d in app.documents" :key="d.id">
                      <span class="badge bg-light text-dark border me-2">{{ d.doc_type }}</span>
                      <a :href="d.file" target="_blank" rel="noopener">View / Download</a>
                      <span class="small text-muted"> ({{ formatDate(d.uploaded_at) }})</span>
                    </li>
                  </ul>
                </div>
                <div class="row g-2 mt-2">
                  <div class="col-md-4">
                    <select v-model="docForm[app.id].doc_type" class="form-select">
                      <option value="PASSPORT">Passport</option>
                      <option value="ID">ID</option>
                      <option value="OTHER">Other</option>
                    </select>
                  </div>
                  <div class="col-md-8">
                    <input type="file" class="form-control" @change="onPickFile(app.id, $event)" />
                  </div>
                </div>
                <button class="btn btn-sm btn-success mt-2" @click="upload(app.id)" :disabled="docForm[app.id].loading">
                  {{ docForm[app.id].loading ? 'Uploading...' : 'Upload' }}
                </button>
                <div v-if="docForm[app.id].error" class="text-danger mt-2">{{ docForm[app.id].error }}</div>
              </details>

              <details class="mt-2" @toggle="maybeLoadEvents(app)">
                <summary class="fw-bold">Status history</summary>
                <div v-if="events[app.id] && events[app.id].length === 0" class="text-muted mt-2">
                  No status history yet.
                </div>
                <ul v-if="events[app.id] && events[app.id].length" class="mt-2">
                  <li v-for="ev in events[app.id]" :key="ev.id">
                    <span class="small text-muted">{{ formatDate(ev.created_at) }}</span>
                    — {{ humanStatus(ev.from_status) }} → {{ humanStatus(ev.to_status) }}
                    <span v-if="ev.comment"> ({{ ev.comment }})</span>
                  </li>
                </ul>
              </details>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      applications: [],
      notifications: [],
      events: {},
      loading: false,
      saving: false,
      error: '',
      form: {
        full_name: '',
        passport_number: '',
        nationality: '',
        destination_country: '',
        travel_date: ''
      },
      docForm: {}
    }
  },
  methods: {
    authHeaders () {
      const token = localStorage.getItem('token')
      return token ? { Authorization: `Token ${token}` } : {}
    },
    formatDate (iso) {
      try { return new Date(iso).toLocaleString() } catch { return iso }
    },
    humanStatus (s) {
      return (s || '').replaceAll('_', ' ').toLowerCase().replace(/(^|\\s)\\S/g, (t) => t.toUpperCase())
    },
    statusBadge (s) {
      if (s === 'APPROVED') return 'bg-success'
      if (s === 'REJECTED') return 'bg-danger'
      if (s === 'UNDER_REVIEW') return 'bg-warning text-dark'
      return 'bg-secondary'
    },
    ensureDocForm (appId) {
      if (!this.docForm[appId]) {
        this.$set
          ? this.$set(this.docForm, appId, { doc_type: 'PASSPORT', file: null, loading: false, error: '' })
          : (this.docForm[appId] = { doc_type: 'PASSPORT', file: null, loading: false, error: '' })
      }
    },
    async loadAll () {
      this.error = ''
      this.loading = true
      try {
        const [appsRes, notifsRes] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/applications/', { headers: { ...this.authHeaders() } }),
          fetch('http://127.0.0.1:8000/api/notifications/', { headers: { ...this.authHeaders() } })
        ])
        const apps = await appsRes.json()
        const notifs = await notifsRes.json()
        if (!appsRes.ok) throw new Error((apps && apps.detail) || 'Failed to load applications')
        if (!notifsRes.ok) throw new Error((notifs && notifs.detail) || 'Failed to load notifications')
        this.applications = apps
        this.notifications = notifs
        this.applications.forEach(a => this.ensureDocForm(a.id))
      } catch (e) {
        this.error = e.message || 'Failed to load data'
      } finally {
        this.loading = false
      }
    },
    async submitApplication () {
      this.error = ''
      this.saving = true
      try {
        const res = await fetch('http://127.0.0.1:8000/api/applications/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...this.authHeaders() },
          body: JSON.stringify(this.form)
        })
        const created = await res.json()
        if (!res.ok) throw new Error((created && created.detail) || JSON.stringify(created) || 'Failed to submit')
        this.applications = [created, ...this.applications]
        this.ensureDocForm(created.id)
        this.form = { full_name: '', passport_number: '', nationality: '', destination_country: '', travel_date: '' }
      } catch (e) {
        this.error = e.message || 'Failed to submit'
      } finally {
        this.saving = false
      }
    },
    onPickFile (appId, e) {
      this.ensureDocForm(appId)
      this.docForm[appId].file = e.target.files && e.target.files[0]
      this.docForm[appId].error = ''
    },
    async upload (appId) {
      this.ensureDocForm(appId)
      const state = this.docForm[appId]
      if (!state.file) {
        state.error = 'Please choose a file first.'
        return
      }
      state.loading = true
      state.error = ''
      try {
        const fd = new FormData()
        fd.append('doc_type', state.doc_type)
        fd.append('file', state.file)
        const res = await fetch(`http://127.0.0.1:8000/api/applications/${appId}/documents/`, {
          method: 'POST',
          headers: { ...this.authHeaders() },
          body: fd
        })
        const data = await res.json()
        if (!res.ok) throw new Error((data && data.detail) || JSON.stringify(data) || 'Upload failed')
        state.file = null
        await this.loadAll()
      } catch (e) {
        state.error = e.message || 'Upload failed'
      } finally {
        state.loading = false
      }
    },
    async maybeLoadEvents (app) {
      const appId = app.id
      if (this.events[appId]) return
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/applications/${appId}/status-events/`, {
          headers: { ...this.authHeaders() }
        })
        const evs = await res.json()
        if (!res.ok) throw new Error((evs && evs.detail) || 'Failed to load history')
        this.$set ? this.$set(this.events, appId, evs) : (this.events[appId] = evs)
      } catch (e) {
        this.$set ? this.$set(this.events, appId, []) : (this.events[appId] = [])
      }
    },
    async markRead (id) {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/notifications/${id}/mark-read/`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json', ...this.authHeaders() },
          body: JSON.stringify({})
        })
        const updated = await res.json()
        if (!res.ok) throw new Error((updated && updated.detail) || 'Failed to mark read')
        this.notifications = this.notifications.map(n => (n.id === id ? updated : n))
      } catch {}
    }
  },
  mounted () {
    this.loadAll()
  }
}
</script>
