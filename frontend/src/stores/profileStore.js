import { defineStore } from "pinia";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    profiles: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchProfiles() {
      this.loading = true;
      try {
        const response = await fetch("http://127.0.0.1:8000/profiles/");
        const data = await response.json();
        this.profiles = data;
        this.error = null;
      } catch (error) {
        console.error("Error fetching profiles:", error);
        this.error = "Failed to fetch profiles";
      } finally {
        this.loading = false;
      }
    },
  },
});
