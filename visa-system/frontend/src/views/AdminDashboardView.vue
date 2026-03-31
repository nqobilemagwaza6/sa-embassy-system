<template>
  <div class="container py-4">
    <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
      <h2 class="mb-0 text-start">Admin Dashboard</h2>
      <button class="btn btn-outline-secondary" @click="load" :disabled="loading">
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="error" class="alert alert-danger text-start">{{ error }}</div>

    <div class="row g-3 mb-3">
      <div class="col-md-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-start">
            <div class="text-muted small">Total</div>
            <div class="fs-4 fw-bold">{{ stats.total }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-start">
            <div class="text-muted small">Approved</div>
            <div class="fs-4 fw-bold text-success">{{ stats.approved }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-start">
            <div class="text-muted small">Rejected</div>
            <div class="fs-4 fw-bold text-danger">{{ stats.rejected }}</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card border-0 shadow-sm">
          <div class="card-body text-start">
            <div class="text-muted small">Pending</div>
            <div class="fs-4 fw-bold">{{ stats.pending }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header text-start fw-bold">All Applications</div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover align-middle">
            <thead>
              <tr>
                <th>ID</th>
                <th>User</th>
                <th>Applicant</th>
                <th>Passport</th>
                <th>Documents</th>
                <th>Status</th>
                <th style="width: 340px;">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.id">
                <td>{{ app.id }}</td>
                <td>{{ app.user?.username }}</td>
                <td>{{ app.full_name }}</td>
                <td>{{ app.passport_number }}</td>
                <td>
                  <details>
                    <summary class="small">
                      {{ (app.documents && app.documents.length) ? (app.documents.length + ' file(s)') : 'No files' }}
                    </summary>
                    <ul v-if="app.documents && app.documents.length" class="mt-2">
                      <li v-for="d in app.documents" :key="d.id">
                        <span class="badge bg-light text-dark border me-2">{{ d.doc_type }}</span>
                        <a :href="d.file" target="_blank" rel="noopener">View / Download</a>
                      </li>
                    </ul>
                  </details>
                </td>
                <td>
                  <span class="badge" :class="statusBadge(app.status)">{{ humanStatus(app.status) }}</span>
                </td>
                <td>
                  <div class="d-flex flex-wrap gap-2">
                    <select v-model="adminEdit[app.id].status" class="form-select form-select-sm" style="max-width: 160px;">
                      <option value="PENDING">Pending</option>
                      <option value="UNDER_REVIEW">Under Review</option>
                      <option value="APPROVED">Approved</option>
                      <option value="REJECTED">Rejected</option>
                    </select>
                    <input
                      v-model.trim="adminEdit[app.id].comment"
                      class="form-control form-control-sm"
                      placeholder="Comment (reason, notes...)"
                      style="max-width: 220px;"
                    />
                    <button class="btn btn-sm btn-success" @click="save(app.id)" :disabled="adminEdit[app.id].loading">
                      {{ adminEdit[app.id].loading ? 'Saving...' : 'Update' }}
                    </button>
                  </div>
                  <div v-if="adminEdit[app.id].error" class="text-danger small mt-1">
                    {{ adminEdit[app.id].error }}
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
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
      adminEdit: {},
      stats: { total: 0, approved: 0, rejected: 0, pending: 0 },
      loading: false,
      error: ''
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
    ensureRow (app) {
      if (!this.adminEdit[app.id]) {
        const row = { status: app.status, comment: app.admin_comment || '', loading: false, error: '' }
        this.$set ? this.$set(this.adminEdit, app.id, row) : (this.adminEdit[app.id] = row)
      }
    },
    computeStats () {
      const s = { total: this.applications.length, approved: 0, rejected: 0, pending: 0, under_review: 0 }
      for (const a of this.applications) {
        if (a.status === 'APPROVED') s.approved++
        else if (a.status === 'REJECTED') s.rejected++
        else if (a.status === 'UNDER_REVIEW') s.under_review++
        else s.pending++
      }
      this.stats = { total: s.total, approved: s.approved, rejected: s.rejected, pending: s.pending }
    },
    async load () {
      this.error = ''
      this.loading = true
      try {
        const res = await fetch('http://127.0.0.1:8000/api/applications/', {
          headers: { ...this.authHeaders() }
        })
        const apps = await res.json()
        if (!res.ok) throw new Error((apps && apps.detail) || 'Failed to load applications (admin)')
        this.applications = apps
        this.applications.forEach(a => this.ensureRow(a))
        this.computeStats()
      } catch (e) {
        this.error = e.message || 'Failed to load admin data'
      } finally {
        this.loading = false
      }
    },
    async save (id) {
      const row = this.adminEdit[id]
      row.loading = true
      row.error = ''
      try {
        if (row.status === 'REJECTED' && !row.comment) {
          row.error = 'Comment is required when rejecting.'
          return
        }
        const res = await fetch(`http://127.0.0.1:8000/api/applications/${id}/admin-status/`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json', ...this.authHeaders() },
          body: JSON.stringify({ status: row.status, comment: row.comment })
        })
        const updated = await res.json()
        if (!res.ok) throw new Error((updated && updated.detail) || JSON.stringify(updated) || 'Update failed')
        this.applications = this.applications.map(a => (a.id === id ? updated : a))
        this.computeStats()
      } catch (e) {
        row.error = e.message || 'Update failed'
      } finally {
        row.loading = false
      }
    }
  },
  mounted () {
    this.load()
  }
}
</script>
