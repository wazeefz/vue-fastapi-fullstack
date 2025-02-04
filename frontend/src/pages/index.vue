<template>
  <v-container>
    <v-card>
      <v-card-title>
        Profiles
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="profileStore.profiles"
        :search="search"
        :loading="profileStore.loading"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:item.is_active="{ value }">
          <v-chip :color="value ? 'success' : 'error'">
            {{ value ? "Active" : "Inactive" }}
          </v-chip>
        </template>
      </v-data-table>
      <v-alert v-if="profileStore.error" type="error" class="mt-4">
        {{ profileStore.error }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { useProfileStore } from "@/stores/profileStore";
import { onMounted } from "vue";

const seacrh = ref("");
const profileStore = useProfileStore();

const headers = [
  { title: "Name", key: "name" },
  { title: "Age", key: "age" },
  { title: "Email", key: "email" },
  { title: "Marital Status", key: "marital_status" },
  { title: "Country", key: "country" },
  { title: "State", key: "state" },
  { title: "Status", key: "is_active" },
];

onMounted(() => {
  profileStore.fetchProfiles();
});
</script>
