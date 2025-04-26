<template>
  <div v-if="show" class="modal-overlay" @click.self="cancel">
    <div class="modal-content delete-confirm-modal">
      <h2>确认删除</h2>
      <p>你确定要永久删除以下食物条目吗？此操作无法撤销。</p>
      <p v-if="itemName || itemId" class="item-to-delete-info">
        <strong v-if="itemId">ID:</strong> {{ itemId }}<br v-if="itemId && itemName"/>
        <strong v-if="itemName">名称:</strong> {{ itemName }}
      </p>
      <div class="modal-actions">
        <button @click="confirm" class="delete-confirm-button">确认删除</button>
        <button @click="cancel" class="cancel-button">取消</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

// Props definition
defineProps({
  show: {
    type: Boolean,
    required: true
  },
  itemName: {
    type: String,
    default: ''
  },
  itemId: {
    type: [String, Number], // Can be string or number ID
    default: null
  }
});

// Emits definition
const emit = defineEmits(['confirm', 'cancel']);

// Methods to emit events
const confirm = () => {
  emit('confirm');
};

const cancel = () => {
  emit('cancel');
};
</script>

<style scoped>
/* Reusing modal styles but scoped to this component */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050; /* Ensure it's above other elements if needed */
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 450px; /* Slightly smaller for confirmation */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-content h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
  font-size: 20px;
}

.delete-confirm-modal p {
  margin-bottom: 15px;
  line-height: 1.6;
  color: #34495e;
}

.item-to-delete-info {
  background-color: #f8f9fa;
  padding: 10px 15px;
  border-radius: 4px;
  border: 1px solid #eee;
  margin-bottom: 20px;
  color: #555;
}

.item-to-delete-info strong {
  margin-right: 5px;
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
  gap: 10px;
}

.delete-confirm-button, .cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.delete-confirm-button {
  background-color: #e74c3c; /* Red color */
  color: white;
}

.delete-confirm-button:hover {
  background-color: #c0392b; /* Darker red */
}

.cancel-button {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

.cancel-button:hover {
  background-color: #dfe6e9;
}
</style> 