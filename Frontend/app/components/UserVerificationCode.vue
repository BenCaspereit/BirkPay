<template>
  <div class="w-full max-w-md mx-auto">
    <div class="bg-white rounded-2xl shadow-xl shadow-gray-200/50 border border-gray-100 p-8">
      <!-- Icon -->
      <div class="w-16 h-16 bg-gray-900 rounded-2xl flex items-center justify-center mx-auto mb-6 transform transition-transform duration-300 hover:scale-110 hover:rotate-12">
        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
        </svg>
      </div>

      <!-- Header -->
      <div class="text-center mb-8">
        <p class="text-2xl font-bold text-gray-900 mb-2">{{ $t('verification.title') }}</p>
        <p class="text-sm text-gray-500">{{ $t('verification.subtitle') }}</p>
        <p class="text-sm text-gray-500">{{ $t('verification.form') }}</p>
      </div>

      <!-- Form -->
      <form class="space-y-6" @submit.prevent="handleSubmit">
        <div class="flex justify-center gap-2 sm:gap-3">
          <input
            v-for="(digit, index) in code"
            :key="index"
            :ref="el => inputRefs[index] = el"
            v-model="code[index]"
            type="text"
            maxlength="1"
            pattern="[0-9]"
            inputmode="numeric"
            class="w-11 h-12 sm:w-12 sm:h-14 text-center text-xl font-bold text-gray-900 bg-gray-50 border-2 border-gray-200 rounded-xl focus:border-gray-900 focus:bg-white focus:outline-none focus:ring-4 focus:ring-gray-900/10 transition-all duration-200 hover:border-gray-300 placeholder-gray-300 hover:shadow-md focus:shadow-lg focus:scale-110"
            placeholder="•"
            required
            @input="handleInput(index, $event)"
            @keydown.backspace="handleBackspace(index, $event)"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="group relative w-full py-3.5 px-4 bg-gradient-to-r from-gray-900 to-gray-700 hover:from-gray-800 hover:to-gray-600 text-white font-semibold rounded-xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-gray-900/20 active:scale-[0.98] overflow-hidden"
        >
          <span class="relative flex items-center justify-center gap-2">
            <span>{{ $t('verification.verifyBtn') }}</span>
            <svg class="w-5 h-5 transform transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
            </svg>
          </span>
        </button>

        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Prop für die E-Mail (wird von außen übergeben, kein Hardcoding mehr)
defineProps({
  email: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['verify', 'resend'])

const code = ref(['', '', '', '', '', ''])
const inputRefs = ref([])
const timer = ref(29)
let interval = null

const formattedTime = computed(() => {
  const minutes = Math.floor(timer.value / 60)
  const seconds = timer.value % 60
  return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`
})

onMounted(() => {
  interval = setInterval(() => {
    if (timer.value > 0) {
      timer.value--
    } else {
      clearInterval(interval)
    }
  }, 1000)
})

const handleInput = (index, event) => {
  const value = event.target.value
  if (value && index < code.value.length - 1) {
    inputRefs.value[index + 1]?.focus()
  }
}

const handleBackspace = (index, event) => {
  if (!code.value[index] && index > 0) {
    inputRefs.value[index - 1]?.focus()
  }
}

const handleSubmit = () => {
  emit('verify', code.value.join(''))
}

const resendCode = () => {
  timer.value = 29
  emit('resend')
}
</script>