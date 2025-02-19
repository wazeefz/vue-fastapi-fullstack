<script setup>
import { ref } from "vue";
import { useImageStore } from "@/stores/imageAnalyticsStore";

const imageStore = useImageStore();
const fileInput = ref(null);

const handleUpload = async () => {
  if (fileInput.value.files.length === 0) {
    alert("Please select an image");
    return;
  }

  const file = fileInput.value.files[0];
  await imageStore.uploadImage(file);
};
</script>

<template>
  <div>
    <input type="file" ref="fileInput" accept="image/jpeg, image/png" />
    <button @click="handleUpload" :disabled="imageStore.loading">
      Upload Image
    </button>

    <div v-if="imageStore.loading">Processing...</div>
    <div v-if="imageStore.error" class="error">{{ imageStore.error }}</div>
    <div v-if="imageStore.analysisResult">
      <h3>Analysis Result:</h3>
      <p>{{ imageStore.analysisResult }}</p>
    </div>
  </div>
</template>

<style scoped>
.error {
  color: red;
}
</style>
