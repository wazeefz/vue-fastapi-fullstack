import { defineStore } from "pinia";

export const useImageStore = defineStore("image", {
  state: () => ({
    analysisResult: null,
    loading: false,
    error: null,
  }),
  actions: {
    async uploadImage(file) {
      this.loading = true;
      this.error = null;

      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://127.0.0.1:8000/image-analytics/", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Failed to analyze image");
        }

        const data = await response.json();
        this.analysisResult = data.analysis;
      } catch (error) {
        console.error("Error uploading image:", error);
        this.error = "Image analysis failed";
      } finally {
        this.loading = false;
      }
    },
  },
});
