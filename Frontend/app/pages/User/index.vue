<template>
  <UserVerificationCode
    email="dein.kunde@domain.de" 
    @verify="onVerify" 
    @resend="onResend" 
  />
</template>

<script setup>
const onVerify = (code) => {
  console.log('Eingegebener Code:', code)
}
const onResend = () => {
  console.log('Code erneut angefordert')
}
</script>