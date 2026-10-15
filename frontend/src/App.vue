<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import Button from "primevue/button";
type Incident = { id: number; title: string; status: string; priority: string; assigneeName: string | null };
const incidents = ref<Incident[]>([]);
const error = ref("");
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" });
async function load() {
  try { incidents.value = (await api.get<Incident[]>("/api/incidents")).data; error.value = ""; }
  catch { error.value = "Could not load incidents. Check that the backend is running."; }
}
async function resolve(id: number) {
  try { await api.patch(`/api/incidents/${id}/status`, { status: "RESOLVED" }); await load(); }
  catch { error.value = "Could not update incident."; }
}
onMounted(load);
</script>
<template>
  <main>
    <header><p class="eyebrow">OPERATIONS / INCIDENTS</p><h1>Enterprise Operations Portal</h1><p>Track and resolve IT incidents</p></header>
    <p v-if="error" role="alert" class="error">{{ error }}</p>
    <section><h2>Incident queue</h2>
      <DataTable :value="incidents" stripedRows paginator :rows="10">
        <Column field="id" header="ID" />
        <Column field="title" header="Incident" />
        <Column field="priority" header="Priority" />
        <Column field="status" header="Status" />
        <Column field="assigneeName" header="Assigned to" />
        <Column header="Action"><template #body="{ data }"><Button label="Resolve" size="small" :disabled="data.status === 'RESOLVED'" @click="resolve(data.id)" /></template></Column>
      </DataTable>
    </section>
  </main>
</template>
<style>
*{box-sizing:border-box}body{margin:0;background:#f5f7fb;color:#172033;font-family:Inter,Arial,sans-serif}main{max-width:1150px;margin:auto;padding:40px 24px}header{margin-bottom:30px}.eyebrow{color:#4267a4;font-size:12px;letter-spacing:2px;font-weight:700}h1{font-size:32px;margin:8px 0}header>p:last-child{color:#64748b}section{background:white;border-radius:14px;padding:24px;box-shadow:0 4px 24px #1720330b}h2{margin:0 0 20px}.error{color:#b42318}
</style>
